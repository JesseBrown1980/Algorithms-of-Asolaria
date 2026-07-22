#!/usr/bin/env python3
"""Prequential retention simulator — fully charged, delayed-promotion convention.

Convention (fixed, per audit): the occurrence that reaches the threshold is
emitted RAW; promotion takes effect for subsequent events. The third
occurrence is therefore the first post-confirmation reuse opportunity.
Charges: raw misses, references, hot bodies+index, probation rows, and the
never-expiring exact replay ledger. Run from the repo root.
"""
import subprocess, hashlib, re, collections, json, sys

REF, IDX, PROB, LEDGER = 16, 64, 32, 16

def sh(cmd): return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout

def events():
    commits = sh("git log --reverse --format=%H").split()
    FUNC_RE = re.compile(r'(?:^|\n)(fn |def |function |    fn )', re.M)
    evs, prev = [], {}
    for c in commits:
        for path in sh(f"git diff-tree --no-commit-id --name-only -r {c}").split():
            if not path.endswith(('.rs','.py','.js','.mjs','.cjs')): continue
            blob = sh(f"git show {c}:{path} 2>/dev/null")
            if not blob: continue
            idxs = [m.start() for m in FUNC_RE.finditer(blob)]
            if not idxs: continue
            for si, ch in enumerate(blob[a:b] for a, b in zip(idxs, idxs[1:] + [len(blob)])):
                h = hashlib.sha256(ch.encode()).hexdigest()[:16]
                if prev.get((path, si)) != h:
                    prev[(path, si)] = h
                    evs.append({'commit': c[:12], 'path': path, 'hash': h, 'len': len(ch)})
    return evs

def run(evs, policy, tau=None):
    counts, dict_, probation, ledger = collections.Counter(), {}, set(), set()
    streamed, promos, curve = 0, [], []
    for i, e in enumerate(evs):
        h, l = e['hash'], e['len']
        ledger.add(h)
        if h in dict_:
            streamed += REF
        else:
            streamed += l
            counts[h] += 1
            promote = (policy == 'fixed' and counts[h] >= tau) or \
                      (policy == 'adaptive' and counts[h] >= 2 and counts[h]*(l-REF) > (l+IDX+PROB))
            if promote:
                dict_[h] = l; probation.discard(h)
                promos.append({'event_idx': i, 'hash': h, 'len': l,
                               'count_at_promotion': counts[h],
                               'triggering_provenance': {'commit': e['commit'], 'path': e['path']},
                               'triggering_occurrence_was': 'raw'})
            elif counts[h] >= 1 and (policy == 'adaptive' or (tau and tau > 1)):
                probation.add(h)
        if i % 50 == 0 or i == len(evs)-1:
            st = sum(dict_.values()) + len(dict_)*IDX + len(probation)*PROB + len(ledger)*LEDGER
            curve.append({'event': i, 'streamed_plus_state': streamed + st})
    state = {'hot_bodies': sum(dict_.values()), 'index': len(dict_)*IDX,
             'probation': len(probation)*PROB, 'replay_ledger': len(ledger)*LEDGER}
    return {'total': streamed + sum(state.values()), 'state_bytes': state,
            'promotions': promos, 'cumulative_curve': curve}

evs = events()
base = run(evs, 'fixed', tau=10**9)
out = {'convention': 'delayed-promotion: triggering occurrence raw; third occurrence = first monetizable reuse',
       'charges': {'ref': REF, 'index': IDX, 'probation_row': PROB, 'ledger_entry': LEDGER},
       'events': len(evs), 'baseline_no_dict_total': base['total'], 'policies': {}}
for tau in range(1, 9):
    r = run(evs, 'fixed', tau=tau)
    out['policies'][f'fixed_tau_{tau}'] = {'total': r['total'], 'vs_baseline': base['total']-r['total'],
        'promoted': len(r['promotions']), 'state_bytes': r['state_bytes'],
        'promotions': r['promotions'] if tau == 2 else len(r['promotions']),
        'cumulative_curve': r['cumulative_curve'] if tau == 2 else None}
g = run(evs, 'adaptive')
t2 = run(evs, 'fixed', tau=2)
set2, setg = {p['hash'] for p in t2['promotions']}, {p['hash'] for p in g['promotions']}
times2 = {p['hash']: p['event_idx'] for p in t2['promotions']}
timesg = {p['hash']: p['event_idx'] for p in g['promotions']}
out['policies']['adaptive_governor'] = {'total': g['total'], 'vs_baseline': base['total']-g['total'],
    'promoted': len(g['promotions']), 'state_bytes': g['state_bytes'], 'promotions': g['promotions'],
    'governor_extra_state_charged': 0,
    'note': 'governor params are 3 integers; charged 0 here — flagged, must be charged in production'}
out['tau2_vs_governor'] = {'promotion_set_equal': set2 == setg,
    'only_tau2': sorted(set2-setg), 'only_governor': sorted(setg-set2),
    'promotion_time_disagreements': [{'hash': h, 'tau2_event': times2[h], 'gov_event': timesg[h]}
                                     for h in sorted(set2 & setg) if times2[h] != timesg[h]]}
blob = json.dumps(out, indent=1, sort_keys=True)
open('tools/honest-compressor/function-memory/prequential-receipt.json','w').write(blob)
print(f"receipt written: {len(blob):,} bytes, sha16={hashlib.sha256(blob.encode()).hexdigest()[:16]}")
print(f"set_equal={out['tau2_vs_governor']['promotion_set_equal']} time_disagreements={len(out['tau2_vs_governor']['promotion_time_disagreements'])}")
for k in ['fixed_tau_2','fixed_tau_3','fixed_tau_5','adaptive_governor']:
    p = out['policies'][k]; print(f"{k}: vs_baseline={p['vs_baseline']:+,} promoted={p['promoted']}")
