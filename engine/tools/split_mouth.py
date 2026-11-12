"""Split the mascot's mouth_open overlays into rig-safe sprites.

The source overlays also contain chin/neck/glasses fragments. Squashing them for in-between
visemes drags those lines into the face (dark mark under the mouth). This writes:
  mouth_patch_<pose>.png  feathered skin ellipse that hides the closed smile line (never scaled)
  mouth_shape_<pose>.png  only the open mouth (outline, teeth, tongue), safe to scale
and prints the mouth box to put in brand.json.

usage: python engine/tools/split_mouth.py brand/mascot
"""
import json, sys, pathlib
import numpy as np
from PIL import Image, ImageFilter

d = pathlib.Path(sys.argv[1])
out = {}
SMILE_Y = {"wave": 668, "thumbs": 672}  # closed-smile line centre in the base poses
for pose, src, base in [("wave", "mouth_open.png", "base_wave.png"), ("thumbs", "thumbs_mouth_open.png", "base_thumbs.png")]:
    ov = np.asarray(Image.open(d / src).convert("RGBA")).astype(np.float32)
    b = np.asarray(Image.open(d / base).convert("RGBA")).astype(np.float32)
    H, W = ov.shape[:2]
    yy, xx = np.mgrid[0:H, 0:W]
    # skin tone sampled from the base cheek under the mouth
    skin = np.median(b[690:705, 420:460, :3].reshape(-1, 3), axis=0)
    dist = np.linalg.norm(ov[..., :3] - skin, axis=-1)
    a = ov[..., 3] / 255
    mouthy = (dist > 45) & (a > 0.5)
    # mouth = largest dark/colored blob in the central band (excludes chin line below and glasses above)
    band = (yy > 615) & (yy < 728) & (xx > 330) & (xx < 560)
    m = mouthy & band
    ys, xs = np.nonzero(m)
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    cx, cy, rx, ry = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2 + 6, (y1 - y0) / 2 + 6
    ell = (((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2) <= 1
    shape_a = np.clip((dist - 20) / 35, 0, 1) * a * ell
    shape = ov.copy(); shape[..., 3] = shape_a * 255
    Image.fromarray(shape.astype(np.uint8)).save(d / f"mouth_shape_{pose}.png")
    # skin patch covering the closed smile line of the base pose
    pr = (((xx - cx) / (rx + 18)) ** 2 + ((yy - SMILE_Y[pose]) / 34) ** 2) <= 1
    patch = np.zeros_like(ov); patch[..., :3] = skin; patch[..., 3] = pr * 255
    pim = Image.fromarray(patch.astype(np.uint8)).filter(ImageFilter.GaussianBlur(5))
    pim.save(d / f"mouth_patch_{pose}.png")
    out[pose] = {"top": int(y0), "cx": round(float(cx), 1), "box": [int(x0), int(y0), int(x1), int(y1)]}
print(json.dumps(out))
