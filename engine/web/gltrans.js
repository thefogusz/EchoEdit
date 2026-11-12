// WebGL host for gl-transitions shaders (engine/vendor/gl-transitions/selected.js, MIT).
// Standard gl-transitions contract: the shader defines `vec4 transition(vec2 uv)` and calls getFromColor/getToColor;
// the host supplies progress (0..1), ratio, and one uniform per parameter. uv origin is bottom-left.
// GLTRANS.render(name, fromCanvas, toCanvas, progress, params) -> a canvas with the blended frame.
// Motion blur (approved by the user, technique as in After Effects): GLTRANS.blurred(...) averages N sub-frames
// around `progress` (shutter = fraction of the transition the virtual shutter stays open).
const GLTRANS = (window.GLTRANS = {});
(function () {
  let cv, gl, buf, texFrom, texTo, progs = {};
  const VS = 'attribute vec2 p; varying vec2 uv; void main(){ uv = p * 0.5 + 0.5; gl_Position = vec4(p, 0.0, 1.0); }';
  function init(w, h) {
    cv = document.createElement('canvas'); cv.width = w; cv.height = h;
    gl = cv.getContext('webgl', { preserveDrawingBuffer: true, premultipliedAlpha: false });
    buf = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, buf);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, -1, 1, 1, -1, 1, 1]), gl.STATIC_DRAW);
    const mk = () => { const t = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D, t);
      for (const [k, v] of [[gl.TEXTURE_MIN_FILTER, gl.LINEAR], [gl.TEXTURE_MAG_FILTER, gl.LINEAR], [gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE], [gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE]]) gl.texParameteri(gl.TEXTURE_2D, k, v);
      return t; };
    texFrom = mk(); texTo = mk();
    gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, true);
  }
  function program(name) {
    if (progs[name]) return progs[name];
    const T = window.GLT[name];
    const FS = `precision highp float; varying vec2 uv; uniform sampler2D from, to; uniform float progress, ratio;
      vec4 getFromColor(vec2 u){ return texture2D(from, u); } vec4 getToColor(vec2 u){ return texture2D(to, u); }
      ${T.glsl}
      void main(){ gl_FragColor = transition(uv); }`;
    const sh = (type, src) => { const s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s);
      if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error(name + ': ' + gl.getShaderInfoLog(s)); return s; };
    const p = gl.createProgram(); gl.attachShader(p, sh(gl.VERTEX_SHADER, VS)); gl.attachShader(p, sh(gl.FRAGMENT_SHADER, FS)); gl.linkProgram(p);
    progs[name] = p; return p;
  }
  GLTRANS.render = function (name, from, to, progress, params = {}) {
    if (!gl) init(from.width, from.height);
    const p = program(name); gl.useProgram(p); gl.viewport(0, 0, cv.width, cv.height);
    gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, texFrom); gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, from);
    gl.activeTexture(gl.TEXTURE1); gl.bindTexture(gl.TEXTURE_2D, texTo); gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, to);
    gl.uniform1i(gl.getUniformLocation(p, 'from'), 0); gl.uniform1i(gl.getUniformLocation(p, 'to'), 1);
    gl.uniform1f(gl.getUniformLocation(p, 'progress'), progress); gl.uniform1f(gl.getUniformLocation(p, 'ratio'), cv.width / cv.height);
    const T = window.GLT[name], P = Object.assign({}, T.defaults, params);
    for (const [k, typ] of Object.entries(T.types)) {
      const loc = gl.getUniformLocation(p, k), v = P[k];
      if (typ === 'float') gl.uniform1f(loc, v); else if (typ === 'vec2') gl.uniform2fv(loc, v); else if (typ === 'vec3') gl.uniform3fv(loc, v);
      else if (typ === 'int' || typ === 'bool') gl.uniform1i(loc, +v);
    }
    const a = gl.getAttribLocation(p, 'p'); gl.bindBuffer(gl.ARRAY_BUFFER, buf); gl.enableVertexAttribArray(a); gl.vertexAttribPointer(a, 2, gl.FLOAT, false, 0, 0);
    gl.drawArrays(gl.TRIANGLES, 0, 6);
    return cv;
  };
  // averaged sub-frames = real motion blur along the move (no ghost copies: samples are dense and evenly weighted)
  let acc = null;
  GLTRANS.blurred = function (name, getFrom, getTo, progress, params, { samples = 12, shutter = 0.35, ease = (x) => x } = {}) {
    const w = getFrom(progress).width, h = getFrom(progress).height;
    if (!acc) { acc = document.createElement('canvas'); acc.width = w; acc.height = h; }
    const g = acc.getContext('2d'); g.globalCompositeOperation = 'source-over'; g.globalAlpha = 1; g.clearRect(0, 0, w, h);
    for (let i = 0; i < samples; i++) {
      const pr = Math.min(1, Math.max(0, progress + (i / (samples - 1) - 0.5) * shutter));
      const c = GLTRANS.render(name, getFrom(pr), getTo(pr), ease(pr), params);
      g.globalAlpha = 1 / (i + 1); g.drawImage(c, 0, 0);   // running mean
    }
    g.globalAlpha = 1; return acc;
  };
})();
