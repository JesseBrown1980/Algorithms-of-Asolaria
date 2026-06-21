#!/usr/bin/env node
/* AoT-decided feed: write the ADDITIVE DISTRICT-F formula fabric feed into the office feed lane
 * (registered -> fed artifact). Does NOT overwrite the 726 feed, does NOT run the live :4949
 * feeder (live-roster ingestion stays a separate gated step). E=0 additive descriptor. */
const fs = require('fs'), crypto = require('crypto');
const RD = 'D:/PID-Registration-Office/registered';
const FEEDDIR = 'D:/PID-Registration-Office/fabric-feed';
const sha = s => crypto.createHash('sha256').update(s).digest('hex');
const rows = []; const seenPid = new Set(); let dups = 0;
for (const f of fs.readdirSync(RD)) {
  if (!/FORMULA.*CORPUS.*\.hbp$/i.test(f)) continue;
  for (const line of fs.readFileSync(RD + '/' + f, 'utf8').split('\n')) {
    if (!line.startsWith('FORMULA|')) continue;
    const g = k => { const m = line.match(new RegExp('\\|' + k + '=([^|]*)')); return m ? m[1] : ''; };
    const pid = g('PID'); if (!pid) continue;
    if (seenPid.has(pid)) { dups++; continue; } seenPid.add(pid);
    rows.push('REG|district=DISTRICT-F|name=' + (line.split('|')[1] || 'formula') + '|pid=' + pid +
      '|hilbert=' + (+g('HILBERT') || 0) + '|layer=formula|class=' + (g('CLASS') || 'formula') +
      '|g1024=' + (+g('GLYPH_BEHCS1024') || 0) + '|g5=' + (+g('GLYPH_BEHCS5') || 0) +
      '|sector=' + (g('SECTOR') || '') + '|role=DISTRICT-F-FORMULA-PID');
  }
}
const body = 'FEEDHDR|district=DISTRICT-F|kind=formula-pid-fabric-feed|rows=' + rows.length + '|registered=office|source=ACER-FORMULA-CORPUS|fed_at=2026-06-20|live_ingest=GATED|json=0\n' + rows.join('\n') + '\n';
const file = body + 'FEEDFTR|rows=' + rows.length + '|body_sha16=' + sha(body).slice(0, 16) + '|json=0\n';
const dest = FEEDDIR + '/district-f-formula-fabric-feed-2026-06-20.hbp';
fs.writeFileSync(dest, file, 'utf8');
fs.writeFileSync(dest + '.sha256', sha(file) + '  district-f-formula-fabric-feed-2026-06-20.hbp\n', 'utf8');
console.log('DISTRICT-F FEED (additive, registered->fed; live :4949 ingest = GATED next step):');
console.log('  ' + dest + '  rows=' + rows.length + '  file_sha16=' + sha(file).slice(0, 16) + '  CR=' + ((file.match(/\r/g) || []).length));
