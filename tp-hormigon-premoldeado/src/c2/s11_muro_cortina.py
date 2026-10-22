# -*- coding: utf-8 -*-
"""E9 Muro cortina stick: croquis (alzado + cortes) en una lámina; especificación y tipos en otra."""
from lib import Sheet, page, spec, heading, breakline, ground, fitview, autocallouts, TB, TS, TD, TT
from s02_fundacion_columna import legend

GLASS, ALU, SPAN, NEO = "#bfe3f0", "#9aa3ab", "#6f8796", "#111111"


@page("E9 · Muro cortina: alzado y cortes")
def croquis(num, total):
    sh = Sheet(num, total, "E9 · Muro cortina · croquis", escalas="alzado 1:100 · cortes 1:5", fname="E9_Muro_Cortina_Croquis")
    heading(sh, "4º CERRAMIENTOS · E9 MURO CORTINA STICK", "Montantes y travesaños de aluminio armados en obra, colgados de la VL / viga L de la estructura premoldeada")
    sh.title_drawing(12, 32, "ALZADO DE UN TRAMO", "Vista exterior 1:100 · 4 módulos", TT)
    v = sh.view(26, 150, 100)
    W = 5000
    for z0, z1, t in ((40, 3250, "v"), (3250, 4710, "s"), (4710, 7750, "v"), (7750, 9390, "s")):
        v.rect(0, z0, W, z1, fill=GLASS if t == "v" else SPAN, sw=0.1)
    for x in range(0, W + 1, 1250): v.rect(x - 25, -150, x + 25, 9420, fill=ALU, sw=0.12)
    for z in (40, 3250, 4710, 7750, 9390): v.rect(-25, z - 25, W + 25, z + 25, fill=ALU, sw=0.12)
    for z, t in ((0, "±0,00"), (4500, "+4,50"), (9090, "+9,09")):
        v.line(-600, z, W + 600, z, sw=0.12, dash="1.5 0.5", stroke="#666"); sh.level(*v.P(W + 900, z), t)
    ground(sh, v.P(-800, 0)[0], v.P(W + 800, 0)[0], v.P(0, -150)[1])
    for k in range(4): v.dim((k * 1250, 9420), ((k + 1) * 1250, 9420), 3.0, "1,25")
    for z0, z1 in ((40, 3250), (3250, 4710), (4710, 7750), (7750, 9390)):
        v.dim((0, z0), (0, z1), 4.0, f"{(z1 - z0) / 1000:.2f}".replace(".", ","))
    for lab, tgt, at in (("1", (1250, 6000), (90, 70)), ("2", (3125, 2000), (90, 128)), ("3", (2500, 3250), (90, 116)),
                         ("4", (3700, 4000), (90, 104)), ("5", (2500, 4710), (90, 92)), ("6", (2500, 40), (90, 146))):
        sh.callout(v.P(*tgt), at, lab)
    legend(sh, 12, 164, ["1 Montante aluminio 50x150 c/ 1,25 m", "2 Paño de visión: DVH 6 + 12 + 3+3 laminado", "3 Travesaño 50x120 (presor + tapa)",
                         "4 Spandrel: vidrio esmaltado + lana (frente de losa)", "5 Junta de dilatación del montante (J11)", "6 Perfil de arranque (J12)"], w=90)
    # corte vertical 1:5
    sh.title_drawing(108, 32, "CORTE VERTICAL", "1:5 · visión (abajo) / spandrel (arriba)", TT)
    box = (106, 42, 200, 118)
    c = fitview(sh, (box[0] + 8, box[1], box[2] - 8, box[3]), (-30, 182, -150, 210), 5)
    a, h = 0, 60
    c.rect(0, -150, 6, -22, fill=GLASS, sw=0.12); c.rect(18, -150, 25, -22, fill=GLASS, sw=0.12)
    c.rect(6, -36, 18, -22, fill=ALU, sw=0.05); c.rect(6, -26, 18, -22, fill=NEO, stroke=None)
    c.rect(0, h + 8, 6, 210, fill=SPAN, sw=0.12)
    c.rect(40, h + 30, 87, 210, mat="lanav", sw=0.08); c.rect(87, h + 24, 93, 210, fill="#888", sw=0.05); c.rect(40, h + 24, 87, h + 30, fill="#888", sw=0.05)
    c.rect(32, a, 150, a + h, fill=ALU, sw=0.18); c.rect(36, a + 4, 146, a + h - 4, fill="#fff", sw=0.06)
    c.rect(8, a + h / 2 - 8, 32, a + h / 2 + 8, fill=ALU, sw=0.08)
    c.rect(-14, a - 22, -2, a + h + 22, fill=ALU, sw=0.1)
    c.poly([(-30, a - 18), (-14, a - 22), (-14, a + h + 22), (-30, a + h + 18)], fill="#b9c0c6", sw=0.1)
    c.line(-14, a + h / 2, 70, a + h / 2, sw=0.25)
    for yy in (a - 20, a + h + 8):
        c.rect(-2, yy, 0, yy + 12, fill=NEO, stroke=None); c.rect(25, yy, 30, yy + 12, fill=NEO, stroke=None)
    c.rect(2, a + h, 24, a + h + 6, fill="#333", stroke=None)
    c.rect(150, -150, 182, 210, fill="#e3e7ea", sw=0.12)
    for z in (-150, 210): breakline(sh, c.P(-40, z), c.P(195, z))
    sh.text(*c.P(-20, -170), "EXT.", TS, anchor="middle", bold=True); sh.text(*c.P(166, -170), "INT.", TS, anchor="middle", bold=True)
    autocallouts(sh, [(l, c.P(*p)) for l, p in (("a", (3, -100)), ("b", (12, -30)), ("c", (90, 30)), ("d", (-8, 45)), ("e", (-22, 15)),
                                                  ("f", (-1, 74)), ("g", (13, 63)), ("h", (63, 160)), ("i", (166, -60)))], box)
    # corte horizontal 1:5
    sh.title_drawing(108, 128, "CORTE HORIZONTAL", "1:5 · por montante", TT)
    m = fitview(sh, (110, 140, 198, 184), (-160, 160, -182, 30), 5)
    D = lambda d: -d
    for s in (-1, 1):
        x0, x1 = s * 10, s * 160
        m.rect(min(x0, x1), D(0), max(x0, x1), D(6), fill=GLASS, sw=0.12)
        m.rect(min(x0, x1), D(18), max(x0, x1), D(25), fill=GLASS, sw=0.12)
        m.rect(min(s * 12, s * 26), D(6), max(s * 12, s * 26), D(18), fill=ALU, sw=0.06)
        m.rect(min(s * 15, s * 35), D(-2), max(s * 15, s * 35), D(0), fill=NEO, stroke=None)
        m.rect(min(s * 15, s * 35), D(25), max(s * 15, s * 35), D(30), fill=NEO, stroke=None)
        breakline(sh, m.P(s * 160, 10), m.P(s * 160, -35))
    m.rect(-25, D(32), 25, D(182), fill=ALU, sw=0.18); m.rect(-22, D(35), 22, D(179), fill="#fff", sw=0.06)
    m.rect(-6, D(8), 6, D(32), fill=ALU, sw=0.08)
    m.rect(-40, D(-14), 40, D(-2), fill=ALU, sw=0.1)
    m.poly([(-36, D(-14)), (36, D(-14)), (30, D(-30)), (-30, D(-30))], fill="#b9c0c6", sw=0.1)
    m.line(0, D(-14), 0, D(70), sw=0.4)
    m.dim((-25, D(182)), (25, D(182)), -3.0, "50")
    m.dim((25, D(32)), (25, D(182)), -6.0, "150")
    sh.text(*m.P(-110, D(-40)), "EXTERIOR", TS, anchor="middle", bold=True); sh.text(*m.P(110, D(150)), "INTERIOR", TS, anchor="middle", bold=True)
    y = 200
    sh.text(108, 196, "Referencias de los cortes", TS, bold=True)
    items = ["a DVH 6 + 12 + 3+3 laminado", "b Separador + butilo + silicona", "c Travesaño tubular 50x120 (6063-T6)",
             "d Presor atornillado (inox c/ 25 cm)", "e Tapa clipada", "f Burletes EPDM", "g Calzo de apoyo del vidrio",
             "h Spandrel: bandeja galv. + lana 50", "i Montante 50x150 en vista"]
    for k, t in enumerate(items):
        lab, txt = t.split(" ", 1)
        col, row = divmod(k, 5)
        xx, yy = 108 + col * 46, y + 2 + row * 5.5
        sh.ball(xx + 2, yy - 0.8, lab, r=1.9); sh.para(xx + 5.5, yy, 40, txt, 2.1, 1.15)
    return sh


@page("E9 · Muro cortina: especificación y tipos")
def especificacion(num, total):
    sh = Sheet(num, total, "E9 · Muro cortina · especificación", escalas="s/ escala", fname="E9_Muro_Cortina_Especificacion")
    heading(sh, "4º CERRAMIENTOS · E9 MURO CORTINA · ESPECIFICACIÓN", "Medidas, función, especificación técnica y justificación del sistema stick")
    y = spec(sh, 12, 32, 186, "ESPECIFICACIÓN TÉCNICA", [
        ("Función:", "cerramiento NO portante de la fachada principal: estanqueidad al agua y al aire, luz natural y visuales, sin cargar la estructura (cuelga de la VL / viga L)."),
        ("Medidas:", "módulo 1,25 m; montantes 50x150 c/ 1,25 m en tramos de 1 nivel (4,68 m) con junta de dilatación de 20 mm; travesaños 50x120; vidrio máx. 1,25 x 3,21 m."),
        ("Máx./mín.:", "luz del montante entre anclajes ≤ 4,50-5,00 m; flecha ≤ L/175 (máx. 19 mm) con el viento de cálculo (CIRSOC 102); módulos usuales 0,90 a 1,50 m."),
        ("Materiales:", "aluminio 6063-T6 anodizado o pintado; DVH 6+12+3+3 (laminado del lado interior); spandrel templado esmaltado 6 mm + lana 50 mm; EPDM y siliconas neutras."),
        ("Prestaciones:", "peso ≈ 45-50 kg/m² · K ≈ 2,8 W/m²K (≈ 1,8 con low-e) · aislación acústica ≈ 35 dB · sin resistencia al fuego: requiere barrera cortafuego en cada losa."),
        ("Anclaje:", "grapa galvanizada regulable en 3 direcciones (± 25 mm) abulonada al riel embutido en la VL: absorbe las tolerancias de la estructura premoldeada (± 10-15 mm)."),
        ("Montaje:", "replanteo topográfico → grapas → montantes de abajo hacia arriba con manguito → travesaños → sellado de barrera → vidrios desde el exterior con plataforma (M6) → presores, tapas y sellos → ensayo de estanqueidad con manguera."),
    ], size=TB, lead=1.3)
    y += 6
    sh.text(12, y, "TIPOS DE MURO CORTINA Y ELECCIÓN", TT, bold=True)
    rows = [("Sistema", "Armado", "Ventaja", "Limitación"),
            ("STICK (elegido)", "en obra, pieza por pieza", "económico; absorbe tolerancias de la estructura premoldeada; perfiles livianos", "más mano de obra en altura y sellados in situ"),
            ("Unitizado", "módulos de piso armados en taller", "rapidez y control de calidad", "requiere grúa y mucha repetición; caro en 2 niveles"),
            ("Semi-unitizado", "montantes en obra + paños de taller", "intermedio", "logística de paños"),
            ("Vidrio estructural (VEC)", "vidrio pegado c/ silicona estructural", "piel continua sin tapas", "costoso; control estricto de adhesión")]
    sh.table(12, y + 2.5, [36, 44, 58, 48], rows, size=TS, lead=1.2)
    return sh


PAGES = [croquis, especificacion]
