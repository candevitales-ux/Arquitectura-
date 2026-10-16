// Geometría de los tres nudos (mm reales, mismas cotas que el corte 1:20)
// Eje de columna = eje de fachada (x = 100). La columna (x -100..300) interrumpe el muro cortina;
// la viga "L" corre por detrás (x 300..800) apoyada en ménsulas interiores.
import { Scene3D } from './lib3d.js';

let ZM = -60;                          // eje de montante
let COL = [-850, -450];                // rango z de la columna (det. 1 y 2)
// complemento de intervalos excluidos dentro de [-1700, 0]
function freeSegs(excl) {
  const ex = [...excl].sort((a, b) => a[0] - b[0]); const out = []; let c = -1700;
  for (const [a, b] of ex) { if (a - c > 15) out.push([c, a]); c = Math.max(c, b); }
  if (0 - c > 15) out.push([c, 0]);
  return out;
}
const SEGS = () => freeSegs([[ZM - 25, ZM + 25], [COL[0] - 10, COL[1] + 10]]);
const GSEGS = () => freeSegs([[ZM - 35, ZM + 35], [COL[0] - 15, COL[1] + 15]]);
const WSEGS = () => freeSegs([[COL[0], COL[1]]]);

// ---------------------------------------------------------------- muro cortina
function mullion(S, y0, y1) {
  S.prism([[32, -ZM - 25], [182, -ZM - 25], [182, -ZM + 25], [32, -ZM + 25]], 'y', y0, y1, 'alu',
    [[[36, -ZM - 21], [178, -ZM - 21], [178, -ZM + 21], [36, -ZM + 21]]]);
  S.box(-14, -2, y0, y1, ZM - 22, ZM + 22, 'alu', { axis: 'y' });
  S.prism([[-30, -ZM - 18], [-14, -ZM - 22], [-14, -ZM + 22], [-30, -ZM + 18]], 'y', y0, y1, 'alu2');
}
// perfil de encuentro muro cortina–columna (ángulo alum. + sellador) en ambas caras de la columna
function encuentro(S, y0, y1) {
  for (const zf of [COL[0], COL[1]]) {
    const s = zf === COL[1] ? 1 : -1;
    S.box(-30, 182, y0, y1, zf + s * 0, zf + s * 12, 'alu2');
    S.box(-30, -10, y0, y1, zf + s * 12, zf + s * 16, 'seal');
  }
}
function transom(S, a, opt = {}) {
  const gb = opt.below !== false, ga = opt.above !== false;
  for (const [z0, z1] of SEGS()) {
    S.prism([[32, a], [150, a], [150, a + 60], [32, a + 60]], 'z', z0, z1, 'alu', [[[36, a + 4], [146, a + 4], [146, a + 56], [36, a + 56]]]);
    S.box(8, 32, a + 22, a + 38, z0, z1, 'alu');
    S.box(-14, -2, gb ? a - 22 : a, ga ? a + 82 : a + 60, z0, z1, 'alu');
    S.prism([[-30, gb ? a - 18 : a + 2], [-14, gb ? a - 22 : a], [-14, ga ? a + 82 : a + 60], [-30, ga ? a + 78 : a + 58]], 'z', z0, z1, 'alu2');
    if (gb) { S.box(-2, 0, a - 20, a - 8, z0, z1, 'neo'); S.box(25, 32, a - 20, a - 8, z0, z1, 'neo'); }
    if (ga) { S.box(-2, 0, a + 68, a + 80, z0, z1, 'neo'); S.box(25, 32, a + 68, a + 80, z0, z1, 'neo'); }
  }
}
function glass(S, y0, y1, spandrel = false) {
  for (const [z0, z1] of GSEGS()) {
    if (spandrel) { S.box(0, 6, y0, y1, z0, z1, 'spandrel'); continue; }
    S.box(0, 6, y0, y1, z0, z1, 'glass'); S.box(18, 25, y0, y1, z0, z1, 'glass');
    S.box(6, 18, y0, y0 + 14, z0, z1, 'alu', { edges: false }); S.box(6, 18, y1 - 14, y1, z0, z1, 'alu', { edges: false });
  }
}
// ---------------------------------------------------------------- estructura
function columna(S, y0, y1) { S.box(-100, 300, y0, y1, COL[0], COL[1], 'pre'); }
function mensula(S, ytop) {          // ménsula interior: sale de la cara x = 300 hacia el interior
  S.prism([[300, ytop], [600, ytop], [600, ytop - 200], [300, ytop - 400]], 'z', COL[0], COL[1], 'pre');
  S.box(320, 580, ytop, ytop + 10, COL[0] + 10, COL[1] - 10, 'neo');
}
function vigaL(S, yb) {
  const yt = yb + 700;
  const P = [[300, yb], [800, yb], [800, yb + 330], [600, yb + 330], [600, yt], [300, yt]];
  S.prism(P, 'z', -660, 0, 'pre');          // viga 1 (apoya en media ménsula)
  S.prism(P, 'z', -1700, -640 - 0, 'pre');  // viga 2
  S.box(300, 800, yb, yt - 0, -660, -640, 'grout', { edges: true });
  for (const x of [360, 450, 540, 660, 740]) S.cyl('z', x, yb + 60, 6.5, -5, 3, 'neo', 12);
  for (const x of [360, 540]) S.cyl('z', x, yt - 55, 6, -5, 3, 'red', 12);
}
function losa(S, yb, xEnd = 1800) {
  const yt = yb + 300;
  const prof = (z0, z1) => [[-z1, yb], [-z0, yb], [-z0, yt], [-z1, yt]];
  const cores = (z0, z1) => { const h = []; for (let zc = z1 - 150; zc > z0 + 100; zc -= 225) h.push({ circle: [-zc, yb + 150, 105] }); return h; };
  for (const [z0, z1] of [[-830, 0], [-1700, -850]]) {
    S.prism(prof(z0, z1), 'x', 620, 920, 'pre');                   // tapón de alvéolos
    S.prism(prof(z0, z1), 'x', 920, xEnd, 'pre', cores(z0, z1));
  }
  S.box(640, 790, yb - 10, yb, -1700, 0, 'neo');
  S.box(600, 620, yb - 10, yt, -1700, 0, 'insitu');
  S.box(620, xEnd, yb + 40, yt, -850, -830, 'grout');
}
function bulon(S, yb, zc = -550) {   // bulón Ø20 ménsula-viga con tuerca en cajeado superior
  S.cyl('y', 450, zc, 10, yb - 200, yb + 700 + 25, 'steel');
  S.cyl('y', 450, zc, 38, yb + 700 + 2, yb + 700 + 8, 'galv');
  S.cyl('y', 450, zc, 20, yb + 700 + 8, yb + 700 + 24, 'steel', 6);
}

// =============================================================== DETALLE 1
export function det1() {
  const S = new Scene3D();
  ZM = -60; COL = [-850, -450];
  columna(S, 7820, 8400); mensula(S, 8250); vigaL(S, 8260); losa(S, 8600);
  S.box(620, 1800, 8900, 8960, -1700, 0, 'insitu');
  // paquete de cubierta escalonado
  const xr = 1800;
  S.box(110, xr, 8960, 8964, -1700, -120, 'film');
  S.box(110, xr, 8964, 9014, -1700, -260, 'eps');
  const sl = (x, b) => b + (x - 110) * 0.02;
  S.prism([[110, 9014], [xr, 9014], [xr, sl(xr, 9054)], [110, 9054]], 'z', -1700, -420, 'hs');
  S.prism([[110, 9054], [xr, sl(xr, 9054)], [xr, sl(xr, 9074)], [110, 9074]], 'z', -1700, -580, 'mort');
  S.prism([[114, 9074], [174, 9074], [114, 9134]], 'z', -1700, -580, 'mort');
  S.prism([[114, 9074], [xr, sl(xr, 9074)], [xr, sl(xr, 9079)], [174, 9079], [119, 9134], [119, 9378], [114, 9378]], 'z', -1700, -740, 'memb');
  S.sheet([[132, 9410], [113, 9410], [113, 9330]], 3, 'z', -1700, -740, 'galv');
  S.box(92, 110, 9381, 9399, -1700, -740, 'seal');
  // panel sándwich (dos paneles, junta vertical)
  for (const [z0, z1] of [[-1700, -1260], [-1240, 0]]) {
    S.prism([[-40, 8420], [20, 8420], [20, 9790], [-40, 9800]], 'z', z0, z1, 'pre');
    S.box(20, 70, 8460, 9760, z0, z1, 'eps');
    S.prism([[20, 8420], [110, 8420], [110, 9380], [90, 9380], [90, 9400], [110, 9400], [110, 9782], [20, 9790], [20, 9760], [70, 9760], [70, 8460], [20, 8460]], 'z', z0, z1, 'pre');
  }
  S.box(-40, 110, 8420, 9790, -1260, -1240, 'seal');
  // cupertina
  S.sheet([[-58, 9715], [-62, 9740], [-62, 9822], [128, 9802], [128, 9745], [134, 9728]], 3, 'z', -1700, 0, 'galv');
  // cámara panel-viga
  S.box(110, 160, 8460, 8890, -1700, 0, 'lana');
  S.box(110, 300, 8406, 8414, -1700, 0, 'galv');
  S.box(110, 300, 8900, 8960, -1700, -120, 'insitu');
  // uniones mecánicas panel-viga
  for (const zc of [-300, -1450]) {
    S.sheet([[116, 8862], [116, 8966], [420, 8966]], 10, 'z', zc - 60, zc + 60, 'steel');
    S.cyl('x', 8915, zc, 8, 40, 160, 'galv'); S.cyl('y', 370, zc, 8, 8890, 8990, 'galv');
    S.sheet([[116, 8600], [116, 8525], [300, 8525]], 10, 'z', zc - 50, zc + 50, 'steel');
  }
  // muro cortina: travesaño superior, vidrio, montante y grapa
  mullion(S, 7840, 8400);
  transom(S, 8340, { above: false });
  glass(S, 7840, 8330); encuentro(S, 7840, 8400);
  for (const [z0, z1] of WSEGS()) S.box(-30, 30, 8400, 8420, z0, z1, 'seal');
  S.box(120, 300, 8270, 8390, ZM - 35, ZM - 25, 'steel');
  S.box(290, 300, 8270, 8390, ZM - 130, ZM - 25, 'steel');
  S.cyl('z', 150, 8330, 6, ZM - 45, ZM + 30, 'galv'); S.cyl('x', 8330, ZM - 90, 8, 280, 380, 'galv');
  // cielorraso
  S.box(800, 1800, 8100, 8112, -1700, -250, 'yeso');
  for (const x of [900, 1300, 1700]) S.box(x, x + 35, 8112, 8147, -1700, -250, 'galv');
  S.box(1117, 1135, 8147, 8590, -1300, -1282, 'galv');

  const A = (n, x, y, z) => S.anchor(n, x, y, z);
  A(1, -10, 9300, 0); A(2, 35, 9600, -1250); A(3, 30, 9810, -900); A(4, 1000, 9078, -1100); A(5, 1200, 9070, -650);
  A(6, 1300, 9050, -500); A(7, 1400, 9000, -330); A(8, 1500, 8962, -170); A(9, 1100, 8930, 0); A(10, 1500, 8750, 0);
  A(11, 770, 8820, 0); A(12, 720, 8595, 0); A(13, 450, 8500, 0); A(14, 660, 8320, 3); A(15, 100, 8000, -450);
  A(16, 450, 8150, -450); A(17, 450, 8100, -550); A(18, 300, 8968, -300); A(19, 200, 8525, -300); A(20, 135, 8700, 0);
  A(21, 180, 8930, -120); A(22, 100, 8000, ZM); A(23, 90, 8370, 0); A(24, 3, 8000, -200); A(25, 295, 8350, ZM - 80);
  A(26, 0, 8410, 0); A(27, 1200, 8106, -250); A(28, 130, 9100, -580); A(29, 100, 8200, -438);
  return S;
}
export const REF1 = [
  'Panel sándwich premoldeado (cenefa/parapeto): H°A° 6 + EPS 5 + H°A° 4 cm, conectores inox.',
  'Junta vertical entre paneles 20 mm: fondo de junta + sellador poliuretánico.',
  'Cupertina chapa galv. N°22 plegada c/ goterones; tornillo + sellador.',
  'Membrana asfáltica 4 mm c/ geotextil; babeta en buña + perfil chapa + sellador.',
  'Carpeta cementicia 1:3, e = 2 cm.',
  'H° de pendiente alivianado, mín. 4 cm, pend. 2 % a canaleta.',
  'Aislación térmica EPS 30 kg/m³, e = 5 cm.',
  'Barrera de vapor: imprimación asfáltica + film 200 µ.',
  'Capa de compresión H°A° in situ 6 cm c/ malla Q188.',
  'Losa alveolar pretensada e = 30 cm (alvéolos Ø 21 cm).',
  'Tapón de H° en alvéolos, zona de apoyo (30 cm).',
  'Apoyo de neopreno continuo 10 mm s/ talón de viga.',
  'Viga portante premoldeada pretensada “L” 30/70, talón 20 cm.',
  'Cordones de pretensado Ø 12,7 mm.',
  'Columna premoldeada H°A° 40x40 en el eje de fachada.',
  'Ménsula interior + apoyo de neopreno 10 mm.',
  'Bulón Ø 20 ménsula–viga en vaina grouteada.',
  'Unión mecánica panel–viga: perfil L 100x10 galv., bulón M16 a inserto + anclaje químico.',
  'Perfil L de restricción inferior del panel.',
  'Lana mineral 50 mm en cámara panel–viga.',
  'H° de relleno in situ s/ chapa galv. (cierre de cámara).',
  'Montante de aluminio 50x150.',
  'Travesaño superior 50x120 + presor + tapa + burletes EPDM.',
  'DVH 6 templado + 12 + 3+3 laminado.',
  'Grapa superior montante–viga, anclaje químico M12.',
  'Sellador silicona neutra + fondo de junta (travesaño/panel).',
  'Cielorraso suspendido placa de roca de yeso 12,5 mm s/ perfilería galv.',
  'Media caña de mortero (encuentro losa–parapeto).',
  'Perfil de encuentro muro cortina–columna (ángulo alum. + sellador).',
];

// =============================================================== DETALLE 2
export function det2() {
  const S = new Scene3D();
  ZM = -60; COL = [-850, -450];
  columna(S, 3280, 5000); mensula(S, 3750); vigaL(S, 3760); losa(S, 4100); bulon(S, 3760);
  // capa de compresión escalonada (se retira sobre la viga para ver la unión)
  S.box(620, 1800, 4400, 4460, -1700, -160, 'insitu');
  S.box(300, 620, 4400, 4460, -1700, -870, 'insitu');
  // estribos salientes de la viga (vinculación)
  for (const zc of [-230, -390]) S.sheet([[350, 4420], [350, 4500], [570, 4500], [570, 4420]], 10, 'z', zc - 5, zc + 5, 'red');
  for (const zc of [-230, -390]) S.cyl('x', 4430, zc, 5, 470, 1500, 'red', 10);
  // piso
  S.box(620, 1800, 4460, 4485, -1700, -330, 'mort');
  for (let z = -480; z > -1700; z -= 603) for (let x = 630; x < 1800; x += 603)
    S.box(x, Math.min(x + 600, 1800), 4485, 4500, Math.max(z - 600, -1700), z, 'porc');
  // riel embutido y grapa de anclaje
  S.box(370, 410, 4436, 4461, -410, -20, 'steel');
  S.box(120, 420, 4460, 4470, ZM - 120, ZM - 26, 'galv');
  S.box(120, 195, 4300, 4470, ZM - 36, ZM - 26, 'galv');
  S.cyl('z', 150, 4380, 6, ZM - 46, ZM + 30, 'steel');
  S.cyl('y', 390, ZM - 70, 6, 4430, 4495, 'steel'); S.cyl('y', 390, ZM - 70, 13, 4470, 4482, 'steel', 6);
  // barrera cortafuego + cubrejunta
  for (const [z0, z1] of WSEGS()) {
    S.box(93, 300, 4340, 4350, z0, z1, 'galv');
    S.box(93, 300, 4350, 4455, z0, z1, 'lana');
    S.box(93, 300, 4455, 4462, z0, Math.min(z1, -60), 'intum');
    S.box(40, 90, 3570, 4550, z0, z1, 'lana'); S.box(90, 93, 3570, 4550, z0, z1, 'galv');
    if (z1 < -160) S.sheet([[182, 4503], [330, 4503]], 3, 'z', z0, z1, 'alu');
  }
  encuentro(S, 3300, 5000);
  // muro cortina
  mullion(S, 3300, 4700); mullion(S, 4720, 5000);
  S.box(60, 150, 4620, 4800, ZM - 14, ZM + 14, 'alu2', { edges: true });
  transom(S, 3500); transom(S, 4560);
  glass(S, 3300, 3490); glass(S, 3570, 4550, true); glass(S, 4630, 5000);
  // cielorraso PB
  S.box(800, 1800, 3500, 3512, -1700, -200, 'yeso');
  for (const x of [900, 1300, 1700]) S.box(x, x + 35, 3512, 3547, -1700, -200, 'galv');
  S.box(1117, 1135, 3547, 4090, -1300, -1282, 'galv');

  const A = (n, x, y, z) => S.anchor(n, x, y, z);
  A(1, 100, 4850, -450); A(2, 450, 3600, -450); A(3, 450, 3755, -460); A(4, 450, 4484, -550); A(5, 380, 4100, 0);
  A(6, 450, 3820, 3); A(7, 470, 4500, -230); A(8, 1500, 4250, 0); A(9, 770, 4250, 0); A(10, 710, 4095, 0);
  A(11, 610, 4300, 0); A(12, 1200, 4430, -160); A(13, 1200, 4472, -330); A(14, 1300, 4500, -700); A(15, 390, 4458, -300);
  A(16, 350, 4470, ZM - 100); A(17, 150, 4380, ZM + 30); A(18, 120, 4200, ZM); A(19, 100, 4710, ZM); A(20, 90, 4590, 0);
  A(21, 3, 4000, 0); A(22, 65, 3800, 0); A(23, 170, 4400, 0); A(24, 170, 4459, -60); A(25, 300, 4504, -160);
  A(26, 10, 4850, 0); A(27, 1200, 3506, -200); A(28, 1126, 3800, -1282); A(29, 100, 3400, -438);
  return S;
}
export const REF2 = [
  'Columna premoldeada H°A° 40x40 H-30 (continua en altura).',
  'Ménsula interior de columna (premoldeada con la columna).',
  'Apoyo de neopreno 10 mm (ménsula/viga).',
  'Bulón Ø 20 en vaina, arandela + tuerca en cajeado; llenado c/ grout.',
  'Viga portante premoldeada pretensada “L” 30/70.',
  'Cordones de pretensado Ø 12,7 mm.',
  'Estribos salientes + barras de vinculación Ø 10 c/ 50 cm (diafragma).',
  'Losa alveolar pretensada e = 30 cm.',
  'Tapón de H° en alvéolos de apoyo.',
  'Neopreno continuo losa / talón de viga.',
  'Junta viga–losa llenada c/ H° in situ (llave de corte).',
  'Capa de compresión H°A° in situ 6 cm c/ malla Q188.',
  'Carpeta de nivelación 2,5 cm.',
  'Porcelanato 60x60 s/ adhesivo cementicio.',
  'Riel de anclaje embutido (tipo Halfen) + bulón T M12.',
  'Grapa de anclaje acero galv. regulable 3D (agujeros colisos).',
  'Bulón M12 inox montante–grapa c/ arandelas aislantes (par galvánico).',
  'Montante de aluminio 50x150.',
  'Junta de dilatación de montante 20 mm c/ manguito interior.',
  'Travesaño 50x120 + presor + tapa + burletes EPDM.',
  'Spandrel: vidrio templado 6 mm esmaltado.',
  'Lana mineral 50 mm + bandeja de chapa galv. (back-pan).',
  'Barrera cortafuego: lana mineral 100 kg/m³ s/ chapa galv.',
  'Sellador intumescente (sello de humo y fuego).',
  'Cubrejunta de aluminio.',
  'DVH 6 + 12 + 3+3 laminado (visión).',
  'Cielorraso suspendido placa de roca de yeso 12,5 mm.',
  'Vela rígida galv. colgada de la losa.',
  'Perfil de encuentro muro cortina–columna (ángulo alum. + sellador).',
];

// =============================================================== DETALLE 3
export function det3() {
  const S = new Scene3D();
  ZM = -235; COL = [-200, 10];
  // fundación cortada por el eje de columna (z = 0); todo centrado en x = 100
  S.box(-950, 1150, -2080, -2000, -1100, 0, 'hs');
  S.prism([[-900, -2000], [1100, -2000], [1100, -1650], [600, -1500], [-400, -1500], [-900, -1650]], 'z', -1050, 0, 'insitu');
  for (let x = -800; x <= 1000; x += 150) S.cyl('z', x, -1930, 6, -1000, 3, 'red', 10);
  for (let z = -100; z > -1000; z -= 150) S.cyl('x', -1918, z, 6, -830, 1030, 'red', 10);
  // tintero: pared posterior + paredes laterales
  S.box(-400, 600, -1500, -620, -500, -250, 'insitu');
  S.box(-400, -150, -1500, -620, -250, 0, 'insitu'); S.box(350, 600, -1500, -620, -250, 0, 'insitu');
  S.box(-150, 350, -1500, -1450, -250, 0, 'insitu');
  S.box(-150, -100, -1450, -620, -250, 0, 'grout'); S.box(300, 350, -1450, -620, -250, 0, 'grout');
  S.box(-100, 300, -1450, -1400, -250, 0, 'grout'); S.box(-100, 300, -1400, -620, -250, -200, 'grout');
  // columna (cortada por su eje)
  S.box(-100, 300, -1400, 900, -200, 0, 'pre');
  // viga de fundación premoldeada sobre tintero (centrada en el eje)
  S.box(-50, 250, -620, -610, -480, -230, 'neo');
  S.prism([[-50, -610], [250, -610], [250, 0], [-20, 0], [-50, -20]], 'z', -1700, -220, 'pre');
  for (const x of [-10, 210]) for (const y of [-570, -40]) S.cyl('z', x, y, 6, -225, -217, 'red', 10);
  S.box(-56, -50, -610, -200, -1700, -220, 'memb');
  // suelo y relleno
  S.box(620, 1800, -900, -330, -1700, 0, 'tierra');
  S.box(-1000, -420, -900, -400, -1700, 0, 'tierra');
  // piso sobre terreno (rodea la columna)
  const capa = (y0, y1, zf, key, x0 = 270) => {
    S.box(310, 1800, y0, y1, -1700, zf, key);
    S.box(x0, 310, y0, y1, -1700, Math.min(zf, -220), key);
  };
  capa(-330, -182, 0, 'tosca', 250); capa(-182, -180, -120, 'film', 250); capa(-180, -60, -240, 'insitu');
  capa(-60, -40, -380, 'hid'); capa(-40, -15, -500, 'mort');
  for (let z = -640; z > -1700; z -= 603) for (let x = 313; x < 1800; x += 603)
    S.box(x, Math.min(x + 600, 1800), -15, 0, Math.max(z - 600, -1700), z, 'porc');
  S.box(275, 310, -15, 0, -1700, -640, 'porc');
  S.box(250, 270, -180, -10, -1700, -220, 'eps');
  for (let z = -300; z > -1700; z -= 150) S.cyl('x', -110, z, 3, 320, 1790, 'red', 8);
  // vereda
  S.box(-1000, -110, -400, -300, -1700, 0, 'tosca'); S.box(-1000, -110, -300, -200, -1700, -150, 'hs');
  S.box(-110, -60, -400, -300, -1700, -220, 'tosca'); S.box(-110, -60, -300, -200, -1700, -220, 'hs');
  S.box(-60, -56, -300, -200, -1700, -220, 'seal');
  // babeta
  S.sheet([[40, 8], [-20, 4], [-62, -10], [-62, -60], [-80, -78]], 3, 'z', -1700, -220, 'galv');
  // muro cortina: arranque, travesaño inferior, montante, vidrio, grapa, encuentro con columna
  S.prism([[25, 0], [190, 0], [190, 40], [182, 40], [182, 6], [32, 6], [32, 40], [25, 40]], 'z', -1700, -210, 'alu');
  for (const zc of [-500, -1000, -1500]) S.cyl('y', 100, zc, 5, -140, 10, 'steel');
  transom(S, 40, { below: false });
  mullion(S, 40, 900);
  glass(S, 110, 900);
  S.box(-30, 182, 0, 900, -212, -200, 'alu2'); S.box(-30, -10, 0, 900, -216, -212, 'seal');
  S.box(-30, 25, 0, 4, -1700, -212, 'seal');
  S.box(185, 250, 180, 190, ZM - 120, ZM - 26, 'galv'); S.box(120, 195, 40, 190, ZM - 36, ZM - 26, 'galv');
  S.cyl('z', 150, 120, 6, ZM - 46, ZM + 30, 'steel');

  const A = (n, x, y, z) => S.anchor(n, x, y, z);
  A(1, 1000, -2040, 0); A(2, 900, -1800, 0); A(3, 470, -1100, 0); A(4, -125, -1000, 0); A(5, 100, -300, 0);
  A(6, 100, -300, -220); A(7, 100, -615, -240); A(8, -53, -450, -600); A(9, 1400, -700, 0); A(10, 1400, -250, 0);
  A(11, 1400, -181, -120); A(12, 1400, -120, -240); A(13, 1400, -50, -380); A(14, 1400, -28, -500); A(15, 1400, -7, -700);
  A(16, 260, -100, -220); A(17, -400, -250, -150); A(18, -58, -250, -150); A(19, -62, -30, -220); A(20, 100, 20, -220);
  A(21, 90, 70, -300); A(22, 110, 600, ZM); A(23, 12, 500, -300); A(24, 220, 185, ZM - 70); A(25, -400, -1930, 0);
  A(26, 100, -1425, -100); A(27, 182, 600, -206);
  return S;
}
export const REF3 = [
  'Hormigón de limpieza H-8, e = 8 cm.',
  'Base aislada H°A° in situ H-25 (s/ cálculo y estudio de suelos).',
  'Tintero / cáliz H°A° in situ (empotramiento ≥ 1,5 b).',
  'Grout cementicio sin retracción (llenado columna–tintero).',
  'Columna premoldeada H°A° 40x40 (corte por eje).',
  'Viga de fundación premoldeada H°A° 30x61 (VF).',
  'Apoyo de neopreno 10 mm VF / tintero.',
  'Aislación hidrófuga vertical: pintura asfáltica + film.',
  'Suelo natural compactado.',
  'Tosca compactada e = 15 cm.',
  'Film de polietileno 200 µ.',
  'Contrapiso H°A° e = 12 cm c/ malla Q188.',
  'Carpeta hidrófuga 2 cm.',
  'Carpeta de nivelación 2,5 cm.',
  'Porcelanato 60x60 s/ adhesivo.',
  'Junta perimetral EPS 20 mm + sellador.',
  'Vereda de H° peinado 10 cm s/ tosca.',
  'Junta de vereda c/ sellador.',
  'Babeta chapa galv. N°24 c/ goterón.',
  'Perfil de arranque alum. c/ drenaje + tarugos a VF.',
  'Travesaño inferior + presor + tapa + burletes.',
  'Montante de aluminio 50x150.',
  'DVH 6 + 12 + 3+3 laminado.',
  'Grapa inferior acero galv. (anclaje a VF).',
  'Parrilla de armadura de la base (Ø s/ cálculo).',
  'Fondo de cáliz / asiento de columna c/ grout (5 cm).',
  'Perfil de encuentro muro cortina–columna + sellador.',
];
