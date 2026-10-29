# TP N°6 Construcciones II – Corte integral ACERO con FRENTE INTEGRAL (A3 vertical)

Entregable: `../entregables/TP6_ACERO_FRENTE_INTEGRAL_A3/Corte_Integral_Acero_Frente_Integral_A3.pdf` (imprimir al 100 %, A3 vertical).

- **Corte**: es el corte original de la alumna (`original/corte_original.pdf`, vectores de AutoCAD) sin redibujar, recortado y
  ubicado a **escala 1:20 real** (el original está a 1:10 en mm de papel). Encima solo se agregan las correcciones de la docente
  (`original/correcciones_docente.jpg`) y líneas de interrupción en los paños vidriados.
- **Detalles 1, 2 y 3**: los mismos círculos del corte, en **axonometría isométrica a 1:10**, modelados con las medidas del original
  (`src/detalles.js`).

Correcciones incorporadas (referencias 36 a 40): 36 chapa plegada para anclaje del panel sándwich · 37 tubo soldado a la viga IPN
para anclar la columna del frente integral (cubierta y entrepiso) · 38 brocas de la baranda a la losa · 39 vela rígida a losa para
cielorraso · 40 dado estructural de H°A° para columna y frente integral, con rayado distinto al del contrapiso (4).

## Regenerar
```
npm install
python3 src/lamina.py && node render.js src/lamina.html build/lamina portrait
```
