# TP N°6 Construcciones II – Corte integral ACERO con FRENTE INTEGRAL (A3 vertical)

Entregable: `../entregables/TP6_ACERO_FRENTE_INTEGRAL_A3/Corte_Integral_Acero_Frente_Integral_A3.pdf` (imprimir al 100 %, A3 vertical).
- Corte integral **esc. 1:20** (`src/corte.py`, SVG en mm de papel).
- 3 detalles en **axonometría isométrica esc. 1:10** (`src/detalles.js`: un único modelo 3D recortado por la caja de cada detalle;
  `src/detalles_lamina.js`: composición, escala exacta 1:10 y globos).

Correcciones de la docente incorporadas: escala real y formato único; chapa plegada para anclaje del panel sándwich (12) sobre montante
de parapeto soldado (13); tubo soldado a la viga para anclar el frente integral (29); baranda fijada a la losa con planchuela + brocas (38);
vela rígida a losa para el cielorraso (45); dado estructural de H°A° para columna y frente integral (23); dado H°A° y contrapiso
H° pobre con rayados distintos y rotulados.

## Regenerar
```
npm install
python3 src/corte.py && node render.js src/lamina.html build/lamina portrait
```
