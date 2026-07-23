#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum Trit { Negative, Center, Positive }

impl Trit {
    pub const ALL: [Trit; 3] = [Trit::Negative, Trit::Center, Trit::Positive];
    pub fn code(self) -> u8 { match self { Trit::Negative => 0, Trit::Center => 1, Trit::Positive => 2 } }
    pub fn glyph(self) -> char { match self { Trit::Negative => '-', Trit::Center => '0', Trit::Positive => '+' } }
    pub fn rgb(self) -> u8 { match self { Trit::Negative => 0, Trit::Center => 127, Trit::Positive => 255 } }
    pub fn invert(self) -> Trit { match self { Trit::Negative => Trit::Positive, Trit::Center => Trit::Center, Trit::Positive => Trit::Negative } }
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum SourceColorSlot { First, Second }

impl SourceColorSlot {
    pub const ALL: [SourceColorSlot; 2] = [SourceColorSlot::First, SourceColorSlot::Second];
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct FlashMirrorSignature { pub red: Trit, pub blue: Trit, pub green: Trit }

impl FlashMirrorSignature {
    pub fn ordinal(self) -> u8 { self.red.code() * 9 + self.blue.code() * 3 + self.green.code() }
    pub fn display_rgb(self) -> [u8; 3] { [self.red.rgb(), self.green.rgb(), self.blue.rgb()] }
    pub fn mirror_paths(self) -> [u8; 3] { [self.red.code() + 1, self.blue.code() + 1, self.green.code() + 1] }
    pub fn all() -> Vec<FlashMirrorSignature> {
        let mut out = Vec::with_capacity(27);
        for red in Trit::ALL { for blue in Trit::ALL { for green in Trit::ALL {
            out.push(FlashMirrorSignature { red, blue, green });
        }}}
        out
    }
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct RimePath(pub Vec<Trit>);

impl RimePath {
    pub fn new() -> Self { Self(Vec::new()) }
    pub fn push(&mut self, trit: Trit) { self.0.push(trit); }
    pub fn pop(&mut self) { self.0.pop(); }
    pub fn address(&self) -> String {
        let mut out = String::from("R");
        for trit in &self.0 { out.push('.'); out.push(trit.glyph()); }
        out
    }
    pub fn base3_code(&self) -> Option<u128> {
        let mut code = 0u128;
        for trit in &self.0 { code = code.checked_mul(3)?.checked_add(u128::from(trit.code()))?; }
        Some(code)
    }
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct RimeCoordinate { pub space: Trit, pub time: Trit, pub color: Trit }

impl RimeCoordinate {
    pub fn ordinal(self) -> u8 { self.space.code() * 9 + self.time.code() * 3 + self.color.code() }
    pub fn all() -> Vec<Self> {
        let mut out = Vec::with_capacity(27);
        for space in Trit::ALL { for time in Trit::ALL { for color in Trit::ALL {
            out.push(Self { space, time, color });
        }}}
        out
    }
}

#[derive(Debug, Eq, PartialEq)]
pub struct TritStats {
    pub source_dimensions: usize,
    pub source_colors: usize,
    pub view_signatures: usize,
    pub coordinates: usize,
}

pub fn verify() -> Result<TritStats, String> {
    let source_colors = SourceColorSlot::ALL;
    if source_colors.len() != 2 { return Err("2D source must start with exactly two color slots".into()); }
    let signatures = FlashMirrorSignature::all();
    let mut ordinals = [false; 27];
    let mut projections = Vec::with_capacity(signatures.len());
    for signature in &signatures {
        let ordinal = usize::from(signature.ordinal());
        if ordinals[ordinal] || projections.contains(&signature.display_rgb()) {
            return Err(format!("flash/mirror signature collision at {ordinal}"));
        }
        ordinals[ordinal] = true;
        projections.push(signature.display_rgb());
        if signature.mirror_paths().iter().any(|path| !(1..=3).contains(path)) {
            return Err("mirror path left the 1/2/3 gate".into());
        }
    }
    if !ordinals.iter().all(|seen| *seen) { return Err("missing RGB flashlight/mirror signature".into()); }
    let coordinates = RimeCoordinate::all();
    let mut seen = [false; 27];
    for coordinate in coordinates.iter().copied() {
        let ordinal = usize::from(coordinate.ordinal());
        if seen[ordinal] { return Err("RIME coordinate collision".into()); }
        seen[ordinal] = true;
    }
    if !seen.iter().all(|value| *value) { return Err("missing RIME coordinate".into()); }
    Ok(TritStats {
        source_dimensions: 2,
        source_colors: source_colors.len(),
        view_signatures: signatures.len(),
        coordinates: coordinates.len(),
    })
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test] fn two_color_2d_source_produces_27_probe_signatures() {
        let stats = verify().unwrap();
        assert_eq!((stats.source_dimensions, stats.source_colors), (2, 2));
        assert_eq!(stats.view_signatures, 27);
    }
    #[test] fn every_flashlight_uses_one_two_or_three_mirrors() {
        assert!(FlashMirrorSignature::all().iter().all(|signature| {
            signature.mirror_paths().iter().all(|path| (1..=3).contains(path))
        }));
    }
    #[test] fn paths_are_variable_length_trit_addresses() {
        let mut path = RimePath::new(); path.push(Trit::Negative); path.push(Trit::Positive);
        assert_eq!(path.address(), "R.-.+"); assert_eq!(path.base3_code(), Some(2));
    }
}
