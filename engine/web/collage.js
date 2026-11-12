// Editorial halftone paper-collage kit for TYPE 2 (news) only.
// Look: flat bold colour field, black-and-white halftone cut-outs, coloured cardstock, cream keylines,
// paper grain + soft shadow, assemble-from-empty motion (pieces fly in and build the picture).
// Method credit: pyang5166/gbro-collage-broll (MIT) style signature; motion numbers from cth9191/animate SPRING
// presets and lemo-opuscar caption-news (MIT). Deterministic: everything is a function of t.
const CL = (window.CL = {});

CL.cream = '#FFF8EC';

// halftone: grayscale -> black dots on cream paper (or transparent), computed once at setup
CL.halftone = function (img, { w, cell = 9, ink = '#111', paper = CL.cream, contrast = 1.25 } = {}) {
  const h = Math.round((img.naturalHeight || img.height) * (w / (img.naturalWidth || img.width)));
  const src = document.createElement('canvas'); src.width = w; src.height = h;
  const sg = src.getContext('2d'); sg.drawImage(img, 0, 0, w, h);
  const d = sg.getImageData(0, 0, w, h).data;
  const out = document.createElement('canvas'); out.width = w; out.height = h;
  const g = out.getContext('2d');
  if (paper) { g.fillStyle = paper; g.fillRect(0, 0, w, h); }
  g.fillStyle = ink;
  for (let y = 0; y < h; y += cell) for (let x = (y / cell) % 2 ? cell / 2 : 0; x < w; x += cell) {
    const i = (Math.min(h - 1, y | 0) * w + Math.min(w - 1, x | 0)) * 4;
    let lum = (0.299 * d[i] + 0.587 * d[i + 1] + 0.114 * d[i + 2]) / 255;
    lum = DE.clamp((lum - 0.5) * contrast + 0.5);
    const r = (1 - lum) * cell * 0.62;
    if (r > 0.4) { g.beginPath(); g.arc(x, y, r, 0, 7); g.fill(); }
  }
  return out.toDataURL('image/png');
};

// torn / cut paper edge as a CSS clip-path polygon (seeded, stable per piece)
CL.torn = function (seed, jag = 1.6, n = 18) {
  const r = DE.seeded(seed); const p = [];
  for (let i = 0; i <= n; i++) p.push(`${(i / n) * 100}% ${r() * jag}%`);
  for (let i = 0; i <= n; i++) p.push(`${100 - r() * jag}% ${(i / n) * 100}%`);
  for (let i = n; i >= 0; i--) p.push(`${(i / n) * 100}% ${100 - r() * jag}%`);
  for (let i = n; i >= 0; i--) p.push(`${r() * jag}% ${(i / n) * 100}%`);
  return `polygon(${p.join(',')})`;
};

// paper grain overlay (generated once)
CL.grain = function (w = 1080, h = 1920, seed = 5) {
  const c = document.createElement('canvas'); c.width = w / 2; c.height = h / 2;
  const g = c.getContext('2d'); const im = g.createImageData(c.width, c.height); const r = DE.seeded(seed);
  for (let i = 0; i < im.data.length; i += 4) { const v = 128 + (r() - 0.5) * 70; im.data[i] = im.data[i + 1] = im.data[i + 2] = v; im.data[i + 3] = 22; }
  g.putImageData(im, 0, 0); return c.toDataURL();
};

// closed-form damped spring 0->1 (animate kit "snappy"-like); dt seconds
CL.spring = (dt, k = 320, c = 30) => {
  if (dt <= 0) return 0;
  const w0 = Math.sqrt(k), z = c / (2 * w0);
  if (z < 1) { const wd = w0 * Math.sqrt(1 - z * z); return 1 - Math.exp(-z * w0 * dt) * (Math.cos(wd * dt) + (z * w0 / wd) * Math.sin(wd * dt)); }
  return 1 - Math.exp(-w0 * dt) * (1 + w0 * dt);
};

// entrance (user review 2026-11-12): pieces flying in from off-frame with spin + bounce were too fast and
// hard to focus on. Now: a short rise (~60 px) + fade, ease-out, no spin, no overshoot. Calm and readable.
CL.arrive = function (dt, from = 'bottom', dist = 60) {
  if (dt <= 0) return { x: 0, y: 0, r: 0, s: 1, o: 0 };
  const k = DE.ease.outCubic(DE.clamp(dt / 0.45));
  const d = Math.min(dist, 70);
  const v = { left: [-d, 0], right: [d, 0], top: [0, -d], bottom: [0, d], drop: [0, -d * 0.6] }[from] || [0, d];
  return { x: v[0] * (1 - k), y: v[1] * (1 - k), r: 0, s: from === 'drop' ? 1.04 - 0.04 * k : 1, o: DE.clamp(dt / 0.3) };
};

// count-up for numbers (motion-prompt #007 idea): fixed width digits, eases out
CL.count = (target, dt, dur = 0.7, dec = 0) => (target * (1 - Math.pow(1 - DE.clamp(dt / dur), 4))).toFixed(dec);
