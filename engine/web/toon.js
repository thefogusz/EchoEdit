// Round-head flat 2D character rig for TYPE 3 (story) — drawn in code so every character stays identical in
// every shot and can blink, emote and move. Look studied from the user's ref (Paper Billions style: big round
// head, small coat body, stick legs, thin ink outline, warm rim light). Our own drawing, our CI colours.
// Deterministic: draw(g, spec, st) is a pure function of its inputs; the page passes t-derived state.
const TOON = (window.TOON = {});
const INK = '#1A1B1E';

TOON.ease = (k) => 1 - Math.pow(1 - Math.min(1, Math.max(0, k)), 3);

// blink: closed for 0.12 s every ~3.4 s, offset per character seed
TOON.blink = (t, seed = 0) => { const p = (t + seed * 1.37) % 3.4; return p < 0.12 ? 1 - Math.abs(p - 0.06) / 0.06 : 0; };

function rr(g, x, y, w, h, r) { g.beginPath(); g.roundRect(x, y, w, h, r); }
function fillStroke(g, fill, lw = 4) { g.fillStyle = fill; g.fill(); g.lineWidth = lw; g.strokeStyle = INK; g.stroke(); }

// arm as a soft bent stroke from the shoulder; a = angle from straight down (rad, + = towards facing side)
function arm(g, sx, sy, a, len, color, hand, dir) {
  const ex = sx + dir * Math.sin(a) * len, ey = sy + Math.cos(a) * len;
  const mx = sx + dir * Math.sin(a) * len * 0.5 + dir * 6, my = sy + Math.cos(a) * len * 0.5 + 4;
  g.lineCap = 'round';
  g.lineWidth = 26; g.strokeStyle = INK; g.beginPath(); g.moveTo(sx, sy); g.quadraticCurveTo(mx, my, ex, ey); g.stroke();
  g.lineWidth = 18; g.strokeStyle = color; g.beginPath(); g.moveTo(sx, sy); g.quadraticCurveTo(mx, my, ex, ey); g.stroke();
  g.beginPath(); g.arc(ex, ey, 12, 0, 7); fillStroke(g, hand, 3.5);
  return [ex, ey];
}

// pose -> arm angles [back, front] at time t
TOON.arms = function (pose, t) {  // [back(left), front(right)] angles from straight down; + = outward/up
  const s = Math.sin(t * 9), w = Math.sin(t * 7), id = 0.18 + 0.03 * Math.sin(t * 1.6);
  switch (pose) {
    case 'scrub': return [-0.45, -0.55 + 0.22 * s];          // hands together in front (sink, dishes)
    case 'wave': return [id, 2.7 + 0.25 * w];
    case 'point': return [id, 1.65];
    case 'hold': return [-0.55, -0.55];                       // holding something in front
    case 'write': return [-0.5, -0.62 + 0.08 * Math.sin(t * 14)];
    case 'shrug': return [1.05, 1.05];
    case 'cheer': return [2.6 + 0.1 * w, 2.6 - 0.1 * w];
    case 'think': return [id, -2.45];                         // hand to chin
    case 'head': return [2.8, 2.8];                           // hands on head (panic)
    default: return [id, 0.18 + 0.03 * Math.sin(t * 1.6 + 1)];
  }
};

function hair(g, h, R, back) {
  if (!h || h.style === 'none') return;
  g.fillStyle = h.color; g.strokeStyle = INK; g.lineWidth = 4;
  if (back) {  // parts drawn behind the head (bob)
    if (h.style === 'bob') { g.beginPath(); g.ellipse(0, 6, R * 1.12, R * 1.08, 0, Math.PI * 1.02, Math.PI * 1.98, true); g.fill(); g.stroke(); }
    return;
  }
  g.beginPath();
  if (h.style === 'short' || h.style === 'grey') {           // neat cap with a side part
    g.moveTo(-R * 0.98, -R * 0.1);
    g.bezierCurveTo(-R * 1.05, -R * 1.15, R * 1.05, -R * 1.2, R * 0.98, -R * 0.15);
    g.bezierCurveTo(R * 0.7, -R * 0.55, R * 0.1, -R * 0.62, -R * 0.25, -R * 0.42);
    g.bezierCurveTo(-R * 0.55, -R * 0.62, -R * 0.85, -R * 0.45, -R * 0.98, -R * 0.1);
  } else if (h.style === 'curly') {
    for (let i = 0; i < 7; i++) { const a = Math.PI * (1.05 + i * 0.15); g.moveTo(Math.cos(a) * R * 0.92 + 22, Math.sin(a) * R * 0.92); g.arc(Math.cos(a) * R * 0.92, Math.sin(a) * R * 0.92, 22, 0, 7); }
  } else if (h.style === 'bob') {
    g.moveTo(-R, 0); g.bezierCurveTo(-R * 1.05, -R * 1.25, R * 1.05, -R * 1.25, R, 0);
    g.bezierCurveTo(R * 0.6, -R * 0.55, -R * 0.3, -R * 0.75, -R, 0);
  } else if (h.style === 'bald') {
    g.moveTo(-R * 0.98, -R * 0.05); g.bezierCurveTo(-R * 1.06, -R * 0.45, -R * 0.8, -R * 0.55, -R * 0.75, -R * 0.4);
    g.lineTo(-R * 0.9, 0); g.moveTo(R * 0.98, -R * 0.05); g.bezierCurveTo(R * 1.06, -R * 0.45, R * 0.8, -R * 0.55, R * 0.75, -R * 0.4); g.lineTo(R * 0.9, 0);
  }
  g.fill(); g.stroke();
}

function face(g, spec, st, R) {
  const look = (st.look || 0) * 10, ex = 24, ey = -2;
  const blink = st.blink || 0, f = st.face || 'neutral';
  // eyes
  g.fillStyle = INK;
  for (const sx of [-1, 1]) {
    const x = sx * ex + look, h = (f === 'shock' ? 12 : 9.5) * (1 - 0.88 * blink);
    g.beginPath(); g.ellipse(x, ey, f === 'shock' ? 7.5 : 6.5, Math.max(1.2, h), 0, 0, 7); g.fill();
    if (f === 'tired') { g.lineWidth = 3; g.strokeStyle = 'rgba(26,27,30,.45)'; g.beginPath(); g.arc(x, ey + 10, 8, 0.2, Math.PI - 0.2); g.stroke(); }
  }
  // brows
  g.strokeStyle = INK; g.lineWidth = 4; g.lineCap = 'round';
  const bro = { worried: [0.35, 4], shock: [0, -8], grin: [0, -2], smile: [0, -1], angry: [-0.35, 3], tired: [0.12, 2], neutral: [0, 0], sad: [0.4, 3] }[f] || [0, 0];
  for (const sx of [-1, 1]) {
    const x = sx * ex + look, y = ey - 22 + bro[1];
    g.beginPath(); g.moveTo(x - 10, y + sx * bro[0] * 12 * -1); g.lineTo(x + 10, y + sx * bro[0] * 12); g.stroke();
  }
  // glasses
  if (spec.glasses === 'round' || spec.glasses === 'square') {
    g.lineWidth = 3.5; g.strokeStyle = INK;
    for (const sx of [-1, 1]) { const x = sx * ex + look * 0.6; g.beginPath(); if (spec.glasses === 'round') g.arc(x, ey, 17, 0, 7); else g.roundRect(x - 18, ey - 13, 36, 26, 7); g.stroke(); }
    g.beginPath(); g.moveTo(-ex + 17 + look * 0.6, ey); g.lineTo(ex - 17 + look * 0.6, ey); g.stroke();
  }
  const my = 30, mx = look * 0.5;
  // facial hair
  if (spec.beard) { g.fillStyle = spec.beard; g.beginPath(); g.moveTo(-R * 0.8, R * 0.25); g.quadraticCurveTo(0, R * 1.25, R * 0.8, R * 0.25);
    g.quadraticCurveTo(R * 0.4, R * 0.62, mx + 16, my + 14); g.lineTo(mx - 16, my + 14); g.quadraticCurveTo(-R * 0.4, R * 0.62, -R * 0.8, R * 0.25); g.fill(); g.lineWidth = 3; g.stroke(); }
  if (spec.mustache) { g.fillStyle = spec.mustache; g.beginPath(); g.ellipse(mx - 9, my - 9, 11, 5, 0.15, 0, 7); g.ellipse(mx + 9, my - 9, 11, 5, -0.15, 0, 7); g.fill(); }
  // mouth
  g.lineWidth = 4; g.strokeStyle = INK; g.fillStyle = '#7A2A22';
  g.beginPath();
  if (f === 'smile') { g.arc(mx, my - 10, 16, 0.25 * Math.PI, 0.75 * Math.PI); g.stroke(); }
  else if (f === 'grin') { g.moveTo(mx - 20, my - 4); g.quadraticCurveTo(mx, my + 26, mx + 20, my - 4); g.closePath(); g.fill(); g.stroke();
    g.fillStyle = '#fff'; g.beginPath(); g.moveTo(mx - 15, my - 2); g.lineTo(mx + 15, my - 2); g.lineTo(mx + 13, my + 4); g.lineTo(mx - 13, my + 4); g.fill(); }
  else if (f === 'shock') { g.ellipse(mx, my + 2, 9, 12, 0, 0, 7); g.fill(); g.stroke(); }
  else if (f === 'worried' || f === 'sad') { g.moveTo(mx - 13, my + 4); g.quadraticCurveTo(mx, my - 6, mx + 13, my + 4); g.stroke(); }
  else if (f === 'talk') { const o = st.mouth ?? 0.5; g.ellipse(mx, my, 11, 3 + 9 * o, 0, 0, 7); g.fill(); g.stroke(); }
  else { g.moveTo(mx - 10, my); g.lineTo(mx + 10, my); g.stroke(); }
}

// spec: {skin, hair:{style,color}, glasses, top:{color, kind:'tee'|'coat'|'apron'|'jacket', accent}, legs, shoes, beard, mustache, size}
// st: {x, y (feet), scale, face, look, blink, pose, t, dir (1 right / -1 left), bob, lean, rim:{color, side}, seated}
TOON.draw = function (g, spec, st) {
  const sc = (st.scale || 1) * (spec.size || 1), dir = st.dir || 1, t = st.t || 0;
  const R = 70, bob = st.bob ?? Math.sin(t * 2.2 + (spec.seed || 0)) * 2.2;
  g.save(); g.translate(st.x, st.y); g.scale(sc * dir, sc); g.rotate((st.lean || 0) * dir);
  const top = spec.top || { color: '#3B4A6B', kind: 'coat' }, skin = spec.skin || '#F2C9A0';
  // shadow
  if (!st.seated) { g.fillStyle = 'rgba(0,0,0,.28)'; g.beginPath(); g.ellipse(0, 2, 62, 11, 0, 0, 7); g.fill(); }
  // legs + shoes
  if (!st.seated) {
    const sw = st.walk ? Math.sin(t * 10) * 0.35 : 0;
    for (const [lx, a] of [[-20, sw], [20, -sw]]) {
      g.save(); g.translate(lx, -62); g.rotate(a);
      rr(g, -11, 0, 22, 58, 9); fillStroke(g, spec.legs || '#2B2F45', 3.5);
      g.beginPath(); g.ellipse(6, 58, 19, 9, 0, 0, 7); fillStroke(g, spec.shoes || INK, 3); g.restore();
    }
  }
  g.translate(0, bob);
  const [aB, aF] = TOON.arms(st.pose, t);
  const sleeve = top.kind === 'tee' || top.kind === 'apron' ? skin : top.color;
  // back arm (behind body)
  arm(g, -38, -150, aB, 76, sleeve === skin ? top.color : sleeve, skin, -1);
  // torso: rounded coat shape
  g.beginPath(); g.moveTo(-46, -168); g.quadraticCurveTo(-60, -110, -56, -62); g.lineTo(56, -62); g.quadraticCurveTo(60, -110, 46, -168);
  g.quadraticCurveTo(0, -182, -46, -168); fillStroke(g, top.color, 4);
  if (top.kind === 'apron') { rr(g, -34, -140, 68, 80, 10); fillStroke(g, top.accent || '#FFF8EC', 3); }
  if (top.kind === 'coat' || top.kind === 'jacket') { g.strokeStyle = INK; g.lineWidth = 3; g.beginPath(); g.moveTo(0, -172); g.lineTo(0, -64); g.stroke();
    g.fillStyle = top.accent || '#FFF8EC'; g.beginPath(); g.moveTo(-14, -174); g.lineTo(0, -146); g.lineTo(14, -174); g.closePath(); g.fill(); }
  if (top.kind === 'tee' && top.accent) { g.fillStyle = top.accent; g.beginPath(); g.arc(0, -120, 14, 0, 7); g.fill(); }
  // rim light on torso
  if (st.rim) { g.save(); g.globalCompositeOperation = 'source-atop'; g.restore(); }
  // head
  g.save(); g.translate(0, -238);
  hair(g, spec.hair, R, true);
  g.beginPath(); g.arc(0, 0, R, 0, 7); fillStroke(g, skin, 4.5);
  // soft shade + rim light (cinematic: lit from the lamp side)
  g.save(); g.beginPath(); g.arc(0, 0, R - 2, 0, 7); g.clip();
  const side = (st.rim?.side ?? 1) * dir;
  const sh = g.createLinearGradient(-R * side, 0, R * side, 0); sh.addColorStop(0, 'rgba(33,74,255,.16)'); sh.addColorStop(0.55, 'rgba(33,74,255,0)');
  g.fillStyle = sh; g.fillRect(-R, -R, 2 * R, 2 * R);
  if (st.rim) { g.strokeStyle = st.rim.color; g.globalAlpha = st.rim.a ?? 0.85; g.lineWidth = 10; g.beginPath(); g.arc(0, 0, R - 4, side > 0 ? -1.2 : Math.PI - 0.4, side > 0 ? 0.4 : Math.PI + 1.2); g.stroke(); }
  g.restore();
  hair(g, spec.hair, R, false);
  face(g, spec, st, R);
  g.restore();
  // front arm
  arm(g, 38, -150, aF, 76, sleeve === skin ? top.color : sleeve, skin, 1);
  g.restore();
};

// ---------- cast (studied from photos only for broad traits: hair, glasses, beard) ----------
TOON.cast = {
  jensen15: { skin: '#F1C79C', hair: { style: 'short', color: '#1E1E24' }, top: { color: '#FFF8EC', kind: 'apron', accent: '#FFFFFF' }, legs: '#2B2F45', size: 0.82, seed: 1 },
  jensen: { skin: '#F1C79C', hair: { style: 'short', color: '#1E1E24' }, glasses: 'square', top: { color: '#3A3F55', kind: 'coat', accent: '#9EE8FF' }, legs: '#22263A', seed: 1 },
  jensenNow: { skin: '#F1C79C', hair: { style: 'short', color: '#26262C' }, top: { color: '#1A1B1E', kind: 'jacket', accent: '#3A3F55' }, legs: '#1A1F33', seed: 1 },  // today: black leather jacket
  chris: { skin: '#F4CDA8', hair: { style: 'curly', color: '#6B4A2E' }, mustache: '#6B4A2E', top: { color: '#2E6B5E', kind: 'jacket', accent: '#FFF8EC' }, legs: '#2B2F45', seed: 2 },
  curtis: { skin: '#F4D2B0', hair: { style: 'bald', color: '#8A6A4A' }, glasses: 'round', beard: '#8A6A4A', top: { color: '#7A3B2E', kind: 'coat', accent: '#FFF8EC' }, legs: '#2B2F45', seed: 3 },
  sega: { skin: '#F1C9A0', hair: { style: 'grey', color: '#BFC4CC' }, glasses: 'square', top: { color: '#1E2A4A', kind: 'coat', accent: '#FFFFFF' }, legs: '#1A1F33', seed: 4 },
  staff: { skin: '#E9BE93', hair: { style: 'short', color: '#3A2A1E' }, top: { color: '#5A6378', kind: 'coat', accent: '#FFF8EC' }, legs: '#2B2F45', seed: 5 },
};
