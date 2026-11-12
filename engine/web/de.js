// DataEchooo render kit: brand tokens, easing, Thai captions, 2.5D mascot rig.
// Contract with engine/render.py: a page defines window.setup(data) (async) and window.renderAt(t) (sync or async).
// Everything here is deterministic in t: no Date.now(), no Math.random() without a seed.

const DE = (window.DE = {});

DE.color = {
  blue: '#214AFF', blueDark: '#0B1B66', ice: '#F3F7FF', sky: '#9EE8FF', teal: '#00C2BB',
  orange: '#FE4C1C', slate: '#A5B7D2', ink: '#1A1B1E', text: '#363636', white: '#FFFFFF',
};

DE.injectFonts = async function (base) {
  const css = `
  @font-face{font-family:Kanit;font-weight:700;src:url(${base}/fonts/Kanit-Bold.ttf)}
  @font-face{font-family:Kanit;font-weight:900;src:url(${base}/fonts/Kanit-Black.ttf)}
  @font-face{font-family:Kanit;font-weight:800;font-style:italic;src:url(${base}/fonts/Kanit-ExtraBoldItalic.ttf)}
  @font-face{font-family:'IBM Plex Sans Thai';font-weight:400;src:url(${base}/fonts/IBMPlexSansThai-Regular.ttf)}
  @font-face{font-family:'IBM Plex Sans Thai';font-weight:700;src:url(${base}/fonts/IBMPlexSansThai-Bold.ttf)}
  @font-face{font-family:'Red Hat Display';font-weight:300 900;src:url(${base}/fonts/RedHatDisplay-Var.ttf)}`;
  const s = document.createElement('style'); s.textContent = css; document.head.appendChild(s);
  const probes = ['900 40px Kanit', '700 40px Kanit', 'italic 800 40px Kanit', '700 40px "IBM Plex Sans Thai"', '400 40px "IBM Plex Sans Thai"', '800 40px "Red Hat Display"'];
  await Promise.all(probes.map((p) => document.fonts.load(p, 'กขคAa')));
  await document.fonts.ready;
};

DE.loadImage = (src) => new Promise((ok, bad) => { const i = new Image(); i.onload = () => ok(i); i.onerror = () => bad(new Error('image ' + src)); i.src = src; });

// ---------- easing / springs ----------
DE.clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
DE.lerp = (a, b, k) => a + (b - a) * k;
DE.ease = {
  outCubic: (k) => 1 - Math.pow(1 - k, 3),
  inOutCubic: (k) => (k < 0.5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2),
  outBack: (k, s = 1.7) => 1 + (s + 1) * Math.pow(k - 1, 3) + s * Math.pow(k - 1, 2),
};
// Damped spring from 0 to 1, dt seconds since trigger. Overshoots ~12% with defaults.
DE.spring = (dt, freq = 9, damp = 0.55) => (dt <= 0 ? 0 : 1 - Math.exp(-damp * freq * dt) * Math.cos(freq * Math.sqrt(1 - damp * damp) * dt));
DE.seeded = (seed) => () => ((seed = (seed * 1664525 + 1013904223) >>> 0) / 4294967296);

// ---------- Thai captions ----------
// chunks: [{start,end,words:[{text,start,end,hl}]}]  (built by engine/captions.py)
// style: {y, size, mode:'pop'|'band', band:{...}}
DE.Captions = class {
  constructor(root, chunks, style = {}) {
    this.chunks = chunks;
    this.st = Object.assign({ y: 1180, size: 92, maxWidth: 900, mode: 'pop' }, style);
    this.el = document.createElement('div');
    this.el.className = 'de-cap';
    Object.assign(this.el.style, {
      position: 'absolute', left: '0', width: '1080px', top: this.st.y + 'px', display: 'flex',
      justifyContent: 'center', pointerEvents: 'none', zIndex: 50,
    });
    root.appendChild(this.el);
    this.cur = -1;
  }
  renderAt(t) {
    const i = this.chunks.findIndex((c) => t >= c.start && t < c.end);
    if (i !== this.cur) { this.cur = i; this.build(i); }
    if (i < 0) return;
    const c = this.chunks[i];
    // gentle: fade + 4 % settle (the springy 0.6->1 pop competed with the visuals)
    const k = DE.ease.outCubic(DE.clamp((t - c.start) / 0.22));
    const box = this.el.firstChild;
    box.style.transform = `translateY(-50%) scale(${0.96 + 0.04 * k})`;
    box.style.opacity = k;
    // Thai audiences expect the whole phrase at once ("set" reveal, default). 'word' = karaoke reveal, opt-in only.
    if (this.st.reveal === 'word') c.words.forEach((w, j) => {
      const span = box.children[j];
      const on = t >= w.start;
      span.style.opacity = on ? 1 : 0.0;
      if (w.hl) span.style.transform = on ? `scale(${1 + 0.15 * (1 - DE.clamp((t - w.start) / 0.25))})` : 'scale(1)';
    });
  }
  build(i) {
    this.el.innerHTML = '';
    if (i < 0) return;
    const s = this.st, band = s.mode === 'band';
    const box = document.createElement('div');
    Object.assign(box.style, {
      maxWidth: s.maxWidth + 'px', textAlign: 'center', lineHeight: '1.45', padding: band ? (s.bandPad || '18px 40px 22px') : '0 20px',
      font: `900 ${s.size}px Kanit, "IBM Plex Sans Thai", sans-serif`, color: band ? DE.color.ink : '#fff',
      background: band ? 'rgba(255,255,255,0.97)' : 'none', borderRadius: band ? '28px' : '0',
      boxShadow: band ? `0 10px 0 ${DE.color.blue}, 0 18px 40px rgba(0,0,0,.25)` : 'none',
      transformOrigin: '50% 50%', wordBreak: 'keep-all', overflowWrap: 'normal',
      minWidth: band ? (s.bandMinWidth || 0) + 'px' : '0',
    });
    for (const w of this.chunks[i].words) {
      const sp = document.createElement('span');
      sp.textContent = w.text;
      sp.style.display = 'inline-block';
      sp.style.transition = 'none';
      if (!band) {
        sp.style.webkitTextStroke = '14px ' + DE.color.ink;
        sp.style.paintOrder = 'stroke fill';
        sp.style.textShadow = '0 8px 0 rgba(0,0,0,.35)';
      }
      if (w.hl) {
        sp.style.color = band ? DE.color.blue : DE.color.sky;
        // never slant Thai: Thai fonts have no italic and the browser fakes it. Italic only for Latin words.
        if (w.hl === 'italic' && !/[฀-๿]/.test(w.text)) { sp.style.fontStyle = 'italic'; sp.style.fontWeight = 800; }
      }
      if (w.space) sp.style.marginLeft = '0.25em';
      box.appendChild(sp);
    }
    this.el.appendChild(box);
  }
};

// ---------- 2.5D mascot rig ----------
// Layers: shadow -> body (base pose) -> mouth overlay (scaled by viseme) -> blink overlay.
// opts: {x,y,scale, env:[0..1 per frame], fps, poses:[{t,pose}], emotes:[{t,type}] , seed}
DE.Mascot = class {
  constructor(canvas, imgs, opts) {
    this.c = canvas; this.g = canvas.getContext('2d'); this.img = imgs; this.o = Object.assign({ fps: 30, seed: 7, x: 820, y: 2000, scale: 0.55, anchor: 'edge' }, opts);
    // deterministic blink schedule
    const r = DE.seeded(this.o.seed); this.blinks = []; let b = 1.2;
    while (b < 600) { this.blinks.push(b); b += 2.2 + r() * 3.2; }
  }
  poseAt(t) { let p = this.o.poses?.[0]?.pose || 'wave', since = -9; for (const q of this.o.poses || []) if (t >= q.t) { p = q.pose; since = q.t; } return [p, t - since]; }
  envAt(t) { const e = this.o.env || []; const f = t * this.o.fps; const i = Math.floor(f); const a = e[i] || 0, b = e[i + 1] || 0; return a + (b - a) * (f - i); }
  emoteAt(t) { let best = null; for (const q of this.o.emotes || []) if (t >= q.t && t - q.t < 0.8) best = { type: q.type, dt: t - q.t }; return best; }
  renderAt(t) {
    const { g, c, img, o } = this;
    g.clearRect(0, 0, c.width, c.height);
    const [pose, since] = this.poseAt(t);
    const base = img[pose] || img.wave;
    const env = this.envAt(t);
    // drawn-on-twos mouth: sample envelope at 15 fps for a hand-animated feel
    const envStep = this.envAt(Math.floor(t * 15) / 15);
    const open = envStep < 0.08 ? 0 : envStep < 0.3 ? 0.4 : envStep < 0.6 ? 0.7 : 1.0;
    // idle breathing + talk bob + pose pop + emotes
    const breathe = Math.sin(t * 2 * Math.PI * 0.35);
    const pop = since < 0.5 ? 1 - DE.spring(since, 12, 0.45) : 0; // 1 -> 0 with overshoot
    const em = this.emoteAt(t);
    let hop = 0, tilt = Math.sin(t * 1.3) * 0.025 + env * 0.03 * Math.sin(t * 9);
    if (em && em.type === 'hop') hop = Math.sin(Math.min(1, em.dt / 0.45) * Math.PI) * 60;
    if (em && em.type === 'shake') tilt += Math.sin(em.dt * 40) * 0.06 * (1 - em.dt / 0.8);
    const sy = 1 + breathe * 0.012 + pop * 0.12 + env * 0.015;
    const sx = 1 - breathe * 0.008 - pop * 0.08;
    // position: optional moves [{t,x,y,scale}] eased over 0.45 s (corner narrator <-> centre host)
    let X = o.x, Y = o.y, S = o.scale;
    for (const mv of o.moves || []) {
      if (t < mv.t) break;
      const k = DE.ease.inOutCubic(DE.clamp((t - mv.t) / 0.45));
      X = DE.lerp(X, mv.x, k); Y = DE.lerp(Y, mv.y, k); S = DE.lerp(S, mv.scale, k);
    }
    const W = 900 * S, H = 1355 * S;
    // ground shadow (2.5D depth cue)
    // edge-anchored (default): the cut-off bust sits below the frame edge, so no floor shadow and hops never lift it into view
    if (o.anchor === 'floor') { g.save(); g.translate(X, Y); g.scale(1 - hop / 400, 1);
    g.fillStyle = 'rgba(11,27,102,0.28)'; g.filter = 'blur(10px)';
    g.beginPath(); g.ellipse(0, 6, W * 0.36, W * 0.07, 0, 0, Math.PI * 2); g.fill(); g.restore(); }
    else hop = Math.min(hop, Math.max(0, Y - 1920 - 4));
    g.save();
    g.translate(X, Y - hop); g.rotate(tilt); g.scale(sx, sy); g.translate(-W / 2, -H);
    // rim light: draw a sky-tinted silhouette slightly offset behind the body
    if (o.rim !== false) {
      g.save(); g.filter = 'blur(3px) brightness(0) invert(1) sepia(1) hue-rotate(160deg) saturate(4)'; g.globalAlpha = 0.55;
      g.drawImage(base, -8 * S * 2, -6 * S * 2, W, H); g.restore();
    }
    g.drawImage(base, 0, 0, W, H);
    if (open > 0) {
      // skin patch hides the closed smile (never scaled), then only the mouth shape is squashed from its top edge
      const th = pose === 'thumbs';
      g.drawImage(th ? img.patchThumbs : img.patchWave, 0, 0, W, H);
      const ay = (th ? 626 : 625) * S;
      g.save(); g.translate(0, ay); g.scale(1, 0.3 + 0.7 * open); g.translate(0, -ay);
      g.drawImage(th ? img.mouthThumbs : img.mouthWave, 0, 0, W, H); g.restore();
    }
    const blink = this.blinks.some((b) => t >= b && t < b + 0.1) || (em && em.type === 'happy');
    if (blink) g.drawImage(img.eyes, 0, 0, W, H);
    g.restore();
  }
};

DE.loadMascot = async function (base) {
  const m = base + '/mascot/';
  const names = ['base_wave', 'base_thumbs', 'mouth_shape_wave', 'mouth_shape_thumbs', 'mouth_patch_wave', 'mouth_patch_thumbs', 'eyes_closed'];
  const [wave, thumbs, mouthWave, mouthThumbs, patchWave, patchThumbs, eyes] = await Promise.all(names.map((n) => DE.loadImage(m + n + '.png')));
  return { wave, thumbs, mouthWave, mouthThumbs, patchWave, patchThumbs, eyes };
};

// ---------- brand ripple wipe (the "ooo" arcs) ----------
// progress 0..1 ; draws 3 expanding arcs from the right edge that cover the frame, then clear.
DE.rippleWipe = function (g, p, w = 1080, h = 1920) {
  if (p <= 0 || p >= 1) return;
  const cols = [DE.color.sky, DE.color.blue, DE.color.blueDark];
  const R = Math.hypot(w, h) * 1.05;
  cols.forEach((col, i) => {
    const k = DE.clamp((p * 1.6 - i * 0.18));
    const out = DE.clamp((p - 0.55) * 2.2 - i * 0.08);
    if (k <= 0) return;
    g.save(); g.beginPath();
    g.arc(w + 80, h * 0.5, R * DE.ease.inOutCubic(k), 0, Math.PI * 2);
    if (out > 0) g.arc(w + 80, h * 0.5, R * DE.ease.inOutCubic(out), 0, Math.PI * 2, true);
    g.fillStyle = col; g.fill(); g.restore();
  });
};
