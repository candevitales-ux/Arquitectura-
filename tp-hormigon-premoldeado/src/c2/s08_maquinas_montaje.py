# -*- coding: utf-8 -*-
"""Máquinas de montaje: M1 grúa telescópica (una lámina) y M2 carretón + M3 balancín (otra lámina)."""
import math
from lib import Sheet, page, spec, heading, ground, wrap, REB, TB, TS, TD, TT
from s02_fundacion_columna import legend
import geo

STEEL, YEL, DARK, TIRE = "#5a5a5a", "#f2c230", "#3a3a3a", "#222"


def wheel(v, x, r=650):
    v.circle(x, r, r, fill=TIRE, sw=0.1); v.circle(x, r, r * 0.45, fill="#888", sw=0.08)


def grua(v, ang=58, L=26000, hook_z=15500):
    """grúa telescópica de 4 ejes (vista lateral) sobre estabilizadores; x = 0 trasera del chasis"""
    for x in (1700, 3350, 9300, 10950): wheel(v, x)
    v.rect(0, 900, 13500, 1900, fill=YEL, sw=0.2)
    v.poly([(11600, 1900), (13500, 1900), (13500, 3300), (12100, 3300), (11600, 2700)], fill=YEL, sw=0.2)
    v.rect(12200, 2500, 13350, 3150, fill="#bfe3f0", sw=0.1)
    for x in (900, 12300):
        v.rect(x - 150, 120, x + 150, 1300, fill=STEEL, sw=0.12); v.rect(x - 450, 0, x + 450, 120, fill=DARK, sw=0.1)
    v.rect(3200, 1900, 6400, 2400, fill=DARK, sw=0.12)
    v.rect(800, 2400, 3400, 4100, fill="#777", sw=0.15)
    v.rect(3200, 2400, 7600, 3400, fill=YEL, sw=0.15)
    v.poly([(6000, 2400), (7600, 2400), (7600, 4300), (6400, 4300)], fill=YEL, sw=0.15)
    v.rect(6600, 3200, 7450, 4100, fill="#bfe3f0", sw=0.08)
    px, pz = 4200, 3500
    a = math.radians(ang); ux, uz = math.cos(a), math.sin(a); nx, nz = -uz, ux
    w0, w1 = 1500, 650
    v.poly([(px + nx * w0 / 2, pz + nz * w0 / 2), (px + ux * L + nx * w1 / 2, pz + uz * L + nz * w1 / 2),
            (px + ux * L - nx * w1 / 2, pz + uz * L - nz * w1 / 2), (px - nx * w0 / 2, pz - nz * w0 / 2)], fill=YEL, sw=0.2)
    for f in (0.32, 0.55, 0.76):
        w = w0 + (w1 - w0) * f
        v.line(px + ux * L * f + nx * w / 2, pz + uz * L * f + nz * w / 2, px + ux * L * f - nx * w / 2, pz + uz * L * f - nz * w / 2, sw=0.15)
    v.line(5600, 2400, px + ux * 8000, pz + uz * 8000, sw=0.7, stroke=STEEL)
    tx, tz = px + ux * L, pz + uz * L
    v.circle(tx, tz, 300, fill=DARK, sw=0.1)
    v.line(tx, tz - 300, tx, hook_z + 600, sw=0.18)
    v.rect(tx - 300, hook_z, tx + 300, hook_z + 600, fill=DARK, sw=0.1)
    v.pline([(tx, hook_z), (tx, hook_z - 300), (tx + 150, hook_z - 450), (tx + 260, hook_z - 300)], sw=0.35)
    return tx, tz, px, pz


@page("M1 · Grúa telescópica autopropulsada")
def m1(num, total):
    sh = Sheet(num, total, "M1 · Grúa telescópica autopropulsada", escalas="vista lateral 1:250", fname="M1_Grua_Telescopica")
    heading(sh, "3º MÁQUINAS DE MONTAJE · M1 GRÚA TELESCÓPICA 90 t", "Equipo principal de izaje: levanta columnas, vigas y paneles (pieza crítica: VP 14,58 m · 12,6 t)")
    sh.title_drawing(12, 32, "VISTA LATERAL · IZANDO UNA VP AL NIVEL +4,50", "esc. 1:250", TT)
    v = sh.view(26, 156, 250)
    tx, tz, px, pz = grua(v)
    for xc in (21000, 36000):
        v.rect(xc - 200, 0, xc + 200, geo.COL_TOP, fill="#cfd3d7", sw=0.15)
        v.poly([(xc - 200, 3655), (xc - 550, 3655), (xc - 550, 3495), (xc - 200, 3185)], fill="#cfd3d7", sw=0.12)
    zp = 5400
    v.rect(tx - 7290, zp, tx + 7290, zp + 750, fill=geo.C_VP, sw=0.25)
    v.line(tx, 15100, tx - 1200, 11600, sw=0.25); v.line(tx, 15100, tx + 1200, 11600, sw=0.25)
    v.rect(tx - 4600, 11300, tx + 4600, 11600, fill=YEL, sw=0.2)
    for s in (-1, 1): v.line(tx + s * 4375, 11300, tx + s * 4375, zp + 750, sw=0.25)
    for s in (-1, 1): v.line(tx + s * 7290, zp + 300, tx + s * 7290 + s * 1500, zp - 1800, sw=0.12, dash="0.6 0.3")
    ground(sh, v.P(-1500, 0)[0], v.P(39000, 0)[0], v.P(0, 0)[1])
    v.dim((4800, 0), (tx, 0), -6.0, f"radio de trabajo R = {(tx - 4800) / 1000:.1f} m".replace(".", ","))
    v.dim((0, 0), (13500, 0), -12.0, "13,50")
    v.dim((-1200, 0), (-1200, tz), 3.0, f"{tz / 1000:.1f} m".replace(".", ","))
    v.line(4800, 0, 4800, 27500, stroke="#b22", sw=0.12, dash="2 0.6 0.4 0.6")
    sh.text(*v.P(5100, 26500), "eje de giro", TS, color="#b22")
    a = math.radians(58)
    for lab, tgt, at in (("1", (px + 12000 * math.cos(a), pz + 12000 * math.sin(a)), (60, 62)), ("2", (2100, 3300), (16, 128)),
                         ("3", (900, 600), (16, 145)), ("4", (6900, 3800), (56, 120)), ("5", (tx, 15800), (150, 60)),
                         ("6", (tx - 3000, 11450), (150, 82)), ("7", (tx + 4000, zp + 375), (196, 118)), ("8", (tx + 7290 + 1000, zp - 1200), (196, 150))):
        sh.callout(v.P(*tgt), at, lab)
    y = legend(sh, 12, 178, ["1 Pluma telescópica de 4 tramos (26 m de trabajo)", "2 Contrapeso desmontable (viaja en camión aparte)",
                             "3 Estabilizadores extendidos c/ placas de reparto 0,9 x 0,9 m", "4 Cabina de operación (giro 360°)",
                             "5 Pasteca y gancho c/ seguro", "6 Balancín de izaje (M3)", "7 VP 14,58 m · 12,6 t", "8 Sogas guía (vientos) p/ orientar la pieza"], w=92)
    sh.text(108, 178, "TABLA DE CARGA", TT, bold=True)
    sh.text(108, 183, "pluma 26 m · contrapeso total · 360°", TS)
    rows = [("R (m)", "Capacidad (t)")] + [(r, c) for r, c in (("8", "38,0"), ("10", "30,5"), ("12", "24,0"), ("14", "19,5"), ("16", "16,0"), ("18", "13,0"))]
    yy = sh.table(108, 186, [30, 60], rows, size=TB, rowh=5.0, fills=[None] + [None, None, None, "#fde8b0", None, None])
    sh.para(108, yy + 5, 90, "Verificación (R = 14 m): VP 12,6 t + balancín 0,8 t + eslingas 0,2 t = 13,6 t ≤ 0,75 x 19,5 t = 14,6 t ✓",
            TB, 1.3)
    return sh


@page("M2 · Carretón + M3 · Balancín de izaje")
def m2m3(num, total):
    sh = Sheet(num, total, "M2 · Carretón + M3 · Balancín de izaje", escalas="carretón 1:200 · balancín 1:100", fname="M2_M3_Carreton_Balancin")
    heading(sh, "3º MÁQUINAS DE MONTAJE · M2 TRANSPORTE Y M3 IZAJE", "Traslado de las piezas largas desde la planta y dispositivo para colgarlas de la grúa")
    sh.title_drawing(12, 32, "M2 · TRACTOR + SEMIRREMOLQUE CARRETÓN EXTENSIBLE", "Vista lateral 1:200 · transportando la VP (pieza > 12 m)", TT)
    c = sh.view(30, 80, 200)
    for x in (900, 4300, 5650): c.circle(x, 520, 520, fill=TIRE, sw=0.1)
    c.rect(0, 800, 6400, 1300, fill="#c0392b", sw=0.15)
    c.poly([(0, 1300), (2400, 1300), (2400, 3700), (300, 3700), (0, 3000)], fill="#c0392b", sw=0.15)
    c.rect(400, 2500, 2200, 3400, fill="#bfe3f0", sw=0.08)
    c.rect(4300, 1300, 5800, 1500, fill=DARK, sw=0.1)
    c.poly([(4000, 1500), (6200, 1500), (6200, 1150), (21500, 1150), (21500, 1500), (21800, 1500), (21800, 900), (4300, 900)], fill="#7f8c8d", sw=0.15)
    for x in (17800, 19200, 20600): c.circle(x, 520, 520, fill=TIRE, sw=0.1)
    for x in (9000, 14000, 19500): c.rect(x - 150, 1500, x + 150, 1650, fill="#8b5a2b", sw=0.06)
    c.rect(6700, 1650, 6700 + 14580, 1650 + 750, fill=geo.C_VP, sw=0.25)
    for x in (9000, 14000, 19500): c.line(x, 2400, x + 600, 1150, sw=0.15)
    ground(sh, c.P(-500, 0)[0], c.P(23000, 0)[0], c.P(0, 0)[1])
    c.dim((0, 0), (21800, 0), -5.0, "≈ 21,80 (requiere permiso de tránsito)")
    c.dim((22300, 0), (22300, 2400), -3.5, "2,40")
    sh.note(c.P(14000, 2000), (90, 50), "VP s/ tacos de madera, fajas de amarre y cantoneras")
    sh.title_drawing(12, 100, "M3 · BALANCÍN (VIGA DE IZAJE) + ESLINGAS", "Esquema 1:100 · izaje de un panel TT por sus 4 insertos", TT)
    b = sh.view(14, 172, 100)
    b.rect(0, 0, 9580, 650, fill=geo.C_TT, sw=0.25); b.line(0, 600, 9580, 600, sw=0.1)
    xc = 4790
    b.rect(xc - 3100, 2000, xc + 3100, 2300, fill=YEL, sw=0.25)
    for s in (-1, 1):
        b.line(xc, 4100, xc + s * 1200, 2300, sw=0.3)
        b.line(xc + s * 2874, 2000, xc + s * 2874, 650, sw=0.3)
        b.circle(xc + s * 2874, 600, 80, fill="#000", sw=0.05)
    b.rect(xc - 200, 4100, xc + 200, 4500, fill=DARK, sw=0.1)
    b.dim((xc - 2874, 0), (xc + 2874, 0), -4.0, "insertos a L/5 de los extremos")
    sh.note(b.P(xc + 600, 3200), (52, 122), "eslingas ≥ 45° c/ la horizontal")
    sh.note(b.P(xc + 2500, 2150), (52, 132), "viga balancín (perfil o tubo)")
    sh.text(126, 110, "Accesorios de izaje", TT, bold=True)
    sh.bullets(126, 116, 72, ["Grillete tipo lira c/ perno roscado", "Eslinga de cable de acero o faja de poliéster (c/ etiqueta de carga)",
                              "Argolla giratoria roscada al inserto", "Gancho c/ lengüeta de seguridad", "Sogas guía (vientos)",
                              "Cuñas, calces y cantoneras"], TS, 1.25, 0.8)
    spec(sh, 12, 186, 186, "FUNCIÓN Y USO", [
        ("M2 Carretón:", "semirremolque extensible 12-25 m, capacidad 30 t; las piezas > 12 m o > 2,60 m de ancho viajan con permiso y escolta, en el orden de montaje."),
        ("M3 Balancín:", "reparte la carga en 2 o 4 puntos con tiros verticales: evita compresión axial y flexiones no previstas en la pieza; la carga del balancín (0,8 t) se suma a la de la pieza."),
        ("Seguridad:", "eslingas y grilletes certificados con su carga máxima de uso; zona de exclusión bajo la carga; se suspende el izaje con viento > 50 km/h."),
    ])
    return sh


PAGES = [m1, m2m3]
