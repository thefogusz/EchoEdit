"""Finalize a clip (user rule 2026-11-12): when the user calls a clip final, delete every unused draft and
intermediate, keep only what rebuilds the final, and make sure its sounds live in library/.

usage: python tools/finalize_job.py <job dir> <final mp4 name> [--yes]
Without --yes it only PRINTS what would be deleted (dry run). Show that list to the user before running with --yes.

Keeps: the final mp4 (+ its *_picture.mp4), the scene/plan/cues/captions files the final was built from (newest of
each kind), scripts, input/ (voice, words, music bed), assets/ actually used, docs. Deletes: other out/ renders, stills,
QA sheets, chunk folders, stems, old plan/scene versions, voice test takes, _trim folders.
"""
import sys, pathlib, re, shutil

job = pathlib.Path(sys.argv[1]).resolve(); final = sys.argv[2]; really = "--yes" in sys.argv
out = job / "out"
keep = {out / final, out / final.replace(".mp4", "_picture.mp4")}
# picture source of a remix (e.g. v7b uses v7_picture)
m = re.match(r"(.*_v\d+)[a-z]?\.mp4$", final)
if m: keep.add(out / f"{m.group(1)}_picture.mp4")
dele = []
for p in out.rglob("*"):
    if p.is_file() and p not in keep: dele.append(p)
# old versions of plan/scene/cues/script: keep only the newest number of each stem
groups = {}
for p in job.glob("*_v*.*"):
    mm = re.match(r"(.+)_v(\d+)[a-z]?(\..+)$", p.name)
    if mm: groups.setdefault((mm.group(1), mm.group(3)), []).append((int(mm.group(2)), p))
for _, items in groups.items():
    items.sort()
    dele += [p for _, p in items[:-1]]
for pat in ("voice_tests*", "voice/_trim", "scene_style.json", "stills.txt"):
    for p in job.glob(pat):
        dele += [q for q in p.rglob("*") if q.is_file()] if p.is_dir() else [p]
size = sum(p.stat().st_size for p in dele if p.exists())
for p in sorted(set(dele)): print("DEL", p.relative_to(job))
print(f"{len(set(dele))} files, {size / 1e6:.0f} MB {'deleted' if really else 'would be deleted (dry run)'}")
if really:
    for p in set(dele):
        if p.exists(): p.unlink()
    for d in sorted([d for d in job.rglob("*") if d.is_dir()], key=lambda d: -len(d.parts)):
        if not any(d.iterdir()): d.rmdir()
