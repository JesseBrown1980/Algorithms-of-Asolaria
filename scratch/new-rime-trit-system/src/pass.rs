use crate::trit::{RimeCoordinate, Trit};

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct PassLedger {
    pub color: Trit,
    pub time: Trit,
    pub space: Trit,
    pub calculation_time: Trit,
    pub play_time: Trit,
    pub bits: Trit,
    pub storage_space: Trit,
}

impl PassLedger {
    pub fn all_center() -> Self { Self { color:Trit::Center, time:Trit::Center, space:Trit::Center, calculation_time:Trit::Center, play_time:Trit::Center, bits:Trit::Center, storage_space:Trit::Center } }
    pub fn trit_count(self) -> usize { [self.color,self.time,self.space,self.calculation_time,self.play_time,self.bits,self.storage_space].iter().filter(|x| **x != Trit::Center).count() }
    pub fn gravity_coupling(self) -> u128 { u128::from(self.trit_count() as u32) * 27 }
    pub fn nearest_third(value: u64, direction: Trit) -> u64 { match direction { Trit::Negative => value / 3, Trit::Center => value, Trit::Positive => value - value / 3 } }
}

pub fn verify() -> Result<usize, String> {
    let coordinates = RimeCoordinate::all();
    if coordinates.len() != 27 { return Err("pass coordinate set is not 27 trits".into()); }
    let ledger = PassLedger::all_center();
    if ledger.gravity_coupling() != 0 || PassLedger::nearest_third(9, Trit::Negative) != 3 || PassLedger::nearest_third(9, Trit::Positive) != 6 { return Err("trit pass arithmetic failed".into()); }
    Ok(coordinates.len())
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test] fn every_pass_uses_trits_and_27_coordinates() { assert_eq!(verify().unwrap(), 27); }
    #[test] fn nearest_third_is_integer_and_directional() { assert_eq!(PassLedger::nearest_third(10,Trit::Negative),3); assert_eq!(PassLedger::nearest_third(10,Trit::Center),10); assert_eq!(PassLedger::nearest_third(10,Trit::Positive),7); }
}