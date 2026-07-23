pub mod nest;
pub mod pass;
pub mod omni;
pub mod storage;
pub mod trit;
pub mod wave;

#[derive(Debug, Eq, PartialEq)]
pub struct BuildReceipt {
    pub trit_glyphs: usize,
    pub coordinates: usize,
    pub nest_nodes: u64,
    pub nest_depth: u8,
    pub omni_stages: usize,
    pub storage_backends: usize,
    pub storage_roundtrips: usize,
    pub storage_file_roundtrips: usize,
}

pub fn verify() -> Result<BuildReceipt, String> {
    let trit = trit::verify()?;
    let nest = nest::verify()?;
    let omni = omni::verify()?;
    let _passes = pass::verify()?;
    let _wave_routes = wave::verify()?;
    let storage = storage::verify()?;
    Ok(BuildReceipt {
        trit_glyphs: trit.glyphs,
        coordinates: trit.coordinates,
        nest_nodes: nest.nodes_per_run,
        nest_depth: nest.depth,
        omni_stages: omni.stages,
        storage_backends: storage.backends,
        storage_roundtrips: storage.roundtrips,
        storage_file_roundtrips: storage.file_roundtrips,
    })
}