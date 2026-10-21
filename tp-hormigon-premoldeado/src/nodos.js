// Nudos axonométricos (isométricos) del corte integral final. Misma geometría que src/final_corte.py.
// x+ interior, y+ arriba (mm, ±0,00 = NPT PB), z = 0 plano de corte (hacia el observador).
import { Scene3D, MAT } from './lib3d.js';
Object.assign(MAT, {
  pa: { color: '#3c4650' }, butyl: { color: '#141414' }, silic: { color: '#4a4a4a' }, pvb: { color: '#e4f2f7' },
  epdm: { color: '#202020' }, inox: { color: '#b9bec4' }, pvc: { color: '#7fa7c9' }, prev: { color: '#c3c9cf' },
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
// grapa en el montante, abulonada al riel embutido de la viga L
function grapa(S, yy) {
  for (const sg of [1, -1]) {
    const a = Math.min(ZM + sg * 25, ZM + sg * 35), b = Math.max(ZM + sg * 25, ZM + sg * 35);
    S.box(120, 195, yy - 70, yy + 70, a, b, 'galv');
  }
  S.box(185, 250, yy - 5, yy + 5, ZM - 80, ZM + 80, 'galv');               // ala horizontal hacia la viga
  S.cyl('z', 150, yy + 40, 6, ZM - 40, ZM + 40, 'inox', 14);
  S.cyl('x', yy, ZM, 7, 240, 285, 'inox', 14);                               // bulón T al riel
}
// viga L premoldeada (alma 30 x 90 + ala 20 x 24), extruida en z
function perfilVLdt(yb) {   // VL doble T 40x70
  const yt = yb + 700;
  return [[250, yb], [650, yb], [650, yb + 150], [530, yb + 210], [510, yb + 210], [510, yt - 190], [530, yt - 190], [650, yt - 130], [650, yt],
    [250, yt], [250, yt - 130], [370, yt - 190], [390, yt - 190], [390, yb + 210], [370, yb + 210], [250, yb + 150]];
}
// VL doble T (portante, sobre ménsula) + viga L de borde ENCIMA (alma 15 x 26 hasta tope capa + talón 25 x 15) que recibe el ala del TT
function vigaL(S, yt, z0, z1, ymin = -1e9) {
  const yv = yt - 210, yb = yt - 910;
  if (ymin <= yb) S.prism(perfilVLdt(yb), 'z', z0, z1, 'pre');
  else S.prism(perfilVLdt(yb).map(([x, y]) => [x, Math.max(y, ymin)]).filter((p, i, a) => i === 0 || p[0] !== a[i - 1][0] || p[1] !== a[i - 1][1]), 'z', z0, z1, 'pre');
  S.prism([[250, yv + 8], [650, yv + 8], [650, yt - 60], [400, yt - 60], [400, yt + 50], [250, yt + 50]], 'z', z0, z1, 'pre');   // viga L
  S.box(250, 650, yv, yv + 8, z0, z1, 'grout');   // junta VL / L c/ mortero
  S.prism([[250, yt - 316], [292, yt - 316], [292, yt - 264], [250, yt - 264], [250, yt - 272], [284, yt - 272], [284, yt - 308], [250, yt - 308]], 'z', z0, z1, 'steel');
  if (z1 === 0) {
    for (const x of [290, 450, 610]) S.cyl('z', x, yv - 45, 6, -4, 2, 'red', 12);
    if (ymin <= yb) for (const x of [290, 370, 450, 530, 610]) S.cyl('z', x, yb + 45, 6.4, -4, 2, 'neo', 12);
    for (const x of [330, 520]) S.cyl('y', x, -1, 8, yv - 120, yv + 125, 'red', 10);
    for (const z of [-60, -160]) S.sheet([[320, yt - 150], [320, yt + 25], [640, yt + 25]], 10, 'z', z - 5, z + 5, 'red');
  }
}
function panelTT(S, yt, x1, zb) {
  const yf = yt - 50;
  S.box(420, x1, yf, yt, zb, 0, 'pre');
  S.box(430, 640, yt - 60, yt - 50, zb, 0, 'neo');
  for (const xc of [1170, 2370]) if (xc + 90 <= x1 + 1)
    S.prism([[xc - 90, yf], [xc + 90, yf], [xc + 60, yt - 650], [xc - 60, yt - 650]], 'z', zb, 0, 'pre');
  S.box(400, 420, yt - 60, yt, zb, 0, 'grout');
  for (const y of [yt - 610, yt - 560]) S.cyl('z', 1170, y, 6.4, -4, 2, 'neo', 12);
}
function capa(S, ytop, x1, zb) {
  S.box(400, x1, ytop, ytop + 50, zb, 0, 'insitu');
  sheetZ(S, [[430, ytop + 25], [x1, ytop + 25]], 6);
  for (let x = 500; x < x1; x += 150) S.cyl('z', x, ytop + 25, 3, -3, 2, 'red', 8);
}
// columna + ménsula corta con diagonal (la viga apoya en su extremo)
function columnaMensula(S, ytopM, y0, y1, zc0, zc1) {
  S.box(250, 650, y0, y1, zc0, zc1, 'pre', { axis: 'y' });                  // columna
  // ménsula: perfil en el plano y-z (cara superior, frente y diagonal), extruida en x
  S.prism([[-zc1, ytopM], [-zc1 - 330, ytopM], [-zc1 - 330, ytopM - 160], [-zc1, ytopM - 470]].map(([u, v]) => [u, v]).reverse(), 'x', 250, 650, 'prev');
  S.box(260, 640, ytopM, ytopM + 10, zc1 + 10, zc1 + 320, 'neo');           // banda de neopreno
  for (const xp of [330, 570]) S.cyl('y', xp, zc1 + 165, 10, ytopM - 260, ytopM + 170, 'steel', 14);    // 2 pernos Ø20 (antivuelco)
}

// =============================================================== NUDO 1 · CUBIERTA
export function n1() {
  const S = new Scene3D();
  const Y0 = 7900, X1 = 1265, ZB = -260, yt = 8915;
  vigaL(S, yt, ZB, 0, Y0);
  panelTT(S, yt, X1, ZB);
  capa(S, yt, X1, ZB);
  // cubierta: barrera de vapor + contrapiso liviano H° c/ EPS + carpeta + membrana
  S.box(250, X1, 8965, 8968, ZB, 0, 'film');
  S.prism([[260, 8968], [400, 8968], [400, 9410], [260, 9440]], 'z', ZB, 0, 'insitu');                  // zócalo superior
  for (const z of [-60, -200]) S.sheet([[300, 8870], [300, 9390], [360, 9390], [360, 8870]], 10, 'z', z - 5, z + 5, 'red');
  const sl = (x, b) => b + (x - 400) * 0.02;
  S.prism([[400, 8968], [X1, 8968], [X1, sl(X1, 9068)], [400, 9068]], 'z', ZB, -60, 'eps');
  S.prism([[400, 9068], [X1, sl(X1, 9068)], [X1, sl(X1, 9088)], [400, 9088]], 'z', ZB, -130, 'mort');
  S.prism([[400, 9088], [460, 9088], [400, 9148]], 'z', ZB, -130, 'mort');
  S.prism([[400, 9088], [X1, sl(X1, 9088)], [X1, sl(X1, 9092)], [460, 9092], [404, 9148], [404, 9335], [400, 9335]], 'z', ZB, -190, 'memb');
  S.sheet([[420, 9356], [402, 9356], [402, 9300]], 3, 'z', ZB, -190, 'galv');
  S.sheet([[-50, 9380], [-52, 9400], [-52, 9472], [430, 9452], [430, 9395], [436, 9380]], 3, 'z', ZB, 0, 'galv');
  // muro cortina
  mullion(S, Y0, 9380);
  for (const [z0, z1] of GSEG(ZB)) { S.box(0, 6, Y0, 9380, z0, z1, 'spandrel'); S.box(40, 90, Y0, 9380, z0, z1, 'lana'); S.box(90, 93, Y0, 9380, z0, z1, 'galv'); }
  S.box(-32, 190, 9380, 9420, ZB, 0, 'alu'); S.box(185, 260, 9420, 9440, ZB, 0, 'seal');
  grapa(S, 8625);
  const A = (n, x, y, z) => S.anchor(n, x, y, z);
  A(1, 200, 9465, -100); A(2, 80, 9400, 0); A(3, 700, 9095, -220); A(4, 700, 9080, -130); A(5, 700, 9020, -60); A(6, 410, 9356, -190);
  A(7, 600, 8966, -20); A(8, 330, 9250, 0); A(9, 420, 9105, -130); A(11, 700, 8940, 0); A(12, 455, 8955, -60); A(13, 1170, 8500, 0); A(20, 540, 8858, 0); A(15, 450, 8200, 0);
  A(14, 330, yt - 150, 0);  A(19, 270, 8625, -40); A(31, 110, 9000, ZM + 25); A(34, 3, 8800, 0); A(35, 65, 8700, 0); A(37, 160, 8625, ZM + 35);
  return S;
}

// =============================================================== NUDO 2 · ENTREPISO (corte entre columnas; al fondo la columna con su ménsula)
export function n2() {
  const S = new Scene3D();
  const Y0 = 2950, Y1 = 4520, X1 = 1265, ZB = -420, yt = 4415, ZC = -400;
  columnaMensula(S, 3495, 2700, Y1, -680, ZC);
  vigaL(S, yt, ZC + 10, 0);
  panelTT(S, yt, X1, ZB);
  capa(S, yt, X1, ZB);
  S.box(250, X1, 4465, 4485, ZB, -120, 'mort');
  S.box(260, X1, 4485, 4500, ZB, -220, 'porc');
  // muro cortina: spandrel, lana, bandeja, cortafuego, grapa
  mullion(S, Y0, Y1);
  for (const [z0, z1] of GSEG(ZB)) {
    S.box(0, 6, Y0, Y1, z0, z1, 'spandrel'); S.box(40, 90, Y0, Y1, z0, z1, 'lana'); S.box(90, 93, Y0, Y1, z0, z1, 'galv');
  }
  S.box(93, 250, 4355, 4365, ZB, 0, 'galv'); S.box(93, 250, 4365, 4458, ZB, 0, 'lana'); S.box(93, 250, 4458, 4466, ZB, 0, 'intum');
  S.sheet([[182, 4503], [330, 4503]], 3, 'z', ZB, -120, 'alu');
  grapa(S, 4125);
  const A = (n, x, y, z) => S.anchor(n, x, y, z);
  A(11, 900, 4440, 0); A(12, 455, 4455, -60); A(13, 1170, 4000, 0); A(20, 540, 4358, 0); A(15, 450, 3700, 0); A(14, 330, yt - 150, 0);  A(16, 650, 2900, -700);
  A(17, 450, 3400, -90); A(18, 500, 3500, -200); A(19, 270, 4125, -40); A(26, 900, 4500, -300); A(27, 900, 4475, -200);
  A(31, 110, 4100, ZM + 25); A(34, 3, 3800, 0); A(35, 65, 3600, 0); A(36, 170, 4410, 0); A(37, 160, 4125, ZM + 35);
  return S;
}

// =============================================================== NUDO 3 · PISO SOBRE TERRENO (corte por eje de columna) — sin viga perimetral
export function n3() {
  const S = new Scene3D();
  const Y0 = -760, Y1 = 260, X0 = -300, X1 = 950, ZB = -250;
  // cuello (corte), relleno, columna (medio, cortada por su eje)
  S.box(-75, 175, Y0, -510, -275, 0, 'insitu'); S.box(725, 975, Y0, -510, -275, 0, 'insitu');
  S.box(175, 250, Y0, -510, -275, 0, 'grout'); S.box(650, 725, Y0, -510, -275, 0, 'grout'); S.box(250, 650, Y0, -510, -275, -200, 'grout');
  S.box(250, 650, Y0, Y1, -200, 0, 'pre', { axis: 'y' });
  for (const [xc, xw, sg] of [[250, 175, -1], [650, 725, 1]])
    for (let yy = -790; yy < -560; yy += 115) {
      sheetZ(S, [[xc, yy], [xc + sg * 55, yy], [xc + sg * 55, yy + 38], [xc + sg * 15, yy + 38]], 7);
      sheetZ(S, [[xw, yy + 58], [xw - sg * 55, yy + 58], [xw - sg * 55, yy + 96], [xw - sg * 15, yy + 96]], 7);
    }
  for (const x of [360, 540]) S.cyl('y', x, -1, 8, Y0, -760, 'red', 12);
  // terreno y vereda
  S.box(X0, -76, Y0, -327, ZB, 0, 'tierra'); S.box(-76, 230, -510, -327, ZB, 0, 'tierra');
  S.box(X0, -66, -327, -250, ZB, 0, 'tosca'); S.box(X0, -66, -250, -150, ZB, -120, 'hs'); S.box(-70, -66, -250, -150, ZB, -120, 'seal');
  S.box(975, X1, Y0, -327, ZB, 0, 'tierra'); S.box(670, 975, -510, -327, ZB, 0, 'tierra');
  // piso (dos tramos) separados de la columna por juntas de dilatación
  for (const [xa, xb] of [[-62, 230], [670, X1]]) {
    S.box(xa, xb, -327, -177, ZB, 0, 'tosca'); S.box(xa, xb, -177, -175, ZB, -40, 'film');
    S.box(xa, xb, -175, -55, ZB, -90, 'hs'); S.box(xa, xb, -55, -35, ZB, -140, 'hid');
  }
  S.box(-62, 182, -35, 0, ZB, -190, 'mort'); S.box(182, 230, -35, -15, ZB, -190, 'mort'); S.box(670, X1, -35, -15, ZB, -190, 'mort');
  S.box(185, 230, -15, 0, ZB, -230, 'porc'); S.box(675, X1, -15, 0, ZB, -230, 'porc');
  for (const xa of [230, 650]) { S.box(xa, xa + 20, -327, -10, ZB, 0, 'eps'); S.box(xa, xa + 20, -10, 0, ZB, 0, 'seal'); }
  S.box(-70, -62, -327, -150, ZB, 0, 'memb');
  // babeta + perfil guía de arranque + travesaño + vidrio + montante (colgado del entrepiso)
  S.sheet([[40, 8], [-20, 4], [-68, -12], [-68, -140], [-88, -160]], 3, 'z', ZB, 0, 'galv');
  S.prism([[25, 0], [190, 0], [190, 40], [182, 40], [182, 6], [32, 6], [32, 40], [25, 40]], 'z', ZB, 0, 'alu');
  for (const z of [-60, -200]) S.cyl('y', 100, z, 5, -110, 6, 'steel', 10);
  for (const [z0, z1] of SEG(ZB)) transom(S, 40, z0, z1, false, true);
  for (const [z0, z1] of GSEG(ZB)) dvh(S, 110, Y1, z0, z1);
  mullion(S, 40, Y1);
  S.box(-30, 25, 0, 4, ZB, 0, 'seal');
  const A = (n, x, y, z) => S.anchor(n, x, y, z);
  A(16, 450, 150, -200); A(39, 100, 20, 0); A(40, -5, 2, 0); A(41, 850, 0, -230); A(42, 850, -25, -190);
  A(43, 850, -45, -140); A(44, 850, -120, -90); A(45, 850, -176, -40); A(46, 850, -260, 0); A(47, 240, -250, 0); A(48, 100, -120, 0);
  A(49, 110, 200, ZM + 25); A(50, -68, -60, -150); A(51, -250, -200, -120); A(52, 450, -650, 0); A(53, 690, -700, 0); A(54, 212, -600, 0);
  A(55, 540, -740, 0); A(56, 850, -700, 0); A(60, 900, -600, 0); A(61, 100, -60, -60); A(33, 12, 200, 0);
  return S;
}
