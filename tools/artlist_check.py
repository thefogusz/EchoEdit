"""List which Artlist files of the baselines are missing on this machine, with the Artlist ID to get each one.

usage: python tools/artlist_check.py [--json]

Nothing is downloaded here. The Artlist licence is per subscriber, so each person downloads with their OWN account:
  - in Claude with the Artlist connector: download_track(songId=<artlist_id>, kind=<music|sfx>, format=wav),
    then save the file at <path> (WAV, sample rate in save_as);
  - or on artlist.io: search the title, download WAV, save at <path>.
Without these files everything still runs: the mixer skips each missing sound and names it.
"""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
m = json.loads((ROOT / "library/audio/artlist_manifest.json").read_text(encoding="utf-8"))
missing = [it for it in m["items"] if not (ROOT / it["path"]).exists()]
if "--json" in sys.argv:
    print(json.dumps(missing, ensure_ascii=False, indent=1)); sys.exit()
print(f"{len(m['items']) - len(missing)}/{len(m['items'])} Artlist files present")
for it in missing:
    print(f"  missing {it['path']:<58} artlist_id {it['artlist_id']:>7} ({it['kind']})  {it['title']}")
if missing:
    print("Get them with YOUR Artlist account (see the top of this file). Each one is optional: the mix skips what is missing.")
