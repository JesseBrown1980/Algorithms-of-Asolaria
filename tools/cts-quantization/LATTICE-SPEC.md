# 27-Cell Identity Lattice — alignment spec for the trilateral overlay

So the three seats' grids overlay cell-for-cell. This seat's FUNCTIONS-WORLD
27 is ALREADY SEALED (RESULTS-cloud-seat.md, commit-tagged); any second run
of the functions world is the REPLICATION arm — welcome, but use this spec
exactly or the subsumption math breaks.

## Corpus (functions world)
fleet1m.bin = first 1,000,000 bytes of the white-room dedup'd fleet corpus
(corpus sha16 567da5c5d3f185bd); fleet1m sha16 8fff365b2487839e.
Events: predict byte i from axes computed at i−1, for i in 1..999,999.

## Axis encoders (exact)
cls(b): letters=0, digits=1, ws(32,10,9)=2, markup(60,62,38,91,93,123,125,
124,61,34)=3, >=128 ->4, else 5.
COLOR: off=() | coarse=(cls(prev),) | fine=(prev_byte,)
TIME:  off=() | coarse=(prev==prev2,) | fine=((2 if prev==prev2 else 0) +
       (1 if cls(prev2)==cls(prev) else 0),)   # 4 states
SPACE: col=0 after newline else col+1 (computed BEFORE event i, i.e. the
       column of byte i). off=() | coarse=(col==0,) | fine=(min(col//8,7),)
Key = COLOR ++ TIME ++ SPACE (tuple concat, that order).

## Predictor
Online Laplace counting over 256 symbols: p = (count[y]+1)/(total+256),
bits += −log2 p, THEN update. Single pass, stream order, no shuffle.
Score = bits / 999,999 (bits per byte). Empty container = 5.4899 bpb.

## Reference grid (this seat, gains vs empty)
(C,T,S) with 0=off 1=coarse 2=fine:
(0,0,1)+.0332 (0,0,2)+.2178 (0,1,0)+.1081 (0,1,1)+.1498 (0,1,2)+.2882
(0,2,0)+.1862 (0,2,1)+.2278 (0,2,2)+.3891 (1,0,0)+.5663 (1,0,1)+.5826
(1,0,2)+.7433 (1,1,0)+.6188 (1,1,1)+.6463 (1,1,2)+.7749 (1,2,0)+.7266
(1,2,1)+.7646 (1,2,2)+.8771 (2,0,0)+1.3975 (2,0,1)+1.3975 (2,0,2)+1.4071
(2,1,0)+1.4619 (2,1,1)+1.4619 (2,1,2)+1.4202 (2,2,0)+1.6109 BEST
(2,2,1)+1.6109 (2,2,2)+1.4685
Anchor cells for byte-exact replication: (0,0,0)=5.4899 bpb;
(2,0,1)−(2,0,0)=+0.0000 (subsumption); (2,2,2)−(2,2,0)=−0.1424 (dilution).

## Overlay rule
A cell property is a LAW OF THE LATTICE if its sign/ordering holds in all
three worlds (packet/text/functions); otherwise it is a law of that world.
