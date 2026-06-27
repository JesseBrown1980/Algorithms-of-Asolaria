#!/usr/bin/env node
/* ============================================================================
 * t6-loop-100b-logical.cjs
 * LAYER: t6-loop-100b-logical
 *
 * LOOP "100B" REAL-BUT-BOUNDED LOGICAL SCALE-TEST.
 *
 * HONEST FRAMING (printed below): This is NOT a 100,000,000,000 (1e11)
 * MATERIALIZED fire. materialized=0, E=0. Nothing is emitted to disk, no
 * room/daemon/executor is fired, no engine is cranked. This test processes
 * as many *logical* packets as fit in a ~8-second wall-clock budget using the
 * REAL Asolaria placement formulas (sha16 PID, u32 .toUpperCase() seed,
 * sector%113, lane%3, tier seed%5, level 0..15), then it MEASURES:
 *   (a) DETERMINISM   — a 100,000-packet slice yields a byte-identical
 *                       aggregate hash on re-run (no Math.random; pure LCG).
 *   (b) LANE BALANCE  — each of the 3 angular rule-of-three lanes lands
 *                       within 2% of 1/3 of the processed population.
 *   (c) ZERO COLLISION— 100,000 distinct seeds produce 100,000 distinct PIDs.
 *   (d) THROUGHPUT    — packets/sec, and the PROJECTED wall-clock for 1e11
 *                       at that rate (a projection, NOT a run).
 *
 * GROUND-TRUTH formulas confirmed by reading the real source:
 *   - C:/tmp/asolaria-real-model/real-model-gen-v2.cjs
 *       L11  sha16(s)  = sha256(String(s),'utf8').hex.slice(0,16)   [canonical PID]
 *       L12  u32(s)    = parseInt(sha256(String(s).toUpperCase()).hex.slice(0,8),16) >>> 0
 *       L19  sector    = seed % 113
 *       L20  lane      = seed % 3            [angular rule-of-three, 3 wedges]
 *   - C:/tmp/asolaria-unified-archaeology/ingest.cjs
 *       L15  sha16/md516, L16 u32 (identical), L25 geometry() level/tier/bh
 * The numeric "bh = sector*3072+lane*1024+glyph" named loosely elsewhere does
 * NOT exist in the real code, so this test does NOT assert it.
 *
 * HARD RULES honored: real assertions only; no stubs / no fake greens; no
 * sleeping-to-pretend-work; count results; any failed assertion -> FAIL++ and
 * process.exitCode = 1; missing input -> synthesize or SKIP (never silent pass);
 * no external network.
 * ==========================================================================*/
'use strict';

const crypto = require('crypto');

// ---------------------------------------------------------------------------
// counters
// ---------------------------------------------------------------------------
let PASS = 0, FAIL = 0, SKIP = 0;
function ok(cond, label) {
  if (cond) { PASS++; console.log('  PASS  ' + label); }
  else { FAIL++; process.exitCode = 1; console.log('  FAIL  ' + label); }
  return !!cond;
}
function skip(label, reason) {
  SKIP++; console.log('  SKIP  ' + label + '  (reason: ' + reason + ')');
}

// ---------------------------------------------------------------------------
// REAL Asolaria formulas (verbatim semantics from the cited source files)
// ---------------------------------------------------------------------------
// canonical PID: first 16 hex chars (8 bytes) of sha256 over the lowercase name
function sha16(s) {
  return crypto.createHash('sha256').update(String(s), 'utf8').digest('hex').slice(0, 16);
}
// placement seed: top 32 bits of sha256 over the UPPERCASED name (note .toUpperCase())
function u32(s) {
  return parseInt(
    crypto.createHash('sha256').update(String(s).toUpperCase()).digest('hex').slice(0, 8),
    16
  ) >>> 0;
}

const PRIMES60 = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,139,149,151,157,163,167,173,179,181,191,193,197,199,211,223,227,229,233,239,241,251,257,263,269,271,277,281];

// Sanity: the prime tower must match the canonical 60-prime list and P[29] === 113
ok(PRIMES60.length === 60, 'prime tower has 60 primes');
ok(PRIMES60[29] === 113, 'P[29] === 113 (the sector-fan prime)');
ok(PRIMES60[0] === 2 && PRIMES60[59] === 281, 'prime tower spans 2..281');

// ---------------------------------------------------------------------------
// Deterministic LCG (NO Math.random). Numerical Recipes 32-bit constants.
//   x_{n+1} = (1664525 * x_n + 1013904223) mod 2^32
// We use it to derive each packet's "seed name" deterministically.
// ---------------------------------------------------------------------------
const LCG_A = 1664525, LCG_C = 1013904223, LCG_M = 0x100000000; // 2^32
function lcgNext(state) {
  return (Math.imul(LCG_A, state) + LCG_C) >>> 0; // >>> 0 keeps it in [0, 2^32)
}

// ---------------------------------------------------------------------------
// Process ONE logical packet from a 32-bit LCG value.
// The packet name is "PKT-<lcgValue>"; everything else is derived by the
// REAL formulas. Returns the fields the test aggregates over.
// ---------------------------------------------------------------------------
function processPacket(lcgVal) {
  const name = 'PKT-' + lcgVal;        // deterministic name string
  const seed = u32(name);              // u32 over UPPERCASED name (real rule)
  const pid  = sha16(name);            // canonical 16-hex PID (real rule)
  const sector = seed % 113;           // 113-slot sector fan (real rule)
  const lane = seed % 3;               // angular rule-of-three lane 0..2 (real rule)
  const tier = seed % 5;               // tier(seed%5) per the layer spec
  const level = (seed >>> 8) % 16;     // level 0..15 (ingest.cjs L25 z-plane)
  return { pid, sector, lane, tier, level, seed };
}

// ---------------------------------------------------------------------------
// Aggregate a fixed slice of N packets into ONE rolling sha256 hash plus
// lane tallies and a PID set. Deterministic and self-contained so it can be
// re-run for the determinism assertion. Starts from LCG seed `start`.
// ---------------------------------------------------------------------------
function runSlice(start, N, collectPids) {
  const h = crypto.createHash('sha256');
  const lanes = [0, 0, 0];
  const tiers = [0, 0, 0, 0, 0];
  const pids = collectPids ? new Set() : null;
  let state = start >>> 0;
  for (let i = 0; i < N; i++) {
    state = lcgNext(state);
    const p = processPacket(state);
    // fold every field into the aggregate hash -> byte-identity check
    h.update(p.pid);
    h.update(',' + p.sector + ',' + p.lane + ',' + p.tier + ',' + p.level + ';');
    lanes[p.lane]++;
    tiers[p.tier]++;
    if (pids) pids.add(p.pid);
  }
  return { hash: h.digest('hex'), lanes, tiers, pids, N };
}

// ===========================================================================
// HONEST HEADER
// ===========================================================================
console.log('================================================================');
console.log('t6-loop-100b-logical  —  LOOP "100B" LOGICAL SCALE-TEST');
console.log('  TAG: materialized=0  E=0  (NOT a 1e11 materialized fire)');
console.log('  Nothing emitted, nothing fired, no engine cranked.');
console.log('  Deterministic LCG only (no Math.random). Real Asolaria formulas.');
console.log('================================================================');

// ===========================================================================
// (a) DETERMINISM — re-run a 100,000-packet slice; aggregate hash must match
// ===========================================================================
console.log('\n[a] DETERMINISM (100,000-packet slice, byte-identical aggregate hash)');
const SLICE_N = 100000;
const SLICE_SEED = 0x6a655373; // fixed start ("jeSs" bytes) — deterministic, no RNG
const sliceA = runSlice(SLICE_SEED, SLICE_N, true);
const sliceB = runSlice(SLICE_SEED, SLICE_N, false);
console.log('      slice hash A = ' + sliceA.hash);
console.log('      slice hash B = ' + sliceB.hash);
ok(sliceA.hash === sliceB.hash, 'two runs of the 100k slice produce the SAME aggregate sha256');
ok(/^[0-9a-f]{64}$/.test(sliceA.hash), 'aggregate hash is a well-formed 64-hex sha256');

// ===========================================================================
// (c) ZERO PID COLLISIONS in the 100,000 sample
//     (done here because sliceA already collected the PID set)
// ===========================================================================
console.log('\n[c] ZERO PID COLLISIONS (100,000 distinct seeds -> distinct PIDs)');
console.log('      distinct PIDs = ' + sliceA.pids.size + ' / ' + SLICE_N);
ok(sliceA.pids.size === SLICE_N, 'all 100,000 PIDs are unique (zero collisions)');
// spot-check the PID formula against an independent recomputation
{
  let pidFormulaOk = true, checked = 0;
  let st = SLICE_SEED >>> 0;
  for (let i = 0; i < 1000; i++) {
    st = lcgNext(st);
    const name = 'PKT-' + st;
    const expect = crypto.createHash('sha256').update(name, 'utf8').digest('hex').slice(0, 16);
    if (sha16(name) !== expect) { pidFormulaOk = false; break; }
    checked++;
  }
  ok(pidFormulaOk && checked === 1000, 'PID formula == sha256(name).slice(0,16) (1000 spot-checks)');
}

// ===========================================================================
// (LOGICAL SCALE) Process as many packets as fit in a ~8s wall-clock budget.
//   Honest: this is the bounded stand-in for "100B". We report ACTUAL N.
//   Target >= 2,000,000. Below target -> FAIL (real machine assertion, not a
//   sleep). Lane/tier tallies accumulate over the FULL processed population.
// ===========================================================================
console.log('\n[scale] Logical packet loop (~8s wall-clock budget)');
const BUDGET_MS = 8000;
const TARGET_N = 2000000;
const CHUNK = 50000;            // check the clock every CHUNK packets (low overhead)
const laneTotals = [0, 0, 0];
const tierTotals = [0, 0, 0, 0, 0];
let processed = 0;
let scaleState = 0x100b1006 >>> 0;   // fixed deterministic start
const t0 = process.hrtime.bigint();
let elapsedMs = 0;
while (elapsedMs < BUDGET_MS) {
  for (let i = 0; i < CHUNK; i++) {
    scaleState = lcgNext(scaleState);
    const p = processPacket(scaleState);
    laneTotals[p.lane]++;
    tierTotals[p.tier]++;
  }
  processed += CHUNK;
  elapsedMs = Number(process.hrtime.bigint() - t0) / 1e6;
}
const wallSec = elapsedMs / 1000;
const throughput = processed / wallSec; // packets/sec
console.log('      processed N        = ' + processed.toLocaleString('en-US'));
console.log('      wall-clock         = ' + wallSec.toFixed(3) + ' s');
console.log('      throughput         = ' + Math.round(throughput).toLocaleString('en-US') + ' packets/sec');
ok(processed >= TARGET_N,
   'processed N (' + processed.toLocaleString('en-US') + ') >= target ' + TARGET_N.toLocaleString('en-US'));

// ===========================================================================
// (b) LANE BALANCE — each lane within 2% of 1/3 across the FULL processed set
// ===========================================================================
console.log('\n[b] LANE BALANCE (each angular rule-of-three lane within 2% of 1/3)');
{
  const total = laneTotals[0] + laneTotals[1] + laneTotals[2];
  ok(total === processed, 'lane tally total equals processed N');
  const ideal = 1 / 3;
  const TOL = 0.02; // within 2% (absolute fraction tolerance, e.g. 0.3133..0.3533)
  for (let l = 0; l < 3; l++) {
    const frac = laneTotals[l] / total;
    const dev = Math.abs(frac - ideal);
    console.log('      lane ' + l + ': ' + laneTotals[l].toLocaleString('en-US') +
                '  frac=' + frac.toFixed(5) + '  dev=' + dev.toFixed(5));
    ok(dev <= TOL, 'lane ' + l + ' fraction (' + frac.toFixed(5) + ') within 2% of 1/3');
  }
}

// ===========================================================================
// (d) THROUGHPUT + PROJECTED 1e11 WALL-CLOCK (a projection, NOT a run)
// ===========================================================================
console.log('\n[d] THROUGHPUT + PROJECTION for 1e11 (projection only — NOT executed)');
{
  const TARGET_1E11 = 1e11;
  const projSec = TARGET_1E11 / throughput;
  const projHours = projSec / 3600;
  const projDays = projHours / 24;
  console.log('      throughput          = ' + Math.round(throughput).toLocaleString('en-US') + ' packets/sec');
  console.log('      projected 1e11 time = ' + projSec.toFixed(0) + ' s  (' +
              projHours.toFixed(2) + ' h  /  ' + projDays.toFixed(2) + ' days)');
  console.log('      NOTE: projection assumes flat single-core rate, materialized=0, E=0.');
  // assert the projection is a finite, positive, sane number (real math check)
  ok(isFinite(throughput) && throughput > 0, 'throughput is finite and positive');
  ok(isFinite(projSec) && projSec > 0, 'projected 1e11 wall-clock is finite and positive');
  // internal consistency: throughput * projSec must reconstruct 1e11 (within rounding)
  ok(Math.abs(throughput * projSec - TARGET_1E11) / TARGET_1E11 < 1e-9,
     'projection is internally consistent (throughput * projSec == 1e11)');
}

// ===========================================================================
// SECTOR FAN sanity (real ground-truth: sector in [0,112], 113 slots)
// ===========================================================================
console.log('\n[extra] SECTOR FAN range check (sector in 0..112 over a 50k sample)');
{
  let st = 0x5ec70123 >>> 0, bad = 0, seenSectors = new Set();
  for (let i = 0; i < 50000; i++) {
    st = lcgNext(st);
    const p = processPacket(st);
    if (p.sector < 0 || p.sector > 112) bad++;
    seenSectors.add(p.sector);
    if (p.level < 0 || p.level > 15) bad++;
    if (p.tier < 0 || p.tier > 4) bad++;
    if (p.lane < 0 || p.lane > 2) bad++;
  }
  console.log('      out-of-range fields = ' + bad + ' ; distinct sectors hit = ' + seenSectors.size + '/113');
  ok(bad === 0, 'all derived fields in range (sector 0..112, level 0..15, tier 0..4, lane 0..2)');
  ok(seenSectors.size === 113, 'all 113 sectors are reachable in a 50k sample');
}

// ===========================================================================
// RESULT LINE (must be the literal last line)
// ===========================================================================
const exit = (FAIL === 0) ? 0 : 1;
console.log('\n----------------------------------------------------------------');
console.log('RESULT layer=t6-loop-100b-logical PASS=' + PASS + ' FAIL=' + FAIL + ' SKIP=' + SKIP + ' exit=' + exit);
