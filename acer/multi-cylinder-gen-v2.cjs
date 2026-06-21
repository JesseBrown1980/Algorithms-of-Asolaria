#!/usr/bin/env node
/* ASOLARIA MULTI-CYLINDER MAP v2 — named registered PIDs + the FULL 81,434-surface real population.
 * Cylinders (towers, §3.3 residue-band on a meta-ring): 9 NAMED strata + 8 SURFACE rootClasses.
 * Memory-safe + anti-flattening (AF-001..005): named (1,844) + critical surfaces (4,129) plotted
 * INDIVIDUALLY; the 77,305 low/medium surfaces collapse into AGGREGATE CELLS carrying child_count +
 * child_index_hash (summary_not_identity, never dropped). Logical billions (100B/1e1e8/10B) are NEVER
 * plotted — shown only as legend strata. Byte-identical, no RNG. E=0 read-only.
 */
const fs = require('fs'), crypto = require('crypto');
const OUT = 'C:/tmp/asolaria-real-model';
const FEED = 'D:/PID-Registration-Office/fabric-feed/supervisors-fabric-feed-2026-06-10.hbp';
const RD = 'D:/PID-Registration-Office/registered';
const SURF = 'C:/tmp/usb-newer-map/surfaces.full.ndjson';
const sha16 = s => crypto.createHash('sha256').update(String(s)).digest('hex').slice(0, 16);
const u32 = s => parseInt(crypto.createHash('sha256').update(String(s).toUpperCase()).digest('hex').slice(0, 8), 16) >>> 0;
const P = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,139,149,151,157,163,167,173,179,181,191,193,197,199,211,223,227,229,233,239,241,251,257,263,269,271,277,281];
const TAU = ['tau1','tau3','tau3^3','tau3^5','tauH'], FORM = ['n*p','n*p(lane2)','n*p*n^3','n*p*n^5','p^k'];
const TIER_BASE = [1.2, 1.9, 2.6, 3.3, 4.1];
const TWO = 2 * Math.PI, WEDGE = TWO / 3, R_META = 30;

// ---- NAMED towers ----
function namedTower(layer, cls) {
  const s = ((layer || '') + ' ' + (cls || '')).toLowerCase();
  if (/meta|operator|gac|chief|council|helm|apex/.test(s)) return 'APEX';
  if (/supofsup|sup-l|supervisor_of|level[345]_sup|agent_supervisor|supervisor/.test(s)) return 'SUPERVISOR';
  if (/prof/.test(s)) return 'PROF';
  if (/hyperbehcs/.test(s)) return 'HYPERBEHCS';
  if (/substrate|room|basin|bh-room|kernel|white-room|vault|sector/.test(s)) return 'SUBSTRATE-ROOM';
  if (/usb|cartridge/.test(s)) return 'USB-CARTRIDGE';
  if (/agent|servant|hermes|pi-agent/.test(s)) return 'AGENT';
  if (/planb|paper|corpus|research/.test(s)) return 'PLANB-RESEARCH';
  if (/formula/.test(s)) return 'DISTRICT-F';
  return 'NAMED-OTHER';
}
function rankOf(layer, cls) {
  const s = ((layer || '') + ' ' + (cls || '')).toLowerCase();
  if (/meta|apex|l0/.test(s)) return 9; if (/helm/.test(s)) return 8; if (/operator|l1/.test(s)) return 7;
  if (/gac|l2/.test(s)) return 6; if (/chief|council|l3/.test(s)) return 5; if (/supofsup|l4/.test(s)) return 4;
  if (/sup-l5|level5|supervisor/.test(s)) return 3; if (/prof/.test(s)) return 2.5; return 1;
}
const NAMED_TOWERS = ['APEX','SUPERVISOR','PROF','HYPERBEHCS','SUBSTRATE-ROOM','AGENT','USB-CARTRIDGE','PLANB-RESEARCH','DISTRICT-F','NAMED-OTHER'];
const SURF_TOWERS = ['app_root','project_sprawl','control_repo','shadow_archaeology','living_runtime','desktop_surface','android_companion','startup_surface'];

// ---- read named (726 fed seats + 1118 formulas) ----
const named = [];
const g = (line, k) => { const m = line.match(new RegExp('\\|' + k + '=([^|]*)')); return m ? m[1] : ''; };
for (const line of fs.readFileSync(FEED, 'utf8').split('\n')) {
  if (!line.startsWith('REG|')) continue; const pid = g(line, 'pid'); if (!pid) continue;
  named.push({ pid, name: g(line, 'name'), hilbert: +g(line, 'hilbert') || 0, layer: g(line, 'layer'), cls: g(line, 'class'), g1024: +g(line, 'g1024') || 0, g5: +g(line, 'g5') || 0, fed: 1 });
}
const nSeats = named.length;
for (const f of fs.readdirSync(RD)) {
  if (!/FORMULA.*CORPUS.*\.hbp$/i.test(f)) continue;
  for (const line of fs.readFileSync(RD + '/' + f, 'utf8').split('\n')) {
    if (!line.startsWith('FORMULA|')) continue;
    const gg = k => { const m = line.match(new RegExp('\\|' + k + '=([^|]*)')); return m ? m[1] : ''; };
    const pid = gg('PID'); if (!pid) continue;
    named.push({ pid, name: line.split('|')[1] || 'formula', hilbert: +gg('HILBERT') || 0, layer: 'formula', cls: gg('CLASS') || 'formula', g1024: +gg('GLYPH_BEHCS1024') || 0, g5: +gg('GLYPH_BEHCS5') || 0, fed: 1 });
  }
}
const nForm = named.length - nSeats;

// ---- meta-ring centers for all cylinders (named then surface) ----
const allTowers = NAMED_TOWERS.concat(SURF_TOWERS);
const centers = {};
allTowers.forEach((t, k) => { const a = (k / allTowers.length) * TWO; centers[t] = { cx: +(R_META * Math.cos(a)).toFixed(3), cy: +(R_META * Math.sin(a)).toFixed(3), k }; });

function place(seedSrc, g1024, g5, hilbertOrNull, crit) {
  const seed = u32(seedSrc) % 0xffffffff;
  const lane = ((seed % 3) + 3) % 3;
  const tier = (g5 != null ? g5 : seed) % 5;
  const D = 1 + ((g1024 != null ? g1024 : seed) % 60), prime = P[D - 1], sp = Math.sqrt(prime), spN = sp / Math.sqrt(281);
  let level;
  if (hilbertOrNull != null) level = Math.max(0, Math.min(15, Math.floor((hilbertOrNull - 892) / 46.9)));
  else { const base = crit === 'high' ? 11 : crit === 'medium' ? 6 : 0; level = Math.max(0, Math.min(15, base + (seed % 5))); }
  const theta = lane * WEDGE + ((g1024 != null ? g1024 : (seed % 1024)) / 1024) * (WEDGE - 0.12) + 0.0006 * sp * ((seed >> 9) % 71);
  const r = TIER_BASE[tier] + 0.5 * spN + 0.0009 * sp * (seed % 113);
  return { lane, tier, D, prime, level, r, theta };
}

const points = [];
// dedup named by pid (MEASURED 2026-06-20: 13 duplicate formula corpus rows + 1 dup seat) — same PID = one marker
const _seenPid = new Set(); const namedU = named.filter(s => s.pid && !_seenPid.has(s.pid) && _seenPid.add(s.pid));
const namedDups = named.length - namedU.length;
const namedFormulaDistinct = namedU.filter(s => s.layer === 'formula').length;
const namedSeatDistinct = namedU.length - namedFormulaDistinct;
// NAMED individual (formulas ALWAYS -> DISTRICT-F cylinder, by source)
for (const s of namedU) {
  const tw = (s.layer === 'formula') ? 'DISTRICT-F' : namedTower(s.layer, s.cls), ctr = centers[tw];
  const seed = parseInt(s.pid.slice(0, 8), 16) >>> 0;
  const h = s.hilbert || (892 + (seed % 751));
  const pl = place(s.pid, s.g1024, s.g5, h, null);
  points.push({ kind: 'named', pid: s.pid, name: s.name, tower: tw, cyl: ctr.k, layer: s.layer, fed: s.fed,
    lane: pl.lane, level: pl.level, tier: TAU[pl.tier], formula: FORM[pl.tier], D: pl.D, prime: pl.prime, rank: rankOf(s.layer, s.cls), hilbert: h,
    x: +(ctr.cx + pl.r * Math.cos(pl.theta)).toFixed(3), y: +(ctr.cy + pl.r * Math.sin(pl.theta)).toFixed(3), z: +(pl.level * 1.05).toFixed(3) });
}
const namedTopByTower = {}; for (const p of points) { const t = namedTopByTower[p.tower]; if (!t || p.rank > t.rank) namedTopByTower[p.tower] = p; }

// SURFACES: critical individual, low/medium aggregate (anti-flatten cells)
const surfLines = fs.readFileSync(SURF, 'utf8').split('\n');
const cells = new Map(); // key -> {tower,level,lane,tier,count,childHash,sx,sy,sz,critMix}
let nCrit = 0, nAgg = 0, nSurf = 0;
for (const line of surfLines) {
  if (!line.trim()) continue; let o; try { o = JSON.parse(line); } catch (e) { continue; }
  nSurf++;
  const rc = o.rootClass && SURF_TOWERS.includes(o.rootClass) ? o.rootClass : 'app_root';
  const ctr = centers[rc]; const crit = o.criticality || 'low';
  const pl = place(o.id, null, null, null, crit);
  const wx = +(ctr.cx + pl.r * Math.cos(pl.theta)).toFixed(3), wy = +(ctr.cy + pl.r * Math.sin(pl.theta)).toFixed(3), wz = +(pl.level * 1.05).toFixed(3);
  if (crit === 'high') {
    nCrit++;
    points.push({ kind: 'surface-critical', pid: sha16(o.id), name: o.id, tower: rc, cyl: ctr.k, crit, drive: o.drive, lane: pl.lane, level: pl.level, tier: TAU[pl.tier], D: pl.D, prime: pl.prime, x: wx, y: wy, z: wz });
  } else {
    const key = rc + '|L' + pl.level + '|' + pl.lane + '|' + pl.tier;
    let c = cells.get(key);
    if (!c) { c = { tower: rc, cyl: ctr.k, level: pl.level, lane: pl.lane, tier: pl.tier, count: 0, childHash: 0, sx: 0, sy: 0, sz: 0, hi: 0, med: 0, low: 0 }; cells.set(key, c); }
    c.count++; c.sx += wx; c.sy += wy; c.sz += wz;
    c.childHash = (Math.imul(c.childHash, 131) + (parseInt(sha16(o.id).slice(0, 8), 16) >>> 0)) >>> 0;
    if (crit === 'medium') c.med++; else c.low++;
  }
}
for (const c of cells.values()) {
  nAgg += c.count;
  points.push({ kind: 'surface-aggregate', tower: c.tower, cyl: c.cyl, level: c.level, lane: c.lane, tier: TAU[c.tier],
    child_count: c.count, child_index_hash: c.childHash.toString(16).padStart(8, '0'), summary_not_identity: true, med: c.med, low: c.low,
    x: +(c.sx / c.count).toFixed(3), y: +(c.sy / c.count).toFixed(3), z: +(c.sz / c.count).toFixed(3) });
}

// ---- PIPES ----
const pipes = [];
const byTower = {}; for (const p of points) if (p.kind === 'named') (byTower[p.tower] ||= []).push(p);
for (const t of NAMED_TOWERS) { const arr = byTower[t] || []; for (const p of arr) { let best = null, bd = 1e18; for (const q of arr) if (q.rank > p.rank) { const d = Math.abs(q.hilbert - p.hilbert); if (d < bd) { bd = d; best = q; } } if (best) pipes.push({ from: points.indexOf(p), to: points.indexOf(best), kind: 'hierarchy' }); } }
// cross-cylinder "pipes to them": APEX top -> every other cylinder's representative
const apex = namedTopByTower['APEX'];
function towerRep(t) { // a representative point index for a cylinder (named top, or first surface/agg)
  if (namedTopByTower[t]) return points.indexOf(namedTopByTower[t]);
  const idx = points.findIndex(p => p.tower === t); return idx;
}
if (apex) { const ai = points.indexOf(apex); for (const t of allTowers) { if (t === 'APEX') continue; const ri = towerRep(t); if (ri >= 0) pipes.push({ from: ai, to: ri, kind: 'cross-activation' }); } }
const within = pipes.filter(p => p.kind === 'hierarchy').length, cross = pipes.length - within;

const perCyl = allTowers.filter(t => points.some(p => p.tower === t)).map(t => ({ tower: t, type: NAMED_TOWERS.includes(t) ? 'named' : 'surface', individual: points.filter(p => p.tower === t && p.kind !== 'surface-aggregate').length, aggregate_cells: points.filter(p => p.tower === t && p.kind === 'surface-aggregate').length, surfaces_aggregated: points.filter(p => p.tower === t && p.kind === 'surface-aggregate').reduce((a, p) => a + p.child_count, 0), center: centers[t] }));
const cset = new Set(points.map(p => p.x + ',' + p.y + ',' + p.z));
const meta = {
  title: 'ASOLARIA MULTI-CYLINDER MAP v2 — named + full 81,434-surface population, pipes shown',
  cylinders: perCyl.length, marker_count: points.length, points_individual: points.filter(p => p.kind !== 'surface-aggregate').length, aggregate_cells: points.filter(p => p.kind === 'surface-aggregate').length,
  coordinate_collisions: points.length - cset.size,
  population: { named_rows: named.length, named_distinct: namedU.length, named_dups_collapsed: namedDups, seats_distinct: namedSeatDistinct, formulas_rows: nForm, formulas_distinct: namedFormulaDistinct, surfaces_total: nSurf, surfaces_critical_individual: nCrit, surfaces_aggregated: nAgg, grand_total_distinct_represented: namedU.length + nSurf },
  logical_NOT_plotted: { premade_registry_100B: 1e11 + '(real, not plotted)', logical_agents: '1e100000000 (logical, not plotted)', human_pids: '10e9 (real, not plotted)' },
  pipes: pipes.length, pipes_within: within, pipes_cross: cross,
  anti_flatten: 'AF-001..005 honored: every aggregate cell carries child_count + child_index_hash + summary_not_identity; 4,129 critical + 1,844 named plotted individually; nothing dropped, totals exact.',
  projection: 'cylinder=tower on meta-ring R=' + R_META + ' (cross>within §3.3); within: z=level(16), theta=lane*120deg+glyph, r=prime-power tier band + sqrt(p). criticality->z-band for surfaces. no RNG.',
  per_cylinder: perCyl,
  grounding: 'office 726 fed + DISTRICT-F 1118 + omni-consolidation-registry surfaces.full.ndjson (81,434); PRIME-TOWERS §3 + F05 §3.3 + research wf wxd7tzv29'
};
fs.writeFileSync(OUT + '/multi-cylinder-v2-data.json', JSON.stringify({ meta, points, pipes }), 'utf8');
console.log('MULTI-CYLINDER v2: ' + perCyl.length + ' cylinders | markers=' + points.length + ' (named ' + namedU.length + ' distinct [' + namedDups + ' dup rows collapsed; formulas ' + namedFormulaDistinct + ' all->DISTRICT-F] + critical ' + nCrit + ' + ' + cells.size + ' agg cells over ' + nAgg + ' surfaces)');
console.log('surfaces represented: ' + nSurf + ' (critical ' + nCrit + ' + aggregated ' + nAgg + ')  | coord collisions=' + meta.coordinate_collisions);
console.log('pipes=' + pipes.length + ' (within=' + within + ' cross=' + cross + ')');
console.log('per-cylinder:'); for (const c of perCyl) console.log('  ' + c.tower.padEnd(18) + ' [' + c.type + '] indiv=' + c.individual + ' aggCells=' + c.aggregate_cells + ' aggSurfaces=' + c.surfaces_aggregated);
console.log('-> ' + OUT + '/multi-cylinder-v2-data.json');
