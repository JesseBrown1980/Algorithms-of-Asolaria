use std::fs;
use std::io::Write;
use std::path::Path;

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum BackendKind { Sgram, Local, Cloud }
#[derive(Debug, Eq, PartialEq)]
pub struct StorageStats { pub backends: usize, pub roundtrips: usize, pub payload_bytes: usize, pub file_roundtrips: usize }

pub fn write_local_file(path: &Path, key: &str, payload: &[u8]) -> std::io::Result<()> { fs::write(path, format!("LOCAL-SLICE|key={key}|payload_hex={}|json=0\n", hex(payload))) }
pub fn write_sgram_file(path: &Path, key: &str, payload: &[u8]) -> std::io::Result<()> { fs::write(path, format!("SGRAM-SLICE|key={key}|payload_hex={}|json=0\n", hex(payload))) }
pub fn write_cloud_manifest(path: &Path, key: &str, payload: &[u8]) -> std::io::Result<()> { fs::write(path, format!("CLOUD-MANIFEST|key={key}|payload_hex={}|json=0\n", hex(payload))) }
pub fn append_file_slice(path: &Path, prefix: &str, key: &str, payload: &[u8]) -> std::io::Result<()> {
    let mut file = fs::OpenOptions::new().create(true).append(true).open(path)?;
    writeln!(file, "{prefix}|key={key}|payload_hex={}|json=0", hex(payload))
}
pub fn read_file_slice(path: &Path, prefix: &str, key: &str) -> std::io::Result<Option<Vec<u8>>> {
    let text = fs::read_to_string(path)?; let wanted = format!("{prefix}|key={key}|payload_hex=");
    Ok(text.lines().rev().find_map(|line| { let value = line.strip_prefix(&wanted)?.strip_suffix("|json=0")?; decode_hex(value) }))
}
fn hex(payload: &[u8]) -> String { payload.iter().map(|byte| format!("{byte:02x}")).collect() }
fn decode_hex(value: &str) -> Option<Vec<u8>> { if value.len() % 2 != 0 { return None; } value.as_bytes().chunks_exact(2).map(|pair| u8::from_str_radix(std::str::from_utf8(pair).ok()?, 16).ok()).collect() }

trait SliceStore { fn write(&mut self, key: &str, payload: &[u8]); fn read(&self, key: &str) -> Option<Vec<u8>>; }
#[derive(Default)] struct LocalStore { rows: Vec<(String, Vec<u8>)> }
impl SliceStore for LocalStore { fn write(&mut self, key: &str, payload: &[u8]) { self.rows.push((key.to_string(), payload.to_vec())); } fn read(&self, key: &str) -> Option<Vec<u8>> { self.rows.iter().rev().find(|row| row.0 == key).map(|row| row.1.clone()) } }
#[derive(Default)] struct SgramStore { rows: Vec<String> }
impl SliceStore for SgramStore { fn write(&mut self, key: &str, payload: &[u8]) { self.rows.push(format!("SGRAM-SLICE|key={key}|payload_hex={}|json=0", hex(payload))); } fn read(&self, key: &str) -> Option<Vec<u8>> { let prefix = format!("SGRAM-SLICE|key={key}|payload_hex="); let row = self.rows.iter().rev().find(|row| row.starts_with(&prefix))?; decode_hex(row.strip_prefix(&prefix)?.strip_suffix("|json=0")?) } }
#[derive(Default)] struct CloudManifestStore { manifest: Vec<(String, Vec<u8>)> }
impl SliceStore for CloudManifestStore { fn write(&mut self, key: &str, payload: &[u8]) { self.manifest.push((key.to_string(), payload.to_vec())); } fn read(&self, key: &str) -> Option<Vec<u8>> { self.manifest.iter().rev().find(|row| row.0 == key).map(|row| row.1.clone()) } }

pub fn verify_file_backends() -> Result<usize, String> {
    let dir = std::env::temp_dir(); let key = "R.-.0.+"; let payload = b"RIME-GLYPH|space=-|time=0|color=+|json=0";
    let paths = [dir.join("rime-verify-local.hbp"), dir.join("rime-verify-sgram.hbp"), dir.join("rime-verify-cloud.manifest")];
    write_local_file(&paths[0], key, payload).map_err(|e| e.to_string())?;
    write_sgram_file(&paths[1], key, payload).map_err(|e| e.to_string())?;
    write_cloud_manifest(&paths[2], key, payload).map_err(|e| e.to_string())?;
    let checks = [("local", "LOCAL-SLICE"), ("sgram", "SGRAM-SLICE"), ("cloud", "CLOUD-MANIFEST")];
    for (path, (name, prefix)) in paths.iter().zip(checks) {
        if read_file_slice(path, prefix, key).map_err(|e| e.to_string())?.as_deref() != Some(payload) { return Err(format!("{name} file round-trip failed")); }
    }
    for path in paths { let _ = fs::remove_file(path); }
    Ok(3)
}
pub fn verify() -> Result<StorageStats, String> {
    let file_roundtrips = verify_file_backends()?;
    let key = "R.-.0.+"; let payload = b"RIME-GLYPH|space=-|time=0|color=+|json=0"; let mut local = LocalStore::default(); let mut sgram = SgramStore::default(); let mut cloud = CloudManifestStore::default(); local.write(key,payload); sgram.write(key,payload); cloud.write(key,payload);
    for (name,value) in [("local",local.read(key)),("sgram",sgram.read(key)),("cloud-manifest",cloud.read(key))] { if value.as_deref()!=Some(payload) { return Err(format!("{name} slice round-trip failed")); } }
    Ok(StorageStats { backends:3, roundtrips:3, payload_bytes:payload.len(), file_roundtrips })
}
#[cfg(test)] mod tests { use super::*; #[test] fn all_storage_adapters_round_trip_the_same_trit_slice() { assert_eq!(verify().unwrap(), StorageStats { backends:3, roundtrips:3, payload_bytes:40, file_roundtrips:3 }); } #[test] fn file_backends_round_trip() { let d=std::env::temp_dir(); let k="R.-.0.+"; let p=b"RIME-GLYPH|space=-|time=0|color=+|json=0"; let a=d.join("rime-local.hbp"); let b=d.join("rime-sgram.hbp"); let c=d.join("rime-cloud.manifest"); write_local_file(&a,k,p).unwrap(); write_sgram_file(&b,k,p).unwrap(); write_cloud_manifest(&c,k,p).unwrap(); append_file_slice(&a,"LOCAL-SLICE","R.-.0.-",b"older").unwrap(); append_file_slice(&b,"SGRAM-SLICE","R.-.0.-",b"older").unwrap(); append_file_slice(&c,"CLOUD-MANIFEST","R.-.0.-",b"older").unwrap(); assert_eq!(read_file_slice(&a,"LOCAL-SLICE",k).unwrap().as_deref(),Some(&p[..])); assert_eq!(read_file_slice(&b,"SGRAM-SLICE",k).unwrap().as_deref(),Some(&p[..])); assert_eq!(read_file_slice(&c,"CLOUD-MANIFEST",k).unwrap().as_deref(),Some(&p[..])); for x in [a,b,c] { let _=fs::remove_file(x); } } }