"""Type 2 v3 (shot-based edit): plan_v3.json + Scribe words + voice -> scene_v3.json for engine/pages/news3.html (plan_v8.json).

usage: python pipelines/news/build_shots.py jobs/<job> [plan_v3.json]
Shot times are authored on the current take (input/words.json). Doc shots need assets/docs/docs.json
from engine/tools/grab_doc.py.
"""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "engine"))
from captions import phrases, sets_from_script, words_from_scribe, words_from_char_units, is_char_level, chunk, envelope

job = pathlib.Path(sys.argv[1]).resolve()
plan = json.loads((job / (sys.argv[2] if len(sys.argv) > 2 else "plan_v3.json")).read_text(encoding="utf-8"))
items = [w for w in json.loads((job / "input/words.json").read_text(encoding="utf-8")) if w.get("type", "word") == "word" and not w["text"].startswith("[")]
words = words_from_char_units(items, plan.get("fixes")) if is_char_level(items) else words_from_scribe(items)
cs = plan.get("caption_script", "")
if cs.startswith("@"): cs = (job / cs[1:]).read_text(encoding="utf-8")  # caption script kept in its own file
caps = (sets_from_script(cs, items, plan.get("keywords", [])) if cs
        else phrases(words, keywords=plan.get("keywords", [])))  # script-aligned Thai sets preferred
# numerals ("$40") cannot align to spoken Thai ("สี่สิบ"): plan.caption_starts pins a set's start to the word time
for txt, st in plan.get("caption_starts", {}).items():
    for k, c in enumerate(caps):
        if " ".join(w["text"] for w in c["words"]).startswith(txt):
            c["start"] = st
            for w in c["words"]: w["start"] = max(w["start"], st)
            if k: caps[k - 1]["end"] = min(caps[k - 1]["end"], st - 0.02)
shots = plan["shots"]
for s in shots:  # src_tag is an alias kept readable in the plan
    if "src_tag" in s: s["src"] = s.pop("src_tag")
# a shot is complete on its first frame (rule from user review): something must land within 0.2 s of the cut
for s in shots:
    if "pieces" in s:
        first = min((p.get("at", 0) for p in s["pieces"]), default=99)
        assert first <= 0.2, f"empty-start shot at {s['t0']}s: first piece arrives at +{first}s"
# continuity check: shots must tile the timeline with no gaps/overlaps
for a, b in zip(shots, shots[1:]):
    assert abs(a["t1"] - b["t0"]) < 1e-6, f"gap/overlap between {a['t1']} and {b['t0']}"
scene = {
    "duration": shots[-1]["t1"],
    "jobBase": job.as_uri(),
    "docs": json.loads((job / "assets/docs/docs.json").read_text(encoding="utf-8")),
    "captions": caps, "shots": shots, "flashes": plan.get("flashes", []), "desks": plan.get("desks"), "grid": plan.get("grid"), "deskDim": plan.get("deskDim"),
    "mascot": dict(plan.get("mascot", {}), env=envelope(job / "input/voice.wav", fps=30)),
}
(job / "scene_v3.json").write_text(json.dumps(scene, ensure_ascii=False, indent=1), encoding="utf-8")
lens = [round(s["t1"] - s["t0"], 2) for s in shots]
print(f"{len(shots)} shots, len min/avg/max = {min(lens)}/{sum(lens)/len(lens):.2f}/{max(lens)} s; {len(caps)} caption chunks; duration {scene['duration']}")
