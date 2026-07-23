pub mod nest;
pub mod pass;
pub mod omni;
pub mod storage;
pub mod trit;
pub mod wave;

#[derive(Debug, Eq, PartialEq)]
pub struct BuildReceipt {
    pub source_dimensions: usize,
    pub source_colors: usize,
    pub view_signatures: usize,
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
        source_dimensions: trit.source_dimensions,
        source_colors: trit.source_colors,
        view_signatures: trit.view_signatures,
        coordinates: trit.coordinates,
        nest_nodes: nest.nodes_per_run,
        nest_depth: nest.depth,
        omni_stages: omni.stages,
        storage_backends: storage.backends,
        storage_roundtrips: storage.roundtrips,
        storage_file_roundtrips: storage.file_roundtrips,
    })
}
