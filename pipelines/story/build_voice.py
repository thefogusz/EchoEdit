"""Join per-line Paxa takes into one voice track + one word timeline.
Each take is trimmed to its spoken span (Paxa json spans) with small handles, then joined with gaps.
usage: python build_voice.py <voice_dir> <out_wav> <out_words_json> [--gap 0.32] [--gaps 3:0.6,10:0.7]
--gaps sets the pause BEFORE line N (1-based) where a new beat starts."""
import json, subprocess, sys, argparse
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("vdir"); ap.add_argument("wav"); ap.add_argument("words")
ap.add_argument("--gap", type=float, default=0.32); ap.add_argument("--gaps", default="")
a = ap.parse_args()
extra = {int(k): float(v) for k, v in (p.split(":") for p in a.gaps.split(",") if p)}
vd = Path(a.vdir); takes = sorted(vd.glob("l[0-9][0-9].mp3"))
SR = 48000; parts, words, t = [], [], 0.0
tmp = vd / "_trim"; tmp.mkdir(exist_ok=True)
for i, mp3 in enumerate(takes, 1):
    sp = json.load(open(mp3.with_suffix(".json"), encoding="utf-8"))["spans"]
    s0, s1 = max(0.0, sp[0]["start"] - 0.08), sp[-1]["end"] + 0.15
    if i > 1: t += extra.get(i, a.gap)
    out = tmp / f"{mp3.stem}.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{s0}", "-to", f"{s1}", "-i", str(mp3),
                    "-af", "afade=t=in:d=0.01,areverse,afade=t=in:d=0.03,areverse", "-ar", str(SR), "-ac", "1", str(out)], check=True)
    for w in sp:
        words.append({"text": w["text"], "start": round(t + w["start"] - s0, 3), "end": round(t + w["end"] - s0, 3), "line": i})
    parts.append((t, out)); t += s1 - s0
# place each part at its start time
inputs, flt = [], []
for k, (st, f) in enumerate(parts):
    inputs += ["-i", str(f)]; flt.append(f"[{k}]adelay={int(st*1000)}|{int(st*1000)}[d{k}]")
flt.append("".join(f"[d{k}]" for k in range(len(parts))) + f"amix=inputs={len(parts)}:normalize=0[o]")
subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(flt), "-map", "[o]", "-ar", str(SR), a.wav], check=True)
json.dump(words, open(a.words, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print(f"wrote {a.wav} ({t:.2f}s, {len(words)} words)")
