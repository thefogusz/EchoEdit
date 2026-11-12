"""Type 1 v3 on the forsample test clip: inserts on the word, like refs/type1 (คนพูด01/02).
Word times: input/words.json (ElevenLabs Scribe, word level). Stat: HubSpot 2025 State of AI in Marketing
("two-thirds of marketers across the globe use AI tools in their daily work", 1,500+ marketers; via Digiday 27 Oct 2025).
usage: python plan_v3.py  -> scene_v3.json for engine/pages/talkinghead3.html"""
import json, pathlib, sys
here = pathlib.Path(__file__).parent
sys.path.insert(0, str(here.parents[2] / "engine"))
from captions import phrases

words = json.loads((here / "input/words.json").read_text(encoding="utf-8"))
def W(text, after=0.0):  # start time of the first word == text at/after `after`
    for w in words:
        if w["start"] >= after - 1e-3 and w["text"] == text: return w["start"]
    raise KeyError((text, after))

DUR = 37.6
S = []
def seg(t0, t1, layout, insert=None, **kw): S.append(dict(t0=round(t0, 3), t1=round(t1, 3), layout=layout, insert=insert, **kw))

seg(0.0, W("ปีหน้า"), "full", zoom=1.1)                                                   # hook on the face
seg(W("ปีหน้า"), W("มองว่า", 3.5), "split", {"kind": "logos", "drain": W("เหนื่อย"), "items": [
    {"logo": "chatgpt_official", "at": W("AI") - 0.05, "h": 240}, {"logo": "claude_official", "at": W("AI") + 0.25, "h": 230},
    {"logo": "gemini_official", "at": W("แล้ว") + 0.05, "h": 150}]})
seg(W("มองว่า", 3.5), W("เหตุผล"), "cut", {"kind": "job", "at": W("มองว่า", 3.5) + 0.05, "title": "นักการตลาด", "sub": "Marketer",
                                            "tags": ["Content", "Ads", "ปีหน้าต้องใช้ AI"]})
seg(W("เหตุผล"), W("เมื่อก่อน"), "split", {"kind": "stat", "at": W("ส่วนใหญ่"), "to": 66, "lit": 2,
                                           "label": "ของนักการตลาดทั่วโลกใช้ AI ทุกวัน", "source": "ที่มา: HubSpot 2025 (1,500+ คน) · Digiday"})
seg(W("เมื่อก่อน"), W("เรา", 11.0), "split", {"kind": "post", "at": W("คอนเทนต์") - 0.1})
seg(W("เรา", 11.0), W("เมื่อก่อน", 15.0), "cut", {"kind": "versus", "at": [W("Quality"), W("Quantity")],
    "keys": [{"t": 0, "q": 0.5, "n": 0.5}]})
seg(W("เมื่อก่อน", 15.0), W("แต่"), "split", {"kind": "versus", "at": [W("เมื่อก่อน", 15.0), W("เมื่อก่อน", 15.0)],
    "keys": [{"t": 0, "q": 0.5, "n": 0.5}, {"t": W("แรง"), "q": 0.5, "n": 0.15}, {"t": W("Quality", 19.0), "q": 0.9, "n": 0.15},
             {"t": W("เพียง"), "q": 0.9, "n": 0.15, "check": 1}]})
seg(W("แต่"), W("ฉะนั้น"), "split", {"kind": "race", "even": W("สูสี"), "ai": W("AI", 26.5), "label": "คุณภาพสูสีกันหมด"})
seg(W("ฉะนั้น"), W("ฉะนั้น", 31.0), "cut", {"kind": "grid", "steps": [{"t": W("ฉะนั้น"), "n": 1}, {"t": W("จำนวน", 29.0), "n": 4},
                                                                       {"t": W("เข้ามา"), "n": 16}, {"t": W("ด้วย", 30.0), "n": 64}]})
seg(W("ฉะนั้น", 31.0), W("เพราะว่า", 35.5), "full", zoom=1.18)                              # the strong statement on the face
seg(W("เพราะว่า", 35.5), DUR, "split", {"kind": "crowd", "at": W("ทุก", 35.9), "label": "ทุกเจ้าใช้กันหมดแล้ว"})

for a, b in zip(S, S[1:]): assert abs(a["t1"] - b["t0"]) < 1e-6 and b["t0"] > a["t0"], (a, b)
caps = phrases(words, keywords=["AI", "Quality", "Quantity", "นักการตลาด", "ปีหน้า"])
scene = {"duration": DUR, "jobBase": here.resolve().as_uri(), "brandBase": (here.parents[2] / "brand").resolve().as_uri(), "footage": "assets/footage.webm",
         "segments": S, "captions": caps, "captionsInFull": False, "splitScale": 1.4,
         "logos": ["chatgpt_official", "claude_official", "gemini_official"],
         "face": json.loads((here / "assets/face.json").read_text())}
(here / "scene_v3.json").write_text(json.dumps(scene, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"{len(S)} segments: " + ", ".join(f"{s['layout']}:{s['t1'] - s['t0']:.1f}s" for s in S))
