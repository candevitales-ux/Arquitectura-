# -*- coding: utf-8 -*-
"""Lámina 11 – E9 Muro cortina stick: alzado del módulo, corte vertical por travesaño, corte horizontal por montante."""
from lib import Sheet, spec, heading, breakline, ground
import geo

GLASS, ALU, SPAN, NEO = "#bfe3f0", "#9aa3ab", "#6f8796", "#111111"


def make(num, total):
    sh = Sheet(num, total, "Cerramientos 1 · muro cortina", "E9 Muro cortina stick: croquis proporcionado, medidas, función y especificación",
               "Alzado 1:100 · corte vertical 1:5 · corte horizontal 1:5")
    heading(sh, "4º MURO CORTINA (CERRAMIENTO VIDRIADO)  ·  1/3", "Sistema stick (montantes y travesaños armados en obra) anclado a la VL / viga L de la estructura premoldeada")

    # ============================================================ ALZADO 1:100
    sh.title_drawing(10, 26, "ALZADO DE UN TRAMO (4 módulos)", "Vista exterior 1:100", 2.0)
    v = sh.view(22, 132, 100)
    W = 5000
    zones = [(40, 3250, "v"), (3250, 4710, "s"), (4710, 7750, "v"), (7750, 9390, "s")]
    for z0, z1, t in zones:
        v.rect(0, z0, W, z1, fill=GLASS if t == "v" else SPAN, sw=0.1)
    for x in range(0, W + 1, 1250):
        v.rect(x - 25, -150, x + 25, 9420, fill=ALU, sw=0.12)
    for z in (40, 3250, 4710, 7750, 9390):
        v.rect(-25, z - 25, W + 25, z + 25, fill=ALU, sw=0.12)
    for z, t in ((0, "±0,00"), (4500, "+4,50"), (9090, "+9,09")):
        v.line(-600, z, W + 600, z, sw=0.1, dash="1.5 0.5", stroke="#666")
        sh.level(*v.P(W + 700, z), t, 1.3)
    ground(sh, v.P(-800, 0)[0], v.P(W + 800, 0)[0], v.P(0, -150)[1])
    for k in range(4): v.dim((k * 1250, 9420), ((k + 1) * 1250, 9420), 2.0, "1,25", size=1.2)
    for z0, z1 in ((40, 3250), (3250, 4710), (4710, 7750), (7750, 9390)):
        v.dim((0, z0), (0, z1), 2.5, f"{(z1 - z0) / 1000:.2f}".replace(".", ","), size=1.2)
    for lab, tgt, at in (("1", (1250, 6000), (84, 50)), ("2", (3125, 6000), (84, 60)), ("3", (2500, 3250), (84, 92)),
                         ("4", (3700, 4000), (84, 82)), ("5", (2500, 4710), (84, 72)), ("6", (2500, 40), (84, 122))):
        sh.callout(v.P(*tgt), at, lab, r=1.4)
    yy = 140
    for t in ("1 Montante aluminio 50x150 c/ 1,25 m", "2 Paño de visión: DVH 6 + 12 + 3+3 laminado", "3 Travesaño 50x120 (presor + tapa)",
              "4 Spandrel: vidrio esmaltado + lana (frente de losa)", "5 Junta de dilatación del montante (J11)", "6 Perfil de arranque (J12)"):
        sh.text(12, yy, t, 1.35); yy += 2.4

    # ============================================================ CORTE VERTICAL 1:10 (travesaño visión / spandrel)
    sh.title_drawing(96, 26, "CORTE VERTICAL POR TRAVESAÑO", "1:5 · paño de visión (abajo) / spandrel (arriba)", 2.0)
    c = sh.view(110, 76, 5)
    a, h = 0, 60
    c.rect(0, -130, 6, -22, fill=GLASS, sw=0.12); c.rect(18, -130, 25, -22, fill=GLASS, sw=0.12)
    c.line(21.5, -130, 21.5, -22, sw=0.05)
    c.rect(6, -36, 18, -22, fill=ALU, sw=0.05); c.rect(6, -26, 18, -22, fill=NEO, stroke=None)
    c.rect(0, h + 8, 6, 210, fill=SPAN, sw=0.12)
    c.rect(40, h + 30, 87, 210, mat="lanav", sw=0.08); c.rect(87, h + 24, 93, 210, fill="#888", sw=0.05); c.rect(40, h + 24, 87, h + 30, fill="#888", sw=0.05)
    c.rect(32, a, 150, a + h, fill=ALU, sw=0.15); c.rect(36, a + 4, 146, a + h - 4, fill="#fff", sw=0.06)
    c.rect(8, a + h / 2 - 8, 32, a + h / 2 + 8, fill=ALU, sw=0.08)
    c.rect(-14, a - 22, -2, a + h + 22, fill=ALU, sw=0.1)
    c.poly([(-30, a - 18), (-14, a - 22), (-14, a + h + 22), (-30, a + h + 18)], fill="#b9c0c6", sw=0.1)
    c.line(-14, a + h / 2, 70, a + h / 2, sw=0.2)
    for yy_ in (a - 20, a + h + 8):
        c.rect(-2, yy_, 0, yy_ + 12, fill=NEO, stroke=None); c.rect(25, yy_, 30, yy_ + 12, fill=NEO, stroke=None)
    c.rect(2, a + h, 24, a + h + 6, fill="#333", stroke=None)
    c.rect(150, -130, 182, 210, fill="#e3e7ea", sw=0.12)
    for z in (-130, 210): breakline(sh, c.P(-40, z), c.P(200, z))
    sh.text(*c.P(-40, -120), "EXT.", 1.3, anchor="end", bold=True); sh.text(*c.P(145, -120), "INT.", 1.3, anchor="end", bold=True)
    for lab, tgt, at in (("a", (3, -100), (99, 92)), ("b", (12, -30), (99, 80)), ("c", (90, 30), (148, 62)), ("d", (-8, 45), (99, 64)),
                         ("e", (-22, 15), (99, 72)), ("f", (-1, 74), (99, 50)), ("g", (13, 63), (148, 52)), ("h", (63, 160), (148, 38)), ("i", (166, -60), (148, 86))):
        sh.callout(c.P(*tgt), at, lab, r=1.3)
    yy = 104
    for t in ("a DVH 6 templado + 12 cámara + 3+3 laminado PVB", "b Separador alum. + butilo + silicona estructural", "c Travesaño tubular 50x120 (alum. 6063-T6)",
              "d Presor atornillado (tornillos inox c/ 25 cm)", "e Tapa clipada", "f Burletes EPDM exterior / interior",
              "g Calzo de apoyo del vidrio (EPDM, a L/4)", "h Spandrel: bandeja galv. + lana 50 mm", "i Montante 50x150 en vista"):
        sh.text(96, yy, t, 1.32); yy += 2.25

    # ============================================================ CORTE HORIZONTAL 1:5 (montante)
    sh.title_drawing(150, 26, "CORTE HORIZONTAL POR MONTANTE", "1:5 · fijación del DVH (sistema presor-tapa)", 2.0)
    m = sh.view(190, 40, 5)
    D = lambda d: -d                                                           # profundidad -> y (exterior arriba)
    for s in (-1, 1):
        x0, x1 = s * 10, s * 160
        m.rect(min(x0, x1), D(0), max(x0, x1), D(6), fill=GLASS, sw=0.12)
        m.rect(min(x0, x1), D(18), max(x0, x1), D(25), fill=GLASS, sw=0.12)
        m.rect(min(s * 12, s * 26), D(6), max(s * 12, s * 26), D(18), fill=ALU, sw=0.06)
        m.rect(min(s * 15, s * 35), D(-2), max(s * 15, s * 35), D(0), fill=NEO, stroke=None)
        m.rect(min(s * 15, s * 35), D(25), max(s * 15, s * 35), D(30), fill=NEO, stroke=None)
        breakline(sh, m.P(s * 160, 10), m.P(s * 160, -35))
    m.rect(-25, D(32), 25, D(182), fill=ALU, sw=0.15); m.rect(-22, D(35), 22, D(179), fill="#fff", sw=0.06)
    m.line(-22, D(110), 22, D(110), sw=0.06)
    m.rect(-6, D(8), 6, D(32), fill=ALU, sw=0.08)
    m.rect(-40, D(-14), 40, D(-2), fill=ALU, sw=0.1)
    m.poly([(-36, D(-14)), (36, D(-14)), (30, D(-30)), (-30, D(-30))], fill="#b9c0c6", sw=0.1)
    m.line(0, D(-14), 0, D(70), sw=0.35)
    m.dim((-25, D(182)), (25, D(182)), -2.2, "50", size=1.2)
    m.dim((25, D(32)), (25, D(182)), -5.0, "150", size=1.2)
    m.dim((-160, D(0)), (-160, D(25)), 3.0, "25", size=1.1)
    sh.text(*m.P(-150, D(-40)), "EXTERIOR", 1.3, bold=True); sh.text(*m.P(60, D(170)), "INTERIOR", 1.3, bold=True)

    # ============================================================ ESPECIFICACIÓN
    spec(sh, 150, 84, 139, "E9 · ESPECIFICACIÓN TÉCNICA", [
        ("Función:", "cerramiento NO portante de la fachada principal: estanqueidad al agua y aire, luz natural y visuales, sin cargar la estructura (cuelga de la VL / viga L)."),
        ("Medidas:", "módulo 1,25 m; montantes 50x150 c/ 1,25 m, tramos de 1 nivel (4,68 m) con junta de dilatación de 20 mm; travesaños 50x120; vidrio máx. 1,25 x 3,21 m."),
        ("Máx./mín.:", "luz del montante entre anclajes ≤ 4,50-5,00 m; flecha ≤ L/175 (máx. 19 mm) con viento de cálculo (CIRSOC 102); módulos usuales 0,90 a 1,50 m."),
        ("Materiales:", "aluminio 6063-T6 anodizado / pintado; DVH 6+12+3+3 (lam. PVB del lado interior por seguridad); spandrel templado esmaltado 6 mm + lana 50 mm; EPDM y siliconas neutras."),
        ("Prestaciones:", "peso ≈ 45-50 kg/m² · K ≈ 2,8 W/m²K (≈ 1,8 con low-e) · aislación acústica ≈ 35 dB · NO aporta resistencia al fuego (requiere barrera cortafuego en cada losa)."),
        ("Anclaje:", "grapa galv. regulable en 3 direcciones (± 25 mm) abulonada al riel embutido en la VL: absorbe tolerancias de la estructura premoldeada (± 10-15 mm)."),
        ("Montaje:", "replanteo topográfico → grapas → montantes (de abajo hacia arriba, c/ manguito) → travesaños → sellado de barrera → vidrios desde el exterior con plataforma (M6) → presores, tapas y sellos; ensayo de estanqueidad con manguera."),
    ], size=1.42, lead=1.22, tsize=2.0)
    sh.text(150, 140, "TIPOS DE MURO CORTINA Y ELECCIÓN", 2.0, bold=True)
    rows = [("Sistema", "Armado", "Ventaja", "Limitación"),
            ("STICK (elegido)", "en obra, pieza por pieza", "económico, absorbe tolerancias de la estructura premoldeada, perfiles livianos", "más mano de obra en altura y sellados in situ"),
            ("Unitizado", "módulos de piso armados en taller", "rapidez y control de calidad", "requiere grúa y alta repetición; caro en 2 niveles"),
            ("Semi-unitizado", "montantes en obra + paños de taller", "intermedio", "logística de paños"),
            ("Vidrio estructural (VEC)", "vidrio pegado c/ silicona", "piel continua sin tapas", "costoso, control estricto de adhesión")]
    sh.table(150, 141.5, [27, 32, 46, 34], rows, size=1.3, lead=1.15)
    return sh
