# -*- coding: utf-8 -*-
"""Detalles de juntas y uniones de cerramientos J9…J15 + dimensionado de juntas (4 por lámina).
Coordenadas como el TP: x+ hacia el interior; muro cortina x -30..182; panel sándwich x 30..230; VL x 250..650."""
from lib import Sheet, page, heading, breakline, wrap, fitview, REB, TB, TS, TD, TT
from s06_juntas_estructura import cell, legend, refs, VISTA, CW, CH
import geo

GLASS, ALU = "#bfe3f0", "#9aa3ab"


def j9(sh, i, j):
    x0, y0, box = cell(sh, i, j, "J9", "Piso s/ terreno / columna", "Corte 1:10 · junta de movimiento")
    v = fitview(sh, (box[0] + 6, box[1], box[2] - 6, box[3]), (-60, 560, -420, 60), 10)
    v.rect(-50, -420, 560, -327, mat="tierra", stroke=None)
    v.rect(-50, -420, 200, 60, mat="HA", sw=0.35)
    breakline(sh, v.P(-50, 70), v.P(200, 70))
    v.rect(220, -327, 560, -177, mat="tosca", sw=0.12)
    v.rect(220, -177, 560, -175, fill="#000", stroke=None)
    v.rect(220, -175, 560, -55, mat="H", sw=0.15)
    v.line(240, -120, 550, -120, stroke=REB, sw=0.2, dash="1 0.3")
    v.rect(220, -55, 560, -35, fill="#c9dbe6", sw=0.1)
    v.rect(220, -35, 560, -10, mat="mort", sw=0.1)
    v.rect(225, -10, 560, 0, fill="#cdbb9c", sw=0.12)
    v.rect(200, -327, 220, -12, mat="epsv", sw=0.08)
    v.rect(200, -12, 225, 0, mat="neo", stroke=None)
    breakline(sh, v.P(560, -340), v.P(560, 10))
    refs(sh, v, box, [(80, -150), (210, -250), (212, -6), (400, -110), (400, -250), (400, -5)])
    legend(sh, x0, y0, ["Columna premoldeada 40x40", "EPS 20 mm en todo el espesor del piso (independiza)", "Sellador poliuretánico s/ fondo de junta",
                        "Contrapiso armado e = 12 cm + carpetas", "Tosca compactada 15 cm + film 200 µ", "Solado cerámico (junta perimetral libre)"])


def j10(sh, i, j):
    x0, y0, box = cell(sh, i, j, "J10", "Muro cortina / VL y viga L", "Corte vertical 1:10 · unión seca regulable")
    v = fitview(sh, (box[0] + 6, box[1], box[2] - 6, box[3]), (-30, 580, -370, 100), 10)
    v.poly([(250, -210), (580, -210), (580, -340), (250, -340)], mat="HA", sw=0.35)
    v.poly([(250, -210), (580, -210), (580, -60), (400, -60), (400, 50), (250, 50)], mat="HA", sw=0.35)
    v.rect(400, 0, 580, 50, mat="HAis", sw=0.2)
    v.rect(250, -370, 580, -340, mat="HA", stroke=None); breakline(sh, v.P(240, -370), v.P(590, -370))
    breakline(sh, v.P(580, -380), v.P(580, 60))
    v.poly([(250, -316), (292, -316), (292, -264), (250, -264), (250, -272), (284, -272), (284, -308), (250, -308)], mat="acero", sw=0.04)
    v.rect(32, -370, 182, 100, fill="#e3e7ea", sw=0.15); v.line(150, -370, 150, 100, sw=0.08)
    v.rect(-30, -370, -14, 100, fill="#e9ecee", sw=0.12)
    v.rect(0, -370, 6, 100, fill="#6f8796", sw=0.12)
    v.rect(40, -370, 87, 100, mat="lanav", sw=0.08); v.rect(87, -370, 93, 100, fill="#888", sw=0.05)
    v.poly([(238, -340), (246, -340), (246, -248), (182, -248), (182, -240), (238, -240)], mat="acero", sw=0.05)
    v.rect(150, -330, 182, -235, fill="#555", sw=0.08)
    v.line(246, -290, 290, -290, sw=0.5); v.rect(262, -298, 284, -282, fill="#777", sw=0.05)
    v.circle(166, -285, 8, fill="#fff", sw=0.2)
    v.rect(246, -340, 250, -240, mat="neo", stroke=None)
    v.rect(93, -50, 250, 43, mat="lana", sw=0.12)
    v.pline([(250, -55), (120, -55), (120, -40)], sw=0.4)
    for z in (-370, 100): breakline(sh, v.P(-40, z), v.P(200, z))
    refs(sh, v, box, [(242, -300), (270, -290), (166, -285), (170, 0), (64, -160), (450, -100), (3, -340)])
    legend(sh, x0, y0, ["Grapa: ángulo galv. 100x100x8 c/ ojal horizontal (± 25 mm)", "Bulón T M12 en riel embutido de la VL",
                        "Bulón M12 inox c/ ojal vertical en el montante", "Barrera cortafuego: lana mineral s/ ángulo",
                        "Spandrel: bandeja galv. c/ lana 50 mm", "Viga L + capa de compresión", "Vidrio templado esmaltado 6 mm"])


def j11(sh, i, j):
    x0, y0, box = cell(sh, i, j, "J11", "Montante / montante (dilatación)", "Corte por eje del montante 1:5")
    v = fitview(sh, (box[0] + 6, box[1], box[2] - 6, box[3]), (-35, 200, 4585, 4835), 5)
    za, zb = 4585, 4835
    for (z0, z1) in ((za, 4700), (4720, zb)):
        v.rect(32, z0, 36, z1, mat="alu", sw=0.1); v.rect(178, z0, 182, z1, mat="alu", sw=0.1)
        v.rect(36, z0, 178, z1, fill="#f6f7f8", stroke=None)
    v.rect(40, 4600, 44, 4820, fill="#7c858d", sw=0.08); v.rect(170, 4600, 174, 4820, fill="#7c858d", sw=0.08)
    v.rect(44, 4600, 170, 4820, fill="none", sw=0.1, dash="0.8 0.4")
    for z in (4640, 4665):
        v.line(20, z, 60, z, sw=0.4); v.line(160, z, 194, z, sw=0.4)
    v.rect(30, 4700, 36, 4720, mat="neo", stroke=None)
    v.rect(-30, za, -14, 4700, fill="#b9c0c6", sw=0.1); v.rect(-30, 4720, -14, zb, fill="#b9c0c6", sw=0.1)
    v.rect(-31, 4700, -14, 4720, mat="neo", stroke=None)
    v.rect(0, za, 6, zb, fill=GLASS, sw=0.1); v.rect(18, za, 25, zb, fill=GLASS, sw=0.1)
    for z in (za, zb): breakline(sh, v.P(-40, z), v.P(200, z))
    v.dim((182, 4700), (182, 4720), -4.0, "20 mm")
    refs(sh, v, box, [(182, 4650), (172, 4790), (40, 4652), (-22, 4710), (100, 4780)])
    legend(sh, x0, y0, ["Montante inferior (punto fijo en la grapa)", "Manguito de aluminio interior 30 cm (encastra en ambos tramos)",
                        "Tornillos inox: fijan el manguito SOLO al tramo inferior", "Sellador / burlete en la tapa",
                        "Tramo superior desliza: absorbe flechas y dilatación (± 10 mm)"])


def j12(sh, i, j):
    x0, y0, box = cell(sh, i, j, "J12", "Muro cortina / piso (arranque)", "Corte vertical 1:10 · seca, deslizante")
    v = fitview(sh, (box[0] + 6, box[1], box[2] - 6, box[3]), (-300, 420, -420, 230), 10)
    v.rect(-300, -420, 420, -327, mat="tierra", stroke=None)
    v.rect(-300, -327, -60, -250, mat="tosca", sw=0.1)
    v.poly([(-300, -250), (-60, -250), (-60, -150), (-300, -157)], mat="H", sw=0.15)
    v.rect(-60, -327, 420, -15, mat="HAis", sw=0.2)
    v.rect(-60, -15, 420, 0, mat="mort", sw=0.1)
    breakline(sh, v.P(420, -430), v.P(420, 20))
    v.rect(25, 0, 190, 40, mat="alu", sw=0.12); v.rect(32, 6, 182, 40, fill="#fff", sw=0.05)
    v.rect(32, 10, 182, 280, fill="#e3e7ea", sw=0.15)
    v.rect(0, 60, 6, 280, fill=GLASS, sw=0.1); v.rect(18, 60, 25, 280, fill=GLASS, sw=0.1)
    v.rect(2, 50, 24, 60, fill="#333", stroke=None)
    v.rect(-30, 30, -14, 280, fill="#b9c0c6", sw=0.1)
    breakline(sh, v.P(-40, 230), v.P(200, 230))
    v.pline([(-80, -140), (-62, -140), (-62, 0), (25, 0), (25, 30)], sw=0.4)
    v.rect(14, 0, 25, 30, mat="neo", stroke=None)
    v.line(107, -10, 107, -110, sw=0.5)
    v.rect(-60, -150, -50, -15, mat="epsv", sw=0.05)
    refs(sh, v, box, [(100, 20), (20, 15), (-62, -60), (107, -80), (13, 55), (-200, -200)])
    legend(sh, x0, y0, ["Perfil guía de arranque U (el montante desliza dentro)", "Sellador siliconado neutro s/ fondo de junta",
                        "Babeta chapa galv. + aislación hidrófuga (gotero)", "Broca c/ prisionero Ø9,5 x 80 + tuerca",
                        "Calzo de apoyo del DVH (EPDM)", "Vereda H° peinado s/ tosca + junta EPS"])


def j13(sh, i, j):
    x0, y0, box = cell(sh, i, j, "J13", "Panel sándwich / VL (fija panel)", "Corte vertical 1:10 · seca, deslizante")
    v = fitview(sh, (box[0] + 6, box[1], box[2] - 6, box[3]), (20, 660, 3930, 4380), 10)
    za, zb = 3930, 4380
    v.rect(30, za, 90, zb, mat="HA", sw=0.25); v.rect(90, za, 150, zb, mat="epsv", sw=0.1); v.rect(150, za, 230, zb, mat="HA", sw=0.25)
    v.rect(90, 4105, 150, 4175, mat="HA", sw=0.1)
    v.poly([(250, 4205), (620, 4205), (620, 4075), (500, 4015), (500, za), (400, za), (400, 4015), (250, 4075)], mat="HA", sw=0.35)
    v.poly([(250, 4205), (620, 4205), (620, 4355), (400, 4355), (400, zb), (250, zb)], mat="HA", sw=0.35)
    for z in (za, zb): breakline(sh, v.P(20, z), v.P(240, z))
    breakline(sh, v.P(620, 4060), v.P(620, 4370))
    v.rect(30, 4110, 230, 4170, fill="#fff", sw=0.1)
    v.rect(30, 4090, 60, 4190, mat="mort", sw=0.1)
    v.rect(250, 4120, 620, 4160, mat="grout", sw=0.08)
    v.line(55, 4140, 650, 4140, sw=0.9)
    v.rect(620, 4105, 632, 4175, mat="acero", sw=0.05); v.rect(632, 4122, 650, 4158, mat="acero", sw=0.05)
    v.rect(60, 4122, 70, 4158, mat="acero", sw=0.05)
    v.rect(230, 4100, 250, 4180, mat="neo", stroke=None)
    v.rect(230, 4180, 250, zb, mat="lanav", sw=0.05); v.rect(230, za, 250, 4100, mat="lanav", sw=0.05)
    refs(sh, v, box, [(350, 4140), (130, 4140), (45, 4170), (240, 4140), (641, 4140), (120, 4300), (240, 4300)])
    legend(sh, x0, y0, ["Bulón pasante M20 galv. (atraviesa panel y ala de la VL en vaina c/ grout)", "Agujero ovalado VERTICAL 40x60 (dilatación)",
                        "Rehundido Ø100 x 3 cm, tapado c/ mortero", "Calce de neopreno en la junta panel / VL", "Placa 120x120 + arandela + tuerca",
                        "Panel 20 cm: H°A° 6 + EPS 6 + H°A° 8 (maciza en el anclaje)", "Junta 2 cm c/ lana mineral + sellador"])


def j14(sh, i, j):
    x0, y0, box = cell(sh, i, j, "J14", "Panel / viga portapanel", "Corte vertical 1:10 · mortero y pasador")
    v = fitview(sh, (box[0] + 6, box[1], box[2] - 6, box[3]), (-130, 450, -300, 220), 10)
    v.rect(-130, -300, 450, -150, mat="tierra", stroke=None)
    v.rect(30, -300, 230, -50, mat="HA", sw=0.35)
    breakline(sh, v.P(20, -300), v.P(240, -300))
    v.rect(30, -50, 230, -40, mat="mort", sw=0.08); v.rect(70, -50, 110, -40, mat="neo", stroke=None)
    v.rect(30, -40, 90, 220, mat="HA", sw=0.25); v.rect(90, -40, 150, 220, mat="epsv", sw=0.1); v.rect(150, -40, 230, 220, mat="HA", sw=0.25)
    breakline(sh, v.P(20, 220), v.P(240, 220))
    v.rect(175, -280, 205, 200, mat="grout", sw=0.08); v.line(190, -270, 190, 190, sw=0.6)
    v.rect(30, -50, 44, -40, mat="neo", stroke=None)
    v.rect(250, -300, 450, 0, mat="HA", sw=0.25); breakline(sh, v.P(450, -310), v.P(450, 10))
    v.rect(230, -300, 250, -50, mat="epsv", sw=0.05); v.rect(230, -50, 250, 0, mat="neo", stroke=None)
    v.line(28, -300, 28, -160, sw=0.5)
    v.rect(-130, -250, 18, -150, mat="H", sw=0.12); v.rect(18, -250, 26, -150, mat="epsv", sw=0.05)
    refs(sh, v, box, [(130, -200), (90, -45), (190, 100), (37, -45), (240, -200), (28, -250)])
    legend(sh, x0, y0, ["Viga portapanel pretensada 20x85 (E11) s/ cuellos", "Mortero de asiento 1 cm + calces de neopreno",
                        "Pasador Ø16 en vaina c/ grout (traba horizontal)", "Sellador PU s/ fondo de junta",
                        "Junta EPS viga / columna 2 cm", "Pintura asfáltica en caras enterradas"])


def j15(sh, i, j):
    x0, y0, box = cell(sh, i, j, "J15", "Panel / panel (junta vertical)", "Corte horizontal 1:5 · junta de movimiento")
    v = fitview(sh, (box[0] + 6, box[1] + 4, box[2] - 6, box[3] - 4), (-160, 160, -20, 215), 5)
    for s in (-1, 1):
        xs = lambda d: s * (10 + d)
        v.poly([(xs(0), 10), (xs(10), 0), (xs(150), 0), (xs(150), 60), (xs(0), 60)], mat="HA", sw=0.3)
        v.rect(min(xs(30), xs(150)), 60, max(xs(30), xs(150)), 120, mat="eps", sw=0.1)
        v.rect(min(xs(0), xs(30)), 60, max(xs(0), xs(30)), 120, mat="HA", stroke=None)
        v.poly([(xs(0), 120), (xs(150), 120), (xs(150), 200), (xs(10), 200), (xs(0), 190)], mat="HA", sw=0.3)
        v.line(xs(0), 60, xs(0), 120, sw=0.3)
        breakline(sh, v.P(s * 160, -5), v.P(s * 160, 205))
    v.rect(-10, 2, 10, 12, fill="#222", stroke=None); v.circle(0, 24, 11, fill="#d8d8d8", sw=0.12)
    v.rect(-10, 188, 10, 198, fill="#222", stroke=None); v.circle(0, 176, 11, fill="#d8d8d8", sw=0.12)
    v.rect(-10, 70, 10, 150, mat="lanav", sw=0.05)
    sh.text(*v.P(-100, -16), "EXTERIOR", TS, anchor="middle", bold=True); sh.text(*v.P(-100, 207), "INTERIOR", TS, anchor="middle", bold=True)
    v.dim((-10, 200), (10, 200), -3.0, "20")
    refs(sh, v, box, [(0, 7), (0, 24), (0, 110), (-80, 90), (-150, 5), (0, 193)])
    legend(sh, x0, y0, ["Sellador PU exterior 10 mm (relación ancho/prof. 2:1)", "Fondo de junta: cordón de polietileno Ø25",
                        "Lana mineral (aislación y cortafuego en la junta)", "Alma EPS 6 cm (hojas unidas c/ conectores)",
                        "Bordes biselados 10 mm (protegen la arista)", "Sellador interior (barrera de vapor / aire)"])


def dimensionado(sh, i, j):
    x0, y0 = 10 + i * (CW + 2), 28 + j * (CH + 2)
    sh.rect(x0, y0, x0 + CW, y0 + CH, stroke="#888", sw=0.15, layer="MARCO")
    sh.ball(x0 + 5, y0 + 5.5, "Δ", r=3.3, fill="#fff1a8")
    sh.text(x0 + 10.5, y0 + 6.2, "Dimensionado de juntas", 2.8, bold=True)
    y = sh.para(x0 + 3, y0 + 14, CW - 6, "Movimiento térmico de un panel de 2,50 m (ΔT = 50 °C, α = 10⁻⁵/°C):", TS, 1.25)
    sh.text(x0 + 6, y + 1, "ΔL = α · L · ΔT = 1,25 mm", TB, bold=True); y += 6
    y = sh.para(x0 + 3, y, CW - 6, "Sellador PU con capacidad de movimiento ± 25 % → ancho mín. = ΔL / 0,25 = 5 mm. Se suman tolerancias de "
                "fabricación (± 5 mm) y de montaje (± 5 mm):", TS, 1.25)
    sh.text(x0 + 6, y + 1, "ancho = 20 mm · prof. = 10 mm", TB, bold=True); y += 6
    rows = [("Junta", "Ancho", "Material"), ("Panel / panel J15", "20 mm", "PU + cordón"), ("Panel / VL J13", "20 mm", "lana + sellador"),
            ("Montante J11", "20 mm", "manguito + silic."), ("Piso / columna J9", "20 mm", "EPS + PU"), ("M. cortina / losa", "≥ 90 mm", "lana cortafuego")]
    y = sh.table(x0 + 3, y, [36, 17, 35], rows, size=TS, rowh=4.4)
    sh.para(x0 + 3, y + 5, CW - 6, "Regla: la junta va donde se interrumpe el material o cambia la rigidez, y nunca se rellena con material rígido.", TS, 1.25, ital=True)


@page("Juntas · detalles J9 a J12 (cerramientos)")
def hoja3(num, total):
    sh = Sheet(num, total, "Juntas y uniones · detalles J9 a J12", escalas="J9, J10 y J12 1:10 · J11 1:5", fname="Juntas_5_Detalles_J9_J12")
    heading(sh, "2º JUNTAS Y UNIONES · DETALLES J9 A J12", "Junta de piso y fijaciones / juntas del muro cortina")
    j9(sh, 0, 0); j10(sh, 1, 0); j11(sh, 0, 1); j12(sh, 1, 1)
    return sh


@page("Juntas · detalles J13 a J15 + dimensionado")
def hoja4(num, total):
    sh = Sheet(num, total, "Juntas y uniones · detalles J13 a J15", escalas="J13 y J14 1:10 · J15 1:5", fname="Juntas_6_Detalles_J13_J15")
    heading(sh, "2º JUNTAS Y UNIONES · DETALLES J13 A J15", "Fijación y juntas del panel sándwich + criterio de dimensionado de juntas")
    j13(sh, 0, 0); j14(sh, 1, 0); j15(sh, 0, 1); dimensionado(sh, 1, 1)
    return sh


PAGES = [hoja3, hoja4]
