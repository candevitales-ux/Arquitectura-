// Mini librería para modelar detalles constructivos en 3D (mm reales).
// x+ hacia el interior, y+ arriba, z+ hacia el observador (plano de corte z = 0).
import * as THREE from 'three';
import { LineSegments2 } from 'three/addons/lines/LineSegments2.js';
import { LineSegmentsGeometry } from 'three/addons/lines/LineSegmentsGeometry.js';
import { LineMaterial } from 'three/addons/lines/LineMaterial.js';

// ---------------------------------------------------------- texturas de rayado
function hatchCanvas(kind, bg) {
  const c = document.createElement('canvas'); c.width = c.height = 128;
  const g = c.getContext('2d'); g.fillStyle = bg; g.fillRect(0, 0, 128, 128);
  g.strokeStyle = '#3d4247'; g.fillStyle = '#3d4247'; g.lineWidth = 2.2;
  const diag = (n) => { for (let i = -128; i < 256; i += 128 / n) { g.beginPath(); g.moveTo(i, 128); g.lineTo(i + 128, 0); g.stroke(); } };
  const dots = (n, r, seed = 1) => { let s = seed; const rnd = () => (s = (s * 9301 + 49297) % 233280) / 233280;
    for (let i = 0; i < n; i++) { g.beginPath(); g.arc(rnd() * 128, rnd() * 128, r * (0.6 + rnd() * 0.7), 0, 7); g.fill(); } };
  const tris = (n, seed = 3) => { let s = seed; const rnd = () => (s = (s * 9301 + 49297) % 233280) / 233280; g.lineWidth = 1.6;
    for (let i = 0; i < n; i++) { const x = rnd() * 118 + 5, y = rnd() * 118 + 5, k = 5 + rnd() * 4; g.beginPath(); g.moveTo(x, y - k); g.lineTo(x + k, y + k * .7); g.lineTo(x - k, y + k * .7); g.closePath(); g.stroke(); } };
  switch (kind) {
    case 'ha': diag(4); break;
    case 'hais': diag(3); dots(14, 2.6); break;
    case 'h': dots(22, 2.4); tris(7); break;
    case 'mort': dots(70, 1.6, 7); break;
    case 'grout': dots(160, 1.8, 5); break;
    case 'tosca': g.fillStyle = '#8f7a50'; dots(70, 2.6, 11); break;
    case 'tierra': g.strokeStyle = '#7d6644'; g.lineWidth = 2; for (const [x, y] of [[10, 30], [70, 20], [40, 90], [95, 80], [5, 120]]) for (let k = 0; k < 3; k++) { g.beginPath(); g.moveTo(x + k * 7, y + 12); g.lineTo(x + k * 7 + 14, y - 2); g.stroke(); } break;
    case 'eps': g.strokeStyle = '#9c8414'; g.lineWidth = 2; for (let y = 16; y < 128; y += 32) { g.beginPath(); for (let x = 0; x <= 128; x += 16) g.lineTo(x, y + ((x / 16) % 2 ? -10 : 10)); g.stroke(); } break;
    case 'lana': g.strokeStyle = '#a5701a'; g.lineWidth = 2; for (let y = 16; y < 128; y += 32) { g.beginPath(); for (let x = 0; x <= 128; x += 4) g.lineTo(x, y + 10 * Math.sin(x / 128 * Math.PI * 4)); g.stroke(); } break;
    default: break;
  }
  return c;
}
const texCache = {};
function hatchTex(kind, bg, period) {
  const key = kind + bg + period; if (texCache[key]) return texCache[key];
  const cv = hatchCanvas(kind, bg);
  if (globalThis.LINE_ONLY || globalThis.GRAY) {   // rayados en escala de grises
    const g = cv.getContext('2d'), im = g.getImageData(0, 0, cv.width, cv.height), d = im.data;
    for (let i = 0; i < d.length; i += 4) { const y = 0.3 * d[i] + 0.59 * d[i + 1] + 0.11 * d[i + 2]; const v = globalThis.GRAY ? y : (y > 200 ? 255 : Math.min(y, 90)); d[i] = d[i + 1] = d[i + 2] = v; }
    g.putImageData(im, 0, 0);
  }
  const t = new THREE.CanvasTexture(cv); t.wrapS = t.wrapT = THREE.RepeatWrapping;
  t.repeat.set(1 / period, 1 / period); t.anisotropy = 8; t.colorSpace = THREE.SRGBColorSpace;
  return (texCache[key] = t);
}

export const MAT = {
  pre: { color: '#c3c9cf', hatch: 'ha', bg: '#d5d9dd', period: 90 },
  insitu: { color: '#d3ccbd', hatch: 'hais', bg: '#ddd7cb', period: 110 },
  hs: { color: '#dedad1', hatch: 'h', bg: '#e6e3dc', period: 120 },
  mort: { color: '#e4e4e2', hatch: 'mort', bg: '#e8e8e6', period: 70 },
  hid: { color: '#bcd3e1', hatch: 'mort', bg: '#c6dbe7', period: 70 },
  grout: { color: '#aeb0b2', hatch: 'grout', bg: '#bdbfc1', period: 70 },
  eps: { color: '#fff0a0', hatch: 'eps', bg: '#fff3b4', period: 60 },
  lana: { color: '#f5d07e', hatch: 'lana', bg: '#f8dc9a', period: 60 },
  tosca: { color: '#e6d6ad', hatch: 'tosca', bg: '#ecdfbd', period: 110 },
  tierra: { color: '#d6c6a4', hatch: 'tierra', bg: '#e0d3b6', period: 200 },
  glass: { color: '#8fd0e8', glass: true },
  spandrel: { color: '#56707f' },
  alu: { color: '#a3abb3' },
  alu2: { color: '#c9d0d6' },
  steel: { color: '#5d6369' },
  galv: { color: '#a0a7ae' },
  neo: { color: '#1d1d1d' },
  memb: { color: '#3a3a3a' },
  porc: { color: '#d2bc9c' },
  yeso: { color: '#f5f5f3' },
  film: { color: '#2f6f96' },
  red: { color: '#a8321e' },
  seal: { color: '#262626' },
  intum: { color: '#c0392b' },
};
const matCache = {};
function materials(key) {
  if (matCache[key]) return matCache[key];
  const m = MAT[key];
  const base = { polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1 };
  let side, cap;
  if (globalThis.LINE_ONLY) {   // solo línea: caras blancas sin sombreado; rayado gris solo en caras cortadas
    if (m.glass) side = new THREE.MeshBasicMaterial({ ...base, color: '#ffffff', transparent: true, opacity: 0, depthWrite: false, side: THREE.DoubleSide });
    else side = new THREE.MeshBasicMaterial({ ...base, color: key === 'red' ? '#ffffff' : '#ffffff' });
    cap = (m.hatch && !m.glass) ? new THREE.MeshBasicMaterial({ ...base, map: hatchTex(m.hatch, '#ffffff', m.period) }) : side;
    return (matCache[key] = [cap, side]);
  }
  if (m.glass) {
    side = new THREE.MeshLambertMaterial({ ...base, color: m.color, transparent: true, opacity: 0.38, depthWrite: false, side: THREE.DoubleSide });
    cap = side;
  } else {
    side = new THREE.MeshLambertMaterial({ ...base, color: m.color });
    cap = m.hatch ? new THREE.MeshLambertMaterial({ ...base, map: hatchTex(m.hatch, m.bg, m.period) }) : side;
  }
  return (matCache[key] = [cap, side]);
}

// ---------------------------------------------------------- escena
export class Scene3D {
  constructor() {
    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color('#ffffff');
    this.scene.add(new THREE.AmbientLight('#ffffff', 1.55));
    const d1 = new THREE.DirectionalLight('#ffffff', 1.25); d1.position.set(0.55, 1.0, 0.75); this.scene.add(d1);
    const d2 = new THREE.DirectionalLight('#ffffff', 0.35); d2.position.set(-0.6, 0.2, 0.9); this.scene.add(d2);
    this.edges = []; this.bbox = new THREE.Box3(); this.anchors = [];
  }
  _add(geom, key, edgeAngle = 20, edges = true) {
    const mesh = new THREE.Mesh(geom, materials(key));
    (this.meshes ||= []).push({ key, geom, mesh });
    if (MAT[key].glass) mesh.renderOrder = 10;
    this.scene.add(mesh);
    geom.computeBoundingBox(); this.bbox.union(geom.boundingBox);
    if (edges) {
      const e = new THREE.EdgesGeometry(geom, edgeAngle);
      this.edges.push({ pos: e.attributes.position.array, w: MAT[key].glass ? 0.6 : 1 });
    }
    return mesh;
  }
  // prisma: perfil 2D (u,v) extruido según eje.
  //  'z': (x=u, y=v, z=w)   'x': (x=w, y=v, z=-u)   'y': (x=u, y=w, z=-v)
  prism(pts, axis, w0, w1, key, holes = [], opt = {}) {
    if (w1 < w0) [w0, w1] = [w1, w0];
    const sh = new THREE.Shape(pts.map(p => new THREE.Vector2(p[0], p[1])));
    for (const h of holes) {
      const p = new THREE.Path();
      if (h.circle) p.absarc(h.circle[0], h.circle[1], h.circle[2], 0, Math.PI * 2, true);
      else { p.moveTo(...h[0]); for (const q of h.slice(1)) p.lineTo(...q); }
      sh.holes.push(p);
    }
    const g = new THREE.ExtrudeGeometry(sh, { depth: w1 - w0, bevelEnabled: false, curveSegments: 28 });
    g.translate(0, 0, w0);
    const M = new THREE.Matrix4();
    if (axis === 'x') M.set(0, 0, 1, 0, 0, 1, 0, 0, -1, 0, 0, 0, 0, 0, 0, 1);
    if (axis === 'y') M.set(1, 0, 0, 0, 0, 0, 1, 0, 0, -1, 0, 0, 0, 0, 0, 1);
    if (axis !== 'z') g.applyMatrix4(M);
    return this._add(g, key, opt.edgeAngle ?? 20, opt.edges ?? true);
  }
  box(x0, x1, y0, y1, z0, z1, key, opt = {}) {  // extruido en z (tapas = caras z, rayadas)
    const ax = opt.axis || 'z';
    const za = Math.min(z0, z1), zb = Math.max(z0, z1);
    if (ax === 'z') return this.prism([[x0, y0], [x1, y0], [x1, y1], [x0, y1]], 'z', za, zb, key, [], opt);
    if (ax === 'x') return this.prism([[-zb, y0], [-za, y0], [-za, y1], [-zb, y1]], 'x', x0, x1, key, [], opt);
    if (ax === 'y') return this.prism([[x0, -zb], [x1, -zb], [x1, -za], [x0, -za]], 'y', y0, y1, key, [], opt);
  }
  cyl(axis, c1, c2, r, w0, w1, key, seg = 28) {   // c1,c2: coordenadas del centro en el plano normal
    const g = new THREE.CylinderGeometry(r, r, Math.abs(w1 - w0), seg);
    const m = (w0 + w1) / 2;
    if (axis === 'y') g.translate(c1, m, c2);
    if (axis === 'x') { g.rotateZ(Math.PI / 2); g.translate(m, c1, c2); }
    if (axis === 'z') { g.rotateX(Math.PI / 2); g.translate(c1, c2, m); }
    return this._add(g, key, 35);
  }
  // chapa plegada: polilínea (u,v) con espesor t, extruida
  sheet(pts, t, axis, w0, w1, key) {
    for (let i = 0; i < pts.length - 1; i++) {
      const [a, b] = [pts[i], pts[i + 1]]; const dx = b[0] - a[0], dy = b[1] - a[1], L = Math.hypot(dx, dy);
      const nx = -dy / L * t / 2, ny = dx / L * t / 2;
      const ex = dx / L * t / 2, ey = dy / L * t / 2;
      this.prism([[a[0] + nx - ex, a[1] + ny - ey], [b[0] + nx + ex, b[1] + ny + ey], [b[0] - nx + ex, b[1] - ny + ey], [a[0] - nx - ex, a[1] - ny - ey]], axis, w0, w1, key, [], { edgeAngle: 40 });
    }
  }
  // exporta geometría (vértices soldados + caras) para CAD
  exportData() {
    const out = [];
    for (const { key, geom } of this.meshes) {
      const pos = geom.attributes.position.array, idx = geom.index ? geom.index.array : null;
      const map = new Map(), V = [], F = [];
      const vid = (i) => { const x = pos[3 * i], y = pos[3 * i + 1], z = pos[3 * i + 2];
        const k = `${x.toFixed(1)},${y.toFixed(1)},${z.toFixed(1)}`; let v = map.get(k);
        if (v === undefined) { v = V.length; map.set(k, v); V.push([+x.toFixed(1), +y.toFixed(1), +z.toFixed(1)]); } return v; };
      const n = idx ? idx.length : pos.length / 3;
      for (let t = 0; t < n; t += 3) {
        const a = vid(idx ? idx[t] : t), b = vid(idx ? idx[t + 1] : t + 1), c = vid(idx ? idx[t + 2] : t + 2);
        if (a !== b && b !== c && a !== c) F.push([a, b, c]);
      }
      out.push({ key, color: MAT[key].color, V, F });
    }
    return { meshes: out, anchors: this.anchors.map(a => ({ n: a.n, p: [a.p.x, a.p.y, a.p.z] })) };
  }
  anchor(n, x, y, z) { this.anchors.push({ n, p: new THREE.Vector3(x, y, z) }); }

  // render a imagen; devuelve dataURL y posiciones de anclas en [0..1]
  // perspectiva cónica simétrica: cámara sobre el plano de simetría z = zc, mirando al centro
  renderPersp(Wpx, Hpx, dir, fov = 28, frac = 0.8, lineW = 2.6, shiftY = 0) {
    const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
    renderer.setPixelRatio(1); renderer.setSize(Wpx, Hpx);
    const target = this.bbox.getCenter(new THREE.Vector3());
    const d = new THREE.Vector3(...dir).normalize();
    const cam = new THREE.PerspectiveCamera(fov, Wpx / Hpx, 5, 1e6);
    const corners = []; const b = this.bbox;
    for (const x of [b.min.x, b.max.x]) for (const y of [b.min.y, b.max.y]) for (const z of [b.min.z, b.max.z]) corners.push(new THREE.Vector3(x, y, z));
    let dist = b.getSize(new THREE.Vector3()).length() * 1.6, cy = 0;
    for (let it = 0; it < 12; it++) {
      cam.position.copy(target).addScaledVector(d, dist); cam.up.set(0, 1, 0); cam.lookAt(target);
      cam.updateMatrixWorld(); cam.updateProjectionMatrix();
      let mx = 0, mny = 1e9, mxy = -1e9;
      for (const c of corners) { const v = c.clone().project(cam); mx = Math.max(mx, Math.abs(v.x)); mny = Math.min(mny, v.y); mxy = Math.max(mxy, v.y); }
      const ext = Math.max(mx, (mxy - mny) / 2);
      cy = (mxy + mny) / 2;
      dist *= Math.pow(ext / frac, 0.9);
      // recentrar en vertical
      const up = new THREE.Vector3(0, 1, 0).applyQuaternion(cam.quaternion);
      target.addScaledVector(up, cy * 0.5 * dist * Math.tan(fov * Math.PI / 360) * 0.9);
    }
    const up = new THREE.Vector3(0, 1, 0).applyQuaternion(cam.quaternion);
    target.addScaledVector(up, -shiftY * dist * Math.tan(fov * Math.PI / 360));
    cam.position.copy(target).addScaledVector(d, dist); cam.lookAt(target); cam.updateMatrixWorld();
    for (const e of this.edges) {
      const g = new LineSegmentsGeometry(); g.setPositions(e.pos);
      const m = new LineMaterial({ color: '#111111', linewidth: lineW * e.w, resolution: new THREE.Vector2(Wpx, Hpx) });
      const l = new LineSegments2(g, m); l.renderOrder = 20; this.scene.add(l);
    }
    renderer.render(this.scene, cam);
    const url = renderer.domElement.toDataURL('image/png');
    const anchors = this.anchors.map(a => { const v = a.p.clone().project(cam); return { n: a.n, x: (v.x + 1) / 2, y: (1 - v.y) / 2 }; });
    renderer.dispose();
    return { url, anchors, scale: 0 };
  }
  // ---------- vectorización 2D (para DWG): caras ordenadas (pintor) + aristas visibles (z-buffer)
  _vectorize(renderer, cam, W, H) {
    const lines = []; this.scene.traverse(o => { if (o.isLineSegments2) { lines.push(o); o.visible = false; } });
    const glassM = (this.meshes || []).filter(m => MAT[m.key].glass).map(m => m.mesh); glassM.forEach(m => m.visible = false);
    const rt = new THREE.WebGLRenderTarget(W, H);
    this.scene.overrideMaterial = new THREE.MeshDepthMaterial({ depthPacking: THREE.RGBADepthPacking });
    const bg = this.scene.background; this.scene.background = null;
    renderer.setRenderTarget(rt); renderer.setClearColor(0xffffff, 1); renderer.clear(); renderer.render(this.scene, cam);
    const buf = new Uint8Array(W * H * 4); renderer.readRenderTargetPixels(rt, 0, 0, W, H, buf);
    renderer.setRenderTarget(null); this.scene.overrideMaterial = null; this.scene.background = bg;
    lines.forEach(o => o.visible = true); glassM.forEach(m => m.visible = true);
    const D = (px, py) => { if (px < 0 || py < 0 || px >= W || py >= H) return 1; const i = (py * W + px) * 4;
      return (buf[i] / 255 / 16777216 + buf[i + 1] / 255 / 65536 + buf[i + 2] / 255 / 256 + buf[i + 3] / 255) * 255 / 256; };
    const v = new THREE.Vector3();
    const proj = (x, y, z) => { v.set(x, y, z).project(cam); return [v.x, v.y, v.z * 0.5 + 0.5]; };
    const visible = (q) => { const px = Math.round((q[0] + 1) / 2 * W - 0.5), py = Math.round((q[1] + 1) / 2 * H - 0.5); let m = 0;
      for (let dx = -1; dx <= 1; dx++) for (let dy = -1; dy <= 1; dy++) m = Math.max(m, D(px + dx, py + dy)); return q[2] <= m + 0.0006; };
    // aristas
    const edges = [];
    for (const e of this.edges) {
      const P = e.pos;
      for (let i = 0; i < P.length; i += 6) {
        const a = proj(P[i], P[i + 1], P[i + 2]), b = proj(P[i + 3], P[i + 4], P[i + 5]);
        const lenPx = Math.hypot((b[0] - a[0]) * W / 2, (b[1] - a[1]) * H / 2); const n = Math.max(2, Math.ceil(lenPx / 1.5));
        let run = null;
        for (let k = 0; k <= n; k++) {
          const t = k / n, q = [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t];
          if (visible(q)) { if (!run) run = [q, q]; else run[1] = q; }
          else if (run) { edges.push([run[0][0], run[0][1], run[1][0], run[1][1], e.w < 1 ? 1 : 0]); run = null; }
        }
        if (run) edges.push([run[0][0], run[0][1], run[1][0], run[1][1], e.w < 1 ? 1 : 0]);
      }
    }
    // caras visibles agrupadas por plano, con profundidad para el orden del pintor
    const toViewer = new THREE.Vector3(); cam.getWorldDirection(toViewer); toViewer.negate();
    const groups = new Map(); const A = new THREE.Vector3(), B = new THREE.Vector3(), C = new THREE.Vector3(), N = new THREE.Vector3();
    (this.meshes || []).forEach((m, mi) => {
      const g = m.geom, P = g.attributes.position.array, idx = g.index ? g.index.array : null;
      const nT = (idx ? idx.length : P.length / 3) / 3;
      const capOf = (t) => { for (const gr of g.groups || []) if (t * 3 >= gr.start && t * 3 < gr.start + gr.count) return gr.materialIndex === 0 && g.type === 'ExtrudeGeometry'; return false; };
      for (let t = 0; t < nT; t++) {
        const i0 = idx ? idx[3 * t] : 3 * t, i1 = idx ? idx[3 * t + 1] : 3 * t + 1, i2 = idx ? idx[3 * t + 2] : 3 * t + 2;
        A.fromArray(P, 3 * i0); B.fromArray(P, 3 * i1); C.fromArray(P, 3 * i2);
        N.subVectors(B, A).cross(new THREE.Vector3().subVectors(C, A)); if (N.lengthSq() < 1e-9) continue; N.normalize();
        if (N.dot(toViewer) <= 1e-4 && !MAT[m.key].glass) continue;
        const d = N.dot(A); const key = mi + '|' + N.x.toFixed(2) + ',' + N.y.toFixed(2) + ',' + N.z.toFixed(2) + '|' + d.toFixed(0);
        let G = groups.get(key);
        if (!G) { G = { key: m.key, color: MAT[m.key].color, hatch: MAT[m.key].hatch || null, glass: !!MAT[m.key].glass, cap: capOf(t), tris: [], dsum: 0, dn: 0 }; groups.set(key, G); }
        const pa = proj(A.x, A.y, A.z), pb = proj(B.x, B.y, B.z), pc = proj(C.x, C.y, C.z);
        G.tris.push([pa[0], pa[1], pb[0], pb[1], pc[0], pc[1]]); G.dsum += pa[2] + pb[2] + pc[2]; G.dn += 3;
        G.shade = Math.max(0.55, Math.min(1, 0.62 + 0.38 * N.dot(new THREE.Vector3(0.55, 1, 0.75).normalize())));
      }
    });
    const faces = [...groups.values()].map(G => ({ key: G.key, color: G.color, hatch: G.hatch, glass: G.glass, cap: G.cap, shade: G.shade, depth: G.dsum / G.dn, tris: G.tris }))
      .sort((p, q) => q.depth - p.depth);
    return { faces, edges };
  }
  render(Wpx, Hpx, dir, frac = 0.72, offset = [0, 0], lineW = 3.2, fixedW = null) {
    const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
    renderer.setPixelRatio(1); renderer.setSize(Wpx, Hpx);
    const target = this.bbox.getCenter(new THREE.Vector3());
    const d = new THREE.Vector3(...dir).normalize();
    const cam = new THREE.OrthographicCamera(-1, 1, 1, -1, -100000, 100000);
    cam.position.copy(target).addScaledVector(d, 20000); cam.up.set(0, 1, 0); cam.lookAt(target);
    cam.updateMatrixWorld();
    // encuadre
    const inv = cam.matrixWorldInverse; let mnx = 1e9, mxx = -1e9, mny = 1e9, mxy = -1e9;
    const b = this.bbox;
    for (const x of [b.min.x, b.max.x]) for (const y of [b.min.y, b.max.y]) for (const z of [b.min.z, b.max.z]) {
      const v = new THREE.Vector3(x, y, z).applyMatrix4(inv); mnx = Math.min(mnx, v.x); mxx = Math.max(mxx, v.x); mny = Math.min(mny, v.y); mxy = Math.max(mxy, v.y);
    }
    const asp = Wpx / Hpx; let w = (mxx - mnx) / frac, h = (mxy - mny) / frac;
    if (w / h > asp) h = w / asp; else w = h * asp;
    if (fixedW) { w = fixedW; h = w / asp; }
    { let ax = 1e9, bx = -1e9, ay = 1e9, by = -1e9; const v = new THREE.Vector3();
      for (const m of this.meshes || []) { const P = m.geom.attributes.position.array;
        for (let i = 0; i < P.length; i += 3) { v.set(P[i], P[i + 1], P[i + 2]).applyMatrix4(inv); ax = Math.min(ax, v.x); bx = Math.max(bx, v.x); ay = Math.min(ay, v.y); by = Math.max(by, v.y); } }
      this.fit = { needW: bx - ax, needH: by - ay };
      if (fixedW) { const cx2 = (ax + bx) / 2, cy2 = (ay + by) / 2; cam.left = cx2 - w / 2; cam.right = cx2 + w / 2; cam.top = cy2 + h / 2; cam.bottom = cy2 - h / 2; cam.updateProjectionMatrix(); } }
    const cx = (mnx + mxx) / 2 - offset[0] * w, cy = (mny + mxy) / 2 - offset[1] * h;
    if (!fixedW) { cam.left = cx - w / 2; cam.right = cx + w / 2; cam.top = cy + h / 2; cam.bottom = cy - h / 2; cam.updateProjectionMatrix(); }
    this.mmPerPx = w / Wpx;
    // aristas
    for (const e of this.edges) {
      const g = new LineSegmentsGeometry(); g.setPositions(e.pos);
      const m = new LineMaterial({ color: '#111111', linewidth: lineW * e.w, resolution: new THREE.Vector2(Wpx, Hpx) });
      const l = new LineSegments2(g, m); l.renderOrder = 20; this.scene.add(l);
    }
    renderer.render(this.scene, cam);
    const url = renderer.domElement.toDataURL('image/png');
    const anchors = this.anchors.map(a => { const v = a.p.clone().project(cam); return { n: a.n, x: (v.x + 1) / 2, y: (1 - v.y) / 2 }; });
    const vec = this.want2D ? this._vectorize(renderer, cam, Wpx, Hpx) : null;
    renderer.dispose();
    return { url, anchors, scale: w, fit: this.fit, vec };
  }
}
