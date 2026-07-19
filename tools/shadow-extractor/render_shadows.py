import numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

cost = np.frombuffer(open('cost10m.bin','rb').read(), dtype='<u2').astype(np.float64)/100.0  # centibits->bits
data = np.frombuffer(open('../slice10M.txt','rb').read(), dtype=np.uint8)
order=11; side=1<<order; TILE=side*side  # 2048^2 = 4,194,304
c=cost[:TILE]; b=data[:TILE]

def hilbert_vec(order, d):
    n=1<<order; x=np.zeros_like(d); y=np.zeros_like(d); t=d.copy(); s=1
    while s<n:
        rx=1&(t//2); ry=1&(t^rx)
        swap=ry==0; flip=swap&(rx==1)
        x=np.where(flip,s-1-x,x); y=np.where(flip,s-1-y,y)
        xs=np.where(swap,y,x); ys=np.where(swap,x,y); x,y=xs,ys
        x=x+s*rx; y=y+s*ry; t//=4; s<<=1
    return x,y
d=np.arange(TILE); hx,hy=hilbert_vec(order,d)

def render(vals, cmap, title, fname, vmin=None, vmax=None, cats=None):
    img=np.zeros((side,side)); img[hy,hx]=vals
    fig,ax=plt.subplots(figsize=(8,8),dpi=110)
    im=ax.imshow(img,cmap=cmap,interpolation='nearest',vmin=vmin,vmax=vmax)
    ax.set_title(title,fontsize=10); ax.set_xticks([]); ax.set_yticks([])
    if cats: 
        from matplotlib.patches import Patch
        ax.legend(handles=[Patch(color=cm,label=nm) for nm,cm in cats],loc='upper right',fontsize=7,framealpha=0.8)
    else:
        cb=fig.colorbar(im,ax=ax,fraction=0.046,pad=0.04)
    fig.tight_layout(); fig.savefig(fname,bbox_inches='tight'); plt.close()
    print("wrote",fname)

# a. prediction-loss
render(np.clip(c,0,8),'viridis','a. prediction-loss shadow (cm3ti bits/byte) — enwik8 10MB distinct tile\nbright = model paid most; NOT a compression claim, a lens','shadow_a_loss.png',0,8)

# b. local entropy (order-0, per 256 block, broadcast)
W=256; nb=TILE//W; ent=np.zeros(TILE)
bb=b[:nb*W].reshape(nb,W)
for i in range(nb):
    _,cnts=np.unique(bb[i],return_counts=True); p=cnts/W; ent[i*W:(i+1)*W]=-(p*np.log2(p)).sum()
render(ent,'magma','b. local entropy (order-0, 256B window)','shadow_b_entropy.png',0,8)

# c. byte-class hues
cls=np.zeros(TILE,dtype=int)
cls[(b>=65)&(b<=90)|(b>=97)&(b<=122)]=1   # letters
cls[(b>=48)&(b<=57)]=2                      # digits
cls[(b==32)|(b==10)|(b==9)]=3              # whitespace
mk=np.isin(b,[60,62,38,91,93,123,125,124,61,34]); cls[mk]=4  # markup <>&[]{}|="
cls[b>=128]=5                               # high byte
palette=['#111111','#4C9F70','#E0B33A','#2C3E50','#D1495B','#8E44AD']
names=['other','letter','digit','whitespace','markup','high-byte']
render(cls.astype(float),ListedColormap(palette),'c. byte-class map','shadow_c_class.png',0,5,
       cats=list(zip(names,palette)))

# d. match-distance (log2 dist to last 8-byte match)
md=np.zeros(TILE); last={}
vb=b.tobytes()
for i in range(TILE-8):
    key=vb[i:i+8]; pv=last.get(key)
    if pv is not None: md[i]=np.log2(i-pv+1)
    last[key]=i
render(np.clip(md,0,24),'cividis','d. match-distance (log2 dist to last 8-byte match)','shadow_d_match.png',0,24)
print("ALL 4 SHADOWS RENDERED")
