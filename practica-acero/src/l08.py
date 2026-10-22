# -*- coding: utf-8 -*-
"""Lámina 08 - Uniones U1 (columna-fundación), U2 (viga principal-columna) y U3 (secundaria-principal)."""
from lib import *
from geom import *

sh = Sheet(8, "Uniones U1 a U3: base, viga principal-columna, secundaria-principal", "PUNTO 2 - JUNTAS Y UNIONES",
           "1:10 - 1:20")
y0 = sh.encabezado("2° UNIONES U1, U2 Y U3", "Detalles a escala de las uniones estructurales principales (ver ubicación en lámina 07)")
L, R = sh.L + 3, sh.R - 3
W2 = (R - L - 6) / 2
XA, XB = L, L + W2 + 6
Y1 = y0 - 3.5

# =============================================================== U1 COLUMNA - FUNDACIÓN
sh.titulo_dib(L, Y1, "U1", "COLUMNA - FUNDACIÓN (PLACA BASE)", "1:10 / 1:20", w=R - L)
TOPP = -330
v = sh.view_in((L, Y1 - 72, L + 72, Y1 - 7), (-380, -720, 330, -60), 10)
v.hatch([(-250, -650), (250, -650), (250, TOPP), (-250, TOPP)], "hormigon"); v.pl([(-250, -650), (-250, TOPP), (250, TOPP), (250, -650)], "1-SECCION", 35)
v.rect(-225, TOPP, 225, TOPP + 30, "1-SECCION", 18); v.hatch([(-225, TOPP), (225, TOPP), (225, TOPP + 30), (-225, TOPP + 30)], "mortero")
v.rect(-225, TOPP + 30, 225, TOPP + 52, "1-SECCION", 35); v.hatch([(-225, TOPP + 30), (225, TOPP + 30), (225, TOPP + 52), (-225, TOPP + 52)], "acero")
ipn_vertical(v, COL, 0, TOPP + 52, -60, False, 35)
filete(v, (-150, TOPP + 52), 8, -1, 1); filete(v, (150, TOPP + 52), 8, 1, 1)
for xx in (-185, 185):
    v.rect(xx - 10, -640, xx + 10, TOPP + 52 + 70, "1-VISTA", 18)
    v.rect(xx - 17, TOPP + 52 + 8, xx + 17, TOPP + 52 + 26, "1-VISTA", 25)
    v.rect(xx - 25, TOPP + 52, xx + 25, TOPP + 52 + 8, "1-VISTA", 18)
    v.rect(xx - 17, TOPP + 2, xx + 17, TOPP + 20, "1-OCULTO", 13)
v.hatch([(-380, -150), (-250, -150), (-250, -60), (-380, -60)], "hormigon"); v.pl([(-380, -60), (-250, -60), (-250, -150), (-380, -150)], "1-VISTA", 18)
v.hatch([(250, -150), (330, -150), (330, -60), (250, -60)], "hormigon"); v.pl([(330, -60), (250, -60), (250, -150), (330, -150)], "1-VISTA", 18)
v.dim((-225, TOPP + 30), (-225, TOPP + 52), -4); v.dim((-225, TOPP), (-225, TOPP + 30), -9)
v.dim((-185, -640), (185, -640), -3)
v.ley("columna IPN 300", (60, -100), (10, 4), 1.5)
v.ley("placa base 450x250x22", (225, TOPP + 41), (4, 6), 1.5)
v.ley("grout sin contracción", (225, TOPP + 15), (4, -2), 1.5)
v.ley("arandela-placa + tuerca", (185, TOPP + 70), (8, 10), 1.5)
v.ley("tuerca de nivelación", (185, TOPP + 11), (6, -8), 1.5)
v.ley("perno M20", (185, -500), (8, 0), 1.5)
v.ley("contrapiso", (300, -100), (2, 3), 1.5)
v.label("CORTE 1:10", -60, -715, 1.5, TA.MIDDLE_CENTER, True)
v = sh.view_in((L + 104, Y1 - 72, L + 150, Y1 - 38), (-250, -200, 250, 170), 20)
v.rect(-225, -125, 225, 125, "1-VISTA", 25)
pts = xf(ipn_poly(*IPN[COL]), 0, 0, 90); v.pl(pts, "1-SECCION", 25, True); v.hatch(pts, "acero")
for cx in (-185, 185):
    for cy in (-85, 85): v.circ((cx, cy), 13, "1-VISTA", 13)
v.label("PLANTA 1:20", 0, -190, 1.4, TA.MIDDLE_CENTER, True)
ficha_spec(sh, L + 104, Y1 - 8, R - L - 104, [
    ("Tipo:", "unión mixta: abulonada (pernos) + húmeda (grout). Placa soldada en taller, pernos en obra."),
    ("Vínculo:", "articulación (4 pernos cerca del alma): transmite compresión, corte y tracción; el giro lo restringen los arriostramientos."),
    ("Montaje:", "tuercas de nivelación a cota; se apoya la columna, se aploma con cuñas/tensores, se ajustan tuercas superiores y se llena con grout (30 mm)."),
    ("Tolerancias:", "plomo ±1/1000; cota ±5 mm."),
], h=1.6, lead=1.36)

# =============================================================== U2 VIGA PRINCIPAL - COLUMNA
Y2 = Y1 - 78
sh.titulo_dib(XA, Y2, "U2", "VIGA PRINCIPAL - COLUMNA", "1:10", w=W2)
v = sh.view_in((XA, Y2 - 92, XA + W2, Y2 - 7), (-300, -700, 560, 150), 10)
ipn_vertical(v, COL, 0, -680, 150, False, 35)
h, b, twb, tf = IPN[VP]
v.pl([(160, 0), (560, 0)], "1-SECCION", 35); v.pl([(160, -h), (560, -h)], "1-SECCION", 35)
v.ln((160, 0), (160, -h), "1-SECCION", 35)
v.ln((160, -tf), (560, -tf), "1-VISTA", 13); v.ln((160, -h + tf), (560, -h + tf), "1-VISTA", 13)
v.rect(150, -450, 270, -50, "1-SECCION", 25); v.hatch([(150, -450), (270, -450), (270, -50), (150, -50)], "gris")
filete(v, (150, -50), 8, 1, 1); filete(v, (150, -450), 8, 1, -1)
for zz in (-370, -290, -210, -130):
    bulon_planta(v, (225, zz), 20)
losa_longitudinal(v, 150, 560, LOSA)
for xx in (300, 450): stud(v, xx, 0)
v.zigzag = None
v.dim((150, -450), (150, -50), -16) if False else None
v.dim((270, -450), (270, -50), 0.01) if False else None
v.dim((560, -370), (560, -130), 5, txt="3 x 80")
v.dim((150, -500), (270, -500), -5)
v.dim((150, -500), (160, -500), -10, txt="10")
v.ley("placa de corte 400x120x10", (250, -60), (8, 18), 1.5)
v.ley("soldada al ala (filete 8)", (154, -46), (-20, 14), 1.5)
v.ley("4 bulones M20 8.8", (225, -290), (14, -26), 1.5)
v.ley("columna IPN 300", (-100, -600), (-2, -4), 1.5)
v.ley("viga IPN 500", (480, -h + 60), (2, -8), 1.5)
v.label("VISTA LATERAL 1:10", 80, -690, 1.5, TA.MIDDLE_CENTER, True)
ficha_spec(sh, XA, Y2 - 94, W2, [
    ("Tipo:", "seca, abulonada; placa soldada en taller (control de calidad) y bulones en obra."),
    ("Vínculo:", "articulada a corte: la placa fina y flexible permite el giro del extremo de la viga."),
    ("Montaje:", "la viga se baja con grúa, se presenta con 2 bulones de montaje y punzón, se aploma y se colocan todos."),
    ("Junta:", "10 mm entre viga y columna para tolerancia."),
], h=1.6, lead=1.36)

# =============================================================== U3 SECUNDARIA - PRINCIPAL
sh.titulo_dib(XB, Y2, "U3", "VIGA SECUNDARIA - VIGA PRINCIPAL", "1:10", w=W2)
v = sh.view_in((XB, Y2 - 92, XB + W2, Y2 - 7), (-320, -700, 560, 150), 10)
seccion_ipn(v, VP, 0, -h / 2)
hs, bs, tws, tfs = IPN[VS]
x0 = twb / 2 + 12
v.pl([(x0, -200), (x0, -40), (x0 + 90, -40), (x0 + 90, 0), (560, 0)], "1-SECCION", 35)
v.ln((x0, -200), (560, -200), "1-SECCION", 35)
v.ln((x0 + 90, -tfs), (560, -tfs), "1-VISTA", 13); v.ln((x0, -200 + tfs), (560, -200 + tfs), "1-VISTA", 13)
v.rect(twb / 2, -170, twb / 2 + 76, -30, "1-SECCION", 25); v.hatch([(twb / 2, -170), (twb / 2 + 76, -170), (twb / 2 + 76, -30), (twb / 2, -30)], "gris")
for zz in (-135, -65):
    v.circ((twb / 2 + 45, zz), 9, "1-VISTA", 18)
    bulon(v, (-twb / 2 - 8, zz), (twb / 2 + 8, zz), 16)
losa_transversal(v, -320, 560, LOSA, 0)
stud(v, 0, 0)
v.ley("doble ángulo L 76x76x8", (twb / 2 + 60, -160), (16, -12), 1.5)
v.ley("2 bulones M16 (al alma ppal.)", (-30, -65), (-8, -8), 1.5)
v.ley("2 bulones M16 (al alma sec.)", (twb / 2 + 45, -135), (18, -22), 1.5)
v.ley("destaje del ala", (x0 + 45, -40), (14, -8), 1.5)
v.ley("viga IPN 500 (cortada)", (-80, -420), (-2, -6), 1.5)
v.ley("viga IPN 200", (545, -180), (-6, 6), 1.5)
v.label("CORTE 1:10", 120, -690, 1.5, TA.MIDDLE_CENTER, True)
ficha_spec(sh, XB, Y2 - 94, W2, [
    ("Tipo:", "seca, abulonada en obra; ángulos abulonados a la secundaria en taller."),
    ("Vínculo:", "articulada (simplemente apoyada): solo transmite corte."),
    ("Detalle:", "la secundaria lleva destaje del ala superior para quedar enrasada con la principal y apoyar la chapa en el mismo plano."),
    ("Montaje:", "se izan de a 2 o 3 vigas por eslinga."),
], h=1.6, lead=1.36)

# =============================================================== funcionamiento de las uniones
Y3 = Y2 - 110
sh.titulo_dib(L, Y3, "F", "CÓMO TRABAJAN LAS UNIONES (ESQUEMAS S/ ESC.)", w=R - L)
def esquema(x0, y0, horiz):
    w, hh = 44, 18
    c = [(x0, y0), (x0, y0 + hh), (x0 + w, y0 + hh), (x0 + w, y0)]
    sh.pl(c, "1-SECCION", 35)
    for px in (x0, x0 + w):
        sh.pl([(px, y0), (px - 2, y0 - 3), (px + 2, y0 - 3)], "1-VISTA", 18, True)
        sh.circ((px, y0), 0.8, "1-VISTA", 18)
    for px in (x0, x0 + w): sh.circ((px, y0 + hh), 0.9, "1-VISTA", 18)
    if horiz:
        sh.pl([(x0, y0), (x0 + w, y0 + hh)], "1-VISTA", 13); sh.pl([(x0 + w, y0), (x0, y0 + hh)], "1-OCULTO", 13)
        sh.pl([(x0 - 14, y0 + hh), (x0 - 2, y0 + hh)], "3-REFS", 25); sh.pl([(x0 - 4, y0 + hh + 1.2), (x0 - 2, y0 + hh), (x0 - 4, y0 + hh - 1.2)], "3-REFS", 25)
        sh.txt("viento", x0 - 14, y0 + hh + 1, 1.5)
    else:
        for i in range(8):
            px = x0 + 4 + i * 5.1
            sh.pl([(px, y0 + hh + 7), (px, y0 + hh + 1)], "3-REFS", 13); sh.pl([(px - 0.8, y0 + hh + 2.4), (px, y0 + hh + 1), (px + 0.8, y0 + hh + 2.4)], "3-REFS", 13)
        sh.pl([(x0, y0 + hh + 7), (x0 + w, y0 + hh + 7)], "3-REFS", 13)
esquema(L + 3, Y3 - 34, False)
esquema(XB + 14 - 8, Y3 - 34, True)
sh.para(L + 82 - 0, Y3 - 8, 6, "") if False else None
ficha_spec(sh, L + 50, Y3 - 6, W2 - 50, [
    ("Verticales:", "losa -> studs (U4) -> secundaria -> doble ángulo (U3) -> principal -> placa de corte (U2) -> columna -> placa base y pernos (U1) -> base."),
    ("Articuladas:", "uniones simples, rápidas y baratas; la viga se calcula simplemente apoyada (12 m) y la columna solo a compresión."),
], h=1.6, lead=1.36)
ficha_spec(sh, XB + 54, Y3 - 6, W2 - 54, [
    ("Horizontales:", "fachada -> losa (diafragma, U5) -> vigas -> cruces de San Andrés (U7) -> columnas -> fundación (U1)."),
    ("Sin cruces:", "el pórtico articulado sería un mecanismo: por eso las cruces se montan antes del apriete final."),
], h=1.6, lead=1.36)
sh.save("L08_Uniones_U1_U3")
