"""Parallel renderer: split the timeline into N frame-aligned chunks, render each with engine/render.py in its own
headless Chromium, then join the chunks losslessly (concat demuxer, stream copy). Same page, same lossless PNG
frames, same x264 settings as render.py, so the picture is identical; only wall-clock time changes.
(User 2026-11-12: "if it is faster and quality does not drop, do it".)

usage: python engine/render_par.py --page P --data D --out out.mp4 --duration 67.4 [--jobs 4] [--fps 30]
Audio is not handled here (the mixer adds it); --base pages are not supported (use render.py).
"""
import argparse, pathlib, subprocess, sys, time

ap = argparse.ArgumentParser()
ap.add_argument("--page", required=True); ap.add_argument("--data", required=True); ap.add_argument("--out", required=True)
ap.add_argument("--duration", type=float, required=True); ap.add_argument("--jobs", type=int, default=4); ap.add_argument("--fps", type=int, default=30)
a = ap.parse_args()

out = pathlib.Path(a.out); tmp = out.with_name(out.stem + "_chunks"); tmp.mkdir(exist_ok=True)
n = int(round(a.duration * a.fps)); per = -(-n // a.jobs)
here = pathlib.Path(__file__).parent
procs, parts, st = [], [], time.time()
for k in range(a.jobs):
    f0, f1 = k * per, min(n, (k + 1) * per)
    if f0 >= f1: break
    part = tmp / f"part{k:02d}.mp4"; parts.append(part)
    cmd = [sys.executable, str(here / "render.py"), "--page", a.page, "--data", a.data, "--out", str(part),
           "--duration", str(a.duration), "--fps", str(a.fps), "--start", f"{f0 / a.fps:.6f}", "--end", f"{f1 / a.fps:.6f}"]
    procs.append(subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace"))
fail = False
for k, p in enumerate(procs):
    log = p.communicate()[0]
    if p.returncode: fail = True; print(f"chunk {k} failed:\n{log[-2000:]}", file=sys.stderr)
if fail: sys.exit("render_par: a chunk failed")
lst = tmp / "list.txt"; lst.write_text("".join(f"file '{p.name}'\n" for p in parts), encoding="utf-8")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", "-movflags", "+faststart", str(out)], check=True)
got = subprocess.run(["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v:0", "-show_entries", "stream=nb_read_packets", "-of", "csv=p=0", str(out)],
                     capture_output=True, text=True).stdout.strip()
if got != str(n): sys.exit(f"render_par: frame count {got} != {n}")
for p in parts: p.unlink()
lst.unlink(); tmp.rmdir()
print(f"wrote {out}  ({n} frames, {len(parts)} chunks, {time.time() - st:.0f}s)")
