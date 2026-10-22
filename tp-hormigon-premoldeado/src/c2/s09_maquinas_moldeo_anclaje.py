# -*- coding: utf-8 -*-
"""Lámina 09 – Máquinas y dispositivos de MOLDEO (planta de premoldeado) y de ANCLAJE en obra."""
import math
from lib import Sheet, spec, heading, ground, breakline, REB
import geo

STEEL, YEL, DARK = "#5a5a5a", "#f2c230", "#3a3a3a"
MOLD = "#7d8a96"


def make(num, total):
    sh = Sheet(num, total, "Máquinas y dispositivos 2", "Moldeo en planta (pista de pretensado) y anclaje en obra",
               "Pista 1:200 · molde 1:50 · gato 1:20 · puntales y plataforma 1:150 · grouteo 1:50 · herramientas 1:20")
    heading(sh, "3º MÁQUINAS Y DISPOSITIVOS DE MOLDEO Y ANCLAJE  ·  2/3", "Moldeo: en la planta del fabricante · Anclaje: en obra, durante y después del montaje")

    # ============================================================ M4 PISTA DE PRETENSADO 1:200
    sh.title_drawing(10, 26, "M4 · PISTA (BANCO) DE PRETENSADO c/ MOLDES METÁLICOS", "Elevación 1:200 · largo de pista 100 m (se muestran los extremos)", 2.1)
    v = sh.view(18, 70, 200)
    w = sh.view(-11, 70, 200)                      # tramo final de la pista (después del corte)
    v.rect(-1500, -400, 11500, 300, mat="H", sw=0.15)
    w.rect(18000, -400, 26500, 300, mat="H", sw=0.15)
    breakline(sh, v.P(11500, -600), v.P(11500, 2600)); breakline(sh, w.P(18000, -600), w.P(18000, 2600))
    v.rect(-1500, 300, 0, 2300, mat="HA", sw=0.25); w.rect(25000, 300, 26500, 2300, mat="HA", sw=0.25)
    v.rect(500, 300, 10080, 950, fill=MOLD, sw=0.15); v.rect(500, 950, 10080, 1000, fill="#e3dccb", sw=0.1)
    w.rect(18000, 300, 24500, 950, fill=MOLD, sw=0.15); w.rect(18000, 950, 24500, 1000, fill="#e3dccb", sw=0.1)
    for vv, (a, b) in ((v, (0, 11500)), (w, (18000, 25000))):
        vv.line(a, 450, b, 450, stroke=REB, sw=0.25); vv.line(a, 560, b, 560, stroke=REB, sw=0.25)
    w.rect(26500, 400, 27900, 650, fill=YEL, sw=0.15); w.line(27900, 525, 28400, 525, sw=0.3)
    w.rect(25800, 1700, 26200, 2200, fill="#777", sw=0.1)
    ground(sh, v.P(-2000, 0)[0], w.P(28600, 0)[0], v.P(0, 300)[1])
    # pórtico grúa de planta (esquema)
    for x in (3000, 9500):
        v.line(x, 300, x, 5000, sw=0.25)
    v.rect(2800, 5000, 9700, 5400, fill=YEL, sw=0.15)
    v.line(6250, 5000, 6250, 3300, sw=0.15); v.rect(6050, 3000, 6450, 3300, fill=DARK, sw=0.1)
    for lab, tgt, at in (("1", (-750, 1500), (12, 42)), ("2", (5000, 500), (40, 80)), ("3", (5000, 975), (70, 44)), ("4", (8000, 450), (80, 80)),
                         ("5", (21200, 525), (128, 50)), ("6", (6000, 5200), (70, 36))):
        sh.callout(v.P(*tgt), at, lab, r=1.4)
    yy = 85
    for t in ("1 Cabezal (muerto) de anclaje de H°A°", "2 Molde metálico (encofrado de acero, reutilizable > 500 usos)", "3 Pieza TT hormigonada",
              "4 Cordones Ø12,7 tesados de cabezal a cabezal", "5 Gato hidráulico de tesado + bomba", "6 Pórtico grúa de planta (desmolde y acopio)"):
        sh.text(12, yy, t, 1.4); yy += 2.4
    w.dim((25000, 2300), (25000 + 1500, 2300), 2.0, "1,50", size=1.2)

    # ============================================================ molde TT 1:50
    sh.title_drawing(140, 26, "Molde TT (sección) 1:50", None, 1.9)
    m = sh.view(146, 50, 50)
    P = geo.perfil_TT()
    m.poly([(-150, 650), (-150, -200), (2550, -200), (2550, 650), (2400, 650), (2400, 600), (1890, 600), (1860, 0), (1740, 0),
            (1710, 600), (690, 600), (660, 0), (540, 0), (510, 600), (0, 600), (0, 650)], fill=MOLD, sw=0.2)
    m.poly(P, mat="HA", sw=0.25)
    for xc in (600, 1800):
        for z in (40, 90, 140): m.dot(xc, z, 0.25, "#000")
    for x in (-150, 2550):
        m.rect(x - 60 if x < 0 else x, 100, x if x < 0 else x + 60, 260, fill=YEL, sw=0.1)
    m.rect(-300, -400, 2700, -200, fill="#888", sw=0.15)
    sh.note(m.P(2580, 180), (204, 34), "vibrador externo", 1.3)
    sh.note(m.P(1200, -300), (204, 44), "bastidor / bancada", 1.3)
    sh.note(m.P(2000, 300), (204, 39), "chapa de molde 8 mm", 1.3)

    # ============================================================ gato 1:20
    sh.title_drawing(140, 66, "Gato de tesado unifilar 1:20", None, 1.9)
    g = sh.view(150, 80, 20)
    g.rect(0, -150, 300, 150, mat="HA", sw=0.2)
    g.rect(300, -50, 360, 50, fill="#999", sw=0.1)
    g.poly([(360, -25), (420, -15), (420, 15), (360, 25)], fill=DARK, sw=0.1)
    g.rect(430, -120, 1100, 120, fill=YEL, sw=0.2); g.rect(1100, -70, 1250, 70, fill="#777", sw=0.15)
    g.line(-100, 0, 1500, 0, stroke=REB, sw=0.3)
    g.line(1250, 40, 1450, 300, sw=0.2)
    sh.note(g.P(390, 0), (176, 72), "cuñas + anclaje", 1.3)
    sh.note(g.P(800, 120), (186, 75.5), "cilindro hidráulico", 1.3)
    sh.text(150, 88, "Fuerza por cordón Ø12,7: 0,75 · 1860 MPa · 98,7 mm² ≈ 138 kN (14 t)", 1.3)

    spec(sh, 232, 26, 57, "Proceso de moldeo", [
        ("1", "limpieza del molde y desmoldante."), ("2", "colocación y tesado de cordones (gato, control de presión y alargamiento)."),
        ("3", "armadura pasiva, insertos, vainas y riel embutido."), ("4", "hormigonado H-45 con vibradores externos."),
        ("5", "curado a vapor 12-16 h (60 °C máx.)."), ("6", "destesado c/ f'c ≥ 30 MPa y corte de cordones c/ amoladora."),
        ("7", "desmolde con pórtico grúa, marcado (código de pieza) y acopio s/ tacos."),
    ], size=1.35, lead=1.22, tsize=1.8)

    # ============================================================ M5 PUNTALES DE APLOMADO 1:150
    sy = 104
    sh.title_drawing(10, sy, "M5 · PUNTALES TELESCÓPICOS DE APLOMADO", "Vista 1:150 · arriostre provisorio de la columna", 1.9)
    p = sh.view(36, 178, 150)
    p.poly([(-525, -510), (525, -510), (525, -1450), (-525, -1450)], fill=geo.C_FUND, sw=0.12)
    p.rect(-200, -1300, 200, geo.COL_TOP, fill="#cfd3d7", sw=0.18)
    for s in (-1, 1):
        p.poly([(s * 200, 3495), (s * 530, 3495), (s * 530, 3335), (s * 200, 3025)], fill="#cfd3d7", sw=0.12)
        p.line(s * 200, 6200, s * 3800, 0, sw=0.4, stroke=STEEL)
        p.line(s * 2000, 3100, s * 2100, 2950, sw=0.6, stroke=YEL)
        p.rect(s * 3800 - 400, -300, s * 3800 + 400, 0, mat="H", sw=0.1)
    ground(sh, p.P(-4800, 0)[0], p.P(4800, 0)[0], p.P(0, 0)[1])
    p.dim((4400, 0), (4400, 6200), -2.0, "≈ 2/3 h", size=1.2)
    sh.note(p.P(-2900, 1500), (12, 140), "puntal regulable 4-7 m", 1.3)
    sh.note(p.P(3800, -150), (52, 182), "muerto de H° / placa", 1.3)

    # ============================================================ M6 PLATAFORMA ELEVADORA 1:150
    sh.title_drawing(78, sy, "M6 · PLATAFORMA ELEVADORA ARTICULADA", "Vista 1:150 · montaje y sellado de fachada", 1.9)
    e = sh.view(84, 183, 150)
    e.rect(0, 400, 2400, 1300, fill=YEL, sw=0.15)
    for x in (400, 2000): e.circle(x, 400, 400, fill="#222", sw=0.08)
    e.rect(600, 1300, 1800, 2100, fill="#777", sw=0.12)
    pts = [(1500, 2000), (3800, 6200), (6000, 4500), (7400, 9200)]
    for a, b in zip(pts, pts[1:]): e.line(*a, *b, sw=0.9, stroke=YEL); e.line(*a, *b, sw=0.15)
    e.rect(7000, 9200, 8400, 10300, fill="none", sw=0.25); e.line(7000, 9700, 8400, 9700, sw=0.1)
    e.rect(9000, 0, 9300, 10800, fill="#bfe3f0", sw=0.15)
    ground(sh, e.P(-500, 0)[0], e.P(10500, 0)[0], e.P(0, 0)[1])
    e.dim((10000, 0), (10000, 10300), -2.0, "h trabajo ≈ 12 m", size=1.2)
    sh.note(e.P(7700, 10000), (113, 112), "canasto 2 personas · 230 kg", 1.3)
    sh.note(e.P(9150, 6000), (125, 150), "muro cortina", 1.3)

    # ============================================================ M7 GROUTEO 1:50
    sh.title_drawing(148, sy, "M7 · EQUIPO DE GROUTEO", "1:50 · mezcladora + bomba + manguera", 1.9)
    q = sh.view(152, 150, 50)
    q.rect(0, 300, 900, 1200, fill="#4a90c2", sw=0.15); q.rect(100, 1200, 800, 1400, fill="#2c5f86", sw=0.12)
    q.rect(0, 0, 1000, 300, fill=DARK, sw=0.12)
    for x in (150, 850): q.circle(x, 0, 150, fill="#222", sw=0.08)
    q.rect(1200, 100, 2300, 700, fill="#d35400", sw=0.15); q.circle(1450, 400, 180, fill="#777", sw=0.1)
    q.pline([(2300, 400), (2500, 400), (2600, 900), (2700, 900)], sw=0.45)
    q.line(900, 800, 1300, 700, sw=0.4)
    q.rect(2700, 600, 2900, 1300, fill="#cfd3d7", sw=0.12)
    ground(sh, q.P(-200, 0)[0], q.P(3000, 0)[0], q.P(0, -150)[1])
    sh.text(152, 157, "Mezcladora de paleta 200 l · bomba de", 1.3)
    sh.text(152, 159.4, "tornillo 2-3 m³/h · manguera Ø25 a la vaina", 1.3)
    sh.text(152, 161.8, "(se inyecta desde abajo, sale por el purgador)", 1.3)

    # ============================================================ M8 HERRAMIENTAS 1:20
    sh.title_drawing(218, sy, "M8 · HERRAMIENTAS DE ANCLAJE", "1:20", 1.9)
    t = sh.view(224, 121, 20)
    t.rect(0, 0, 450, 40, fill="#888", sw=0.12); t.rect(450, -30, 520, 70, fill=DARK, sw=0.1); t.circle(485, 20, 40, fill="none", sw=0.12)
    t.rect(-60, 5, 0, 35, fill="#555", sw=0.08)
    sh.text(220, 127, "Llave dinamométrica (torque M12-M20)", 1.3)
    t2 = sh.view(224, 136, 20)
    t2.rect(0, 0, 300, 150, fill="#2e86c1", sw=0.15); t2.rect(60, -200, 160, 0, fill="#2e86c1", sw=0.12)
    t2.line(300, 75, 560, 75, sw=0.5)
    sh.text(240, 141, "Taladro percutor +", 1.3); sh.text(240, 143.4, "broca widia Ø9,5", 1.3)
    t3 = sh.view(268, 176, 20)
    for s_ in (-1, 1): t3.line(0, 450, s_ * 220, 0, sw=0.2)
    t3.line(0, 0, 0, 450, sw=0.15)
    t3.rect(-100, 450, 100, 650, fill=YEL, sw=0.12); t3.circle(0, 690, 40, fill="#e74c3c", sw=0.05)
    t3.rect(-1150, 0, -550, 70, fill="#d4ac0d", sw=0.12); t3.circle(-850, 35, 22, fill="#5dade2", sw=0.05)
    sh.text(220, 180.5, "Nivel láser rotativo / estación total y nivel", 1.3)
    sh.text(220, 182.9, "de burbuja (aplomado ± 5 mm, nivel de apoyos)", 1.3)
    spec(sh, 148, 168, 64, None, [
        ("Anclaje en obra:", "cuñas + puntales hasta que fragua el grout del cáliz (24-48 h); vainas y juntas se inyectan con M7; bulones y grapas se aprietan al torque de proyecto (M8)."),
    ], size=1.3, lead=1.22)
    return sh
