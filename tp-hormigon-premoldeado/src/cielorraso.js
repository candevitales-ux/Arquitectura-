// Cielorraso técnico suspendido de placas de roca de yeso sobre estructura de perfiles de chapa galvanizada (steel frame / "junta tomada").
// Coordenadas en mm reales: x+ a la derecha, y+ arriba, z+ hacia el observador. y = 0: cara inferior de las placas.
import { Scene3D, MAT } from './lib3d.js';

Object.assign(MAT, {
  mamp: { color: '#d9b39a', hatch: 'ha', bg: '#e7cbb7', period: 90 },   // mampostería revocada
  masilla: { color: '#e9e2cf' },                                           // cinta + masilla de juntas
});

export const DIM = {
  PL: 12.5,          // placa de roca de yeso estándar 12,5 mm
  H: 650,            // cara inferior de la losa (pleno = 650 - 12,5 mm)
  E: 120,            // espesor de losa
  X: 2700, Z: 2000,  // sector representado
  SEC: [-1600, -1200, -800, -400, -19],   // montantes secundarios c/ 40 cm (eje, en z)
  MAE: [900, 2100],                        // vigas maestras c/ 1,20 m (eje, en x)
  VEL: [-1500, -500],                      // velas rígidas c/ 1,00 m (en z)
};

// perfil C de chapa (polilínea): alma en u = u0 de largo w (centrada en vc); alas de ancho d hacia dir; labios de 6 mm
function C(u0, vc, d, w, dir = 1, lip = 6) {
  const a = vc - w / 2, b = vc + w / 2, f = u0 + dir * d;
  return lip ? [[f, a + lip], [f, a], [u0, a], [u0, b], [f, b], [f, b - lip]] : [[f, a], [u0, a], [u0, b], [f, b]];
}
const T = 1;   // espesor de chapa dibujado (real 0,52 mm)

export function cielorraso(crop = null) {
  const S = new Scene3D(); if (crop) S.crop = crop;
  const { PL, H, E, X, Z, SEC, MAE, VEL } = DIM;
  const yS = PL + 1.5 + 17;          // eje del montante secundario (alma 34)
  const yM = PL + 1.5 + 34 + 1 + 17; // eje de la viga maestra (apoyada sobre los secundarios)
  const yMb = yM - 17;

  // ------------------------------------------------ envolvente: losa y muros
  S.box(-150, X, H, H + E, -Z - 150, 0, 'insitu');
  S.box(-150, 0, -150, H, -Z - 150, 0, 'mamp');                               // muro izquierdo
  S.box(0, X, -150, H, -Z - 150, -Z, 'mamp', { axis: 'x' });                  // muro del fondo

  // ------------------------------------------------ soleras perimetrales PGU 35 (fijadas al muro)
  S.sheet([[29, PL + 0.5], [0.5, PL + 0.5], [0.5, PL + 36.5], [29, PL + 36.5]], T, 'z', -Z + 29, 0, 'galv');
  S.sheet([[Z - 29, PL + 0.5], [Z - 0.5, PL + 0.5], [Z - 0.5, PL + 36.5], [Z - 29, PL + 36.5]], T, 'x', 0.5, X, 'galv');
  for (const z of [-1700, -1100, -500]) S.cyl('x', PL + 18.5, z, 6, 1, 3.5, 'steel', 16);        // tarugo + tornillo c/ 60 cm
  for (const x of [150, 750, 1350, 1950, 2550]) S.cyl('z', x, PL + 18.5, 6, -Z + 1, -Z + 3.5, 'steel', 16);

  // ------------------------------------------------ montantes secundarios PGC 34 c/ 40 cm (encastrados en la solera)
  for (const zc of SEC) S.sheet(C(-zc - 17.5, yS, 35, 34, 1), T, 'x', 2, X - 300, 'galv');

  // ------------------------------------------------ vigas maestras (montante 34) c/ 1,20 m, sobre los secundarios
  for (const xm of MAE) {
    S.sheet(C(xm + 17.5, yM, 35, 34, -1), T, 'z', -Z + 10, 0, 'galv');
    for (const zc of SEC) S.cyl('y', xm, zc, 4, yMb, yMb + 2.5, 'steel', 14);     // T1 maestra–secundario
    // velas rígidas (montante 34) c/ 1,00 m: atornilladas al alma de la maestra y ancladas a la losa
    for (const zv of VEL) {
      S.sheet(C(xm + 18.5, -zv, 34, 35, 1), T, 'y', yMb, H - 2, 'galv');
      for (const y of [yM - 8, yM + 8]) S.cyl('x', y, zv, 4, xm + 15, xm + 18, 'steel', 14);   // T1 vela–maestra
      // ángulo de anclaje 40 x 50 + broca / tarugo a la losa
      S.sheet([[xm + 17.5, H - 45], [xm + 17.5, H - 0.6], [xm - 35, H - 0.6]], 1.2, 'z', zv - 25, zv + 25, 'galv');
      S.cyl('y', xm - 14, zv, 7.5, H - 4.5, H - 1.2, 'steel', 6);                  // cabeza de broca (hex)
      S.cyl('y', xm - 14, zv, 3.5, H - 1.2, H + 45, 'steel', 12);
      for (const y of [H - 32, H - 16]) S.cyl('x', y, zv, 4, xm + 15, xm + 17, 'steel', 14);   // T1 ángulo–vela
    }
  }

  // ------------------------------------------------ placas de roca de yeso 12,5 mm (junta tomada)
  const plates = [[0, 1200, -Z, 0], [1200, 1800, -Z, -1200]];
  for (const [x0, x1, z0, z1] of plates) S.box(x0, x1, 0, PL, z0, z1, 'yeso', { axis: 'y' });
  S.box(1150, 1250, -0.9, 0, -Z, -1200, 'masilla', { axis: 'y' });                     // cinta de papel + masilla
  // tornillos T2 c/ 25 cm sobre cada montante (cabeza al ras de la placa)
  for (const [x0, x1, z0, z1] of plates) {
    const zs = [...SEC.map(z => Math.min(z, z1 - 10)), -Z + 15].filter(z => z > z0 && z < z1 || z === z1 - 10);
    for (const z of zs) for (let x = x0 + 25; x < x1; x += 250) S.cyl('y', x, z, 4, -0.5, 0.2, 'neo', 14);
  }

  // ------------------------------------------------ referencias
  S.anchor(1, 2560, H, -260);
  S.anchor(2, 0, -90, -700);
  S.anchor(3, 2460, PL + 0.5, -Z + 14);
  S.anchor(4, 2550, PL + 18.5, -Z + 3.5);
  S.anchor(5, 2330, PL + 1.5, -400);
  S.anchor(6, 2085, yMb, -1000);
  S.anchor(7, 2100 + 52, 360, -500);
  S.anchor(8, 2100 - 20, H - 0.6, -500 + 25);
  S.anchor(9, 2100 + 16, yM - 8, -500);
  S.anchor(10, 500, 0, -900);
  S.anchor(11, 525, -0.5, -400);
  S.anchor(12, 1200, -0.9, -1650);
  S.anchor(13, 1800, PL / 2, -1600);
  // anclas adicionales solo para los detalles (fuera del recorte se descartan solas)
  if (crop) {
    S.anchor(1, 2150, H, -430); S.anchor(7, 2152, 600, -500); S.anchor(9, 2116, H - 16, -500);                 // A
    S.anchor(5, 2205, yS + 17, -390); S.anchor(6, 2085, yM + 17, -320); S.anchor(7, 2152, 170, -500);
    S.anchor(9, 2100, yMb + 2.5, -400);                                                                         // B
    S.anchor(2, 1640, -100, -2000); S.anchor(3, 1880, PL + 0.5, -1985); S.anchor(4, 1950, PL + 18.5, -Z + 3.5);
    S.anchor(10, 1650, 0, -1800); S.anchor(11, 1725, -0.5, -1985); S.anchor(5, 1900, PL + 1.5, -1600);        // C
  }
  return S;
}

export const REFS = [
  'Losa de H°A° (e = 12 cm) – cara inferior',
  'Muro de mampostería revocada',
  'Solera perimetral PGU 35 x 28 x 0,52 mm (chapa galv.)',
  'Fijación de solera: tarugo nylon Ø 8 + tornillo c/ 60 cm',
  'Montante secundario PGC 34 x 35 x 0,52 mm c/ 40 cm, encastrado en la solera',
  'Viga maestra (montante 34) c/ 1,20 m, perpendicular a los secundarios',
  'Vela rígida (montante 34) c/ 1,00 m sobre cada maestra',
  'Ángulo de anclaje galv. + broca metálica Ø 8 a la losa',
  'Tornillos T1 (punta aguja) en uniones perfil–perfil',
  'Placa de roca de yeso estándar 12,5 mm (1,20 x 2,40 m), lado largo ⟂ montantes',
  'Tornillos T2 c/ 25 cm sobre montantes y soleras',
  'Junta tomada: cinta de papel microperforada + masilla (3 manos)',
  'Borde de placa (canto) – placa atornillada a la cara inferior de los montantes',
];

// recortes para los detalles ampliados
export const CROPS = {
  A: { x0: 2010, x1: 2190, y0: 560, y1: 770, z0: -590, z1: -410 },   // anclaje de la vela a la losa
  B: { x0: 1990, x1: 2220, y0: 10, y1: 200, z0: -620, z1: -290 },    // cruce maestra – secundario – vela
  C: { x0: 1560, x1: 1990, y0: -120, y1: 110, z0: -2150, z1: -1560 }, // solera perimetral + placa + muro
};
