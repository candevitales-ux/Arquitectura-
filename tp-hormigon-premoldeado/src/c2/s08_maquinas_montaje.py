# -*- coding: utf-8 -*-
"""Lámina 08 – Máquinas de montaje: grúa telescópica autopropulsada, carretón de transporte y balancín de izaje."""
import math
from lib import Sheet, spec, heading, ground, REB
import geo

STEEL, YEL, DARK, TIRE = "#5a5a5a", "#f2c230", "#3a3a3a", "#222"


def wheel(v, x, r=650):
    v.circle(x, r, r, fill=TIRE, sw=0.1); v.circle(x, r, r * 0.45, fill="#888", sw=0.08)


def grua(v, ang=58, L=26000, hook_z=15500):
    """grúa telescópica de 4 ejes (vista lateral) apoyada sobre estabilizadores; x = 0 trasera del chasis"""
    for x in (1700, 3350, 9300, 10950): wheel(v, x)
    v.rect(0, 900, 13500, 1900, fill=YEL, sw=0.2)                                 # chasis
    v.poly([(11600, 1900), (13500, 1900), (13500, 3300), (12100, 3300), (11600, 2700)], fill=YEL, sw=0.2)   # cabina conductor
    v.rect(12200, 2500, 13350, 3150, fill="#bfe3f0", sw=0.1)
    for x in (900, 12300):                                                          # estabilizadores
        v.rect(x - 150, 120, x + 150, 1300, fill=STEEL, sw=0.12)
        v.rect(x - 450, 0, x + 450, 120, fill=DARK, sw=0.1)
    v.rect(3200, 1900, 6400, 2400, fill=DARK, sw=0.12)                              # tornamesa
    v.rect(800, 2400, 3400, 4100, fill="#777", sw=0.15)                             # contrapeso
    v.rect(3200, 2400, 7600, 3400, fill=YEL, sw=0.15)                               # superestructura
    v.poly([(6000, 2400), (7600, 2400), (7600, 4300), (6400, 4300)], fill=YEL, sw=0.15)   # cabina grúa
    v.rect(6600, 3200, 7450, 4100, fill="#bfe3f0", sw=0.08)
    px, pz = 4200, 3500
    a = math.radians(ang)
    ux, uz = math.cos(a), math.sin(a); nx, nz = -uz, ux
    w0, w1 = 1500, 650
    v.poly([(px + nx * w0 / 2, pz + nz * w0 / 2), (px + ux * L + nx * w1 / 2, pz + uz * L + nz * w1 / 2),
            (px + ux * L - nx * w1 / 2, pz + uz * L - nz * w1 / 2), (px - nx * w0 / 2, pz - nz * w0 / 2)], fill=YEL, sw=0.2)
    for f in (0.32, 0.55, 0.76):                                                   # tramos telescópicos
        w = w0 + (w1 - w0) * f
        v.line(px + ux * L * f + nx * w / 2, pz + uz * L * f + nz * w / 2, px + ux * L * f - nx * w / 2, pz + uz * L * f - nz * w / 2, sw=0.15)
    # cilindro de elevación
    v.line(5600, 2400, px + ux * 8000, pz + uz * 8000, sw=0.6, stroke=STEEL)
    tx, tz = px + ux * L, pz + uz * L
    v.circle(tx, tz, 300, fill=DARK, sw=0.1)
    v.line(tx, tz - 300, tx, hook_z + 600, sw=0.15)
    v.rect(tx - 300, hook_z, tx + 300, hook_z + 600, fill=DARK, sw=0.1)            # pasteca
    v.pline([(tx, hook_z), (tx, hook_z - 300), (tx + 150, hook_z - 450), (tx + 260, hook_z - 300)], sw=0.3)
    return tx, tz, px, pz


def balancin(v, xc, z_hook, z_beam, half, z_piece, pick):
    """balancín: eslingas a 60° gancho -> extremos de la viga, y eslingas verticales a los insertos"""
    v.line(xc, z_hook - 400, xc - half, z_beam + 250, sw=0.2); v.line(xc, z_hook - 400, xc + half, z_beam + 250, sw=0.2)
    v.rect(xc - half - 200, z_beam, xc + half + 200, z_beam + 300, fill=YEL, sw=0.2)
    for s in (-1, 1):
        v.circle(xc + s * half, z_beam + 300, 90, sw=0.15)
        v.line(xc + s * pick, z_beam, xc + s * pick, z_piece, sw=0.2)
        v.circle(xc + s * pick, z_beam - 80, 80, sw=0.12)


def make(num, total):
    sh = Sheet(num, total, "Máquinas y dispositivos 1", "Montaje: grúa telescópica, transporte en carretón y balancín de izaje",
               "Grúa 1:300 · carretón 1:200 · balancín 1:100 · accesorios s/ escala")
    heading(sh, "3º MÁQUINAS Y DISPOSITIVOS DE MONTAJE  ·  1/3", "Equipos para transportar, izar y posicionar las piezas premoldeadas (pieza crítica: VP 14,58 m · 12,6 t)")

    # ============================================================ M1 GRÚA 1:300
    sh.title_drawing(10, 26, "M1 · GRÚA TELESCÓPICA AUTOPROPULSADA 90 t", "Vista lateral 1:300 · izando una VP al nivel +4,50", 2.2)
    v = sh.view(18, 121, 300)
    tx, tz, px, pz = grua(v)
    # pórtico existente + VP izada
    for xc in (21000, 36000):
        v.rect(xc - 200, 0, xc + 200, geo.COL_TOP, fill="#cfd3d7", sw=0.12)
        v.poly([(xc - 200, 3655), (xc - 550, 3655), (xc - 550, 3495), (xc - 200, 3185)], fill="#cfd3d7", sw=0.1)
    zp = 5400
    v.rect(tx - 7290, zp, tx + 7290, zp + 750, fill=geo.C_VP, sw=0.2)
    balancin(v, tx, 15500, 11300, 4500, zp + 750, 4375)
    for s in (-1, 1): v.line(tx + s * 7290, zp + 300, tx + s * 7290 + s * 1500, zp - 1800, sw=0.1, dash="0.6 0.3")
    sh.text(*v.P(tx + 8000, zp - 2100), "sogas guía", 1.3)
    ground(sh, v.P(-1500, 0)[0], v.P(40000, 0)[0], v.P(0, 0)[1])
    v.dim((4800, 0), (tx, 0), -5.5, f"radio de trabajo R = {(tx - 4800) / 1000:.1f} m".replace(".", ","), size=1.4)
    v.dim((-1200, 0), (-1200, tz), 2.5, f"{tz / 1000:.1f} m".replace(".", ","), size=1.4)
    v.dim((0, -2500), (13500, -2500), 0, "13,50", size=1.3)
    v.line(4800, 0, 4800, 28000, stroke="#b22", sw=0.1, dash="2 0.6 0.4 0.6")
    sh.text(*v.P(4900, 22000), "eje de giro", 1.3, color="#b22")
    for lab, tgt, at in (("1", (px + 12000 * math.cos(math.radians(58)), pz + 12000 * math.sin(math.radians(58))), (40, 50)),
                         ("2", (2100, 3300), (14, 92)), ("3", (900, 600), (14, 104)), ("4", (6900, 3800), (40, 84)),
                         ("5", (tx, 15800), (110, 40)), ("6", (tx - 3000, 11450), (110, 62)), ("7", (tx + 4000, zp + 375), (110, 100))):
        sh.callout(v.P(*tgt), at, lab, r=1.5)
    legend = ["Pluma telescópica 4 tramos (26 m de trabajo)", "Contrapeso desmontable (viaja en camión aparte)",
              "Estabilizadores c/ placas de reparto 0,9 x 0,9", "Cabina de operación (giro 360°)", "Pasteca y gancho c/ seguro",
              "Balancín de izaje (M3)", "VP 14,58 m · 12,6 t"]
    yy = 74
    for k, t in enumerate(legend):
        sh.text(206, yy + k * 2.5, f"{k + 1}  {t}", 1.4)
    # tabla de carga
    sh.text(206, 95, "TABLA DE CARGA (pluma 26 m, contrapeso total, 360°)", 1.6, bold=True)
    rows = [("R (m)", "8", "10", "12", "14", "16", "18"), ("Cap. (t)", "38,0", "30,5", "24,0", "19,5", "16,0", "13,0")]
    sh.table(206, 96.5, [14, 11.5, 11.5, 11.5, 11.5, 11.5, 11.5], rows, size=1.4, rowh=3.0, fills=[None, None])
    sh.para(206, 106.5, 83, "Verificación: VP 12,6 t + balancín 0,8 t + eslingas 0,2 t = 13,6 t ≤ 0,75 x 19,5 t (R = 14 m) → 14,6 t ✓. "
            "Se usa la tabla del fabricante del equipo alquilado.", 1.4, 1.25)

    # ============================================================ M2 CARRETÓN 1:200
    sh.title_drawing(10, 136, "M2 · TRACTOR + SEMIRREMOLQUE CARRETÓN EXTENSIBLE", "Vista lateral 1:200 · transporte de la VP (pieza > 12 m)", 2.0)
    c = sh.view(14, 179, 200)
    for x in (900, 4300, 5650): wheel(c, x, 520)
    c.rect(0, 800, 6400, 1300, fill="#c0392b", sw=0.15)
    c.poly([(0, 1300), (2400, 1300), (2400, 3700), (300, 3700), (0, 3000)], fill="#c0392b", sw=0.15)
    c.rect(400, 2500, 2200, 3400, fill="#bfe3f0", sw=0.08)
    c.rect(4300, 1300, 5800, 1500, fill=DARK, sw=0.1)                              # quinta rueda
    c.poly([(4000, 1500), (6200, 1500), (6200, 1150), (21500, 1150), (21500, 1500), (21800, 1500), (21800, 900), (4300, 900)], fill="#7f8c8d", sw=0.15)
    for x in (17800, 19200, 20600): wheel(c, x, 520)
    c.rect(6400, 1500, 6600, 2200, fill=DARK, sw=0.08)
    for x in (9000, 14000, 19500): c.rect(x - 150, 1500, x + 150, 1650, fill="#8b5a2b", sw=0.06)
    c.rect(6700, 1650, 6700 + 14580, 1650 + 750, fill=geo.C_VP, sw=0.2)
    for x in (9000, 14000, 19500): c.line(x, 2400, x + 600, 1150, sw=0.12)
    ground(sh, c.P(-500, 0)[0], c.P(23000, 0)[0], c.P(0, 0)[1])
    c.dim((0, -200), (21800, -200), -2.5, "≈ 21,80 (largo total: requiere permiso de tránsito)", size=1.35)
    c.dim((22300, 0), (22300, 2400), -2.5, "2,40", size=1.3)
    sh.note(c.P(14000, 2000), (60, 153), "VP s/ tacos de madera y fajas de amarre c/ cantoneras", 1.35)

    # ============================================================ M3 BALANCÍN 1:100
    sh.title_drawing(150, 136, "M3 · BALANCÍN (VIGA DE IZAJE) + ESLINGAS", "Esquema 1:100 · izaje de un panel TT (4 insertos)", 2.0)
    b = sh.view(150, 186, 100)
    b.rect(0, 0, 9580, 650, fill=geo.C_TT, sw=0.2)
    b.line(0, 600, 9580, 600, sw=0.08)
    xc = 4790
    b.rect(xc - 3100, 2000, xc + 3100, 2300, fill=YEL, sw=0.2)
    for s in (-1, 1):
        b.line(xc, 4100, xc + s * 1200, 2300, sw=0.22)
        b.line(xc + s * 2874, 2000, xc + s * 2874, 650, sw=0.22)
        b.circle(xc + s * 2874, 600, 70, fill="#000", sw=0.05)
    b.rect(xc - 200, 4100, xc + 200, 4500, fill=DARK, sw=0.1)
    b.dim((xc - 2874, 0), (xc + 2874, 0), -2.3, "insertos a L/5 de los extremos", size=1.25)
    sh.text(*b.P(xc + 1100, 3500), "≥ 45° c/ la horizontal", 1.35)
    sh.text(250, 150, "Accesorios", 1.6, bold=True)
    sh.bullets(250, 153.5, 39, ["Grillete tipo lira c/ perno roscado", "Eslinga de cable de acero o faja poliéster (c/ etiqueta CMU)",
              "Argolla giratoria roscada al inserto", "Gancho c/ lengüeta de seguridad", "Sogas guía (vientos) p/ orientar la pieza",
              "Cuñas, calces y cantoneras"], size=1.3, lead=1.2, gap=0.3)

    # ============================================================ ESPECIFICACIONES (arriba derecha)
    spec(sh, 206, 26, 83, "Función y uso", [
        ("M1 Grúa:", "eleva y posiciona columnas, vigas y TT; trabaja SIEMPRE sobre estabilizadores extendidos y placas de reparto sobre suelo compactado."),
        ("Capacidad:", "90 t nominal (a 3 m); se elige por el par carga x radio de la pieza más pesada y más lejana, no por la capacidad nominal."),
        ("M2 Carretón:", "semirremolque extensible 12-25 m, capacidad 30 t; las piezas > 12 m o > 2,60 m de ancho viajan c/ permiso y escolta."),
        ("M3 Balancín:", "reparte la carga en 2 o 4 puntos con tiros verticales: evita compresión axial en la pieza y flexión no prevista; las eslingas a la grúa forman ≥ 45° con la horizontal."),
        ("Señalero:", "rigger habilitado coordina por radio con el operador; zona de exclusión bajo la carga."),
    ], size=1.45, tsize=1.9)
    return sh
