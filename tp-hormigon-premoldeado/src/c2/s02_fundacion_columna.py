# -*- coding: utf-8 -*-
"""Lámina 02 – E1 fundación tipo cáliz y E2 columna premoldeada con ménsulas cortas."""
from lib import Sheet, Iso, spec, heading, breakline, ground, REB
import geo

VISTA = "#eceeef"


def zig(v, x, y0, y1, amp=12, step=60):
    pts, y, s = [], y0, 1
    while y <= y1:
        pts.append((x + amp * s, y)); y += step; s = -s
    v.pline(pts, sw=0.12)


def make(num, total):
    sh = Sheet(num, total, "Elementos constructivos 1", "E1 Fundación tipo cáliz · E2 Columna premoldeada pretensada c/ ménsulas",
               "Corte y planta E1 1:50 · vistas columna 1:100 · sección y ménsula 1:20 · isometría 1:150")
    heading(sh, "1º ELEMENTOS CONSTRUCTIVOS DEL SISTEMA  ·  1/3", "Croquis a escala con medidas, función y especificación técnica (valores de catálogo de premoldeados, verificar con el fabricante)")

    # ============================================================ E1 · CORTE 1:50
    sh.title_drawing(10, 26, "E1 · FUNDACIÓN TIPO CÁLIZ", None, 2.5)
    sh.text(10, 30, "Corte por eje de columna 1:50", 1.6, color="#222")
    v = sh.view(38, 43, 50)
    v.rect(-1150, -2150, 1150, -150, mat="tierra", stroke=None)
    v.rect(-1050, -2150, 1050, -2050, mat="H", sw=0.15)
    v.poly([(-1000, -2050), (1000, -2050), (1000, -1750), (525, -1450), (-525, -1450), (-1000, -1750)], mat="HAis", sw=0.3)
    v.poly([(-525, -1450), (525, -1450), (525, -510), (275, -510), (275, -1350), (-275, -1350), (-275, -510), (-525, -510)], mat="HAis", sw=0.3)
    v.rect(-275, -1350, 275, -510, mat="grout", sw=0.15)
    v.rect(-200, -1300, 200, 250, mat="HA", sw=0.3)
    sh.rect(*v.P(-200, 250), *v.P(200, 330), fill="#fff", stroke=None)
    breakline(sh, v.P(-260, 250), v.P(260, 250))
    for s in (-1, 1):
        zig(v, s * 275, -1330, -560); zig(v, s * 200, -1290, -560, amp=8)
        v.poly([(s * 205, -510), (s * 270, -510), (s * 215, -620)], fill="#6b4f2a", stroke="#000", sw=0.08)     # cuñas
    v.pline([(-940, -1880), (-940, -1985), (940, -1985), (940, -1880)], stroke=REB, sw=0.2)
    for x in range(-900, 950, 150): v.dot(x, -1965, 0.25)
    for x in (-470, 470):
        v.pline([(x + (60 if x < 0 else -60), -1985), (x, -1985), (x, -560)], stroke=REB, sw=0.15)
    yg = v.P(0, -150)[1]
    ground(sh, v.P(-1150, 0)[0], v.P(-200, 0)[0], yg); ground(sh, v.P(200, 0)[0], v.P(1150, 0)[0], yg)
    v.dim((-1000, -2150), (1000, -2150), -2.5, "2,00")
    v.dim((-525, -510), (525, -510), 2.0, "1,05", size=1.5)
    v.dim((-275, -1350), (275, -1350), -1.8, "0,55", size=1.5)
    v.dim((1050, -2150), (1050, -2050), -2.0, "0,10", size=1.4)
    v.dim((1050, -2050), (1050, -1750), -2.0, "0,30", size=1.5)
    v.dim((1050, -1750), (1050, -1450), -2.0, "0,30", size=1.5)
    v.dim((1050, -1450), (1050, -510), -2.0, "0,94", size=1.5)
    v.dim((-1100, -1300), (-1100, -510), 2.0, "0,79", size=1.5)
    sh.level(*v.P(-1150, -150), "NTN -0,15", 1.4)
    sh.level(*v.P(1150, -510), "-0,51", 1.4)
    sh.level(*v.P(1150, -2150), "-2,15", 1.4)
    for lab, tgt, at in (("1", (-700, -1900), (10, 74)), ("2", (-400, -1000), (10, 62)), ("3", (100, 0), (54, 36)),
                         ("4", (240, -900), (73, 52)), ("5", (238, -560), (73, 45)), ("6", (-275, -900), (10, 52)), ("7", (500, -2100), (73, 84))):
        sh.callout(v.P(*tgt), at, lab, r=1.6)
    # planta 1:50
    sh.text(64, 92, "Planta 1:50", 1.6, color="#222")
    p = sh.view(84, 116, 50)
    p.rect(-1000, -1000, 1000, 1000, fill="#f3f0ea", sw=0.25)
    for sx in (-1, 1):
        for sy in (-1, 1):
            p.line(sx * 1000, sy * 1000, sx * 525, sy * 525, sw=0.12)
    p.rect(-525, -525, 525, 525, mat="HAis", sw=0.3)
    p.rect(-275, -275, 275, 275, mat="grout", sw=0.15)
    p.rect(-200, -200, 200, 200, mat="HA", sw=0.3)
    p.dim((-1000, -1000), (1000, -1000), -2.2, "2,00", size=1.5)
    p.dim((1000, -525), (1000, 525), -2.4, "1,05", size=1.4)
    p.dim((-1000, -200), (-1000, 200), 2.4, "0,40", size=1.4)
    sh.text(10, 117, "Holgura columna / alvéolo: 7,5 cm por lado", 1.45, ital=True, color="#333")
    leg = ["1 Base H°A° H-25 colada in situ, parrilla Ø12 c/15", "2 Cuello (cáliz) H°A° in situ, pared e = 0,25",
           "3 Columna premoldeada 40x40 (E2)", "4 Relleno microhormigón / grout sin retracción", "5 Cuñas de madera dura o acero p/ aplomar (se retiran)",
           "6 Llaves de corte (superficie rugosa) en alvéolo y columna", "7 H° de limpieza H-8, e = 0,10"]
    yy = 94
    for t in leg: sh.text(10, yy, t, 1.5); yy += 2.6
    spec(sh, 10, 142, 94, "E1 · Especificación", [
        ("Función:", "transmitir al suelo las cargas de la columna y materializar su EMPOTRAMIENTO (la estructura premoldeada articulada en vigas se estabiliza por las columnas empotradas)."),
        ("Medidas:", "base 2,00 x 2,00 x 0,30 + tronco 0,30; cuello 1,05 x 1,05; alvéolo 0,55 x 0,55, prof. 0,84; cota de fundación -2,15 (s/ estudio de suelos)."),
        ("Máx./mín.:", "empotramiento ≥ 1,5 a 2 veces el lado de la columna (mín. 0,60 m); pared del cáliz ≥ 0,20 m; holgura 5 a 8 cm por lado para aplomar."),
        ("Materiales:", "H-25, acero ADN 420, recubrimiento 5 cm; relleno grout cementicio sin retracción ≥ 30 MPa."),
        ("Colocación:", "excavar, H° de limpieza, armar base y cuello, encofrar el alvéolo con molde rugoso (llaves de corte), hormigonar; montar la columna, aplomar con cuñas y puntales, rellenar con grout y retirar cuñas a las 24-48 h."),
    ], size=1.6)

    # ============================================================ E2 · VISTAS 1:100
    sh.title_drawing(112, 26, "E2 · COLUMNA PREMOLDEADA PRETENSADA 40x40", None, 2.5)
    sh.text(112, 30, "Vista frontal (desde fachada) y lateral 1:100", 1.6, color="#222")
    for ox, lateral in ((128, False), (160, True)):
        v = sh.view(ox, 124, 100)
        v.rect(-200, geo.COL_BOT, 200, geo.COL_TOP, fill=VISTA, sw=0.3)
        for yt in (3495, 7995):
            if not lateral:
                for s in (-1, 1):
                    v.poly([(s * 200, yt), (s * 530, yt), (s * 530, yt - 160), (s * 200, yt - 470)], fill=VISTA, sw=0.3)
                    v.line(s * 365, yt - 260, s * 365, yt, sw=0.1, dash="0.8 0.4")
            else:
                v.line(-200, yt, 200, yt, sw=0.15); v.line(-200, yt - 470, 200, yt - 470, sw=0.1, dash="0.8 0.4")
        if lateral:
            for yt in (3655, 8155):
                v.poly([(200, yt), (550, yt), (550, yt - 160), (200, yt - 470)], fill=VISTA, sw=0.3)
                v.line(375, yt - 260, 375, yt, sw=0.1, dash="0.8 0.4")
        # cáliz en corte (esquemático)
        v.poly([(-1000, -2050), (1000, -2050), (1000, -1750), (525, -1450), (525, -510), (275, -510), (275, -1350), (-275, -1350), (-275, -510),
                (-525, -510), (-525, -1450), (-1000, -1750)], fill="#f4f1ea", sw=0.15, dash="0.8 0.4")
        v.rect(-200, geo.COL_BOT, 200, -510, fill=VISTA, sw=0.25)
        sh.line(v.P(-1300, -150)[0], v.P(0, -150)[1], v.P(1300, -150)[0], v.P(0, -150)[1], sw=0.25)
        v.circle(0, geo.COL_TOP - 250, 60, sw=0.15)                    # inserto de izaje
        v.dim((-200, geo.COL_BOT), (-200, geo.COL_TOP), 5.5 if not lateral else 3.5, "10,22")
    v1 = sh.view(128, 124, 100)
    sh.text(128, 147, "FRONTAL", 1.5, anchor="middle", bold=True); sh.text(160, 147, "LATERAL", 1.5, anchor="middle", bold=True)
    for z, t in ((geo.COL_TOP, "+8,92"), (7995, "+8,00 apoyo VL"), (3495, "+3,50 apoyo VL"), (0, "±0,00"), (-510, "-0,51"), (geo.COL_BOT, "-1,30")):
        sh.level(v1.P(560, z)[0] + 1, v1.P(0, z)[1], t, 1.35)
    v2 = sh.view(160, 124, 100)
    for z, t in ((8155, "+8,16 apoyo VP"), (3655, "+3,66 apoyo VP")):
        sh.level(v2.P(560, z)[0] + 1, v2.P(0, z)[1], t, 1.35)
    sh.note(v1.P(0, geo.COL_TOP - 250), (114, 36), "Inserto de izaje", 1.4, anchor="end")

    # ============================================================ sección 1:20
    sh.text(186, 30, "Sección A-A 1:20", 1.6, color="#222")
    s = sh.view(194, 45, 20)
    s.rect(-200, -200, 200, 200, mat="HA", sw=0.35)
    s.rect(-160, -160, 160, 160, fill="none", stroke=REB, sw=0.18)
    for x in (-150, 0, 150):
        for y in (-150, 150): s.dot(x, y, 0.42, "#000")
    for y in (0,):
        for x in (-150, 150): s.dot(x, y, 0.42, "#000")
    s.dim((-200, -200), (200, -200), -2.5, "0,40", size=1.5)
    s.dim((200, -200), (200, 200), -2.5, "0,40", size=1.5)
    sh.text(186, 61, "8 cordones Ø12,7 + estribos Ø8 c/15", 1.35)
    sh.text(186, 63.4, "recubrimiento 3 cm · H-40", 1.35)

    # ============================================================ ménsula 1:20
    sh.text(210, 30, "Ménsula corta (apoyo VL) 1:20", 1.6, color="#222")
    m = sh.view(224, 42, 20)
    m.rect(-250, -620, 0, 200, fill=VISTA, sw=0.3)
    breakline(sh, m.P(-300, 200), m.P(40, 200)); breakline(sh, m.P(-300, -620), m.P(40, -620))
    m.poly([(0, 0), (330, 0), (330, -160), (0, -470)], mat="HA", sw=0.35)
    m.rect(15, 0, 315, 10, mat="neo", stroke=None)
    m.pline([(-200, -40), (300, -40), (300, -150)], stroke=REB, sw=0.2)
    m.pline([(-200, -420), (40, -440), (300, -170)], stroke=REB, sw=0.15)
    for y in (-100, -200, -300): m.line(-30, y, 300 if y > -170 else 300 - (-170 - y) * 0.9, y, stroke=REB, sw=0.1)
    m.rect(155, -260, 175, 170, mat="acero", sw=0.05)
    m.dim((0, 0), (330, 0), 3.4, "0,33", size=1.4)
    m.dim((330, 0), (330, -160), 2.0, "0,16", size=1.4)
    m.dim((330, 0), (330, -470), 6.0, "0,47", size=1.4)
    sh.note(m.P(165, 150), (250, 33), "Perno Ø20", 1.35)
    sh.note(m.P(250, 5), (250, 38.5), "Neopreno 10 mm", 1.35)
    sh.note(m.P(200, -40), (250, 52), "Tensor sup.", 1.35)
    sh.note(m.P(100, -400), (250, 62), "Armad. diagonal", 1.35)

    # ============================================================ isometría
    S = Iso((1, -1, 1))
    h = 200
    S.box(-1000, 1000, -1000, 1000, -2050, -1750, geo.C_FUND, sw=0.1)
    S.box(-525, 525, -525, 525, -1750, -510, geo.C_FUND, sw=0.1)
    S.box(-h, h, -h, h, -510, geo.COL_TOP, geo.C_COL, sw=0.12)
    for yt in (3495, 7995):
        for sd in (1, -1):
            S.prism([(sd * (h + u) if sd > 0 else -(h + u), yt + vv) for u, vv in geo.mensula_pts(1)], "y", -h, h, geo.C_COL, sw=0.12)
    for yt in (3655, 8155):
        S.prism([(h + u, yt + vv) for u, vv in geo.mensula_pts(1, saliente=350)], "x", -h, h, geo.C_COL, sw=0.12)
    ox, oy = S.fit((266, 76, 289, 150), 150)
    S.draw(sh, ox, oy, 150)
    sh.text(262, 72, "Isometría 1:150", 1.5, color="#222")
    sh.text(262, 74.5, "(ménsulas VL y VP)", 1.35, color="#222")

    spec(sh, 186, 82, 72, "E2 · Especificación", [
        ("Función:", "recibir las vigas VL y VP en sus ménsulas y llevar las cargas al cáliz; con el empotramiento da la estabilidad lateral del pórtico."),
        ("Medidas:", "40 x 40 cm, largo 10,22 m de una pieza (2 niveles); ménsulas cortas 33-35 x 47 cm (frente 16)."),
        ("Máx./mín.:", "secciones de catálogo 30x30 a 60x60; largo ≤ 14-18 m (transporte y volteo); ménsula ≥ 25 cm de apoyo."),
        ("Materiales:", "H-40/H-45 vibrado, cordones de acero de pretensado Ø12,7 grado 1860, estribos ADN 420."),
        ("Peso:", "≈ 4,5 t (0,40 x 0,40 x 10,22 x 2,5 t/m³ + ménsulas)."),
        ("Insertos:", "vainas Ø40 p/ pernos de apoyo, insertos de izaje roscados, placas p/ arriostres provisorios."),
        ("Colocación:", "volteo con grúa y 2 puntos de tiro; se introduce en el cáliz, se aploma (± 5 mm) con cuñas y puntales, se rellena con grout y recién a las 48 h se montan las vigas."),
    ], size=1.55)
    return sh
