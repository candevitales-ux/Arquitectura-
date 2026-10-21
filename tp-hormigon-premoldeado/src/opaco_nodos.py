# -*- coding: utf-8 -*-
"""Genera build/nodos_opaco.js a partir de src/nodos.js (vidriado): reutiliza la misma estructura (VL doble T + viga L,
panel TT, capa, columna + ménsula, cuello de fundación) y reemplaza el muro cortina por el panel sándwich opaco."""
import os, re
here = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(here, "nodos.js"), encoding="utf-8").read()
base = src[:src.index("// =============================================================== NUDO 1")]
base = base.replace("from './lib3d.js'", "from '/src/lib3d.js'")
base = re.sub(r"\n  S\.prism\(\[\[250, yt - 376\].*?'steel'\);", "", base)          # sin riel de muro cortina en la VL
assert "function vigaL" in base and "function panelTT" in base and "function columnaMensula" in base
OPACO = r'''
// ====================== CERRAMIENTO OPACO: panel sándwich (x 30..230) + fija panel en el alma de la VL
function panelO(S, y0, y1, z0, z1, top = false, bot = false) {
  S.box(30, 90, y0, y1, z0, z1, 'pre'); S.box(150, 230, y0, y1, z0, z1, 'pre');
  const cuts = [bot ? y0 + 60 : y0]; for (const yy of [4140, 8640]) if (yy - 150 > cuts[0] && yy + 150 < (top ? y1 - 60 : y1)) cuts.push(yy - 150, yy + 150);
  cuts.push(top ? y1 - 60 : y1);
  for (let k = 0; k < cuts.length; k += 2) S.box(90, 150, cuts[k], cuts[k + 1], z0, z1, 'eps');
  for (let k = 1; k < cuts.length - 1; k += 2) S.box(90, 150, cuts[k], cuts[k + 1], z0, z1, 'pre');   // zona maciza
  if (top) S.box(90, 150, y1 - 60, y1, z0, z1, 'pre');
  if (bot) S.box(90, 150, y0, y0 + 60, z0, z1, 'pre');
}
// anclaje pasante (Astori): rehundido Ø100 en la cara ext., agujero ovalado por TODO el panel, calce en la junta,
// vaina en el ala superior de la VL, arandela + tuerca del lado interior
function fijaO(S, yy, zc) {
  S.cyl('x', yy, zc, 10, 40, 700, 'inox', 14);
  S.box(60, 68, yy - 40, yy + 40, zc - 40, zc + 40, 'steel'); hex(S, 'x', yy, zc, 17, 44, 60);
  S.box(232, 248, yy - 40, yy + 40, zc - 40, zc + 40, 'neo');
  S.box(650, 660, yy - 40, yy + 40, zc - 40, zc + 40, 'steel'); hex(S, 'x', yy, zc, 18, 660, 682);
}

// =============================================================== NUDO 1 · CUBIERTA
export function n1() {
  const S = new Scene3D();
  const Y0 = 8060, X1 = 1265, ZB = -170, yt = 8915, yv = yt - 210, yl = yt - 60;
  // VL doble T + viga de borde premoldeada (apoyo del ala del TT) + canaleta H° in situ c/ hueco semicircular
  S.prism(perfilVLdt(yt - 910).map(([x, y]) => [x, Math.max(y, Y0)]).filter((p, i, a) => i === 0 || p[0] !== a[i - 1][0] || p[1] !== a[i - 1][1]), 'z', ZB, 0, 'pre');
  S.box(250, 650, yv, yv + 8, ZB, 0, 'grout');
  S.box(250, 650, yv + 8, yl, ZB, 0, 'pre');
  const C = 420, AR = (r) => { const a = []; for (let k = 0; k <= 24; k++) { const t = -k * Math.PI / 24; a.push([C + r * Math.cos(t), 9040 + r * Math.sin(t)]); } return a; };
  S.prism([[250, yl], [560, yl], [560, 9040], ...AR(115), [C - 115, 9150], [250, 9150]], 'z', ZB, 0, 'insitu');
  S.prism([...AR(115), [305, 9150], [330, 9150], ...AR(90).reverse()], 'z', ZB, 0, 'eps');
  S.prism([...AR(90), [330, 9150], [345, 9150], ...AR(75).reverse()], 'z', ZB, -60, 'mort');
  S.box(250, 345, 9150, 9175, ZB, 0, 'eps'); S.box(250, 345, 9175, 9185, ZB, -60, 'mort');
  for (const z of [-60, -200]) S.sheet([[278, yl - 90], [278, 9120]], 10, 'z', z - 5, z + 5, 'red');
  // panel TT (ala s/ viga de borde) + capa
  S.box(580, X1, yt - 50, yt, ZB, 0, 'pre'); S.box(590, 645, yt - 60, yt - 50, ZB, 0, 'neo'); S.box(560, 580, yt - 60, yt, ZB, 0, 'grout');
  S.prism([[1080, yt - 50], [1260, yt - 50], [1230, yt - 650], [1110, yt - 650]], 'z', ZB, 0, 'pre');
  S.box(570, X1, yt, yt + 50, ZB, 0, 'insitu');
  // paquete de cubierta con pendiente hacia la canaleta + membrana continua hasta la babeta del parapeto
  const sl = (x, b) => b + (x - 570) * 0.02;
  S.box(570, X1, 8965, 8968, ZB, 0, 'film');
  S.prism([[570, 8968], [X1, 8968], [X1, sl(X1, 9068)], [630, sl(630, 9068)], [570, 9010]], 'z', ZB, -60, 'eps');
  S.prism([[570, 9010], [630, sl(630, 9068)], [X1, sl(X1, 9068)], [X1, sl(X1, 9088)], [630, sl(630, 9088)], [560, 9040], [570, 9040]], 'z', ZB, -130, 'mort');
  S.sheet([[X1, sl(X1, 9092)], [630, sl(630, 9092)], [560, 9044], ...AR(73), [347, 9188], [234, 9188], [234, 9335]], 4, 'z', ZB, -190, 'memb');
  S.sheet([[214, 9346], [238, 9346], [238, 9290]], 3, 'z', ZB, -190, 'galv');
  panelO(S, Y0, 9440, ZB, 0, true, false);
  S.box(230, 250, Y0, 8855, ZB, 0, 'lana'); S.box(230, 250, 8855, 9185, ZB, 0, 'eps');
  S.sheet([[-2, 9375], [12, 9390], [12, 9472], [248, 9458], [248, 9395], [262, 9380]], 3, 'z', ZB, 0, 'galv');
  S.cyl('y', 130, -130, 4, 9440, 9472, 'inox', 10); hex(S, 'y', 130, -130, 11, 9466, 9474);
  fijaO(S, 8640, -90);
  const A = (n, x, y, z) => S.anchor(n, x, y, z);
  A(1, 20, 9450, -60); A(2, 130, 9474, -130); A(3, 900, 9100, -220); A(4, 900, 9095, -130); A(5, 900, 9030, -60); A(6, 238, 9320, -200);
  A(7, 800, 8966, -20); A(8, 240, 9100, 0); A(9, 420, 8968, -100); A(58, 420, 8935, 0); A(57, 120, 8700, 0); A(10, 900, 8940, 0); A(11, 285, 9060, -60); A(12, 1170, 8500, 0);
  A(19, 600, 8858, 0); A(14, 450, 8200, 0); A(13, 400, 8780, 0); A(25, 60, 9200, 0); A(26, 190, 9000, 0); A(27, 120, 8800, 0);
  A(29, 690, 8640, -90); A(31, 240, 8300, 0);
  return S;
}

// =============================================================== NUDO 2 · ENTREPISO (corte entre columnas; al fondo la columna con su ménsula)
export function n2() {
  const S = new Scene3D();
  const Y0 = 3060, Y1 = 4520, X1 = 1265, ZB = -400, yt = 4415, ZC = -380;
  columnaMensula(S, 3495, Y0, Y1, -580, ZC);
  vigaL(S, yt, ZC + 10, 0);
  panelTT(S, yt, X1, ZB);
  capa(S, yt, X1, ZB);
  S.box(250, X1, 4465, 4485, ZB, -120, 'mort');
  S.box(260, X1, 4485, 4500, ZB, -220, 'porc');
  // panel con junta vertical (fondo de junta + sellador), juntas con la estructura, piso hasta el panel
  panelO(S, Y0, Y1, ZB, -290); panelO(S, Y0, Y1, -270, 0);
  S.box(30, 45, Y0, Y1, -290, -270, 'seal'); S.box(215, 230, Y0, Y1, -290, -270, 'seal'); S.box(45, 215, Y0, Y1, -285, -275, 'lana');
  S.box(230, 250, 3505, 4465, ZB, 0, 'lana');
  S.box(230, 240, 4465, 4500, ZB, 0, 'eps'); S.box(240, 250, 4465, 4485, ZB, -120, 'mort'); S.box(240, 260, 4485, 4500, ZB, -220, 'porc');
  S.box(230, 240, 4500, 4600, ZB, -220, 'porc');
  fijaO(S, 4140, -150);
  const A = (n, x, y, z) => S.anchor(n, x, y, z);
  A(10, 900, 4440, 0); A(11, 455, 4455, -60); A(12, 1170, 4000, 0); A(19, 540, 4358, 0); A(14, 450, 3700, 0); A(13, 330, 4265, 0);
  A(15, 650, 2900, -700); A(16, 450, 3400, -90); A(17, 500, 3508, -200); A(20, 900, 4500, -300); A(21, 900, 4475, -200);
  A(25, 60, 4100, 0); A(26, 190, 3600, 0); A(27, 120, 4300, 0); A(29, 690, 4140, -150); A(31, 240, 4200, 0);
  A(32, 235, 4500, -60); A(33, 230, 3300, -280);
  return S;
}

// =============================================================== NUDO 3 · PISO SOBRE TERRENO (corte por eje de columna) — panel sobre viga portapanel
export function n3() {
  const S = new Scene3D();
  const Y0 = -760, Y1 = 260, X0 = -300, X1 = 950, ZB = -250, ZV = -520;
  S.box(-75, 175, Y0, -510, -275, 0, 'insitu'); S.box(725, 975, Y0, -510, -275, 0, 'insitu');
  S.box(175, 250, Y0, -510, -275, 0, 'grout'); S.box(650, 725, Y0, -510, -275, 0, 'grout'); S.box(250, 650, Y0, -510, -275, -200, 'grout');
  S.box(250, 650, Y0, Y1, -200, 0, 'pre', { axis: 'y' });
  for (const [xc, xw, sg] of [[250, 175, -1], [650, 725, 1]])
    for (let yy = -790; yy < -560; yy += 115) {
      sheetZ(S, [[xc, yy], [xc + sg * 55, yy], [xc + sg * 55, yy + 38], [xc + sg * 15, yy + 38]], 7);
      sheetZ(S, [[xw, yy + 58], [xw - sg * 55, yy + 58], [xw - sg * 55, yy + 96], [xw - sg * 15, yy + 96]], 7);
    }
  // viga portapanel s/ neopreno en el cuello, pintura asfáltica, junta EPS con la columna
  S.box(30, 175, -510, -500, -275, 0, 'neo');
  S.box(30, 230, -500, -50, ZV, 0, 'pre');
  S.box(30, 230, -900, -500, ZV, -285, 'pre');                                       // cuerpo de la viga entre cuellos (h 0,85)
  S.box(26, 30, -900, -160, ZV, 0, 'memb');
  S.box(230, 250, -500, -327, ZB, 0, 'eps');
  // terreno y vereda
  S.box(X0, -76, Y0, -327, ZB, 0, 'tierra'); S.box(-76, 26, -510, -327, ZB, 0, 'tierra');
  S.box(X0, 18, -327, -250, ZB, 0, 'tosca'); S.box(X0, 18, -250, -150, ZB, -120, 'hs'); S.box(18, 26, -250, -150, ZB, -120, 'eps');
  S.box(975, X1, Y0, -327, ZB, 0, 'tierra'); S.box(670, 975, -510, -327, ZB, 0, 'tierra');
  // piso interior separado de la columna por junta de dilatación
  S.box(670, X1, -327, -177, ZB, 0, 'tosca'); S.box(670, X1, -177, -175, ZB, -40, 'film');
  S.box(670, X1, -175, -55, ZB, -90, 'hs'); S.box(670, X1, -55, -35, ZB, -140, 'hid');
  S.box(670, X1, -35, -15, ZB, -190, 'mort'); S.box(675, X1, -15, 0, ZB, -230, 'porc');
  for (const xa of [230, 650]) { S.box(xa, xa + 20, -327, -10, ZB, 0, 'eps'); S.box(xa, xa + 20, -10, 0, ZB, 0, 'seal'); }
  // panel: mortero de asiento + pasador Ø16 en vaina c/ grout + selladores
  panelO(S, -40, Y1, ZV, 0, false, true);
  S.box(30, 230, -50, -40, ZV, 0, 'mort'); S.box(30, 44, -50, -40, ZV, 0, 'seal');
  S.cyl('y', 190, -125, 8, -330, 230, 'steel', 12);
  const A = (n, x, y, z) => S.anchor(n, x, y, z);
  A(15, 450, 150, -200); A(25, 60, 150, 0); A(26, 190, 100, 0); A(27, 120, 200, 0); A(43, 130, -45, 0); A(34, 25, -45, 0);
  A(42, 120, -300, 0); A(44, 28, -400, -100); A(45, -200, -150, -200); A(56, 22, -200, 0); A(55, 90, -505, 0);
  A(35, 850, 0, -230); A(36, 850, -25, -190); A(37, 850, -45, -140); A(38, 850, -120, -90); A(39, 850, -176, -40); A(40, 850, -260, 0);
  A(41, 660, -250, 0); A(46, 450, -650, 0); A(47, 690, -700, 0); A(48, 212, -600, 0); A(49, 540, -740, 0); A(50, 850, -700, 0); A(54, 900, -600, 0);
  return S;
}
'''
os.makedirs("build", exist_ok=True)
open("build/nodos_opaco.js", "w", encoding="utf-8").write(base + OPACO)
print("ok nodos_opaco.js")
