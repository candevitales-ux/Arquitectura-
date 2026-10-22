# -*- coding: utf-8 -*-
"""Lámina 07 – Detalles de juntas y uniones de cerramientos J9…J15 + dimensionado de juntas.
Coordenadas como el TP: x+ hacia el interior; muro cortina x -30..182; panel sándwich x 30..230; VL x 250..650."""
from lib import Sheet, heading, breakline, wrap, REB
from s06_juntas_estructura import cell, legend, VISTA
import geo

GLASS, ALU = "#bfe3f0", "#9aa3ab"


def make(num, total):
    sh = Sheet(num, total, "Juntas y uniones 3", "Juntas y uniones de cerramientos J9 a J15 · dimensionado de juntas",
               "J9, J10, J13 y J14 1:10 · J12 1:15 · J11 y J15 1:5")
    heading(sh, "2º JUNTAS Y UNIONES DEL SISTEMA  ·  3/3", "Juntas de movimiento y fijaciones de los cerramientos (muro cortina y panel sándwich)")

    # ------------------------------------------------------------ J9 piso / columna 1:10
    x0, y0 = cell(sh, 0, 0, "J9", "Piso s/ terreno / columna", "Corte 1:10 · junta de movimiento")
    v = sh.view(x0 + 10, y0 + 15, 10)
    v.rect(-50, -420, 560, -327, mat="tierra", stroke=None)
    v.rect(-50, -420, 200, 60, mat="HA", sw=0.3)
    breakline(sh, v.P(-50, 70), v.P(200, 70)); breakline(sh, v.P(-55, -420), v.P(-55, 60))
    v.rect(220, -327, 560, -177, mat="tosca", sw=0.12)
    v.rect(220, -177, 560, -175, fill="#000", stroke=None)
    v.rect(220, -175, 560, -55, mat="H", sw=0.15)
    v.line(240, -120, 550, -120, stroke=REB, sw=0.15, dash="1 0.3")
    v.rect(220, -55, 560, -35, fill="#c9dbe6", sw=0.1)
    v.rect(220, -35, 560, -10, mat="mort", sw=0.1)
    v.rect(225, -10, 560, 0, fill="#cdbb9c", sw=0.12)
    v.rect(200, -327, 220, -12, mat="epsv", sw=0.08)
    v.rect(200, -12, 225, 0, mat="neo", stroke=None)
    for x in (560,): breakline(sh, v.P(x, -340), v.P(x, 10))
    for lab, tgt, at in (("1", (80, -150), (x0 + 4, y0 + 40)), ("2", (210, -200), (x0 + 28, y0 + 60)), ("3", (212, -6), (x0 + 30, y0 + 9.5)),
                         ("4", (400, -110), (x0 + 65, y0 + 25)), ("5", (400, -250), (x0 + 65, y0 + 50)), ("6", (400, -5), (x0 + 50, y0 + 9.5))):
        sh.callout(v.P(*tgt), at, lab, r=1.4)
    v.dim((200, 0), (220, 0), 4.0, "2 cm", size=1.2)
    legend(sh, x0, y0 + 63, ["Columna premoldeada 40x40", "EPS 20 mm en todo el espesor del piso (independiza)", "Sellador poliuretánico s/ fondo de junta",
                             "Contrapiso armado e = 12 cm + carpetas", "Tosca compactada 15 cm + film 200 µ", "Solado cerámico (junta perimetral libre)"])

    # ------------------------------------------------------------ J10 muro cortina / viga L 1:10
    x0, y0 = cell(sh, 1, 0, "J10", "Muro cortina / VL y viga L", "Corte vertical 1:10 · unión seca regulable")
    v = sh.view(x0 + 8, y0 + 19, 10)
    yt = 0
    v.poly([(250, -210), (580, -210), (580, -340), (250, -340)], mat="HA", sw=0.3)
    breakline(sh, v.P(580, -360), v.P(580, -200))
    v.poly([(250, -210), (580, -210), (580, -60), (400, -60), (400, 50), (250, 50)], mat="HA", sw=0.3)
    v.rect(400, 0, 580, 50, mat="HAis", sw=0.2)
    v.rect(250, -370, 580, -340, mat="HA", stroke=None); breakline(sh, v.P(240, -370), v.P(590, -370))
    v.poly([(250, -316), (292, -316), (292, -264), (250, -264), (250, -272), (284, -272), (284, -308), (250, -308)], mat="acero", sw=0.04)
    # montante en vista + spandrel
    v.rect(32, -370, 182, 100, fill="#e3e7ea", sw=0.15)
    v.line(150, -370, 150, 100, sw=0.08)
    v.rect(-30, -370, -14, 100, fill="#e9ecee", sw=0.12)
    v.rect(0, -370, 6, 100, fill="#6f8796", sw=0.12)
    v.rect(40, -370, 87, 100, mat="lanav", sw=0.08); v.rect(87, -370, 93, 100, fill="#888", sw=0.05)
    # grapa: ángulo galv. + placa al montante
    v.poly([(238, -340), (246, -340), (246, -248), (182, -248), (182, -240), (238, -240)], mat="acero", sw=0.05)
    v.rect(150, -330, 182, -235, fill="#555", sw=0.08)
    v.line(246, -290, 290, -290, sw=0.45); v.rect(262, -298, 284, -282, fill="#777", sw=0.05)
    v.circle(166, -285, 8, fill="#fff", sw=0.2)
    v.rect(246, -340, 250, -240, mat="neo", stroke=None)
    # barrera cortafuego
    v.rect(93, -50, 250, 43, mat="lana", sw=0.12)
    v.pline([(250, -55), (120, -55), (120, -40)], sw=0.35)
    for lab, tgt, at in (("1", (240, -260), (x0 + 6, y0 + 52)), ("2", (270, -290), (x0 + 50, y0 + 52)), ("3", (166, -285), (x0 + 22, y0 + 56)),
                         ("4", (170, 0), (x0 + 24, y0 + 9.5)), ("5", (110, -160), (x0 + 6, y0 + 38)), ("6", (450, -100), (x0 + 63, y0 + 26)),
                         ("7", (3, -350), (x0 + 6, y0 + 58))):
        sh.callout(v.P(*tgt), at, lab, r=1.4)
    legend(sh, x0, y0 + 63, ["Grapa: ángulo galv. 100x100x8 c/ ojal horizontal (± 25 mm)", "Bulón T M12 en riel embutido de la VL",
                             "Bulón M12 inox c/ ojal vertical en el montante (± 15 mm)", "Barrera cortafuego: lana mineral comprimida s/ ángulo",
                             "Spandrel: bandeja galv. c/ lana 50 mm", "Viga L + capa", "Vidrio templado esmaltado 6 mm"])

    # ------------------------------------------------------------ J11 montante / montante 1:5
    x0, y0 = cell(sh, 2, 0, "J11", "Montante / montante (dilatación)", "Corte por eje del montante 1:5 · junta de dilatación")
    v = sh.view(x0 + 18, y0 + 34 + 4710 / 5, 5)
    za, zb = 4585, 4835
    for (z0, z1) in ((za, 4700), (4720, zb)):
        v.rect(32, z0, 36, z1, mat="alu", sw=0.1); v.rect(178, z0, 182, z1, mat="alu", sw=0.1)
        v.rect(36, z0, 178, z1, fill="#f6f7f8", stroke=None)
    v.rect(40, 4600, 44, 4820, fill="#7c858d", sw=0.08); v.rect(170, 4600, 174, 4820, fill="#7c858d", sw=0.08)
    v.rect(44, 4600, 170, 4820, fill="none", sw=0.08, dash="0.8 0.4")
    for z in (4640, 4665):
        v.line(20, z, 60, z, sw=0.35); v.line(160, z, 194, z, sw=0.35)
    v.rect(30, 4700, 36, 4720, mat="neo", stroke=None)
    v.rect(-30, za, -14, 4700, fill="#b9c0c6", sw=0.1); v.rect(-30, 4720, -14, zb, fill="#b9c0c6", sw=0.1)
    v.rect(-31, 4700, -14, 4720, mat="neo", stroke=None)
    v.rect(0, za, 6, zb, fill=GLASS, sw=0.1); v.rect(18, za, 25, zb, fill=GLASS, sw=0.1)
    for z in (za, zb): breakline(sh, v.P(-40, z), v.P(200, z))
    v.dim((182, 4700), (182, 4720), -3.0, "20 mm", size=1.2)
    for lab, tgt, at in (("1", (182, 4650), (x0 + 63, y0 + 46)), ("2", (172, 4760), (x0 + 63, y0 + 16)), ("3", (40, 4652), (x0 + 6, y0 + 50)),
                         ("4", (-22, 4710), (x0 + 6, y0 + 30)), ("5", (100, 4790), (x0 + 50, y0 + 10))):
        sh.callout(v.P(*tgt), at, lab, r=1.4)
    legend(sh, x0, y0 + 63, ["Montante inferior (punto fijo en la grapa)", "Manguito de aluminio interior 30 cm (encastra en ambos tramos)",
                             "Tornillos inox: fijan el manguito SOLO al tramo inferior", "Sellador siliconado estructural / burlete en la tapa",
                             "Tramo superior desliza: absorbe flecha de vigas y dilatación (± 10 mm)"])

    # ------------------------------------------------------------ J12 arranque muro cortina 1:15
    x0, y0 = cell(sh, 3, 0, "J12", "Muro cortina / piso (arranque)", "Corte vertical 1:15 · seca, deslizante")
    v = sh.view(x0 + 26, y0 + 31, 15)
    v.rect(-380, -420, 500, -327, mat="tierra", stroke=None)
    v.rect(-380, -327, -60, -250, mat="tosca", sw=0.1)
    v.poly([(-380, -250), (-60, -250), (-60, -150), (-380, -157)], mat="H", sw=0.15)
    v.rect(-60, -327, 500, -15, mat="HAis", sw=0.2)
    v.rect(-60, -15, 500, 0, mat="mort", sw=0.1)
    breakline(sh, v.P(500, -430), v.P(500, 20))
    v.rect(25, 0, 190, 40, mat="alu", sw=0.12); v.rect(32, 6, 182, 40, fill="#fff", sw=0.05)
    v.rect(32, 10, 182, 280, fill="#e3e7ea", sw=0.15)
    v.rect(0, 60, 6, 280, fill=GLASS, sw=0.1); v.rect(18, 60, 25, 280, fill=GLASS, sw=0.1)
    v.rect(2, 50, 24, 60, fill="#333", stroke=None)
    v.rect(-30, 30, -14, 280, fill="#b9c0c6", sw=0.1)
    for z in (280,): breakline(sh, v.P(-40, z), v.P(200, z))
    v.pline([(-80, -140), (-62, -140), (-62, 0), (25, 0), (25, 30)], sw=0.35)
    v.rect(14, 0, 25, 30, mat="neo", stroke=None)
    v.line(107, -10, 107, -110, sw=0.45)
    v.rect(-60, -150, -50, -15, mat="epsv", sw=0.05)
    for lab, tgt, at in (("1", (100, 20), (x0 + 63, y0 + 30)), ("2", (20, 15), (x0 + 6, y0 + 12)), ("3", (-62, -60), (x0 + 6, y0 + 52)),
                         ("4", (107, -80), (x0 + 63, y0 + 52)), ("5", (13, 55), (x0 + 6, y0 + 24)), ("6", (-200, -200), (x0 + 6, y0 + 60))):
        sh.callout(v.P(*tgt), at, lab, r=1.4)
    legend(sh, x0, y0 + 63, ["Perfil guía de arranque U (el montante desliza dentro)", "Sellador siliconado neutro s/ fondo de junta",
                             "Babeta chapa galv. + aislación hidrófuga (gotero)", "Broca c/ prisionero Ø9,5 x 80 + tuerca",
                             "Calzo de apoyo del DVH (EPDM)", "Vereda H° peinado s/ tosca + junta EPS"])

    # ------------------------------------------------------------ J13 panel / VL 1:10
    x0, y0 = cell(sh, 0, 1, "J13", "Panel sándwich / VL (fija panel)", "Corte vertical 1:10 · seca, deslizante")
    v = sh.view(x0 + 3, y0 + 34 + 4150 / 10, 10)
    za, zb = 3930, 4380
    v.rect(30, za, 90, zb, mat="HA", sw=0.25); v.rect(90, za, 150, zb, mat="epsv", sw=0.1); v.rect(150, za, 230, zb, mat="HA", sw=0.25)
    v.rect(90, 4105, 150, 4175, mat="HA", sw=0.1)
    v.poly([(250, 4205), (620, 4205), (620, 4075), (500, 4015), (500, za), (400, za), (400, 4015), (250, 4075)], mat="HA", sw=0.3)
    v.poly([(250, 4205), (620, 4205), (620, 4355), (400, 4355), (400, zb), (250, zb)], mat="HA", sw=0.3)
    for z in (za, zb): breakline(sh, v.P(20, z), v.P(240, z))
    breakline(sh, v.P(620, 4060), v.P(620, 4370))
    v.rect(30, 4110, 230, 4170, fill="#fff", sw=0.1)
    v.rect(30, 4090, 60, 4190, mat="mort", sw=0.1)
    v.rect(250, 4120, 620, 4160, mat="grout", sw=0.08)
    v.line(55, 4140, 650, 4140, sw=0.8)
    v.rect(620, 4105, 632, 4175, mat="acero", sw=0.05); v.rect(632, 4122, 650, 4158, mat="acero", sw=0.05)
    v.rect(60, 4122, 70, 4158, mat="acero", sw=0.05)
    v.rect(230, 4100, 250, 4180, mat="neo", stroke=None)
    v.rect(230, 4180, 250, zb, mat="lanav", sw=0.05); v.rect(230, za, 250, 4100, mat="lanav", sw=0.05)
    for lab, tgt, at in (("1", (350, 4140), (x0 + 40, y0 + 10)), ("2", (130, 4140), (x0 + 22, y0 + 59)), ("3", (45, 4170), (x0 + 6, y0 + 12)),
                         ("4", (240, 4140), (x0 + 30, y0 + 59)), ("5", (641, 4140), (x0 + 63, y0 + 26)), ("6", (120, 4300), (x0 + 6, y0 + 22)),
                         ("7", (240, 4300), (x0 + 30, y0 + 10))):
        sh.callout(v.P(*tgt), at, lab, r=1.4)
    legend(sh, x0, y0 + 63, ["Bulón pasante M20 galv. (atraviesa panel y ala de la VL en vaina c/ grout)", "Agujero ovalado VERTICAL 40x60 (permite dilatación)",
                             "Rehundido Ø100 x 3 cm, tapado c/ mortero", "Calce de neopreno en la junta panel / VL", "Placa 120x120 + arandela + tuerca (lado interior)",
                             "Panel 20 cm: H°A° 6 + EPS 6 + H°A° portante 8 · zona maciza en el anclaje", "Junta 2 cm c/ lana mineral cortafuego + sellador"])

    # ------------------------------------------------------------ J14 panel / viga portapanel 1:10
    x0, y0 = cell(sh, 1, 1, "J14", "Panel / viga portapanel", "Corte vertical 1:10 · apoyo con mortero y pasador")
    v = sh.view(x0 + 18, y0 + 31, 10)
    v.rect(-130, -300, 450, -150, mat="tierra", stroke=None)
    v.rect(30, -300, 230, -50, mat="HA", sw=0.3)
    for z in (-300,): breakline(sh, v.P(20, z), v.P(240, z))
    v.rect(30, -50, 230, -40, mat="mort", sw=0.08); v.rect(70, -50, 110, -40, mat="neo", stroke=None)
    v.rect(30, -40, 90, 220, mat="HA", sw=0.25); v.rect(90, -40, 150, 220, mat="epsv", sw=0.1); v.rect(150, -40, 230, 220, mat="HA", sw=0.25)
    breakline(sh, v.P(20, 220), v.P(240, 220))
    v.rect(175, -280, 205, 200, mat="grout", sw=0.08); v.line(190, -270, 190, 190, sw=0.5)
    v.rect(30, -50, 44, -40, mat="neo", stroke=None)
    v.rect(250, -300, 450, 0, mat="HA", sw=0.25); breakline(sh, v.P(450, -310), v.P(450, 10))
    v.rect(230, -300, 250, -50, mat="epsv", sw=0.05); v.rect(230, -50, 250, 0, mat="neo", stroke=None)
    v.line(28, -300, 28, -160, sw=0.45)
    v.rect(-130, -250, 18, -150, mat="H", sw=0.12); v.rect(18, -250, 26, -150, mat="epsv", sw=0.05)
    for lab, tgt, at in (("1", (130, -200), (x0 + 63, y0 + 46)), ("2", (90, -45), (x0 + 6, y0 + 20)), ("3", (190, 100), (x0 + 63, y0 + 12)),
                         ("4", (37, -45), (x0 + 6, y0 + 30)), ("5", (240, -200), (x0 + 63, y0 + 56)), ("6", (28, -250), (x0 + 6, y0 + 50))):
        sh.callout(v.P(*tgt), at, lab, r=1.4)
    legend(sh, x0, y0 + 63, ["Viga portapanel pretensada 20x85 (E11) s/ cuellos de base", "Mortero de asiento 1 cm + calces de neopreno (nivelación)",
                             "Pasador Ø16 en vaina c/ grout (evita desplazamiento horizontal)", "Sellador PU s/ fondo de junta (enrasado)",
                             "Junta EPS viga / columna 2 cm", "Pintura asfáltica en caras enterradas"])

    # ------------------------------------------------------------ J15 panel / panel 1:5
    x0, y0 = cell(sh, 2, 1, "J15", "Panel / panel (junta vertical)", "Corte horizontal 1:5 · junta de movimiento")
    v = sh.view(x0 + 34, y0 + 55, 5)
    for s in (-1, 1):
        e = s * 10
        xs = lambda d: s * (10 + d)
        v.poly([(xs(0), 10), (xs(10), 0), (xs(150), 0), (xs(150), 60), (xs(0), 60)], mat="HA", sw=0.25)
        v.rect(min(xs(30), xs(150)), 60, max(xs(30), xs(150)), 120, mat="eps", sw=0.1)
        v.rect(min(xs(0), xs(30)), 60, max(xs(0), xs(30)), 120, mat="HA", stroke=None)
        v.poly([(xs(0), 120), (xs(150), 120), (xs(150), 200), (xs(10), 200), (xs(0), 190)], mat="HA", sw=0.25)
        v.line(xs(0), 60, xs(0), 120, sw=0.25)
        breakline(sh, v.P(s * 160, -5), v.P(s * 160, 205))
    v.rect(-10, 2, 10, 12, fill="#222", stroke=None)
    v.circle(0, 24, 11, fill="#d8d8d8", sw=0.1)
    v.rect(-10, 188, 10, 198, fill="#222", stroke=None); v.circle(0, 176, 11, fill="#d8d8d8", sw=0.1)
    v.rect(-10, 70, 10, 150, mat="lanav", sw=0.05)
    sh.text(*v.P(0, -16), "EXTERIOR", 1.3, anchor="middle", bold=True); sh.text(*v.P(0, 206), "INTERIOR", 1.3, anchor="middle", bold=True)
    v.dim((-10, 200), (10, 200), -2.5, "20", size=1.2)
    for lab, tgt, at in (("1", (0, 7), (x0 + 63, y0 + 58)), ("2", (0, 24), (x0 + 63, y0 + 50)), ("3", (0, 110), (x0 + 63, y0 + 34)),
                         ("4", (-80, 90), (x0 + 3, y0 + 30)), ("5", (-150, 5), (x0 + 3, y0 + 58)), ("6", (0, 193), (x0 + 63, y0 + 14))):
        sh.callout(v.P(*tgt), at, lab, r=1.4)
    legend(sh, x0, y0 + 63, ["Sellador PU exterior 10 mm (relación ancho/prof. 2:1)", "Fondo de junta: cordón de polietileno Ø25",
                             "Lana mineral (aislación y cortafuego en la junta)", "Alma EPS 6 cm (hoja ext. y portante unidas c/ conectores)",
                             "Bordes biselados 10 mm (protegen la arista)", "Sellador interior (barrera de vapor / aire)"])

    # ------------------------------------------------------------ dimensionado de juntas
    x0, y0 = cell(sh, 3, 1, "Δ", "Dimensionado de juntas de fachada", "Criterio de cálculo")
    y = y0 + 11
    y = sh.para(x0 + 2, y, 64, "Movimiento térmico de un panel de 2,50 m (ΔT = 50 °C, α = 10⁻⁵/°C):", 1.4, 1.3)
    sh.text(x0 + 6, y + 0.5, "ΔL = α · L · ΔT = 10⁻⁵ · 2500 · 50 = 1,25 mm", 1.5, bold=True); y += 4.4
    y = sh.para(x0 + 2, y, 64, "Sellador PU con capacidad de movimiento ± 25 % → ancho mínimo = ΔL / 0,25 = 5 mm. "
                "Se suman tolerancias de fabricación (± 5 mm) y de montaje (± 5 mm):", 1.4, 1.3)
    sh.text(x0 + 6, y + 0.5, "ancho adoptado = 20 mm · profundidad = 10 mm", 1.5, bold=True); y += 4.6
    rows = [("Junta", "Ancho", "Material"), ("Panel / panel (J15)", "20 mm", "PU + cordón Ø25"), ("Panel / estructura (J13)", "20 mm", "lana + sellador"),
            ("Montante / montante (J11)", "20 mm", "manguito + silicona"), ("Piso / columna (J9)", "20 mm", "EPS + PU"),
            ("Muro cortina / losa", "≥ 90 mm", "lana cortafuego")]
    y = sh.table(x0 + 2, y, [25, 12, 27], rows, size=1.32, rowh=2.9)
    y = sh.para(x0 + 2, y + 3, 64, "Regla: la junta se ubica donde se interrumpe el material o cambia la rigidez, y nunca se la rellena con material rígido.", 1.35, 1.3, ital=True)
    return sh
