#!/usr/bin/env node
/*
 * master-run.cjs — adversarial independent re-runner.
 *
 * Runs EACH C:/tmp/asolaria-tests/t*.cjs file with `node`, captures the
 * ACTUAL process exit code and stdout, parses the
 *   "RESULT ... PASS=n FAIL=m SKIP=k" line from the real output,
 * and prints a TOTAL line. The re-run is the source of truth — no
 * reported number is trusted; everything below is recomputed from this
 * fresh execution.
 */
'use strict';

const { spawnSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const DIR = __dirname; // C:/tmp/asolaria-tests
const files = fs.readdirSync(DIR)
  .filter(f => /^t.*\.cjs$/.test(f) && f !== 'master-run.cjs')
  .sort();

// RESULT layer=<name> PASS=<n> FAIL=<m> SKIP=<k> exit=<...>
const RESULT_RE = /RESULT\b.*?PASS=(\d+)\s+FAIL=(\d+)\s+SKIP=(\d+)/;

let totPass = 0, totFail = 0, totSkip = 0;
let anyMissingResult = false;
const rows = [];

for (const f of files) {
  const full = path.join(DIR, f);
  const res = spawnSync(process.execPath, [full], {
    encoding: 'utf8',
    timeout: 300000,
    maxBuffer: 64 * 1024 * 1024,
  });

  const stdout = res.stdout || '';
  const stderr = res.stderr || '';
  const combined = stdout + '\n' + stderr;

  // ACTUAL exit code from the spawned process (null if killed by signal/timeout)
  let exit = res.status;
  const killed = res.signal != null || res.error != null;

  const m = combined.match(RESULT_RE);
  let pass = null, fail = null, skip = null, hasResult = false;
  if (m) {
    hasResult = true;
    pass = parseInt(m[1], 10);
    fail = parseInt(m[2], 10);
    skip = parseInt(m[3], 10);
    totPass += pass;
    totFail += fail;
    totSkip += skip;
  } else {
    anyMissingResult = true;
  }

  rows.push({
    file: f,
    exit: exit,
    signal: res.signal || null,
    error: res.error ? String(res.error.message || res.error) : null,
    killed,
    hasResult,
    pass, fail, skip,
  });

  const exitStr = killed ? `KILLED(signal=${res.signal}${res.error ? ',err=' + (res.error.code || res.error.message) : ''})` : String(exit);
  if (hasResult) {
    console.log(`LAYER ${f}  exit=${exitStr}  PASS=${pass} FAIL=${fail} SKIP=${skip}`);
  } else {
    console.log(`LAYER ${f}  exit=${exitStr}  PASS=? FAIL=? SKIP=?  *** NO RESULT LINE FOUND ***`);
    if (stderr.trim()) {
      console.log('   stderr(tail): ' + stderr.trim().split('\n').slice(-3).join(' | '));
    }
  }
}

console.log('');
console.log(`TOTAL files=${files.length}  PASS=${totPass}  FAIL=${totFail}  SKIP=${totSkip}` +
            (anyMissingResult ? '  (WARNING: one or more layers emitted NO RESULT line)' : ''));

// Machine-readable block for downstream comparison.
console.log('JSON ' + JSON.stringify({
  files: files.length,
  total_pass: totPass,
  total_fail: totFail,
  total_skip: totSkip,
  any_missing_result: anyMissingResult,
  layers: rows,
}));
