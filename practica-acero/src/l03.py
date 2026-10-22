# -*- coding: utf-8 -*-
"""Lámina 03 - Elementos 1: base aislada, pernos de anclaje, placa base y columna HEB 200."""
from lib import *
from geom import *

sh = Sheet(NUM["fund"], "Fundación, pernos de anclaje, placa base y columna", "PUNTO 1 - ELEMENTOS CONSTRUCTIVOS",
           "1:25 - 1:10 - 1:20 - 1:5 - 1:125")
y0 = sh.encabezado("1° ELEMENTOS: FUNDACIÓN Y COLUMNA", "Croquis a escala con medidas, función y especificación técnica")
L, R = sh.L + 3, sh.R - 3
W2 = (R - L - 6) / 2
XA, XB = L, L + W2 + 6
YT, YM = y0 - 3.5, y0 - 135
A2, B2 = PL_A / 2, PL_B / 2            # semilados de la placa base
TOPP = -330                            # coronamiento del pedestal
ZP0, ZP1 = TOPP + 30, TOPP + 30 + PL_E  # placa base (sobre 30 mm de grout)
hc, bc, twc, tfc = IPN[COL]
BT = FUND + BASE_E                     # cara superior de la base

# =============================================================== 1. BASE AISLADA (1:25)
sh.titulo_dib(XA, YT, 1, "BASE AISLADA H°A° + PEDESTAL", "1:25", w=W2)
v = sh.view_in((XA, YT - 92, XA + W2, YT - 8), (-1220, -1620, 920, 330), 25)
v.ln((-900, -150), (-260, -150), "1-VISTA", 25); v.ln((260, -150), (900, -150), "1-VISTA", 25)
v.hatch([(-900, -150), (-260, -150), (-260, 0), (-900, 0)], "hormigon"); v.rect(-900, -150, -260, 0, "1-SECCION", 25)
v.hatch([(260, -150), (900, -150), (900, 0), (260, 0)], "hormigon"); v.rect(260, -150, 900, 0, "1-SECCION", 25)
v.hatch([(-900, -150), (-850, -150), (-850, -1600), (-900, -1600)], "tierra")
v.hatch([(850, -150), (900, -150), (900, -1600), (850, -1600)], "tierra")
base = [(-BASE / 2, FUND), (BASE / 2, FUND), (BASE / 2, BT), (250, BT), (250, TOPP), (-250, TOPP), (-250, BT), (-BASE / 2, BT)]
v.hatch(base, "hormigon"); v.pl(base, "1-SECCION", 50, True)
v.rect(-850, FUND - 50, 850, FUND, "1-SECCION", 18); v.hatch([(-850, FUND - 50), (850, FUND - 50), (850, FUND), (-850, FUND)], "gris")
# armaduras: parrilla inferior y barras del pedestal
v.ln((-750, FUND + 50), (750, FUND + 50), "1-VISTA", 35)
for xx in range(-700, 701, 140): v.circ((xx, FUND + 70), 12, "1-VISTA", 13)
for xx in (-200, 200):
    v.pl([(xx + (-150 if xx < 0 else 150), FUND + 60), (xx, FUND + 60), (xx, TOPP - 50)], "1-VISTA", 35)
for zz in range(int(BT + 50), int(TOPP - 40), 150): v.rect(-205, zz, 205, zz + 4, "1-VISTA", 13)
# grout, placa y columna
v.rect(-A2, TOPP, A2, ZP0, "1-SECCION", 18); v.hatch([(-A2, TOPP), (A2, TOPP), (A2, ZP0), (-A2, ZP0)], "mortero")
v.rect(-A2, ZP0, A2, ZP1, "1-SECCION", 35); v.hatch([(-A2, ZP0), (A2, ZP0), (A2, ZP1), (-A2, ZP1)], "acero")
ipn_vertical(v, COL, 0, ZP1, 300, False, 35)
# pernos
for xx in (-PX, PX):
    v.rect(xx - 10, TOPP - 520, xx + 10, ZP1 + 60, "1-VISTA", 18)
    v.rect(xx - 40, TOPP - 530, xx + 40, TOPP - 520, "1-VISTA", 25)
    v.rect(xx - 17, ZP1, xx + 17, ZP1 + 18, "1-VISTA", 25)
# cotas y niveles
v.dim((-BASE / 2, FUND), (BASE / 2, FUND), -5)
v.dim((-250, BT), (250, BT), 3)
v.dim((-BASE / 2, FUND), (-BASE / 2, BT), -3)
v.dim((-BASE / 2, BT), (-BASE / 2, TOPP), -3)
v.nivel(-950, 0, "±0,00", -1); v.nivel(-950, FUND, "-1,50", -1); v.nivel(-950, TOPP, "-0,33", -1)
for n, at, off in [(1, (650, FUND + 250), (8, 9)), (2, (PX, TOPP - 330), (14, -3)), (3, (A2, ZP0 + 10), (14, 5)),
                   (4, (0, 250), (11, 2))]:
    v.ref(n, at, off)
v.ley("H° limpieza e = 5 cm", (650, FUND - 25), (2, -5))
v.ley("parrilla Ø12 c/14", (-500, FUND + 50), (-2, 14))
v.ley("grout e = 30", (-A2, TOPP + 15), (-6, 10))
ficha_spec(sh, XA, YT - 95, W2, [
    ("Función:", "transmitir al suelo la carga de la columna (≈ 300 kN de compresión, más corte y tracción del arriostramiento)."),
    ("Medidas:", "base 1,60 x 1,60 x 0,45 m (≈ 1,3 kg/cm² sobre el suelo); pedestal 0,50 x 0,50 m hasta -0,33; fondo -1,50 (según estudio de suelos)."),
    ("Especificación:", "H-25 colado en obra, ADN 420: parrilla Ø12 c/14 en ambos sentidos, pedestal 8 Ø16 + estribos Ø8 c/15; recubrimiento 5 cm; H° de limpieza 5 cm."),
    ("Colocación:", "los pernos se dejan colados con plantilla antes de hormigonar; la placa queda bajo el contrapiso."),
])

# =============================================================== 2. PERNOS DE ANCLAJE (1:10) + PLANTILLA (1:20)
sh.titulo_dib(XB, YT, 2, "PERNOS M20 + PLANTILLA", "1:10 / 1:20", w=W2)
v = sh.view_in((XB, YT - 92, XB + 52, YT - 8), (-330, -30, 130, 620), 10)
Lp = 600
v.rect(-10, 0, 10, Lp, "1-SECCION", 25); v.hatch([(-10, 0), (10, 0), (10, Lp), (-10, Lp)], "gris")
for zz in range(Lp - 150, Lp, 6): v.ln((-10, zz), (10, zz + 3), "1-VISTA", 9)
v.rect(-40, -10, 40, 0, "1-SECCION", 25); v.rect(-17, 0, 17, 16, "1-VISTA", 25)       # placa de anclaje + tuerca
for z0 in (Lp - 150, Lp - 106):                                                     # tuerca de nivelación / superior
    v.rect(-17, z0, 17, z0 + 16, "1-VISTA", 25)
v.rect(-22, Lp - 134, 22, Lp - 126, "1-VISTA", 18)                                    # arandela de nivelación
v.rect(-112, Lp - 126, 112, Lp - 106, "1-OCULTO", 13)                                 # placa base (fantasma)
v.ln((-60, Lp - 160), (60, Lp - 160), "1-OCULTO", 13)
v.dim((40, -10), (40, Lp), 5)
v.dim((40, Lp - 150), (40, Lp), 9)
v.dim((-40, -10), (40, -10), -4)
v.ref(2, (0, 300), (-8, 0))
v.ley("tuerca + arandela", (-17, Lp - 98), (-4, 5))
v.ley("tuerca de nivelación", (-17, Lp - 142), (-4, -3))
v.ley("sup. pedestal", (-60, Lp - 160), (-2, -8))
v.ley("rosca 150", (-10, Lp - 40), (-6, 3))
v.ley("placa de anclaje 80x80x10", (-40, -5), (-2, 6))
v2 = sh.view_in((XB + 52, YT - 62, XB + W2, YT - 10), (-250, -330, 260, 200), 20)
v2.rect(-210, -130, 210, 130, "1-VISTA", 25); v2.hatch([(-210, -130), (210, -130), (210, 130), (-210, 130)], "madera")
for cx in (-PX, PX):
    for cy in (-PY, PY):
        v2.circ((cx, cy), 13, "1-SECCION", 25)
v2.ln((-250, 0), (250, 0), "1-EJES", 9); v2.ln((0, -160), (0, 160), "1-EJES", 9)
v2.dim((-PX, 130), (PX, 130), 3); v2.dim((210, -PY), (210, PY), 3)
v2.label("PLANTILLA 1:20", 0, -195, 2.0, TA.MIDDLE_CENTER, True)
v2.label("fenólico 18 mm", 0, -255, 2.0, TA.MIDDLE_CENTER)
v2.label("(fija los pernos)", 0, -315, 2.0, TA.MIDDLE_CENTER)
ficha_spec(sh, XB, YT - 95, W2, [
    ("Función:", "anclar la columna a la fundación y tomar el corte y la tracción (arrancamiento) en la base."),
    ("Medidas:", "barra roscada M20, largo 600 mm, rosca 150 mm, saliente 110 mm sobre el pedestal; 4 por columna a 300 x 120 mm."),
    ("Especificación:", "acero F-24 galvanizado en caliente; placa de anclaje 80x80x10; 3 tuercas y arandela por perno."),
    ("Colocación:", "plantilla de fenólico; tolerancia ±3 mm en planta y ±5 mm en altura; proteger la rosca hasta el montaje."),
])

# =============================================================== 3. PLACA BASE (1:10)
sh.titulo_dib(XA, YM, 3, f"PLACA BASE {PL_A} x {PL_B} x {PL_E}", "1:10", w=W2)
v = sh.view_in((XA, YM - 46, XA + W2, YM - 9), (-215, -195, 255, 165), 10)            # planta
v.rect(-A2, -B2, A2, B2, "1-VISTA", 35)
pts = xf(perfil_poly(COL), 0, 0, 90)
v.pl(pts, "1-SECCION", 35, True); v.hatch(pts, "acero")
for cx in (-PX, PX):
    for cy in (-PY, PY):
        bulon_planta(v, (cx, cy), 20)
v.dim((-A2, B2), (A2, B2), 4); v.dim((A2, -B2), (A2, B2), 5)
v.dim((-PX, -B2), (PX, -B2), -4); v.dim((A2, -PY), (A2, PY), 12)
v.label("PLANTA", 0, -185, 2.0, TA.MIDDLE_CENTER, True)
v = sh.view_in((XA, YM - 86, XA + W2, YM - 48), (-480, -190, 255, 170), 10, ha="r")            # corte
v.rect(-A2, 30, A2, 30 + PL_E, "1-SECCION", 35); v.hatch([(-A2, 30), (A2, 30), (A2, 30 + PL_E), (-A2, 30 + PL_E)], "acero")
v.rect(-A2, 0, A2, 30, "1-SECCION", 18); v.hatch([(-A2, 0), (A2, 0), (A2, 30), (-A2, 30)], "mortero")
v.rect(-245, -120, 245, 0, "1-VISTA", 18); v.hatch([(-245, -120), (245, -120), (245, 0), (-245, 0)], "hormigon")
ipn_vertical(v, COL, 0, 30 + PL_E, 160, False, 35)
filete(v, (-hc / 2, 30 + PL_E), 8, -1, 1); filete(v, (hc / 2, 30 + PL_E), 8, 1, 1)
for xx in (-PX, PX):
    v.rect(xx - 10, -120, xx + 10, 30 + PL_E + 60, "1-VISTA", 13)
    v.rect(xx - 17, 30 + PL_E + 8, xx + 17, 30 + PL_E + 26, "1-VISTA", 25); v.rect(xx - 25, 30 + PL_E, xx + 25, 30 + PL_E + 8, "1-VISTA", 13)
v.dim((245, 30), (245, 30 + PL_E), 3); v.dim((245, 0), (245, 30), 3)
v.label("CORTE", 0, -170, 2.0, TA.MIDDLE_CENTER, True)
v.ley("filete 8 mm perimetral", (-hc / 2 - 2, 30 + PL_E + 4), (-16, 9))
v.ley("grout sin contracción", (-A2, 15), (-6, -4))
v.ley("arandela-placa + tuerca", (-PX, 30 + PL_E + 18), (-14, 15))
ficha_spec(sh, XA, YM - 89, W2, [
    ("Función:", "repartir la carga de la columna sobre el hormigón y recibir los pernos de anclaje."),
    ("Medidas:", f"{PL_A} x {PL_B} x {PL_E} mm; 4 agujeros Ø26 (perno M20 + 6 mm de tolerancia de montaje), a 40 mm del borde."),
    ("Especificación:", "chapa F-24 soldada en taller a la columna con filete de 8 mm en todo el contorno del perfil; arandela-placa 50x50x8 en cada perno."),
    ("Colocación:", "se apoya sobre las tuercas de nivelación, se aploma y se llenan los 30 mm con grout cementicio sin contracción (fluido)."),
])

# =============================================================== 4. COLUMNA HEB 200 (1:5 y 1:125)
sh.titulo_dib(XB, YM, 4, "COLUMNA HEB 200", "1:5 / 1:125", w=W2)
v = sh.view_in((XB, YM - 70, XB + 60, YM - 9), (-160, -150, 140, 135), 5)
seccion_ipn(v, COL, 0, 0)
v.dim((-bc / 2, hc / 2), (bc / 2, hc / 2), 4); v.dim((bc / 2, -hc / 2), (bc / 2, hc / 2), 6)
v.ley("tw = 9", (twc / 2, -40), (10, -4))
v.ley("tf = 15", (-bc / 2 + 30, -hc / 2 + tfc / 2), (-6, -9))
v.label("SECCIÓN 1:5", 0, -hc / 2 - 40, 2.0, TA.MIDDLE_CENTER, True)
v = sh.view_in((XB + 60, YM - 86, XB + W2, YM - 9), (-700, -1200, 2000, 7300), 125)           # pieza de taller
v.rect(-hc / 2, ZP1, hc / 2, N2 - 160, "1-VISTA", 25)
v.rect(-A2, ZP0, A2, ZP1, "1-VISTA", 25)
for z in (N1 - LOSA - 500, N2 - LOSA - 500):
    v.rect(hc / 2, z + 50, hc / 2 + 120, z + 450, "1-VISTA", 13); v.rect(-hc / 2 - 120, z + 50, -hc / 2, z + 450, "1-VISTA", 13)
v.dim((-A2, ZP1), (-A2, N2 - 160), -6)
v.label("ELEVACIÓN 1:125", 600, -1100, 2.0, TA.MIDDLE_CENTER, True)
v.ley("placas de corte", (hc / 2 + 120, N2 - LOSA - 280), (-24, 9))
v.ley("placa base", (A2, ZP0), (3, 5))
ficha_spec(sh, XB, YM - 72, 60, [
    ("HEB 200:", "h 200, b 200, tw 9, tf 15 mm; 61,3 kg/m; A = 78,1 cm²; i mín. = 5,07 cm."),
], h=2.0, lead=1.38)
ficha_spec(sh, XB, YM - 89, W2, [
    ("Función:", "bajar las cargas de las vigas a la fundación y formar los pórticos."),
    ("Por qué HEB:", "alas anchas y paralelas: con 3,66 m entre losas la esbeltez es 72 (un IPN 300 daría 143 y pandearía)."),
    ("Especificación:", "acero F-24; pieza única de 7,52 m; llega de taller con placa base, placas de corte y agujeros; antióxido + esmalte."),
])
sh.save(f"L{lam('fund')}_Fundacion_columna")
