#!/usr/bin/env python3
# sphere_moe.py — Jesse's sphere ensemble as an honest neural network.
# Three (or N) separately-parameterized "spheres" (experts), a learned colored
# mirror (router) that decides how much each sphere speaks per position, and an
# optional rule-of-three refinement loop. Byte-level language model; the score
# is validation bits-per-character (bpc), same referee as the compressor line.
#
# Every organ has an ablation switch, so any seat that runs this measures what
# each part earns. No claim ships without its number.
#
#   python3 sphere_moe.py --data enwik8 --bytes 2000000            # full machine
#   python3 sphere_moe.py --data enwik8 --bytes 2000000 --no-router # uniform mix
#   python3 sphere_moe.py --data enwik8 --bytes 2000000 --experts 1 # one sphere
#   python3 sphere_moe.py --data enwik8 --bytes 2000000 --loops 1   # no recurrence
#
# CPU-friendly sizes by default; grows with --dim/--hidden on GPU seats.
import argparse, math, time
import torch
import torch.nn as nn
import torch.nn.functional as F

def get_args():
    p = argparse.ArgumentParser()
    p.add_argument('--data', required=True, help='path to a byte corpus (e.g. enwik8)')
    p.add_argument('--bytes', type=int, default=2_000_000, help='bytes of corpus to use')
    p.add_argument('--ctx', type=int, default=64)
    p.add_argument('--dim', type=int, default=64)
    p.add_argument('--hidden', type=int, default=128)
    p.add_argument('--experts', type=int, default=3, help='number of spheres')
    p.add_argument('--loops', type=int, default=3, help='rule-of-three refinement passes')
    p.add_argument('--no-router', action='store_true', help='ablate the mirror: uniform expert mix')
    p.add_argument('--steps', type=int, default=3000)
    p.add_argument('--batch', type=int, default=64)
    p.add_argument('--lr', type=float, default=3e-4)
    p.add_argument('--seed', type=int, default=1024)
    p.add_argument('--device', default='cuda' if torch.cuda.is_available() else 'cpu')
    return p.parse_args()

class Sphere(nn.Module):
    """One expert: a small GRU that reads the context window."""
    def __init__(self, dim, hidden):
        super().__init__()
        self.rnn = nn.GRU(dim, hidden, batch_first=True)
        self.out = nn.Linear(hidden, dim)
    def forward(self, x):                 # x: (B, T, dim)
        h, _ = self.rnn(x)
        return self.out(h)                # (B, T, dim)

class SphereMoE(nn.Module):
    def __init__(self, a):
        super().__init__()
        self.a = a
        self.emb = nn.Embedding(256, a.dim)
        self.spheres = nn.ModuleList(Sphere(a.dim, a.hidden) for _ in range(a.experts))
        # the colored mirror: routes per position over spheres
        self.mirror = nn.Linear(a.dim, a.experts)
        self.norm = nn.LayerNorm(a.dim)
        self.head = nn.Linear(a.dim, 256)
    def forward(self, idx):               # idx: (B, T) int64
        x = self.emb(idx)
        for _ in range(max(1, self.a.loops)):     # rule-of-three refinement
            outs = torch.stack([s(x) for s in self.spheres], dim=-2)  # (B,T,E,dim)
            if self.a.no_router:
                mix = outs.mean(dim=-2)
            else:
                gate = F.softmax(self.mirror(x), dim=-1)              # (B,T,E)
                mix = (outs * gate.unsqueeze(-1)).sum(dim=-2)
            x = self.norm(x + mix)                                    # residual refine
        return self.head(x)               # (B, T, 256)

def batches(data, ctx, batch, device, gen):
    n = data.size(0) - ctx - 1
    while True:
        ix = torch.randint(0, n, (batch,), generator=gen)
        x = torch.stack([data[i:i+ctx] for i in ix]).to(device)
        y = torch.stack([data[i+1:i+ctx+1] for i in ix]).to(device)
        yield x, y

def main():
    a = get_args()
    torch.manual_seed(a.seed)
    gen = torch.Generator().manual_seed(a.seed)
    raw = open(a.data, 'rb').read(a.bytes)
    data = torch.tensor(list(raw), dtype=torch.long)
    split = int(0.9 * len(data))
    train, val = data[:split], data[split:]
    model = SphereMoE(a).to(a.device)
    nparams = sum(p.numel() for p in model.parameters())
    opt = torch.optim.AdamW(model.parameters(), lr=a.lr)
    tb = batches(train, a.ctx, a.batch, a.device, gen)
    t0 = time.time()
    model.train()
    for step in range(1, a.steps + 1):
        x, y = next(tb)
        logits = model(x)
        loss = F.cross_entropy(logits.reshape(-1, 256), y.reshape(-1))
        opt.zero_grad(); loss.backward(); opt.step()
        if step % 500 == 0 or step == 1:
            print(f"step {step} train_bpc {loss.item()/math.log(2):.4f} ({time.time()-t0:.0f}s)", flush=True)
    # validation bpc — the referee number
    model.eval()
    vb = batches(val, a.ctx, a.batch, a.device, gen)
    tot, cnt = 0.0, 0
    with torch.no_grad():
        for _ in range(100):
            x, y = next(vb)
            logits = model(x)
            tot += F.cross_entropy(logits.reshape(-1, 256), y.reshape(-1), reduction='sum').item()
            cnt += y.numel()
    bpc = tot / cnt / math.log(2)
    cfg = f"experts={a.experts} loops={a.loops} router={not a.no_router}"
    print(f"RESULT sphere-moe {cfg} params={nparams} data={a.bytes} val_bpc={bpc:.4f} seed={a.seed}")

if __name__ == '__main__':
    main()
