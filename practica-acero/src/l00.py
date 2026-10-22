# -*- coding: utf-8 -*-
"""Lámina 01 - Carátula: datos, consigna resumida e índice de láminas."""
from lib import *
from geom import *

sh = Sheet(NUM["caratula"], "Carátula, consigna e índice", "CARÁTULA", "s/ esc.")
L, R = sh.L + 3, sh.R - 3
y = sh.T - 14
sh.txt("UNM - CONSTRUCCIONES 2", L, y, 3.0, bold=True, layer="3-TITULOS")
y -= 14
sh.txt("PRÁCTICA EN CLASE", L, y, 5.0, bold=True, layer="3-TITULOS")
y -= 9
sh.txt("GRANDES LUCES EN ACERO", L, y, 7.0, bold=True, layer="3-TITULOS")
y -= 8
sh.txt("Sistema del TP6 ACERO: pórticos de 12 m con losa colaborante (steel deck)", L, y, 2.6, layer="3-TITULOS")
y -= 4
sh.pl([(L, y), (R, y)], "3-TITULOS", 70)
y -= 8
for a, b in (("ALUMNA:", "Vitale Candelaria"), ("GRUPO:", "13"), ("DOCENTES:", "Arq. Tucci y Arq. Cardozo"), ("FECHA:", FECHA),
             ("FORMATO:", f"{TOTAL} láminas A4 vertical - PDF y DWG (hoja a escala 1:1)")):
    sh.txt(a, L, y, 2.6, bold=True); sh.txt(b, L + 26, y, 2.6); y -= 5
y -= 3
sh.titulo_dib(L, y, "C", "CONSIGNA", w=R - L)
y = ficha_spec(sh, L, y - 6, R - L, [
    ("1°", "Listar gráficamente los elementos constructivos del sistema, con referencias, medidas, función y especificación técnica (manual del fabricante)."),
    ("2°", "Enumerar gráficamente cada junta y unión entre los elementos del sistema (manual del fabricante y teórica de juntas y uniones)."),
    ("3°", "Describir y graficar las máquinas y herramientas de montaje, moldeo y anclaje (mín. 3) y cómo se planifica su alquiler, armado y acceso a la obra."),
    ("4°", "Muro exterior: muro cortina (CW) y el integral elegido, vidriado y opaco; croquis proporcionados, comparación y justificación."),
], h=2.2, lead=1.45) - 4
sh.titulo_dib(L, y, "i", "ÍNDICE DE LÁMINAS", w=R - L)
rows = [[f"{n:02d}", t, p] for n, t, p in LAMINAS]
sh.tabla(L, y - 5, [("N°", 10), ("Contenido", R - L - 10 - 16), ("Punto", 16)], rows, h=2.2, lead=1.3, pad=1.1)
sh.save(f"L{NUM['caratula']:02d}_Caratula_indice")
