"""One-step setup for EchoEdit on a new machine (Windows / macOS / Linux). Safe to run again.

usage: python tools/setup.py [--yes] [--earshot] [--no-test]
  --yes       answer yes to installs it would ask about (ffmpeg via winget/brew)
  --earshot   also install earshot (optional audio QA; ~2 GB with CPU torch)
  --no-test   skip the 2-second render test of the three baseline clips

What it does:
  1. checks Python (3.10+)
  2. makes .venv in the repo and installs requirements.txt + Playwright Chromium
  3. checks ffmpeg/ffprobe (offers to install them)
  4. creates ~/.config/dataechooo/elevenlabs.env for your ElevenLabs key (you paste the key; it is never printed)
  5. checks Codex CLI (images in the ChatGPT plan) and its sign-in
  6. scans every tool (tools/capabilities.py) and renders 2 s of each baseline clip as a test
Afterwards: run Python through .venv (Windows: .venv\\Scripts\\python, macOS/Linux: .venv/bin/python).
"""
import argparse, os, pathlib, platform, shutil, subprocess, sys, venv

ROOT = pathlib.Path(__file__).resolve().parents[1]
WIN = platform.system() == "Windows"
VPY = ROOT / (".venv/Scripts/python.exe" if WIN else ".venv/bin/python")
OK, NO, WARN = "[ok]", "[!!]", "[--]"
problems = []


def say(tag, msg):
    print(f"{tag} {msg}", flush=True)
    if tag == NO:
        problems.append(msg)


def ask(q, yes):
    if yes:
        return True
    try:
        return input(f"{q} [y/N] ").strip().lower() in ("y", "yes")
    except EOFError:
        return False


def run(cmd, **kw):
    return subprocess.run([str(c) for c in cmd], **kw)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--yes", action="store_true"); ap.add_argument("--earshot", action="store_true")
    ap.add_argument("--no-test", action="store_true")
    a = ap.parse_args()

    print("== 1. Python")
    if sys.version_info < (3, 10):
        sys.exit(f"Python 3.10+ needed, this is {platform.python_version()}. Install from python.org, then run again.")
    say(OK, f"Python {platform.python_version()}")

    print("== 2. Python packages (.venv)")
    if not VPY.exists():
        venv.EnvBuilder(with_pip=True).create(ROOT / ".venv")
    r = run([VPY, "-m", "pip", "install", "-q", "--upgrade", "pip"])
    r = run([VPY, "-m", "pip", "install", "-q", "-r", ROOT / "requirements.txt"])
    say(OK if r.returncode == 0 else NO, "requirements.txt" + ("" if r.returncode == 0 else " failed (see pip output above)"))
    r = run([VPY, "-m", "playwright", "install", "chromium"])
    say(OK if r.returncode == 0 else NO, "Chromium for Playwright")

    print("== 3. ffmpeg")
    if not (shutil.which("ffmpeg") and shutil.which("ffprobe")):
        cmd = (["winget", "install", "-e", "--id", "Gyan.FFmpeg", "--accept-source-agreements", "--accept-package-agreements"] if WIN
               else ["brew", "install", "ffmpeg"] if platform.system() == "Darwin" else None)
        if cmd and shutil.which(cmd[0]) and ask(f"ffmpeg is missing. Install it with: {' '.join(cmd[:4])} ?", a.yes):
            run(cmd)
            say(WARN, "ffmpeg installed: close and reopen the terminal (PATH), then run setup again")
        else:
            say(NO, "ffmpeg missing: Windows `winget install Gyan.FFmpeg`, macOS `brew install ffmpeg`, Linux `sudo apt install ffmpeg`")
    else:
        v = run(["ffmpeg", "-version"], capture_output=True, text=True).stdout.split("\n")[0]
        say(OK, v[:60])
        if "libvpx" not in run(["ffmpeg", "-hide_banner", "-encoders"], capture_output=True, text=True).stdout:
            say(NO, "this ffmpeg has no libvpx (VP9): install a full build (Gyan.FFmpeg / brew ffmpeg)")

    print("== 4. ElevenLabs key (voice + word timing)")
    env = pathlib.Path.home() / ".config/dataechooo/elevenlabs.env"
    if not env.exists():
        env.parent.mkdir(parents=True, exist_ok=True)
        env.write_text("# paste your key after the = sign. Never commit or share this file.\nELEVENLABS_API_KEY=\n", encoding="utf-8")
    has = any(l.startswith("ELEVENLABS_API_KEY=") and l.split("=", 1)[1].strip() for l in env.read_text(encoding="utf-8").splitlines())
    say(OK if has or os.environ.get("ELEVENLABS_API_KEY") else WARN,
        f"key {'found' if has else 'not set yet: open ' + str(env) + ' and paste it after ELEVENLABS_API_KEY='}")

    print("== 5. Codex CLI (images inside a ChatGPT plan)")
    sys.path.insert(0, str(ROOT / "tools"))
    from run_codex import find_codex
    cx = find_codex()
    if not cx:
        say(WARN, "Codex CLI not found (optional, for new images): npm install -g @openai/codex, then codex login")
    else:
        st = run([cx, "login", "status"], capture_output=True, text=True)
        say(OK if st.returncode == 0 else WARN, f"Codex {'signed in' if st.returncode == 0 else 'found but not signed in: run codex login'}")

    if a.earshot:
        print("== earshot (optional audio QA)")
        run([VPY, "-m", "pip", "install", "-q", "torch", "--index-url", "https://download.pytorch.org/whl/cpu"])
        r = run([VPY, "-m", "pip", "install", "-q", "earshot[mcp] @ git+https://github.com/Leonxlnx/earshot"])
        say(OK if r.returncode == 0 else NO, "earshot (run: .venv python -m earshot doctor)")

    print("== 6. Tool scan")
    run([VPY, ROOT / "tools/capabilities.py"], env={**os.environ, "PYTHONUTF8": "1"})
    if not a.no_test and shutil.which("ffmpeg"):
        print("== 7. Test: render + mix 2 s of each baseline clip")
        for t in ("type1", "type2", "type3"):
            r = run([VPY, ROOT / "tools/rebuild.py", t, "--preview", "2"], env={**os.environ, "PYTHONUTF8": "1"})
            say(OK if r.returncode == 0 else NO, f"{t} 2-second test" + ("" if r.returncode == 0 else " failed (output above)"))

    music = list((ROOT / "library/audio/music").glob("*.wav"))
    print("\n== Summary")
    if not music:
        say(WARN, "Artlist music not on this machine (SFX are in the repo): python tools/artlist_check.py lists it; download with your own Artlist account")
    if problems:
        print("Fix these, then run setup again:"); [print("  -", p) for p in problems]; sys.exit(1)
    print(f"Ready. Python for this repo: {VPY.relative_to(ROOT)}. Open the folder in Claude Code and ask for a clip.")


if __name__ == "__main__":
    main()
