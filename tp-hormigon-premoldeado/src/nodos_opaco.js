// Nudos 3D del corte integral OPACO (misma geometría que src/opaco_corte.py).
// x+ interior, y+ arriba (mm, ±0,00 = NPT PB), z = 0 plano de corte (hacia el observador), z− hacia el fondo.
import { Scene3D, MAT } from './lib3d.js';
Object.assign(MAT, {
  inox: { color: '#b9bec4' }, liv: { color: '#eeeeee', hatch: 'mort', bg: '#f1f1f1', period: 140 },
});
const hex = (S, axis, c1, c2, r, w0, w1, key = 'inox') => S.cyl(axis, c1, c2, r, w0, w1, key, 6);

// recorta un polígono por y >= ymin (Sutherland–Hodgman)
function clipY(P, ymin) {
  const out = [];
  for (let i = 0; i < P.length; i++) {
    const a = P[i], b = P[(i + 1) % P.length], ina = a[1] >= ymin, inb = b[1] >= ymin;
    if (ina) out.push(a);
    if (ina !== inb) { const t = (ymin - a[1]) / (b[1] - a[1]); out.push([a[0] + t * (b[0] - a[0]), ymin]); }
  }
  return out;
}
const VP = (yb) => [[0, 0], [400, 0], [400, 130], [260, 190], [260, 520], [400, 580], [400, 700], [0, 700], [0, 580], [140, 520], [140, 190], [0, 130]].map(([x, y]) => [x, yb + y]);

// panel sándwich e = 0,20 (hoja ext. 60 | EPS 60 | hoja int. 80)
function panel(S, y0, y1, z0, z1, top = false, bot = false) {
  S.box(-220, -160, y0, y1, z0, z1, 'pre');
  S.box(-100, -20, y0, y1, z0, z1, 'pre');
  const e0 = bot ? y0 + 60 : y0, e1 = top ? y1 - 60 : y1;
  S.box(-160, -100, e0, e1, z0, z1, 'eps');
  if (top) S.box(-160, -100, y1 - 60, y1, z0, z1, 'pre');
  if (bot) S.box(-160, -100, y0, y0 + 60, z0, z1, 'pre');
}
// fija panel completo (riel + bulón T, 2 ángulos con ovalados, bulón de regulación, bulón M16 pasante en el alma)
function fijaPanel(S, yy, zc) {
  S.box(-50, -20, yy - 20, yy + 20, zc - 160, zc + 160, 'steel');
  S.box(-44, -20, yy - 11, yy + 11, zc - 161, zc + 161, 'neo');                   // ranura del riel
  S.sheet([[-15, yy - 50], [-15, yy + 35], [90, yy + 35]], 10, 'z', zc - 50, zc + 50, 'galv');
  S.sheet([[30, yy + 45], [135, yy + 45], [135, yy + 140]], 10, 'z', zc - 50, zc + 50, 'galv');
  S.cyl('x', yy, zc, 8, -42, -4, 'inox', 14); hex(S, 'x', yy, zc, 15, -10, -2);   // bulón T + tuerca
  S.cyl('y', 60, zc, 8, yy + 15, yy + 72, 'inox', 14); hex(S, 'y', 60, zc, 15, yy + 50, yy + 58); hex(S, 'y', 60, zc, 15, yy + 22, yy + 30);
  S.cyl('x', yy + 90, zc, 8, 118, 292, 'inox', 14); hex(S, 'x', yy + 90, zc, 15, 118, 130); hex(S, 'x', yy + 90, zc, 17, 262, 282);
}
function vigaVP(S, yb, z0, z1, ymin = -1e9) {
  S.prism(clipY(VP(yb), ymin), 'z', z0, z1, 'pre');
  if (z1 === 0) for (const x of [50, 125, 200, 275, 350]) if (yb + 45 > ymin) S.cyl('z', x, yb + 45, 6, -4, 2, 'neo', 12);
}

// =============================================================== NUDO 1 · CUBIERTA
export function n1() {
  const S = new Scene3D();
  const Y0 = 8560, X1 = 600, ZB = -420;
  panel(S, Y0, 10200, ZB, -310, true, false); panel(S, Y0, 10200, -290, 0, true, false);
  S.box(-35, -20, Y0, 10200, -310, -290, 'seal'); S.box(-220, -205, Y0, 10200, -310, -290, 'seal'); S.box(-205, -35, Y0, 10200, -305, -295, 'lana');
  S.box(-38, -20, 9930, 9950, ZB - 1, 1, 'neo');                                     // buña (sellador)
  vigaVP(S, 8310, ZB, 0, Y0);
  S.box(-20, 0, Y0, 9010, ZB, 0, 'lana');
  fijaPanel(S, 8645, -150);
  // panel Pi: losa superior + nervio (el plano de corte pasa entre nervios)
  S.box(200, X1, 9460, 9520, ZB, 0, 'pre');
  S.prism([[270, 9460], [420, 9460], [400, 9020], [290, 9020]], 'x', 200, X1, 'pre');
  S.box(220, 390, 9010, 9020, -410, -280, 'neo');
  // H° in situ: macizado entre nervios + canaleta, estribos salientes de la VP
  S.prism([[0, 9010], [400, 9010], [400, 9460], [200, 9460], [200, 9250], [0, 9250]], 'z', ZB, 0, 'insitu');
  for (const z of [-120, -400]) for (const x of [120, 280]) S.sheet([[x - 40, 8960], [x - 40, 9200], [x + 40, 9200], [x + 40, 8960]], 10, 'z', z - 5, z + 5, 'red');
  S.box(-20, 0, 9010, 9250, ZB, 0, 'eps');
  // paquete de cubierta (escalonado para ver cada capa)
  const sl = (x, b) => b + (x - 200) * 0.02;
  S.box(200, X1, 9520, 9523, ZB, 0, 'film');
  S.box(200, X1, 9523, 9573, ZB, -70, 'eps');
  S.prism([[200, 9573], [X1, 9573], [X1, sl(X1, 9633)], [200, 9633]], 'z', ZB, -150, 'liv');
  S.prism([[200, 9633], [X1, sl(X1, 9633)], [X1, sl(X1, 9653)], [200, 9653]], 'z', ZB, -230, 'mort');
  S.box(-20, 200, 9250, 9270, ZB, 0, 'mort'); S.box(185, 200, 9270, 9633, ZB, -150, 'mort');
  S.prism([[185, 9270], [145, 9270], [185, 9310]], 'z', ZB, 0, 'mort'); S.prism([[-20, 9270], [20, 9270], [-20, 9310]], 'z', ZB, 0, 'mort');
  S.sheet([[X1, sl(X1, 9656)], [200, 9656], [181, 9637], [181, 9312], [143, 9274], [22, 9274], [-16, 9312], [-16, 9890]], 4, 'z', ZB, -310, 'memb');
  S.sheet([[-30, 9940], [-26, 9940], [-11, 9925], [-11, 9860]], 3, 'z', ZB, -310, 'galv');
  // cupertina + tornillos
  S.sheet([[-262, 10095], [-245, 10112], [-245, 10222], [8, 10210], [8, 10112], [25, 10095]], 3, 'z', ZB, 0, 'galv');
  for (const z of [-150, -420]) { S.cyl('y', -110, z, 4, 10150, 10226, 'inox', 10); hex(S, 'y', -110, z, 11, 10224, 10232); }
  const A = (n, x, y, z) => S.anchor(n, x, y, z);
  A(1, -245, 10170, 0); A(2, -110, 10230, -420); A(3, -11, 9900, -400); A(4, 600, 9660, -400); A(5, 600, 9650, -260);
  A(6, 600, 9620, -170); A(7, 600, 9560, -50); A(8, 630, 9521, 0); A(9, 640, 9250, -300); A(10, 80, 9275, -150); A(11, 170, 9280, 0);
  A(12, 120, 9150, 0); A(14, -10, 9150, 0); A(15, 330, 8800, 0); A(22, -190, 9500, 0); A(23, -130, 9700, 0);
  A(24, -60, 9300, 0); A(26, 40, 8680, -150); A(27, 285, 8735, -150); A(28, -10, 8800, 0); A(59, -20, 9950, -300);
  return S;
}

// =============================================================== NUDO 2 · ENTREPISO (corte por eje de columna; detrás, el tramo entre columnas)
export function n2() {
  const S = new Scene3D();
  const Y0 = 3230, Y1 = 4600, X1 = 760, ZB = -700, ZC = -200;
  panel(S, Y0, Y1, ZB, 0);
  S.box(-20, 0, 3345, 4355, ZB, 0, 'lana'); S.box(-20, 0, Y0, 3345, ZC - 20, 0, 'lana');
  // columna (mitad, cortada por su eje) + ménsula interior cortada (apoyo del recorte de losa) + ménsula lateral (apoyo VP)
  S.box(0, 400, Y0, Y1, ZC, 0, 'pre');
  S.prism([[400, 4045], [600, 4045], [600, 3795], [400, 3595]], 'z', ZC, 0, 'pre');
  S.box(420, 590, 4045, 4055, ZC + 10, 0, 'neo');
  S.cyl('y', 510, -100, 9, 3800, 4250, 'steel', 12);                                   // pasador Ø16 del recorte
  S.prism([[-ZC, 3335], [-ZC + 200, 3335], [-ZC + 200, Y0], [-ZC, Y0]], 'x', 0, 400, 'pre');
  S.box(10, 390, 3335, 3345, ZC - 200, ZC - 10, 'neo');
  // viga VP-70 entre columnas (apoya en la ménsula lateral), fija panel en su alma
  vigaVP(S, 3345, ZB, ZC - 10, Y0);
  S.box(100, 390, 4045, 4055, ZB, ZC - 10, 'neo');
  fijaPanel(S, 3680, -520);
  // losa alveolar con RECORTE alrededor de la columna: el diente apoya en la ménsula interior; hueco relleno con H° in situ
  const ends = { capa: X1, liv: X1 - 70, mort: X1 - 140, porc: X1 - 210 };
  S.box(420, X1, 4055, 4355, ZC - 20, 0, 'pre');
  S.box(10, X1, 4055, 4355, ZB, ZC - 20, 'pre');
  for (const z of [-60, -180, -300, -420, -540]) S.cyl('x', 4205, z, 42, z > ZC - 20 ? 520 : 170, X1 + 1, 'neo', 20);
  S.box(400, 420, 4055, 4355, ZC - 20, 0, 'grout'); S.box(10, 420, 4055, 4355, ZC - 20, ZC, 'grout');
  // capa de compresión y piso (alrededor de la columna y hasta el panel), juntas
  const lay = (y0, y1, key, xe) => { S.box(420, xe, y0, y1, ZC - 20, 0, key); S.box(-10, xe, y0, y1, ZB, ZC - 20, key); };
  lay(4355, 4405, 'insitu', ends.capa); lay(4405, 4465, 'liv', ends.liv); lay(4465, 4485, 'mort', ends.mort); lay(4485, 4500, 'porc', ends.porc);
  S.box(400, 420, 4355, 4500, ZC - 20, 0, 'eps'); S.box(0, 420, 4355, 4500, ZC - 20, ZC, 'eps');
  S.box(-20, -10, 4355, 4500, ZB, ZC - 20, 'eps'); S.box(-20, -10, 4500, 4600, ZB, ZC - 20, 'porc');
  // cielorraso suspendido (rodea columna y ménsula)
  S.box(420, X1, 3250, 3262, ZC - 220, 0, 'yeso'); S.box(-8, X1, 3250, 3262, ZB, ZC - 220, 'yeso');
  S.box(633, 667, 3262, 3297, ZB, 0, 'galv');
  S.cyl('y', 650, -100, 5, 3297, 4055, 'galv', 10);
  const A = (n, x, y, z) => S.anchor(n, x, y, z);
  A(30, ends.porc - 80, 4500, -500); A(31, ends.mort - 40, 4485, -500); A(32, ends.liv - 40, 4465, -500); A(20, ends.capa - 30, 4405, -500);
  A(19, 700, 4200, 0); A(18, 520, 3900, 0); A(13, 510, 4050, 0); A(53, 410, 4250, 0); A(16, 200, 3500, 0); A(22, -190, 3500, 0);
  A(23, -130, 3600, 0); A(24, -60, 3700, 0); A(28, -10, 3900, 0); A(29, -15, 4560, -650); A(33, 700, 3256, 0); A(34, 650, 3700, -100);
  A(21, 300, 4050, -650);
  return S;
}

// =============================================================== NUDO 3 · PISO S/ TERRENO Y FUNDACIÓN (corte por eje de columna)
export function n3() {
  const S = new Scene3D();
  const YB = -900, Y1 = 300, X0 = -400, X1 = 720, ZB = -520, ZK = -450, ZH = -250;
  // cáliz: paredes (perfil x-y con dientes) + pared del fondo
  const teeth = (x, ya, yb, s) => { const p = []; for (let y = ya; y < yb - 1; y += 100) p.push([x, y], [x + s * 15, y + 25], [x + s * 15, y + 75], [x, y + 100]); return p; };
  const L = [[-250, YB], [-50, YB], ...teeth(-50, YB, -650, 1).filter(q => q[1] > YB && q[1] < -650), [-50, -650], [-250, -650]];
  const R = [[450, YB], [650, YB], [650, -650], [450, -650], ...teeth(450, YB, -650, -1).filter(q => q[1] > YB && q[1] < -650).reverse()];
  S.prism(L, 'z', ZH, 0, 'insitu'); S.prism(R, 'z', ZH, 0, 'insitu');
  S.box(-250, 650, YB, -650, ZK, ZH, 'insitu');
  S.box(-50, 0, YB, -650, ZH, 0, 'grout'); S.box(400, 450, YB, -650, ZH, 0, 'grout'); S.box(-50, 450, YB, -650, ZH, -200, 'grout');
  // columna (mitad, cortada por su eje)
  S.box(0, 400, YB, Y1, -200, 0, 'pre');
  // viga portapanel s/ neopreno, junta EPS con la columna, pintura asfáltica
  S.box(-245, -50, -650, -640, ZK, 0, 'neo');
  S.prism([[-245, -640], [-20, -640], [-20, -50], [-220, -50], [-245, -75]], 'z', ZB, 0, 'pre');
  S.box(-20, 0, -640, -50, ZB, 0, 'eps');
  S.box(-249, -245, -640, -205, ZB, 0, 'memb');
  // panel: mortero de asiento + calces, pasador en vaina, sellador exterior
  panel(S, -40, Y1, ZB, 0, false, true);
  S.box(-220, -20, -50, -40, ZB, 0, 'mort');
  S.box(-232, -219, -52, -38, ZB, 0, 'seal');
  S.cyl('y', -60, -350, 8, -330, 230, 'steel', 12);
  S.box(-20, 0, -50, 0, ZB, 0, 'seal');
  // vereda y su contrapiso de tosca, junta
  S.box(X0, -255, -380, -280, ZB, 0, 'tosca'); S.box(X0, -255, -280, -200, ZB, -60, 'hs');
  S.box(-255, -249, -280, -200, ZB, 0, 'eps');
  // piso interior (rodea la columna y llega al panel detrás de ella), junta EPS perimetral
  const floor = (y0, y1, key, zf) => { if (zf > -220) S.box(420, X1, y0, y1, -220, zf, key); S.box(0, X1, y0, y1, ZB, Math.min(-220, zf), key); };
  S.box(420, X1, -420, -157, -220, 0, 'tosca'); S.box(0, X1, -640, -157, ZB, -220, 'tosca');
  floor(-157, -155, 'film', 0); floor(-155, -35, 'hs', 0); floor(-35, -15, 'hid', -60); floor(-15, 0, 'porc', -130);
  S.box(400, 420, -420, 0, -220, 0, 'eps'); S.box(0, 420, -420, 0, -220, -200, 'eps');
  const A = (n, x, y, z) => S.anchor(n, x, y, z);
  A(22, -190, 200, 0); A(23, -130, 250, 0); A(24, -60, 150, 0); A(42, -150, -45, 0); A(44, -130, -350, 0); A(45, -150, -645, 0);
  A(46, -226, -45, 0); A(47, -247, -450, 0); A(48, -350, -200, -300); A(49, -350, -330, 0); A(50, -252, -240, 0); A(51, 200, -500, 0);
  A(52, -150, -800, 0); A(53, 425, -800, 0); A(60, -10, -400, 0); A(36, 600, 0, -350); A(37, 700, -25, -60); A(38, 700, -95, 0);
  A(39, 700, -156, 0); A(40, 700, -300, 0); A(41, 410, -200, 0);
  return S;
}
