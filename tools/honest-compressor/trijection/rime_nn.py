#!/usr/bin/env python3
"""
rime_nn.py — the NEURAL frontier attempt: a compact char-level GRU byte-model
trained on enwik8 (CPU, torch), the honest technology that reaches toward the
Hutter frontier below the count-based floor. Operator: Jesse Daniel Brown.

Reports held-out bits-per-char (= bpc) periodically; checkpoints the model.
Honest: below-1 bpc is SOTA (big neural ensembles, GPU-days). This is a SMALL
CPU model — it will beat the order-k wall and probably the CM, and it maps the
neural trajectory honestly. Never below Shannon. The measurement is the referee.
"""
import time, json, math, os
import torch, torch.nn as nn

torch.manual_seed(27)
torch.set_num_threads(3)                      # leave a core for the CM job
S = "/tmp/claude-0/-home-user/9ebd6119-d7ee-5c30-a062-d04210f7bc39/scratchpad"
CORPUS = f"{S}/enwik9"
RECEIPT = f"{S}/rime_nn.jsonl"
NTRAIN = 100_000_000                          # enwik8-sized training span
NHELD  = 2_000_000
SEQ, BATCH, HID, EMB, LAYERS = 128, 64, 512, 128, 2
LR = 2e-3

raw = open(CORPUS, 'rb').read(NTRAIN + NHELD)
train = torch.frombuffer(bytearray(raw[:NTRAIN]), dtype=torch.uint8).long()
held  = torch.frombuffer(bytearray(raw[NTRAIN:NTRAIN+NHELD]), dtype=torch.uint8).long()

class GRUByte(nn.Module):
    def __init__(self):
        super().__init__()
        self.emb = nn.Embedding(256, EMB)
        self.gru = nn.GRU(EMB, HID, LAYERS, batch_first=True)
        self.out = nn.Linear(HID, 256)
    def forward(self, x, h=None):
        e = self.emb(x)
        y, h = self.gru(e, h)
        return self.out(y), h

model = GRUByte()
opt = torch.optim.Adam(model.parameters(), lr=LR)
lossf = nn.CrossEntropyLoss()
nparams = sum(p.numel() for p in model.parameters())

def log(o):
    with open(RECEIPT, 'a') as f: f.write(json.dumps(o) + "\n")
log(dict(event="start", params=nparams, seq=SEQ, batch=BATCH, hid=HID, layers=LAYERS,
         train_bytes=NTRAIN, held_bytes=NHELD, note="char GRU, CPU torch, held-out bpc"))
print(f"model params={nparams:,}  seq={SEQ} batch={BATCH} hid={HID}x{LAYERS}", flush=True)

@torch.no_grad()
def eval_bpc(nchunks=40):
    model.eval()
    tot_bits = 0.0; tot = 0; h = None
    step = SEQ
    for c in range(nchunks):
        i = c*step
        if i+SEQ+1 > len(held): break
        x = held[i:i+SEQ].unsqueeze(0); y = held[i+1:i+SEQ+1].unsqueeze(0)
        logits, h = model(x, h); h = h.detach()
        ll = lossf(logits.reshape(-1,256), y.reshape(-1))
        tot_bits += ll.item()*y.numel()/math.log(2); tot += y.numel()
    model.train()
    return tot_bits/tot

t0 = time.time(); step = 0; run = True
BUDGET = 5.5*3600
# contiguous BPTT: split train into BATCH streams
stream_len = (NTRAIN-1)//BATCH
streams = train[:BATCH*stream_len+1]
best = 9.9
pos = 0; h = None
while time.time()-t0 < BUDGET:
    # build batch of (BATCH, SEQ)
    if pos+SEQ+1 > stream_len:
        pos = 0; h = None
    xb = torch.stack([train[b*stream_len+pos : b*stream_len+pos+SEQ] for b in range(BATCH)])
    yb = torch.stack([train[b*stream_len+pos+1 : b*stream_len+pos+SEQ+1] for b in range(BATCH)])
    logits, h = model(xb, h); h = h.detach()
    loss = lossf(logits.reshape(-1,256), yb.reshape(-1))
    opt.zero_grad(); loss.backward()
    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
    opt.step()
    pos += SEQ; step += 1
    if step % 200 == 0:
        train_bpc = loss.item()/math.log(2)
        el = time.time()-t0
        print(f"[{el:6.0f}s] step {step:,}  train bpc {train_bpc:.4f}  "
              f"({step*BATCH*SEQ/el/1e3:.0f} KB/s)", flush=True)
    if step % 2000 == 0:
        hb = eval_bpc()
        el = time.time()-t0
        rec = dict(event="eval", t_s=round(el), step=step, heldout_bpc=round(hb,4),
                   seen_MB=round(step*BATCH*SEQ/1e6,1))
        log(rec)
        print(f"    >>> held-out bpc = {hb:.4f}  (seen {step*BATCH*SEQ/1e6:.0f} MB)", flush=True)
        if hb < best:
            best = hb; torch.save(model.state_dict(), f"{S}/rime_nn_best.pt")
            log(dict(event="best", step=step, heldout_bpc=round(hb,4)))
log(dict(event="done", best_heldout_bpc=round(best,4), steps=step, wall_s=round(time.time()-t0)))
print(f"\nDONE: best held-out bpc = {best:.4f} over {step:,} steps")
