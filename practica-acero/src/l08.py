# -*- coding: utf-8 -*-
"""Lámina 08 - Uniones U1 (columna-fundación), U2 (viga principal-columna) y U3 (secundaria-principal)."""
from lib import *
from geom import *

sh = Sheet(NUM["u13"], "Uniones U1, U2, U3 y funcionamiento", "PUNTO 2 - JUNTAS Y UNIONES", "1:10 - 1:20", hmin=2.3)
y0 = sh.encabezado("2° UNIONES U1, U2 Y U3", f"Detalles a escala de las uniones estructurales principales (ver ubicación en lámina {lam('uesq')})")
L, R = sh.L + 3, sh.R - 3
W2 = (R - L - 6) / 2
XA, XB = L, L + W2 + 6
Y1 = y0 - 3.5

# =============================================================== U1 COLUMNA - FUNDACIÓN
sh.titulo_dib(L, Y1, "U1", "COLUMNA - FUNDACIÓN (PLACA BASE)", "1:10 / 1:20", w=R - L)
TOPP = -330
A2 = PL_A / 2; ZP0, ZP1 = TOPP + 30, TOPP + 30 + PL_E; hc = IPN[COL][0]
v = sh.view_in((L, Y1 - 70, L + 72, Y1 - 7), (-330, -720, 300, -60), 10)
v.hatch([(-250, -650), (250, -650), (250, TOPP), (-250, TOPP)], "hormigon"); v.pl([(-250, -650), (-250, TOPP), (250, TOPP), (250, -650)], "1-SECCION", 35)
v.rect(-A2, TOPP, A2, ZP0, "1-SECCION", 18); v.hatch([(-A2, TOPP), (A2, TOPP), (A2, ZP0), (-A2, ZP0)], "mortero")
v.rect(-A2, ZP0, A2, ZP1, "1-SECCION", 35); v.hatch([(-A2, ZP0), (A2, ZP0), (A2, ZP1), (-A2, ZP1)], "acero")
ipn_vertical(v, COL, 0, ZP1, -60, False, 35)
filete(v, (-hc / 2, ZP1), 8, -1, 1); filete(v, (hc / 2, ZP1), 8, 1, 1)
for xx in (-PX, PX):
    v.rect(xx - 10, -640, xx + 10, ZP1 + 70, "1-VISTA", 18)
    v.rect(xx - 17, ZP1 + 8, xx + 17, ZP1 + 26, "1-VISTA", 25)
    v.rect(xx - 25, ZP1, xx + 25, ZP1 + 8, "1-VISTA", 18)
    v.rect(xx - 17, TOPP + 2, xx + 17, TOPP + 20, "1-OCULTO", 13)
v.hatch([(-330, -150), (-250, -150), (-250, -60), (-330, -60)], "hormigon"); v.pl([(-330, -60), (-250, -60), (-250, -150), (-330, -150)], "1-VISTA", 18)
v.hatch([(250, -150), (300, -150), (300, -60), (250, -60)], "hormigon"); v.pl([(300, -60), (250, -60), (250, -150), (300, -150)], "1-VISTA", 18)
v.dim((-A2, ZP0), (-A2, ZP1), -4); v.dim((-A2, TOPP), (-A2, ZP0), -9)
v.dim((-PX, -640), (PX, -640), -3)
v.ley("columna HEB 200", (40, -100), (12, 4))
v.ley("placa base 380x250x20", (A2, ZP0 + 10), (4, 7))
v.ley("grout sin contracción", (A2, TOPP + 15), (4, -2))
v.ley("arandela-placa + tuerca", (PX, ZP1 + 20), (8, 13))
v.ley("tuerca de nivelación", (PX, TOPP + 11), (6, -8))
v.ley("perno M20", (PX, -500), (8, 0))
v.label("CORTE 1:10", -30, -705, 2.0, TA.MIDDLE_CENTER, True)
yb = ficha_spec(sh, L + 94, Y1 - 8, R - L - 94, [
    ("Tipo:", "unión mixta: abulonada (pernos) + húmeda (grout). Placa soldada en taller, pernos en obra."),
    ("Vínculo:", "articulación: transmite compresión, corte y tracción; el giro lo toman los arriostramientos."),
    ("Montaje:", "tuercas de nivelación a cota; se apoya la columna, se aploma, se ajustan las tuercas y se llena con grout."),
    ("Tolerancias:", "plomo ±1/1000; cota ±5 mm."),
], h=2.0, lead=1.38)
v = sh.view_in((L + 94, Y1 - 72, L + 140, yb - 2), (-210, -200, 210, 140), 20)
v.rect(-A2, -PL_B / 2, A2, PL_B / 2, "1-VISTA", 25)
pts = xf(perfil_poly(COL), 0, 0, 90); v.pl(pts, "1-SECCION", 25, True); v.hatch(pts, "acero")
for cx in (-PX, PX):
    for cy in (-PY, PY): v.circ((cx, cy), 13, "1-VISTA", 13)
v.label("PLANTA 1:20", 0, -185, 2.0, TA.MIDDLE_CENTER, True)

# =============================================================== U2 VIGA PRINCIPAL - COLUMNA
Y2 = Y1 - 78
sh.titulo_dib(XA, Y2, "U2", "VIGA PRINCIPAL - COLUMNA", "1:10", w=W2)
v = sh.view_in((XA, Y2 - 92, XA + W2, Y2 - 7), (-250, -700, 560, 150), 10)
ipn_vertical(v, COL, 0, -680, 150, False, 35)
h, b, twb, tf = IPN[VP]
v.pl([(110, 0), (560, 0)], "1-SECCION", 35); v.pl([(110, -h), (560, -h)], "1-SECCION", 35)
v.ln((110, 0), (110, -h), "1-SECCION", 35)
v.ln((110, -tf), (560, -tf), "1-VISTA", 13); v.ln((110, -h + tf), (560, -h + tf), "1-VISTA", 13)
v.rect(100, -410, 220, -90, "1-SECCION", 25); v.hatch([(100, -410), (220, -410), (220, -90), (100, -90)], "gris")
filete(v, (100, -90), 8, 1, 1); filete(v, (100, -410), 8, 1, -1)
for zz in (-370, -290, -210, -130):
    bulon_planta(v, (165, zz), 20)
losa_longitudinal(v, 100, 560, LOSA)
for xx in (300, 450): stud(v, xx, 0)
v.zigzag = None
v.dim((150, -450), (150, -50), -16) if False else None
v.dim((270, -450), (270, -50), 0.01) if False else None
v.dim((560, -370), (560, -130), 5, txt="3 x 80")
v.dim((100, -500), (220, -500), -5)
v.dim((100, -500), (110, -500), -10, txt="10")
v.ley("placa de corte 320x120x10", (215, -110), (18, -4))
v.ley("filete 8 al ala", (104, -86), (-10, 18))
v.ley("4 bulones M20 8.8", (172, -290), (20, -6))
v.ley("columna HEB 200", (-60, -600), (3, -6))
v.ley("viga IPN 500", (480, -h), (-4, -6))
v.label("VISTA LATERAL 1:10", 200, -690, 2.0, TA.MIDDLE_CENTER, True)
ficha_spec(sh, XA, Y2 - 95, W2, [
    ("Tipo:", "seca, abulonada; placa soldada en taller (control de calidad) y bulones en obra."),
    ("Vínculo:", "articulada a corte: la placa fina y flexible permite el giro del extremo de la viga."),
    ("Montaje:", "la viga se baja con grúa, se presenta con 2 bulones de montaje y punzón, se aploma y se colocan todos."),
    ("Junta:", "10 mm entre viga y columna para tolerancia."),
], h=2.0, lead=1.36)

# =============================================================== U3 SECUNDARIA - PRINCIPAL
sh.titulo_dib(XB, Y2, "U3", "VIGA SECUNDARIA - PRINCIPAL", "1:10", w=W2)
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
v.ley("2 L 76x76x8", (twb / 2 + 60, -160), (16, -12))
v.ley("2 M16 al alma ppal.", (-30, -65), (-2, -26))
v.ley("2 M16 al alma sec.", (twb / 2 + 45, -135), (12, -26))
v.ley("destaje del ala", (x0 + 45, -40), (16, -6))
v.ley("IPN 500 (cortada)", (-60, -440), (-2, -10))
v.ley("IPN 200", (545, -180), (-4, -40))
v.label("CORTE 1:10", 120, -690, 2.0, TA.MIDDLE_CENTER, True)
ficha_spec(sh, XB, Y2 - 95, W2, [
    ("Tipo:", "seca, abulonada en obra; ángulos abulonados a la secundaria en taller."),
    ("Vínculo:", "articulada (simplemente apoyada): solo transmite corte."),
    ("Detalle:", "destaje del ala superior para quedar enrasada con la principal (la chapa apoya en un solo plano)."),
    ("Montaje:", "se izan de a 2 o 3 vigas por eslinga."),
], h=2.0, lead=1.36)

# =============================================================== funcionamiento de las uniones
Y3 = Y2 - 130
sh.titulo_dib(L, Y3, "F", "CÓMO TRABAJAN LAS UNIONES (ESQUEMAS S/ ESC.)", w=R - L)
def esquema(x0, y0, horiz):
    w, hh = 34, 16
    c = [(x0, y0), (x0, y0 + hh), (x0 + w, y0 + hh), (x0 + w, y0)]
    sh.pl(c, "1-SECCION", 35)
    for px in (x0, x0 + w):
        sh.pl([(px, y0), (px - 2, y0 - 3), (px + 2, y0 - 3)], "1-VISTA", 18, True)
        sh.circ((px, y0), 0.8, "1-VISTA", 18)
    for px in (x0, x0 + w): sh.circ((px, y0 + hh), 0.9, "1-VISTA", 18)
    if horiz:
        sh.pl([(x0, y0), (x0 + w, y0 + hh)], "1-VISTA", 13); sh.pl([(x0 + w, y0), (x0, y0 + hh)], "1-OCULTO", 13)
        sh.pl([(x0 - 14, y0 + hh), (x0 - 2, y0 + hh)], "3-REFS", 25); sh.pl([(x0 - 4, y0 + hh + 1.2), (x0 - 2, y0 + hh), (x0 - 4, y0 + hh - 1.2)], "3-REFS", 25)
        sh.txt("viento", x0 - 14, y0 + hh + 1, 2.0)
    else:
        for i in range(8):
            px = x0 + 3 + i * 4.0
            sh.pl([(px, y0 + hh + 7), (px, y0 + hh + 1)], "3-REFS", 13); sh.pl([(px - 0.8, y0 + hh + 2.4), (px, y0 + hh + 1), (px + 0.8, y0 + hh + 2.4)], "3-REFS", 13)
        sh.pl([(x0, y0 + hh + 7), (x0 + w, y0 + hh + 7)], "3-REFS", 13)
esquema(L + 1, Y3 - 34, False)
esquema(XB + 14, Y3 - 34, True)
sh.para(L + 82 - 0, Y3 - 8, 6, "") if False else None
ficha_spec(sh, L + 38, Y3 - 8, W2 - 38, [
    ("Verticales:", "losa > studs (U4) > secundaria > U3 > principal > U2 > columna > U1 > base."),
], h=2.0, lead=1.36)
ficha_spec(sh, XB + 51, Y3 - 8, W2 - 51, [
    ("Viento:", "losa (diafragma) > cruces (U7) > columnas > U1. Sin cruces, el pórtico articulado se cae."),
], h=2.0, lead=1.36)
sh.save(f"L{lam('u13')}_Uniones_U1_U3")
