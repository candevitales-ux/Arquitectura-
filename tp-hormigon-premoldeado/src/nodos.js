// Nudos axonométricos (isométricos) del corte integral final. Misma geometría que src/final_corte.py.
// x+ interior, y+ arriba (mm, ±0,00 = NPT PB), z = 0 plano de corte (hacia el observador).
import { Scene3D, MAT } from './lib3d.js';
Object.assign(MAT, {
  pa: { color: '#3c4650' }, butyl: { color: '#141414' }, silic: { color: '#4a4a4a' }, pvb: { color: '#e4f2f7' },
  epdm: { color: '#202020' }, inox: { color: '#b9bec4' }, pvc: { color: '#7fa7c9' },
});
const ZM = -250;   // eje del montante (detrás del plano de corte)
const sheetZ = (S, pts, t = 8, key = 'red') => S.sheet(pts, t, 'z', -1.5, 1.5, key);
const hex = (S, axis, c1, c2, r, w0, w1, key = 'inox') => S.cyl(axis, c1, c2, r, w0, w1, key, 6);

// ---------------------------------------------------------------- muro cortina
function transom(S, a, z0, z1, below = true, above = true) {
  S.prism([[32, a], [150, a], [150, a + 60], [32, a + 60]], 'z', z0, z1, 'alu', [[[36, a + 4], [146, a + 4], [146, a + 56], [36, a + 56]]]);
  S.box(8, 32, a + 22, a + 38, z0, z1, 'alu');
  const lo = below ? a - 22 : a, hi = above ? a + 82 : a + 60;
  S.box(-14, -2, lo, hi, z0, z1, 'alu');
  S.prism([[-30, lo + 4], [-14, lo], [-14, hi], [-30, hi - 4]], 'z', z0, z1, 'alu2');
  if (below) { S.box(-2, 0, a - 20, a - 8, z0, z1, 'epdm'); S.box(25, 32, a - 20, a - 8, z0, z1, 'epdm'); }
  if (above) { S.box(-2, 0, a + 68, a + 80, z0, z1, 'epdm'); S.box(25, 32, a + 68, a + 80, z0, z1, 'epdm'); }
}
function dvh(S, y0, y1, z0, z1) {
  S.box(0, 6, y0, y1, z0, z1, 'glass'); S.box(18, 25, y0, y1, z0, z1, 'glass');
  S.box(6, 18, y0, y0 + 14, z0, z1, 'alu'); S.box(6, 18, y1 - 14, y1, z0, z1, 'alu');
}
function mullion(S, y0, y1) {
  S.prism([[32, -ZM - 25], [182, -ZM - 25], [182, -ZM + 25], [32, -ZM + 25]], 'y', y0, y1, 'alu', [[[36, -ZM - 21], [178, -ZM - 21], [178, -ZM + 21], [36, -ZM + 21]]]);
  S.box(-14, -2, y0, y1, ZM - 22, ZM + 22, 'alu', { axis: 'y' });
  S.prism([[-30, -ZM - 18], [-14, -ZM - 22], [-14, -ZM + 22], [-30, -ZM + 18]], 'y', y0, y1, 'alu2');
}
const SEG = (zb) => [[zb, ZM - 25], [ZM + 25, 0]];
const GSEG = (zb) => [[zb, ZM - 35], [ZM + 35, 0]];
// grapa en el montante, abulonada a la placa de anclaje de la VL
function grapa(S, yy) {
  for (const s of [1, -1]) {
    const a = Math.min(ZM + s * 25, ZM + s * 35), b = Math.max(ZM + s * 25, ZM + s * 35);
    S.box(120, 240, yy - 70, yy + 70, a, b, 'galv');
  }
  S.cyl('z', 150, yy, 6, ZM - 40, ZM + 40, 'inox', 14);
}
// VL doble T 40x70 (perfil del corte)
function perfilVL(yb) {
  const yt = yb + 700;
  return [[250, yb], [650, yb], [650, yb + 150], [530, yb + 210], [510, yb + 210], [510, yt - 190], [530, yt - 190], [650, yt - 130], [650, yt],
    [250, yt], [250, yt - 130], [370, yt - 190], [390, yt - 190], [390, yb + 210], [370, yb + 210], [250, yb + 150]];
}
function armVL(S, yb, ymin = -1e9) {
  const yt = yb + 700;
  for (const x of [290, 370, 450, 530, 610]) if (yb + 45 > ymin) S.cyl('z', x, yb + 45, 6.4, -4, 2, 'neo', 12);
  for (const x of [330, 570]) if (yb + 100 > ymin) S.cyl('z', x, yb + 100, 6.4, -4, 2, 'neo', 12);
  for (const x of [290, 450, 610]) S.cyl('z', x, yt - 45, 6, -4, 2, 'red', 12);
  const y0 = Math.max(yb + 30, ymin + 5);
  sheetZ(S, [[400, y0], [400, yt - 30]], 6); sheetZ(S, [[500, y0], [500, yt - 30]], 6);
  for (const z of [-30, -100]) S.sheet([[420, yt - 80], [420, yt + 40], [480, yt + 40], [480, yt - 80]], 10, 'z', z - 5, z + 5, 'red');
}
function bulonPasante(S, yy, z = -65) {
  S.box(232, 250, yy - 60, yy + 60, z - 60, z + 60, 'steel');          // placa de anclaje
  S.cyl('x', yy, z, 14, 250, 390, 'galv', 16);                           // tubo separador
  S.cyl('x', yy, z, 9.5, 214, 548, 'steel', 16);                         // bulón 3/4"
  S.cyl('x', yy, z, 45, 510, 520, 'galv', 24);                           // arandela Ø90
  hex(S, 'x', yy, z, 18, 520, 542, 'steel'); hex(S, 'x', yy, z, 18, 214, 232, 'steel');
}
function panelTT(S, ytop, x1, zb) {     // flange z zb..0 ; nervio cortado; extremo s/ VP
  S.box(660, x1, ytop - 50, ytop, zb, 0, 'pre');
  S.box(650, 660, ytop - 50, ytop, zb, 0, 'grout');
  if (x1 > 1200) {
    S.prism([[1185, ytop - 50], [Math.min(1365, x1), ytop - 50], [Math.min(1335, x1), ytop - 600], [1215, ytop - 600]], 'z', -150, 0, 'pre');
    for (const y of [ytop - 560, ytop - 500]) S.cyl('z', 1275, y, 6.4, -4, 2, 'neo', 12);
  }
}
function capa(S, ytop, x1, zb) {
  S.box(250, x1, ytop, ytop + 50, zb, 0, 'insitu');
  sheetZ(S, [[280, ytop + 25], [x1, ytop + 25]], 6);
  for (let x = 350; x < x1; x += 150) S.cyl('z', x, ytop + 25, 3, -3, 2, 'red', 8);
}

// =============================================================== NUDO 1 · CUBIERTA
export function n1() {
  const S = new Scene3D();
  const Y0 = 8400, X1 = 900, ZB = -250, yb = 8215;
  // columna (vista, detrás) — termina bajo la VL de cubierta
  // VL de cubierta recortada en Y0 (incluye el alma con el bulón pasante)
  const P = [[250, Y0], [390, Y0], [390, yb + 700 - 190], [370, yb + 700 - 190], [250, yb + 700 - 130], [250, yb + 700], [650, yb + 700], [650, yb + 700 - 130], [530, yb + 700 - 190], [510, yb + 700 - 190], [510, Y0], [390, Y0]];
  S.prism([[390, Y0], [510, Y0], [510, yb + 510], [530, yb + 510], [650, yb + 570], [650, yb + 700], [250, yb + 700], [250, yb + 570], [370, yb + 510], [390, yb + 510]], 'z', ZB, 0, 'pre');
  armVL(S, yb, Y0); bulonPasante(S, yb + 350);
  // panel TT + VP (vista)
  panelTT(S, 8915, X1, ZB);
  S.box(660, X1, Y0, 8865, ZB, -150, 'pre');                             // VP (apoyo de TT)
  capa(S, 8915, X1, ZB);
  // cubierta
  S.box(250, X1, 8965, 8968, ZB, 0, 'film');
  S.prism([[260, 8968], [400, 8968], [400, 9410], [260, 9440]], 'z', ZB, 0, 'insitu');                  // zócalo superior
  for (const z of [-60, -200, -320]) S.sheet([[300, 8870], [300, 9390], [360, 9390], [360, 8870]], 10, 'z', z - 5, z + 5, 'red');
  S.box(400, X1, 8968, 9018, ZB, -60, 'eps');
  const sl = (x, b) => b + (x - 400) * 0.02;
  S.prism([[400, 9018], [X1, 9018], [X1, sl(X1, 9068)], [400, 9068]], 'z', ZB, -120, 'hs');
  S.prism([[400, 9068], [X1, sl(X1, 9068)], [X1, sl(X1, 9088)], [400, 9088]], 'z', ZB, -180, 'mort');
  S.prism([[400, 9088], [460, 9088], [400, 9148]], 'z', ZB, -180, 'mort');
  S.prism([[400, 9088], [X1, sl(X1, 9088)], [X1, sl(X1, 9092)], [460, 9092], [404, 9148], [404, 9335], [400, 9335]], 'z', ZB, -240, 'memb');
  S.sheet([[420, 9356], [402, 9356], [402, 9300]], 3, 'z', ZB, -240, 'galv');
  // cupertina
  S.sheet([[-50, 9380], [-52, 9400], [-52, 9472], [430, 9452], [430, 9395], [436, 9380]], 3, 'z', ZB, 0, 'galv');
  // muro cortina: spandrel, lana, bandeja, cierre superior
  mullion(S, Y0, 9380);
  for (const [z0, z1] of GSEG(ZB)) { S.box(0, 6, Y0, 9380, z0, z1, 'spandrel'); S.box(40, 90, Y0, 9380, z0, z1, 'lana'); S.box(90, 93, Y0, 9380, z0, z1, 'galv'); }
  S.box(-32, 190, 9380, 9420, ZB, 0, 'alu'); S.box(185, 260, 9420, 9440, ZB, 0, 'seal');
  grapa(S, 8565);
  const A = (n, x, y, z) => S.anchor(n, x, y, z);
  A(1, 200, 9465, -100); A(2, 80, 9400, 0); A(3, 700, 9095, -280); A(4, 800, 9088, -200); A(5, 800, 9050, -140); A(6, 800, 8995, -80);
  A(7, 700, 8966, -20); A(8, 330, 9250, 0); A(9, 420, 9105, -190); A(10, 800, 8940, 0); A(11, 420, 8955, -30); A(12, 900, 8890, 0);
  A(13, 450, 8500, 0); A(14, 800, 8600, -150); A(18, 520, 8565, -65); A(25, 110, 9000, ZM + 25); A(28, 3, 8800, 0); A(29, 65, 8700, 0); A(31, 200, 8565, ZM + 35);
  return S;
}

// =============================================================== NUDO 2 · ENTREPISO
export function n2() {
  const S = new Scene3D();
  const Y0 = 3450, Y1 = 4520, X1 = 1000, ZB = -200, yb = 3715;
  // columna en vista (detrás) + ménsula cortada + VL (tramo sobre la ménsula) + VL del otro lado
  S.box(250, 650, Y0, Y1, ZB, -150, 'pre', { axis: 'y' });
  S.box(250, 650, Y0, 3705, -150, 0, 'pre');
  for (const x of [285, 615]) S.cyl('z', x, 3645, 6, -4, 2, 'red', 10);
  sheetZ(S, [[285, 3665], [615, 3665]], 6);
  S.box(250, 650, 3705, 3715, -140, 0, 'neo');
  S.cyl('y', 450, -65, 10, 3505, yb + 140, 'steel', 14);                // perno de fijación
  S.prism(perfilVL(yb), 'z', -130, 0, 'pre');
  armVL(S, yb); bulonPasante(S, yb + 350);
  // VP (vista) + panel TT (nervio cortado) + capa + piso
  S.box(660, X1, Y0, 4365, ZB, -150, 'pre');
  panelTT(S, 4415, X1, ZB);
  capa(S, 4415, X1, ZB);
  S.box(250, X1, 4465, 4485, ZB, -120, 'mort');
  S.box(260, X1, 4485, 4500, ZB, -220, 'porc');
  // cielorraso: gancho al nervio
  // muro cortina: travesaño, spandrel, vidrio, lana, bandeja, cortafuego, grapa
  mullion(S, Y0, Y1);
  for (const [z0, z1] of GSEG(ZB)) {
    S.box(0, 6, Y0, Y1, z0, z1, 'spandrel'); S.box(40, 90, Y0, Y1, z0, z1, 'lana'); S.box(90, 93, Y0, Y1, z0, z1, 'galv');
  }
  S.box(93, 250, 4355, 4365, ZB, 0, 'galv'); S.box(93, 250, 4365, 4458, ZB, 0, 'lana'); S.box(93, 250, 4458, 4466, ZB, 0, 'intum');
  S.sheet([[182, 4503], [330, 4503]], 3, 'z', ZB, -120, 'alu');
  grapa(S, 4065);
  const A = (n, x, y, z) => S.anchor(n, x, y, z);
  A(10, 1000, 4440, 0); A(11, 450, 4455, -30); A(12, 900, 4390, 0); A(13, 450, 3900, 0); A(14, 900, 3800, -150); A(15, 450, 4200, -150);
  A(16, 400, 3650, 0); A(17, 450, 3710, -60); A(18, 520, 4065, -65); A(20, 900, 4500, -300); A(21, 900, 4475, -200);
  A(25, 110, 4100, ZM + 25); A(28, 3, 4000, 0); A(29, 65, 3900, 0); A(30, 170, 4410, 0); A(31, 200, 4065, ZM + 35);
  return S;
}

// =============================================================== NUDO 3 · CERRAMIENTO Y PISO SOBRE TERRENO (corte por eje de columna)
export function n3() {
  const S = new Scene3D();
  const Y0 = -760, Y1 = 260, X0 = -300, X1 = 950, ZB = -250;
  // cuello (corte), relleno, columna (medio, cortada por su eje)
    S.box(-75, 175, Y0, -510, -275, 0, 'insitu'); S.box(725, 975, Y0, -510, -275, 0, 'insitu');
  S.box(175, 250, Y0, -510, -275, 0, 'grout'); S.box(650, 725, Y0, -510, -275, 0, 'grout'); S.box(250, 650, Y0, -510, -275, -200, 'grout');
  S.box(250, 650, Y0, Y1, -200, 0, 'pre', { axis: 'y' });
  // horquillas entrelazadas (sobre la cara de corte)
  for (const [xc, xw, s] of [[250, 175, -1], [650, 725, 1]])
    for (let yy = -790; yy < -560; yy += 115) {
      sheetZ(S, [[xc, yy], [xc + s * 55, yy], [xc + s * 55, yy + 38], [xc + s * 15, yy + 38]], 7);
      sheetZ(S, [[xw, yy + 58], [xw - s * 55, yy + 58], [xw - s * 55, yy + 96], [xw - s * 15, yy + 96]], 7);
    }
  for (const x of [360, 540]) S.cyl('y', x, -1, 8, Y0, -760, 'red', 12);      // armadura de vinculación
  // caño pluvial en la columna (cortado) y salida al interior
  S.box(395, 505, Y0 + 300, Y1, -2, 1, 'pvc');
  S.cyl('x', -385, -60, 55, 505, X1, 'pvc', 20);
  // VPP + neopreno + aislación hidrófuga
  S.box(-50, 250, -510, -500, ZB, 0, 'neo');
  S.prism([[-50, -500], [250, -500], [250, 0], [-20, 0], [-50, -25]], 'z', ZB, 0, 'pre');
  sheetZ(S, [[-15, -470], [215, -470], [215, -35], [-15, -35], [-15, -470]], 6);
  for (const x of [5, 195]) for (const y of [-450, -55]) S.cyl('z', x, y, 6, -4, 2, 'red', 10);
  S.box(-56, -50, -505, -150, ZB, 0, 'memb');
  // terreno, tosca, vereda
  S.box(X0, -56, Y0, -400, ZB, 0, 'tierra');
  S.box(X0, -60, -400, -250, ZB, 0, 'tosca'); S.box(X0, -60, -250, -150, ZB, -120, 'hs'); S.box(-60, -56, -250, -150, ZB, -120, 'seal');
  S.box(975, X1, Y0, -327, ZB, 0, 'tierra');
  // piso interior escalonado
  S.box(650, X1, -327, -177, ZB, 0, 'tosca'); S.box(650, X1, -177, -175, ZB, -60, 'film');
  S.box(670, X1, -175, -55, ZB, -120, 'hs'); S.box(670, X1, -55, -35, ZB, -180, 'hid'); S.box(670, X1, -35, -15, ZB, -230, 'mort');
  S.box(675, X1, -15, 0, ZB, -280, 'porc');
  S.box(650, 670, -175, -10, ZB, -60, 'eps');
  // babeta + arranque + travesaño inferior + vidrio + montante + grapa inferior
  S.sheet([[40, 8], [-20, 4], [-64, -12], [-64, -60], [-84, -80]], 3, 'z', ZB, 0, 'galv');
  S.prism([[25, 0], [190, 0], [190, 40], [182, 40], [182, 6], [32, 6], [32, 40], [25, 40]], 'z', ZB, 0, 'alu');
  for (const [z0, z1] of SEG(ZB)) transom(S, 40, z0, z1, false, true);
  for (const [z0, z1] of GSEG(ZB)) dvh(S, 110, Y1, z0, z1);
  mullion(S, 40, Y1);
  S.box(-30, 25, 0, 4, ZB, 0, 'seal');
  S.box(185, 250, 180, 190, ZM - 120, ZM - 26, 'galv'); S.box(120, 195, 40, 190, ZM - 36, ZM - 26, 'galv');
  const A = (n, x, y, z) => S.anchor(n, x, y, z);
  A(15, 450, 150, -200); A(19, 450, -100, 1); A(33, 100, 20, 0); A(34, -5, 2, 0); A(35, 900, 0, -280); A(36, 900, -25, -230);
  A(37, 900, -45, -180); A(38, 900, -120, -120); A(39, 900, -176, -60); A(40, 900, -260, 0); A(41, 660, -100, -60); A(42, 100, -250, 0);
  A(43, 100, -505, -10); A(44, -64, -40, -150); A(45, -300, -200, -120); A(46, 450, -650, 0); A(47, 690, -700, 0); A(48, 212, -600, 0);
  A(49, 540, -790, 0); A(50, 850, -700, 0); A(54, 900, -600, 0); A(55, 800, -385, -60); A(27, 12, 200, 0);
  return S;
}
