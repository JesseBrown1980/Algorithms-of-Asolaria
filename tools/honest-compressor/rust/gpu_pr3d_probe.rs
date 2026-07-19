//! Rust 1.81 / CUDA proof for the integer 2D opposed-marker + cube mapping.
//!
//! The full 3D sphere binding is unverified. Standalone: std only, no Cargo/nvcc,
//! no Node/V8, and no corpus access.  The CUDA kernel is integer-only PTX for
//! sm_61.  A run is evidence only when every CPU byte equals every GPU byte and
//! both device-buffer canaries remain intact.

use std::env;
use std::ffi::{CStr, CString};
use std::mem::size_of;
use std::os::raw::{c_char, c_int, c_uint, c_void};
use std::ptr;
use std::slice;
use std::time::Instant;

type CuDevice = c_int;
type CuContext = *mut c_void;
type CuModule = *mut c_void;
type CuFunction = *mut c_void;
type CuDevicePtr = u64;
type CuResult = c_int;

const CUDA_SUCCESS: CuResult = 0;
const OUTPUT_WORDS: usize = 16;
const GUARD_BYTES: usize = 64;
const MAX_RECORDS: usize = 1_048_576;
const MAX_DEVICE_BYTES: usize = 512 * 1024 * 1024;
const BLOCK_SIZE: u32 = 128;
const HEX_Q15: [(i32, i32); 6] = [
    (32768, 0),
    (16384, 28378),
    (-16384, 28378),
    (-32768, 0),
    (-16384, -28378),
    (16384, -28378),
];
const TRIAD_PRIMES: [usize; 2] = [2, 3];

#[link(name = "cuda")]
extern "C" {
    fn cuInit(flags: c_uint) -> CuResult;
    fn cuDriverGetVersion(version: *mut c_int) -> CuResult;
    fn cuDeviceGet(device: *mut CuDevice, ordinal: c_int) -> CuResult;
    fn cuDeviceGetName(name: *mut c_char, len: c_int, dev: CuDevice) -> CuResult;
    fn cuDeviceComputeCapability(
        major: *mut c_int,
        minor: *mut c_int,
        dev: CuDevice,
    ) -> CuResult;
    #[link_name = "cuCtxCreate_v2"]
    fn cuCtxCreate(ctx: *mut CuContext, flags: c_uint, dev: CuDevice) -> CuResult;
    #[link_name = "cuCtxDestroy_v2"]
    fn cuCtxDestroy(ctx: CuContext) -> CuResult;
    fn cuModuleLoadDataEx(
        module: *mut CuModule,
        image: *const c_void,
        num_options: c_uint,
        options: *mut c_int,
        option_values: *mut *mut c_void,
    ) -> CuResult;
    fn cuModuleUnload(module: CuModule) -> CuResult;
    fn cuModuleGetFunction(
        function: *mut CuFunction,
        module: CuModule,
        name: *const c_char,
    ) -> CuResult;
    #[link_name = "cuMemGetInfo_v2"]
    fn cuMemGetInfo(free: *mut usize, total: *mut usize) -> CuResult;
    #[link_name = "cuMemAlloc_v2"]
    fn cuMemAlloc(ptr: *mut CuDevicePtr, bytes: usize) -> CuResult;
    #[link_name = "cuMemFree_v2"]
    fn cuMemFree(ptr: CuDevicePtr) -> CuResult;
    #[link_name = "cuMemcpyHtoD_v2"]
    fn cuMemcpyHtoD(dst: CuDevicePtr, src: *const c_void, bytes: usize) -> CuResult;
    #[link_name = "cuMemcpyDtoH_v2"]
    fn cuMemcpyDtoH(dst: *mut c_void, src: CuDevicePtr, bytes: usize) -> CuResult;
    fn cuLaunchKernel(
        function: CuFunction,
        grid_x: c_uint,
        grid_y: c_uint,
        grid_z: c_uint,
        block_x: c_uint,
        block_y: c_uint,
        block_z: c_uint,
        shared_mem_bytes: c_uint,
        stream: *mut c_void,
        kernel_params: *mut *mut c_void,
        extra: *mut *mut c_void,
    ) -> CuResult;
    fn cuCtxSynchronize() -> CuResult;
    fn cuGetErrorName(error: CuResult, text: *mut *const c_char) -> CuResult;
    fn cuGetErrorString(error: CuResult, text: *mut *const c_char) -> CuResult;
}

fn cuda_error(code: CuResult, operation: &str) -> String {
    unsafe {
        let mut name = ptr::null();
        let mut detail = ptr::null();
        let _ = cuGetErrorName(code, &mut name);
        let _ = cuGetErrorString(code, &mut detail);
        let name = if name.is_null() {
            "CUDA_ERROR_UNKNOWN".into()
        } else {
            CStr::from_ptr(name).to_string_lossy().into_owned()
        };
        let detail = if detail.is_null() {
            "no driver detail".into()
        } else {
            CStr::from_ptr(detail).to_string_lossy().into_owned()
        };
        format!("{operation}: {name} ({code}): {detail}")
    }
}

fn cuda_check(code: CuResult, operation: &str) -> Result<(), String> {
    if code == CUDA_SUCCESS {
        Ok(())
    } else {
        Err(cuda_error(code, operation))
    }
}

struct Context(CuContext);
impl Drop for Context {
    fn drop(&mut self) {
        if !self.0.is_null() {
            unsafe {
                let _ = cuCtxDestroy(self.0);
            }
        }
    }
}

struct Module(CuModule);
impl Drop for Module {
    fn drop(&mut self) {
        if !self.0.is_null() {
            unsafe {
                let _ = cuModuleUnload(self.0);
            }
        }
    }
}

struct DeviceBuffer(CuDevicePtr);
impl Drop for DeviceBuffer {
    fn drop(&mut self) {
        if self.0 != 0 {
            unsafe {
                let _ = cuMemFree(self.0);
            }
        }
    }
}

#[repr(C)]
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
struct InputRecord {
    colors: [i32; 6],
    slice_id: u32,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
struct OmegaProjection {
    ports: [i32; 4],
    markers: [usize; 4],
    xy: [i32; 2],
}

fn duality_counts(n: usize) -> Option<(usize, usize)> {
    if n % 3 != 0 {
        return None;
    }
    Some((2 * (n / 3), 4 * (n / 3)))
}

fn omega_project(colors: [i32; 3], slice_id: usize, triad: usize) -> OmegaProjection {
    let prime = TRIAD_PRIMES[triad];
    let omit = (prime + slice_id) % 3;
    let mut selected = [0usize; 2];
    let mut cursor = 0usize;
    for index in 0..3 {
        if index != omit {
            selected[cursor] = index;
            cursor += 1;
        }
    }

    let sum = colors[0] + colors[1] + colors[2];
    let mean = sum.div_euclid(3);
    let parity = sum.rem_euclid(3);
    let q = [
        colors[0] - mean,
        colors[1] - mean,
        colors[2] - mean,
    ];
    let qa = q[selected[0]];
    let qb = q[selected[1]];
    let qo = parity - qa - qb;
    debug_assert_eq!(qo, q[omit]);

    let da = (qa - qo).div_euclid(2);
    let db = (qb - qo).div_euclid(2);
    let ports = [da, db, -da, -db];
    let pose = (prime * (slice_id + 1) + triad) % 6;
    let ia = (pose + 2 * selected[0]) % 6;
    let ib = (pose + 2 * selected[1]) % 6;
    let markers = [ia, ib, (ia + 3) % 6, (ib + 3) % 6];

    let mut accum = [0i64; 2];
    for index in 0..4 {
        accum[0] += ports[index] as i64 * HEX_Q15[markers[index]].0 as i64;
        accum[1] += ports[index] as i64 * HEX_Q15[markers[index]].1 as i64;
    }
    OmegaProjection {
        ports,
        markers,
        xy: [(accum[0] / 65536) as i32, (accum[1] / 65536) as i32],
    }
}

fn cube_faces(colors: [i32; 3], slice_id: usize, triad: usize) -> [i32; 6] {
    let sum = colors[0] + colors[1] + colors[2];
    let mean = sum.div_euclid(3);
    let q = [
        colors[0] - mean,
        colors[1] - mean,
        colors[2] - mean,
    ];
    let pose = (TRIAD_PRIMES[triad] * (slice_id + 1) + triad) % 6;
    let axis = pose % 3;
    let rotated = [q[axis], q[(axis + 1) % 3], q[(axis + 2) % 3]];
    [
        rotated[0],
        -rotated[0],
        rotated[1],
        -rotated[1],
        rotated[2],
        -rotated[2],
    ]
}

fn project_cpu(record: &InputRecord) -> [i32; OUTPUT_WORDS] {
    let mut out = [0i32; OUTPUT_WORDS];
    for triad in 0..2 {
        let base_in = triad * 3;
        let colors = [
            record.colors[base_in],
            record.colors[base_in + 1],
            record.colors[base_in + 2],
        ];
        let sphere = omega_project(colors, record.slice_id as usize, triad);
        let cube = cube_faces(colors, record.slice_id as usize, triad);
        let base_out = triad * 8;
        out[base_out] = sphere.xy[0];
        out[base_out + 1] = sphere.xy[1];
        out[base_out + 2..base_out + 8].copy_from_slice(&cube);
    }
    out
}

fn ptx_block(
    suffix: &str,
    color_offsets: [usize; 3],
    output_offset: usize,
    prime: usize,
    triad: usize,
) -> String {
    format!(
        r#"
    // PRIME_RULE_OF_THREE_DUALITY triad {triad}.
    ld.global.s32 %r30, [%rd4+{c0}];
    ld.global.s32 %r31, [%rd4+{c1}];
    ld.global.s32 %r32, [%rd4+{c2}];
    add.s32 %r33, %r30, %r31;
    add.s32 %r33, %r33, %r32;
    div.s32 %r34, %r33, 3;
    rem.s32 %r35, %r33, 3;
    setp.lt.s32 %p2, %r35, 0;
    @%p2 add.s32 %r34, %r34, -1;
    @%p2 add.s32 %r35, %r35, 3;
    sub.s32 %r36, %r30, %r34;
    sub.s32 %r37, %r31, %r34;
    sub.s32 %r38, %r32, %r34;

    add.u32 %r39, %r20, {prime};
    rem.u32 %r39, %r39, 3;
    setp.eq.u32 %p3, %r39, 0;
    @%p3 bra OMIT0_{suffix};
    setp.eq.u32 %p4, %r39, 1;
    @%p4 bra OMIT1_{suffix};
    bra OMIT2_{suffix};
OMIT0_{suffix}:
    mov.u32 %r40, 1;
    mov.u32 %r41, 2;
    mov.b32 %r42, %r37;
    mov.b32 %r43, %r38;
    mov.b32 %r44, %r36;
    bra SELECTED_{suffix};
OMIT1_{suffix}:
    mov.u32 %r40, 0;
    mov.u32 %r41, 2;
    mov.b32 %r42, %r36;
    mov.b32 %r43, %r38;
    mov.b32 %r44, %r37;
    bra SELECTED_{suffix};
OMIT2_{suffix}:
    mov.u32 %r40, 0;
    mov.u32 %r41, 1;
    mov.b32 %r42, %r36;
    mov.b32 %r43, %r37;
    mov.b32 %r44, %r38;
SELECTED_{suffix}:
    sub.s32 %r45, %r42, %r44;
    div.s32 %r46, %r45, 2;
    rem.s32 %r47, %r45, 2;
    setp.lt.s32 %p2, %r47, 0;
    @%p2 add.s32 %r46, %r46, -1;
    sub.s32 %r48, %r43, %r44;
    div.s32 %r49, %r48, 2;
    rem.s32 %r50, %r48, 2;
    setp.lt.s32 %p2, %r50, 0;
    @%p2 add.s32 %r49, %r49, -1;

    add.u32 %r51, %r20, 1;
    mul.lo.u32 %r51, %r51, {prime};
    add.u32 %r51, %r51, {triad};
    rem.u32 %r51, %r51, 6;
    mul.lo.u32 %r52, %r40, 2;
    add.u32 %r52, %r52, %r51;
    rem.u32 %r52, %r52, 6;
    mul.lo.u32 %r53, %r41, 2;
    add.u32 %r53, %r53, %r51;
    rem.u32 %r53, %r53, 6;

    mov.u64 %rd12, HEX_Q15;
    mul.wide.u32 %rd13, %r52, 8;
    add.s64 %rd14, %rd12, %rd13;
    ld.const.s32 %r56, [%rd14];
    ld.const.s32 %r57, [%rd14+4];
    mul.wide.u32 %rd13, %r53, 8;
    add.s64 %rd14, %rd12, %rd13;
    ld.const.s32 %r58, [%rd14];
    ld.const.s32 %r59, [%rd14+4];

    mul.wide.s32 %rd15, %r46, %r56;
    add.s64 %rd10, %rd15, %rd15;
    mul.wide.s32 %rd16, %r49, %r58;
    add.s64 %rd16, %rd16, %rd16;
    add.s64 %rd10, %rd10, %rd16;
    mul.wide.s32 %rd17, %r46, %r57;
    add.s64 %rd11, %rd17, %rd17;
    mul.wide.s32 %rd18, %r49, %r59;
    add.s64 %rd18, %rd18, %rd18;
    add.s64 %rd11, %rd11, %rd18;
    div.s64 %rd20, %rd10, 65536;
    div.s64 %rd21, %rd11, 65536;
    cvt.s32.s64 %r60, %rd20;
    cvt.s32.s64 %r61, %rd21;
    st.global.s32 [%rd6+{o0}], %r60;
    st.global.s32 [%rd6+{o1}], %r61;

    rem.u32 %r62, %r51, 3;
    setp.eq.u32 %p5, %r62, 0;
    @%p5 bra AXIS0_{suffix};
    setp.eq.u32 %p6, %r62, 1;
    @%p6 bra AXIS1_{suffix};
    bra AXIS2_{suffix};
AXIS0_{suffix}:
    mov.b32 %r63, %r36;
    mov.b32 %r64, %r37;
    mov.b32 %r65, %r38;
    bra AXIS_READY_{suffix};
AXIS1_{suffix}:
    mov.b32 %r63, %r37;
    mov.b32 %r64, %r38;
    mov.b32 %r65, %r36;
    bra AXIS_READY_{suffix};
AXIS2_{suffix}:
    mov.b32 %r63, %r38;
    mov.b32 %r64, %r36;
    mov.b32 %r65, %r37;
AXIS_READY_{suffix}:
    neg.s32 %r66, %r63;
    neg.s32 %r67, %r64;
    neg.s32 %r68, %r65;
    st.global.s32 [%rd6+{o2}], %r63;
    st.global.s32 [%rd6+{o3}], %r66;
    st.global.s32 [%rd6+{o4}], %r64;
    st.global.s32 [%rd6+{o5}], %r67;
    st.global.s32 [%rd6+{o6}], %r65;
    st.global.s32 [%rd6+{o7}], %r68;
"#,
        suffix = suffix,
        triad = triad,
        prime = prime,
        c0 = color_offsets[0],
        c1 = color_offsets[1],
        c2 = color_offsets[2],
        o0 = output_offset,
        o1 = output_offset + 4,
        o2 = output_offset + 8,
        o3 = output_offset + 12,
        o4 = output_offset + 16,
        o5 = output_offset + 20,
        o6 = output_offset + 24,
        o7 = output_offset + 28,
    )
}

fn build_ptx() -> String {
    let block_a = ptx_block("A", [0, 4, 8], 0, 2, 0);
    let block_b = ptx_block("B", [12, 16, 20], 32, 3, 1);
    format!(
        r#".version 6.4
.target sm_61
.address_size 64

.const .align 8 .s32 HEX_Q15[12] = {{
    32768, 0, 16384, 28378, -16384, 28378,
    -32768, 0, -16384, -28378, 16384, -28378
}};

.visible .entry project_records(
    .param .u64 input_ptr,
    .param .u64 output_ptr,
    .param .u32 record_count
)
{{
    .reg .pred %p<16>;
    .reg .b32 %r<96>;
    .reg .b64 %rd<32>;

    ld.param.u64 %rd1, [input_ptr];
    ld.param.u64 %rd2, [output_ptr];
    ld.param.u32 %r1, [record_count];
    mov.u32 %r2, %ctaid.x;
    mov.u32 %r3, %ntid.x;
    mov.u32 %r4, %tid.x;
    mad.lo.u32 %r5, %r2, %r3, %r4;
    setp.ge.u32 %p1, %r5, %r1;
    @%p1 bra DONE;
    mul.wide.u32 %rd3, %r5, 28;
    add.s64 %rd4, %rd1, %rd3;
    mul.wide.u32 %rd5, %r5, 64;
    add.s64 %rd6, %rd2, %rd5;
    ld.global.u32 %r20, [%rd4+24];
{block_a}
{block_b}
DONE:
    ret;
}}
"#,
        block_a = block_a,
        block_b = block_b
    )
}

fn records_as_bytes(records: &[InputRecord]) -> &[u8] {
    unsafe {
        slice::from_raw_parts(
            records.as_ptr() as *const u8,
            records.len() * size_of::<InputRecord>(),
        )
    }
}

fn words_as_bytes(words: &[i32]) -> &[u8] {
    unsafe {
        slice::from_raw_parts(words.as_ptr() as *const u8, std::mem::size_of_val(words))
    }
}

fn guarded(payload: &[u8], guard: u8, payload_fill: Option<u8>) -> Vec<u8> {
    let mut bytes = vec![guard; GUARD_BYTES + payload.len() + GUARD_BYTES];
    if let Some(fill) = payload_fill {
        bytes[GUARD_BYTES..GUARD_BYTES + payload.len()].fill(fill);
    } else {
        bytes[GUARD_BYTES..GUARD_BYTES + payload.len()].copy_from_slice(payload);
    }
    bytes
}

fn canaries_ok(bytes: &[u8], payload_len: usize, guard: u8) -> bool {
    bytes[..GUARD_BYTES].iter().all(|byte| *byte == guard)
        && bytes[GUARD_BYTES + payload_len..]
            .iter()
            .all(|byte| *byte == guard)
}

fn fnv1a64(bytes: &[u8]) -> u64 {
    let mut hash = 0xcbf29ce484222325u64;
    for byte in bytes {
        hash ^= *byte as u64;
        hash = hash.wrapping_mul(0x100000001b3);
    }
    hash
}

struct Rng(u64);
impl Rng {
    fn next_u32(&mut self) -> u32 {
        let mut x = self.0;
        x ^= x >> 12;
        x ^= x << 25;
        x ^= x >> 27;
        self.0 = x;
        (x.wrapping_mul(0x2545f4914f6cdd1d) >> 32) as u32
    }
}

fn make_records(count: usize, seed: u64) -> Vec<InputRecord> {
    let mut rng = Rng(if seed == 0 { 0x6a09e667f3bcc909 } else { seed });
    (0..count)
        .map(|_| {
            let mut colors = [0i32; 6];
            for color in &mut colors {
                *color = (rng.next_u32() % 4095) as i32 - 2047;
            }
            InputRecord {
                colors,
                slice_id: rng.next_u32() % 1_000_000,
            }
        })
        .collect()
}

fn device_alloc(bytes: usize) -> Result<DeviceBuffer, String> {
    let mut ptr = 0;
    unsafe {
        cuda_check(cuMemAlloc(&mut ptr, bytes), "cuMemAlloc")?;
    }
    Ok(DeviceBuffer(ptr))
}

fn run(records: usize, seed: u64) -> Result<String, String> {
    if records == 0 || records > MAX_RECORDS {
        return Err(format!("records_out_of_range:{records}:max={MAX_RECORDS}"));
    }
    let (selected, gradient_views) =
        duality_counts(6).ok_or_else(|| "duality_count_preflight_failed".to_string())?;
    if (selected, gradient_views) != (4, 8) {
        return Err(format!(
            "duality_count_mismatch:selected={selected}:views={gradient_views}"
        ));
    }
    if size_of::<InputRecord>() != 28 {
        return Err(format!(
            "input_layout_mismatch:{}:expected=28",
            size_of::<InputRecord>()
        ));
    }

    unsafe {
        cuda_check(cuInit(0), "cuInit")?;
    }
    let mut driver_version = 0;
    unsafe {
        cuda_check(
            cuDriverGetVersion(&mut driver_version),
            "cuDriverGetVersion",
        )?;
    }
    let mut device = 0;
    unsafe {
        cuda_check(cuDeviceGet(&mut device, 0), "cuDeviceGet")?;
    }
    let mut major = 0;
    let mut minor = 0;
    unsafe {
        cuda_check(
            cuDeviceComputeCapability(&mut major, &mut minor, device),
            "cuDeviceComputeCapability",
        )?;
    }
    if major < 6 || (major == 6 && minor < 1) {
        return Err(format!("compute_capability_hold:{major}.{minor}:need>=6.1"));
    }
    let mut name_buf = [0 as c_char; 128];
    unsafe {
        cuda_check(
            cuDeviceGetName(name_buf.as_mut_ptr(), name_buf.len() as c_int, device),
            "cuDeviceGetName",
        )?;
    }
    let device_name = unsafe { CStr::from_ptr(name_buf.as_ptr()) }
        .to_string_lossy()
        .replace('|', "_");

    let mut raw_context = ptr::null_mut();
    unsafe {
        cuda_check(cuCtxCreate(&mut raw_context, 0, device), "cuCtxCreate")?;
    }
    let _context = Context(raw_context);

    let mut free_bytes = 0usize;
    let mut total_bytes = 0usize;
    unsafe {
        cuda_check(
            cuMemGetInfo(&mut free_bytes, &mut total_bytes),
            "cuMemGetInfo",
        )?;
    }

    let input_records = make_records(records, seed);
    let input_payload = records_as_bytes(&input_records);
    let mut expected_words = Vec::with_capacity(records * OUTPUT_WORDS);
    for record in &input_records {
        expected_words.extend_from_slice(&project_cpu(record));
    }
    let expected_payload = words_as_bytes(&expected_words);
    let input_host = guarded(input_payload, 0xa5, None);
    let output_initial = guarded(expected_payload, 0x5a, Some(0xcd));
    let device_bytes = input_host
        .len()
        .checked_add(output_initial.len())
        .ok_or_else(|| "allocation_overflow".to_string())?;
    let quarter_free = free_bytes / 4;
    if device_bytes > MAX_DEVICE_BYTES || device_bytes > quarter_free {
        return Err(format!(
            "allocation_hold:requested={device_bytes}:max={MAX_DEVICE_BYTES}:quarter_free={quarter_free}"
        ));
    }

    let ptx = CString::new(build_ptx()).map_err(|_| "ptx_contains_nul".to_string())?;
    let mut raw_module = ptr::null_mut();
    unsafe {
        cuda_check(
            cuModuleLoadDataEx(
                &mut raw_module,
                ptx.as_ptr() as *const c_void,
                0,
                ptr::null_mut(),
                ptr::null_mut(),
            ),
            "cuModuleLoadDataEx",
        )?;
    }
    let _module = Module(raw_module);
    let kernel_name = CString::new("project_records").unwrap();
    let mut function = ptr::null_mut();
    unsafe {
        cuda_check(
            cuModuleGetFunction(&mut function, raw_module, kernel_name.as_ptr()),
            "cuModuleGetFunction",
        )?;
    }

    let input_device = device_alloc(input_host.len())?;
    let output_device = device_alloc(output_initial.len())?;
    unsafe {
        cuda_check(
            cuMemcpyHtoD(
                input_device.0,
                input_host.as_ptr() as *const c_void,
                input_host.len(),
            ),
            "cuMemcpyHtoD(input)",
        )?;
        cuda_check(
            cuMemcpyHtoD(
                output_device.0,
                output_initial.as_ptr() as *const c_void,
                output_initial.len(),
            ),
            "cuMemcpyHtoD(output)",
        )?;
    }

    let mut input_payload_ptr = input_device.0 + GUARD_BYTES as u64;
    let mut output_payload_ptr = output_device.0 + GUARD_BYTES as u64;
    let mut count_u32 = records as u32;
    let mut params = [
        &mut input_payload_ptr as *mut CuDevicePtr as *mut c_void,
        &mut output_payload_ptr as *mut CuDevicePtr as *mut c_void,
        &mut count_u32 as *mut u32 as *mut c_void,
    ];
    let grid = (count_u32 + BLOCK_SIZE - 1) / BLOCK_SIZE;
    let started = Instant::now();
    unsafe {
        cuda_check(
            cuLaunchKernel(
                function,
                grid,
                1,
                1,
                BLOCK_SIZE,
                1,
                1,
                0,
                ptr::null_mut(),
                params.as_mut_ptr(),
                ptr::null_mut(),
            ),
            "cuLaunchKernel",
        )?;
        cuda_check(cuCtxSynchronize(), "cuCtxSynchronize")?;
    }
    let elapsed_us = started.elapsed().as_micros();

    let mut input_after = vec![0u8; input_host.len()];
    let mut output_after = vec![0u8; output_initial.len()];
    unsafe {
        cuda_check(
            cuMemcpyDtoH(
                input_after.as_mut_ptr() as *mut c_void,
                input_device.0,
                input_after.len(),
            ),
            "cuMemcpyDtoH(input)",
        )?;
        cuda_check(
            cuMemcpyDtoH(
                output_after.as_mut_ptr() as *mut c_void,
                output_device.0,
                output_after.len(),
            ),
            "cuMemcpyDtoH(output)",
        )?;
    }

    let input_canary = canaries_ok(&input_after, input_payload.len(), 0xa5);
    let output_canary = canaries_ok(&output_after, expected_payload.len(), 0x5a);
    let input_unchanged = input_after == input_host;
    let actual_payload =
        &output_after[GUARD_BYTES..GUARD_BYTES + expected_payload.len()];
    if !input_canary || !output_canary || !input_unchanged {
        return Err(format!(
            "canary_hold:input={}:output={}:input_unchanged={}",
            input_canary as u8, output_canary as u8, input_unchanged as u8
        ));
    }
    if actual_payload != expected_payload {
        let mismatch = actual_payload
            .iter()
            .zip(expected_payload.iter())
            .position(|(actual, expected)| actual != expected)
            .unwrap_or(usize::MAX);
        return Err(format!("cpu_gpu_mismatch:byte={mismatch}"));
    }

    Ok(format!(
        "GPUPR3D|status=PASS|records={records}|seed={seed}|sectors=6|selected={selected}|gradient_views={gradient_views}|device={device_name}|cc={major}.{minor}|driver={driver_version}|input_bytes={}|output_bytes={}|device_alloc_bytes={device_bytes}|free_before={free_bytes}|total_vram={total_bytes}|cpu_gpu_parity=1|input_canary=1|output_canary=1|output_fnv64={:016x}|elapsed_us={elapsed_us}|json=0",
        input_payload.len(),
        expected_payload.len(),
        fnv1a64(actual_payload)
    ))
}

fn parse_args() -> Result<(usize, u64), String> {
    let mut records = 1usize;
    let mut seed = 1_784_482_902u64;
    let args: Vec<String> = env::args().collect();
    let mut index = 1usize;
    while index < args.len() {
        match args[index].as_str() {
            "--records" => {
                index += 1;
                records = args
                    .get(index)
                    .ok_or_else(|| "missing_records_value".to_string())?
                    .parse()
                    .map_err(|_| "invalid_records_value".to_string())?;
            }
            "--seed" => {
                index += 1;
                seed = args
                    .get(index)
                    .ok_or_else(|| "missing_seed_value".to_string())?
                    .parse()
                    .map_err(|_| "invalid_seed_value".to_string())?;
            }
            "--help" | "-h" => {
                println!(
                    "usage: gpu_pr3d_probe [--records N] [--seed N]\nfirst warm-up rung: --records 1"
                );
                std::process::exit(0);
            }
            other => return Err(format!("unknown_argument:{other}")),
        }
        index += 1;
    }
    Ok((records, seed))
}

fn clean_reason(reason: &str) -> String {
    reason
        .chars()
        .map(|character| {
            if character == '|' || character == '\r' || character == '\n' {
                '_'
            } else {
                character
            }
        })
        .collect()
}

fn main() {
    let result = parse_args().and_then(|(records, seed)| run(records, seed));
    match result {
        Ok(receipt) => println!("{receipt}"),
        Err(reason) => {
            eprintln!(
                "GPUPR3D|status=HOLD|reason={}|json=0",
                clean_reason(&reason)
            );
            std::process::exit(2);
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn input_layout_is_stable() {
        assert_eq!(size_of::<InputRecord>(), 28);
        assert_eq!(OUTPUT_WORDS, 16);
    }

    #[test]
    fn duality_counts_match_the_operator_rule() {
        assert_eq!(duality_counts(3), Some((2, 4)));
        assert_eq!(duality_counts(6), Some((4, 8)));
        assert_eq!(duality_counts(12), Some((8, 16)));
        assert_eq!(duality_counts(24), Some((16, 32)));
        assert_eq!(duality_counts(5), None);
    }

    #[test]
    fn opposed_marker_ports_are_inverse_pairs() {
        for slice_id in 0..24 {
            for triad in 0..2 {
                let projection = omega_project([-2047, 17, 2030], slice_id, triad);
                assert_eq!(projection.ports[2], -projection.ports[0]);
                assert_eq!(projection.ports[3], -projection.ports[1]);
                assert_eq!(projection.markers[2], (projection.markers[0] + 3) % 6);
                assert_eq!(projection.markers[3], (projection.markers[1] + 3) % 6);
            }
        }
    }

    #[test]
    fn cube_faces_are_normal_inverse_pairs() {
        for slice_id in 0..24 {
            for triad in 0..2 {
                let faces = cube_faces([-2047, 17, 2030], slice_id, triad);
                assert_eq!(faces[1], -faces[0]);
                assert_eq!(faces[3], -faces[2]);
                assert_eq!(faces[5], -faces[4]);
            }
        }
    }

    #[test]
    fn negative_euclidean_division_fixture_matches_expected_vector() {
        let record = InputRecord {
            colors: [-2047, -1, 2047, 2039, -2033, -17],
            slice_id: 37,
        };
        assert_eq!(
            project_cpu(&record),
            [
                0, 1772, 0, 0, 2048, -2048, -2046, 2046,
                1522, 890, -2029, 2029, -13, 13, 2043, -2043,
            ]
        );
    }

    #[test]
    fn embedded_ptx_contains_both_triads_and_sm61_target() {
        let ptx = build_ptx();
        assert!(ptx.contains(".target sm_61"));
        assert!(ptx.contains("OMIT0_A"));
        assert!(ptx.contains("OMIT0_B"));
        assert!(ptx.contains("project_records"));
    }
}
