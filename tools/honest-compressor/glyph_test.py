#!/usr/bin/env python3
# Trained-glyph test for the honest-compressor lane.
# Answers the question: does a LARGER trained glyph vocabulary (1024 / 4096),
# rather than a 256-byte alphabet, lower cm2's byte-exact total on real text?
#
# Two tokenizers, both TRAINED on the corpus and both SHIPPED+COUNTED:
#   - bpe   : greedy merges (as in cm_asolaria), dictionary = varint merge pairs
#   - unigram: sentencepiece unigram-LM vocab; dictionary = the id->bytes table,
#              length-prefixed varints (exactly what the decoder needs, nothing else)
#
# The model over the glyph stream is cm2 (bitwise logistic mixing + APM + match).
# Honesty gates unchanged: total = payload + decoder + dictionary, byte-exact;
# SHA-256 restore using ONLY the shipped table or the run is invalid; no external
# data at decode; nothing below entropy is claimed. If a bigger vocabulary makes
# total bpc dive toward zero on distinct text, that is the dictionary smuggling
# content, not compression — the floor N*H(X) does not move.
import hashlib, os, sys, time
import cm2_asolaria as cm2

def varint(v):
    b = bytearray()
    while True:
        c = v & 0x7F; v >>= 7
        if v: b.append(c | 0x80)
        else: b.append(c); break
    return bytes(b)

# ---- BPE front end: reuse cm2's trained merges, ship varint pairs ----
def tok_bpe(data, n_merges):
    seq, merges = cm2.bpe_train(data, n_merges)
    dict_b = cm2.merges_bytes(merges)
    def decode(ids):
        return cm2.bpe_decode(ids, merges)
    return seq, 256 + len(merges), dict_b, decode

# ---- Unigram (sentencepiece) front end: ship id->bytes table ----
def tok_unigram(data, vocab_size, tag):
    import sentencepiece as spm
    txt = f"corpus_{tag}.txt"; open(txt, "wb").write(data)
    model_prefix = f"uni_{tag}_{vocab_size}"
    if not os.path.exists(model_prefix + ".model"):
        spm.SentencePieceTrainer.train(
            input=txt, model_prefix=model_prefix, vocab_size=vocab_size,
            model_type="unigram", character_coverage=1.0, byte_fallback=True,
            add_dummy_prefix=False, normalization_rule_name="identity",
            treat_whitespace_as_suffix=False, remove_extra_whitespaces=False,
            hard_vocab_limit=False, bos_id=-1, eos_id=-1, unk_id=0, pad_id=-1)
    sp = spm.SentencePieceProcessor(model_file=model_prefix + ".model")
    # id -> raw bytes table (byte-fallback pieces decode to exact bytes)
    text = data.decode("utf-8")            # native encoding of the corpus
    ids = sp.encode(text, out_type=int)
    V = sp.get_piece_size()
    id2bytes = []
    for i in range(V):
        p = sp.id_to_piece(i)
        if p.startswith("<0x") and p.endswith(">"):
            id2bytes.append(bytes([int(p[3:5], 16)]))
        else:
            id2bytes.append(p.replace("▁", " ").encode("utf-8"))
    # verify tokenizer is exactly invertible on THIS corpus; else fall back to bytes
    recon = b"".join(id2bytes[i] for i in ids)
    if recon != data:
        return None
    # shipped dictionary = length-prefixed id->bytes table (what decode needs)
    tbl = bytearray()
    for bs in id2bytes:
        tbl += varint(len(bs)) + bs
    dict_b = len(tbl)
    def decode(seq_ids):
        return b"".join(id2bytes[i] for i in seq_ids)
    return ids, V, dict_b, decode

def run(path, kind, param, k):
    data = open(path, "rb").read()
    N = len(data); sha_in = hashlib.sha256(data).hexdigest()
    t0 = time.time()
    if kind == "bpe":
        front = tok_bpe(data, param)
    else:
        front = tok_unigram(data, param, tag=os.path.basename(path).split(".")[0])
    if front is None:
        print(f"{kind}:{param} k={k}  tokenizer NOT byte-invertible on corpus -> REJECT", flush=True)
        return None
    seq, V, dict_b, decode = front
    tok_s = time.time() - t0
    t1 = time.time(); comp = cm2.compress(seq, V, k); enc_s = time.time() - t1
    t2 = time.time(); seq2 = cm2.decompress(comp, len(seq), V, k)
    body = decode(seq2); dec_s = time.time() - t2
    ok = hashlib.sha256(body).hexdigest() == sha_in
    decoder_b = os.path.getsize(os.path.abspath("cm2_asolaria.py")) + os.path.getsize(os.path.abspath(__file__))
    payload = len(comp); total = payload + dict_b + decoder_b
    chars_per_glyph = N / len(seq)
    bits_per_glyph = payload * 8 / len(seq)          # looks LOW; measured over fewer symbols
    bpc_char = total * 8 / N                          # the HONEST number: per original byte
    line = (f"glyph {kind:7s} V={V:5d} k={k} glyphs={len(seq):7d} "
            f"payload={payload:7d} dict={dict_b:6d} decoder={decoder_b} "
            f"total={total:7d}  bits/glyph={bits_per_glyph:.3f} chars/glyph={chars_per_glyph:.2f}  "
            f"BPC_CHAR={bpc_char:.4f}  "
            f"restore={'OK' if ok else 'FAIL'}  tok={tok_s:.0f}s enc={enc_s:.0f}s dec={dec_s:.0f}s")
    print(line, flush=True)
    with open("glyph-sweep.log", "a") as f:
        f.write(line + "\n")
    return line

if __name__ == "__main__":
    path = sys.argv[1]
    for spec in sys.argv[2:]:
        kind, param, k = spec.split(":")
        run(path, kind, int(param), int(k))
