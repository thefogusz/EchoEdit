"""Thai caption + audio helpers.

words_from_whisper(json)   -> [{text,start,end}]  (re-segmented with PyThaiNLP)
words_from_scribe(json)    -> same, from ElevenLabs Scribe output
chunk(words, ...)          -> [{start,end,words:[{text,start,end,hl,space}]}]
envelope(wav, fps)         -> [0..1] loudness per video frame (mouth driver)
"""
import json, re, wave
import numpy as np
from pythainlp.tokenize import word_tokenize

THAI = re.compile(r"[฀-๿]")
PUNCT = re.compile(r"[.!?…,\"“”'‘’]+")  # spoken captions drop sentence punctuation


def _split_timed(text, start, end):
    """Split one timed span into Thai words; share the time by character count."""
    toks = [t for t in word_tokenize(text, engine="newmm", keep_whitespace=True)]
    out, n = [], sum(len(t) for t in toks) or 1
    t = start
    space = False
    for tok in toks:
        d = (end - start) * len(tok) / n
        if tok.isspace():
            space = True; t += d; continue
        tok = PUNCT.sub("", tok)
        if not tok:
            t += d; continue
        out.append({"text": tok, "start": round(t, 3), "end": round(t + d, 3), "space": space})
        space = False; t += d
    return out


def words_from_whisper(path):
    d = json.load(open(path, encoding="utf-8"))
    words = []
    for seg in d["segments"]:
        for w in seg.get("words", []):
            words += _split_timed(w["word"].strip(), w["start"], w["end"]) if w["word"].strip() else []
    return _merge_fragments(words)


def words_from_scribe(items):
    """items: [{text,start,end,type?}] from Scribe; spacing entries are dropped."""
    words = []
    for w in items:
        if w.get("type") in ("spacing", "audio_event") or not w["text"].strip():
            if words: words[-1]["_gap_after"] = True
            continue
        words += _split_timed(w["text"].strip(), w["start"], w["end"])
        if words and len(words) > 1 and words[-2].get("_gap_after"):
            words[-1]["space"] = True
    for w in words: w.pop("_gap_after", None)
    return _merge_fragments(words)


def char_timeline(items):
    """[(char, start, end)] from Scribe items of any granularity (phrase or per-character)."""
    out = []
    for w in items:
        if w.get("type", "word") != "word" or w["text"].startswith("["):
            continue
        t, n = w["text"], max(1, len(w["text"]))
        for i, ch in enumerate(t):
            if ch.isspace():
                continue
            a = w["start"] + (w["end"] - w["start"]) * i / n
            out.append((ch, round(a, 3), round(a + (w["end"] - w["start"]) / n, 3)))
    return out


def is_char_level(items):
    ws = [w for w in items if w.get("type", "word") == "word"]
    return bool(ws) and sum(len(w["text"]) for w in ws) / len(ws) < 3


def words_from_char_units(items, fixes=None, gap=0.18):
    """Per-character Scribe output -> Thai words. Pauses > gap split runs; PyThaiNLP segments each run."""
    # Thai items are glued into runs (split on pauses); Latin/number items stay whole words.
    runs, cur = [], []
    for w in items:
        if w.get("type", "word") != "word" or w["text"].startswith("["):
            continue
        thai = bool(THAI.search(w["text"]))
        if not thai:
            if cur: runs.append(cur); cur = []
            runs.append([(w["text"], w["start"], w["end"], "latin")])
            continue
        if cur and w["start"] - cur[-1][2] > gap:
            runs.append(cur); cur = []
        cur += char_timeline([w])
    if cur: runs.append(cur)
    words = []
    for r in runs:
        if len(r[0]) == 4:  # whole Latin word
            tok = PUNCT.sub("", r[0][0]) if not re.fullmatch(r"[\d.]+%?", r[0][0]) else r[0][0]
            if tok: words.append({"text": tok, "start": r[0][1], "end": r[0][2], "space": bool(words)})
            continue
        text = "".join(c[0] for c in r)
        i, first = 0, True
        for tok in word_tokenize(text, engine="newmm", keep_whitespace=False):
            seg = r[i:i + len(tok)]; i += len(tok)
            tok2 = PUNCT.sub("", tok)
            if tok2 and seg:
                words.append({"text": tok2, "start": seg[0][1], "end": seg[-1][2], "space": first and bool(words)})
                first = False
    for k, v in (fixes or {}).items():
        for w in words:
            if w["text"] == k: w["text"] = v
    return _merge_fragments(words)


def _merge_fragments(words):
    """Glue lone Thai marks/1-char fragments onto the previous word so tone marks never start a line."""
    out = []
    for w in words:
        if out and (len(w["text"]) == 1 and THAI.match(w["text"])) and not w.get("space"):
            out[-1]["text"] += w["text"]; out[-1]["end"] = w["end"]
        else:
            out.append(dict(w))
    return out


def phrases(words, max_chars=22, gap=0.22, keywords=(), italic=()):
    """Thai 'set' captions: one spoken phrase per caption (split on pauses), <= max_chars visible chars,
    never break between a number and its unit. Each set holds until the next starts."""
    return chunk(words, max_chars=max_chars, max_words=99, gap=gap, keywords=keywords, italic=italic)


def chunk(words, max_chars=14, max_words=3, gap=0.28, keywords=(), italic=()):
    """Group words into on-screen chunks. Break on pauses, char budget, or word budget."""
    chunks, cur = [], []
    def flush():
        if cur:
            chunks.append({"start": cur[0]["start"], "end": cur[-1]["end"], "words": cur.copy()}); cur.clear()
    for w in words:
        w = dict(w)
        key = w["text"].strip().lower()
        w["hl"] = "italic" if any(k.lower() in key for k in italic) else (True if any(k.lower() in key for k in keywords) else False)
        chars = sum(len(x["text"]) for x in cur) + len(w["text"])
        if cur and (w["start"] - cur[-1]["end"] > gap or chars > max_chars or len(cur) >= max_words):
            flush()
        if not cur: w["space"] = False
        cur.append(w)
    flush()
    # hold each chunk until the next starts (max +0.4s) so captions don't flicker
    for a, b in zip(chunks, chunks[1:]):
        a["end"] = round(min(b["start"], a["end"] + 0.4), 3)
    if chunks: chunks[-1]["end"] = round(chunks[-1]["end"] + 0.4, 3)
    return chunks


def envelope(wav_path, fps=30, floor_db=-45.0):
    with wave.open(str(wav_path)) as w:
        sr, ch = w.getframerate(), w.getnchannels()
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    if ch > 1: x = x.reshape(-1, ch).mean(1)
    hop = sr // fps
    n = len(x) // hop
    rms = np.sqrt(np.mean(x[: n * hop].reshape(n, hop) ** 2, axis=1) + 1e-12)
    db = 20 * np.log10(rms)
    peak = np.percentile(db, 95)
    v = np.clip((db - floor_db) / (peak - floor_db), 0, 1)
    v = np.convolve(v, [0.25, 0.5, 0.25], mode="same")  # light smoothing
    return [round(float(a), 3) for a in v]


def sets_from_script(caption_script, items, keywords=(), max_chars=24):
    """Caption sets = the phrases of the written script (split on ' / ' or newlines), timed by aligning
    their characters to the Scribe character timeline. Display text comes from the script (exact spelling,
    numerals, brand names), timing from the audio. Long phrases split at a PyThaiNLP word boundary."""
    import difflib
    tl = char_timeline(items)
    raw = [p.strip() for p in re.split(r"\s*/\s*|\n+", caption_script) if p.strip()]
    sets = []
    for p in raw:  # split over-long phrases at the word boundary closest to the middle
        vis = p.replace(" ", "")
        if len(vis) <= max_chars:
            sets.append(p); continue
        toks = word_tokenize(p, engine="newmm", keep_whitespace=True)
        acc, best, bi = 0, 1e9, 1
        for i, tk in enumerate(toks[:-1]):
            acc += len(tk.replace(" ", ""))
            if abs(acc - len(vis) / 2) < best: best, bi = abs(acc - len(vis) / 2), i + 1
        sets += ["".join(toks[:bi]).strip(), "".join(toks[bi:]).strip()]
    norm = lambda s: re.sub(r"[\s.,!?…“”\"']", "", s).lower()
    S, owner = [], []
    for k, p in enumerate(sets):
        for ch in norm(p): S.append(ch); owner.append(k)
    B = [c[0].lower() for c in tl]
    sm = difflib.SequenceMatcher(None, S, B, autojunk=False)
    t_of = [None] * len(S)
    for blk in sm.get_matching_blocks():
        for i in range(blk.size): t_of[blk.a + i] = (tl[blk.b + i][1], tl[blk.b + i][2])
    out = []
    for k, p in enumerate(sets):
        idx = [i for i, o in enumerate(owner) if o == k and t_of[i]]
        if not idx: continue
        st, en = t_of[idx[0]][0], t_of[idx[-1]][1]
        ws = [{"text": w, "start": st, "end": en, "space": j > 0,
               "hl": any(kw.lower() in w.lower() for kw in keywords)} for j, w in enumerate(p.split(" "))]
        out.append({"start": round(st, 3), "end": round(en, 3), "words": ws})
    for a, b in zip(out, out[1:]):
        a["end"] = round(max(a["end"], b["start"] - 0.02) if b["start"] - a["end"] < 1.8 else a["end"] + 0.4, 3)
    if out: out[-1]["end"] += 0.5
    return out
