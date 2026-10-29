// Detalles axonométricos (isométricos) 1:10 del corte integral acero + frente integral.
// Un único modelo 3D del edificio (misma geometría que src/corte.py) recortado por la "caja" de cada detalle.
// x+ interior, y+ arriba (mm, ±0,00 = NPT PB), z = 0 plano de corte (hacia el observador), z- hacia el fondo.
// Ejes: columna HEB 200 y montante del frente integral en z = -125.
import * as THREE from 'three';
import { Scene3D, MAT } from './lib3d.js';
Object.assign(MAT, {
  hl: { color: '#efe6cc', hatch: 'mort', bg: '#f3ecd8', period: 50 },
  pur: { color: '#fff0a0', hatch: 'eps', bg: '#fff3b4', period: 40 },
  steelv: { color: '#8c949b' },
  inox: { color: '#b9bec4' },
  epdm: { color: '#202020' },
});

// ------------------------------------------------------------------ recorte por caja (Sutherland–Hodgman en 2D)
function clipPoly(P, u0, u1, v0, v1) {
  const edge = (P, inside, inter) => { const o = []; for (let i = 0; i < P.length; i++) { const a = P[i], b = P[(i + 1) % P.length];
    const ia = inside(a), ib = inside(b); if (ia) o.push(a); if (ia !== ib) o.push(inter(a, b)); } return o; };
  const lerp = (a, b, t) => [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t];
  P = edge(P, p => p[0] >= u0, (a, b) => lerp(a, b, (u0 - a[0]) / (b[0] - a[0]))); if (!P.length) return P;
  P = edge(P, p => p[0] <= u1, (a, b) => lerp(a, b, (u1 - a[0]) / (b[0] - a[0]))); if (!P.length) return P;
  P = edge(P, p => p[1] >= v0, (a, b) => lerp(a, b, (v0 - a[1]) / (b[1] - a[1]))); if (!P.length) return P;
  P = edge(P, p => p[1] <= v1, (a, b) => lerp(a, b, (v1 - a[1]) / (b[1] - a[1])));
  return P;
}
const area = (P) => { let s = 0; for (let i = 0; i < P.length; i++) { const a = P[i], b = P[(i + 1) % P.length]; s += a[0] * b[1] - b[0] * a[1]; } return Math.abs(s / 2); };

class Clipped extends Scene3D {
  constructor(box) { super(); this.B = box; }
  _ranges(axis) {   // [uRange, vRange, wRange] del perfil según el eje de extrusión
    const { x, y, z } = this.B;
    if (axis === 'z') return [x, y, z];
    if (axis === 'x') return [[-z[1], -z[0]], y, x];
    return [x, [-z[1], -z[0]], y];
  }
  prism(pts, axis, w0, w1, key, holes = [], opt = {}) {
    if (w1 < w0) [w0, w1] = [w1, w0];
    const [U, V, W] = this._ranges(axis);
    w0 = Math.max(w0, W[0]); w1 = Math.min(w1, W[1]); if (w1 - w0 < 0.3) return null;
    const P = clipPoly(pts, U[0], U[1], V[0], V[1]); if (P.length < 3 || area(P) < 1) return null;
    const H = holes.filter(h => !h.circle && h.every(p => p[0] > U[0] && p[0] < U[1] && p[1] > V[0] && p[1] < V[1]));
    return super.prism(P, axis, w0, w1, key, H, opt);
  }
  cyl(axis, c1, c2, r, w0, w1, key, seg = 28, half = false) {
    seg = Math.min(seg, 8);   // facetas de 45° -> el contorno se dibuja en modo solo línea
    const { x, y, z } = this.B; if (w1 < w0) [w0, w1] = [w1, w0];
    const R = { x, y, z }[axis]; w0 = Math.max(w0, R[0]); w1 = Math.min(w1, R[1]); if (w1 - w0 < 0.3) return null;
    // centro dentro de la caja
    const [p1, p2] = axis === 'y' ? [x, z] : axis === 'x' ? [y, z] : [x, y];
    if (c1 + r < p1[0] || c1 - r > p1[1] || c2 + r < p2[0] || c2 - r > p2[1]) return null;
    if (!half) return super.cyl(axis, c1, c2, r, w0, w1, key, seg);
    // medio cilindro vertical cortado por z = 0 (queda la mitad z < 0)
    const g = new THREE.CylinderGeometry(r, r, w1 - w0, seg, 1, false, Math.PI / 2, Math.PI);
    g.translate(c1, (w0 + w1) / 2, c2);
    const cap = new THREE.PlaneGeometry(2 * r, w1 - w0); cap.translate(c1, (w0 + w1) / 2, c2);
    this._add(cap, key, 30); return this._add(g, key, 35);
  }
}

// ------------------------------------------------------------------ constantes (= corte.py)
const ZM = -125, ZB = -250;                 // eje montante / columna ; fondo del detalle
const BX0 = 230, BX1 = 320;                 // IPN 200
const YE_B = 2640, YR_B = 5680;             // fondo vigas IPN 200
const XE = 1600;
const seg2 = (zb = -1e5) => [[zb, ZM - 25], [ZM + 25, 1e5]];   // tramos a ambos lados del montante

// ------------------------------------------------------------------ frente integral
function travesano(S, a, below = true, above = true) {
  for (const [z0, z1] of seg2()) {
    S.prism([[34, a], [114, a], [114, a + 60], [34, a + 60]], 'z', z0, z1, 'alu', [[[37, a + 3], [111, a + 3], [111, a + 57], [37, a + 57]]]);
    S.prism([[114, a + 4], [124, a + 4], [124, a + 56], [114, a + 56], [114, a + 50], [120, a + 50], [120, a + 10], [114, a + 10]], 'z', z0, z1, 'alu2');
    S.box(24, 34, a + 23, a + 37, z0, z1, 'alu');
    const lo = below ? a - 20 : a, hi = above ? a + 80 : a + 60;
    S.box(-12, -2, lo, hi, z0, z1, 'alu');
    S.prism([[-20, lo + 4], [-12, lo], [-12, hi], [-20, hi - 4]], 'z', z0, z1, 'alu2');
    if (below) { S.box(-2, 0, a - 18, a - 6, z0, z1, 'epdm'); S.box(24, 26, a - 18, a - 6, z0, z1, 'epdm'); }
    if (above) { S.box(-2, 0, a + 66, a + 78, z0, z1, 'epdm'); S.box(24, 26, a + 66, a + 78, z0, z1, 'epdm'); }
  }
}
function dvh(S, y0, y1) {
  for (const [z0, z1] of seg2()) {
    S.box(0, 6, y0, y1, z0, z1, 'glass'); S.box(18, 24, y0, y1, z0, z1, 'glass');
    S.box(6, 18, y0, y0 + 14, z0, z1, 'alu'); S.box(6, 18, y1 - 14, y1, z0, z1, 'alu');
  }
}
function montante(S, y0, y1) {
  const v = (z) => -z;
  S.prism([[34, v(ZM + 25)], [114, v(ZM + 25)], [114, v(ZM - 25)], [34, v(ZM - 25)]], 'y', y0, y1, 'alu', [[[37, v(ZM + 22)], [111, v(ZM + 22)], [111, v(ZM - 22)], [37, v(ZM - 22)]]]);
  S.box(114, 124, y0, y1, ZM - 21, ZM + 21, 'alu2', { axis: 'y' });
  S.box(24, 34, y0, y1, ZM - 7, ZM + 7, 'alu', { axis: 'y' });
  S.box(-12, -2, y0, y1, ZM - 22, ZM + 22, 'alu', { axis: 'y' });
  S.prism([[-20, v(ZM + 18)], [-12, v(ZM + 22)], [-12, v(ZM - 22)], [-20, v(ZM - 18)]], 'y', y0, y1, 'alu2');
}
// tubo 80x50x2 soldado (a la viga / columna) + grapa de doble planchuela + bulones M10
function tuboSoldado(S, yc) {
  const v = (z) => -z;
  S.prism([[-(ZM + 25), yc - 40], [-(ZM - 25), yc - 40], [-(ZM - 25), yc + 40], [-(ZM + 25), yc + 40]], 'x', 124, 230, 'steelv',
    [[[-(ZM + 23), yc - 38], [-(ZM - 23), yc - 38], [-(ZM - 23), yc + 38], [-(ZM + 23), yc + 38]]]);
  for (const [za, zb] of [[ZM - 31, ZM - 25], [ZM + 25, ZM + 31]]) S.box(70, 200, yc - 50, yc + 50, za, zb, 'galv');
  for (const xb of [90, 170]) { S.cyl('z', xb, yc, 5, ZM - 36, ZM + 36, 'inox', 14); for (const zz of [ZM - 34, ZM + 34]) S.cyl('z', xb, yc, 9, zz - 3, zz + 3, 'inox', 6); }
  S.box(226, 230, yc - 40, yc + 40, ZM - 27, ZM + 27, 'neo');   // cordón de soldadura
}

// ------------------------------------------------------------------ estructura
function hebCol(S, y0, y1) {
  const v = (z) => -z;
  S.prism([[230, v(-25)], [245, v(-25)], [245, v(-120.5)], [415, v(-120.5)], [415, v(-25)], [430, v(-25)], [430, v(-225)], [415, v(-225)], [415, v(-129.5)],
    [245, v(-129.5)], [245, v(-225)], [230, v(-225)]], 'y', y0, y1, 'steelv');
}
function ipn200(S, yb) {
  const yt = yb + 200, xc = (BX0 + BX1) / 2;
  const P = [[BX0, yb], [BX1, yb], [BX1, yb + 11], [xc + 4, yb + 18], [xc + 4, yt - 18], [BX1, yt - 11], [BX1, yt], [BX0, yt], [BX0, yt - 11], [xc - 4, yt - 18], [xc - 4, yb + 18], [BX0, yb + 11]];
  S.prism(P, 'z', -1e5, 0, 'steel');                                             // módulo entre columnas: viga continua
}
function ipn180(S, yt) {   // viga secundaria perpendicular a la fachada, en el eje de columna, extruida en x
  const u = (z) => -z, yb = yt - 180;
  S.prism([[u(ZM + 41), yb], [u(ZM - 41), yb], [u(ZM - 41), yb + 10], [u(ZM - 3.5), yb + 15], [u(ZM - 3.5), yt - 15], [u(ZM - 41), yt - 10], [u(ZM - 41), yt],
    [u(ZM + 41), yt], [u(ZM + 41), yt - 10], [u(ZM + 3.5), yt - 15], [u(ZM + 3.5), yb + 15], [u(ZM + 41), yb + 10]], 'x', 430, XE, 'steelv');
  S.box(430, 520, yt - 165, yt - 15, ZM + 3.5, ZM + 11, 'galv');                // chapa de unión soldada a la columna
  for (const y of [yt - 130, yt - 90, yt - 50]) { S.cyl('z', 488, y, 7, ZM - 10, ZM + 18, 'inox', 14); S.cyl('z', 488, y, 11, ZM + 11, ZM + 17, 'inox', 6); }
}
function losa(S, yb) {
  const top = yb + 120, x0 = BX0, x1 = XE;
  const prof = [[x0, yb]];
  for (let x = x0 + 20; x < x1; x += 200) prof.push([x, yb], [x + 25, yb + 50], [x + 105, yb + 50], [x + 130, yb]);
  prof.push([x1, yb]);
  S.prism([...prof, [x1, top], [x0, top]], 'z', -1e5, 0, 'pre');
  const sh = prof.map(p => [p[0], p[1] - 0.9]);
  for (let i = 0; i < sh.length - 1; i++) S.sheet([sh[i], sh[i + 1]], 1.6, 'z', -1e5, 0, 'galv');
  S.sheet([[x0 + 30, yb + 95], [x1, yb + 95]], 5, 'z', -1e5, 0, 'red');
  for (let x = x0 + 120; x < x1; x += 150) S.cyl('z', x, yb + 95, 2.5, -1e5, 0.5, 'red', 8);
  for (let x = x0 + 180; x < x1 - 50; x += 600) S.prism([[x - 12, yb + 50], [x + 12, yb + 50], [x + 4, yb + 90], [x - 4, yb + 90]], 'z', -60, -40, 'neo');
  for (const zz of [-12, -237]) for (const x of [262, 288]) { S.cyl('y', x, zz, 5, yb, yb + 80, 'steel', 12); S.cyl('y', x, zz, 9, yb + 72, yb + 80, 'steel', 14); }
  S.sheet([[x0 - 1, yb - 20], [x0 - 1, top], [x0 + 30, top]], 1.6, 'z', -1e5, 0, 'galv');   // zinguería de borde
  return top;
}
function cielorraso(S, y, yfix) {
  S.box(150, XE, y, y + 9.5, -1e5, 0, 'yeso');
  for (let x = 260; x < XE; x += 400) S.prism([[x, y + 9.5], [x + 35, y + 9.5], [x + 35, y + 45], [x, y + 45], [x, y + 42], [x + 32, y + 42], [x + 32, y + 12.5], [x, y + 12.5]], 'z', -1e5, -15, 'galv');
  S.box(150, XE, y + 42, y + 45, -1e5, -15, 'galv', {});
  S.sheet([[150, y + 30], [150, y - 2], [134, y - 2], [134, y - 20]], 1.6, 'z', -1e5, -5, 'galv');                    // Z buña
  S.prism([[150, y + 9.5], [190, y + 9.5], [190, y + 45], [150, y + 45], [150, y + 42], [187, y + 42], [187, y + 12.5], [150, y + 12.5]], 'z', -1e5, -15, 'galv');  // C perimetral
  S.box(150, 153, y + 9.5, y + 45, -1e5, -15, 'neo');
  const yb = { 2400: YE_B, 5380: YR_B }[y];
  S.box(268, 284, y + 45, yb, ZM - 90 - 17, ZM - 90 + 17, 'galv', { axis: 'y' });                                  // cuelgue del C a la viga
  for (const xc of [480, 1100]) {                                                                                    // velas rígidas a losa
    S.prism([[xc - 17, -(-23)], [xc + 17, -(-23)], [xc + 17, -(-57)], [xc - 17, -(-57)], [xc - 17, -(-54)], [xc + 14, -(-54)], [xc + 14, -(-26)], [xc - 17, -(-26)]], 'y', y + 45, yfix - 4, 'galv');
    S.box(xc + 17, xc + 21, yfix - 45, yfix, -57, -23, 'galv'); S.box(xc + 21, xc + 60, yfix - 4, yfix, -57, -23, 'galv');
    S.cyl('y', xc + 45, -40, 3, yfix - 8, yfix + 25, 'inox', 8);
  }
}
function baranda(S, yfl) {
  S.box(290, 390, yfl, yfl + 8, ZM - 50, ZM + 50, 'inox');
  for (const x of [305, 375]) for (const z of [ZM - 35, ZM + 35]) { S.cyl('y', x, z, 5, yfl - 90, yfl + 14, 'steel', 12); S.cyl('y', x, z, 9, yfl + 8, yfl + 16, 'steel', 6); }
  S.cyl('y', 340, ZM, 21, yfl + 8, yfl + 450, 'inox', 32);
  S.cyl('z', 340, yfl + 450, 21, -1e5, 0, 'inox', 32);
}

// ------------------------------------------------------------------ modelo completo
function modelo(S) {
  // ---- terreno, fundación, dado
  S.box(-700, -46, -1700, -200, -1e5, 0, 'tierra'); S.box(700, XE, -1700, -175, -1e5, 0, 'tierra');
  S.box(-700, -46, -200, -100, -1e5, -20, 'hs');                                                 // vereda
  S.box(-46, -40, -620, -20, -1e5, 0, 'memb');                                                   // aislación hidrófuga del dado
  S.box(-470, 1130, -1550, -1500, -1e5, 0, 'hs');
  S.prism([[-420, -1500], [1080, -1500], [1080, -1250], [700, -960], [-40, -960], [-420, -1250]], 'z', -1e5, 0, 'insitu');
  S.prism([[-40, -960], [700, -960], [700, -250], [140, -250], [140, -20], [-40, -20]], 'z', -495, 0, 'insitu');
  for (const x of [0, 660]) S.cyl('y', x, -6, 6, -1450, x > 300 ? -300 : -60, 'red', 10);
  S.sheet([[100, -900], [100, -60], [40, -60]], 10, 'z', -12, -2, 'red');
  // pernos en "J" (los de adelante cortados por el plano), grout, platabanda, tuercas, cartelas
  for (const x of [205, 455]) {
    S.cyl('y', x, 0, 10, -810, -160, 'steel', 20, true);
    S.cyl('y', x, -250, 10, -760, -160, 'steel', 20);
    for (const [ya, yb2, r] of [[-246, -230, 17], [-200, -196, 20], [-196, -180, 17], [-180, -164, 17]]) {
      S.cyl('y', x, 0, r, ya, yb2, ya === -200 ? 'galv' : 'steel', 6, true); S.cyl('y', x, -250, r, ya, yb2, ya === -200 ? 'galv' : 'steel', 6);
    }
  }
  S.box(155, 505, -250, -225, -300, 0, 'grout');
  S.box(155, 505, -225, -200, -300, 0, 'steel');
  for (const [xa, s] of [[230, -1], [430, 1]]) S.prism([[xa, -200], [xa + s * 70, -200], [xa, -100]], 'z', ZM - 6, ZM + 6, 'steelv');
  // ---- piso PB
  S.box(700, XE, -177, -175, -1e5, -30, 'film');
  // sobre el dado el relleno se recorta (z < -150) para ver la platabanda, tuercas y pernos
  S.prism([[700, -177], [XE, -177], [XE, -55], [700, -55]], 'z', -1e5, 0, 'hs');
  S.prism([[140, -250], [700, -250], [700, -55], [140, -55]], 'z', -1e5, -150, 'hs');
  S.box(700, XE, -55, -35, -1e5, -40, 'hid'); S.box(140, 700, -55, -35, -1e5, -190, 'hid');
  S.box(700, XE, -35, -15, -1e5, -80, 'mort'); S.box(140, 700, -35, -15, -1e5, -215, 'mort');
  S.box(700, XE, -15, 0, -1e5, -120, 'porc'); S.box(140, 700, -15, 0, -1e5, -240, 'porc');
  // ---- frente integral: arranque
  S.prism([[-20, -20], [130, -20], [130, 30], [124, 30], [124, -14], [-14, -14], [-14, 30], [-20, 30]], 'z', -1e5, 0, 'alu');
  for (const x of [10, 100]) for (const z of [-60, -190]) { S.cyl('y', x, z, 5, -110, -14, 'steel', 10); S.cyl('y', x, z, 9, -16, -10, 'steel', 6); }
  S.box(130, 140, -20, 0, -1e5, 0, 'seal');
  S.sheet([[-20, 28], [-34, 14], [-60, -6], [-60, -45], [-72, -58]], 2, 'z', -1e5, 0, 'galv');
  S.box(-28, -20, -20, 10, -1e5, 0, 'seal');
  // ---- estructura (los detalles 1 y 2 se toman en un módulo entre columnas; el 3 en el eje de columna)
  if (S.B.y[1] < 1000) hebCol(S, -200, YR_B + 200);
  for (const yb of [YE_B, YR_B]) { ipn200(S, yb); losa(S, yb + 200); }
  cielorraso(S, 2400, YE_B + 200); cielorraso(S, 5380, YR_B + 200);
  // ---- entrepiso
  S.box(BX0, XE, 2960, 2985, -1e5, -60, 'mort');
  S.box(BX0, XE, 2985, 3000, -1e5, -110, 'porc');
  S.sheet([[124, 3000], [190, 3000], [232, 3008], [300, 3008]], 1.6, 'z', -1e5, 0, 'galv');
  S.box(118, 126, 2985, 3006, -1e5, 0, 'seal');
  S.box(190, 227, 2600, 2958, -1e5, 0, 'eps');
  baranda(S, 3000);
  // ---- frente integral
  montante(S, 30, 5800);
  travesano(S, 30, false, true); dvh(S, 90, 2580); travesano(S, 2580);
  for (const [z0, z1] of seg2()) { S.box(-8, 32, 2640, 3040, z0, z1, 'pur'); S.box(-8, -7, 2640, 3040, z0, z1, 'galv'); S.box(31, 32, 2640, 3040, z0, z1, 'galv'); }
  travesano(S, 3040); dvh(S, 3100, 5500); travesano(S, 5500, true, false);
  tuboSoldado(S, 2740); tuboSoldado(S, 5740);
  // ---- cubierta y parapeto
  const yp = (x, b) => b + (x - BX0) * 0.02;
  S.box(BX0, XE, 6000, 6003, -1e5, -20, 'film');
  S.prism([[BX0 + 4, 6003], [XE, 6003], [XE, yp(XE, 6070)], [BX0 + 4, 6070]], 'z', -1e5, -40, 'hl');
  S.prism([[BX0 + 4, 6070], [XE, yp(XE, 6070)], [XE, yp(XE, 6090)], [BX0 + 4, 6090]], 'z', -1e5, -80, 'mort');
  S.prism([[BX0 + 4, 6090], [XE, yp(XE, 6090)], [XE, yp(XE, 6094)], [BX0 + 50, 6094], [BX0 + 8, 6136], [BX0 + 8, 6330], [BX0 + 4, 6330]], 'z', -1e5, -120, 'memb');
  S.sheet([[BX0 + 3, 6000], [BX0 + 3, 6330], [BX0 - 6, 6330]], 2, 'z', -1e5, 0, 'galv'); S.sheet([[BX0 + 3, 6003], [BX0 + 60, 6003]], 2, 'z', -1e5, 0, 'galv');
  const v = (z) => -z;
  S.prism([[130, v(ZM + 50)], [230, v(ZM + 50)], [230, v(ZM - 50)], [130, v(ZM - 50)]], 'y', 5780, 6400, 'steelv', [[[133, v(ZM + 47)], [227, v(ZM + 47)], [227, v(ZM - 47)], [133, v(ZM - 47)]]]);
  S.box(226, 230, 5860, 5880, ZM - 50, ZM + 50, 'neo');
  for (const yc of [5960, 6260]) {
    S.sheet([[130, yc - 40], [55, yc - 40], [55, yc + 40], [130, yc + 40]], 2.5, 'z', -1e5, 0, 'galv');
    for (const z of [ZM - 30, ZM + 30]) S.cyl('x', yc, z, 4, 120, 145, 'inox', 8);
  }
  S.sheet([[30, ZM - 45].map((q, i) => i ? -q : q), [30, -(ZM - 25)], [55, -(ZM - 20)], [55, -(ZM + 20)], [30, -(ZM + 25)], [30, -(ZM + 45)]], 2, 'y', 5880, 6380, 'galv');  // omega
  S.sheet([[-10, 5597], [32, 5597], [32, 5670]], 2.5, 'z', -1e5, 0, 'galv');                                                                    // perfil L/Z inferior
  S.box(-10, 30, 5600, 6400, -1e5, 0, 'pur'); S.box(-10, -9, 5600, 6400, -1e5, 0, 'galv'); S.box(29, 30, 5600, 6400, -1e5, 0, 'galv');
  S.sheet([[30, 5598], [-10, 5598], [-30, 5570], [-30, 5552], [-20, 5560]], 2, 'z', -1e5, 0, 'galv');
  S.box(-12, -2, 5566, 5596, -1e5, 0, 'seal');
  S.sheet([[-28, 6330], [-28, 6405], [245, 6440], [245, 6350], [252, 6340]], 2, 'z', -1e5, 0, 'galv');
  S.box(-10, 230, 6400, 6405, -1e5, 0, 'seal');
}

// ------------------------------------------------------------------ referencias (n, x, y, z)
const ANCH = [
  // cubierta
  [1, 100, 6425, -60], [2, 600, 6094, -125], [3, 600, 6082, -85], [4, 600, 6040, -45], [5, 600, 6001, -22], [10, 233, 6200, -30], [6, 700, 5980, 0], [7, 708, 5945, -50],
  [17, 760, 5880, -40], [8, 262, 5930, -12], [9, 10, 6150, 0], [11, 42, 6300, ZM - 22], [12, 90, 6220, 0], [13, 180, 6300, ZM + 50], [32, -25, 5575, 0],
  [26, 80, 5530, 0], [28, 3, 5450, -20], [27, 118, 5650, ZM + 21], [29, 180, 5740, ZM + 25], [30, 140, 5700, ZM + 31], [14, 275, 5760, 0], 
  [45, 497, 5600, -40], [44, 350, 5385, 0], [46, 142, 5380, 0], [47, 276, 5470, ZM - 73],
  // entrepiso
  [28, 3, 3300, -20], [31, 2, 3115, 0], [26, 80, 3070, 0], [36, 12, 2900, 0], [29, 180, 2740, ZM + 25], [30, 140, 2700, ZM + 31], [27, 118, 2470, ZM + 21],
  [37, 340, 3300, ZM + 21], [38, 340, 3008, ZM + 30], [39, 450, 2995, -110], [3, 450, 2975, -60], [33, 160, 3002, 0], [34, 208, 2800, 0], [18, 229, 2900, 0],
  [6, 450, 2930, 0], [17, 500, 2843, -30], [14, 275, 2700, 0], [45, 497, 2600, -40], [47, 276, 2500, ZM - 73], [44, 350, 2405, 0],
  [46, 142, 2395, 0], [8, 262, 2930, -12],
  // PB
  [16, 430, 120, -100], [26, 80, 60, 0], [31, 135, -8, 0], [35, 60, -5, 0], [33, -50, 0, 0], [48, -300, -100, -60], [49, -43, -300, 0],
  [23, 60, -400, 0], [21, 205, -400, 0], [20, 455, -172, 0], [19, 480, -212, 0], [22, 470, -238, 0], [39, 600, 0, -150], [3, 600, -15, -100], [40, 600, -35, -60],
  [41, 600, -120, 0], [42, 690, -177, -40], [43, 690, -400, 0], [28, 3, 170, -20],
];

export const DETALLES = [
  { n: 1, t: 'D1 · CUBIERTA / FRENTE INTEGRAL', st: 'Axonometría ESC. 1:10 · módulo entre columnas', box: { x: [-40, 510], y: [5400, 6470], z: [ZB, 0] } },
  { n: 2, t: 'D2 · ENTREPISO / FRENTE INTEGRAL', st: 'Axonometría ESC. 1:10 · módulo entre columnas', box: { x: [-40, 510], y: [2390, 3475], z: [ZB, 0] } },
  { n: 3, t: 'D3 · ARRANQUE / DADO ESTRUCTURAL', st: 'Axonometría ESC. 1:10 · eje de columna (corte por línea de pernos)', box: { x: [-400, 850], y: [-500, 200], z: [ZB, 0] } },
];
export function escena(d) {
  const S = new Clipped(d.box);
  modelo(S);
  const { x, y, z } = d.box;
  for (const [n, ax, ay, az] of ANCH) if (ax >= x[0] && ax <= x[1] && ay >= y[0] && ay <= y[1] && az >= z[0] && az <= z[1]) S.anchor(n, ax, ay, az);
  return S;
}
