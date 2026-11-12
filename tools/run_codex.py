"""Run one Codex CLI job (image generation or a scoped code task) inside the user's ChatGPT plan. No API key, no extra cost.

usage: python tools/run_codex.py <TASK.md> <job-name> [--images a.png,b.png] [--effort low|medium|high] [--read-only]
  TASK.md   a brief (see docs/prompts/): outcome, locked style, file list, acceptance, where to write
  job-name  a new folder work/codex-jobs/<job-name>/ (must not exist). Codex runs there; outputs land under it.
  --images  reference images Codex should look at (absolute or repo-relative paths, comma separated)

Needs: Codex CLI installed and signed in (`codex login`, ChatGPT account). tools/setup.py checks it.
Writes: final.md (Codex's answer), events.jsonl, stderr.log, exit-code.txt in the job folder.
Then: check the images yourself (open them), copy the good ones into the clip's assets/.
"""
import argparse, glob, os, pathlib, shutil, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]


def find_codex():
    if os.environ.get("CODEX_BIN"):
        return os.environ["CODEX_BIN"]
    hit = shutil.which("codex")
    if hit:
        return hit
    # the Codex desktop app on Windows keeps its CLI in a hashed folder that changes on update: take the newest
    cands = glob.glob(os.path.expanduser("~/AppData/Local/OpenAI/Codex/bin/*/codex.exe"))
    cands += glob.glob("/Applications/Codex.app/Contents/Resources/codex")
    return max(cands, key=os.path.getmtime) if cands else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("task"); ap.add_argument("name")
    ap.add_argument("--images", default="")
    ap.add_argument("--effort", default="medium", choices=["low", "medium", "high"])
    ap.add_argument("--read-only", action="store_true")
    a = ap.parse_args()

    codex = find_codex()
    if not codex:
        sys.exit("Codex CLI not found. Install: npm install -g @openai/codex  then: codex login  (or set CODEX_BIN)")
    task = pathlib.Path(a.task).resolve()
    if not task.exists():
        sys.exit(f"task file missing: {task}")
    out = ROOT / "work/codex-jobs" / a.name
    if out.exists():
        sys.exit(f"{out} already exists: pick a new job name")
    out.mkdir(parents=True)
    images = [str(pathlib.Path(p).resolve()) for p in a.images.split(",") if p]
    for p in images:
        if not pathlib.Path(p).exists():
            sys.exit(f"image missing: {p}")

    args = [codex, "-a", "never", "exec", "-C", str(out), "--skip-git-repo-check",
            "-s", "read-only" if a.read_only else "workspace-write",
            "-c", f'model_reasoning_effort="{a.effort}"', "--json", "-o", str(out / "final.md")]
    if images:
        args += ["-i", ",".join(images)]
    args += ["-"]
    print(f"codex job -> {out.relative_to(ROOT)} (this can take several minutes)", flush=True)
    (out / "version.txt").write_text(subprocess.run([codex, "--version"], capture_output=True, text=True).stdout)
    with open(task, "rb") as fin, open(out / "events.jsonl", "wb") as fev, open(out / "stderr.log", "wb") as ferr:
        rc = subprocess.run(args, stdin=fin, stdout=fev, stderr=ferr).returncode
    if rc == 0 and not (out / "final.md").exists():
        rc = 1
        (out / "stderr.log").open("a").write("Codex exited without a final answer\n")
    (out / "exit-code.txt").write_text(str(rc))
    made = [str(p.relative_to(out)) for p in out.rglob("*.png")]
    print(f"exit={rc}; images: {len(made)}")
    for m in made:
        print("  ", m)
    if rc:
        print(f"see {(out / 'stderr.log').relative_to(ROOT)}")
    sys.exit(rc)


if __name__ == "__main__":
    main()
