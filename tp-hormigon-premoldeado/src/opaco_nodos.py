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
  S.box(90, 150, bot ? y0 + 60 : y0, top ? y1 - 60 : y1, z0, z1, 'eps');
  if (top) S.box(90, 150, y1 - 60, y1, z0, z1, 'pre');
  if (bot) S.box(90, 150, y0, y0 + 60, z0, z1, 'pre');
}
function fijaO(S, yy, zc) {
  S.box(200, 230, yy - 20, yy + 20, zc - 90, zc + 90, 'steel');
  S.sheet([[235, yy - 50], [235, yy + 35], [340, yy + 35]], 10, 'z', zc - 50, zc + 50, 'galv');
  S.sheet([[280, yy + 45], [385, yy + 45], [385, yy + 140]], 10, 'z', zc - 50, zc + 50, 'galv');
  S.cyl('x', yy, zc, 8, 208, 246, 'inox', 14); hex(S, 'x', yy, zc, 15, 240, 248);
  S.cyl('y', 310, zc, 8, yy + 15, yy + 72, 'inox', 14); hex(S, 'y', 310, zc, 15, yy + 50, yy + 58);
  S.cyl('x', yy + 90, zc, 8, 368, 542, 'inox', 14); hex(S, 'x', yy + 90, zc, 15, 368, 380); hex(S, 'x', yy + 90, zc, 17, 512, 532);
}

// =============================================================== NUDO 1 · CUBIERTA
export function n1() {
  const S = new Scene3D();
  const Y0 = 7900, X1 = 1265, ZB = -260, yt = 8915;
  vigaL(S, yt, ZB, 0, Y0);
  panelTT(S, yt, X1, ZB);
  capa(S, yt, X1, ZB);
  S.box(240, X1, 8965, 8968, ZB, 0, 'film');
  S.box(230, 240, 8965, 9100, ZB, 0, 'eps');
  const sl = (x, b) => b + (x - 240) * 0.02;
  S.prism([[240, 8968], [X1, 8968], [X1, sl(X1, 9068)], [240, 9068]], 'z', ZB, -60, 'eps');
  S.prism([[240, 9068], [X1, sl(X1, 9068)], [X1, sl(X1, 9088)], [240, 9088]], 'z', ZB, -130, 'mort');
  S.prism([[240, 9088], [300, 9088], [240, 9148]], 'z', ZB, -130, 'mort');
  S.sheet([[X1, sl(X1, 9092)], [300, 9092], [234, 9150], [234, 9335]], 4, 'z', ZB, -190, 'memb');
  S.sheet([[214, 9346], [238, 9346], [238, 9290]], 3, 'z', ZB, -190, 'galv');
  panelO(S, Y0, 9440, ZB, 0, true, false);
  S.box(230, 250, Y0, 8965, ZB, 0, 'lana');
  S.sheet([[-2, 9375], [12, 9390], [12, 9472], [248, 9458], [248, 9395], [262, 9380]], 3, 'z', ZB, 0, 'galv');
  S.cyl('y', 130, -130, 4, 9440, 9472, 'inox', 10); hex(S, 'y', 130, -130, 11, 9466, 9474);
  fijaO(S, 8300, -150);
  const A = (n, x, y, z) => S.anchor(n, x, y, z);
  A(1, 20, 9450, -60); A(2, 130, 9474, -130); A(3, 700, 9095, -220); A(4, 700, 9080, -130); A(5, 700, 9020, -60); A(6, 238, 9320, -200);
  A(7, 600, 8966, -20); A(8, 235, 9050, 0); A(9, 255, 9100, -130); A(10, 700, 8940, 0); A(11, 455, 8955, -60); A(12, 1170, 8500, 0);
  A(19, 540, 8858, 0); A(14, 450, 8200, 0); A(13, 330, 8765, 0); A(25, 60, 9200, 0); A(26, 190, 9000, 0); A(27, 120, 8800, 0);
  A(29, 300, 8340, -150); A(30, 450, 8390, -150); A(31, 240, 8500, 0);
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
  // panel con junta vertical (fondo de junta + sellador), juntas con la estructura, piso hasta el panel
  panelO(S, Y0, Y1, ZB, -290); panelO(S, Y0, Y1, -270, 0);
  S.box(30, 45, Y0, Y1, -290, -270, 'seal'); S.box(215, 230, Y0, Y1, -290, -270, 'seal'); S.box(45, 215, Y0, Y1, -285, -275, 'lana');
  S.box(230, 250, 3505, 4465, ZB, 0, 'lana');
  S.box(230, 240, 4465, 4500, ZB, 0, 'eps'); S.box(240, 250, 4465, 4485, ZB, -120, 'mort'); S.box(240, 260, 4485, 4500, ZB, -220, 'porc');
  S.box(230, 240, 4500, 4600, ZB, -220, 'porc');
  fijaO(S, 3800, -150);
  const A = (n, x, y, z) => S.anchor(n, x, y, z);
  A(10, 900, 4440, 0); A(11, 455, 4455, -60); A(12, 1170, 4000, 0); A(19, 540, 4358, 0); A(14, 450, 3700, 0); A(13, 330, 4265, 0);
  A(15, 650, 2900, -700); A(16, 450, 3400, -90); A(17, 500, 3508, -200); A(20, 900, 4500, -300); A(21, 900, 4475, -200);
  A(25, 60, 4100, 0); A(26, 190, 3600, 0); A(27, 120, 4300, 0); A(29, 300, 3840, -150); A(30, 450, 3890, -150); A(31, 240, 4200, 0);
  A(32, 235, 4500, -60); A(33, 230, 3300, -280);
  return S;
}

// =============================================================== NUDO 3 · PISO SOBRE TERRENO (corte por eje de columna) — panel sobre viga portapanel
export function n3() {
  const S = new Scene3D();
  const Y0 = -760, Y1 = 260, X0 = -300, X1 = 950, ZB = -250;
  S.box(-75, 175, Y0, -510, -275, 0, 'insitu'); S.box(725, 975, Y0, -510, -275, 0, 'insitu');
  S.box(175, 250, Y0, -510, -275, 0, 'grout'); S.box(650, 725, Y0, -510, -275, 0, 'grout'); S.box(250, 650, Y0, -510, -275, -200, 'grout');
  S.box(250, 650, Y0, Y1, -200, 0, 'pre', { axis: 'y' });
  for (const [xc, xw, sg] of [[250, 175, -1], [650, 725, 1]])
    for (let yy = -790; yy < -560; yy += 115) {
      sheetZ(S, [[xc, yy], [xc + sg * 55, yy], [xc + sg * 55, yy + 38], [xc + sg * 15, yy + 38]], 7);
      sheetZ(S, [[xw, yy + 58], [xw - sg * 55, yy + 58], [xw - sg * 55, yy + 96], [xw - sg * 15, yy + 96]], 7);
    }
  // viga portapanel s/ neopreno en el cuello, pintura asfáltica, junta EPS con la columna
  S.box(10, 175, -510, -500, ZB, 0, 'neo');
  S.prism([[10, -500], [230, -500], [230, -50], [30, -50], [10, -70]], 'z', ZB, 0, 'pre');
  S.box(6, 10, -500, -160, ZB, 0, 'memb');
  S.box(230, 250, -500, -327, ZB, 0, 'eps');
  // terreno y vereda
  S.box(X0, -76, Y0, -327, ZB, 0, 'tierra'); S.box(-76, 6, -510, -327, ZB, 0, 'tierra');
  S.box(X0, 0, -327, -250, ZB, 0, 'tosca'); S.box(X0, 0, -250, -150, ZB, -120, 'hs'); S.box(0, 6, -250, -150, ZB, -120, 'eps');
  S.box(975, X1, Y0, -327, ZB, 0, 'tierra'); S.box(670, 975, -510, -327, ZB, 0, 'tierra');
  // piso interior separado de la columna por junta de dilatación
  S.box(670, X1, -327, -177, ZB, 0, 'tosca'); S.box(670, X1, -177, -175, ZB, -40, 'film');
  S.box(670, X1, -175, -55, ZB, -90, 'hs'); S.box(670, X1, -55, -35, ZB, -140, 'hid');
  S.box(670, X1, -35, -15, ZB, -190, 'mort'); S.box(675, X1, -15, 0, ZB, -230, 'porc');
  for (const xa of [230, 650]) { S.box(xa, xa + 20, -327, -10, ZB, 0, 'eps'); S.box(xa, xa + 20, -10, 0, ZB, 0, 'seal'); }
  // panel: mortero de asiento + pasador Ø16 en vaina c/ grout + selladores
  panelO(S, -40, Y1, ZB, 0, false, true);
  S.box(30, 230, -50, -40, ZB, 0, 'mort'); S.box(18, 31, -52, -38, ZB, 0, 'seal');
  S.cyl('y', 190, -125, 8, -330, 230, 'steel', 12);
  const A = (n, x, y, z) => S.anchor(n, x, y, z);
  A(15, 450, 150, -200); A(25, 60, 150, 0); A(26, 190, 100, 0); A(27, 120, 200, 0); A(43, 130, -45, 0); A(34, 25, -45, 0);
  A(42, 120, -300, 0); A(44, 8, -400, -100); A(45, -200, -150, -200); A(56, 3, -200, 0); A(55, 90, -505, 0);
  A(35, 850, 0, -230); A(36, 850, -25, -190); A(37, 850, -45, -140); A(38, 850, -120, -90); A(39, 850, -176, -40); A(40, 850, -260, 0);
  A(41, 660, -250, 0); A(46, 450, -650, 0); A(47, 690, -700, 0); A(48, 212, -600, 0); A(49, 540, -740, 0); A(50, 850, -700, 0); A(54, 900, -600, 0);
  return S;
}
'''
os.makedirs("build", exist_ok=True)
open("build/nodos_opaco.js", "w", encoding="utf-8").write(base + OPACO)
print("ok nodos_opaco.js")
