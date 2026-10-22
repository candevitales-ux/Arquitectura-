# -*- coding: utf-8 -*-
"""Lámina 06 – Detalles de uniones estructurales J1…J8."""
from lib import Sheet, heading, breakline, wrap, REB
import geo

VISTA = "#eceeef"
JY = "#fff1a8"
CW, CH = 69.75, 81.0


def cell(sh, i, j, lab, title, scale_txt):
    x0, y0 = 10 + i * CW, 24 + j * CH
    sh.rect(x0, y0, x0 + CW - 1.5, y0 + CH - 1.5, stroke="#999", sw=0.12, layer="MARCO")
    sh.ball(x0 + 3.6, y0 + 3.8, lab, r=2.4, fill=JY)
    sh.text(x0 + 7, y0 + 3.6, title, 1.75, bold=True)
    sh.text(x0 + 7, y0 + 6.2, scale_txt, 1.4, color="#333")
    return x0, y0


def legend(sh, x0, y, items, w=66):
    for k, t in enumerate(items):
        lines = wrap(t, w - 4, 1.32)
        sh.text(x0 + 1.5, y, f"{k + 1}", 1.32, bold=True)
        for ln in lines:
            sh.text(x0 + 4, y, ln, 1.32); y += 1.32 * 1.25
        y += 0.25
    return y


def make(num, total):
    sh = Sheet(num, total, "Juntas y uniones 2", "Detalles de las uniones de la estructura J1 a J8",
               "J1, J2, J3 y J8 1:25 · J5 1:20 · J6 1:15 · J4 1:10 · J7 1:5")
    heading(sh, "2º JUNTAS Y UNIONES DEL SISTEMA  ·  2/3", "Uniones de la estructura premoldeada (numeración de la lámina 05)")

    # ------------------------------------------------------------ J1 columna / cáliz 1:25
    x0, y0 = cell(sh, 0, 0, "J1", "Columna / cáliz", "Corte 1:25 · unión húmeda, empotramiento")
    v = sh.view(x0 + 34, y0 - 3, 25)
    v.rect(-700, -1420, 700, -300, mat="tierra", stroke=None)
    v.poly([(-525, -1420), (525, -1420), (525, -510), (275, -510), (275, -1350), (-275, -1350), (-275, -510), (-525, -510)], mat="HAis", sw=0.3)
    v.rect(-275, -1350, 275, -510, mat="grout", sw=0.12)
    v.rect(-200, -1300, 200, -330, mat="HA", sw=0.3)
    breakline(sh, v.P(-260, -330), v.P(260, -330))
    for s in (-1, 1):
        v.poly([(s * 205, -510), (s * 270, -510), (s * 215, -640)], fill="#6b4f2a", stroke="#000", sw=0.08)
        pts = [(s * (275 + (10 if k % 2 else 0)), -1330 + k * 55) for k in range(15)]
        v.pline(pts, sw=0.1)
        pts = [(s * (200 - (8 if k % 2 else 0)), -1290 + k * 55) for k in range(14)]
        v.pline(pts, sw=0.1)
        v.pline([(s * 420, -1400), (s * 420, -560)], stroke=REB, sw=0.14)
    for lab, tgt, at in (("1", (0, -800), (x0 + 60, y0 + 18)), ("2", (240, -1000), (x0 + 60, y0 + 30)), ("3", (400, -900), (x0 + 60, y0 + 42)),
                         ("4", (240, -560), (x0 + 60, y0 + 12)), ("5", (-275, -1100), (x0 + 6, y0 + 40))):
        sh.callout(v.P(*tgt), at, lab, r=1.4)
    v.dim((-700, -1300), (-700, -510), 1.5, "0,79", size=1.3)
    legend(sh, x0, y0 + 62, ["Columna premoldeada 40x40, superficie rugosa en el tramo empotrado",
                             "Grout sin retracción ≥ 30 MPa colado por gravedad en la holgura de 7,5 cm",
                             "Cuello / cáliz H°A° in situ (pared 0,25 m)", "Cuña de madera dura (aplomado ± 5 mm), se retira a las 24 h",
                             "Llaves de corte (dientes) en el alvéolo: transmiten el momento"])

    # ------------------------------------------------------------ J2 VL / ménsula 1:25
    x0, y0 = cell(sh, 1, 0, "J2", "Viga VL / ménsula de columna", "Corte longitudinal 1:25 · unión seca articulada")
    v = sh.view(x0 + 18, y0 + 39, 25)
    v.rect(-380, -500, 0, 720, fill=VISTA, sw=0.25)
    breakline(sh, v.P(-420, 720), v.P(40, 720)); breakline(sh, v.P(-420, -500), v.P(40, -500))
    v.poly([(0, -10), (330, -10), (330, -170), (0, -480)], mat="HA", sw=0.3)
    v.rect(10, 0, 1180, 700, mat="HA", sw=0.3)
    v.line(10, 150, 1180, 150, sw=0.1); v.line(10, 550, 1180, 550, sw=0.1)
    breakline(sh, v.P(1180, -40), v.P(1180, 740))
    sh.rect(*v.P(1180, 760), *v.P(1300, -60), fill="#fff", stroke=None)
    v.rect(20, -10, 320, 0, mat="neo", stroke=None)
    for xp in (165,):
        v.rect(xp - 22, 0, xp + 22, 190, mat="grout", sw=0.1)
        v.rect(xp - 10, -270, xp + 10, 175, mat="acero", sw=0.05)
    v.rect(0, 0, 10, 700, fill="#fff", sw=0.05)
    v.line(10, 45, 1180, 45, stroke=REB, sw=0.12, dash="1 0.4")
    for lab, tgt, at in (("1", (600, 350), (x0 + 50, y0 + 16)), ("2", (240, -5), (x0 + 50, y0 + 49)), ("3", (165, 120), (x0 + 30, y0 + 13)),
                         ("4", (165, -150), (x0 + 30, y0 + 55)), ("5", (5, 400), (x0 + 6, y0 + 12))):
        sh.callout(v.P(*tgt), at, lab, r=1.4)
    legend(sh, x0, y0 + 62, ["VL doble T 40x70 pretensada (apoyo ≥ 15 cm)", "Neopreno zunchado 10 mm (giro y dilatación libres)",
                             "Vaina Ø40 en la viga rellena c/ grout (2 por apoyo)", "Perno Ø20 anclado en la ménsula: antivuelco y anti-deslizamiento",
                             "Junta 1 cm viga / columna (sin contacto)"])

    # ------------------------------------------------------------ J3 VP / ménsula 1:25
    x0, y0 = cell(sh, 2, 0, "J3", "Viga VP / ménsula de columna", "Corte longitudinal 1:25 · unión seca articulada")
    v = sh.view(x0 + 18, y0 + 40.5, 25)
    v.rect(-380, -500, 0, 770, fill=VISTA, sw=0.25)
    breakline(sh, v.P(-420, 770), v.P(40, 770)); breakline(sh, v.P(-420, -500), v.P(40, -500))
    v.poly([(0, -10), (350, -10), (350, -170), (0, -480)], mat="HA", sw=0.3)
    v.rect(10, 0, 1180, 750, mat="HA", sw=0.3)
    v.line(10, 150, 1180, 150, sw=0.1)
    sh.rect(*v.P(1180, 790), *v.P(1300, -60), fill="#fff", stroke=None)
    breakline(sh, v.P(1180, -40), v.P(1180, 790))
    v.rect(20, -10, 340, 0, mat="neo", stroke=None)
    v.rect(175 - 22, 0, 175 + 22, 200, mat="grout", sw=0.1)
    v.rect(175 - 10, -270, 175 + 10, 185, mat="acero", sw=0.05)
    v.rect(0, 0, 10, 750, fill="#fff", sw=0.05)
    for x in range(200, 1180, 120): v.dot(x, 45, 0.25, "#000")
    for lab, tgt, at in (("1", (700, 450), (x0 + 50, y0 + 15)), ("2", (260, -5), (x0 + 50, y0 + 49)), ("3", (175, 120), (x0 + 30, y0 + 12)),
                         ("4", (300, -100), (x0 + 30, y0 + 55))):
        sh.callout(v.P(*tgt), at, lab, r=1.4)
    legend(sh, x0, y0 + 62, ["VP T invertida h 0,75 (12,6 t): apoyo ≥ 20 cm", "Neopreno 10 mm 300 x 320",
                             "Perno Ø20 en vaina Ø40 c/ grout (1 por apoyo, centrado)", "Ménsula corta c/ diagonal: tensor sup. Ø16 + estribos",
                             "Orden: se monta la VP antes que los TT; se colan las vainas al final del nivel"])

    # ------------------------------------------------------------ J4 viga L / VL 1:10
    x0, y0 = cell(sh, 3, 0, "J4", "Viga L de borde / VL", "Corte transversal 1:10 · unión húmeda rígida")
    v = sh.view(x0 + 14, y0 + 106, 10)
    v.poly([(0, 480), (0, 570), (120, 510), (140, 510), (140, 480)], mat="HA", sw=0.3)
    v.poly([(400, 480), (400, 570), (280, 510), (260, 510), (260, 480)], mat="HA", sw=0.3)
    v.poly([(0, 570), (0, 700), (400, 700), (400, 570), (280, 510), (120, 510)], mat="HA", sw=0.3)
    v.rect(140, 480, 260, 510, mat="HA", stroke=None)
    breakline(sh, v.P(-30, 480), v.P(430, 480))
    v.rect(0, 700, 400, 708, mat="mort", sw=0.1)
    v.poly(geo.perfil_L(0, 708), mat="HA", sw=0.3)
    for x in (80, 270):
        v.rect(x - 20, 708, x + 20, 840, mat="grout", sw=0.08)
        v.line(x, 580, x, 830, stroke=REB, sw=0.4)
    v.pline([(70, 820), (70, 990), (390, 990)], stroke=REB, sw=0.3)
    for x in (45, 200, 355): v.dot(x, 655, 0.35)
    for lab, tgt, at in (("1", (300, 620), (x0 + 60, y0 + 50)), ("2", (300, 704), (x0 + 60, y0 + 38)), ("3", (300, 780), (x0 + 60, y0 + 28)),
                         ("4", (270, 760), (x0 + 60, y0 + 18)), ("5", (230, 990), (x0 + 50, y0 + 9.5))):
        sh.callout(v.P(*tgt), at, lab, r=1.4)
    v.dim((0, 708), (0, 968), 2.0, "0,26", size=1.3)
    legend(sh, x0, y0 + 62, ["Ala superior de la VL doble T", "Cama de mortero 1:3, e = 8 mm (nivela y reparte)",
                             "Viga L de borde premoldeada", "2 barras Ø12 c/ 60 cm salientes de la VL, en vainas Ø40 de la L c/ grout",
                             "Estribos salientes 2Ø10: anclan la capa de compresión"])

    # ------------------------------------------------------------ J5 nervio TT / talón VP 1:15
    x0, y0 = cell(sh, 0, 1, "J5", "Nervio TT / talón de VP", "Corte por eje del nervio 1:20 · apoyo simple seco")
    v = sh.view(x0 + 30, y0 + 52, 20)
    v.poly([(0, 0), (480, 0), (480, 750), (150, 750), (150, 150), (0, 150)], mat="HA", sw=0.3)
    breakline(sh, v.P(480, -20), v.P(480, 770))
    v.poly([(-460, 750), (140, 750), (140, 160), (-10, 160), (-10, 100), (-460, 100)], mat="HA", sw=0.3)
    v.line(-460, 700, 140, 700, sw=0.1)
    breakline(sh, v.P(-460, 80), v.P(-460, 770))
    v.rect(10, 150, 140, 160, mat="neo", stroke=None)
    v.rect(-460, 750, 480, 800, mat="HAis", sw=0.25)
    v.line(-450, 785, 470, 785, stroke=REB, sw=0.25)
    v.line(-450, 140, 120, 140, stroke=REB, sw=0.15); v.pline([(100, 140), (100, 690), (-200, 690)], stroke=REB, sw=0.15)
    for lab, tgt, at in (("1", (-250, 400), (x0 + 5, y0 + 22)), ("2", (60, 130), (x0 + 5, y0 + 50)), ("3", (75, 155), (x0 + 64, y0 + 52)),
                         ("4", (300, 400), (x0 + 64, y0 + 30)), ("5", (0, 785), (x0 + 30, y0 + 10))):
        sh.callout(v.P(*tgt), at, lab, r=1.4)
    v.dim((0, 0), (150, 0), -1.8, "0,15", size=1.2)
    legend(sh, x0, y0 + 62, ["Panel TT h 0,65: nervio con rebaje (dap) de 5 cm en el extremo", "Armadura de suspensión del dap (horquilla)",
                             "Neopreno 10 mm s/ talón (apoyo ≥ 13 cm)", "Viga VP T invertida", "Barras de negativo Ø12 en la capa (continuidad)"])

    # ------------------------------------------------------------ J6 ala TT / talón viga L 1:15
    x0, y0 = cell(sh, 1, 1, "J6", "Ala TT / talón viga L", "Corte transversal 1:15 · apoyo seco + grout")
    v = sh.view(x0 + 5, y0 + 22, 15)
    v.poly([(0, -218), (400, -218), (400, -348), (280, -408), (260, -408), (260, -440), (140, -440), (140, -408), (120, -408), (0, -348)], mat="HA", sw=0.3)
    breakline(sh, v.P(110, -440), v.P(290, -440))
    v.rect(0, -218, 400, -210, mat="mort", sw=0.1)
    v.poly([(0, -210), (400, -210), (400, -60), (150, -60), (150, 50), (0, 50)], mat="HA", sw=0.3)
    v.rect(170, -50, 950, 0, mat="HA", sw=0.3)
    v.poly([(680, -50), (860, -50), (842, -440), (698, -440)], mat="HA", sw=0.3)
    breakline(sh, v.P(950, -70), v.P(950, 70)); breakline(sh, v.P(670, -440), v.P(870, -440))
    v.rect(180, -60, 390, -50, mat="neo", stroke=None)
    v.rect(150, -60, 170, 0, mat="grout", sw=0.05)
    v.rect(150, 0, 950, 50, mat="HAis", sw=0.25)
    v.line(160, 25, 940, 25, stroke=REB, sw=0.2)
    v.pline([(70, -150), (70, 25), (140, 25)], stroke=REB, sw=0.25)
    v.poly([(0, -316), (42, -316), (42, -264), (0, -264), (0, -272), (34, -272), (34, -308), (0, -308)], mat="acero", sw=0.04)
    for lab, tgt, at in (("1", (700, -25), (x0 + 60, y0 + 12)), ("2", (300, -55), (x0 + 60, y0 + 28)), ("3", (160, -30), (x0 + 30, y0 + 46)),
                         ("4", (250, -130), (x0 + 22, y0 + 50)), ("5", (500, 25), (x0 + 45, y0 + 9.5)), ("6", (20, -290), (x0 + 3, y0 + 46))):
        sh.callout(v.P(*tgt), at, lab, r=1.4)
    v.dim((170, -60), (400, -60), -9.0, "0,23 apoyo", size=1.2)
    legend(sh, x0, y0 + 59, ["Ala del TT (borde longitudinal del panel)", "Neopreno 10 mm continuo s/ talón de la viga L",
                             "Junta 2 cm ala / alma L rellena c/ grout", "Viga L de borde (talón 40 x 15)",
                             "Capa de compresión c/ malla Ø6 c/15", "Riel embutido en la VL (fijación del muro cortina)"])

    # ------------------------------------------------------------ J7 TT / TT 1:5
    x0, y0 = cell(sh, 2, 1, "J7", "Panel TT / panel TT", "Corte transversal 1:5 · junta longitudinal")
    v = sh.view(x0 + 34, y0 + 36, 5)
    for s in (-1, 1):
        v.poly([(s * 160, 0), (s * 10, 0), (s * 10, 12), (s * 20, 20), (s * 20, 32), (s * 10, 40), (s * 10, 50), (s * 160, 50)], mat="HA", sw=0.3)
        breakline(sh, v.P(s * 160, -6), v.P(s * 160, 56))
        v.rect(s * 15 if s > 0 else -95, 42, s * 95 if s > 0 else -15, 50, mat="acero", sw=0.04)
        v.line(s * 60, 42, s * 60, 5, sw=0.3)
    v.poly([(-10, 0), (10, 0), (10, 12), (20, 20), (20, 32), (10, 40), (10, 50), (-10, 50), (-10, 40), (-20, 32), (-20, 20), (-10, 12)], mat="grout", sw=0.1)
    v.rect(-40, 50, 40, 58, mat="acero", sw=0.05)
    v.rect(-160, 50, 160, 100, mat="HAis", sw=0.25)
    v.line(-155, 78, 155, 78, stroke=REB, sw=0.2)
    v.rect(-12, -6, 12, 0, fill="#999", sw=0.05)
    for lab, tgt, at in (("1", (-100, 25), (x0 + 6, y0 + 50)), ("2", (0, 26), (x0 + 34, y0 + 52)), ("3", (60, 46), (x0 + 63, y0 + 18)),
                         ("4", (0, 54), (x0 + 50, y0 + 11)), ("5", (100, 85), (x0 + 63, y0 + 30)), ("6", (0, -3), (x0 + 63, y0 + 48))):
        sh.callout(v.P(*tgt), at, lab, r=1.4)
    legend(sh, x0, y0 + 59, ["Ala de TT (5 cm) con borde tipo llave de corte", "Llave de corte rellena c/ grout (transmite corte vertical)",
                             "Chapa 100x8 embutida c/ anclajes, c/ 1,50 m", "Cubrejunta 80x8 soldado en obra (cordón 5 mm)",
                             "Capa de compresión e = 5 cm c/ malla", "Fondo de junta / cordón (contiene el grout)"])

    # ------------------------------------------------------------ J8 capa / VP 1:25
    x0, y0 = cell(sh, 3, 1, "J8", "Capa de compresión / VP y TT", "Corte transversal 1:25 · unión húmeda de continuidad")
    v = sh.view(x0 + 22, y0 + 45, 25)
    v.poly(geo.perfil_VP(), mat="HA", sw=0.3)
    for sd, xe, xf in ((-1, 140, -420), (1, 560, 1120)):
        v.poly([(xf, 750), (xe, 750), (xe, 160), (xe + sd * 150, 160), (xe + sd * 150, 100), (xf, 100)], fill=VISTA, sw=0.2)
        breakline(sh, v.P(xf, 80), v.P(xf, 820))
        v.rect(min(xe, xe + sd * 130), 150, max(xe, xe + sd * 130), 160, mat="neo", stroke=None)
    v.rect(-420, 750, 1120, 800, mat="HAis", sw=0.25)
    v.line(-410, 790, 1110, 790, stroke=REB, sw=0.3)
    v.line(-410, 775, 1110, 775, stroke=REB, sw=0.12, dash="1 0.3")
    for x in (230, 470):
        v.pline([(x, 600), (x, 780), (x + 40, 780)], stroke=REB, sw=0.2)
    v.rect(140, 750, 150, 800, mat="grout", stroke=None); v.rect(550, 750, 560, 800, mat="grout", stroke=None)
    for lab, tgt, at in (("1", (700, 790), (x0 + 60, y0 + 12)), ("2", (230, 700), (x0 + 6, y0 + 12)), ("3", (900, 775), (x0 + 60, y0 + 22)),
                         ("4", (350, 400), (x0 + 60, y0 + 46)), ("5", (145, 770), (x0 + 30, y0 + 11.5))):
        sh.callout(v.P(*tgt), at, lab, r=1.4)
    legend(sh, x0, y0 + 59, ["Barras de negativo Ø12 c/ 20, L = 2,50 m s/ la VP", "Estribos salientes de la VP (conectores de corte)",
                             "Malla Ø6 c/15 continua (diafragma rígido horizontal)", "Viga VP + extremos de TT apoyados en los talones",
                             "Juntas TT / VP llenas c/ grout antes de hormigonar la capa"])
    return sh
