import time, math
from collections import defaultdict
S="/tmp/claude-0/-home-user/9ebd6119-d7ee-5c30-a062-d04210f7bc39/scratchpad"
raw=open(f"{S}/enwik9",'rb').read(30_000_000)
held=raw[28_000_000:29_000_000]
KMAX=6
print(f"{'train':>7} | best backoff order (held-out bpc)")
print("-"*48)
for NT in (1_500_000, 6_000_000, 24_000_000):
    tr=raw[:NT]
    counts=[defaultdict(lambda:defaultdict(int)) for _ in range(KMAX+1)]
    tot=[defaultdict(int) for _ in range(KMAX+1)]
    for i in range(KMAX,NT):
        b=tr[i]
        for k in range(KMAX+1):
            c=tr[i-k:i]; counts[k][c][b]+=1; tot[k][c]+=1
    best=(99,0)
    row=[]
    for K in range(1,KMAX+1):
        bits=0.0
        for i in range(KMAX,len(held)):
            b=held[i]; p=None
            for k in range(K,-1,-1):
                c=held[i-k:i]; d=counts[k].get(c)
                if d is not None: p=(d.get(b,0)+1)/(tot[k][c]+256); break
            if p is None: p=1/256
            bits+=-math.log2(p)
        bpc=bits/(len(held)-KMAX); row.append(bpc)
        if bpc<best[0]: best=(bpc,K)
    print(f"{NT//1000000 or NT/1e6:>6}M | best=order-{best[1]}  ({best[0]:.4f})   curve: {[round(x,2) for x in row]}",flush=True)
