use crate::trit::{RimePath, Trit};

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum GateState { Negative, Center, Positive }

impl GateState {
    fn compare(reported: Trit, recomputed: Trit) -> Self {
        if reported == recomputed { GateState::Positive } else { GateState::Negative }
    }
}

#[derive(Debug)]
struct Node { truth: Trit, reported: Trit, gate: GateState, subtree_ok: bool, failures: Vec<String> }

#[derive(Debug, Eq, PartialEq)]
pub struct NestStats { pub depth: u8, pub nodes_per_run: u64, pub tamper_levels: u8 }

fn truth(path: &RimePath, children: &[Node]) -> Trit {
    let mut total = path.0.len() as u64;
    for (index, child) in children.iter().enumerate() { total += u64::from(child.truth.code()) * (index as u64 + 1); }
    Trit::ALL[(total % 3) as usize]
}

fn node(path: &mut RimePath, depth: u8, max_depth: u8, tamper_depth: Option<u8>, count: &mut u64) -> Node {
    *count += 1;
    let mut children = Vec::new();
    if depth < max_depth {
        for trit in Trit::ALL { path.push(trit); children.push(node(path, depth + 1, max_depth, tamper_depth, count)); path.pop(); }
    }
    let recomputed = truth(path, &children);
    let planted = tamper_depth == Some(depth) && path.0.iter().all(|trit| *trit == Trit::Negative);
    let reported = if planted { if recomputed == Trit::Center { Trit::Positive } else { recomputed.invert() } } else { recomputed };
    let gate = GateState::compare(reported, recomputed);
    let mut failures = Vec::new();
    if gate == GateState::Negative { failures.push(path.address()); }
    for child in &children { failures.extend(child.failures.iter().cloned()); }
    let subtree_ok = gate == GateState::Positive && children.iter().all(|child| child.subtree_ok);
    Node { truth: recomputed, reported, gate, subtree_ok, failures }
}

fn run(depth: u8, tamper_depth: Option<u8>) -> (Node, u64) {
    let mut path = RimePath::new(); let mut count = 0; let root = node(&mut path, 0, depth, tamper_depth, &mut count); (root, count)
}

pub fn scaling_state(subtree_ok: bool, operator_consent: bool) -> GateState {
    if !operator_consent { GateState::Center } else if subtree_ok { GateState::Positive } else { GateState::Negative }
}

pub fn verify() -> Result<NestStats, String> {
    let depth = 7u8;
    let expected = (3u64.pow(u32::from(depth) + 1) - 1) / 2;
    let (clean, count) = run(depth, None);
    if count != expected || !clean.subtree_ok || clean.gate != GateState::Positive || clean.truth != clean.reported || scaling_state(true, false) != GateState::Center || scaling_state(true, true) != GateState::Positive { return Err(format!("clean nest failed: {clean:?}")); }
    for level in 1..=depth {
        let (tampered, count) = run(depth, Some(level));
        let expected_path = format!("R{}", ".-".repeat(level as usize));
        if count != expected || tampered.subtree_ok || tampered.failures != vec![expected_path.clone()] || scaling_state(false, true) != GateState::Negative { return Err(format!("tamper missed at {level}: {:?}", tampered.failures)); }
    }
    Ok(NestStats { depth, nodes_per_run: expected, tamper_levels: depth })
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test] fn watcher_catches_every_prime_depth() { let stats = verify().unwrap(); assert_eq!(stats.nodes_per_run, 3280); assert_eq!(stats.tamper_levels, 7); }
    #[test] fn consent_is_center_until_operator_supplies_it() { assert_eq!(scaling_state(true, false), GateState::Center); assert_eq!(scaling_state(true, true), GateState::Positive); }
}