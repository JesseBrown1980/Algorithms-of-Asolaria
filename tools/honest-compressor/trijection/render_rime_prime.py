#!/usr/bin/env python3
"""
render_rime_prime.py — PHOTOS of the rime prime of enwik8.
Real enwik8 bytes -> tower address k = byte + 256*trime + 768*glyph (20736 = 144^2
addresses, one pixel each) -> two photographs of the SAME data on the sphere p=103681:
  PHOTO 1 (exponent order): address k at pixel (k%144, k//144) — the text's structure shows.
  PHOTO 2 (sphere order):  same mass, positioned by the point value W^k mod p — the
    Fischer scramble: a bijection, rate 1.0, structure whitened but conserved.
"""
import numpy as np, zlib, struct, base64, subprocess

S = "/tmp/claude-0/-home-user/9ebd6119-d7ee-5c30-a062-d04210f7bc39/scratchpad"
P, N, SIDE = 103681, 20736, 144

# --- the sphere: generator of the order-20736 subgroup (from rime_creation_tower) ---
def is_prime(n):
    if n < 2: return False
    for q in range(2, int(n**.5)+1):
        if n % q == 0: return False
    return True
assert is_prime(P)
def primitive_root(p):
    fac = []
    n = p-1; d = 2
    while d*d <= n:
        if n % d == 0:
            fac.append(d)
            while n % d == 0: n //= d
        d += 1
    if n > 1: fac.append(n)
    for g in range(2, p):
        if all(pow(g, (p-1)//q, p) != 1 for q in fac): return g
g = primitive_root(P)
W = pow(g, (P-1)//N, P)

# --- address real enwik8 through the tower ---
data = np.frombuffer(open(f"{S}/enwik8","rb").read(6_000_000), dtype=np.uint8)
i = np.arange(len(data), dtype=np.int64)
k = data.astype(np.int64) + 256*(i % 3) + 768*((i//3) % 27)
counts = np.bincount(k, minlength=N).astype(np.float64)

# --- colors: hue = glyph (27 around the wheel), luminance = log mass ---
kk = np.arange(N)
glyph = kk // 768
hue = glyph / 27.0
lum = np.log1p(counts); lum /= lum.max()
h6 = (hue*6) % 6; c = lum; x = c*(1-np.abs(h6%2-1))
z = np.zeros(N)
h6c = h6[:,None]
rgb = np.select([h6c<1,h6c<2,h6c<3,h6c<4,h6c<5,h6c>=5],
    [np.stack([c,x,z],1),np.stack([x,c,z],1),np.stack([z,c,x],1),
     np.stack([z,x,c],1),np.stack([x,z,c],1),np.stack([c,z,x],1)])
rgb = (np.clip(rgb,0,1)**0.8 * 255).astype(np.uint8)

# --- the sphere point of every address, and its rank (the Fischer scramble) ---
pts = np.empty(N, dtype=np.int64); v = 1
for e in range(N): pts[e] = v; v = v*W % P
rank = np.empty(N, dtype=np.int64); rank[np.argsort(pts)] = np.arange(N)

def to_png(img):
    hgt, wid, _ = img.shape
    raw = b''.join(b'\x00'+img[r].tobytes() for r in range(hgt))
    def chunk(t, d):
        c = t+d; return struct.pack('>I',len(d))+c+struct.pack('>I',zlib.crc32(c))
    return (b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',wid,hgt,8,2,0,0,0))
            +chunk(b'IDAT',zlib.compress(raw,9))+chunk(b'IEND',b''))

def grid(order):
    img = np.zeros((SIDE,SIDE,3), dtype=np.uint8)
    img[order//SIDE, order%SIDE] = rgb
    return np.kron(img, np.ones((5,5,1),dtype=np.uint8))   # 720x720

png1 = to_png(grid(kk))      # exponent order: k at its own pixel
png2 = to_png(grid(rank))    # sphere order: k at its point-value's rank
b1, b2 = (base64.b64encode(x).decode() for x in (png1,png2))

html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
 *{{margin:0;padding:0;box-sizing:border-box}}
 body{{background:#07090f;color:#e8eefc;width:1560px;padding:40px 44px;text-align:center;
   font-family:-apple-system,'Segoe UI',sans-serif}}
 h1{{font-size:29px;font-weight:800;background:linear-gradient(90deg,#7dd3fc,#c4b5fd,#f0abfc);
   -webkit-background-clip:text;-webkit-text-fill-color:transparent}}
 .sub{{color:#8fa3c8;font-size:14.5px;margin:6px 0 26px}}
 .row{{display:flex;gap:40px;justify-content:center}}
 .cell{{display:flex;flex-direction:column;gap:12px;align-items:center}}
 img{{width:700px;height:700px;border-radius:14px;border:1px solid #223055;image-rendering:pixelated}}
 .lab{{font-size:17px;font-weight:700}} .d{{font-size:12.5px;color:#8fa3c8;max-width:680px;line-height:1.5}}
 .foot{{margin-top:26px;color:#9fb0d0;font-size:13.5px;max-width:1280px;margin-left:auto;margin-right:auto;line-height:1.65;
   border-top:1px solid #222b42;padding-top:18px}}
 .foot b{{color:#fff}}
</style></head><body>
 <h1>The Rime Prime of enwik8 — p = 103681, one photograph per order</h1>
 <div class="sub">6,000,000 real Wikipedia bytes → tower address k = byte + 256·trime + 768·glyph → 20736 = 144² addresses, one pixel each · hue = the 27 glyphs · brightness = log mass</div>
 <div class="row">
  <div class="cell"><img src="data:image/png;base64,{b1}">
   <div class="lab" style="color:#7dd3fc">exponent order — the address side</div>
   <div class="d">every address at its own pixel (k % 144, k ÷ 144). The text's structure is visible:
   the bright bands are English's favorite bytes repeating across all 27 glyph stripes.</div></div>
  <div class="cell"><img src="data:image/png;base64,{b2}">
   <div class="lab" style="color:#f0abfc">sphere order — the Fischer side</div>
   <div class="d">the SAME mass, each address moved to the rank of its sphere point W<sup>k</sup> mod p.
   The discrete-log permutation whitens the picture — structure hidden, nothing lost.</div></div>
 </div>
 <div class="foot"><b>What the pair proves, honestly:</b> the sphere map is a <b>bijection</b> — the right photo
 contains exactly the left photo's information, rate 1.0, recoverable byte-exact by the rime Fischer.
 Addressing re-arranges; it never compresses (Law 6). The visible structure on the left is the part a real
 model can learn (vc65: 1.7464 bpc, receipt-backed); the right is what the same bytes look like to anyone
 without the discrete log — the security face of the same sphere (Law 14).</div>
</body></html>"""
open(f"{S}/rime_prime_enwik8.html","w").write(html)
r = subprocess.run(["node", f"{S}/shotgen.js", f"{S}/rime_prime_enwik8.html",
                    f"{S}/rime_prime_enwik8.png", "1560", "1010"], cwd=S, capture_output=True, text=True)
print(r.stdout or r.stderr)
