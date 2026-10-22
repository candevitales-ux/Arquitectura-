# -*- coding: utf-8 -*-
"""Lámina 06 - Elementos 4: arriostramientos, bulones, soldadura, fijaciones de chapa y protección."""
from lib import *
from geom import *

sh = Sheet(6, "Arriostramientos, bulones, soldadura, fijaciones y protección", "PUNTO 1 - ELEMENTOS CONSTRUCTIVOS",
           "1:125 - 1:10 - 1:5 - 1:2 - 1:2,5")
y0 = sh.encabezado("1° ELEMENTOS: ARRIOSTRAMIENTOS Y ELEMENTOS DE UNIÓN", "Croquis a escala con medidas, función y especificación técnica")
L, R = sh.L + 3, sh.R - 3
W2 = (R - L - 6) / 2
XA, XB = L, L + W2 + 6
Y1 = y0 - 3.5

# =============================================================== 15. ARRIOSTRAMIENTO
sh.titulo_dib(L, Y1, 15, "ARRIOSTRAMIENTO: CRUZ DE SAN ANDRÉS CON TENSOR", "1:125 / 1:10 / 1:5", w=R - L)
v = sh.view_in((L, Y1 - 88, L + 46, Y1 - 8), (-1100, -1150, 4400, 7600), 125)
for yy in (0, VANO):
    v.rect(yy - 150, -300, yy + 150, N2, "1-VISTA", 25)
for z in (N1, N2):
    v.rect(150, z - LOSA - 200 * 0, VANO - 150, z - LOSA + 0 + 0, "1-VISTA", 13)
    v.rect(150, z - 500 - LOSA, VANO - 150, z - LOSA, "1-VISTA", 25)
for zl, zh in ((0, N1 - LOSA - 500), (N1, N2 - LOSA - 500)):
    v.ln((150, zl + 200), (VANO - 150, zh), "1-SECCION", 25); v.ln((VANO - 150, zl + 200), (150, zh), "1-SECCION", 25)
    xm = VANO / 2; zm = (zl + 200 + zh) / 2
    v.rect(xm - 300, zm - 300 * (zh - zl - 200) / (VANO - 300), xm + 300, zm + 300 * (zh - zl - 200) / (VANO - 300), "1-VISTA", 9) if False else None
v.ln((-600, 0), (VANO + 600, 0), "1-VISTA", 25)
v.dim((0, -300), (VANO, -300), -4)
v.nivel(-500, N1, "+3,80", -1); v.nivel(-500, N2, "+7,40", -1); v.nivel(-500, 0, "±0,00", -1)
v.label("ELEVACIÓN EJE 6 (B-C) 1:125", 1700, -1100, 1.5, TA.MIDDLE_CENTER, True)
v.ley("barra Ø20", (VANO * 0.3, 200 + (N1 - LOSA - 700) * 0.3 / 1), (8, 2), 1.5)
# cartela 1:10 (nudo inferior: columna + placa base)
v = sh.view_in((L + 47, Y1 - 60, L + 106, Y1 - 8), (-160, -160, 400, 330), 10)
v.rect(-150, -100, 150, 330, "1-VISTA", 25)                        # columna (alma vista)
v.ln((-150 + 16, -100), (-150 + 16, 330), "1-VISTA", 13); v.ln((150 - 16, -100), (150 - 16, 330), "1-VISTA", 13)
v.rect(-225, -122, 225, -100, "1-VISTA", 25)
g = [(150, 0), (330, 0), (330, 60), (150, 240)]
v.pl(g, "1-SECCION", 35, True); v.hatch(g, "gris")
filete(v, (150, 0), 8, 1, 1)
ang = math.atan2(N1 - LOSA - 700, VANO - 300)
cx, cy = 270, 90
ux, uy = math.cos(ang), math.sin(ang)
v.circ((cx, cy), 13, "1-VISTA", 25)
v.pl([(cx - uy * 30, cy + ux * 30), (cx + ux * 120 - uy * 30, cy + uy * 120 + ux * 30)], "1-VISTA", 18)
v.pl([(cx + uy * 30, cy - ux * 30), (cx + ux * 120 + uy * 30, cy + uy * 120 - ux * 30)], "1-VISTA", 18)
v.pl([(cx + ux * 120 - uy * 10, cy + uy * 120 + ux * 10), (cx + ux * 230 - uy * 10, cy + uy * 230 + ux * 10)], "1-SECCION", 25)
v.pl([(cx + ux * 120 + uy * 10, cy + uy * 120 - ux * 10), (cx + ux * 230 + uy * 10, cy + uy * 230 - ux * 10)], "1-SECCION", 25)
v.label("CARTELA 1:10", 80, -145, 1.5, TA.MIDDLE_CENTER, True)
v.ley("cartela e = 10 soldada", (300, 20), (2, -6), 1.5)
v.ley("horquilla + pasador Ø20", (cx, cy), (-16, 12), 1.5)
# tensor 1:5
v = sh.view_in((L + 108, Y1 - 60, R, Y1 - 8), (-180, -90, 180, 90), 5)
v.rect(-75, -25, 75, 25, "1-VISTA", 35); v.rect(-55, -15, 55, 15, "1-VISTA", 18)
v.hatch([(-75, -25), (75, -25), (75, 25), (-75, 25)], "gris", holes=[[(-55, -15), (55, -15), (55, 15), (-55, 15)]])
for sgn in (-1, 1):
    v.rect(sgn * 20 if sgn > 0 else -175, -10, 175 if sgn > 0 else -20, 10, "1-VISTA", 25)
    v.rect(sgn * 55 - (16 if sgn > 0 else 0) + (0 if sgn > 0 else 0), -17, sgn * 55 + (0 if sgn > 0 else 16), 17, "1-VISTA", 18)
for xx in range(-171, -25, 8): v.ln((xx, -10), (xx + 4, 10), "1-VISTA", 9)
for xx in range(25, 171, 8): v.ln((xx, -10), (xx + 4, 10), "1-VISTA", 9)
v.dim((-75, -25), (75, -25), -5); v.dim((75, -25), (75, 25), 5)
v.label("TENSOR (TORNIQUETE) M20 1:5", 0, -85, 1.5, TA.MIDDLE_CENTER, True)
v.ley("rosca derecha", (-150, 10), (-2, 9), 1.5); v.ley("rosca izquierda", (150, 10), (-2, 9), 1.5)
v.ley("contratuercas", (-55, -17), (-6, -10), 1.5)
ficha_spec(sh, L + 52, Y1 - 62, R - L - 52, [
    ("Función:", "dar estabilidad lateral al edificio (viento y sismo): las barras trabajan solo a tracción y llevan la fuerza horizontal a las fundaciones."),
    ("Ubicación:", "laterales (ejes 1 y 6, vano B-C) y contrafrente (eje D, vanos 1-2 y 5-6), en los dos niveles; el frente vidriado queda libre."),
    ("Medidas:", "barra redonda Ø20 F-24 roscada M20 en los extremos; tensor M20 de 150 mm; cartela 10 mm; horquilla con pasador Ø20."),
    ("Colocación:", "se monta después de aplomar el pórtico y se tensa con el torniquete hasta eliminar la flecha (sin forzar la estructura)."),
], h=1.65, lead=1.38)

# =============================================================== 16. BULONES
Y2 = Y1 - 92
sh.titulo_dib(XA, Y2, 16, "BULÓN ISO 8.8 M20", "1:2", w=W2)
v = sh.view_in((XA, Y2 - 40, XA + W2, Y2 - 6), (-40, -40, 120, 28), 2)
v.rect(0, -30, 18, 30, "1-SECCION", 25); v.hatch([(0, -30), (18, -30), (18, 30), (0, 30)], "acero")
v.rect(18, -30, 38, 30, "1-SECCION", 25); v.hatch([(18, -30), (38, -30), (38, 30), (18, 30)], "acero")
bulon(v, (-4, 0), (42, 0), 20)
v.rect(-4, -18, 0, 18, "1-VISTA", 18); v.rect(38, -18, 42, 18, "1-VISTA", 18)
v.dim((-17, -30), (66, -30), -4, txt="L = 75")
v.ley("cabeza hexagonal", (-10, 16), (-4, 5), 1.5)
v.ley("arandela endurecida", (-2, -18), (-4, -5), 1.5)
v.ley("tuerca clase 8", (52, 16), (4, 5), 1.5)
filas = [["Clase", "8.8: fu 800 MPa / fy 640 MPa (equivale a ASTM A325)"],
         ["Diámetros", "M20 (vigas-columnas), M16 (secundarias)"],
         ["Agujero", "d + 2 mm: Ø22 para M20, Ø18 para M16"],
         ["Distancias", "al borde ≥ 1,5 d; entre bulones ≥ 3 d (60 mm)"],
         ["Apriete", "ajustado con llave de impacto; control con llave de torque (M20 ≈ 400 N·m)"],
         ["Acabado", "galvanizado o zincado; rosca fuera del plano de corte"]]
sh.tabla(XA, Y2 - 42, [("Ítem", 16), ("Especificación", W2 - 16)], filas, h=1.6, lead=1.3, pad=0.55)

# =============================================================== 17. SOLDADURA
sh.titulo_dib(XB, Y2, 17, "SOLDADURA: FILETE Y A TOPE", "1:2,5", w=W2)
v = sh.view_in((XB, Y2 - 40, XB + 42, Y2 - 6), (-15, -32, 55, 50), 2.5)
v.rect(0, 0, 40, 10, "1-SECCION", 25); v.hatch([(0, 0), (40, 0), (40, 10), (0, 10)], "acero")
v.rect(15, 10, 25, 45, "1-SECCION", 25); v.hatch([(15, 10), (25, 10), (25, 45), (15, 45)], "acero")
filete(v, (25, 10), 8, 1, 1); filete(v, (15, 10), 8, -1, 1)
v.dim((25, 10), (33, 10), -4, txt="8")
v.label("filete a = 0,7 x cateto", 20, -28, 1.4, TA.MIDDLE_CENTER)
v = sh.view_in((XB + 44, Y2 - 40, XB + W2, Y2 - 6), (-50, -32, 50, 55), 2.5)
v.pl([(-45, 0), (-2, 0), (-2, 12), (-8, 20), (-45, 20)], "1-SECCION", 25, True); v.hatch([(-45, 0), (-2, 0), (-2, 12), (-8, 20), (-45, 20)], "acero")
v.pl([(45, 0), (2, 0), (2, 12), (8, 20), (45, 20)], "1-SECCION", 25, True); v.hatch([(45, 0), (2, 0), (2, 12), (8, 20), (45, 20)], "acero")
v.hatch([(-2, 0), (2, 0), (2, 12), (8, 20), (-8, 20), (-2, 12)], "negro")
# símbolo de soldadura
v.ln((0, 30), (-20, 50), "3-COTAS", 13); v.ln((-20, 50), (-48, 50), "3-COTAS", 13)
v.pl([(-34, 50), (-30, 54), (-26, 50)], "3-COTAS", 13)
v.label("a tope en V (bisel 60°)", 0, -28, 1.4, TA.MIDDLE_CENTER)
filas = [["Proceso", "taller: semiautomática MIG (ER70S-6); obra: electrodo E7018"],
         ["Uso", "placa base, placas de corte, cartelas, studs; en obra solo studs y fijación de chapa"],
         ["Cordón", "filete mín. 5 mm, adoptado 8 mm; a tope con penetración completa"],
         ["Control", "soldador calificado; inspección visual 100 % y tintas penetrantes"],
         ["Símbolo", "flecha + línea de referencia; triángulo = filete; V = a tope"]]
sh.tabla(XB, Y2 - 42, [("Ítem", 16), ("Especificación", W2 - 16)], filas, h=1.6, lead=1.3, pad=0.55)

# =============================================================== 18. FIJACIONES DE CHAPA
Y3 = Y2 - 82
sh.titulo_dib(XA, Y3, 18, "FIJACIONES DE LA CHAPA", "1:2", w=W2)
v = sh.view_in((XA, Y3 - 36, XA + 30, Y3 - 6), (-15, -20, 15, 40), 2)
v.rect(-15, -12, 15, 0, "1-SECCION", 25); v.hatch([(-15, -12), (15, -12), (15, 0), (-15, 0)], "acero")
v.rect(-15, 0, 15, 1, "1-SECCION", 18)
v.pl([(-2, -10), (0, -12), (2, -10), (2, 14), (-2, 14)], "1-VISTA", 18, True)
v.rect(-6, 14, 6, 16, "1-VISTA", 18); v.rect(-7, 1, 7, 3, "1-VISTA", 18); v.rect(-5, 16, 5, 30, "1-OCULTO", 9)
v.label("clavo pólvora", 0, -18, 1.4, TA.MIDDLE_CENTER)
v = sh.view_in((XA + 30, Y3 - 36, XA + 60, Y3 - 6), (-15, -20, 15, 40), 2)
v.rect(-15, -2, 15, 0, "1-SECCION", 18); v.rect(-15, 0, 15, 1, "1-SECCION", 18)
v.pl([(-2.4, -10), (0, -14), (2.4, -10), (2.4, 4), (-2.4, 4)], "1-VISTA", 18, True)
for zz in range(-9, 3, 2): v.ln((-2.4, zz), (2.4, zz + 1), "1-VISTA", 9)
v.rect(-6, 4, 6, 8, "1-VISTA", 18); v.rect(-8, 1, 8, 4, "1-VISTA", 18); v.hatch([(-8, 1), (8, 1), (8, 4), (-8, 4)], "negro")
v.label("autoperforante", 0, -18, 1.4, TA.MIDDLE_CENTER)
ficha_spec(sh, XA + 61, Y3 - 6, W2 - 61, [
    ("Clavo:", "tipo X-ENP 19 con arandelas, colocado con pistola de pólvora; ala ≥ 6 mm."),
    ("Autoperf.:", "#10 x 19 (Ø4,8) con arandela EPDM; costura de solapes."),
    ("Tapón:", "alternativa: soldadura Ø16 en el valle."),
], h=1.5, lead=1.36)
ficha_spec(sh, XA, Y3 - 39, W2, [
    ("Función:", "fijar la chapa a las vigas durante el montaje (evita que se vuele o se corra) y coser los solapes para que trabaje como un diafragma."),
    ("Cantidad:", "en cada valle de los extremos de la chapa y c/ 450 mm en apoyos intermedios; costura lateral c/ 600 mm."),
], h=1.6, lead=1.38)

# =============================================================== 19. PROTECCIÓN
sh.titulo_dib(XB, Y3, 19, "PROTECCIÓN DEL ACERO", "s/ esc.", w=W2)
cap = [("acero F-24 arenado grado Sa 2½", 255), ("1. antióxido epoxi / fosfato de zinc 50 µm (taller)", 225),
       ("2. retoque en obra de uniones y raspones", 205), ("3. esmalte sintético 2 manos 60 µm", 185),
       ("o pintura intumescente (F60) 1 a 2 mm", 165)]
xx, yy = XB + 2, Y3 - 9
for i, (s, g) in enumerate(cap):
    x0 = xx + i * 5
    sh.solid([(x0, yy - 28), (x0 + 5, yy - 28), (x0 + 5, yy), (x0, yy)], g)
    sh.pl([(x0, yy - 28), (x0 + 5, yy - 28), (x0 + 5, yy), (x0, yy)], "1-VISTA", 13, True)
    sh.leyenda(s, (x0 + 2.5, yy - 3 - i * 5.5), (26 - i * 5, 0), 1.5)
ficha_spec(sh, XB, Y3 - 39, W2, [
    ("Función:", "evitar la corrosión del acero y retrasar la pérdida de resistencia en un incendio (el acero pierde la mitad a ~550 °C)."),
    ("Especificación:", "la chapa colaborante y los bulones llevan galvanizado de fábrica; las caras de contacto de uniones y las alas con studs no se pintan."),
], h=1.6, lead=1.38)
sh.save("L06_Arriostramientos_uniones")
