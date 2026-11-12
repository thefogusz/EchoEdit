"""Track the speaker's face so reframing never cuts it. Writes [{t, cx, cy, h}] in source-normalised units (0..1).

usage: python engine/tools/face_track.py footage.mp4 out.json [--fps 10]
Uses OpenCV YuNet (engine/models/face_detection_yunet_2023mar.onnx), keeps the most confident face, fills misses by
interpolation and smooths with a 0.4 s moving average so the crop glides instead of jittering.
"""
import json, sys
import cv2
import numpy as np

src, out = sys.argv[1], sys.argv[2]
fps = float(sys.argv[sys.argv.index("--fps") + 1]) if "--fps" in sys.argv else 10.0
cap = cv2.VideoCapture(src)
vfps = cap.get(cv2.CAP_PROP_FPS) or 30
W, H = cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
import pathlib
model = str(pathlib.Path(__file__).resolve().parents[1] / "models" / "face_detection_yunet_2023mar.onnx")
det = cv2.FaceDetectorYN.create(model, "", (int(W), int(H)), 0.6, 0.3, 5000)
step = max(1, int(round(vfps / fps)))
ts, vals, i = [], [], 0
while True:
    ok, fr = cap.read()
    if not ok: break
    if i % step == 0:
        _, faces = det.detect(fr)
        ts.append(i / vfps)
        if faces is not None and len(faces):
            x, y, w, h = max(faces, key=lambda f: f[-1])[:4]
            vals.append([(x + w / 2) / W, (y + h / 2) / H, h / H])
        else:
            vals.append([np.nan] * 3)
    i += 1
a = np.array(vals, dtype=float)
hit = ~np.isnan(a[:, 0])
for c in range(3):  # fill misses
    a[:, c] = np.interp(np.arange(len(a)), np.nonzero(hit)[0], a[hit, c])
k = max(1, int(fps * 0.4)); ker = np.ones(k) / k
for c in range(3):
    a[:, c] = np.convolve(np.pad(a[:, c], (k // 2, k - 1 - k // 2), mode="edge"), ker, mode="valid")
json.dump([{"t": round(t, 3), "cx": round(r[0], 4), "cy": round(r[1], 4), "h": round(r[2], 4)} for t, r in zip(ts, a)], open(out, "w"))
print(f"{len(ts)} samples, faces found in {hit.mean() * 100:.0f}%, cy range {a[:, 1].min():.2f}-{a[:, 1].max():.2f}")
