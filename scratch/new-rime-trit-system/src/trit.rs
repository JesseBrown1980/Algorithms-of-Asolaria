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
pub struct ColorGlyph { pub red: Trit, pub green: Trit, pub blue: Trit }

impl ColorGlyph {
    pub fn ordinal(self) -> u8 { self.red.code() * 9 + self.green.code() * 3 + self.blue.code() }
    pub fn rgb(self) -> [u8; 3] { [self.red.rgb(), self.green.rgb(), self.blue.rgb()] }
    pub fn all() -> Vec<ColorGlyph> {
        let mut out = Vec::with_capacity(27);
        for red in Trit::ALL { for green in Trit::ALL { for blue in Trit::ALL {
            out.push(ColorGlyph { red, green, blue });
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
pub struct TritStats { pub glyphs: usize, pub coordinates: usize }

pub fn verify() -> Result<TritStats, String> {
    let glyphs = ColorGlyph::all();
    let mut ordinals = [false; 27];
    let mut rgb = Vec::with_capacity(glyphs.len());
    for glyph in &glyphs {
        let ordinal = usize::from(glyph.ordinal());
        if ordinals[ordinal] || rgb.contains(&glyph.rgb()) { return Err(format!("glyph collision at {ordinal}")); }
        ordinals[ordinal] = true;
        rgb.push(glyph.rgb());
    }
    if !ordinals.iter().all(|seen| *seen) { return Err("missing trinary color glyph".into()); }
    let coordinates = RimeCoordinate::all();
    let mut seen = [false; 27];
    for coordinate in coordinates.iter().copied() {
        let ordinal = usize::from(coordinate.ordinal());
        if seen[ordinal] { return Err("RIME coordinate collision".into()); }
        seen[ordinal] = true;
    }
    if !seen.iter().all(|value| *value) { return Err("missing RIME coordinate".into()); }
    Ok(TritStats { glyphs: glyphs.len(), coordinates: coordinates.len() })
}

#[cfg(test)]
mod tests {
    use super::*;#[test] fn exactly_27_color_glyphs() { assert_eq!(verify().unwrap().glyphs, 27); }
    #[test] fn paths_are_variable_length_trit_addresses() {
        let mut path = RimePath::new(); path.push(Trit::Negative); path.push(Trit::Positive);
        assert_eq!(path.address(), "R.-.+"); assert_eq!(path.base3_code(), Some(2));
    }
}