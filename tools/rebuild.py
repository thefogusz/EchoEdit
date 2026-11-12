"""Rebuild a baseline final from the repo, the same way it was made (one command per type).

usage: python tools/rebuild.py type1|type2|type3 [--preview SECONDS] [--jobs 4]
  --preview 3   render + mix only the first 3 s (fast check that the whole chain works on this machine)

Steps per type: prepare inputs (footage / clips / music bed) -> scene -> cues -> render_par -> mix.
Output: jobs/<job>/out/<name>.mp4 (out/ is git-ignored). Compare it with deliverables/.
Needs: tools/setup.py done; Artlist audio in library/audio, downloaded with your own account (tools/artlist_check.py), for the exact sound.
Missing Artlist files do not stop a preview: the mix runs without music / with the SFX it has, and says so.
"""
import argparse, json, pathlib, shutil, subprocess, sys, urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
PY = sys.executable
DELIV = {"type1": "type1_talkinghead_forsample_v3.mp4", "type2": "type2_news_fable52_v8.mp4", "type3": "type3_story_nvidia_p1_v3.mp4"}

BASE = {
    "type1": dict(job="jobs/type1_talkinghead/2026-11-12_th_sample", page="engine/pages/talkinghead3.html",
                  scene_cmd=["{job}/plan_v3.py"], scene="scene_v3.json", dur=37.6,
                  cues=None, cue_file="cues_v3.json",  # cues_v3.json is committed (made from the scene by the plan step)
                  music=("library/audio/music/artlist_liam-mansfield_a-little-curious.wav", 38, 38.5, 0.4),
                  sfx="library/audio/sfx", mix=["--music-db", "-22", "--duck-db", "-6"], name="th_sample_v3"),
    "type2": dict(job="jobs/type2_news/2026-11-12_news_fable52", page="engine/pages/news3.html",
                  scene_cmd=["pipelines/news/build_shots.py", "{job}", "plan_v8.json"], scene="scene_v3.json", dur=68.66,
                  cues=["news", "{job}/plan_v8.json"], cue_file="cues_v8.json",
                  music=("library/audio/music/artlist_ariel-shalom_groove-express.wav", 42, 68.5, 0.25),
                  sfx="library/audio/sfx", mix=["--music-db", "-15", "--duck-db", "-6"], name="news_fable52_v8"),
    "type3": dict(job="jobs/type3_story/2026-11-12_story_nvidia", page="engine/pages/story2d.html",
                  scene_cmd=["{job}/part1_scene_v3.py"], scene="scene.json", dur=62.5,
                  cues=["story", "{job}/scene.json"], cue_file="cues.json",
                  music=("library/audio/music/artlist_dor-ben-lulu_moments-apart.wav", 29, 63, 0.4),
                  sfx="library/audio/sfx,library/audio/foley", mix=["--music-db", "-24", "--duck-db", "-6"],
                  mute_file="music_mute.txt", name="nvidia_p1_v3"),
}


def run(cmd, **kw):
    print("  $", " ".join(str(c) for c in cmd)[:220], flush=True)
    subprocess.run([str(c) for c in cmd], check=True, cwd=ROOT, **kw)


def ff(*args):
    run(["ffmpeg", "-v", "error", "-y", *args])


def prepare_type1(job):
    webm = job / "assets/footage.webm"
    if not webm.exists():
        print("- footage.webm from input/footage.mp4 (VP9: pages can only play WebM)")
        ff("-i", job / "input/footage.mp4", "-an", "-c:v", "libvpx-vp9", "-b:v", "2M", "-r", "30", webm)


def prepare_type2(job):
    """X clips used as inserts: download the public media, cut the same 4 s, encode VP9 (recipe in 3d_clips.json)."""
    media = job / "assets/media"
    clips = json.loads((media / "3d_clips.json").read_text(encoding="utf-8"))
    for key, c in clips.items():
        out = media / (c["make"]["out"] + ".webm")
        if out.exists():
            continue
        src = media / f"{key}.mp4"
        if not src.exists():
            print(f"- download {c['src']} (credited on screen, see CREDITS.txt)")
            try:
                req = urllib.request.Request(c["media"], headers={"User-Agent": "Mozilla/5.0 (EchoEdit)"})
                src.write_bytes(urllib.request.urlopen(req, timeout=180).read())
            except Exception as e:  # the mirror may go away; the shot then shows an empty frame, say so
                print(f"  ! could not download ({e}); get it from {c['src']} and save as {src.relative_to(ROOT)}")
                continue
        ff("-ss", str(c["make"]["ss"]), "-t", "4", "-i", src, "-an", "-c:v", "libvpx-vp9", "-b:v", "3M",
           "-deadline", "good", "-cpu-used", "5", "-vf", "scale=1440:-2", out)


def music_bed(job, spec, dur):
    track, ss, t, fade = spec
    track = ROOT / track
    bed = job / "out/music_bed.wav"
    if not track.exists():
        print(f"  ! {track.relative_to(ROOT)} missing (Artlist, not in git): mixing WITHOUT music."
              " See: python tools/artlist_check.py")
        return None
    ff("-ss", str(ss), "-t", str(min(t, dur + 0.5)), "-i", track, "-af", f"afade=t=in:d={fade}", bed)
    return bed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("type", choices=sorted(BASE))
    ap.add_argument("--preview", type=float, help="only the first N seconds")
    ap.add_argument("--jobs", type=int, default=4)
    a = ap.parse_args()
    b = BASE[a.type]
    job = ROOT / b["job"]
    (job / "out").mkdir(exist_ok=True)
    for tool in ("ffmpeg", "ffprobe"):
        if not shutil.which(tool):
            sys.exit(f"{tool} not found: run python tools/setup.py first")
    fill = lambda xs: [x.replace("{job}", b["job"]) for x in xs]

    print(f"[1/5] inputs ({a.type})")
    {"type1": prepare_type1, "type2": prepare_type2}.get(a.type, lambda j: None)(job)
    print("[2/5] scene")
    run([PY, *fill(b["scene_cmd"])], env={**__import__("os").environ, "PYTHONUTF8": "1"})
    print("[3/5] cues")
    if b["cues"]:
        run([PY, "engine/cues.py", *fill(b["cues"]), f"{b['job']}/{b['cue_file']}"])
    dur = a.preview or b["dur"]
    tag = f"{b['name']}_preview{int(dur)}s" if a.preview else b["name"]
    pic = job / f"out/{tag}_picture.mp4"
    print(f"[4/5] render {dur} s")
    if a.preview:
        run([PY, "engine/render.py", "--page", b["page"], "--data", f"{b['job']}/{b['scene']}", "--out", pic,
             "--duration", b["dur"], "--start", 0, "--end", dur])
    else:
        run([PY, "engine/render_par.py", "--page", b["page"], "--data", f"{b['job']}/{b['scene']}", "--out", pic,
             "--duration", dur, "--jobs", a.jobs])
    print("[5/5] mix")
    bed = music_bed(job, b["music"], dur)
    cmd = [PY, "engine/mix.py", "--video", pic, "--voice", f"{b['job']}/input/voice.wav", "--sfx-dir", b["sfx"],
           "--cues", f"{b['job']}/{b['cue_file']}", "--out", job / f"out/{tag}.mp4", *b["mix"]]
    if bed:
        cmd += ["--music", bed]
    if b.get("mute_file") and (job / b["mute_file"]).exists():
        cmd += ["--music-mute", (job / b["mute_file"]).read_text(encoding="utf-8").strip()]
    run(cmd)
    out = job / f"out/{tag}.mp4"
    print(f"\ndone: {out.relative_to(ROOT)}")
    if not a.preview:
        compare(out, ROOT / "deliverables" / DELIV[a.type])


def measure(path):
    r = subprocess.run(["ffmpeg", "-nostats", "-i", str(path), "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True)
    lines = [l for l in r.stderr.splitlines() if l.strip().startswith("I:")]
    return lines[-1].split()[1] if lines else "?"


def compare(new, base):
    """Picture: PSNR of the whole clip vs the baseline (35+ dB = same picture after encoding). Sound: integrated loudness."""
    if not base.exists():
        return
    r = subprocess.run(["ffmpeg", "-i", str(new), "-i", str(base), "-lavfi", "[0:v][1:v]psnr", "-f", "null", "-"],
                       capture_output=True, text=True)
    psnr = next((l.split("average:")[1].split()[0] for l in r.stderr.splitlines() if "average:" in l), "?")
    print(f"vs {base.relative_to(ROOT)}: picture PSNR {psnr} dB (35+ = same picture), loudness {measure(new)} vs {measure(base)} LUFS")


if __name__ == "__main__":
    main()
