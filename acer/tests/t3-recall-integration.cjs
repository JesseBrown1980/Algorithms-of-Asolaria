#!/usr/bin/env node
/* =============================================================================
 * t3-recall-integration  —  INTEGRATION / total-recall (.hbp + .hbi O(seek))
 * -----------------------------------------------------------------------------
 * Mirrors the REAL pattern from:
 *   C:/tmp/asolaria-unified-archaeology/build-hbi.cjs      (index builder)
 *   C:/tmp/asolaria-unified-archaeology/archaeology-serve.cjs (O(seek) recall)
 *
 * What this asserts (REAL assertions, no stubs, no fake greens):
 *   A) Build a synthetic 500-row .hbp where every data row is
 *        ARCH|ts=<d>|src=<s>|pid=<16hex>|bh=<BH.string>|...
 *      (plus an ARCHHDR| header line that MUST be excluded by the indexer,
 *       exactly like the live table's first line).
 *   B) Build its .hbi (pid+bh+ts -> offset+len) using the byte-scan indexer
 *      logic copied from build-hbi.cjs (0x0A line split, 'A','R' fast-path,
 *      startsWith('ARCH|'), len excludes the trailing \n).
 *   C) For 50 random rows: open the .hbp, seek to entry.offset, read entry.len
 *      bytes (single fs.readSync — O(seek), NO file scan), and assert the
 *      recalled bytes:
 *         - start with "ARCH|"  (byte-exact prefix)
 *         - contain  "pid=<the right pid>"
 *         - the recalled byte length == entry.len, and byte[len] in the file is \n
 *      i.e. a byte-exact O(seek) round-trip.
 *   D) Cross-check: the indexer must NOT index the ARCHHDR| line (count==500).
 *   E) Live sub-test: if C:/tmp/asolaria-unified-archaeology/ASOLARIA-UNIFIED-
 *      ARCHAEOLOGY.hbi exists, parse 3 real HBI| rows, seek the real .hbp at
 *      their offset/len, and assert each recalled row starts with "ARCH|" and
 *      contains its pid (byte-exact recall against the LIVE 195MB table).
 *      If the .hbi (or .hbp) is absent -> SKIP with a printed reason (NOT pass).
 *
 * Ground-truth honored:
 *   - canonical PID = sha16(name) = sha256(String(name),'utf8').slice(0,16)
 *     (real-model-gen-v2.cjs L11 / ingest.cjs L15). Synthetic rows mint pids
 *     this exact way so the test exercises the real PID rule.
 *   - bh is an OPAQUE STRING "BH.<tier>.L<level>.D<D>.<K>" (ingest.cjs L25);
 *     the prompt's bh = sector*3072+lane*1024+glyph formula DOES NOT EXIST and
 *     is NOT asserted here.
 *   - lane = seed % 3 ; sector = u32(name) % 113 ; u32 hashes the .toUpperCase()
 *     name (v2 L12/L19/L20). Used only to make realistic bh strings; the recall
 *     assertions are byte-exact and do not depend on these.
 *
 * HARD RULES: count results; any failed assertion -> FAIL++ and exitCode=1.
 * Last line is exactly the RESULT line.
 * ===========================================================================*/
'use strict';
const fs = require('fs');
const os = require('os');
const path = require('path');
const crypto = require('crypto');

let PASS = 0, FAIL = 0, SKIP = 0;
function ok(cond, msg) {
  if (cond) { PASS++; console.log('  PASS ' + msg); }
  else { FAIL++; process.exitCode = 1; console.log('  FAIL ' + msg); }
}
function skip(msg, reason) { SKIP++; console.log('  SKIP ' + msg + ' :: reason=' + reason); }

// ---- ground-truth PID / seed helpers (verbatim rules from v2 L11-L12) -------
const sha16 = name => crypto.createHash('sha256').update(String(name), 'utf8').digest('hex').slice(0, 16);
const u32   = name => parseInt(crypto.createHash('sha256').update(String(name).toUpperCase()).digest('hex').slice(0, 8), 16) >>> 0;
const TIERS = ['τ1', 'τ3', 'τ3^3', 'τ3^5', 'τH'];
const PRIMES60 = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,139,149,151,157,163,167,173,179,181,191,193,197,199,211,223,227,229,233,239,241,251,257,263,269,271,277,281];

// =============================================================================
// SETUP: synthetic 500-row .hbp + .hbi in an isolated temp dir
// =============================================================================
const N = 500;
const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 't3-recall-'));
const SYN_HBP = path.join(tmpDir, 'SYNTH-ARCHAEOLOGY.hbp');
const SYN_HBI = path.join(tmpDir, 'SYNTH-ARCHAEOLOGY.hbi');

// Build the synthetic .hbp. We keep an authoritative expectation map so the
// recall assertions compare against KNOWN-good bytes, not against the indexer.
const expected = []; // { pid, bh, ts, line }  (line = the exact row text, no \n)
const lines = [];

// Header line — MUST be ignored by the indexer (starts 'ARCH' but not 'ARCH|').
lines.push('ARCHHDR|table=SYNTH-ARCHAEOLOGY|vantage=acer|rows=' + N +
           '|formula=PID=sha256name16;triad=md5_16;lane=seed%3|read_only=1|E=0|json=0');

for (let i = 0; i < N; i++) {
  const name = 'synthetic-artifact-' + i + '-' + crypto.randomBytes(4).toString('hex');
  const pid  = sha16(name);                 // canonical 16-hex PID
  const seed = u32(name);
  const lane = seed % 3;                     // rule-of-three angular lane (0,1,2)
  const sector = seed % 113;                 // 113-slot sector fan
  const tier = TIERS[seed % TIERS.length];
  const level = seed % 16;                   // L0..L15
  const D = (seed % 60) + 1;                 // 1..60
  const prime = PRIMES60[(D - 1) % PRIMES60.length];
  const cube = prime * prime * prime;
  const K = seed % cube;
  const bh = 'BH.' + tier + '.L' + level + '.D' + D + '.' + K;   // opaque STRING bh
  const ts = '20' + (18 + (i % 9)) + '-' + String(1 + (i % 12)).padStart(2, '0') + '-' +
             String(1 + (i % 27)).padStart(2, '0');
  // ARCH data row in the live shape (pid/bh/ts present, extra fields padded so
  // rows vary in length, exercising real per-row offset/len arithmetic).
  const line = 'ARCH|ts=' + ts + '|src=SYN|cls=test|name=' + name +
               '|pid=' + pid + '|bh=' + bh + '|sector=' + sector + '|lane=' + lane +
               '|sig=' + crypto.randomBytes(2 + (i % 6)).toString('hex');
  lines.push(line);
  expected.push({ pid, bh, ts, line });
}
fs.writeFileSync(SYN_HBP, lines.join('\n') + '\n', 'utf8');

// ---- Build the .hbi using build-hbi.cjs's exact byte-scan indexer logic -----
const buf = fs.readFileSync(SYN_HBP);
const sha256buf = b => crypto.createHash('sha256').update(b).digest('hex');
const fileSha = sha256buf(buf);
const idx = [];
{
  let start = 0;
  for (let i = 0; i < buf.length; i++) {
    if (buf[i] === 0x0A) {
      if (buf[start] === 0x41 && buf[start + 1] === 0x52) {       // 'A','R'
        const line = buf.toString('utf8', start, i);
        if (line.startsWith('ARCH|')) {
          const pid = (line.match(/\|pid=([0-9a-f]{16})/) || [])[1] || '';
          const bh  = (line.match(/\|bh=([^|]+)/) || [])[1] || '';
          const ts  = (line.match(/\|ts=([^|]+)/) || [])[1] || '';
          idx.push({ pid, bh, ts, offset: start, len: i - start }); // len excludes \n
        }
      }
      start = i + 1;
    }
  }
}
{
  const out = [];
  out.push('HBIHDR|for=SYNTH-ARCHAEOLOGY.hbp|file_sha256=' + fileSha + '|rows=' + idx.length +
           '|key=pid+bh+ts->offset+len|pattern=F05-total-recall-O(seek)|json=0');
  for (let n = 0; n < idx.length; n++) {
    const r = idx[n];
    out.push('HBI|row=' + n + '|pid=' + r.pid + '|bh=' + r.bh + '|ts=' + r.ts +
             '|offset=' + r.offset + '|len=' + r.len);
  }
  fs.writeFileSync(SYN_HBI, out.join('\n') + '\n', 'utf8');
}

// =============================================================================
// TEST D: the indexer indexed exactly the 500 data rows (ARCHHDR| excluded)
// =============================================================================
console.log('--- D: indexer scope (ARCHHDR header must be excluded) ---');
ok(idx.length === N, 'indexed exactly ' + N + ' ARCH data rows (got ' + idx.length + '); ARCHHDR| not indexed');
ok(idx.every(e => /^[0-9a-f]{16}$/.test(e.pid)), 'every indexed row has a 16-hex pid');

// Re-parse the written .hbi the way archaeology-serve.cjs does, to prove the
// sidecar we wrote is consumable by the real server's loader.
const byPid = new Map();
for (const line of fs.readFileSync(SYN_HBI, 'utf8').split('\n')) {
  if (line.charCodeAt(0) !== 72 || !line.startsWith('HBI|')) continue;   // 'H'
  const pid = (line.match(/\|pid=([0-9a-f]{16})/) || [])[1];
  const off = +((line.match(/\|offset=(\d+)/) || [])[1]);
  const len = +((line.match(/\|len=(\d+)/) || [])[1]);
  if (pid) byPid.set(pid, [off, len]);
}
ok(byPid.size === N, 'serve-style .hbi loader parsed ' + N + ' pid->offset entries (got ' + byPid.size + ')');

// =============================================================================
// TEST A/B/C: 50 random rows — byte-exact O(seek) round-trip via the .hbi
// =============================================================================
console.log('--- A/B/C: 50 random O(seek) recalls (seek+read by .hbi entry, no scan) ---');
const fd = fs.openSync(SYN_HBP, 'r');
function recallAt(offset, len) {
  const b = Buffer.alloc(len);
  const read = fs.readSync(fd, b, 0, len, offset);   // single seek-read, O(seek)
  return { read, str: b.toString('utf8') };
}

// pick 50 distinct random row indices in [0,500)
const picks = new Set();
while (picks.size < 50) picks.add(Math.floor(Math.random() * N));
const sampleIdx = [...picks];

let recallHits = 0, prefixHits = 0, lenExact = 0, newlineBoundary = 0, viaIndexHits = 0;
const fileLen = buf.length;
for (const i of sampleIdx) {
  const exp = expected[i];
  // Path 1: recall straight from the byte-scan index entry (build-hbi path)
  const e = idx[i];
  const r = recallAt(e.offset, e.len);
  if (r.str.startsWith('ARCH|')) prefixHits++;
  if (r.str.includes('pid=' + exp.pid)) recallHits++;
  if (r.read === e.len && r.str === exp.line) lenExact++;       // byte-exact full row
  // boundary: the byte immediately after the recalled span is the row's \n
  if (e.offset + e.len < fileLen && buf[e.offset + e.len] === 0x0A) newlineBoundary++;

  // Path 2: recall via the serve-style pid->[off,len] map (proves the .hbi key
  // resolves the same bytes — a true integration of builder + server loader)
  const entry = byPid.get(exp.pid);
  if (entry) {
    const r2 = recallAt(entry[0], entry[1]);
    if (r2.str.startsWith('ARCH|') && r2.str.includes('pid=' + exp.pid)) viaIndexHits++;
  }
}
fs.closeSync(fd);

ok(prefixHits === 50,      'all 50 recalled rows start with "ARCH|" (got ' + prefixHits + ')');
ok(recallHits === 50,      'all 50 recalled rows contain the correct pid (got ' + recallHits + ')');
ok(lenExact === 50,        'all 50 recalls are byte-exact full-row round-trips (got ' + lenExact + ')');
ok(newlineBoundary === 50, 'all 50 entry.len spans end exactly at the row \\n boundary (got ' + newlineBoundary + ')');
ok(viaIndexHits === 50,    'all 50 recalls resolve via the serve-style pid->offset map (got ' + viaIndexHits + ')');

// Negative control: a random pid that is NOT in the table must miss the index
// (proves the hit above is real lookup, not always-true).
const bogus = sha16('definitely-not-in-the-table-' + crypto.randomBytes(8).toString('hex'));
ok(!byPid.has(bogus), 'a non-existent pid is absent from the index (negative control)');

// =============================================================================
// TEST E: LIVE index — seek-test 3 real rows from ASOLARIA-UNIFIED-ARCHAEOLOGY
// =============================================================================
console.log('--- E: LIVE ASOLARIA-UNIFIED-ARCHAEOLOGY recall (3 real rows) ---');
const DIR = 'C:/tmp/asolaria-unified-archaeology';
const LIVE_HBP = DIR + '/ASOLARIA-UNIFIED-ARCHAEOLOGY.hbp';
const LIVE_HBI = DIR + '/ASOLARIA-UNIFIED-ARCHAEOLOGY.hbi';

if (!fs.existsSync(LIVE_HBI)) {
  skip('live recall (3 real rows)', 'missing ' + LIVE_HBI + ' (live .hbi not present)');
} else if (!fs.existsSync(LIVE_HBP)) {
  skip('live recall (3 real rows)', 'missing ' + LIVE_HBP + ' (.hbi present but .hbp absent)');
} else {
  // Parse the first 3 HBI| data rows from the live sidecar (serve-style regex).
  const liveRows = [];
  const stream = fs.readFileSync(LIVE_HBI, 'utf8');
  let nl = -1, lineNo = 0, taken = 0, lineStart = 0;
  // scan line-by-line without splitting the whole 64MB into an array
  for (let i = 0; i < stream.length && taken < 3; i++) {
    if (stream.charCodeAt(i) === 0x0A) {
      const line = stream.slice(lineStart, i);
      lineStart = i + 1;
      if (line.charCodeAt(0) === 72 && line.startsWith('HBI|')) {  // 'H'
        const pid = (line.match(/\|pid=([0-9a-f]{16})/) || [])[1];
        const off = +((line.match(/\|offset=(\d+)/) || [])[1]);
        const len = +((line.match(/\|len=(\d+)/) || [])[1]);
        if (pid && Number.isFinite(off) && Number.isFinite(len)) {
          liveRows.push({ pid, off, len });
          taken++;
        }
      }
    }
  }
  if (liveRows.length < 3) {
    skip('live recall (3 real rows)', 'live .hbi parsed only ' + liveRows.length + ' usable HBI| rows (need 3)');
  } else {
    const lfd = fs.openSync(LIVE_HBP, 'r');
    const liveSize = fs.statSync(LIVE_HBP).size;
    let liveHits = 0;
    for (const r of liveRows) {
      if (r.off + r.len > liveSize) {
        console.log('  (live) row pid=' + r.pid + ' off=' + r.off + ' len=' + r.len + ' exceeds file size ' + liveSize);
        continue;
      }
      const b = Buffer.alloc(r.len);
      fs.readSync(lfd, b, 0, r.len, r.off);
      const s = b.toString('utf8');
      const good = s.startsWith('ARCH|') && s.includes('pid=' + r.pid);
      console.log('  (live) pid=' + r.pid + ' @off=' + r.off + ' len=' + r.len +
                  ' -> ' + (good ? 'HIT' : 'MISS') + ' :: ' + s.slice(0, 80));
      if (good) liveHits++;
    }
    fs.closeSync(lfd);
    ok(liveHits === 3, 'LIVE: all 3 real rows recalled byte-exact (start "ARCH|" + correct pid) (got ' + liveHits + ')');
  }
}

// ---- cleanup synthetic artifacts (best-effort, non-fatal) -------------------
try { fs.rmSync(tmpDir, { recursive: true, force: true }); } catch (e) { /* non-fatal */ }

// =============================================================================
console.log('');
console.log('RESULT layer=t3-recall-integration PASS=' + PASS + ' FAIL=' + FAIL + ' SKIP=' + SKIP +
            ' exit=' + (FAIL > 0 ? 1 : 0));
