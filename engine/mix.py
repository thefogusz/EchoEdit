"""Sound pass: voice + music bed (ducked) + SFX cues from the plan -> mastered audio muxed onto a rendered video.

usage:
  python engine/mix.py --video in.mp4 --voice voice.wav --music bed.mp3 --sfx-dir sfx/ --cues cues.json --out out.mp4
  cues.json: [{"t": 1.28, "sfx": "whoosh", "db": -16, "align": "peak"}, ...]
    align "peak": the loudest point of the SFX lands on t (whooshes); "onset": the sound starts at t (stamps, pops).
Rules (docs/REF_SPEC.md): music -20..-25 dB under voice with sidechain ducking, no hit on top of a word, master -14 LUFS / TP <= -1.5.
"""
import argparse, json, pathlib, subprocess, tempfile, wave
import numpy as np

SR = 48000


def load(path, ch=1, af=None):
    """Decode any audio to float32 @48k via ffmpeg (ch=1 mono, ch=2 -> shape (n, 2))."""
    cmd = ["ffmpeg", "-v", "error", "-i", str(path)] + (["-af", af] if af else []) + ["-ac", str(ch), "-ar", str(SR), "-f", "f32le", "-"]
    x = np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, dtype=np.float32).copy()
    return x.reshape(-1, 2) if ch == 2 else x


def db(x): return 10 ** (x / 20)


def trim(x, thr=0.02):
    """Drop leading/trailing near-silence so onsets are exact."""
    idx = np.nonzero(np.abs(x) > thr * np.abs(x).max())[0]
    return x[idx[0]: idx[-1] + int(0.03 * SR)] if len(idx) else x


def main():
    ap = argparse.ArgumentParser()
    for k in ("video", "voice", "music", "sfx-dir", "cues", "out"): ap.add_argument("--" + k, required=k != "music")
    ap.add_argument("--music-db", type=float, default=-15, help="music RMS relative to the voice RMS in gaps")
    ap.add_argument("--duck-db", type=float, default=-6, help="extra music reduction while the voice talks (gentle: no pumping)")
    ap.add_argument("--stems", help="write voice/music/sfx stems here for measuring")
    ap.add_argument("--music-mute", default="", help="t0-t1,t0-t1: music fully out (ref: voice-only tension), 0.25 s fades")
    a = ap.parse_args()

    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", a.video],
                               capture_output=True, text=True).stdout)
    n = int(dur * SR)
    voice = np.zeros(n, np.float32); v = load(a.voice, af="equalizer=f=2500:t=o:w=1.2:g=-3")[:n]; voice[:len(v)] = v
    # voice to a consistent level (RMS of speech ~ -20 dBFS)
    act = voice[np.abs(voice) > 0.01]
    voice *= db(-20) / (np.sqrt(np.mean(act ** 2)) + 1e-9)

    music = np.zeros((n, 2), np.float32)
    if a.music:
        m = load(a.music, ch=2)  # keep the bed stereo (earshot: mix was nearly mono)
        reps = int(np.ceil(n / len(m))); m = np.tile(m, (reps, 1))[:n]
        m *= db(-20) / (np.sqrt(np.mean(m ** 2)) + 1e-9)
        # gentle duck: 0.3 s attack / 0.8 s release on a speech mask, so the bed breathes instead of pumping
        env = np.abs(voice); win = int(0.05 * SR); env = np.convolve(env, np.ones(win) / win, mode="same")
        talk = (env > db(-40)).astype(np.float32)
        hop = 480; tk = talk[::hop]; sm = np.zeros_like(tk); a_up, a_dn = hop / (0.3 * SR), hop / (0.8 * SR)
        for i in range(1, len(tk)): sm[i] = sm[i - 1] + (tk[i] - sm[i - 1]) * (a_up if tk[i] > sm[i - 1] else a_dn)
        talk = np.interp(np.arange(n), np.arange(len(sm)) * hop, sm).astype(np.float32)
        gain = db(a.music_db) * (1 - talk + talk * db(a.duck_db))
        fade = np.ones(n, np.float32); f = int(0.6 * SR); fade[-f:] = np.linspace(1, 0, f)
        for rng in filter(None, a.music_mute.split(",")):  # music drop-outs, 0.25 s fade out / 0.15 s fade back in
            m0, m1 = (float(x) for x in rng.split("-")); i0, i1 = int(m0 * SR), min(n, int(m1 * SR))
            fo, fi = int(0.25 * SR), int(0.15 * SR)
            fade[max(0, i0 - fo):i0] *= np.linspace(1, 0, i0 - max(0, i0 - fo)); fade[i0:i1] = 0
            if i1 < n: fade[i1:min(n, i1 + fi)] *= np.linspace(0, 1, min(n, i1 + fi) - i1)
        music = m * (gain * fade)[:, None]

    fx = np.zeros((n, 2), np.float32)
    # SFX: round-robin over variants (<name>.mp3, <name>_2.mp3 ...) with a small pitch jitter, so no hit repeats exactly
    import glob, random
    rnd = random.Random(7); bank = {}; used = {}
    def variants(name):
        if name not in bank:
            files = sorted(f for d in a.sfx_dir.split(",") for ext in ("mp3", "wav") for f in glob.glob(str(pathlib.Path(d) / f"{name}.{ext}")) + glob.glob(str(pathlib.Path(d) / f"{name}_[0-9]*.{ext}")))  # --sfx-dir may list several folders (sfx,foley)
            vs = []
            for f in files:
                s = trim(load(f)); s *= db(-6) / (np.abs(s).max() + 1e-9)
                s[-int(0.01 * SR):] *= np.linspace(1, 0, int(0.01 * SR)); vs.append(s)
            bank[name] = vs
        return bank[name]
    for c in json.loads(pathlib.Path(a.cues).read_text(encoding="utf-8")):
        vs = variants(c["sfx"]); k = used.get(c["sfx"], 0); used[c["sfx"]] = k + 1
        s = vs[k % len(vs)]
        if c.get("dur"):  # cut a long effect (e.g. a counter run) to the length of its picture event
            m = int(c["dur"] * SR); s = s[:m].copy(); f = min(len(s), int(0.04 * SR)); s[-f:] *= np.linspace(1, 0, f)
        rate = 1 + rnd.uniform(-0.04, 0.04)  # +-4 % speed/pitch
        s = np.interp(np.arange(0, len(s), rate), np.arange(len(s)), s).astype(np.float32)
        peak = int(np.argmax(np.abs(s)))
        anchor = {"peak": peak, "end": len(s)}.get(c.get("align"), 0)
        start = int(c["t"] * SR) - anchor
        s = s * db(c.get("db", -14))
        a0, b0 = max(0, start), min(n, start + len(s))
        pan = c.get("pan", rnd.uniform(-0.35, 0.35))  # constant-power pan, slight spread so hits don't stack in the centre
        gl, gr = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
        if b0 > a0:
            seg = s[a0 - start: b0 - start]
            fx[a0:b0, 0] += seg * gl * 1.414; fx[a0:b0, 1] += seg * gr * 1.414

    mix = voice[:, None] + music + fx
    if a.stems:
        d = pathlib.Path(a.stems); d.mkdir(parents=True, exist_ok=True)
        for name, sig in (("voice", np.repeat(voice[:, None], 2, 1)), ("music", music), ("sfx", fx), ("mix", mix)):
            with wave.open(str(d / f"{name}.wav"), "wb") as w:
                w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
                w.writeframes((np.clip(sig, -1, 1) * 32767).astype(np.int16).tobytes())
    tmp = pathlib.Path(tempfile.mkdtemp()) / "mix.wav"
    with wave.open(str(tmp), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(mix, -1, 1) * 32767).astype(np.int16).tobytes())
    # two-pass loudnorm to -14 LUFS, TP -1.5, then mux (video stream copied, not re-encoded)
    meas = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(tmp), "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                          capture_output=True, text=True).stderr
    j = json.loads(meas[meas.rindex("{"): meas.rindex("}") + 1])
    ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:"
          f"measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.video, "-i", str(tmp), "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-af", ln + ",aresample=48000", "-ac", "2", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", a.out], check=True)
    # verify on the encoded file (rule: measure the MP4, not the WAV) and correct any residual offset
    def measure(path):
        e = subprocess.run(["ffmpeg", "-nostats", "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
        import re
        i = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", e)[-1]); p = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", e)[-1])
        return i, p
    i, p = measure(a.out)
    gain = min(-14.0 - i, -1.5 - p)  # reach -14 LUFS without pushing true peak above -1.5
    if abs(gain) > 0.3:
        fixed = str(pathlib.Path(a.out).with_suffix(".tmp.mp4"))
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.out, "-map", "0", "-c:v", "copy", "-af", f"volume={gain:.2f}dB",
                        "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", fixed], check=True)
        pathlib.Path(fixed).replace(a.out)
        i, p = measure(a.out)
    print(f"wrote {a.out}  ({i:.1f} LUFS, peak {p:.1f} dBFS)")


if __name__ == "__main__":
    main()
