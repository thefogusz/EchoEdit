"""Type 3 / NVIDIA Part 1 v3: shotplan_v3.md -> scene.json for engine/pages/story2d.html.
Voice: Aidan, one take (voice_el/full_v2.mp3 -> input/voice.wav, input/words.json). One spoken phrase = one cut.
Built from the ref shot catalog (docs/REF_TYPE3_SHOTS.md): counters on every number, props change on the word,
push-in lands on the key word, same frame new era, top-down table for plans/money, gags after lines.
usage: python part1_scene_v3.py  (writes scene.json + music_mute.txt)"""
import json, pathlib, sys
here = pathlib.Path(__file__).parent
sys.path.insert(0, str(here.parents[2] / "engine"))
from captions import sets_from_script

words = json.loads((here / "input/words.json").read_text(encoding="utf-8"))
caps = sets_from_script((here / "caption_script_v2.txt").read_text(encoding="utf-8"), words, ["NVIDIA", "Jensen", "30", "1992", "1993", "1996", "1997", "NV1", "Sega"])
T = [c["start"] for c in caps]   # phrase starts: cuts land here
P = {k: f"assets/plates/{v}.png" for k, v in {
    "kitchen": "b01_kitchen", "booth": "b02_booth", "office": "b03_office", "city": "b04_city", "stage": "b05_stage",
    "store": "b06_store", "meeting": "b07_meeting", "floor": "b08_floor", "dinertop": "b09_diner_top", "desktop": "b10_desk_top"}.items()}

def cam(z0, z1, x0=540, y0=960, x1=None, y1=None):
    return {"z": [z0, z1], "x": [x0, x1 if x1 is not None else x0], "y": [y0, y1 if y1 is not None else y0]}
S = []
def shot(t0, t1, **kw): S.append(dict(t0=round(t0, 3), t1=round(t1, 3), **kw))
END = 62.5
NOW = lambda **k: dict({"who": "jensenNow", "x": 540, "y": 1120, "scale": 1.6}, **k)
FOUND = lambda pose, face, y=1400: [{"who": "chris", "x": 230, "y": y, "scale": 1.45, "pose": pose, "face": face},
                                    {"who": "jensen", "x": 520, "y": y + 20, "scale": 1.5, "pose": pose, "face": face},
                                    {"who": "curtis", "x": 800, "y": y, "scale": 1.45, "pose": pose, "face": face, "dir": -1}]
BOOTH = [{"who": "chris", "x": 245, "y": 1255, "scale": 1.12, "seated": True, "pose": "point", "face": "grin"},
         {"who": "jensen", "x": 540, "y": 1255, "scale": 1.12, "seated": True, "pose": "idle", "face": "smile", "look": -0.4},
         {"who": "curtis", "x": 835, "y": 1255, "scale": 1.12, "seated": True, "pose": "think", "face": "neutral", "dir": -1}]
BOOTH_CAM = cam(1.04, 1.07, 540, 1060)
NUMC = dict(color="#214AFF", glow="rgba(255,255,255,.95)")

# 1 hook: the line itself, typed with the voice (ref: twist line alone on a card)
shot(0, T[2], card={"lines": ["\u201cอีก 30 วัน", "บริษัทเราจะเจ๊ง\u201d"], "hot": 1, "size": 96, "type": T[2] - 0.4})
# 2 "not from a small company": tiny office, nobody there, slow push
shot(T[2], T[4], plate="office", cam=cam(1.0, 1.06, 520, 980))
# 3 "but from the CEO": push+blur to the stage, push-in lands on the word
shot(T[4], T[5], plate="stage", **{"in": "push"}, cam=cam(1.04, 1.22, 540, 900, 540, 800), actors=[NOW(pose="point", face="grin", look=0.3)],
     tags=[{"text": "CEO", "sub": "NVIDIA", "ax": 560, "ay": 700, "x": 640, "y": 520, "at": T[4] + 0.15}])
# 4 the tower: crane up (power), $5T counter lands on "5 ล้านล้าน"
shot(T[5], T[7], plate="city", cam=cam(1.15, 1.2, 540, 1300, 540, 700),
     counters=[dict(NUMC, **{"from": 0, "to": 5, "prefix": "$", "suffix": "T", "x": 540, "y": 980, "at": T[6] + 0.1, "dur": 1.1, "size": 240, "label": "มูลค่าบริษัท (ต.ค. 2025)"})])
# 5 chapter title (flash in, music comes in with a stab)
shot(T[7], T[8], **{"in": "flash"}, card={"title": "NVIDIA", "sub": "30 วันก่อนเจ๊ง · Part 1"})
# 6 Jensen waves, tag beside his head
shot(T[8], T[9], plate="stage", cam=cam(1.12, 1.18, 540, 900), actors=[NOW(y=1130, scale=1.7, pose="wave", face="grin")],
     tags=[{"text": "Jensen Huang", "sub": "ผู้ก่อตั้ง NVIDIA", "ax": 600, "ay": 660, "x": 640, "y": 470, "at": T[8] + 0.1}])
# 7 flashback: year rolls back
shot(T[9], T[10], rewind={"from": 2025, "to": 1978})
# 8 Denny's 1978, wide dollhouse frame; teenage Jensen walks in
shot(T[10], T[12], plate="booth", cam=BOOTH_CAM, chip={"text": "1978 · ร้าน Denny's", "at": T[10] + 0.1},
     actors=[{"who": "jensen15", "x": 1250, "y": 1560, "dir": -1, "scale": 1.7, "pose": "idle", "face": "smile", "walk": True,
              "keys": [{"t": T[10], "x": 1250}, {"t": T[11] + 0.5, "x": 870}, {"t": T[11] + 0.6, "walk": False}]}])
# 9 "washing dishes": kitchen
shot(T[12], T[13], plate="kitchen", cam=cam(1.15, 1.2, 520, 960),
     actors=[{"who": "jensen15", "x": 600, "y": 1290, "scale": 1.75, "pose": "scrub", "face": "tired", "look": -0.4}],
     props=[{"kind": "dish", "x": 600, "y": 1185, "s": 1.0, "front": True}])
# 10 back in the same Denny's frame: tray, and the plate tower keeps growing (gag)
shot(T[13], T[14], plate="booth", cam=BOOTH_CAM,
     actors=[{"who": "jensen15", "x": 1000, "y": 1560, "dir": -1, "scale": 1.7, "pose": "hold", "face": "worried", "walk": True,
              "keys": [{"t": T[13], "x": 1000}, {"t": T[14], "x": 820}]}],
     props=[{"kind": "tray", "follow": 0, "dx": 0, "dy": -165, "s": 1.0, "front": True},
            {"kind": "stack", "follow": 0, "dx": -30, "dy": -190, "n0": 3, "n1": 15, "at": T[13] + 0.2, "dur": 1.4, "front": True}])
# 11 same frame, new era: 1992, three engineers in the booth
shot(T[14], T[15], plate="booth", fg={"y": 1118}, cam=BOOTH_CAM, actors=BOOTH, chip={"text": "ปลายปี 1992 · ร้าน Denny's", "at": T[14] + 0.05})
# 12 tags pop one at a time
w = (T[16] - T[15]) / 3
shot(T[15], T[16], plate="booth", fg={"y": 1118}, cam=cam(1.07, 1.12, 540, 1060), actors=BOOTH,
     tags=[{"text": "Chris", "ax": 245, "ay": 900, "x": 120, "y": 690, "at": T[15], "until": T[15] + w},
           {"text": "Jensen", "ax": 540, "ay": 900, "x": 440, "y": 690, "at": T[15] + w, "until": T[15] + 2 * w},
           {"text": "Curtis", "ax": 835, "ay": 900, "x": 960, "y": 690, "at": T[15] + 2 * w, "align": "right"}])
# 13 top-down table: the chip idea drawn on a napkin
shot(T[16], T[18], plate="dinertop", cam=cam(1.0, 1.08, 540, 960),
     props=[{"kind": "napkin", "x": 540, "y": 960, "s": 1.7, "r": -0.06, "at": T[16] + 0.2, "front": True}])
# 14 April 1993: founders arrive in the tiny office
shot(T[18], T[19], plate="office", **{"in": "push"}, cam=cam(1.08, 1.12, 500, 1060), actors=FOUND("idle", "smile"),
     chip={"text": "เมษายน 1993", "at": T[18] + 0.1})
# 15 NVIDIA is born: push-in lands on the word, cheer
shot(T[19], T[20], plate="office", cam=cam(1.1, 1.25, 500, 1080, 520, 1060), actors=FOUND("cheer", "grin"),
     tags=[{"text": "NVIDIA", "sub": "บริษัทเกิดแล้ว", "ax": 520, "ay": 990, "x": 600, "y": 600, "at": T[19] + 0.4}])
# 16 first chip NV1: store, push-in lands on the box
BOX = {"kind": "box", "x": 540, "y": 990, "s": 1.3, "label": "NV1", "price": "$249", "price2": "$99", "drop": T[21] + 0.15}
shot(T[20], T[21], plate="store", **{"in": "push"}, cam=cam(1.0, 1.3, 540, 1000, 560, 900), props=[BOX])
# 17 same frame: doesn't sell -> price drops on the word, dust
shot(T[21], T[22], plate="store", cam=cam(1.3, 1.34, 560, 900), props=[BOX])
# 18 top-down: the Sega deal tears, red X
shot(T[22], T[23], plate="desktop", cam=cam(1.0, 1.05, 540, 960),
     props=[{"kind": "contract", "x": 540, "y": 960, "s": 1.6, "tear": T[22] + 0.75, "front": True},
            {"kind": "redx", "x": 540, "y": 960, "r": 150, "at": T[22] + 1.0, "front": True}])
# 19 "but Sega's president": the other side (push+blur)
shot(T[23], T[24], plate="meeting", **{"in": "push"}, cam=cam(1.15, 1.2, 640, 1000),
     actors=[{"who": "sega", "x": 640, "y": 1350, "scale": 1.6, "pose": "hold", "face": "smile", "dir": -1}],
     tags=[{"text": "ประธาน Sega", "ax": 640, "ay": 900, "x": 760, "y": 640, "at": T[23] + 0.1}])
# 20 top-down: the cheque slides in, $5,000,000 counts up on the word
shot(T[24], T[25], plate="desktop", cam=cam(1.0, 1.05, 540, 960),
     props=[{"kind": "check", "x0": 1100, "x": 540, "y": 900, "s": 1.6, "at": T[24] + 0.1, "text": "$5,000,000", "front": True}],
     counters=[dict(NUMC, **{"from": 0, "to": 5000000, "prefix": "$", "x": 540, "y": 1190, "at": T[24] + 0.9, "dur": 1.0, "size": 130})])
# 21 "Jensen said": medium close, talking
shot(T[25], T[26], plate="office", cam=cam(1.25, 1.3, 420, 1000),
     actors=[{"who": "jensen", "x": 380, "y": 1450, "scale": 1.8, "pose": "point", "face": "talk", "look": 0.5}])
# 22 six months: counter lands on the word
shot(T[26], T[28], plate="office", cam=cam(1.25, 1.32, 420, 1000),
     actors=[{"who": "jensen", "x": 380, "y": 1450, "scale": 1.8, "pose": "think", "face": "worried", "look": 0.5}],
     counters=[dict(NUMC, **{"from": 0, "to": 6, "suffix": " เดือน", "x": 760, "y": 640, "at": T[27] + 0.8, "dur": 0.6, "size": 150})])
# 23 1996: 100 people, 60 vanish on "เหลือ 40" (same frame)
shot(T[28], T[31], plate="floor", **{"in": "push"}, cam=cam(1.02, 1.06, 540, 980), chip={"text": "ปี 1996", "at": T[28] + 0.1},
     props=[{"kind": "crowd", "cols": 10, "rows": 10, "x": 270, "y": 640, "dx": 60, "dy": 62, "keep": 40, "cut": T[30], "front": True}],
     counters=[dict(NUMC, **{"from": 0, "to": 100, "suffix": " คน", "x": 540, "y": 1560, "at": T[29] + 0.3, "dur": 0.6, "size": 150, "until": T[30]}),
               dict(NUMC, **{"from": 100, "to": 40, "suffix": " คน", "x": 540, "y": 1560, "at": T[30], "dur": 0.6, "size": 150, "color": "#FE4C1C"})])
# 24 mid-1997: the phone rings (music drops out)
shot(T[31], T[32], plate="office", **{"in": "push"}, cam=cam(1.15, 1.2, 520, 1000), chip={"text": "กลางปี 1997", "at": T[31] + 0.1},
     actors=[{"who": "jensen", "x": 300, "y": 1400, "scale": 1.6, "pose": "idle", "face": "shock", "look": 1}],
     props=[{"kind": "phone", "x": 640, "y": 880, "s": 1.0, "ring0": T[31] + 0.1, "ring1": T[32], "front": True}])
# 25 payroll: push-in on his face
shot(T[32], T[33], plate="office", cam=cam(1.25, 1.4, 380, 960, 360, 900),
     actors=[{"who": "jensen", "x": 360, "y": 1420, "scale": 1.7, "pose": "head", "face": "worried"}])
# 26 one month left: zoom into the calendar, page flips (gag)
shot(T[33], T[34], plate="office", **{"in": "zoom"}, cam=cam(1.5, 1.6, 880, 600),
     props=[{"kind": "calendar", "x": 880, "y": 640, "s": 1.0, "from": 30, "to": 29, "flip": T[33] + 0.9, "hot": True, "head": "เงินเดือนเหลืออีก", "front": True}])
# 27 top-down desk: one chip left
shot(T[34], T[35], plate="desktop", cam=cam(1.0, 1.12, 540, 960),
     props=[{"kind": "chip", "x": 540, "y": 960, "s": 1.9, "at": T[34] + 0.05, "label": "?", "front": True}])
# 28 pull-back: how small he is in the empty office
shot(T[35], T[36], plate="office", cam=cam(1.5, 1.0, 330, 1150, 540, 960),
     actors=[{"who": "jensen", "x": 330, "y": 1400, "scale": 1.3, "pose": "think", "face": "worried", "look": 1}])
# 29 cliffhanger card, typed with the voice
shot(T[36], T[38], card={"lines": ["มันจะทันไหม?", "ติดตาม Part 2"], "hot": 1, "size": 96, "type": T[38] - T[36] - 0.3})
# 30 CTA: logo + follow button + the founders waving
shot(T[38], END, noLogo=True, cta={"button": "กดติดตาม", "actors": [
    {"who": "chris", "x": 250, "y": 1560, "scale": 1.45, "pose": "wave", "face": "grin"},
    {"who": "jensen", "x": 540, "y": 1600, "scale": 1.6, "pose": "cheer", "face": "grin"},
    {"who": "curtis", "x": 830, "y": 1560, "scale": 1.45, "pose": "wave", "face": "grin", "dir": -1}]})

for a, b in zip(S, S[1:]): assert abs(a["t1"] - b["t0"]) < 1e-6, (a["t1"], b["t0"])
quiet = [(x["t0"], x["t1"]) for x in S if x.get("card") or x.get("cta") or x.get("rewind")]
caps = [c for c in caps if not any(c["start"] >= q0 - 0.05 and c["start"] < q1 for q0, q1 in quiet)]
for c in caps:
    for q0, q1 in quiet:
        if c["start"] < q0 < c["end"]: c["end"] = q0 - 0.02
D = {"jobBase": here.resolve().as_uri(), "brandBase": (here.parents[2] / "brand").resolve().as_uri(),
     "plates": P, "captions": caps, "capY": 1400, "duration": END,
     "pill": {"from": T[27], "to": T[36], "label": "เงินพอจ่ายเงินเดือนอีก",
              "values": [{"t": T[27], "text": None}, {"t": T[27] + 1.2, "text": "6 เดือน"}, {"t": T[28], "text": None},
                         {"t": T[32], "text": "1 เดือน", "hot": True}, {"t": T[33], "text": None}, {"t": T[34], "text": "1 เดือน", "hot": True}]},
     "music_mute": [[0.0, T[7]], [T[31], T[36]]],
     "extra_cues": [  # foley: sounds of the scene itself (ref), library/audio/foley
        {"t": 0.15, "sfx": "tick", "db": -22, "dur": T[2] - 0.3},
        {"t": T[6] + 0.1, "sfx": "swell", "db": -19, "align": "end"},
        {"t": T[10], "sfx": "diner_walla", "db": -27, "dur": T[12] - T[10]},
        {"t": T[12], "sfx": "dishes_sink", "db": -19, "dur": T[13] - T[12]},
        {"t": T[13], "sfx": "diner_walla", "db": -27, "dur": T[16] - T[13]},
        {"t": T[13] + 0.35, "sfx": "cup_place", "db": -21}, {"t": T[13] + 0.85, "sfx": "cup_place", "db": -21}, {"t": T[13] + 1.35, "sfx": "cup_place", "db": -20},
        {"t": T[16] + 0.2, "sfx": "pencil", "db": -19, "dur": 2.4},
        {"t": T[22] + 0.75, "sfx": "paper_tear", "db": -16},
        {"t": T[24] + 0.1, "sfx": "paper", "db": -19},
        {"t": T[31] + 0.1, "sfx": "phone_ring", "db": -17, "dur": T[32] - T[31] - 0.1},
        {"t": T[7] - 0.35, "sfx": "tapestop", "db": -20},
        {"t": T[32], "sfx": "tick", "db": -24, "dur": T[36] - T[32]}],
     "shots": S}
(here / "scene.json").write_text(json.dumps(D, ensure_ascii=False, indent=1), encoding="utf-8")
(here / "music_mute.txt").write_text(",".join(f"{a:.2f}-{b:.2f}" for a, b in D["music_mute"]), encoding="utf-8")
d = sorted(x["t1"] - x["t0"] for x in S)
print(f"{len(S)} shots, median {d[len(d)//2]:.2f}s, min {d[0]:.2f}s, {len(caps)} caption sets, end {END}")
