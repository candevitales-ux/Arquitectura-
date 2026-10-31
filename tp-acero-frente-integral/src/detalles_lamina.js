// Composición de los detalles 1, 2 y 3 (axonometría isométrica, ESC. 1:10 exacta) en la lámina.
import { DETALLES, escena } from './detalles.js';
import { MAT } from './lib3d.js';
globalThis.LINE_ONLY = true;
for (const k of Object.keys(MAT)) { const m = MAT[k]; if (k === 'red') { m.color = '#444444'; continue; } m.color = '#ffffff'; if (m.bg) m.bg = '#ffffff'; }
const PX = 14, DEN = 10, HD = 10, ISO = [1, 1, 1];
const SLOTS = [
  { d: 0, x: 30, y: 33, W: 145, H: 112 },
  { d: 1, x: 30, y: 148, W: 145, H: 112 },
  { d: 2, x: 30, y: 263, W: 145, H: 118 },
];
export async function dibujar(page) {
  let o = '';
  const T = (x, y, s, z = {}) => o += `<text x="${x}" y="${y}" font-size="${z.size || 2.4}" font-weight="${z.w || 'normal'}" fill="${z.fill || '#000'}" text-anchor="${z.a || 'start'}">${s}</text>`;
  const Ln = (p) => o += `<polyline points="${p.map(q => q.join(',')).join(' ')}" fill="none" stroke="#000" stroke-width="0.15"/>`;
  for (const s of SLOTS) {
    const D = DETALLES[s.d], iw = s.W, ih = s.H - HD;
    const S = escena(D); S.want2D = !!globalThis.WANT2D;   // vectores 2D para el DWG
    const r = S.render(Math.round(iw * PX), Math.round(ih * PX), ISO, 1, [0, 0], 2.0, iw * DEN);
    console.log(D.t, 'necesita', (S.fit.needW / DEN).toFixed(1), 'x', (S.fit.needH / DEN).toFixed(1), 'mm; slot', iw, 'x', ih);
    if (r.vec) { const mx = (x) => s.x + (x + 1) / 2 * iw, my = (y) => s.y + HD + (1 - y) / 2 * ih;
      (globalThis.VEC2D ||= []).push({ d: D.n, faces: r.vec.faces.map(f => ({ ...f, tris: f.tris.map(t => [mx(t[0]), my(t[1]), mx(t[2]), my(t[3]), mx(t[4]), my(t[5])]) })),
        edges: r.vec.edges.map(e => [mx(e[0]), my(e[1]), mx(e[2]), my(e[3]), e[4]]) }); }
    const img = document.createElement('img'); img.className = 'det'; img.src = r.url;
    Object.assign(img.style, { left: s.x + 'mm', top: (s.y + HD) + 'mm', width: iw + 'mm', height: ih + 'mm' });
    page.appendChild(img);
    T(s.x - 18, s.y + 6.5, `${D.n}.`, { size: 8, fill: '#ff0000' });
    T(s.x - 9, s.y + 3.6, `DETALLE ${D.n} · AXONOMETRÍA ESC 1:10`, { size: 2.8, w: 'bold' });
    T(s.x - 9, s.y + 7.2, D.st, { size: 2.2 });
    const pts = r.anchors.map(a => ({ n: a.n, ax: s.x + a.x * iw, ay: s.y + HD + a.y * ih }));
    const cx = s.x + iw / 2, half = (S.fit.needW / DEN) / 2;
    const byX = [...pts].sort((p, q) => p.ax - q.ax); byX.forEach((p, k) => p.left = k < Math.ceil(pts.length / 2));
    for (const side of [true, false]) {
      const L = pts.filter(p => p.left === side).sort((a, b) => a.ay - b.ay);
      const gap = 5.6, ymin = s.y + HD + 3, ymax = s.y + s.H - 3;
      L.forEach((p, k) => { p.by = Math.max(p.ay, k ? L[k - 1].by + gap : ymin); });
      for (let k = L.length - 1; k >= 0; k--) { const lim = k === L.length - 1 ? ymax : L[k + 1].by - gap; if (L[k].by > lim) L[k].by = lim; }
      const bx = side ? Math.max(s.x + 3, cx - half - 8) : Math.min(s.x + iw - 3, cx + half + 8);
      for (const p of L) {
        Ln([[p.ax, p.ay], [side ? bx + 6 : bx - 6, p.by], [side ? bx + 2.6 : bx - 2.6, p.by]]);
        o += `<circle cx="${p.ax}" cy="${p.ay}" r="0.35" fill="#000"/><circle cx="${bx}" cy="${p.by}" r="2.6" fill="#fff" stroke="#000" stroke-width="0.18"/>`;
        T(bx, p.by + 1.25, p.n, { size: 3.5, a: 'middle' });
      }
    }
  }
  return o;
}
