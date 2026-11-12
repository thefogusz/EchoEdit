"""ElevenLabs TTS straight from the API with the user's own key (user, 2026-11-12: use an ElevenLabs API key
instead of Paxa). The whole script goes in ONE call so the voice stays consistent (per-line calls drift).
Returns the audio plus per-character timing, so no Scribe pass is needed.

Key: put ELEVENLABS_API_KEY=... in  ~/.config/dataechooo/elevenlabs.env  (never in the repo, never in chat).
This script reads it and never prints it.

usage: python pipelines/tts_elevenlabs.py <script.txt> <out.mp3> --voice <voice_id> [--model eleven_v4] [--speed 1.0]
writes out.mp3 + out.json  ({"chars": [{"text","start","end"}...]} at character level, usable as Scribe-style items)
"""
import argparse, base64, json, os, pathlib, sys, urllib.request, urllib.error

ap = argparse.ArgumentParser()
ap.add_argument("script"); ap.add_argument("out"); ap.add_argument("--voice", required=True)
ap.add_argument("--model", default="eleven_v4"); ap.add_argument("--speed", type=float, default=1.0)
ap.add_argument("--stability", type=float, default=0.5)
a = ap.parse_args()

env = pathlib.Path.home() / ".config/dataechooo/elevenlabs.env"
key = os.environ.get("ELEVENLABS_API_KEY")
if not key and env.exists():
    for line in env.read_text(encoding="utf-8").splitlines():
        if line.strip().startswith("ELEVENLABS_API_KEY="): key = line.split("=", 1)[1].strip().strip('"')
if not key: sys.exit(f"no key: put ELEVENLABS_API_KEY=... in {env}")

text = pathlib.Path(a.script).read_text(encoding="utf-8").strip()
body = {"text": text, "model_id": a.model, "voice_settings": {"stability": a.stability, "similarity_boost": 0.8, "speed": a.speed}}
req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{a.voice}/with-timestamps",
                             data=json.dumps(body).encode(), method="POST",
                             headers={"xi-api-key": key, "Content-Type": "application/json", "Accept": "application/json"})
try:
    r = json.load(urllib.request.urlopen(req, timeout=300))
except urllib.error.HTTPError as e:
    sys.exit(f"ElevenLabs HTTP {e.code}: {e.read()[:300].decode(errors='replace')}")
out = pathlib.Path(a.out)
out.write_bytes(base64.b64decode(r["audio_base64"]))
al = r.get("alignment") or r.get("normalized_alignment") or {}
chars = [{"text": c, "start": round(s, 3), "end": round(e, 3)}
         for c, s, e in zip(al.get("characters", []), al.get("character_start_times_seconds", []), al.get("character_end_times_seconds", []))]
out.with_suffix(".json").write_text(json.dumps({"chars": chars}, ensure_ascii=False), encoding="utf-8")
print(f"wrote {out} ({len(text)} chars, {len(chars)} timed)")
