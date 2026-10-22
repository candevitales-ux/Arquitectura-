# -*- coding: utf-8 -*-
"""Lámina 03 - Elementos 1: base aislada, pernos de anclaje, placa base y columna IPN 300."""
from lib import *
from geom import *

sh = Sheet(3, "Fundación, pernos de anclaje, placa base y columna", "PUNTO 1 - ELEMENTOS CONSTRUCTIVOS",
           "1:25 - 1:10 - 1:5 - 1:125")
y0 = sh.encabezado("1° ELEMENTOS: FUNDACIÓN Y COLUMNA", "Croquis a escala con medidas, función y especificación técnica")
L, R = sh.L + 3, sh.R - 3
W2 = (R - L - 6) / 2
XA, XB = L, L + W2 + 6
YT, YM = y0 - 3.5, y0 - 121

# =============================================================== 1. BASE AISLADA (1:25)
sh.titulo_dib(XA, YT, 1, "BASE AISLADA H°A° + PEDESTAL", "1:25", w=W2)
v = sh.view_in((XA, YT - 88, XA + W2, YT - 7), (-1250, -1620, 950, 330), 25)
TOPP = -330                      # coronamiento del pedestal
v.ln((-950, -150), (-260, -150), "1-VISTA", 25); v.ln((260, -150), (950, -150), "1-VISTA", 25)
v.hatch([(-950, -150), (-260, -150), (-260, 0), (-950, 0)], "hormigon"); v.rect(-950, -150, -260, 0, "1-SECCION", 25)
v.hatch([(260, -150), (950, -150), (950, 0), (260, 0)], "hormigon"); v.rect(260, -150, 950, 0, "1-SECCION", 25)
v.hatch([(-950, -150), (-750, -150), (-750, -1600), (-950, -1600)], "tierra")
v.hatch([(750, -150), (950, -150), (950, -1600), (750, -1600)], "tierra")
base = [(-700, FUND), (700, FUND), (700, FUND + 400), (250, FUND + 400), (250, TOPP), (-250, TOPP), (-250, FUND + 400), (-700, FUND + 400)]
v.hatch(base, "hormigon"); v.pl(base, "1-SECCION", 50, True)
v.rect(-750, FUND - 50, 750, FUND, "1-SECCION", 18); v.hatch([(-750, FUND - 50), (750, FUND - 50), (750, FUND), (-750, FUND)], "gris")
# armaduras: parrilla inferior y barras del pedestal
v.ln((-650, FUND + 50), (650, FUND + 50), "1-VISTA", 35)
for xx in range(-600, 601, 150): v.circ((xx, FUND + 70), 12, "1-VISTA", 13)
for xx in (-200, 200):
    v.pl([(xx - 150 * (1 if xx < 0 else -1) * 0 + (-150 if xx < 0 else 150), FUND + 60), (xx, FUND + 60), (xx, TOPP - 50)], "1-VISTA", 35)
for zz in range(int(FUND + 450), int(TOPP - 40), 150): v.rect(-205, zz, 205, zz + 4, "1-VISTA", 13)
# grout, placa y columna
v.rect(-225, TOPP, 225, TOPP + 30, "1-SECCION", 18); v.hatch([(-225, TOPP), (225, TOPP), (225, TOPP + 30), (-225, TOPP + 30)], "mortero")
v.rect(-225, TOPP + 30, 225, TOPP + 52, "1-SECCION", 35); v.hatch([(-225, TOPP + 30), (225, TOPP + 30), (225, TOPP + 52), (-225, TOPP + 52)], "acero")
ipn_vertical(v, COL, 0, TOPP + 52, 300, False, 35)
# pernos
for xx in (-185, 185):
    v.rect(xx - 10, TOPP - 520, xx + 10, TOPP + 52 + 60, "1-VISTA", 18)
    v.rect(xx - 40, TOPP - 530, xx + 40, TOPP - 520, "1-VISTA", 25)
    v.rect(xx - 17, TOPP + 52, xx + 17, TOPP + 52 + 18, "1-VISTA", 25)
# cotas y niveles
v.dim((-700, FUND), (700, FUND), -5)
v.dim((-250, FUND + 400), (250, FUND + 400), 3)
v.dim((-700, FUND), (-700, FUND + 400), -3)
v.dim((-700, FUND + 400), (-700, TOPP), -3)
v.nivel(-1000, 0, "±0,00", -1); v.nivel(-1000, FUND, "-1,50", -1); v.nivel(-1000, TOPP, "-0,33", -1)
for n, at, off in [(1, (550, FUND + 250), (9, 7)), (2, (185, TOPP - 330), (14, -3)), (3, (225, TOPP + 45), (14, 5)),
                   (4, (0, 250), (11, 2))]:
    v.ref(n, at, off)
v.ley("H° limpieza e = 5 cm", (600, FUND - 25), (2, -4))
v.ley("parrilla Ø12 c/15", (-450, FUND + 50), (-2, 7))
v.ley("grout e = 30", (-225, TOPP + 15), (-4, 9))
ficha_spec(sh, XA, YT - 90, W2, [
    ("Función:", "transmitir al suelo la carga de la columna (compresión, corte y momento de vuelco del viento)."),
    ("Medidas:", "base 1,40 x 1,40 x 0,40 m; pedestal 0,50 x 0,50 m hasta -0,33; fondo -1,50 (s/ estudio de suelos)."),
    ("Especificación:", "H-25 colado in situ, ADN 420: parrilla Ø12 c/15, pedestal 4 Ø16 + estribos Ø8 c/15; recubrimiento 5 cm; H° de limpieza 5 cm."),
    ("Colocación:", "los pernos se dejan colados con plantilla antes de hormigonar; la placa queda bajo el contrapiso."),
])

# =============================================================== 2. PERNOS DE ANCLAJE (1:10)
sh.titulo_dib(XB, YT, 2, "PERNOS DE ANCLAJE M20 + PLANTILLA", "1:10", w=W2)
v = sh.view_in((XB, YT - 88, XB + 52, YT - 7), (-330, -30, 130, 620), 10)
# perno en elevación
Lp = 600
v.rect(-10, 0, 10, Lp, "1-SECCION", 25); v.hatch([(-10, 0), (10, 0), (10, Lp), (-10, Lp)], "gris")
for zz in range(Lp - 150, Lp, 6): v.ln((-10, zz), (10, zz + 3), "1-VISTA", 9)
v.rect(-40, -10, 40, 0, "1-SECCION", 25); v.rect(-17, 0, 17, 16, "1-VISTA", 25)       # placa de anclaje + tuerca
for z0 in (Lp - 150, Lp - 104):                                                     # tuerca de nivelación / superior
    v.rect(-17, z0, 17, z0 + 16, "1-VISTA", 25)
v.rect(-22, Lp - 134, 22, Lp - 126, "1-VISTA", 18)                                    # arandela de nivelación
v.rect(-112, Lp - 126, 112, Lp - 104, "1-OCULTO", 13)                                 # placa base (fantasma)
v.ln((-60, Lp - 160), (60, Lp - 160), "1-OCULTO", 13)
v.dim((40, -10), (40, Lp), 5)
v.dim((40, Lp - 150), (40, Lp), 9)
v.dim((-40, -10), (40, -10), -4)
v.ref(2, (0, 300), (-8, 0))
v.ley("tuerca + arandela", (-17, Lp - 96), (-4, 5))
v.ley("tuerca de nivelación", (-17, Lp - 142), (-4, -3))
v.ley("sup. pedestal", (-60, Lp - 160), (-2, -8))
v.ley("rosca 150", (-10, Lp - 40), (-6, 3))
v.ley("placa de anclaje 80x80x10", (-40, -5), (-2, 6))
# plantilla en planta
v2 = sh.view_in((XB + 52, YT - 60, XB + W2, YT - 10), (-280, -320, 300, 200), 20)
v2.rect(-260, -140, 260, 140, "1-VISTA", 25); v2.hatch([(-260, -140), (260, -140), (260, 140), (-260, 140)], "madera")
for cx in (-185, 185):
    for cy in (-85, 85):
        v2.circ((cx, cy), 13, "1-SECCION", 25)
v2.ln((-300, 0), (300, 0), "1-EJES", 9); v2.ln((0, -170), (0, 170), "1-EJES", 9)
v2.dim((-185, 140), (185, 140), 3); v2.dim((260, -85), (260, 85), 3)
v2.label("PLANTILLA 1:20", 0, -200, 1.7, TA.MIDDLE_CENTER, True)
v2.label("fenólico 18 mm: fija los", 0, -250, 1.6, TA.MIDDLE_CENTER)
v2.label("pernos al hormigonar", 0, -295, 1.6, TA.MIDDLE_CENTER)
ficha_spec(sh, XB, YT - 90, W2, [
    ("Función:", "anclar la columna a la fundación y tomar el corte y el arrancamiento (tracción) en la base."),
    ("Medidas:", "barra roscada M20 (Ø20), largo 600 mm, rosca 150 mm, saliente 100-110 mm sobre el pedestal; 4 por columna a 370 x 170 mm."),
    ("Especificación:", "acero F-24 (SAE 1020) galvanizado en caliente; placa de anclaje 80x80x10; 3 tuercas + arandela por perno."),
    ("Colocación:", "plantilla de fenólico; tolerancia ±3 mm en planta y ±5 mm en altura; proteger la rosca hasta el montaje."),
])

# =============================================================== 3. PLACA BASE (1:10)
sh.titulo_dib(XA, YM, 3, "PLACA BASE 450 x 250 x 22", "1:10", w=W2)
v = sh.view_in((XA, YM - 46, XA + W2, YM - 10), (-240, -210, 290, 150), 10)            # planta
v.rect(-225, -125, 225, 125, "1-VISTA", 35)
pts = ipn_poly(*IPN[COL]); pts = xf(pts, 0, 0, 90)
v.pl(pts, "1-SECCION", 35, True); v.hatch(pts, "acero")
for cx in (-185, 185):
    for cy in (-85, 85):
        bulon_planta(v, (cx, cy), 20)
v.dim((-225, 125), (225, 125), 4); v.dim((225, -125), (225, 125), 5)
v.dim((-185, -125), (185, -125), -4)
v.label("PLANTA", 0, -190, 1.8, TA.MIDDLE_CENTER, True)
v = sh.view_in((XA, YM - 82, XA + W2, YM - 46), (-245, -190, 290, 170), 10, ha="r")            # corte
v.rect(-225, 30, 225, 52, "1-SECCION", 35); v.hatch([(-225, 30), (225, 30), (225, 52), (-225, 52)], "acero")
v.rect(-225, 0, 225, 30, "1-SECCION", 18); v.hatch([(-225, 0), (225, 0), (225, 30), (-225, 30)], "mortero")
v.rect(-245, -120, 245, 0, "1-VISTA", 18); v.hatch([(-245, -120), (245, -120), (245, 0), (-245, 0)], "hormigon")
ipn_vertical(v, COL, 0, 52, 160, False, 35)
filete(v, (-150, 52), 8, -1, 1); filete(v, (150, 52), 8, 1, 1)
for xx in (-185, 185):
    v.rect(xx - 10, -120, xx + 10, 52 + 60, "1-VISTA", 13)
    v.rect(xx - 17, 52, xx + 17, 70, "1-VISTA", 25); v.rect(xx - 22, 52 - 4 + 4, xx + 22, 52 + 4 + 0, "1-VISTA", 13)
v.dim((245, 30), (245, 52), 3); v.dim((245, 0), (245, 30), 3)
v.label("CORTE", 0, -170, 1.8, TA.MIDDLE_CENTER, True)
v.ley("filete 8 mm perimetral", (-152, 56), (-14, 8))
v.ley("grout sin contracción", (-225, 15), (-6, -4))
v.ley("arandela-placa + tuerca", (-185, 70), (-10, 12))
ficha_spec(sh, XA, YM - 84, W2, [
    ("Función:", "repartir la carga de la columna sobre el hormigón y recibir los pernos de anclaje."),
    ("Medidas:", "450 x 250 x 22 mm; 4 agujeros Ø26 (perno M20 + 6 mm de tolerancia de montaje)."),
    ("Especificación:", "chapa F-24 soldada en taller a la columna con filete de 8 mm en todo el perímetro del perfil; arandela-placa 50x50x8 sobre cada agujero."),
    ("Colocación:", "se apoya sobre las tuercas de nivelación; se aploma y luego se llena el espacio de 30 mm con grout cementicio sin contracción (fluido)."),
])

# =============================================================== 4. COLUMNA IPN 300 (1:5 y 1:125)
sh.titulo_dib(XB, YM, 4, "COLUMNA IPN 300", "1:5 / 1:125", w=W2)
v = sh.view_in((XB, YM - 82, XB + 46, YM - 10), (-150, -185, 140, 175), 5)
seccion_ipn(v, COL, 0, 0)
h, b, twb, tf = IPN[COL]
v.dim((-b / 2, h / 2), (b / 2, h / 2), 4); v.dim((b / 2, -h / 2), (b / 2, h / 2), 9)
v.ley("tw = 10,8", (twb / 2, -60), (8, -5), 1.6)
v.ln((-b / 2, -h / 2 + tf), (-b / 2 - 30, -h / 2 + tf), "3-COTAS", 9)
v.label("tf = 16,2", -b / 2 - 15, -h / 2 + tf + 6, 1.6, TA.RIGHT)
v.label("SECCIÓN 1:5", 0, -h / 2 - 28, 1.8, TA.MIDDLE_CENTER, True)
v = sh.view_in((XB + 46, YM - 82, XB + W2, YM - 10), (-900, -1250, 2600, 7300), 125)           # elevación de la pieza de taller
v.rect(-150, -330 + 52, 150, N2 - 160, "1-VISTA", 25)
v.rect(-225, -330 + 30, 225, -330 + 52, "1-VISTA", 25)
for z in (N1 - LOSA - 500, N2 - LOSA - 500):
    v.rect(150, z + 80, 260, z + 480, "1-VISTA", 13); v.rect(-260, z + 80, -150, z + 480, "1-VISTA", 13)
v.dim((-225, -278), (-225, N2 - 160), -6)
v.label("ELEVACIÓN 1:125", 0, -1150, 1.8, TA.MIDDLE_CENTER, True)
v.ley("placas de corte", (260, N1 - LOSA - 220), (3, 5), 1.6)
v.ley("placas de corte", (260, N2 - LOSA - 220), (3, -6), 1.6)
v.ley("placa base", (225, -290), (3, 4), 1.6)
ficha_spec(sh, XB, YM - 84, W2, [
    ("Función:", "bajar las cargas de las vigas a la fundación y formar los pórticos."),
    ("Medidas:", "IPN 300: h 300, b 125, tw 10,8, tf 16,2 mm; 54,2 kg/m; A = 69 cm²; Ix = 9800 cm⁴; largo 7,52 m en una sola pieza."),
    ("Especificación:", "acero F-24; llega de taller con placa base, placas de corte y agujeros hechos; antióxido + esmalte."),
])
sh.save("L03_Fundacion_columna")
