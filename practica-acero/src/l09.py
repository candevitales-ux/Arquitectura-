# -*- coding: utf-8 -*-
"""Lámina 09 - Uniones U4 (losa-viga), U5 (chapa-chapa y chapa-viga), U6 (borde de losa), U7 (arriostramiento)."""
from lib import *
from geom import *

sh = Sheet(NUM["u47"], "Uniones U4 a U7: losa-viga, chapas, borde de losa, arriostramiento", "PUNTO 2 - JUNTAS Y UNIONES",
           "1:5 - 1:10", hmin=2.6)
y0 = sh.encabezado("2° UNIONES U4, U5, U6 Y U7", f"Detalles a escala de las uniones del entrepiso y del arriostramiento (ver lámina {lam('uesq')})")
L, R = sh.L + 3, sh.R - 3
W2 = (R - L - 6) / 2
XA, XB = L, L + W2 + 6
Y1 = y0 - 3.5
h5, b5, tw5, tf5 = IPN[VP]
h2, b2, tw2, tf2 = IPN[VS]

# =============================================================== U4 LOSA - VIGA SECUNDARIA
sh.titulo_dib(XA, Y1, "U4", "LOSA - VIGA (CONEXIÓN DE CORTE)", "1:5", w=W2)
v = sh.view_in((XA, Y1 - 78, XA + W2, Y1 - 8), (-220, -150, 220, 190), 5)
v.rect(-220, -tf2, 220, 0, "1-SECCION", 35); v.hatch([(-220, -tf2), (220, -tf2), (220, 0), (-220, 0)], "acero")
v.rect(-220, -150, 220, -tf2, "1-VISTA", 13)
v.ln((-220, -150), (220, -150), "1-VISTA", 13)
ch = losa_transversal(v, -215, 215, LOSA, -PASO / 2 + 0)
for xx in (-PASO / 2, PASO / 2):
    stud(v, xx, 0)
v.dim((-215, 0), (-215, LOSA), -5); v.dim((-215, 0), (-215, H_DECK), -11)
v.dim((PASO / 2 - 16, 125), (PASO / 2 + 16, 125), 3) if False else None
v.ley("stud Ø19 x 125 (1 por valle)", (-PASO / 2 + 10, 100), (6, 17), 1.5)
v.ley("soldado a través de la chapa", (PASO / 2 + 10, 4), (8, -8), 1.5)
v.ley("malla Q188 a 25 mm", (100, LOSA - 30), (6, 9), 1.5)
v.ley("ala sup. IPN 200", (150, -6), (2, -10), 1.5)
v.label("CORTE POR LA VIGA SECUNDARIA 1:5", 0, -145, 1.5, TA.MIDDLE_CENTER, True)
ficha_spec(sh, XA, Y1 - 80, W2, [
    ("Tipo:", "soldada (stud) + húmeda (hormigón). Es la única unión que se hace en altura con soldadura."),
    ("Función:", "toma el rasante entre losa y viga: ambas trabajan juntas (viga T compuesta), lo que reduce el perfil necesario."),
    ("Control:", "1 stud cada 100 se dobla a 15° con martillo; no debe fisurarse el cordón."),
], h=2.0, lead=1.36)

# =============================================================== U5 CHAPA - VIGA PRINCIPAL Y COSTURA
sh.titulo_dib(XB, Y1, "U5", "CHAPA - VIGA Y CHAPA - CHAPA", "1:5", w=W2)
v = sh.view_in((XB, Y1 - 78, XB + W2, Y1 - 8), (-215, -170, 215, 190), 5)
seccion_ipn(v, VP, 0, -h5 / 2) if False else None
pts = perfil_poly(VP); pts = [(x, y - h5 / 2) for x, y in pts]
top = [p for p in pts if p[1] > -160]
v.pl([(-b5 / 2, -150), (-b5 / 2, -tf5 + 4), (-tw5 / 2, -tf5 - 3), (-tw5 / 2, -150)], "1-SECCION", 35)
v.pl([(b5 / 2, -150), (b5 / 2, -tf5 + 4), (tw5 / 2, -tf5 - 3), (tw5 / 2, -150)], "1-SECCION", 35)
v.pl([(-b5 / 2, -tf5 + 4), (-b5 / 2, 0), (b5 / 2, 0), (b5 / 2, -tf5 + 4)], "1-SECCION", 35)
v.hatch([(-b5 / 2, -tf5 + 4), (-b5 / 2, 0), (b5 / 2, 0), (b5 / 2, -tf5 + 4), (tw5 / 2, -tf5 - 3), (tw5 / 2, -150), (-tw5 / 2, -150), (-tw5 / 2, -tf5 - 3)], "acero")
ch = losa_transversal(v, -210, 210, LOSA, 0)
stud(v, 0, 0)
for xx in (-55, 55):
    v.pl([(xx - 2, -12), (xx, -16), (xx + 2, -12), (xx + 2, 14), (xx - 2, 14)], "1-VISTA", 18, True)
    v.rect(xx - 6, 14, xx + 6, 17, "1-VISTA", 18)
# solape lateral con autoperforante (a la derecha)
v.ley("clavo de pólvora (2 por valle)", (55, 10), (-16, -22), 1.5)
v.ley("stud Ø19", (0, 100), (-6, 14), 1.5)
v.ley("valle apoyado (mín. 40 mm)", (-60, 0), (-4, -24), 1.5)
v.ley("viga IPN 500", (-60, -120), (-4, -6), 1.5)
v.label("CORTE POR LA VIGA PRINCIPAL 1:5", 0, -165, 1.5, TA.MIDDLE_CENTER, True)
ficha_spec(sh, XB, Y1 - 80, W2, [
    ("Tipo:", "seca, mecánica (clavos de pólvora / autoperforantes). Provisoria hasta el hormigonado y luego diafragma."),
    ("Chapa - viga:", "clavo en cada valle en los extremos de chapa; c/ 450 mm en apoyos intermedios."),
    ("Chapa - chapa:", "solape lateral de 1 media onda (macho-hembra) cosido con autoperforante #10 c/ 600 mm; solape de extremo a tope sobre la viga."),
], h=2.0, lead=1.36)

# =============================================================== U6 BORDE DE LOSA
Y2 = Y1 - 112
sh.titulo_dib(XA, Y2, "U6", "BORDE DE LOSA - VIGA DE BORDE", "1:5", w=W2)
v = sh.view_in((XA, Y2 - 80, XA + W2, Y2 - 8), (-250, -230, 190, 175), 5)
seccion_ipn(v, VS, 0, -h2 / 2)
losa_longitudinal(v, -25, 185, LOSA)
v.pl([(-60, LOSA), (-63, LOSA), (-63, -18 + 3), (45, -18 + 3), (45, -15 + 3), (-60, -15 + 3)], "1-SECCION", 35, True)
v.hatch([(-25, 0), (-60, 0), (-60, LOSA), (-25, LOSA)], "hormigon")
v.ln((-60, LOSA), (-25, LOSA), "1-SECCION", 35)
v.pl([(-63, LOSA), (-63 + 30, LOSA)], "1-SECCION", 25)
stud(v, 0, 0)
v.pl([(20, LOSA - 40), (-50, LOSA - 40), (-50, 20)], "1-VISTA", 18)
v.dim((-63, -15), (-63, LOSA), -6)
v.dim((-63, LOSA), (0, LOSA), 4)
v.ley("cenefa e = 1,6", (-63, 20), (-2, -22), 1.5)
v.ley("rienda de fleje c/ 600", (-50, 60), (8, 20), 1.5)
v.ley("fijación al ala c/ 300", (20, -12), (10, -10), 1.5)
v.ley("viga de borde IPN 200", (40, -150), (8, -4), 1.5)
v.label("CORTE 1:5 (frente A)", -30, -225, 1.5, TA.MIDDLE_CENTER, True)
ficha_spec(sh, XA, Y2 - 87, W2, [
    ("Tipo:", "seca (cenefa fijada) + húmeda (hormigón que la rellena)."),
    ("Función:", "cerrar el encofrado perdido en el perímetro y dejar el canto recto y a plomo para recibir el cerramiento."),
    ("Junta:", "entre losa y muro cortina queda una junta de 20-30 mm que se cierra con barrera cortafuego (ver U9)."),
], h=2.0, lead=1.36)

# =============================================================== U7 ARRIOSTRAMIENTO - NUDO SUPERIOR
sh.titulo_dib(XB, Y2, "U7", "ARRIOSTRAMIENTO - NUDO SUPERIOR", "1:10", w=W2)
v = sh.view_in((XB, Y2 - 80, XB + W2, Y2 - 8), (-200, -470, 650, 230), 10)
ipn_vertical(v, COL, 0, -460, 220, True, 35)                       # en el lateral se ve el ala de la HEB
v.pl([(100, 220), (650, 220)], "1-VISTA", 13, lt="DASHED2")
v.rect(100, 0, 650, 200, "1-VISTA", 25); v.ln((100, 27), (650, 27), "1-VISTA", 13)
g = [(100, 0), (370, 0), (370, -60), (100, -270)]
v.pl(g, "1-SECCION", 35, True); v.hatch(g, "gris")
ang = math.atan2(-(N1 - LOSA - 700), VANO - 200)
cx, cy = 230, -100
ux, uy = math.cos(ang), math.sin(ang)
v.circ((cx, cy), 13, "1-VISTA", 25)
for sgn in (-1, 1):
    v.pl([(cx + sgn * uy * 30, cy - sgn * ux * 30), (cx + ux * 120 + sgn * uy * 30, cy + uy * 120 - sgn * ux * 30)], "1-VISTA", 18)
v.pl([(cx + ux * 120 - uy * 10, cy + uy * 120 + ux * 10), (cx + ux * 420 - uy * 10, cy + uy * 420 + ux * 10)], "1-SECCION", 25)
v.pl([(cx + ux * 120 + uy * 10, cy + uy * 120 - ux * 10), (cx + ux * 420 + uy * 10, cy + uy * 420 - ux * 10)], "1-SECCION", 25)
v.ley("columna HEB 200 (ala)", (-60, -420), (6, -2))
v.ley("viga IPN 500 del pórtico extremo", (500, 120), (-6, 12))
v.ley("cartela e = 10", (330, -40), (6, 6))
v.ley("horquilla + pasador Ø20", (cx, cy), (-4, -16))
v.ley("barra Ø20 (al tensor)", (cx + ux * 380, cy + uy * 380), (-4, -7))
v.label("ELEVACIÓN 1:10 (lateral)", 250, -455, 2.0, TA.MIDDLE_CENTER, True)
ficha_spec(sh, XB, Y2 - 87, W2, [
    ("Tipo:", "cartela soldada en taller + horquilla con pasador en obra (unión de un solo bulón)."),
    ("Vínculo:", "articulado; la barra solo trabaja a tracción. El eje de la barra pasa por el nudo columna-viga (sin excentricidad)."),
    ("Ajuste:", "con el tensor central, hasta sacar la flecha de la barra."),
], h=2.0, lead=1.36)
sh.save(f"L{lam('u47')}_Uniones_U4_U7")
