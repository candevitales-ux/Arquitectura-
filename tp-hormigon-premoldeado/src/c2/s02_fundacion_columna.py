# -*- coding: utf-8 -*-
"""E1 fundación tipo cáliz y E2 columna premoldeada con ménsulas cortas (una lámina cada una)."""
from lib import Sheet, Iso, page, spec, heading, breakline, ground, REB, TB, TS, TD, TT
import geo

VISTA = "#eceeef"


def zig(v, x, y0, y1, amp=12, step=60):
    pts, y, s = [], y0, 1
    while y <= y1:
        pts.append((x + amp * s, y)); y += step; s = -s
    v.pline(pts, sw=0.12)


def legend(sh, x, y, items, w=186, size=TS):
    for t in items:
        lab, txt = t.split(" ", 1)
        sh.ball(x + 2.2, y - 0.8, lab, r=2.0)
        y = sh.para(x + 6, y, w - 6, txt, size, 1.25) + 1.2
    return y


@page("E1 · Fundación tipo cáliz")
def fundacion(num, total):
    sh = Sheet(num, total, "E1 · Fundación tipo cáliz", escalas="corte 1:25 · planta 1:50", fname="E1_Fundacion_Caliz")
    heading(sh, "1º ELEMENTOS · E1 FUNDACIÓN TIPO CÁLIZ", "Base y cuello de H°A° colados in situ que reciben y empotran la columna premoldeada")
    sh.title_drawing(12, 32, "CORTE POR EJE DE COLUMNA", "esc. 1:25", TT)
    v = sh.view(62, 52, 25)
    v.rect(-1150, -2150, 1150, -150, mat="tierra", stroke=None)
    v.rect(-1050, -2150, 1050, -2050, mat="H", sw=0.15)
    v.poly([(-1000, -2050), (1000, -2050), (1000, -1750), (525, -1450), (-525, -1450), (-1000, -1750)], mat="HAis", sw=0.35)
    v.poly([(-525, -1450), (525, -1450), (525, -510), (275, -510), (275, -1350), (-275, -1350), (-275, -510), (-525, -510)], mat="HAis", sw=0.35)
    v.rect(-275, -1350, 275, -510, mat="grout", sw=0.15)
    v.rect(-200, -1300, 200, 250, mat="HA", sw=0.35)
    breakline(sh, v.P(-260, 250), v.P(260, 250))
    for s in (-1, 1):
        zig(v, s * 275, -1330, -560); zig(v, s * 200, -1290, -560, amp=8)
        v.poly([(s * 205, -510), (s * 270, -510), (s * 215, -620)], fill="#6b4f2a", stroke="#000", sw=0.08)
    v.pline([(-940, -1880), (-940, -1985), (940, -1985), (940, -1880)], stroke=REB, sw=0.25)
    for x in range(-900, 950, 150): v.dot(x, -1965, 0.4)
    for x in (-430, 430):
        v.pline([(x + (60 if x < 0 else -60), -1985), (x, -1985), (x, -560)], stroke=REB, sw=0.2)
    yg = v.P(0, -150)[1]
    ground(sh, v.P(-1150, 0)[0], v.P(-200, 0)[0], yg); ground(sh, v.P(200, 0)[0], v.P(1150, 0)[0], yg)
    v.dim((-1000, -2150), (1000, -2150), -4.0, "2,00")
    v.dim((-525, -510), (525, -510), 3.0, "1,05")
    v.dim((-275, -1350), (275, -1350), -3.0, "0,55")
    v.dim((1050, -2150), (1050, -2050), -4.0, "0,10")
    v.dim((1050, -2050), (1050, -1750), -4.0, "0,30")
    v.dim((1050, -1750), (1050, -1450), -4.0, "0,30")
    v.dim((1050, -1450), (1050, -510), -4.0, "0,94")
    v.dim((-1150, -1300), (-1150, -510), 4.0, "0,79")
    sh.level(*v.P(-1150, -150), "NTN -0,15")
    sh.level(*v.P(1250, -510), "-0,51")
    sh.level(*v.P(1250, -2150), "-2,15")
    for lab, tgt, at in (("1", (-700, -1900), (14, 132)), ("2", (-400, -1000), (14, 112)), ("3", (100, 0), (100, 52)),
                         ("4", (240, -900), (115, 96)), ("5", (238, -560), (115, 78)), ("6", (-275, -1150), (14, 98)), ("7", (500, -2100), (115, 140))):
        sh.callout(v.P(*tgt), at, lab)
    # planta 1:50
    sh.title_drawing(140, 32, "PLANTA", "esc. 1:50", TT)
    p = sh.view(168, 72, 50)
    p.rect(-1000, -1000, 1000, 1000, fill="#f3f0ea", sw=0.25)
    for sx in (-1, 1):
        for sy in (-1, 1): p.line(sx * 1000, sy * 1000, sx * 525, sy * 525, sw=0.12)
    p.rect(-525, -525, 525, 525, mat="HAis", sw=0.3)
    p.rect(-275, -275, 275, 275, mat="grout", sw=0.15)
    p.rect(-200, -200, 200, 200, mat="HA", sw=0.3)
    p.dim((-1000, -1000), (1000, -1000), -3.5, "2,00")
    p.dim((1000, -525), (1000, 525), -3.5, "1,05")
    sh.para(140, 102, 60, "Holgura columna / alvéolo: 7,5 cm por lado para aplomar.", TS, 1.25, ital=True)
    y = 154
    sh.text(12, y, "REFERENCIAS", TT, bold=True); y += 6
    y = legend(sh, 12, y, ["1 Base H°A° H-25 colada in situ, parrilla Ø12 c/15", "2 Cuello (cáliz) H°A° in situ, pared e = 0,25 m",
                           "3 Columna premoldeada 40x40 (E2)", "4 Relleno microhormigón / grout sin retracción",
                           "5 Cuñas de madera dura o acero p/ aplomar (se retiran)", "6 Llaves de corte (superficie rugosa) en alvéolo y columna",
                           "7 H° de limpieza H-8, e = 0,10 m"])
    spec(sh, 12, y + 8, 186, "ESPECIFICACIÓN", [
        ("Función:", "transmitir al suelo las cargas de la columna y materializar su EMPOTRAMIENTO: la estructura premoldeada (vigas articuladas) se estabiliza por las columnas empotradas."),
        ("Medidas:", "base 2,00 x 2,00 x 0,30 + tronco 0,30; cuello 1,05 x 1,05; alvéolo 0,55 x 0,55, prof. 0,84; fundación a -2,15 (s/ estudio de suelos)."),
        ("Máx./mín.:", "empotramiento ≥ 1,5 a 2 veces el lado de la columna (mín. 0,60 m); pared del cáliz ≥ 0,20 m; holgura 5 a 8 cm por lado."),
        ("Materiales:", "H-25, acero ADN 420, recubrimiento 5 cm; relleno grout cementicio sin retracción ≥ 30 MPa."),
        ("Colocación:", "excavar, H° de limpieza, armar base y cuello, encofrar el alvéolo con molde rugoso, hormigonar; montar la columna, aplomar con cuñas y puntales, rellenar con grout y retirar cuñas a las 24-48 h."),
    ])
    return sh


@page("E2 · Columna premoldeada c/ ménsulas")
def columna(num, total):
    sh = Sheet(num, total, "E2 · Columna premoldeada pretensada", escalas="vistas 1:100 · sección y ménsula 1:10 · isometría 1:150", fname="E2_Columna")
    heading(sh, "1º ELEMENTOS · E2 COLUMNA PREMOLDEADA 40x40", "Columna pretensada de una pieza (2 niveles) con ménsulas cortas para apoyar las vigas VL y VP")
    sh.title_drawing(12, 32, "VISTAS", "esc. 1:100", TT)
    for ox, lateral in ((30, False), (68, True)):
        v = sh.view(ox, 141, 100)
        v.rect(-200, geo.COL_BOT, 200, geo.COL_TOP, fill=VISTA, sw=0.3)
        for yt in (3495, 7995):
            if not lateral:
                for s in (-1, 1):
                    v.poly([(s * 200, yt), (s * 530, yt), (s * 530, yt - 160), (s * 200, yt - 470)], fill=VISTA, sw=0.3)
            else:
                v.line(-200, yt, 200, yt, sw=0.15); v.line(-200, yt - 470, 200, yt - 470, sw=0.1, dash="0.8 0.4")
        if lateral:
            for yt in (3655, 8155):
                v.poly([(200, yt), (550, yt), (550, yt - 160), (200, yt - 470)], fill=VISTA, sw=0.3)
        v.poly([(-1000, -2050), (1000, -2050), (1000, -1750), (525, -1450), (525, -510), (275, -510), (275, -1350), (-275, -1350), (-275, -510),
                (-525, -510), (-525, -1450), (-1000, -1750)], fill="#f4f1ea", sw=0.15, dash="0.8 0.4")
        v.rect(-200, geo.COL_BOT, 200, -510, fill=VISTA, sw=0.25)
        sh.line(v.P(-1300, 0)[0], v.P(0, -150)[1], v.P(1300, 0)[0], v.P(0, -150)[1], sw=0.25)
        v.circle(0, geo.COL_TOP - 250, 60, sw=0.15)
        v.dim((-200, geo.COL_BOT), (-200, geo.COL_TOP), 7.0, "10,22")
        sh.text(ox, 167, "LATERAL" if lateral else "FRONTAL", TS, anchor="middle", bold=True)
    v1 = sh.view(30, 141, 100); v2 = sh.view(68, 141, 100)
    for z, t in ((geo.COL_TOP, "+8,92"), (7995, "+8,00"), (3495, "+3,50"), (-510, "-0,51")):
        sh.level(v1.P(600, z)[0] + 1, v1.P(0, z)[1], t)
    for z, t in ((8155, "+8,16"), (3655, "+3,66"), (0, "±0,00"), (geo.COL_BOT, "-1,30")):
        sh.level(v2.P(600, z)[0] + 1, v2.P(0, z)[1], t)
    sh.note(v1.P(0, geo.COL_TOP - 250), (40, 40), "inserto de izaje")
    sh.para(12, 172, 90, "Frontal: ménsulas de las VL (a ambos lados, sobre la fachada). Lateral: ménsula de la VP (hacia el interior).", TS, 1.25, ital=True)
    # sección 1:10
    sh.title_drawing(108, 32, "SECCIÓN A-A", "esc. 1:10", TT)
    s = sh.view(128, 64, 10)
    s.rect(-200, -200, 200, 200, mat="HA", sw=0.35)
    s.rect(-160, -160, 160, 160, fill="none", stroke=REB, sw=0.25)
    for x in (-150, 0, 150):
        for y in (-150, 150): s.dot(x, y, 0.7, "#000")
    for x in (-150, 150): s.dot(x, 0, 0.7, "#000")
    s.dim((-200, -200), (200, -200), -3.5, "0,40")
    s.dim((200, -200), (200, 200), -3.5, "0,40")
    sh.para(108, 94, 46, "8 cordones Ø12,7 + estribos Ø8 c/15 · recubrimiento 3 cm · H-40", TS, 1.25)
    # isometría
    S = Iso((1, -1, 1)); h = 200
    S.box(-1000, 1000, -1000, 1000, -2050, -1750, geo.C_FUND, sw=0.1)
    S.box(-525, 525, -525, 525, -1750, -510, geo.C_FUND, sw=0.1)
    S.box(-h, h, -h, h, -510, geo.COL_TOP, geo.C_COL, sw=0.12)
    for yt in (3495, 7995):
        for sd in (1, -1):
            S.prism([(sd * (h + u), yt + vv) for u, vv in geo.mensula_pts(1)], "y", -h, h, geo.C_COL, sw=0.12)
    for yt in (3655, 8155):
        S.prism([(h + u, yt + vv) for u, vv in geo.mensula_pts(1, saliente=350)], "x", -h, h, geo.C_COL, sw=0.12)
    ox, oy = S.fit((166, 40, 200, 108), 150); S.draw(sh, ox, oy, 150)
    sh.text(160, 32, "ISOMETRÍA", TT, bold=True); sh.text(160, 37, "esc. 1:150", TS)
    # ménsula 1:10
    sh.title_drawing(108, 112, "MÉNSULA CORTA (apoyo VL)", "esc. 1:10", TT)
    m = sh.view(132, 140, 10)
    m.rect(-220, -520, 0, 120, fill=VISTA, sw=0.3)
    breakline(sh, m.P(-260, 120), m.P(30, 120)); breakline(sh, m.P(-260, -520), m.P(30, -520))
    m.poly([(0, 0), (330, 0), (330, -160), (0, -470)], mat="HA", sw=0.4)
    m.rect(15, 0, 315, 10, mat="neo", stroke=None)
    m.pline([(-180, -40), (300, -40), (300, -150)], stroke=REB, sw=0.3)
    m.pline([(-180, -420), (40, -440), (300, -170)], stroke=REB, sw=0.25)
    for y in (-100, -200): m.line(-30, y, 300, y, stroke=REB, sw=0.15)
    m.rect(155, -260, 175, 110, mat="acero", sw=0.05)
    m.dim((0, 0), (330, 0), 7.5, "0,33")
    m.dim((330, 0), (330, -160), -3.0, "0,16")
    m.dim((330, 0), (330, -470), -11.0, "0,47")
    sh.note(m.P(165, 90), (168, 124), "perno Ø20")
    sh.note(m.P(250, 5), (168, 130), "neopreno 10 mm")
    sh.note(m.P(200, -40), (178, 160), "tensor sup. Ø16")
    sh.note(m.P(100, -400), (150, 170), "armadura diagonal")
    spec(sh, 12, 205, 186, "ESPECIFICACIÓN", [
        ("Función:", "recibir las vigas VL y VP en sus ménsulas y llevar las cargas al cáliz; con el empotramiento da la estabilidad lateral del pórtico."),
        ("Medidas:", "40 x 40 cm, largo 10,22 m de una pieza; ménsulas cortas 33-35 x 47 cm (frente 16) · peso ≈ 4,5 t."),
        ("Máx./mín.:", "secciones de catálogo 30x30 a 60x60; largo ≤ 14-18 m (transporte y volteo); apoyo en ménsula ≥ 25 cm."),
        ("Materiales:", "H-40/H-45 vibrado, cordones de pretensado Ø12,7 grado 1860, estribos ADN 420; insertos de izaje y vainas Ø40 p/ pernos."),
        ("Colocación:", "volteo con grúa y 2 puntos de tiro; se introduce en el cáliz, se aploma (± 5 mm) con cuñas y puntales, se rellena con grout y a las 48 h se montan las vigas."),
    ])
    return sh


PAGES = [fundacion, columna]
