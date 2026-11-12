"""Frame-accurate renderer: HTML page with window.setup(data) + window.renderAt(t) -> video.

Each frame: renderAt(i/fps) in headless Chromium, screenshot, pipe PNG to ffmpeg.
Optional --base video is scaled to 1080x1920 and the page frames are overlaid on it
(page background must be transparent). Optional --audio is muxed and loudness-normalised.

usage:
  python engine/render.py --page engine/pages/x.html --data job/scene.json --out out.mp4 --duration 12
        [--base base.mp4] [--audio voice.wav] [--fps 30] [--start 0] [--end N] [--preview 5]
"""
import argparse, json, pathlib, subprocess, sys, time
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parents[1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--page", required=True)
    ap.add_argument("--data", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--duration", type=float, required=True)
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--base")
    ap.add_argument("--audio")
    ap.add_argument("--start", type=float, default=0.0, help="render only from this time (seconds)")
    ap.add_argument("--end", type=float)
    ap.add_argument("--stills", help="comma list of seconds: write PNG stills instead of video")
    a = ap.parse_args()

    W, H, fps = 1080, 1920, a.fps
    data = json.loads(pathlib.Path(a.data).read_text(encoding="utf-8"))
    data.setdefault("brandBase", (ROOT / "brand").as_uri())
    page_url = pathlib.Path(a.page).resolve().as_uri()
    t0, t1 = a.start, a.end if a.end is not None else a.duration
    n = int(round((t1 - t0) * fps))
    out = pathlib.Path(a.out); out.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        br = p.chromium.launch(args=["--allow-file-access-from-files", "--force-color-profile=srgb", "--font-render-hinting=none"])
        pg = br.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        pg.on("console", lambda m: print("[page]", m.text, file=sys.stderr))
        pg.on("pageerror", lambda e: (print("[page error]", e, file=sys.stderr)))
        pg.goto(page_url)
        pg.evaluate("async (d) => { await window.setup(d); }", data)

        if a.stills:
            for s in [float(x) for x in a.stills.split(",")]:
                pg.evaluate("async (t) => { await window.renderAt(t); }", s)
                pg.screenshot(path=str(out.with_name(f"{out.stem}_{s:05.2f}.png")), omit_background=bool(a.base))
            br.close(); return

        cmd = ["ffmpeg", "-v", "error", "-y"]
        if a.base:
            cmd += ["-ss", str(t0), "-t", str(t1 - t0), "-i", a.base]
        cmd += ["-f", "image2pipe", "-framerate", str(fps), "-c:v", "png", "-i", "-"]
        if a.audio:
            cmd += ["-ss", str(t0), "-t", str(t1 - t0), "-i", a.audio]
        if a.base and data.get("baseZoom"):
            # punch-in zoom per segment: [[t0,t1,z],...]  (face sits ~38% from top, keep it there)
            z = "1"
            for s0, s1, zz in reversed(data["baseZoom"]):
                z = f"if(between(t,{s0 - t0},{s1 - t0}),{zz},{z})"
            fc = (f"[0:v]fps={fps},scale=w='{W}*({z})':h='{H}*({z})':eval=frame:flags=lanczos,"
                  f"crop={W}:{H}:(iw-{W})/2:(ih-{H})*0.38,setsar=1[bg];"
                  f"[bg][1:v]overlay=0:0:format=auto,format=yuv420p[v]")
            cmd += ["-filter_complex", fc, "-map", "[v]"]
            amap = "2:a" if a.audio else "0:a?"
        elif a.base:
            fc = (f"[0:v]scale={W}:{H}:flags=lanczos,fps={fps},setsar=1[bg];"
                  f"[bg][1:v]overlay=0:0:format=auto,format=yuv420p[v]")
            cmd += ["-filter_complex", fc, "-map", "[v]"]
            amap = "2:a" if a.audio else "0:a?"
        else:
            cmd += ["-map", "0:v", "-pix_fmt", "yuv420p"]
            amap = "1:a" if a.audio else None
        if amap:
            cmd += ["-map", amap, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k", "-ar", "48000"]
        cmd += ["-c:v", "libx264", "-preset", "medium", "-crf", "18", "-r", str(fps), "-shortest", "-movflags", "+faststart", str(out)]

        ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        st = time.time()
        for i in range(n):
            t = t0 + i / fps
            pg.evaluate("async (t) => { await window.renderAt(t); }", t)
            ff.stdin.write(pg.screenshot(type="png", omit_background=bool(a.base)))
            if i % 90 == 0:
                print(f"frame {i}/{n}  {time.time()-st:.0f}s", file=sys.stderr)
        ff.stdin.close(); rc = ff.wait(); br.close()
        if rc:
            sys.exit(f"ffmpeg failed rc={rc}")
    print(f"wrote {out}  ({n} frames, {time.time()-st:.0f}s)")


if __name__ == "__main__":
    main()
