#!/usr/bin/env python3
"""Local Feasible-Set Quantization Hypothesis — Gate 1 (counting-model arms).

Synthetic packet universe: 3 color x 3 time x 3 space regimes, balanced.
Space sets the feasible set F (open=3, boundary=2, wall=1); color+time score
within F. Online counting predictors (encoder/decoder symmetric).
Arms: unmasked / masked-derivable / masked-transmitted;
      one shared pool vs 27 regime tables (oracle routing).
Claims tested: (1) mask accounting decides whether constraints earn,
(2) hard veto earns iff it doesn't hurt valid predictions,
(3) 27 regimes earn vs one pool (counting analogue).
Deterministic: seeded PRNG, no wall clock.
"""
import math, random, itertools, collections, json, hashlib

random.seed(27)
N = 27000  # 1000 events per regime
events = []
regimes = list(itertools.product(range(3), range(3), range(3)))  # (c,t,s)
for c, t, s in regimes:
    F = {0: [0,1,2], 1: [0,1], 2: [c % 3 if True else 0]}[s] if s != 2 else [c]
    F = [0,1,2] if s == 0 else ([0,1] if s == 1 else [c])
    for i in range(N // 27):
        # energy: color prefers dir c; time modifies: stable=keep, drift=rotate by i//50, reset=uniform
        pref = c if t == 0 else (c + i // 50) % 3 if t == 1 else None
        w = [1.0, 1.0, 1.0]
        if pref is not None: w[pref] = 6.0
        wf = [w[a] if a in F else 0.0 for a in range(3)]
        tot = sum(wf)
        r = random.random() * tot
        a = 0
        acc = 0
        for d in range(3):
            acc += wf[d]
            if r <= acc: a = d; break
        events.append((c, t, s, tuple(F), a))
random.shuffle(events)

def run(masked, charge_mask, pooled):
    counts = collections.defaultdict(lambda: [1, 1, 1])  # laplace
    bits = 0.0
    viol = 0
    for c, t, s, F, a in events:
        key = 'pool' if pooled else (c, t, s)
        cnt = counts[key]
        if masked:
            tot = sum(cnt[d] for d in F)
            p = cnt[a] / tot
        else:
            tot = sum(cnt)
            p = cnt[a] / tot
            top = max(range(3), key=lambda d: cnt[d])
            if top not in F: viol += 1
        bits += -math.log2(p)
        if charge_mask: bits += math.log2(3)  # transmit spatial regime (3 states)
        cnt[a] += 1
    return bits, viol

arms = {}
arms['A_unmasked_pool']        = run(False, False, True)
arms['B_unmasked_27']          = run(False, False, False)
arms['C_masked_derivable_pool']= run(True,  False, True)
arms['D_masked_derivable_27']  = run(True,  False, False)
arms['E_masked_transmitted_27']= run(True,  True,  False)

out = {'events': len(events), 'regimes': 27,
       'feasible_bound_bits': {'open': math.log2(3), 'boundary': 1.0, 'wall': 0.0},
       'arms': {k: {'total_bits': round(v[0], 1), 'bpe': round(v[0]/len(events), 4),
                    'forbidden_top1_violations': v[1]} for k, v in arms.items()}}
blob = json.dumps(out, indent=1, sort_keys=True)
open('tools/cts-quantization/gate1-receipt.json', 'w').write(blob)
print(blob)
print('receipt sha16:', hashlib.sha256(blob.encode()).hexdigest()[:16])
