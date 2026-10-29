// Composición de los 3 detalles axonométricos (isométrica, esc. 1:10 exacta) en la lámina A3.
import { DETALLES, escena } from './detalles.js';
import { MAT } from './lib3d.js';
globalThis.LINE_ONLY = true;
for (const k of Object.keys(MAT)) { const m = MAT[k]; if (k === 'red') { m.color = '#444444'; continue; } m.color = '#ffffff'; if (m.bg) m.bg = '#ffffff'; }
const PX = 14, DEN = 10, HD = 9, ISO = [1, 1, 1];
export const SLOTS = [
  { d: 0, x: 6, y: 131, W: 83, H: 133 },
  { d: 1, x: 90, y: 131, W: 83, H: 133 },
  { d: 2, x: 6, y: 266, W: 167, H: 131 },
];
export async function dibujar(page) {
  let o = '';
  const T = (x, y, s, z = {}) => o += `<text x="${x}" y="${y}" font-size="${Math.max(z.size || 2.8, 2.8)}" font-weight="${z.w || 'normal'}" fill="${z.fill || '#000'}" text-anchor="${z.a || 'start'}">${s}</text>`;
  const Ln = (p) => o += `<polyline points="${p.map(q => q.join(',')).join(' ')}" fill="none" stroke="#000" stroke-width="0.12"/>`;
  for (const s of SLOTS) {
    const D = DETALLES[s.d];
    const iw = s.W, ih = s.H - HD;
    const S = escena(D);
    const r = S.render(Math.round(iw * PX), Math.round(ih * PX), ISO, 1, [0, 0], 2.2, iw * DEN);
    console.log(D.t, 'necesita', (S.fit.needW / DEN).toFixed(1), 'x', (S.fit.needH / DEN).toFixed(1), 'mm; slot', iw, 'x', ih);
    const img = document.createElement('img'); img.className = 'det'; img.src = r.url;
    Object.assign(img.style, { left: s.x + 'mm', top: (s.y + HD) + 'mm', width: iw + 'mm', height: ih + 'mm' });
    page.appendChild(img);
    T(s.x + 1, s.y + 3.5, D.t, { size: 3.1, w: 'bold' });
    T(s.x + 1, s.y + 7.3, D.st);
    // globos
    const pts = r.anchors.map(a => ({ n: a.n, ax: s.x + a.x * iw, ay: s.y + HD + a.y * ih }));
    const byX = [...pts].sort((p, q) => p.ax - q.ax); byX.forEach((p, k) => p.left = k < Math.ceil(pts.length / 2));
    const cx = s.x + iw / 2, half = (S.fit.needW / DEN) / 2;
    for (const side of [true, false]) {
      const L = pts.filter(p => p.left === side).sort((a, b) => a.ay - b.ay);
      const gap = 5.5, ymin = s.y + HD + 2.6, ymax = s.y + s.H - 2.6;
      L.forEach((p, k) => { p.by = Math.max(p.ay, k ? L[k - 1].by + gap : ymin); });
      for (let k = L.length - 1; k >= 0; k--) { const lim = k === L.length - 1 ? ymax : L[k + 1].by - gap; if (L[k].by > lim) L[k].by = lim; }
      const bx = side ? Math.max(s.x + 2.6, cx - half - 6) : Math.min(s.x + iw - 2.6, cx + half + 6);
      for (const p of L) {
        Ln([[p.ax, p.ay], [side ? bx + 5.5 : bx - 5.5, p.by], [side ? bx + 2.35 : bx - 2.35, p.by]]);
        o += `<circle cx="${p.ax}" cy="${p.ay}" r="0.35" fill="#000"/><circle cx="${bx}" cy="${p.by}" r="2.35" fill="#fff" stroke="#000" stroke-width="0.2"/>`;
        T(bx, p.by + 1.0, p.n, { w: 'bold', a: 'middle' });
      }
    }
  }
  return o;
}
