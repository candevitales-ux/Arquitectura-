# -*- coding: utf-8 -*-
"""Detalles de las uniones de la estructura J1…J8 (4 por lámina)."""
from lib import Sheet, page, heading, breakline, wrap, fitview, autocallouts, REB, TB, TS, TD, TT
import geo

VISTA = "#eceeef"
JY = "#fff1a8"
CW, CH = 94.0, 118.0


def cell(sh, i, j, lab, title, sub):
    x0, y0 = 10 + i * (CW + 2), 28 + j * (CH + 2)
    sh.rect(x0, y0, x0 + CW, y0 + CH, stroke="#888", sw=0.15, layer="MARCO")
    sh.ball(x0 + 5, y0 + 5.5, lab, r=3.3, fill=JY)
    sh.text(x0 + 10.5, y0 + 6.2, title, 2.8, bold=True)
    sh.text(x0 + 3, y0 + 12.5, sub, TS, color="#333")
    return x0, y0, (x0 + 1, y0 + 15, x0 + CW - 1, y0 + 80)


def legend(sh, x0, y0, items):
    y = y0 + 85
    for k, t in enumerate(items):
        sh.ball(x0 + 3.6, y - 0.8, str(k + 1), r=1.9)
        for ln in wrap(t, CW - 9, TS):
            sh.text(x0 + 7, y, ln, TS); y += TS * 1.2
        y += 0.9


def refs(sh, v, box, pts):
    autocallouts(sh, [(str(k + 1), v.P(*p)) for k, p in enumerate(pts)], box)


def j1(sh, i, j):
    x0, y0, box = cell(sh, i, j, "J1", "Columna / cáliz", "Corte 1:20 · unión húmeda, empotramiento")
    v = fitview(sh, box, (-700, 700, -1420, -330), 20)
    v.rect(-700, -1420, 700, -330, mat="tierra", stroke=None)
    v.poly([(-525, -1420), (525, -1420), (525, -510), (275, -510), (275, -1350), (-275, -1350), (-275, -510), (-525, -510)], mat="HAis", sw=0.35)
    v.rect(-275, -1350, 275, -510, mat="grout", sw=0.12)
    v.rect(-200, -1300, 200, -330, mat="HA", sw=0.35)
    breakline(sh, v.P(-260, -330), v.P(260, -330))
    for s in (-1, 1):
        v.poly([(s * 205, -510), (s * 270, -510), (s * 215, -640)], fill="#6b4f2a", stroke="#000", sw=0.08)
        v.pline([(s * (275 + (10 if k % 2 else 0)), -1330 + k * 55) for k in range(15)], sw=0.12)
        v.pline([(s * (200 - (8 if k % 2 else 0)), -1290 + k * 55) for k in range(14)], sw=0.12)
        v.pline([(s * 420, -1400), (s * 420, -560)], stroke=REB, sw=0.18)
    v.dim((-600, -1300), (-600, -510), 0, "0,79")
    refs(sh, v, box, [(0, -800), (240, -1000), (400, -900), (240, -560), (-275, -1100)])
    legend(sh, x0, y0, ["Columna premoldeada 40x40, superficie rugosa en el tramo empotrado", "Grout sin retracción ≥ 30 MPa en la holgura de 7,5 cm",
                        "Cuello (cáliz) H°A° in situ, pared 0,25 m", "Cuña de madera dura (aplomado ± 5 mm), se retira a las 24 h",
                        "Llaves de corte en el alvéolo: transmiten el momento"])


def j2(sh, i, j):
    x0, y0, box = cell(sh, i, j, "J2", "Viga VL / ménsula de columna", "Corte longitudinal 1:20 · unión seca articulada")
    v = fitview(sh, (box[0] + 6, box[1], box[2] - 6, box[3]), (-300, 1180, -500, 720), 20)
    v.rect(-300, -500, 0, 720, fill=VISTA, sw=0.25)
    breakline(sh, v.P(-340, 720), v.P(40, 720)); breakline(sh, v.P(-340, -500), v.P(40, -500))
    v.poly([(0, -10), (330, -10), (330, -170), (0, -480)], mat="HA", sw=0.35)
    v.rect(10, 0, 1180, 700, mat="HA", sw=0.35)
    v.line(10, 150, 1180, 150, sw=0.12); v.line(10, 550, 1180, 550, sw=0.12)
    breakline(sh, v.P(1180, -40), v.P(1180, 740))
    v.rect(20, -10, 320, 0, mat="neo", stroke=None)
    v.rect(143, 0, 187, 190, mat="grout", sw=0.1)
    v.rect(155, -270, 175, 175, mat="acero", sw=0.05)
    v.line(10, 45, 1180, 45, stroke=REB, sw=0.15, dash="1 0.4")
    refs(sh, v, box, [(700, 350), (240, -5), (165, 120), (165, -150), (5, 400)])
    legend(sh, x0, y0, ["VL doble T 40x70 pretensada (apoyo ≥ 15 cm)", "Neopreno zunchado 10 mm (giro y dilatación libres)",
                        "Vaina Ø40 en la viga rellena c/ grout (2 por apoyo)", "Perno Ø20 anclado en la ménsula: antivuelco",
                        "Junta 1 cm viga / columna (sin contacto)"])


def j3(sh, i, j):
    x0, y0, box = cell(sh, i, j, "J3", "Viga VP / ménsula de columna", "Corte longitudinal 1:20 · unión seca articulada")
    v = fitview(sh, (box[0] + 6, box[1], box[2] - 6, box[3]), (-300, 1180, -500, 770), 20)
    v.rect(-300, -500, 0, 770, fill=VISTA, sw=0.25)
    breakline(sh, v.P(-340, 770), v.P(40, 770)); breakline(sh, v.P(-340, -500), v.P(40, -500))
    v.poly([(0, -10), (350, -10), (350, -170), (0, -480)], mat="HA", sw=0.35)
    v.rect(10, 0, 1180, 750, mat="HA", sw=0.35)
    v.line(10, 150, 1180, 150, sw=0.12)
    breakline(sh, v.P(1180, -40), v.P(1180, 790))
    v.rect(20, -10, 340, 0, mat="neo", stroke=None)
    v.rect(153, 0, 197, 200, mat="grout", sw=0.1)
    v.rect(165, -270, 185, 185, mat="acero", sw=0.05)
    for x in range(260, 1180, 120): v.dot(x, 45, 0.4, "#000")
    refs(sh, v, box, [(750, 450), (270, -5), (175, 120), (300, -120)])
    legend(sh, x0, y0, ["VP T invertida h 0,75 (12,6 t): apoyo ≥ 20 cm", "Neopreno 10 mm 300 x 320",
                        "Perno Ø20 en vaina Ø40 c/ grout (1 por apoyo)", "Ménsula corta c/ diagonal: tensor sup. Ø16 + estribos",
                        "Orden: VP antes que los TT; las vainas se rellenan al final del nivel"])


def j4(sh, i, j):
    x0, y0, box = cell(sh, i, j, "J4", "Viga L de borde / VL", "Corte transversal 1:10 · unión húmeda rígida")
    v = fitview(sh, box, (-30, 430, 480, 1000), 10)
    v.poly([(0, 700), (400, 700), (400, 570), (280, 510), (260, 510), (260, 480), (140, 480), (140, 510), (120, 510), (0, 570)], mat="HA", sw=0.35)
    breakline(sh, v.P(110, 480), v.P(290, 480))
    v.rect(0, 700, 400, 708, mat="mort", sw=0.1)
    v.poly(geo.perfil_L(0, 708), mat="HA", sw=0.35)
    for x in (80, 270):
        v.rect(x - 20, 708, x + 20, 840, mat="grout", sw=0.08)
        v.line(x, 580, x, 830, stroke=REB, sw=0.5)
    v.pline([(70, 820), (70, 990), (390, 990)], stroke=REB, sw=0.35)
    for x in (45, 200, 355): v.dot(x, 655, 0.5)
    v.dim((400, 708), (400, 968), -3.0, "0,26")
    refs(sh, v, box, [(300, 620), (300, 704), (300, 790), (270, 760), (230, 990)])
    legend(sh, x0, y0, ["Ala superior de la VL doble T", "Cama de mortero 1:3, e = 8 mm (nivela y reparte)", "Viga L de borde premoldeada",
                        "2 barras Ø12 c/ 60 cm salientes de la VL, en vainas Ø40 de la L c/ grout", "Estribos salientes 2Ø10: anclan la capa"])


def j5(sh, i, j):
    x0, y0, box = cell(sh, i, j, "J5", "Nervio TT / talón de VP", "Corte por eje del nervio 1:15 · apoyo simple seco")
    v = fitview(sh, box, (-460, 480, 0, 800), 15)
    v.poly([(0, 0), (480, 0), (480, 750), (150, 750), (150, 150), (0, 150)], mat="HA", sw=0.35)
    breakline(sh, v.P(480, -20), v.P(480, 770))
    v.poly([(-460, 750), (140, 750), (140, 160), (-10, 160), (-10, 100), (-460, 100)], mat="HA", sw=0.35)
    v.line(-460, 700, 140, 700, sw=0.12)
    breakline(sh, v.P(-460, 80), v.P(-460, 770))
    v.rect(10, 150, 140, 160, mat="neo", stroke=None)
    v.rect(-460, 750, 480, 800, mat="HAis", sw=0.25)
    v.line(-450, 785, 470, 785, stroke=REB, sw=0.3)
    v.line(-450, 135, 120, 135, stroke=REB, sw=0.2); v.pline([(100, 135), (100, 690), (-200, 690)], stroke=REB, sw=0.2)
    v.dim((0, 0), (150, 0), -3.0, "0,15")
    refs(sh, v, box, [(-250, 400), (60, 135), (75, 155), (300, 400), (0, 785)])
    legend(sh, x0, y0, ["Panel TT h 0,65: nervio con rebaje (dap) de 5 cm en el extremo", "Armadura de suspensión del dap (horquilla)",
                        "Neopreno 10 mm s/ talón (apoyo ≥ 13 cm)", "Viga VP T invertida", "Barras de negativo Ø12 en la capa (continuidad)"])


def j6(sh, i, j):
    x0, y0, box = cell(sh, i, j, "J6", "Ala TT / talón viga L", "Corte transversal 1:15 · apoyo seco + grout")
    v = fitview(sh, (box[0] + 5, box[1], box[2] - 5, box[3]), (-30, 950, -440, 60), 15)
    v.poly([(0, -218), (400, -218), (400, -348), (280, -408), (260, -408), (260, -440), (140, -440), (140, -408), (120, -408), (0, -348)], mat="HA", sw=0.35)
    breakline(sh, v.P(110, -440), v.P(290, -440))
    v.rect(0, -218, 400, -210, mat="mort", sw=0.1)
    v.poly([(0, -210), (400, -210), (400, -60), (150, -60), (150, 50), (0, 50)], mat="HA", sw=0.35)
    v.rect(170, -50, 950, 0, mat="HA", sw=0.35)
    v.poly([(680, -50), (860, -50), (842, -440), (698, -440)], mat="HA", sw=0.35)
    breakline(sh, v.P(950, -70), v.P(950, 70)); breakline(sh, v.P(670, -440), v.P(870, -440))
    v.rect(180, -60, 390, -50, mat="neo", stroke=None)
    v.rect(150, -60, 170, 0, mat="grout", sw=0.05)
    v.rect(150, 0, 950, 50, mat="HAis", sw=0.25)
    v.line(160, 25, 940, 25, stroke=REB, sw=0.25)
    v.pline([(70, -150), (70, 25), (140, 25)], stroke=REB, sw=0.3)
    v.poly([(0, -316), (42, -316), (42, -264), (0, -264), (0, -272), (34, -272), (34, -308), (0, -308)], mat="acero", sw=0.04)
    refs(sh, v, box, [(700, -25), (300, -55), (160, -30), (250, -130), (550, 25), (20, -290)])
    legend(sh, x0, y0, ["Ala del TT (borde longitudinal del panel)", "Neopreno 10 mm continuo s/ talón (apoyo 23 cm)",
                        "Junta 2 cm ala / alma L rellena c/ grout", "Viga L de borde (talón 40 x 15)",
                        "Capa de compresión c/ malla Ø6 c/15", "Riel embutido en la VL (fijación del muro cortina)"])


def j7(sh, i, j):
    x0, y0, box = cell(sh, i, j, "J7", "Panel TT / panel TT", "Corte transversal 1:5 · junta longitudinal")
    v = fitview(sh, (box[0] + 6, box[1] + 10, box[2] - 6, box[3] - 10), (-160, 160, -6, 100), 5)
    for s in (-1, 1):
        v.poly([(s * 160, 0), (s * 10, 0), (s * 10, 12), (s * 20, 20), (s * 20, 32), (s * 10, 40), (s * 10, 50), (s * 160, 50)], mat="HA", sw=0.35)
        breakline(sh, v.P(s * 160, -6), v.P(s * 160, 56))
        v.rect(15 if s > 0 else -95, 42, 95 if s > 0 else -15, 50, mat="acero", sw=0.04)
        v.line(s * 60, 42, s * 60, 5, sw=0.4)
    v.poly([(-10, 0), (10, 0), (10, 12), (20, 20), (20, 32), (10, 40), (10, 50), (-10, 50), (-10, 40), (-20, 32), (-20, 20), (-10, 12)], mat="grout", sw=0.1)
    v.rect(-40, 50, 40, 58, mat="acero", sw=0.05)
    v.rect(-160, 50, 160, 100, mat="HAis", sw=0.25)
    v.line(-155, 78, 155, 78, stroke=REB, sw=0.25)
    v.rect(-12, -6, 12, 0, fill="#999", sw=0.05)
    refs(sh, v, box, [(-100, 25), (0, 26), (60, 46), (0, 54), (100, 85), (0, -3)])
    legend(sh, x0, y0, ["Ala de TT (5 cm) con borde tipo llave de corte", "Llave de corte rellena c/ grout (transmite corte vertical)",
                        "Chapa 100x8 embutida c/ anclajes, c/ 1,50 m", "Cubrejunta 80x8 soldado en obra",
                        "Capa de compresión e = 5 cm c/ malla", "Fondo de junta (contiene el grout)"])


def j8(sh, i, j):
    x0, y0, box = cell(sh, i, j, "J8", "Capa de compresión / VP y TT", "Corte transversal 1:20 · unión húmeda de continuidad")
    v = fitview(sh, (box[0] + 6, box[1], box[2] - 6, box[3]), (-420, 1120, 0, 800), 20)
    v.poly(geo.perfil_VP(), mat="HA", sw=0.35)
    for sd, xe, xf in ((-1, 140, -420), (1, 560, 1120)):
        v.poly([(xf, 750), (xe, 750), (xe, 160), (xe + sd * 150, 160), (xe + sd * 150, 100), (xf, 100)], fill=VISTA, sw=0.25)
        breakline(sh, v.P(xf, 80), v.P(xf, 820))
        v.rect(min(xe, xe + sd * 130), 150, max(xe, xe + sd * 130), 160, mat="neo", stroke=None)
    v.rect(-420, 750, 1120, 800, mat="HAis", sw=0.25)
    v.line(-410, 790, 1110, 790, stroke=REB, sw=0.35)
    v.line(-410, 775, 1110, 775, stroke=REB, sw=0.15, dash="1 0.3")
    for x in (230, 470): v.pline([(x, 600), (x, 780), (x + 40, 780)], stroke=REB, sw=0.25)
    v.rect(140, 750, 150, 800, mat="grout", stroke=None); v.rect(550, 750, 560, 800, mat="grout", stroke=None)
    refs(sh, v, box, [(700, 790), (230, 700), (900, 775), (350, 400), (145, 770)])
    legend(sh, x0, y0, ["Barras de negativo Ø12 c/ 20, L = 2,50 m s/ la VP", "Estribos salientes de la VP (conectores de corte)",
                        "Malla Ø6 c/15 continua (diafragma rígido horizontal)", "Viga VP + extremos de TT apoyados en los talones",
                        "Juntas TT / VP llenas c/ grout antes de la capa"])


@page("Juntas · detalles J1 a J4")
def hoja1(num, total):
    sh = Sheet(num, total, "Juntas y uniones · detalles J1 a J4", escalas="J1, J2 y J3 1:20 · J4 1:10", fname="Juntas_3_Detalles_J1_J4")
    heading(sh, "2º JUNTAS Y UNIONES · DETALLES J1 A J4", "Uniones de la estructura premoldeada (numeración de la lámina 09)")
    j1(sh, 0, 0); j2(sh, 1, 0); j3(sh, 0, 1); j4(sh, 1, 1)
    return sh


@page("Juntas · detalles J5 a J8")
def hoja2(num, total):
    sh = Sheet(num, total, "Juntas y uniones · detalles J5 a J8", escalas="J5 y J6 1:15 · J7 1:5 · J8 1:20", fname="Juntas_4_Detalles_J5_J8")
    heading(sh, "2º JUNTAS Y UNIONES · DETALLES J5 A J8", "Uniones de los entrepisos: apoyo de los TT, junta entre paneles y capa de compresión")
    j5(sh, 0, 0); j6(sh, 1, 0); j7(sh, 0, 1); j8(sh, 1, 1)
    return sh


PAGES = [hoja1, hoja2]
