# -*- coding: utf-8 -*-
"""Lámina 10 - Uniones U8 (panel sándwich - estructura), U9 (muro cortina - losa), U10 (cubierta - parapeto)."""
from lib import *
from geom import *

sh = Sheet(NUM["u810"], "Uniones U8 a U10: cerramientos a la estructura y cubierta", "PUNTO 2 - JUNTAS Y UNIONES", "1:5 - 1:10", hmin=2.4)
y0 = sh.encabezado("2° UNIONES U8, U9 Y U10", f"Juntas entre los cerramientos (opaco y vidriado) y la estructura de acero (ver lámina {lam('uesq')})")
L, R = sh.L + 3, sh.R - 3
W2 = (R - L - 6) / 2
XA, XB = L, L + W2 + 6
Y1 = y0 - 3.5
EP = 80                                     # espesor del panel

# =============================================================== U8 PANEL - ESTRUCTURA
sh.titulo_dib(L, Y1, "U8", "PANEL SÁNDWICH 80 - ESTRUCTURA", "1:5", w=R - L)
# planta: junta vertical sobre columna (x = hacia afuera, y = a lo largo de la fachada)
v = sh.view_in((L, Y1 - 82, L + 88, Y1 - 8), (-140, -190, 150, 180), 5)
v.pl([(-140, -100), (0, -100), (0, 100), (-140, 100)], "1-SECCION", 35)       # ala de la columna HEB 200 (corte)
v.hatch([(-15, -100), (0, -100), (0, 100), (-15, 100)], "acero")
v.ln((-15, -100), (-15, 100), "1-SECCION", 25)
v.hatch([(-140, -4.5), (-15, -4.5), (-15, 4.5), (-140, 4.5)], "acero"); v.pl([(-140, -4.5), (-15, -4.5)], "1-SECCION", 25); v.pl([(-140, 4.5), (-15, 4.5)], "1-SECCION", 25)
v.rect(0, -50, 20, 50, "1-SECCION", 35); v.rect(2, -48, 18, 48, "1-VISTA", 13)                    # montante tubo 100x20x2
filete(v, (0, 50), 4, 1, 1); filete(v, (0, -50), 4, 1, -1)
for sgn in (-1, 1):
    y_in, y_out = sgn * 5, sgn * 165
    pp = [(20, y_in), (20, y_out), (20 + EP, y_out), (20 + EP, y_in)]
    v.hatch(pp, "aislacion")
    v.pl([(20, y_out), (20, y_in), (20 + EP, y_in), (20 + EP, y_out)], "1-SECCION", 35)
    v.ln((20.5, y_in), (20.5, y_out), "1-VISTA", 9); v.ln((20 + EP - 0.5, y_in), (20 + EP - 0.5, y_out), "1-VISTA", 9)
    bulon(v, (20 + EP + 4, sgn * 30), (2, sgn * 30), 6, cab=3, tuerca=False, lw=13)
v.rect(20 + EP, -40, 20 + EP + 2, 40, "1-SECCION", 25)
v.rect(20 + EP - 15, -5, 20 + EP, 5, "1-VISTA", 13); v.hatch([(20 + EP - 15, -5), (20 + EP, -5), (20 + EP, 5), (20 + EP - 15, 5)], "negro")
v.ley("columna HEB 200", (-80, 60), (-2, 22), 1.5)
v.ley("montante tubo 100x20x2", (10, -48), (-6, -14), 1.5)
v.ley("panel PUR 80", (60, 140), (14, 4), 1.5)
v.ley("autoperforante Ø6,3 + EPDM", (90, 30), (16, 10), 1.5)
v.ley("sellador PU + respaldo", (92, 0), (16, -2), 1.5)
v.ley("tapajunta prepintado", (101, -30), (14, -12), 1.5)
v.label("PLANTA - JUNTA VERTICAL 1:5", 0, -185, 1.5, TA.MIDDLE_CENTER, True)
# corte: arranque sobre viga portapanel
v = sh.view_in((L + 94, Y1 - 82, R, Y1 - 8), (-140, -160, 140, 210), 5)
v.rect(-60, -100, 0, 0, "1-SECCION", 35); v.rect(-57, -97, -3, -3, "1-VISTA", 13)                # viga portapanel 100x60 (girada)
v.hatch([(-60, -100), (0, -100), (0, -97), (-60, -97)], "negro")
v.hatch([(-140, -160), (-60, -160), (-60, -10), (-140, -10)], "hormigon"); v.pl([(-140, -10), (-60, -10)], "1-SECCION", 25)
v.hatch([(-60, -160), (100, -160), (100, -100), (-60, -100)], "hormigon"); v.pl([(-60, -100), (140, -100)], "1-SECCION", 25)
v.pl([(-2, 30), (0, 30), (0, 2), (20 + EP + 2, 2), (20 + EP + 2, -30), (20 + EP + 14, -42)], "1-SECCION", 25)   # U de arranque + babeta con gotero
pp = [(20, 6), (20 + EP, 6), (20 + EP, 210), (20, 210)]
v.hatch(pp, "aislacion"); v.pl(pp, "1-SECCION", 35, True)
v.rect(20, 2, 20 + EP, 6, "1-VISTA", 13); v.hatch([(20, 2), (20 + EP, 2), (20 + EP, 6), (20, 6)], "negro")
bulon(v, (20 + EP + 4, 120), (2, 120), 6, cab=3, tuerca=False, lw=13)
v.rect(0, 20, 20, 210, "1-VISTA", 18)
v.ley("viga portapanel 100x60x3,2", (-30, -50), (-4, 22), 1.5)
v.ley("U de arranque + babeta", (110, -30), (-4, -14), 1.5)
v.ley("cinta butílica", (50, 4), (14, 14), 1.5)
v.ley("contrapiso", (100, -110), (4, -6), 1.5)
v.label("CORTE - ARRANQUE 1:5", 0, -155, 1.5, TA.MIDDLE_CENTER, True)
ficha_spec(sh, L, Y1 - 86, R - L, [
    ("Tipo:", "seca, atornillada; junta machihembrada entre paneles y junta sellada sobre columnas."),
    ("Movimiento:", "la chapa exterior dilata ~1 mm/m con 50 °C: la junta vertical (10 mm) y el sellador elástico absorben el movimiento."),
    ("Fijación:", "2 autoperforantes Ø6,3 por panel y apoyo, sin aplastar el núcleo."),
    ("Agua:", "babeta con gotero en el arranque y paneles con el macho hacia arriba."),
], h=2.0, lead=1.36)

# =============================================================== U9 MURO CORTINA - LOSA
Y2 = Y1 - 114
sh.titulo_dib(XA, Y2, "U9", "MURO CORTINA - LOSA (ANCLAJE)", "1:5", w=W2)
v = sh.view_in((XA, Y2 - 102, XA + W2, Y2 - 14), (-160, -175, 270, 250), 5)
# losa de entrepiso (0 a 140) con cenefa y viga de borde debajo
v.hatch([(-160, 0), (-60, 0), (-60, LOSA), (-160, LOSA)], "hormigon"); v.pl([(-160, LOSA), (-60, LOSA), (-60, 0), (-160, 0)], "1-SECCION", 35)
v.pl([(-60, LOSA), (-63, LOSA), (-63, -3), (-150, -3)], "1-SECCION", 25)
v.rect(-150, -160, -60, -3, "1-VISTA", 18); v.hatch([(-150, -14), (-60, -14), (-60, -3), (-150, -3)], "acero")
v.rect(-83, 55, -63, 95, "1-SECCION", 25); v.hatch([(-83, 55), (-63, 55), (-63, 95), (-83, 95)], "gris")     # riel embutido
# grapa: placa contra el canto + brazo horizontal + aleta que toma el montante
gr = [(-63, 30), (-53, 30), (-53, 110), (140, 110), (140, 120), (-63, 120)]
v.pl(gr, "1-SECCION", 35, True); v.hatch(gr, "acero")
bulon(v, (-48, 75), (-80, 75), 12, cab=6, tuerca=False, lw=13)
v.rect(60, 120, 140, 205, "1-VISTA", 25); v.hatch([(60, 120), (140, 120), (140, 205), (60, 205)], "gris")
v.circ((100, 165), 7, "1-VISTA", 25); v.circ((100, 165), 13, "1-VISTA", 13)
# montante 50 x 150 (se ve de costado: 150 de profundidad), empalme y vidrio
v.rect(60, -160, 210, 250, "1-SECCION", 35)
v.ln((60, 222), (210, 222), "1-SECCION", 35); v.rect(66, 180, 204, 250, "1-OCULTO", 9)
v.rect(210, -160, 230, 250, "1-VISTA", 13)
v.rect(232, -160, 257, 250, "1-SECCION", 25); v.hatch([(232, -160), (257, -160), (257, 250), (232, 250)], "vidrio")
# barrera cortafuego entre canto de losa y montante
v.hatch([(-53, 40), (60, 40), (60, 108), (-53, 108)], "lana"); v.rect(-53, 40, 60, 108, "1-VISTA", 13)
v.dim((60, -160), (210, -160), -4)
v.ley("grapa regulable", (-20, 120), (-4, 9))
v.ley("riel + bulón T", (-73, 55), (-2, -14))
v.ley("bulón M12 inox", (100, 165), (-10, 20))
v.ley("montante 50x150", (135, 20), (4, -10))
v.ley("empalme c/ junta 20", (210, 222), (-6, 4))
v.ley("cortafuego", (0, 70), (-6, -26))
v.ley("vidrio", (245, -120), (-4, -8))
v.label("CORTE VERTICAL 1:5", -60, -150, 2.0, TA.MIDDLE_CENTER, True)
ficha_spec(sh, XA, Y2 - 106, W2, [
    ("Tipo:", "seca y regulable en 3 direcciones (riel, agujeros ovalados y suplementos)."),
    ("Movimiento:", "el montante cuelga de cada losa; la junta horizontal de 20 mm con manguito absorbe la flecha de la viga y la dilatación."),
    ("Fuego / aire:", "la barrera de lana mineral sellada cierra el hueco losa-muro entre pisos."),
], h=2.0, lead=1.36)

# =============================================================== U10 CUBIERTA - PARAPETO
sh.titulo_dib(XB, Y2, "U10", "CUBIERTA - PARAPETO (FACHADA D)", "1:10", w=W2)
v = sh.view_in((XB, Y2 - 92, XB + W2, Y2 - 9), (-520, -230, 300, 640), 10)
v.hatch([(-500, -LOSA), (-60, -LOSA), (-60, 0), (-500, 0)], "hormigon"); v.rect(-500, -LOSA, -60, 0, "1-SECCION", 35)
v.rect(-145, -LOSA - 200, -55, -LOSA, "1-VISTA", 18)
v.pl([(-500, 0), (-500, 72), (-60, 40), (-60, 0)], "1-VISTA", 18); v.hatch([(-500, 0), (-500, 72), (-60, 40), (-60, 0)], "mortero")
v.pl([(-500, 78), (-60, 46), (-40, 46), (-40, 250)], "1-SECCION", 35)
v.rect(-40, 0, -20, 600, "1-VISTA", 18)                                         # montante de parapeto
v.rect(0, -110, EP, 600, "1-SECCION", 35); v.hatch([(0, -110), (EP, -110), (EP, 600), (0, 600)], "aislacion")
v.pl([(-30, 250), (-30, 300), (-55, 300)], "1-SECCION", 18)
v.pl([(-60, 620), (-60, 600), (-50, 610), (EP + 40, 610), (EP + 40, 560)], "1-SECCION", 35)
v.pl([(-60, 580), (-60, 620)], "1-SECCION", 35)
v.ln((-20, 610), (EP + 40, 610), "1-SECCION", 35)
v.dim((-600, 0), (-600, 80), -4) if False else None
v.ley("cupertina chapa galv. N°22", (-30, 612), (-8, -4), 1.5)
v.ley("babeta: membrana rebatida 25 cm", (-40, 200), (-10, 14), 1.5)
v.ley("membrana asfáltica 4 mm", (-300, 68), (2, 20), 1.5)
v.ley("contrapiso alivianado 1-2 %", (-400, 40), (2, 9), 1.5)
v.ley("panel 80 (parapeto)", (EP, 300), (-28, -10), 1.5)
v.ley("losa cubierta + viga de borde", (-300, -100), (2, -9), 1.5)
v.ley("montante de parapeto", (-30, 450), (-4, 6), 1.5)
v.label("CORTE 1:10", 150, -150, 1.5, TA.MIDDLE_CENTER, True)
ficha_spec(sh, XB, Y2 - 106, W2, [
    ("Tipo:", "junta de estanqueidad (no estructural): membrana, babeta y cupertina superpuestas."),
    ("Movimiento:", "la babeta queda suelta del panel y la cupertina solapa: absorben dilatación sin fisurar."),
    ("Agua:", "pendiente 1-2 % hacia embudos; la cupertina vuelca hacia la cubierta y gotea afuera."),
], h=2.0, lead=1.36)
sh.save(f"L{lam('u810')}_Uniones_U8_U10")
