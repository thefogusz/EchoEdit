"""Derive SFX cues from a shot plan so every sound sits on a visual event (no sound without a picture).

usage: python engine/cues.py news jobs/<job>/plan_v3.json out_cues.json
       python engine/cues.py story jobs/<job>/scene.json out_cues.json
       python engine/cues.py talkinghead jobs/<job>/plan_v2.json out_cues.json
"""
import json, sys

kind, plan_path, out = sys.argv[1], sys.argv[2], sys.argv[3]
p = json.load(open(plan_path, encoding="utf-8"))
cues = []
if kind == "news":
    # v7 (user review 2026-11-12): "SFX not varied, no whoosh, add light basic whooshes and interaction sounds".
    # Every cut gets a light whoosh (4 real Artlist variants round-robin), every visual event its own role sound,
    # all kept under the voice. Role -> file in library/audio/sfx (see LICENSE.txt there).
    W = -15  # whoosh level: audible but light
    for s in p["shots"]:
        cs = s.get("cut_sfx")
        if s["t0"] > 0:
            if cs == "riser": cues.append({"t": s["t0"], "sfx": "riser", "db": -18, "align": "end"})
            elif cs == "chime": cues.append({"t": s["t0"] + 0.35, "sfx": "chime", "db": -20})
            cues.append({"t": s["t0"], "sfx": "whoosh", "db": W, "align": "peak"})
        for h in s.get("highlights", []):
            if h["at"] >= 0: cues.append({"t": s["t0"] + h["at"], "sfx": "pen", "db": -20})
        cards = 0
        for pc in s.get("pieces", []):
            at = s["t0"] + pc.get("at", 0); k = pc.get("k")
            if at < s["t0"] + 0.12 and k in ("doc", "photo", "video"): at = s["t0"] + 0.12  # never on top of the cut whoosh
            if k == "num":
                cues.append({"t": at, "sfx": "counter", "db": -25, "dur": 0.7})
                cues.append({"t": at + 0.7, "sfx": "pop", "db": -16})
            elif k == "logo": cues.append({"t": at + 0.1, "sfx": "logo", "db": -19})
            elif k == "doc": cues.append({"t": at + 0.05, "sfx": "paper", "db": -20})
            elif k == "photo": cues.append({"t": at + 0.05, "sfx": "swish_paper", "db": -23, "dur": 0.55})
            elif k == "video": cues.append({"t": at + 0.05, "sfx": "shutter", "db": -21})
            elif k == "card":
                cards += 1
                cues.append({"t": at + 0.08, "sfx": "click" if cards % 2 else "pop", "db": -21 if cards % 2 else -22})
            for h in pc.get("highlights", []):
                cues.append({"t": s["t0"] + h["at"], "sfx": "pen", "db": -20})
    m = p.get("mascot", {})
    for mv in m.get("moves", []): cues.append({"t": mv["t"], "sfx": "whoosh", "db": -19, "align": "peak"})
    for e in m.get("emotes", []): cues.append({"t": e["t"], "sfx": "pop", "db": -23})
elif kind == "story":
    # type 3, from the ref audit (docs/REF_TYPE3_AUDIT.md): whoosh only on whip-pan place changes (not every cut),
    # reverse swell peaking INTO text cards and punch-throughs, stab on the chapter title, rewind sound on the
    # flashback, a clock under the voice-only tension stretch, pops on tags/chips, counters on numbers.
    shots = p["shots"]
    for i, s in enumerate(shots):
        nxt = shots[i + 1] if i + 1 < len(shots) else None
        if s.get("in") in ("whip", "push"): cues.append({"t": s["t0"], "sfx": "whoosh", "db": -16, "align": "peak"})
        if s.get("in") == "zoom": cues.append({"t": s["t0"], "sfx": "swell", "db": -18, "align": "end"})
        if nxt and (nxt.get("card") and not nxt["card"].get("title") or s.get("out") == "punch"):
            cues.append({"t": nxt["t0"], "sfx": "swell", "db": -17, "align": "end"})
        if s.get("card", {}).get("title"): cues.append({"t": s["t0"], "sfx": "stab", "db": -14})
        if s.get("rewind"): cues.append({"t": s["t0"], "sfx": "rewind", "db": -15})
        if s.get("cta"): cues.append({"t": s["t0"] + 0.45, "sfx": "chime", "db": -19})
        for tg in s.get("tags", []): cues.append({"t": tg["at"] + 0.05, "sfx": "pop", "db": -24})
        for lk in s.get("links", []):
            cues.append({"t": lk["at"], "sfx": "pen", "db": -21})
            if lk.get("breakAt"): cues.append({"t": lk["breakAt"], "sfx": "swish_paper", "db": -17, "dur": 0.5})
        for c in s.get("counters", []):
            if c["to"] != c["from"]: cues.append({"t": c["at"], "sfx": "counter", "db": -24, "dur": max(0.3, c.get("dur", 0.8))})
            cues.append({"t": c["at"] + c.get("dur", 0.8), "sfx": "pop", "db": -16})
        for pr in s.get("props", []):
            k = pr["kind"]
            if k == "napkin": cues.append({"t": pr.get("at", s["t0"]) + 0.05, "sfx": "pen", "db": -20})
            elif k == "check" and pr["x0"] != pr["x"]: cues.append({"t": pr["at"], "sfx": "paper", "db": -19})
            elif k == "box" and s["t0"] <= pr["drop"] < s["t1"]: cues.append({"t": pr["drop"], "sfx": "logo", "db": -20})
            elif k == "chip": cues.append({"t": pr.get("at", s["t0"]) + 0.1, "sfx": "pop_2", "db": -19})
        # jump cut on a locked set: a small click marks it
        prv = shots[i - 1] if i else None
        # (v3: no UI click on jump cuts; the user found UI clicks out of place in a story)
    cues += p.get("extra_cues", [])  # scene-specific foley written by the scene script
    for m0, m1 in p.get("music_mute", []):
        if m1 - m0 > 4:  # long drop-out = tension stretch: clock under the voice
            cues.append({"t": m0 + 0.1, "sfx": "tick", "db": -24, "dur": m1 - m0 - 0.3})
else:
    segs = p["segments"]
    for a, b in zip(segs, segs[1:]):
        if a["layout"] != b["layout"] or b.get("insert"):
            cues.append({"t": b["t0"], "sfx": "whoosh", "db": -18, "align": "peak"})
        for k, lg in enumerate(b.get("insert", {}).get("logos", [])):
            cues.append({"t": b["t0"] + k * 0.12, "sfx": "pop", "db": -18})
        if b.get("insert", {}).get("kind") == "bars":
            cues.append({"t": b["t0"] + 0.12, "sfx": "pop", "db": -17})
# keep pops at least 90 ms apart (a run keeps its rhythm, never a double hit)
cues.sort(key=lambda c: c["t"])
kept = []
for c in cues:
    if kept and c["sfx"] == kept[-1]["sfx"] and c["t"] - kept[-1]["t"] < 0.09: continue
    if kept and "whoosh" not in (c["sfx"], kept[-1]["sfx"]) and c["t"] - kept[-1]["t"] < 0.06: continue
    kept.append(c)
json.dump(kept, open(out, "w", encoding="utf-8"), indent=1)
print(f"{len(kept)} cues -> {out}")
