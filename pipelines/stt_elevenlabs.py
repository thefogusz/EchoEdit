"""ElevenLabs Scribe speech-to-text with word timestamps, using the user's own key
(~/.config/dataechooo/elevenlabs.env, ELEVENLABS_API_KEY=...; never printed).
usage: python pipelines/stt_elevenlabs.py <audio_or_video> <out.json> [--lang tha]
writes {"text": ..., "words": [{"text","start","end","type"}...]} (Scribe items; Thai comes back per character)."""
import argparse, json, os, pathlib, subprocess, sys, tempfile, uuid, urllib.request, urllib.error

ap = argparse.ArgumentParser(); ap.add_argument("src"); ap.add_argument("out"); ap.add_argument("--lang", default="tha")
a = ap.parse_args()
env = pathlib.Path.home() / ".config/dataechooo/elevenlabs.env"
key = os.environ.get("ELEVENLABS_API_KEY")
if not key and env.exists():
    for line in env.read_text(encoding="utf-8").splitlines():
        if line.strip().startswith("ELEVENLABS_API_KEY="): key = line.split("=", 1)[1].strip().strip('"')
if not key: sys.exit(f"no key: put ELEVENLABS_API_KEY=... in {env}")

tmp = pathlib.Path(tempfile.gettempdir()) / f"stt_{uuid.uuid4().hex}.mp3"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.src, "-vn", "-ac", "1", "-ar", "16000", "-b:a", "64k", str(tmp)], check=True)
b = "----dataechooo" + uuid.uuid4().hex
parts = []
for k, v in (("model_id", "scribe_v1"), ("language_code", a.lang), ("timestamps_granularity", "word"), ("tag_audio_events", "false")):
    parts.append(f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
parts.append(f'--{b}\r\nContent-Disposition: form-data; name="file"; filename="a.mp3"\r\nContent-Type: audio/mpeg\r\n\r\n'.encode() + tmp.read_bytes() + b"\r\n")
parts.append(f"--{b}--\r\n".encode())
req = urllib.request.Request("https://api.elevenlabs.io/v1/speech-to-text", data=b"".join(parts), method="POST",
                             headers={"xi-api-key": key, "Content-Type": f"multipart/form-data; boundary={b}"})
try:
    r = json.load(urllib.request.urlopen(req, timeout=600))
except urllib.error.HTTPError as e:
    sys.exit(f"ElevenLabs HTTP {e.code}: {e.read()[:300].decode(errors='replace')}")
finally:
    tmp.unlink(missing_ok=True)
pathlib.Path(a.out).write_text(json.dumps({"text": r.get("text", ""), "words": r.get("words", [])}, ensure_ascii=False), encoding="utf-8")
print(f"wrote {a.out}: {len(r.get('words', []))} items")
