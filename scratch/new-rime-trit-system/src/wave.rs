use crate::trit::{RimeCoordinate, Trit};

pub const DEEP_WAVE_ROUTES: usize = 6 * 6 * 6 * 6 * 6 * 12;

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct WaveRoute { pub slot: usize, pub carrier: RimeCoordinate, pub pass: Trit }

pub fn route(slot: usize) -> WaveRoute {
    let slot = slot % DEEP_WAVE_ROUTES;
    let carrier = RimeCoordinate { space: Trit::ALL[(slot / 1) % 3], time: Trit::ALL[(slot / 3) % 3], color: Trit::ALL[(slot / 9) % 3] };
    let pass = Trit::ALL[(slot / 27) % 3];
    WaveRoute { slot, carrier, pass }
}

pub fn verify() -> Result<usize, String> {
    if DEEP_WAVE_ROUTES != 93_312 { return Err("deep wave route topology mismatch".into()); }
    let first = route(0); let last = route(DEEP_WAVE_ROUTES - 1);
    if first.slot != 0 || last.slot != DEEP_WAVE_ROUTES - 1 { return Err("wave route bounds failed".into()); }
    Ok(DEEP_WAVE_ROUTES)
}

#[cfg(test)]
mod tests { use super::*; #[test] fn deep_wave_is_route_topology_over_fixed_27_carrier() { assert_eq!(verify().unwrap(), 93_312); assert_eq!(route(0).carrier, RimeCoordinate { space:Trit::Negative, time:Trit::Negative, color:Trit::Negative }); } }