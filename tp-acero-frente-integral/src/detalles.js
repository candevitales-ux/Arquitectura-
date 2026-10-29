// Detalles 1, 2 y 3 (los círculos del corte original) en axonometría isométrica.
// La geometría se toma del corte original de la alumna: coordenadas "P" = mm de papel del PDF original (dibujado a 1:10),
// x a la derecha (interior), y hacia abajo. En 3D: x = (P - 193,6)·10 mm, y = (300 - P)·10 mm, z = profundidad (0 = plano de corte).
// Los elementos cortados se extruyen z ∈ [-200, 0]; detrás (z -200…-250) va la columna del frente integral (en vista en el corte)
// y la chapa de unión de la IPN con sus bulones. Correcciones de la docente: 36 a 40 (mismas que en el corte).
import * as THREE from 'three';
import { Scene3D, MAT } from './lib3d.js';
Object.assign(MAT, {
  hl: { color: '#efe6cc', hatch: 'h', bg: '#f3ecd8', period: 60 },
  pur: { color: '#fff0a0', hatch: 'eps', bg: '#fff3b4', period: 40 },
  inox: { color: '#b9bec4' }, epdm: { color: '#202020' },
});

// ------------------------------------------------------------------ recorte por caja
function clipPoly(P, u0, u1, v0, v1) {
  const edge = (P, inside, inter) => { const o = []; for (let i = 0; i < P.length; i++) { const a = P[i], b = P[(i + 1) % P.length];
    const ia = inside(a), ib = inside(b); if (ia) o.push(a); if (ia !== ib) o.push(inter(a, b)); } return o; };
  const lerp = (a, b, t) => [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t];
  P = edge(P, p => p[0] >= u0, (a, b) => lerp(a, b, (u0 - a[0]) / (b[0] - a[0]))); if (!P.length) return P;
  P = edge(P, p => p[0] <= u1, (a, b) => lerp(a, b, (u1 - a[0]) / (b[0] - a[0]))); if (!P.length) return P;
  P = edge(P, p => p[1] >= v0, (a, b) => lerp(a, b, (v0 - a[1]) / (b[1] - a[1]))); if (!P.length) return P;
  return edge(P, p => p[1] <= v1, (a, b) => lerp(a, b, (v1 - a[1]) / (b[1] - a[1])));
}
const area = (P) => { let s = 0; for (let i = 0; i < P.length; i++) { const a = P[i], b = P[(i + 1) % P.length]; s += a[0] * b[1] - b[0] * a[1]; } return Math.abs(s / 2); };
class Clipped extends Scene3D {
  constructor(box) { super(); this.B = box; }
  _r(axis) { const { x, y, z } = this.B; if (axis === 'z') return [x, y, z]; if (axis === 'x') return [[-z[1], -z[0]], y, x]; return [x, [-z[1], -z[0]], y]; }
  prism(pts, axis, w0, w1, key, holes = [], opt = {}) {
    if (w1 < w0) [w0, w1] = [w1, w0];
    const [U, V, W] = this._r(axis); w0 = Math.max(w0, W[0]); w1 = Math.min(w1, W[1]); if (w1 - w0 < 0.3) return null;
    const P = clipPoly(pts, U[0], U[1], V[0], V[1]); if (P.length < 3 || area(P) < 0.5) return null;
    const H = holes.filter(h => h.every(p => p[0] > U[0] && p[0] < U[1] && p[1] > V[0] && p[1] < V[1]));
    return super.prism(P, axis, w0, w1, key, H, opt);
  }
  cyl(axis, c1, c2, r, w0, w1, key, seg = 8, half = false) {
    seg = Math.min(seg, 8); const { x, y, z } = this.B; if (w1 < w0) [w0, w1] = [w1, w0];
    const R = { x, y, z }[axis]; w0 = Math.max(w0, R[0]); w1 = Math.min(w1, R[1]); if (w1 - w0 < 0.3) return null;
    const [p1, p2] = axis === 'y' ? [x, z] : axis === 'x' ? [y, z] : [x, y];
    if (c1 + r < p1[0] || c1 - r > p1[1] || c2 + r < p2[0] || c2 - r > p2[1]) return null;
    if (!half) return super.cyl(axis, c1, c2, r, w0, w1, key, seg);
    const g = new THREE.CylinderGeometry(r, r, w1 - w0, seg, 1, false, Math.PI / 2, Math.PI); g.translate(c1, (w0 + w1) / 2, c2);
    const cap = new THREE.PlaneGeometry(2 * r, w1 - w0); cap.translate(c1, (w0 + w1) / 2, c2);
    this._add(cap, key, 30); return this._add(g, key, 35);
  }
}

// ------------------------------------------------------------------ coordenadas P -> mm
const X = (p) => (p - 193.6) * 10, Y = (p) => (300 - p) * 10;
const D = -350, ZM0 = -25, ZM1 = 25, ZF = -25;   // profundidad · columna del F.I. (cortada por su eje, z = 0) · travesaños y vidrios detrás de ella
let S;
const box = (x0, x1, y0, y1, z0, z1, key) => S.box(Math.min(X(x0), X(x1)), Math.max(X(x0), X(x1)), Math.min(Y(y0), Y(y1)), Math.max(Y(y0), Y(y1)), z0, z1, key);
const pz = (pts, key, z0 = D, z1 = 0, holes = []) => S.prism(pts.map(([a, b]) => [X(a), Y(b)]), 'z', z0, z1, key, holes.map(h => h.map(([a, b]) => [X(a), Y(b)])));
const sh = (pts, t, key, z0 = D, z1 = 0) => S.sheet(pts.map(([a, b]) => [X(a), Y(b)]), t, 'z', z0, z1, key);
const cy = (axis, a, b, r, w0, w1, key, seg = 8, half = false) => {   // a,b en P o z según el eje
  if (axis === 'y') return S.cyl('y', X(a), b, r, Math.min(Y(w0), Y(w1)), Math.max(Y(w0), Y(w1)), key, seg, half);
  if (axis === 'z') return S.cyl('z', X(a), Y(b), r, w0, w1, key, seg);
  return S.cyl('x', Y(a), b, r, Math.min(X(w0), X(w1)), Math.max(X(w0), X(w1)), key, seg);
};

// ------------------------------------------------------------------ piezas del original
function panel9(y0, y1) {                     // termopanel: núcleo PUR 40 + chapa exterior con nervios + chapa interior
  box(181.6, 186.7, y0, y1, D - 50, 0, 'pur'); box(186.7, 186.8, y0, y1, D - 50, 0, 'galv');
  const pts = []; for (let y = y0; y < y1; y += 4.5) pts.push([181.6, y], [181.6, y + 0.8], [181.2, y + 1.2], [181.2, y + 3.3], [181.6, y + 3.7]);
  pts.push([181.6, y1]); sh(pts, 0.8, 'galv', D - 50, 0);
}
function zClip(y, up) {                       // 11: sujeción perfil Z / omega del panel
  const s = up ? -1 : 1;
  sh([[186.8, y + s * 0.8], [186.8, y], [188.2, y - s * 0.3], [188.2, y - s * 1.1]], 2, 'galv', -150, -110);
  sh([[186.8, y + s * 0.8], [186.8, y], [188.2, y - s * 0.3], [188.2, y - s * 1.1]], 2, 'galv', -60, -20);
}
function eps28(y0, y1) { box(188.4, 191.9, y0, y1, D, 0, 'eps'); }
function ipn13(yt) {                          // IPN 200 cortada + chapa de unión a columna con bulones (en vista)
  const d = yt - 48.3, P = [[193.8, 48.3], [203.0, 48.3], [203.0, 49.0], [199.0, 49.8], [199.0, 68.7], [203.0, 69.5], [203.0, 70.2], [193.8, 70.2], [193.8, 69.5], [198.2, 68.7], [198.2, 49.8], [193.8, 49.0]]
    .map(([a, b]) => [a, b + d]);
  pz(P, 'steel', D, 0);
  box(191.9, 204.8, 49.2 + d, 69.0 + d, D - 15, D, 'steel');
  for (const yy of [53.1, 59.1, 65.1]) for (const xx of [194.05, 202.8]) { cy('z', xx, yy + d, 15, D, D + 12, 'steel'); cy('z', xx, yy + d, 7, D + 12, D + 20, 'steel'); }
  for (const s of [-1, 1]) { const xw = s < 0 ? 198.2 : 199.0;                      // ángulos de unión al alma
    box(xw, xw + s * 0.6, 50.5 + d, 67.5 + d, D, D + 50, 'galv'); }
}
function losa6(yt, yv) {                      // capa de compresión + placa colaborante (valles en yv, crestas 5,6 mm P arriba)
  const prof = [[188.4, yv], [211.8, yv], [215.3, yv - 5.6], [228.5, yv - 5.6], [232.0, yv], [240, yv]];
  pz([...prof, [240, yt], [188.4, yt]], 'pre');
  sh(prof.map(([a, b]) => [a, b + 0.05]), 1.2, 'galv');
  sh([[194.5, yt + 2.4], [240, yt + 2.4]], 4, 'red', D, -10);                                   // malla
  for (const xx of [197.5, 214.4, 224.3]) cy('z', xx, yt + 2.4, 2.5, D, -10, 'red');
  pz([[216.6, yv - 5.6], [216.6, yv - 7.0], [221.6, yv - 7.4], [226.4, yv - 7.0], [226.4, yv - 5.6]], 'neo', -120, -90);   // separador
  for (const z of [-40, -160]) { cy('y', 206.3, z, 5, yv, yt + 2.2, 'steel'); cy('y', 206.3, z, 9, yt + 2.2, yt + 1.6, 'steel'); }   // conectores
  sh([[188.25, yv + 0.1], [188.25, yt]], 3, 'galv');                                            // 12 zinguería de borde
  sh([[201.6, yv], [201.6, yv - 1.3], [202.7, yv - 1.3], [202.7, yv - 0.8]], 1.5, 'galv');
}
function travesano(yt, yb, z1 = ZF) {                   // 20: tapa ext. MT-0819 + canal de vidrio + tapa int. MT-0817 (cuerpo)
  pz([[193.6, yt], [195.2, yt], [195.2, yb], [193.6, yb]], 'alu', D, 0, [[[193.85, yt + 0.25], [194.95, yt + 0.25], [194.95, yb - 0.25], [193.85, yb - 0.25]]]);
  pz([[197.4, yt], [203.0, yt], [203.0, yb], [197.4, yb]], 'alu', D, 0, [[[197.65, yt + 0.25], [202.75, yt + 0.25], [202.75, yb - 0.25], [197.65, yb - 0.25]]]);
  box(195.2, 197.4, yt, yt + 0.5, D, 0, 'alu'); box(195.2, 197.4, yb - 0.5, yb, D, 0, 'alu');
  box(195.2, 195.45, yt + 0.5, yb - 0.5, D, 0, 'epdm'); box(197.15, 197.4, yt + 0.5, yb - 0.5, D, 0, 'epdm');
}
function vidrio(y0, y1) { box(195.45, 195.85, y0, y1, D, ZF, 'glass'); box(196.95, 197.35, y0, y1, D, ZF, 'glass'); box(195.85, 196.95, y0, y0 + 0.8, D, ZF, 'alu'); box(195.85, 196.95, y1 - 0.8, y1, D, ZF, 'alu'); }
// 21: columna del frente integral (en vista, detrás); "ventana" abierta hacia el interior para ver el tubo soldado (37)
function columnaFI(y0, y1) {                 // 21: columna del frente integral, cortada por su eje (z = 0): se ve el tubo soldado adentro
  const U = [[193.6, 0], [193.85, 0], [193.85, 22.5], [202.75, 22.5], [202.75, 0], [203.0, 0], [203.0, 25], [193.6, 25]].map(([a, v]) => [X(a), v]);
  S.prism(U, 'y', Math.min(Y(y0), Y(y1)), Math.max(Y(y0), Y(y1)), 'alu');
}
function tubo37(yb) {                          // 37: tubo 40x40 soldado al ala inferior de la IPN, dentro de la columna del F.I. + bulón pasante
  const U = [[198.0, 0], [198.3, 0], [198.3, 17], [201.7, 17], [201.7, 0], [202.0, 0], [202.0, 20], [198.0, 20]].map(([a, v]) => [X(a), v]);
  S.prism(U, 'y', Y(yb + 13.5), Y(yb), 'steel');
  for (const [a, b] of [[197.4, 198.0], [202.0, 202.6]]) box(a, b, yb, yb + 0.6, -20, 0, 'neo');   // cordón de soldadura
  cy('z', 200.0, yb + 9.5, 6, -33, 0, 'inox'); cy('z', 200.0, yb + 9.5, 10, -34, -28, 'inox', 6);
}
function bulonIPN(ya, yb2) { cy('y', 200.0, 0, 6, ya, yb2, 'steel', 8, true); }
function cielorraso(yC) {                      // yC = cara inferior IPN 180 (65,9 / 179,4)
  const d = yC - 65.9;
  const zc = -230;                             // el cielorraso se recorta para ver la columna del frente integral detrás
  box(205.5, 240, 69.6 + d, 70.3 + d, zc, 0, 'yeso');
  for (const xc of [209.4]) {
    sh([[xc, 65.9 + d], [xc, 69.6 + d], [xc + 3.2, 69.6 + d], [xc + 3.2, 65.9 + d]], 1.6, 'galv', zc, 0);     // 18 perfil C
    box(xc + 0.2, xc + 3.0, 65.6 + d, 65.9 + d, zc, 0, 'neo');
  }
  sh([[205.5, 69.6 + d], [205.5, 70.9 + d], [204.6, 70.9 + d], [204.6, 71.5 + d]], 1.2, 'galv', zc, 0);       // 14 perfil Z buña
}
function vela39(x, ytop, ybot) {               // vela rígida a losa: montante 35 + ángulo de fijación
  const z0 = -100, z1 = -65;
  S.prism([[X(x - 1.75), -z1], [X(x + 1.75), -z1], [X(x + 1.75), -z0], [X(x - 1.75), -z0], [X(x - 1.75), -z0 - 3], [X(x + 1.45), -z0 - 3], [X(x + 1.45), -z1 + 3], [X(x - 1.75), -z1 + 3]],
    'y', Y(ybot), Y(ytop + 0.6), 'galv');
  box(x - 1.75, x + 3.2, ytop + 0.1, ytop + 0.6, z0, z1, 'galv');
  cy('y', x + 2.4, (z0 + z1) / 2, 3, ytop + 0.1, ytop - 2.2, 'inox');
}
function baranda26(yp, yb, brocas) {           // yp: planchuela, yb: centro de la esfera/tubo posapié
  const zc = -40;
  box(203.8, 208.1, yp - 0.3, yp, zc - 35, zc + 35, 'inox');
  cy('y', 206.0, zc, 5, yp - 0.3, yb + 0.8, 'inox');
  cy('z', 206.0, yb, 8, D, 0, 'inox');
  if (brocas) for (const xx of [204.45, 207.5]) { cy('y', xx, zc, 4, yp, yp + 5.8, 'steel'); cy('y', xx, zc, 8, yp - 0.3, yp - 0.75, 'steel', 6); }
}

// ------------------------------------------------------------------ modelo (todo el corte)
function modelo() {
  // ---------- CUBIERTA (detalle 1)
  panel9(15.0, 70.5);
  sh([[180.6, 16.8], [180.6, 15.0], [188.4, 15.25], [188.4, 16.6]], 1.5, 'galv', D - 50, 0);                // 1 cupertina
  sh([[187.35, 15.6], [187.35, 28.6], [188.0, 29.6], [240, 29.6]], 5, 'memb', D, 0);                     // 2 membrana
  box(188.4, 240, 30.0, 32.1, D, -30, 'mort');                                                           // 3 carpeta
  box(189.0, 240, 32.1, 37.5, D, -60, 'hl');                                                             // 4 contrapiso liviano
  sh([[188.6, 30.2], [188.6, 37.2], [194.5, 37.2]], 2, 'galv', D, 0);                                    // 10 perfil L
  box(188.4, 240, 37.5, 38.0, D, -90, 'film');                                                           // 5 barrera de vapor
  losa6(38.0, 48.3);
  eps28(48.4, 70.3); zClip(33.4, true); zClip(69.8, false);
  ipn13(48.3);
  sh([[181.6, 70.6], [192.0, 70.6], [193.6, 70.9]], 1.5, 'galv', D - 50, 0);                             // 19 zinguería buña
  travesano(70.5, 76.4); vidrio(76.4, 100);
  bulonIPN(66.0, 72.3);
  columnaFI(70.5, 104); tubo37(70.25);
  cielorraso(65.9);
  // corrección 36: chapa plegada de anclaje del panel, atornillada al panel y con brocas a la losa
  sh([[187.78, 17.2], [187.78, 37.72], [197.2, 37.72]], 2.5, 'galv', -170, -30);
  for (const z of [-140, -60]) { for (const yy of [21.0, 33.0]) S.cyl('x', Y(yy), z, 3, X(184.2), X(188.1), 'inox');
    for (const xx of [192.0, 195.6]) { cy('y', xx, z, 4, 37.72, 41.6, 'steel'); cy('y', xx, z, 8, 37.72, 37.3, 'steel', 6); } }
  for (const x of [211.0]) vela39(x, 48.35, 65.9);
  // ---------- ENTREPISO (detalle 2)
  vidrio(130, 145.4); travesano(145.4, 150.6); columnaFI(130, 150.6);
  cy('y', 200.85, 0, 6, 149.4, 162.2, 'steel', 8, true); box(198.8, 202.9, 149.4, 150.6, -20, 0, 'steel');
  panel9(151.0, 184.4);
  sh([[178.0, 152.8], [178.0, 151.9], [193.4, 150.55]], 1.5, 'galv', D - 50, 0);                        // 25 alféizar
  box(193.0, 193.6, 150.1, 150.7, D, 0, 'seal');                                                         // 24 sellador
  box(203.4, 240, 148.5, 149.3, D, -100, 'porc');                                                        // 27 solado
  box(203.4, 240, 149.3, 150.6, D, -60, 'mort');                                                         // 3 carpeta
  box(188.4, 240, 150.6, 151.0, D, -30, 'film');                                                         // 5
  losa6(151.0, 161.8);
  eps28(161.9, 184.3); zClip(153.6, true); zClip(182.7, false);
  ipn13(161.8);
  baranda26(148.55, 139.4, true);
  sh([[181.6, 184.5], [192.0, 184.5], [193.6, 184.8]], 1.5, 'galv', D - 50, 0);
  travesano(184.4, 190.4); vidrio(190.4, 215);
  bulonIPN(179.5, 186.0);
  columnaFI(184.4, 215); tubo37(183.75);
  cielorraso(179.4);
  vela39(211.0, 161.85, 179.5);
  // ---------- ARRANQUE (detalle 3)
  vidrio(235, 257.3); travesano(257.3, 262.5); columnaFI(235, 262.5);
  cy('y', 200.85, 0, 6, 261.3, 278.5, 'steel', 8, true); box(199.3, 202.7, 261.3, 262.4, -20, 0, 'steel');
  box(193.0, 193.6, 262.0, 262.6, D, 0, 'seal'); sh([[183.0, 264.0], [193.4, 262.6]], 1.5, 'galv', D, 0);
  box(203.6, 240, 258.4, 258.9, D, -100, 'porc');                                                        // 27
  box(203.6, 240, 258.9, 261.4, D, -60, 'mort');                                                         // 3
  box(203.6, 240, 261.4, 263.75, D, -30, 'hid');                                                         // 33
  pz([[150, 264.5], [178.3, 263.9], [178.3, 271.5], [150, 271.5]], 'hl', D, 0);                        // 4 contrapiso (exterior)
  pz([[218.4, 263.75], [240, 263.75], [240, 271.5], [218.4, 271.5]], 'hl', D, 0);                      // 4 contrapiso (interior)
  pz([[178.3, 263.75], [218.4, 263.75], [218.4, 271.5], [178.3, 271.5]], 'insitu', D, 0);              // 40 DADO estructural H°A°
  box(178.3, 218.4, 271.5, 272.6, D, 0, 'steel');                                                      // 29 platabanda
  pz([[178.3, 272.6], [218.4, 272.6], [218.4, 300], [178.3, 300]], 'insitu', D, 0);                    // 34 cuello de la zapata
  for (const [a, b] of [[150, 178.3], [218.4, 240]]) { box(a, b, 271.5, 271.8, D, 0, 'film'); box(a, b, 271.8, 300, D, 0, 'tierra'); }
  for (const xx of [183.4, 213.6]) {                                                                     // 31 pernos (cortados) + 30 tuercas
    cy('y', xx, 0, 6, 268.0, 300, 'steel', 8, true);
    for (const [a, b, r] of [[268.0, 268.7, 7], [268.7, 270.0, 16], [270.0, 271.5, 16], [272.6, 274.0, 16]]) cy('y', xx, 0, r, a, b, 'steel', 6, true);
  }
  baranda26(258.3, 249.7, false);
}

const ANCH = [
  // detalle 1
  [1, 184.5, 15.1, -100], [2, 210, 29.6, -100], [3, 215, 31.0, -40], [4, 220, 35.0, -70], [5, 225, 37.7, -100], [6, 218, 45.0, 0], [7, 221.5, 41.0, -105],
  [8, 206.3, 44.0, -40], [9, 184.0, 40.0, 0], [10, 188.6, 34.0, -15], [11, 187.5, 69.6, -130], [12, 188.25, 44.0, 0], [13, 198.6, 60.0, 0],
  [14, 205.1, 70.9, -60], [15, 225, 70.3, -60], [18, 211.0, 69.6, -150], [19, 186.0, 70.6, -100], [20, 200.0, 76.4, -80], [22, 196.4, 90, -60], [21, 202.9, 98, -10],
  [28, 190.1, 60.0, 0], [36, 192.0, 37.72, -100], [37, 200.0, 79.0, 0], [39, 211.0, 58.0, -65],
  // detalle 2
  [26, 206.0, 139.4, -90], [38, 207.5, 152.0, -40], [27, 225, 148.5, -100], [3, 225, 149.9, -70], [5, 225, 150.8, -40], [24, 193.3, 150.4, -100], [25, 180, 151.9, -150],
  [9, 184.0, 165, 0], [28, 190.1, 172, 0], [12, 188.25, 156.0, 0], [13, 198.6, 175.0, 0], [6, 218, 158, 0], [17, 230, 161.0, -60],
  [20, 200.0, 190.4, -80], [21, 202.9, 204, -10], [37, 200.0, 192.5, 0], [39, 211.0, 172.0, -65], [15, 225, 183.7, -60], [18, 211.0, 183.2, -150], [14, 205.1, 184.4, -60],
  [22, 196.4, 140, -60], [11, 187.5, 153.6, -130],
  // detalle 3
  [22, 196.4, 245, -60], [20, 200.0, 262.0, -80], [26, 206.0, 249.7, -90], [27, 225, 258.4, -100], [3, 225, 260.0, -60], [33, 225, 262.5, -30], [24, 193.3, 262.3, -100],
  [25, 186, 263.6, -100], [4, 225, 267.0, 0], [4, 160, 267.5, 0], [40, 205, 267.0, 0], [29, 190, 272.0, 0], [30, 213.6, 269.3, 0], [31, 183.4, 285, 0],
  [32, 228, 271.6, -100], [34, 200, 285, 0], [35, 228, 285, 0], [21, 202.9, 245, -10],
];

export const DETALLES = [
  { n: 1, t: 'DETALLE 1', st: 'Encuentro cubierta / frente integral (círculo 1 del corte)', box: { x: [X(179.8), X(240)], y: [Y(104), Y(13.8)], z: [D - 15, 0] } },
  { n: 2, t: 'DETALLE 2', st: 'Encuentro entrepiso / frente integral (círculo 2 del corte)', box: { x: [X(177.3), X(240)], y: [Y(205), Y(134)], z: [D - 15, 0] } },
  { n: 3, t: 'DETALLE 3', st: 'Arranque del frente integral y base de columna (círculo 3 del corte)', box: { x: [X(150), X(240)], y: [Y(300), Y(240)], z: [D, 0] } },
];
export function escena(d) {
  S = new Clipped(d.box);
  modelo();
  const { x, y, z } = d.box;
  for (const [n, a, b, c] of ANCH) { const ax = X(a), ay = Y(b); if (ax >= x[0] && ax <= x[1] && ay >= y[0] && ay <= y[1] && c >= z[0] && c <= z[1]) S.anchor(n, ax, ay, c); }
  return S;
}
