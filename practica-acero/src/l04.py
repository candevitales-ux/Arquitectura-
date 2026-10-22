# -*- coding: utf-8 -*-
"""Lámina 04 - Elementos 2: viga principal IPN 500, viga secundaria IPN 200, viga de borde y piezas de unión."""
from lib import *
from geom import *

sh = Sheet(NUM["vigas"], "Vigas principales, secundarias, de borde y piezas de unión", "PUNTO 1 - ELEMENTOS CONSTRUCTIVOS",
           "1:10 - 1:100 - 1:75 - 1:5")
y0 = sh.encabezado("1° ELEMENTOS: VIGAS Y PIEZAS DE UNIÓN", "Croquis a escala con medidas, función y especificación técnica")
L, R = sh.L + 3, sh.R - 3
W2 = (R - L - 6) / 2
XA, XB = L, L + W2 + 6
Y1 = y0 - 3.5

# =============================================================== 5. VIGA PRINCIPAL IPN 500
sh.titulo_dib(L, Y1, 5, "VIGA PRINCIPAL IPN 500 - LUZ 12,00 m", "1:10 / 1:100", w=R - L)
# sección compuesta 1:10
v = sh.view_in((L, Y1 - 86, L + 44, Y1 - 9), (-200, -590, 240, 170), 10)
h, b, twb, tf = IPN[VP]
seccion_ipn(v, VP, 0, -h / 2)
losa_transversal(v, -190, 190, LOSA, 0)
stud(v, 0, 0)
v.dim((-b / 2, -h), (b / 2, -h), -4)
v.dim((b / 2, -h), (b / 2, 0), 6)
v.dim((190, 0), (190, LOSA), 3)
v.label("SECCIÓN 1:10", 0, -h - 75, 1.7, TA.MIDDLE_CENTER, True)
v.ley("stud Ø19", (8, 60), (14, -3), 1.6)
# elevación 1:100
v = sh.view_in((L + 46, Y1 - 46, R, Y1 - 8), (-600, -1300, 12500, 900), 100)
for yy in (0, ANCHO):
    v.rect(yy - 150, -1000, yy + 150, 600, "1-VISTA", 18)
    v.eje((yy, -1200), (yy, 800))
v.rect(150 + 10, -500, ANCHO - 160, 0, "1-SECCION", 35)
v.ln((160, -tf), (ANCHO - 160, -tf), "1-VISTA", 13); v.ln((160, -500 + tf), (ANCHO - 160, -500 + tf), "1-VISTA", 13)
x = 160 + 150
while x < ANCHO - 200:
    v.ln((x, 0), (x, 125), "1-VISTA", 13); x += 300
for k in range(1, 6):
    xx = k * SEC
    v.rect(xx - 60, -230, xx + 60, -30, "1-OCULTO", 9)
v.dim((0, 600), (ANCHO, 600), 3)
for k in range(6): v.dim((k * SEC, -500), (k * SEC + SEC, -500), -4)
v.label("ELEVACIÓN 1:100", 6000, -1300, 1.7, TA.MIDDLE_CENTER, True)
v.ley("studs Ø19 c/ 300 (en el valle de la chapa)", (3210, 125), (4, 9), 1.6)
v.ley("ángulos p/ secundarias", (8000, -130), (8, 7), 1.6)
ficha_spec(sh, L + 48, Y1 - 48, R - L - 48, [
    ("Función:", "salvar la luz de 12,00 m sin apoyos, recibir las reacciones de las vigas secundarias y, con los conectores, trabajar en sección compuesta con la losa."),
    ("Medidas:", "IPN 500: h 500, b 185, tw 18, tf 27 mm; 141 kg/m; Ix = 68.740 cm⁴; Wx = 2.750 cm³; pieza de 11,68 m (entra en un semirremolque de 12 m)."),
    ("Especificación:", "acero F-24; contraflecha 30 mm; agujeros Ø22 en el alma para bulones M20; se iza con 2 eslingas (balancín) y se abulona a las placas de corte de las columnas."),
], h=1.75)

# =============================================================== 6. VIGA SECUNDARIA IPN 200
Y2 = Y1 - 92
sh.titulo_dib(XA, Y2, 6, "VIGA SECUNDARIA IPN 200", "1:10 / 1:75", w=W2)
v = sh.view_in((XA, Y2 - 50, XA + 26, Y2 - 6), (-110, -265, 135, 160), 10)
seccion_ipn(v, VS, 0, -100)
losa_longitudinal(v, -100, 100, LOSA)
stud(v, 0, 0)
h, b, twb, tf = IPN[VS]
v.dim((-b / 2, -200), (b / 2, -200), -4)
v.dim((b / 2, -200), (b / 2, 0), 6)
v.label("SECCIÓN 1:10", 0, -260, 1.6, TA.MIDDLE_CENTER, True)
v = sh.view_in((XA + 27, Y2 - 50, XA + W2, Y2 - 6), (-200, -700, 4200, 500), 75)
v.rect(-150, -500, 9, 300, "1-VISTA", 13); v.rect(VANO - 9, -500, VANO + 150, 300, "1-VISTA", 13)
v.eje((0, -650), (0, 450)); v.eje((VANO, -650), (VANO, 450))
p = [(19, -200), (19, -40), (110, -40), (110, 0), (VANO - 110, 0), (VANO - 110, -40), (VANO - 19, -40), (VANO - 19, -200)]
v.pl(p, "1-SECCION", 35, True)
v.ln((110, -tf), (VANO - 110, -tf), "1-VISTA", 13); v.ln((19, -200 + tf), (VANO - 19, -200 + tf), "1-VISTA", 13)
for xx in (20, VANO - 95):
    v.rect(xx, -170, xx + 75, -50, "1-VISTA", 18)
v.dim((0, 0), (VANO, 0), 6)
v.dim((19, -200), (VANO - 19, -200), -4)
v.label("ELEVACIÓN 1:75", 2000, -700, 1.6, TA.MIDDLE_CENTER, True)
v.ley("destaje 90 x 40", (110, -20), (4, 10), 1.6)
v.ley("doble ángulo", (VANO - 60, -110), (-6, -11), 1.6)
ficha_spec(sh, XA, Y2 - 56, W2, [
    ("Función:", "apoyo de la chapa colaborante cada 2,00 m; lleva las cargas de la losa a las vigas principales."),
    ("Medidas:", "IPN 200: h 200, b 90, tw 7,5, tf 11,3 mm; 26,2 kg/m; Wx = 214 cm³; largo 3,96 m."),
    ("Especificación:", "F-24; destaje del ala superior para quedar enrasada con la viga principal; unión articulada con doble ángulo y 2 bulones M16."),
])

# =============================================================== 7. VIGA DE BORDE IPN 200
sh.titulo_dib(XB, Y2, 7, "VIGA DE BORDE + BORDE DE LOSA", "1:10", w=W2)
v = sh.view_in((XB, Y2 - 52, XB + W2, Y2 - 9), (-500, -270, 380, 170), 10, ha="r")
seccion_ipn(v, VS, 0, -100)
losa_longitudinal(v, -25, 370, LOSA)
stud(v, 0, 0)
# cenefa de borde (L de chapa plegada) fijada al ala superior
cen = [(-60, LOSA), (-60, -15), (45, -15)]
v.pl([(-60, LOSA), (-63, LOSA), (-63, -18), (45, -18), (45, -15), (-60, -15)], "1-SECCION", 35, True)
v.hatch([(-25, 0), (-60, 0), (-60, LOSA), (-25, LOSA)], "hormigon")
v.ln((-60, LOSA), (-25, LOSA), "1-SECCION", 35)
v.ln((-25, 0), (-25, LOSA), "1-OCULTO", 9)
v.dim((-63, -18), (-63, LOSA), -5)
v.dim((-63, LOSA), (0, LOSA), 4)
v.ley("cenefa chapa galv. e = 1,6", (-63, 60), (-8, 8), 1.6)
v.ley("riel de anclaje p/ CW", (-60, -150), (-6, -4), 1.6)
v.rect(-60, -165, -45, -135, "1-VISTA", 18)
v.ley("fijación de cenefa", (20, -16), (8, -10), 1.6)
v.ley("chapa colaborante", (250, 0), (-4, -16), 1.6)
v.label("SECCIÓN 1:10 (frente A)", 0, -265, 1.6, TA.MIDDLE_CENTER, True)
ficha_spec(sh, XB, Y2 - 56, W2, [
    ("Función:", "cerrar el perímetro de la losa, atar las columnas de la fachada y recibir los anclajes del cerramiento."),
    ("Medidas:", "IPN 200 (igual a la secundaria), vano 4,00 m; vuelo de losa 60 mm hasta la cenefa."),
    ("Especificación:", "F-24; en el frente lleva riel de anclaje soldado para las grapas del muro cortina; en laterales recibe la viga portapanel."),
])

# =============================================================== 8. PIEZAS DE UNIÓN
Y3 = Y2 - 78
sh.titulo_dib(L, Y3, 8, "PIEZAS DE UNIÓN: PLACA DE CORTE Y DOBLE ÁNGULO", "1:10 / 1:5", w=R - L)
# placa de corte (vista de frente) para viga principal
v = sh.view_in((L, Y3 - 55, L + 30, Y3 - 6), (-80, -270, 160, 215), 10)
v.rect(-60, -200, 60, 200, "1-SECCION", 35); v.hatch([(-60, -200), (60, -200), (60, 200), (-60, 200)], "gris")
for zz in (-120, -40, 40, 120):
    v.circ((15, zz), 11, "1-VISTA", 18)
v.dim((-60, -200), (60, -200), -4); v.dim((60, -200), (60, 200), 4)
v.dim((60, -120), (60, -40), 11)
v.label("PLACA 1:10", 15, -250, 1.6, TA.MIDDLE_CENTER, True)
# placa en planta soldada al ala de la columna
v = sh.view_in((L + 32, Y3 - 52, L + 80, Y3 - 6), (-170, -200, 250, 70), 10)
pts = xf(perfil_poly(COL), 0, 0, 90); v.pl(pts, "1-SECCION", 35, True); v.hatch(pts, "acero")
v.rect(62, -5, 182, 5, "1-SECCION", 35); v.hatch([(62, -5), (182, -5), (182, 5), (62, 5)], "acero")
filete(v, (62, 5), 8, 1, 1); filete(v, (62, -5), 8, 1, -1)
v.rect(102, 5, 230, 23, "1-VISTA", 18)                               # alma de la viga (fantasma)
bulon(v, (130, 41), (130, -5 - 0), 20)
v.label("PLANTA 1:10 (soldada al ala)", 30, -190, 1.6, TA.MIDDLE_CENTER, True)
v.ley("alma IPN 500", (220, 23), (-2, 8), 1.5)
# doble ángulo
v = sh.view_in((L + 82, Y3 - 52, L + 128, Y3 - 6), (-95, -125, 95, 60), 5)
v.rect(-4, -70, 4, 40, "1-VISTA", 13)
angular(v, -4, -70, 76, 8, 90, True); angular(v, 4, -70, 76, 8, 0, True)
for a in (-1,):
    pass
v.ln((-80, -70), (80, -70), "1-VISTA", 13)
v.dim((-80, -70), (80, -70), -4)
v.label("2 L 76x76x8 - PLANTA 1:5", 0, -115, 1.6, TA.MIDDLE_CENTER, True)
v.ley("alma IPN 200", (0, 30), (6, 4), 1.5)
v = sh.view_in((L + 130, Y3 - 52, R, Y3 - 6), (-40, -125, 120, 90), 5)
v.rect(0, -70, 76, 70, "1-SECCION", 35); v.hatch([(0, -70), (76, -70), (76, 70), (0, 70)], "gris")
for zz in (-35, 35): v.circ((38, zz), 9, "1-VISTA", 18)
v.dim((0, -70), (76, -70), -4); v.dim((76, -70), (76, 70), 4); v.dim((76, -35), (76, 35), 10)
v.label("ÁNGULO 1:5 - 2 M16", 38, -115, 1.6, TA.MIDDLE_CENTER, True)
ficha_spec(sh, L, Y3 - 58, R - L, [
    ("Función:", "vincular vigas con columnas y vigas entre sí transmitiendo el corte (uniones articuladas de montaje en seco)."),
    ("Placa de corte:", "chapa F-24 de 400 x 120 x 10 mm soldada en taller al ala de la columna (filete 8 mm ambos lados); 4 agujeros Ø22, paso 80 mm, para M20."),
    ("Doble ángulo:", "2 L 76 x 76 x 8 (3\" x 5/16\") de 140 mm, abulonados al alma de la viga principal y de la secundaria; 2 bulones M16 por ala, agujeros Ø18."),
])
sh.save(f"L{lam('vigas')}_Vigas_piezas_union")
