"""Tighten a narration: shorten pauses longer than --max to --keep, then apply --tempo (pitch kept).
Maps Scribe word timestamps through both steps so captions/shots stay in sync.

usage: python engine/tighten.py voice_raw.mp3 words_raw.json voice.wav words.json [--max 0.3] [--keep 0.22] [--tempo 1.05]
"""
import argparse, json, subprocess
import numpy as np

SR = 48000
ap = argparse.ArgumentParser()
ap.add_argument("src"); ap.add_argument("words_in"); ap.add_argument("dst"); ap.add_argument("words_out")
ap.add_argument("--max", type=float, default=0.3); ap.add_argument("--keep", type=float, default=0.22)
ap.add_argument("--tempo", type=float, default=1.05)
a = ap.parse_args()

x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", a.src, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                                 capture_output=True, check=True).stdout, np.float32).copy()
d = json.load(open(a.words_in, encoding="utf-8")); words = d["words"] if isinstance(d, dict) else d
# pauses from the audio itself (Scribe stretches Thai characters across pauses, so its gaps are unreliable)
sd = subprocess.run(["ffmpeg", "-hide_banner", "-i", a.src, "-af", f"silencedetect=n=-38dB:d={a.max}", "-f", "null", "-"],
                    capture_output=True, text=True).stderr
import re
st = [float(v) for v in re.findall(r"silence_start: ([\d.]+)", sd)]
en = [float(v) for v in re.findall(r"silence_end: ([\d.]+)", sd)]
cuts = []  # (orig_start, orig_end) of removed audio; keep a.keep of each pause, centred
for s0, s1 in zip(st, en):
    if s0 < 0.05 or s1 > len(x) / SR - 0.05:
        continue
    pad = a.keep / 2
    if s1 - s0 > a.keep: cuts.append((s0 + pad, s1 - pad))
keep_mask = np.ones(len(x), bool)
for c0, c1 in cuts:
    i0, i1 = int(c0 * SR), int(c1 * SR)
    keep_mask[i0:i1] = False
    f = int(0.008 * SR)  # 8 ms fades at the join
    if i0 - f > 0: x[i0 - f:i0] *= np.linspace(1, 0, f)
    if i1 + f < len(x): x[i1:i1 + f] *= np.linspace(0, 1, f)
y = x[keep_mask]


def mapt(t):
    removed = sum(max(0.0, min(t, c1) - c0) for c0, c1 in cuts)
    return (t - removed) / a.tempo


subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-",
                "-af", f"atempo={a.tempo}", a.dst], input=y.tobytes(), check=True)
for w in words:
    w["start"], w["end"] = round(mapt(w["start"]), 3), round(mapt(w["end"]), 3)
json.dump(words, open(a.words_out, "w", encoding="utf-8"), ensure_ascii=False)
print(f"removed {sum(c1 - c0 for c0, c1 in cuts):.2f}s of pauses in {len(cuts)} cuts; {len(x)/SR:.2f}s -> {len(y)/SR/a.tempo:.2f}s")
