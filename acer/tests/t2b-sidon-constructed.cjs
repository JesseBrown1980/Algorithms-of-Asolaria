#!/usr/bin/env node
/* t2b — POSITIVE Sidon-tower test: 0 collisions UNDER the correct construction.
 * t2 proved the property FAILS for a naive x_i=c_i*sqrt(p_i) with unconstrained small c_i
 * (1.7M collisions). This test proves it HOLDS under the canon construction:
 *   STE super-increasing anchor band (REPORT §4.1 Part C): anchor_{k} on a dedicated
 *   dominant axis, super-increasing => the anchor set is a Sidon (B2) set => all pairwise
 *   |a_k-a_j| distinct => squared anchor distances distinct; scale by GUARD>maxIntra so the
 *   bounded within-tower coords can never bridge two anchor bands. d^2 exact via BigInt.
 * If this is distinct-for-all-pairs, the 0-collision certificate is CONSTRUCTED, not generic.
 */
const P = [2,3,5,7,11,13,17,19,23,29,31,37]; // 12 within-tower (intra) dims
const pDom = 73n;                            // dominant-axis prime
const N = 400;
let pass = 0, fail = 0;
const chk = (c, label) => { if (c) { pass++; console.log('  PASS  ' + label); } else { fail++; console.log('  FAIL  ' + label); } };

// maxIntra = upper bound on any pair's within-tower squared contribution
let maxIntra = 0n;
for (const p of P) { const pb = BigInt(p); maxIntra += pb * BigInt((p - 1) * (p - 1)); }
const GUARD = maxIntra + 1n;

// super-increasing anchors a_k = GUARD * 3^k  (3^k is super-increasing => Sidon set)
const anchors = []; let pw = 1n;
for (let k = 0; k < N; k++) { anchors.push(GUARD * pw); pw *= 3n; }

// within-tower coords: deterministic small digits c_i in [0, p_i-1]
function intra(idx) { const v = []; for (let i = 0; i < P.length; i++) v.push((idx * 31 + i * 7) % P[i]); return v; }
const coords = []; for (let k = 0; k < N; k++) coords.push(intra(k));

// all pairwise exact squared distances d^2 = pDom*(a_i-a_j)^2 + sum p_i*(c_i-c_j)^2
const seen = new Set(); let pairs = 0, collisions = 0, firstCol = null;
for (let i = 0; i < N; i++) {
  for (let j = i + 1; j < N; j++) {
    const da = anchors[i] - anchors[j];
    let d2 = pDom * da * da;
    for (let t = 0; t < P.length; t++) { const dc = BigInt(coords[i][t] - coords[j][t]); d2 += BigInt(P[t]) * dc * dc; }
    pairs++;
    const key = d2.toString();
    if (seen.has(key)) { collisions++; if (!firstCol) firstCol = [i, j]; } else seen.add(key);
  }
}
const expectedPairs = N * (N - 1) / 2;
console.log('CONSTRUCTION: STE super-increasing anchors a_k=GUARD*3^k, GUARD=' + GUARD + ' (>maxIntra=' + maxIntra + '), ' + P.length + ' intra dims, N=' + N);
console.log('pairs=' + pairs + '  distinct=' + seen.size + '  collisions=' + collisions + (firstCol ? '  first@(' + firstCol + ')' : ''));
chk(pairs === expectedPairs, 'pair_count == C(N,2) == ' + expectedPairs);
chk(collisions === 0, 'ZERO collisions under STE construction (exact BigInt squared distances)');
chk(seen.size === expectedPairs, 'distinct_count == pair_count (' + seen.size + ' == ' + expectedPairs + ')');
// contrast assertion: the construction is the REASON (GUARD dominates intra band)
chk(GUARD > maxIntra, 'GUARD (' + GUARD + ') strictly dominates maxIntra (' + maxIntra + ') — bands cannot bridge');

const exit = fail === 0 ? 0 : 1;
console.log('RESULT layer=t2b-sidon-constructed PASS=' + pass + ' FAIL=' + fail + ' SKIP=0 exit=' + exit);
process.exitCode = exit;
