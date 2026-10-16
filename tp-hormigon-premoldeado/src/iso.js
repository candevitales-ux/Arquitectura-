// Lámina 4 – Los mismos 3 detalles de la Lámina 3 en AXONOMETRÍA ISOMÉTRICA.
// Coordenadas del corte integral (mm): x+ interior, y+ arriba, z = 0 plano de corte (hacia el observador).
// Cada modelo se recorta a la ventana del detalle en corte (caras de recorte rayadas).
import { Scene3D, MAT } from './lib3d.js';

Object.assign(MAT, {
  pa: { color: '#3c4650' }, butyl: { color: '#141414' }, silic: { color: '#4a4a4a' }, desic: { color: '#e9e2c3' },
  pvb: { color: '#e4f2f7' }, epdm: { color: '#202020' }, inox: { color: '#b9bec4' }, yeso: { color: '#f2f2f0', hatch: null },
});
const hex = (S, axis, c1, c2, r, w0, w1, key = 'inox') => S.cyl(axis, c1, c2, r, w0, w1, key, 6);
const sheetZ = (S, pts, t = 8, key = 'red') => S.sheet(pts, t, 'z', -1.5, 1.5, key);   // trazo sobre la cara de corte
function arc(cx, cy, r, a0, a1, n = 14) { const p = []; for (let k = 0; k <= n; k++) { const a = (a0 + (a1 - a0) * k / n) * Math.PI / 180; p.push([cx + r * Math.cos(a), cy + r * Math.sin(a)]); } return p; }

// ---------------------------------------------------------------- muro cortina (perfiles de la Lámina 3)
function transom(S, a, z0, z1, below = true, above = true) {
  S.prism([[32, a], [150, a], [150, a + 60], [32, a + 60]], 'z', z0, z1, 'alu',
    [[[34.5, a + 2.5], [89.5, a + 2.5], [89.5, a + 57.5], [34.5, a + 57.5]], [[92, a + 2.5], [147.5, a + 2.5], [147.5, a + 57.5], [92, a + 57.5]]]);
  S.prism([[12, a + 22], [32, a + 22], [32, a + 38], [12, a + 38]], 'z', z0, z1, 'alu', [{ circle: [22, a + 30, 3.2] }]);
  S.box(8, 12, a + 20, a + 40, z0, z1, 'pa');
  const lo = below ? a - 22 : a, hi = above ? a + 82 : a + 60;
  S.box(-16, -4, lo, hi, z0, z1, 'alu');
  S.prism([[-16, lo - 2], [-32, lo + 3], [-32, hi - 3], [-16, hi + 2], [-16, hi - 1], [-29, hi - 5], [-29, lo + 5], [-16, lo + 1]], 'z', z0, z1, 'alu2');
  if (below) { S.box(-4, 0, a - 20, a - 6, z0, z1, 'epdm'); S.box(25, 32, a - 20, a - 6, z0, z1, 'epdm'); }
  if (above) {
    S.box(-4, 0, a + 66, a + 80, z0, z1, 'epdm'); S.box(25, 32, a + 66, a + 80, z0, z1, 'epdm');
    S.box(4, 32, a + 58, a + 62, z0, z1, 'alu');
  }
}
function calzo(S, a, z0, z1) { S.box(3, 23, a + 62, a + 70, z0, z1, 'epdm'); }
function dvh(S, y0, y1, z0, z1, lo = true, hi = true) {
  S.box(0, 6, y0, y1, z0, z1, 'glass'); S.box(18, 21, y0, y1, z0, z1, 'glass'); S.box(21, 21.76, y0, y1, z0, z1, 'pvb'); S.box(21.76, 24.76, y0, y1, z0, z1, 'glass');
  for (const [e, s] of [[y0, 1], [y1, -1]]) {
    if ((s > 0 && !lo) || (s < 0 && !hi)) continue;
    const r = (a, b) => [Math.min(e + s * a, e + s * b), Math.max(e + s * a, e + s * b)];
    let [p, q] = r(0, 5); S.box(6, 18, p, q, z0, z1, 'silic');
    [p, q] = r(5, 14); S.box(6.6, 17.4, p, q, z0, z1, 'alu'); S.box(6, 6.6, p, q, z0, z1, 'butyl'); S.box(17.4, 18, p, q, z0, z1, 'butyl');
  }
}
function mullion(S, zc, y0, y1) {
  S.prism([[32, -zc - 25], [182, -zc - 25], [182, -zc + 25], [32, -zc + 25]], 'y', y0, y1, 'alu',
    [[[34.5, -zc - 22.5], [89.5, -zc - 22.5], [89.5, -zc + 22.5], [34.5, -zc + 22.5]], [[92, -zc - 22.5], [179.5, -zc - 22.5], [179.5, -zc + 22.5], [92, -zc + 22.5]]]);
  S.box(-16, -4, y0, y1, zc - 24, zc + 24, 'alu', { axis: 'y' });
  S.prism([[-16, -zc - 27], [-32, -zc - 24], [-32, -zc + 24], [-16, -zc + 27]], 'y', y0, y1, 'alu2');
}
function vigaPerfil(yb, ycut = null) {
  const yt = yb + 700, c = 15;
  return [[250 + c, yb], [750 - c, yb], [750, yb + c], [750, yb + 330], [550, yb + 330], [550, yt], [250, yt], [250, yb + c]];
}
function armaduraViga(S, yb) {
  const yt = yb + 700;
  sheetZ(S, [[298, yb + 30], [502, yb + 30], [520, yb + 48], [520, yt - 48], [502, yt - 30], [298, yt - 30], [280, yt - 48], [280, yb + 48], [298, yb + 30]], 8);
  sheetZ(S, [[520, yb + 30], [705, yb + 30], [720, yb + 45], [720, yb + 285], [705, yb + 300], [520, yb + 300]], 8);
  for (const x of [310, 400, 490, 610, 690]) S.cyl('z', x, yb + 62, 6.35, -4, 2, 'neo', 12);
  for (const x of [310, 490]) S.cyl('z', x, yb + 128, 6.35, -4, 2, 'neo', 12);
  for (const x of [300, 400, 500]) S.cyl('z', x, yt - 50, 6, -4, 2, 'red', 12);
  for (const y of [yb + 250, yb + 400]) { S.cyl('z', 292, y, 5, -4, 2, 'red', 10); S.cyl('z', 508, y, 5, -4, 2, 'red', 10); }
}
// losa alveolar cortada por un alvéolo en z = 0 (semi-alvéolo en la cara de corte)
function losa(S, yb, x0, x1, zBack) {
  const yt = yb + 300, cy = yb + 150, R = 105;
  const notch = [[0, yb], [-zBack, yb], [-zBack, yt], [0, yt], [0, cy + R], ...arc(0, cy, R, 90, -90).slice(1, -1), [0, cy - R]];
  const holes = []; for (let zc = -225; zc > zBack + 120; zc -= 225) holes.push({ circle: [-zc, cy, R] });
  S.prism(notch, 'x', x0 + 300, x1, 'pre', holes);
  S.prism([[0, yb], [-zBack, yb], [-zBack, yt], [0, yt]], 'x', x0, x0 + 300, 'pre');       // zona de tapones (macizada)
  S.prism([[0, cy + R], ...arc(0, cy, R, 90, -90).slice(1, -1), [0, cy - R]], 'x', x0, x0 + 300, 'hs');
  S.cyl('x', yb + 26, -60, 6.35, x0 + 30, x1, 'neo', 10);                                 // cordón en nervio
}

// =============================================================== DETALLE 1 · COLUMNA – VIGA (corte por el eje del bulón)
export function i1() {
  const S = new Scene3D();
  const yb = 3760, yt = 4460, ZB = -1000, Y0 = 3300, Y1 = 4540, X1 = 900;
  // columna (cara frontal en z = -175; continúa: cortes sup. e inf. rayados)
  S.box(250, 650, Y0, Y1, -575, -175, 'pre', { axis: 'y' });
  // ménsula (cortada por el eje del bulón, z = 0)
  S.box(250, 650, 3450, 3750, -175, 0, 'pre');
  S.prism([[175, 3450], [0, 3450], [175, 3350]], 'x', 250, 650, 'pre');
  S.box(270, 630, 3750, 3760, -165, 0, 'neo');
  // armadura de ménsula sobre la cara de corte
  sheetZ(S, [[280, 3720], [620, 3720]], 10); for (const x of [300, 600]) S.cyl('z', x, 3700, 6, -4, 2, 'red', 10);
  // bulón Ø20 + placa de anclaje (medio bulón: eje en el plano de corte)
  S.box(440, 460, 3420, yt + 25, -10, 0, 'steel'); S.box(420, 480, 3405, 3420, -30, 0, 'steel');
  // viga "L": tramo frontal sobre la ménsula (z -155..0), con vaina y cajeado en la cara de corte
  const P = vigaPerfil(yb);
  S.prism(P, 'z', -155, -25, 'pre');
  S.prism(P, 'z', -25, 0, 'pre', [[[425, yb], [475, yb], [475, yt - 80], [510, yt - 80], [510, yt], [390, yt], [390, yt - 80], [425, yt - 80]].map(p => p)].slice(0, 0));
  // vaina + grout + cajeado (sobre la cara de corte)
  S.box(425, 440, yb, yt - 80, -24, 0.5, 'grout'); S.box(460, 475, yb, yt - 80, -24, 0.5, 'grout');
  S.box(390, 510, yt - 80, yt, -24, 0.5, 'grout');
  S.box(410, 490, yt - 46, yt - 40, -24, 1, 'galv'); S.box(430, 470, yt - 40, yt - 22, -24, 1, 'steel');
  armaduraViga(S, yb);
  sheetZ(S, [[470, yt - 160], [470, yt - 25], [X1, yt - 25]], 8);
  // viga del otro lado de la columna
  S.prism(P, 'z', ZB, -595, 'pre');
  S.box(250, 750, yb, yt, -595, -575, 'grout');
  // riel Halfen embutido (en el eje del montante, z = -600)
  S.prism([[270, yt], [270, yt - 46], [330, yt - 46], [330, yt], [318, yt], [318, yt - 6], [325, yt - 6], [325, yt - 41], [275, yt - 41], [275, yt - 6], [282, yt - 6], [282, yt]], 'z', -150, -20, 'steel');
  // losas, juntas y capa de compresión
  S.box(590, 740, 4090, 4100, -155, 0, 'neo'); S.box(590, 740, 4090, 4100, ZB, -595, 'neo');
  losa(S, 4100, 570, X1, -155);
  S.prism([[155, 4100], [-(ZB), 4100], [-(ZB), 4400], [155, 4400]], 'x', 660, X1, 'pre');   // losa junto a la columna
  S.box(550, 570, 4090, 4400, -155, 0, 'insitu'); S.box(550, 570, 4090, 4400, ZB, -595, 'insitu');
  S.cyl('z', 560, 4250, 5, -155, 2, 'red', 10);
  S.box(550, X1, 4400, yt, -1000, 0, 'insitu');
  sheetZ(S, [[580, 4430], [X1, 4430]], 6); for (let x = 650; x < X1; x += 150) S.cyl('z', x, 4430, 3, -3, 2, 'red', 8);
  // piso escalonado
  S.box(250, X1, yt, yt + 25, ZB, -150, 'mort');
  S.box(260, X1, yt + 25, yt + 30, ZB, -300, 'mort');
  S.box(260, X1, yt + 30, yt + 40, ZB, -300, 'porc');
  // barrera cortafuego (borde de la ventana) y cielorraso
  S.box(185, 250, 4344, 4455, ZB, 0, 'lana'); S.box(185, 250, 4455, 4462, ZB, 0, 'intum');
  S.box(200, X1, 3500, 3512.5, -170, 0, 'yeso'); S.box(660, X1, 3500, 3512.5, ZB, -170, 'yeso');
  S.prism([[810, 3512.5], [865, 3512.5], [855, 3547], [820, 3547]], 'z', ZB, 0, 'galv');

  const A = (n, x, y, z) => S.anchor(n, x, y, z);
  A(1, 450, 3330, -175); A(2, 450, 3600, -100); A(3, 450, 3550, 0); A(4, 300, 3700, 1); A(5, 300, 3755, -80); A(6, 330, 4200, 0);
  A(7, 690, 3822, 2); A(8, 520, 4000, 1); A(9, 432, 4100, 0); A(10, 450, 4430, 1); A(11, 700, 4095, -60); A(12, X1, 4250, -500);
  A(13, 720, 4300, 0); A(14, 560, 4300, 0); A(15, 850, 4430, -50); A(16, 470, 4380, 1); A(17, 700, 4500, -500); A(18, 300, 4458, -80);
  A(19, 820, 3506, -100);
  return S;
}

// =============================================================== DETALLE 3 · VIDRIO – VIGA DE ENTREPISO (montante en z = -300)
export function i3() {
  const S = new Scene3D();
  const yb = 3760, yt = 4460, ZM = -300, ZB = -600, Y0 = 4080, Y1 = 4760, X1 = 640;
  // viga (recortada en Y0: incluye talón y losa)
  const P = vigaPerfil(yb).map(([x, y]) => [Math.min(x, X1), Math.max(y, Y0)]);
  S.prism([[250, Y0], [X1, Y0], [X1, yb + 330], [550, yb + 330], [550, yt], [250, yt]], 'z', ZB, 0, 'pre');
  for (const x of [300, 400, 500]) S.cyl('z', x, yt - 50, 6, -4, 2, 'red', 12);
  sheetZ(S, [[280, Y0], [280, yt - 48], [298, yt - 30], [502, yt - 30], [520, yt - 48], [520, Y0]], 8);
  S.box(590, X1, 4090, 4100, ZB, 0, 'neo');
  losa(S, 4100, 570, X1, ZB);
  S.box(550, 570, 4090, 4400, ZB, 0, 'insitu');
  S.box(570, X1, 4400, yt, ZB, 0, 'insitu');
  S.box(620, X1, yt, yt + 25, ZB, -120, 'mort'); S.box(620, X1, yt + 25, yt + 40, ZB, -240, 'porc');
  // riel Halfen (perfil C) + pernos
  S.prism([[280, yt], [280, yt - 45], [320, yt - 45], [320, yt], [311, yt], [311, yt - 5], [316, yt - 5], [316, yt - 41], [284, yt - 41], [284, yt - 5], [289, yt - 5], [289, yt]], 'z', ZM - 170, ZM + 170, 'steel');
  for (const z of [ZM - 120, ZM + 120]) S.cyl('y', 300, z, 8, yt - 130, yt - 44, 'steel');
  // montante (junta de dilatación a +4,70 con manguito)
  mullion(S, ZM, Y0, 4700); mullion(S, ZM, 4720, Y1);
  S.box(38, 176, 4620, 4760, ZM - 19, ZM + 19, 'alu2', { axis: 'y' });
  // grapas dobles
  for (const s of [1, -1]) {
    const zz = (a, b) => [Math.min(ZM + s * a, ZM + s * b), Math.max(ZM + s * a, ZM + s * b)];
    let [a, b] = zz(25, 30); S.box(115, 200, 4290, yt + 10, a, b, 'neo');
    [a, b] = zz(30, 40); S.box(120, 200, 4290, yt, a, b, 'galv');
    [a, b] = zz(30, 140); S.box(190, 380, yt, yt + 10, a, b, 'galv');
    [a, b] = zz(40, 41.5); S.box(125, 165, 4383, 4397, a, b, 'butyl');
    S.cyl('y', 300, ZM + s * 85, 6, yt - 40, yt + 26, 'inox', 16);
    S.cyl('y', 300, ZM + s * 85, 16, yt + 10, yt + 13, 'inox');
    hex(S, 'y', 300, ZM + s * 85, 11, yt + 13, yt + 26);
    [a, b] = zz(41, 50); hex(S, 'z', 145, 4390, 10, a, b);
  }
  S.cyl('z', 145, 4390, 6, ZM - 52, ZM + 52, 'inox', 16);
  // travesaño, vidrios, spandrel, lana
  for (const [z0, z1] of [[ZB, ZM - 25], [ZM + 25, 0]]) {
    transom(S, 4560, z0, z1); calzo(S, 4560, z0 + 30, z1 - 30 > z0 + 30 ? z0 + 130 : z1);
  }
  for (const [z0, z1] of [[ZB, ZM - 35], [ZM + 35, 0]]) {
    S.box(0, 6, Y0, 4550, z0, z1, 'spandrel');
    S.box(40, 90, Y0, 4550, z0, z1, 'lana'); S.box(90, 92, Y0, 4550, z0, z1, 'galv');
    dvh(S, 4630, Y1, z0, z1, true, false);
  }
  // barrera cortafuego (retirada junto al montante) + ángulo soporte + cubrejunta
  for (const [z0, z1] of [[ZB, ZM - 160], [ZM + 160, 0]]) {
    S.sheet([[93, 4342], [248, 4342], [248, 4280]], 2.5, 'z', z0, z1, 'galv');
    S.box(93, 250, 4344, 4455, z0, z1, 'lana'); S.box(93, 250, 4455, 4462, z0, z1, 'intum');
    S.sheet([[182, 4503], [182, 4500], [330, 4500], [330, 4503]], 2.5, 'z', z0, z1, 'alu');
  }
  const A = (n, x, y, z) => S.anchor(n, x, y, z);
  A(1, 400, 4250, 0); A(2, 300, 4440, ZM - 160); A(3, 300, yt + 26, ZM + 85); A(4, 360, yt + 10, ZM - 100); A(5, 175, 4320, ZM + 40);
  A(6, 145, 4390, ZM + 50); A(7, 115, 4300, ZM + 27); A(8, 110, 4200, ZM + 25); A(9, 100, 4710, ZM + 19); A(10, 60, 4590, 0);
  A(11, -24, 4590, 0); A(12, -2, 4648, 0); A(13, 13, 4626, -30); A(14, 12, 4700, 0); A(15, 3, 4300, 0); A(16, 65, 4300, 0);
  A(17, 220, 4400, 0); A(18, 230, 4459, 0); A(19, 248, 4310, 0); A(20, 300, 4503, -100); A(21, 600, 4480, -300);
  return S;
}

// =============================================================== DETALLE 2 · VIDRIO – MURO (PANEL) (montante en z = -300)
export function i2() {
  const S = new Scene3D();
  const ZM = -300, ZB = -600, Y0 = 8080, Y1 = 8640, X1 = 330;
  // panel sándwich (cortado arriba en Y1), goterón, conectores, inserto
  S.prism([[-40, 8434], [-30, 8434], [-30, 8420], [-16, 8420], [-16, 8434], [-16, 8420], [20, 8420], [20, Y1], [-40, Y1]], 'z', ZB, 0, 'pre');
  S.box(20, 70, 8460, Y1, ZB, 0, 'eps');
  S.prism([[20, 8420], [110, 8420], [110, Y1], [70, Y1], [70, 8460], [20, 8460]], 'z', ZB, 0, 'pre');
  for (const y of [8560]) sheetZ(S, [[5, y], [85, y + 60]], 8);
  sheetZ(S, [[-25, 8470], [-25, Y1]], 5); sheetZ(S, [[95, 8470], [95, Y1]], 5);
  S.cyl('x', 8566, -150, 8, 60, 140, 'steel', 12);
  // cámara: lana + chapa de cierre + perfil L de restricción
  S.box(110, 160, 8460, Y1, ZB, 0, 'lana');
  S.box(110, 250, 8406, 8414, ZB, 0, 'galv');
  S.sheet([[116, 8600], [116, 8525], [250, 8525]], 10, 'z', -200, -100, 'steel');
  // viga de cubierta (recortada en X1 e Y1)
  S.box(250, X1, 8260, Y1, ZB, 0, 'pre');
  for (const y of [8320]) S.cyl('z', 310, y, 6.35, -4, 2, 'neo', 12);
  sheetZ(S, [[280, 8260 + 48], [280, Y1]], 8); sheetZ(S, [[280, 8290], [X1, 8290]], 8);
  S.box(250, X1, 8250, 8260, ZB, 0, 'neo');
  // cielorraso
  S.box(200, X1, 8100, 8112.5, ZB, 0, 'yeso');
  // muro cortina: travesaño superior, vidrio, montante, sellador + fondo de junta
  for (const [z0, z1] of [[ZB, ZM - 25], [ZM + 25, 0]]) transom(S, 8340, z0, z1, true, false);
  for (const [z0, z1] of [[ZB, ZM - 35], [ZM + 35, 0]]) dvh(S, Y0, 8330, z0, z1, false, true);
  mullion(S, ZM, Y0, 8400);
  S.box(-32, 30, 8402, 8420, ZB, 0, 'seal');
  S.cyl('z', 0, 8411, 8, ZB, 1, 'yeso', 16);
  // grapas superiores (dobles) a la cara de la viga
  for (const s of [1, -1]) {
    const zz = (a, b) => [Math.min(ZM + s * a, ZM + s * b), Math.max(ZM + s * a, ZM + s * b)];
    let [a, b] = zz(25, 30); S.box(115, 200, 8270, 8390, a, b, 'neo');
    [a, b] = zz(30, 40); S.box(120, 240, 8270, 8390, a, b, 'galv');
    [a, b] = zz(30, 110); S.box(240, 250, 8270, 8390, a, b, 'galv');
    [a, b] = zz(40, 41.5); S.box(130, 170, 8323, 8337, a, b, 'butyl');
    hex(S, 'x', 8330, ZM + s * 75, 10, 232, 240);
    [a, b] = zz(41, 50); hex(S, 'z', 150, 8330, 10, a, b);
  }
  S.cyl('z', 150, 8330, 6, ZM - 52, ZM + 52, 'inox', 16);
  const A = (n, x, y, z) => S.anchor(n, x, y, z);
  A(1, -10, 8540, 0); A(2, 45, 8590, 1); A(3, -23, 8424, -100); A(4, 0, 8411, 0); A(5, 90, 8370, 0); A(6, 12, 8250, 0);
  A(7, 60, 8220, ZM + 25); A(8, 150, 8330, ZM + 50); A(9, 236, 8330, ZM - 75); A(10, 180, 8410, 0); A(11, 135, 8600, 0);
  A(12, 200, 8525, -150); A(13, 100, 8566, -150); A(14, 300, 8500, 0); A(15, 300, 8106, 0);
  return S;
}
