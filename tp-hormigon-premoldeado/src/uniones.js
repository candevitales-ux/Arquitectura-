// Lámina 3 – Detalles de uniones a nivel 1:1, en perspectiva simétrica (plano de simetría z = 0)
// Mismas coordenadas que el corte integral: x+ interior, y+ arriba (±0,00 = NPT PB), mm reales.
import { Scene3D, MAT } from './lib3d.js';

Object.assign(MAT, {
  pa: { color: '#3c4650' },          // poliamida (barrera térmica)
  butyl: { color: '#141414' },
  silic: { color: '#4a4a4a' },
  desic: { color: '#e9e2c3' },
  pvb: { color: '#e4f2f7' },
  epdm: { color: '#202020' },
  inox: { color: '#b9bec4' },
});

// ---------------------------------------------------------------- utilidades
const hex = (S, axis, c1, c2, r, w0, w1, key = 'inox') => S.cyl(axis, c1, c2, r, w0, w1, key, 6);
const vigaP = (yb) => { const yt = yb + 700; return [[250, yb], [750, yb], [750, yb + 330], [550, yb + 330], [550, yt], [250, yt]]; };
function losa(S, yb, x0, x1, z0, z1) {   // losa alveolar extruida en x, alvéolos Ø210
  const yt = yb + 300, h = [];
  for (let zc = z1 - 150; zc > z0 + 100; zc -= 225) h.push({ circle: [-zc, yb + 150, 105] });
  S.prism([[-z1, yb], [-z0, yb], [-z0, yt], [-z1, yt]], 'x', x0, x0 + 300, 'pre');
  S.prism([[-z1, yb], [-z0, yb], [-z0, yt], [-z1, yt]], 'x', x0 + 300, x1, 'pre', h);
}

// =============================================================== UNIÓN 1: COLUMNA – VIGAS
export function u1() {
  const S = new Scene3D();
  const yb = 3760, yt = 4460, C = 200;               // columna z -200..200
  // columna 40x40 (continúa hacia arriba y abajo: cortes rayados)
  S.box(250, 650, 3150, 4900, -C, C, 'pre', { axis: 'y' });
  // ménsulas simétricas sobre las caras z = ±200
  for (const s of [1, -1]) {
    const pts = [[C, 3750], [C + 350, 3750], [C + 350, 3550], [C, 3350]].map(([z, y]) => [-(s * z), y]);
    S.prism(s > 0 ? pts : pts.reverse(), 'x', 250, 650, 'pre');
    // chapa de borde de ménsula (perfil L embutido) y neopreno
    S.box(250, 650, 3740, 3750, s * (C + 330), s * (C + 350), 'steel');
    S.box(270, 630, 3750, 3760, s * (C + 20), s * (C + 330), 'neo');
    // vigas "L" (cortadas a 1,20 m)
    S.prism(vigaP(yb), 'z', s > 0 ? C + 20 : -1000, s > 0 ? 1000 : -(C + 20), 'pre');
    // junta viga–columna llenada c/ mortero
    S.box(250, 750, yb, yt, s * C, s * (C + 20), 'grout');
    // bulón Ø20 + vaina grouteada + cajeado superior con arandela y tuerca
    const zb = s * (C + 160);
    S.cyl('y', 400, zb, 10, 3480, yt + 26, 'steel', 20);
    S.box(345, 455, yt - 2, yt + 1, zb - 55, zb + 55, 'grout');
    S.cyl('y', 400, zb, 40, yt + 1, yt + 7, 'galv');
    hex(S, 'y', 400, zb, 21, yt + 7, yt + 24, 'steel');
    // estribos salientes de la viga (vinculación con la capa de compresión)
    for (const zz of [s * 600, s * 850]) S.sheet([[300, yt - 30], [300, yt + 70], [520, yt + 70], [520, yt - 30]], 10, 'z', zz - 5, zz + 5, 'red');
    // cordones de pretensado vistos en el corte
    for (const x of [310, 400, 490, 610, 690]) S.cyl('z', x, yb + 60, 6.5, s > 0 ? 995 : -1003, s > 0 ? 1003 : -995, 'neo', 12);
    // losas alveolares sobre el talón
    S.box(590, 740, 4090, 4100, s > 0 ? C + 20 : -1000, s > 0 ? 1000 : -(C + 20), 'neo');
    losa(S, 4100, 570, 1050, s > 0 ? C + 20 : -1000, s > 0 ? 1000 : -(C + 20));
    // capa de compresión (sector alejado, para dejar ver la unión)
    S.box(570, 900, 4400, yt, s > 0 ? 700 : -1000, s > 0 ? 1000 : -700, 'insitu');
  }
  // losa recortada frente a la columna + llenado in situ alrededor de la columna
  losa(S, 4100, 660, 1050, -C - 20, C + 20);
  S.box(650, 660, 4100, 4400, -C - 20, C + 20, 'grout');
  // armadura de continuidad sobre el apoyo (pasa junto a la columna)
  for (const x of [700, 780, 860]) S.cyl('z', x, yt + 14, 8, -950, 950, 'red', 10);
  for (const z of [-800, -400, 400, 800]) S.cyl('x', yt + 6, z, 5, 680, 1000, 'red', 10);

  const A = (n, x, y, z) => S.anchor(n, x, y, z);
  A(1, 650, 4750, 0); A(2, 650, 3500, 380); A(2, 650, 3500, -380); A(3, 650, 3745, 540); A(4, 640, 3755, -470);
  A(5, 750, 3900, 800); A(5, 750, 3900, -800); A(6, 700, 4200, 210); A(7, 400, yt + 20, 360); A(8, 400, yt, -360);
  A(9, 520, yt + 70, 850); A(10, 690, yb + 60, 1000); A(11, 1050, 4250, 700); A(11, 1050, 4250, -500); A(12, 700, 4095, -800);
  A(13, 800, yt, 850); A(14, 760, yt + 14, -900); A(15, 655, 4300, 0); A(16, 950, yt + 6, -400);
  return S;
}
export const RU1 = [
  'Columna premoldeada H°A° 40x40 H-30 (continua; cortes rayados).',
  'Ménsulas cortas simétricas, hormigonadas con la columna.',
  'Perfil L de borde embutido en la ménsula (protección de arista).',
  'Apoyo de neopreno 10 mm (absorbe giros y tolerancias).',
  'Viga portante premoldeada pretensada “L” 30/70 (talón 20x33).',
  'Junta viga–columna 20 mm llenada con mortero sin retracción.',
  'Bulón Ø 20 anclado en la ménsula, pasante por vaina Ø 50 en la viga.',
  'Cajeado superior: arandela + tuerca; luego llenado con grout.',
  'Estribos salientes de la viga (vinculación con la capa de compresión).',
  'Cordones de pretensado Ø 12,7 mm.',
  'Losa alveolar pretensada e = 30 cm (alvéolos Ø 21 cm).',
  'Neopreno continuo losa / talón de viga.',
  'Capa de compresión H°A° in situ 6 cm c/ malla Q188 (sector).',
  'Armadura de continuidad sobre el apoyo (negativos), pasa junto a la columna.',
  'Losa recortada frente a la columna + llenado in situ.',
  'Barras transversales de vinculación losa–viga.',
];

// =============================================================== UNIÓN 2: VIDRIO – MONTANTE (corte horizontal)
export function u2() {
  const S = new Scene3D();
  const H = 170;
  // montante 50x150: dos cámaras + nariz con canal de tornillo
  S.prism([[32, -25], [182, -25], [182, 25], [32, 25]], 'y', 0, H, 'alu',
    [[[35, -22], [99, -22], [99, 22], [35, 22]], [[103, -22], [179, -22], [179, 22], [103, 22]]]);
  S.prism([[14, -8], [32, -8], [32, 8], [14, 8]], 'y', 0, H, 'alu', [{ circle: [22, 0, 3.2] }]);
  S.box(9, 14, 0, H, -10, 10, 'pa', { axis: 'y' });                  // barrera térmica de poliamida
  // paños DVH a ambos lados
  for (const s of [1, -1]) {
    const z0 = s * 12, z1 = s * 420, zs = (a, b) => [Math.min(s * a, s * b), Math.max(s * a, s * b)];
    const g = (x0, x1, key, top) => { const [a, b] = zs(12, 95); S.box(x0, x1, 0, top, a, b, key, { axis: 'y' }); };
    g(0, 6, 'glass', 160); g(18, 21, 'glass', 160); g(21, 22, 'pvb', 160); g(22, 25, 'glass', 160);
    // sello perimetral del DVH
    let [a, b] = zs(12, 17); S.box(6, 18, 0, 155, a, b, 'silic', { axis: 'y' });      // sellador secundario (silicona estructural)
    [a, b] = zs(17, 29); S.box(7, 17, 0, 155, a, b, 'alu', { axis: 'y' });            // separador de aluminio
    [a, b] = zs(19, 27); S.box(9, 15, 0, 156, a, b, 'desic', { axis: 'y' });          // desecante
    [a, b] = zs(17, 29); S.box(6, 7, 0, 155, a, b, 'butyl', { axis: 'y' }); S.box(17, 18, 0, 155, a, b, 'butyl', { axis: 'y' });
    // burletes EPDM exterior e interior (perfil cuña)
    const bur = (xa, xb, top) => { const [p, q] = zs(13, 24); S.box(xa, xb, 0, top, p, q, 'epdm', { axis: 'y' }); };
    bur(-4, 0, 145); bur(25, 32, 145);
  }
  // presor de aluminio y tapa clipada
  S.prism([[-16, -26], [-4, -26], [-4, 26], [-16, 26]], 'y', 0, 130, 'alu', [{ circle: [-10, 0, 3.5] }]);
  S.prism([[-16, -27], [-32, -27], [-32, 27], [-16, 27], [-16, 24], [-29, 24], [-29, -24], [-16, -24]].map(([x, z]) => [x, z]), 'y', 0, 110, 'alu2');
  // tornillos inox c/ 25 cm (cabeza dentro de la tapa)
  for (const y of [40, 120]) {
    S.cyl('x', y, 0, 3, -14, 30, 'inox', 16);
    hex(S, 'x', y, 0, 6, -19, -14, 'inox');
  }
  // calzo de apoyo y travesaño inferior (referencia de encuentro)
  const A = (n, x, y, z) => S.anchor(n, x, y, z);
  A(1, 110, H, 0); A(2, 22, H, 0); A(3, 11, H, 6); A(4, 3, 160, 70); A(4, 3, 160, -70); A(5, 21.5, 160, -80);
  A(6, 12, 155, 14); A(7, 12, 155, -23); A(8, 12, 156, 23); A(9, 6.5, 155, -26); A(10, -2, 145, 18);
  A(11, 28, 145, -18); A(12, -10, 130, 20); A(13, -30, 110, -10); A(14, -19, 120, 0); A(15, 0, 100, 0);
  return S;
}
export const RU2 = [
  'Montante de aluminio 50x150 (aleación 6063 T6), dos cámaras.',
  'Nariz del montante con canal para tornillo.',
  'Barrera térmica de poliamida (corta el puente térmico).',
  'DVH: vidrio exterior templado 6 mm.',
  'Vidrio interior laminado 3+3 con lámina PVB 0,76 (seguridad).',
  'Sellador secundario: silicona estructural.',
  'Separador de aluminio (cámara 12 mm, aire o argón).',
  'Sales desecantes dentro del separador.',
  'Sellador primario: cordón de butilo (barrera de vapor).',
  'Burlete exterior de EPDM.',
  'Burlete interior de EPDM (apoyo del vidrio).',
  'Presor de aluminio (fija el vidrio contra el montante).',
  'Tapa exterior clipada (cubre-presor), anodizada.',
  'Tornillo inox c/ 25 cm, presor → montante.',
  'Junta entre paños 24 mm, drenada y ventilada.',
];

// =============================================================== UNIÓN 3: VIDRIO – VIGA DE ENTREPISO
export function u3() {
  const S = new Scene3D();
  const yb = 3760, yt = 4460, Z = 380;
  // viga L, neopreno, losa, junta, capa de compresión y piso
  S.prism(vigaP(yb), 'z', -Z, Z, 'pre');
  for (const x of [310, 400, 490, 610, 690]) for (const s of [1, -1]) S.cyl('z', x, yb + 60, 6.5, s * Z - 4, s * Z + 4, 'neo', 12);
  S.box(590, 740, 4090, 4100, -Z, Z, 'neo');
  losa(S, 4100, 570, 950, -Z, Z);
  S.box(550, 570, 4090, 4400, -Z, Z, 'insitu');
  S.box(570, 950, 4400, 4460, -Z, Z, 'insitu');
  S.box(700, 950, 4460, 4485, -Z, Z, 'mort');
  S.box(800, 950, 4485, 4500, -Z, Z, 'porc');
  // riel de anclaje tipo Halfen embutido (perfil C) + pernos de anclaje
  S.prism([[280, 4460], [280, 4415], [320, 4415], [320, 4460], [311, 4460], [311, 4455], [316, 4455], [316, 4419], [284, 4419], [284, 4455], [289, 4455], [289, 4460]], 'z', -Z, Z, 'steel');
  for (const z of [-250, 250]) S.cyl('y', 300, z, 8, 4330, 4416, 'steel');
  // montante (con junta de dilatación y manguito interior)
  for (const [y0, y1] of [[4000, 4700], [4720, 4900]])
    S.prism([[32, -25], [182, -25], [182, 25], [32, 25]], 'y', y0, y1, 'alu', [[[35, -22], [179, -22], [179, 22], [35, 22]]]);
  S.box(38, 176, 4620, 4800, -19, 19, 'alu2', { axis: 'y' });
  S.box(-14, -2, 4000, 4900, -22, 22, 'alu', { axis: 'y' });
  S.prism([[-30, -18], [-14, -22], [-14, 22], [-30, 18]], 'y', 4000, 4900, 'alu2');
  // grapas dobles (una a cada lado del montante), regulables 3D
  for (const s of [1, -1]) {
    const zz = (a, b) => [Math.min(s * a, s * b), Math.max(s * a, s * b)];
    let [a, b] = zz(25, 30); S.box(100, 200, 4330, 4470, a, b, 'neo');                 // separador aislante (evita par galvánico)
    [a, b] = zz(30, 40); S.box(100, 200, 4330, 4470, a, b, 'galv');                    // ala vertical
    [a, b] = zz(30, 140); S.box(190, 370, 4460, 4470, a, b, 'galv');                    // ala horizontal s/ viga
    [a, b] = zz(40, 41); S.box(122, 168, 4392, 4408, a, b, 'butyl');                    // colisos (ajuste)
    [a, b] = zz(75, 95); S.box(270, 330, 4470, 4471, a, b, 'butyl');
    // bulón cabeza martillo en el riel + arandela + tuerca
    S.cyl('y', 300, s * 85, 6, 4425, 4500, 'inox', 16);
    S.cyl('y', 300, s * 85, 16, 4470, 4474, 'inox');
    hex(S, 'y', 300, s * 85, 11, 4474, 4486, 'inox');
    S.box(292, 308, 4425, 4433, s * 85 - 14, s * 85 + 14, 'inox');
    hex(S, 'z', 140, 4400, 11, ...zz(41, 50).sort((p, q) => p - q), 'inox');
  }
  S.cyl('z', 140, 4400, 6, -52, 52, 'inox', 16);   // bulón M12 pasante por el montante
  // travesaño + presor + tapa a ambos lados del montante
  for (const [z0, z1] of [[-Z, -25], [25, Z]]) {
    S.prism([[32, 4560], [150, 4560], [150, 4620], [32, 4620]], 'z', z0, z1, 'alu', [[[36, 4564], [146, 4564], [146, 4616], [36, 4616]]]);
    S.box(8, 32, 4582, 4598, z0, z1, 'alu');
    S.box(-14, -2, 4538, 4642, z0, z1, 'alu');
    S.prism([[-30, 4542], [-14, 4538], [-14, 4642], [-30, 4638]], 'z', z0, z1, 'alu2');
    for (const yy of [4540, 4628]) { S.box(-2, 0, yy, yy + 12, z0, z1, 'epdm'); S.box(25, 32, yy, yy + 12, z0, z1, 'epdm'); }
    S.box(2, 24, 4620, 4626, z0 < 0 ? -320 : 220, z0 < 0 ? -220 : 320, 'neo');   // calzo de apoyo
  }
  // spandrel (vidrio esmaltado), lana mineral, bandeja y vidrio de visión
  for (const [z0, z1] of [[-Z, -35], [35, Z]]) {
    S.box(0, 6, 4000, 4550, z0, z1, 'spandrel');
    S.box(40, 90, 4000, 4550, z0, z1, 'lana');
    S.box(90, 93, 4000, 4550, z0, z1, 'galv');
    S.box(0, 6, 4630, 4900, z0, z1, 'glass'); S.box(18, 25, 4630, 4900, z0, z1, 'glass');
    S.box(6, 18, 4630, 4644, z0, z1, 'alu');
  }
  // barrera cortafuego (retirada junto al montante para ver la grapa)
  for (const [z0, z1] of [[-Z, -160], [160, Z]]) {
    S.box(93, 250, 4340, 4350, z0, z1, 'galv');
    S.box(93, 250, 4350, 4455, z0, z1, 'lana');
    S.box(93, 250, 4455, 4462, z0, z1, 'intum');
    S.sheet([[182, 4503], [330, 4503]], 3, 'z', z0, z1, 'alu');
  }

  const A = (n, x, y, z) => S.anchor(n, x, y, z);
  A(1, 500, 4100, Z); A(1, 500, 4100, -Z); A(2, 300, 4440, 300); A(3, 300, 4370, -250); A(4, 150, 4400, 40); A(4, 150, 4400, -40);
  A(5, 145, 4400, 41); A(6, 280, 4465, 110); A(6, 280, 4465, -110); A(7, 300, 4486, 85); A(7, 300, 4486, -85); A(8, 140, 4400, -50);
  A(9, 100, 4380, 27); A(10, 110, 4710, 0); A(11, 110, 4800, 0); A(12, 90, 4590, 300); A(13, 3, 4300, -300); A(14, 65, 4300, 300);
  A(15, 170, 4400, 300); A(16, 170, 4460, -300); A(17, 250, 4503, 300); A(18, 900, 4480, -300); A(19, 950, 4250, 200);
  A(20, 12, 4800, -300);
  return S;
}
export const RU3 = [
  'Viga portante premoldeada pretensada “L” (borde de losa).',
  'Riel de anclaje embutido tipo Halfen (perfil C, hormigonado en planta).',
  'Pernos de anclaje del riel en el hormigón.',
  'Grapas dobles de acero galv. (una a cada lado del montante).',
  'Agujeros colisos: regulación en altura y profundidad.',
  'Ala horizontal sobre la viga c/ coliso transversal (regulación lateral).',
  'Bulón cabeza martillo M12 en el riel + arandela + tuerca.',
  'Bulón M12 inox pasante por el montante (montante colgado).',
  'Separadores aislantes de neopreno (evitan el par galvánico acero/aluminio).',
  'Junta de dilatación del montante 20 mm.',
  'Manguito interior de empalme (deslizante).',
  'Travesaño 50x120 + presor + tapa + burletes EPDM.',
  'Spandrel: vidrio templado 6 mm esmaltado.',
  'Lana mineral 50 mm + bandeja de chapa galv. (back-pan).',
  'Barrera cortafuego: lana mineral 100 kg/m³ s/ chapa galv. (retirada en el montante).',
  'Sellador intumescente.',
  'Cubrejunta de aluminio.',
  'Capa de compresión + carpeta + porcelanato.',
  'Losa alveolar pretensada e = 30 cm.',
  'DVH de visión 6 + 12 + 3+3 laminado.',
];
