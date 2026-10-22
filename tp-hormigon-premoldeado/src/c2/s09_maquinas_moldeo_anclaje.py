# -*- coding: utf-8 -*-
"""Máquinas y dispositivos de MOLDEO (planta del fabricante) y de ANCLAJE en obra (una lámina cada uno)."""
from lib import Sheet, page, spec, heading, ground, breakline, wrap, fitview, REB, TB, TS, TD, TT
from s02_fundacion_columna import legend
from s06_juntas_estructura import CW, CH
import geo

STEEL, YEL, DARK = "#5a5a5a", "#f2c230", "#3a3a3a"
MOLD = "#7d8a96"


@page("M4 · Moldeo: pista de pretensado, molde y gato")
def moldeo(num, total):
    sh = Sheet(num, total, "M4 · Moldeo en planta", escalas="pista 1:200 · molde 1:25 · gato 1:20", fname="M4_Moldeo_Pista_Pretensado")
    heading(sh, "3º MÁQUINAS DE MOLDEO · M4 PISTA DE PRETENSADO", "Las piezas se fabrican en la planta del premoldeador, en moldes metálicos sobre pistas de tesado")
    sh.title_drawing(12, 32, "PISTA (BANCO) DE PRETENSADO c/ MOLDES METÁLICOS", "Elevación 1:200 · pista de 100 m (se muestran los extremos)", TT)
    v = sh.view(24, 84, 200)
    w = sh.view(24 + 78 - 18000 / 200, 84, 200)
    v.rect(-1500, -400, 11500, 300, mat="H", sw=0.15)
    w.rect(18000, -400, 26500, 300, mat="H", sw=0.15)
    breakline(sh, v.P(11500, -600), v.P(11500, 2600)); breakline(sh, w.P(18000, -600), w.P(18000, 2600))
    v.rect(-1500, 300, 0, 2300, mat="HA", sw=0.25); w.rect(25000, 300, 26500, 2300, mat="HA", sw=0.25)
    v.rect(500, 300, 10080, 950, fill=MOLD, sw=0.15); v.rect(500, 950, 10080, 1000, fill="#e3dccb", sw=0.1)
    w.rect(18000, 300, 24500, 950, fill=MOLD, sw=0.15); w.rect(18000, 950, 24500, 1000, fill="#e3dccb", sw=0.1)
    for vv, (a, b) in ((v, (0, 11500)), (w, (18000, 25000))):
        vv.line(a, 450, b, 450, stroke=REB, sw=0.3); vv.line(a, 560, b, 560, stroke=REB, sw=0.3)
    w.rect(26500, 400, 27900, 650, fill=YEL, sw=0.15); w.line(27900, 525, 28400, 525, sw=0.35)
    ground(sh, v.P(-2000, 0)[0], w.P(28600, 0)[0], v.P(0, 300)[1])
    for x in (3000, 9500): v.line(x, 300, x, 5000, sw=0.3)
    v.rect(2800, 5000, 9700, 5400, fill=YEL, sw=0.15)
    v.line(6250, 5000, 6250, 3300, sw=0.18); v.rect(6050, 3000, 6450, 3300, fill=DARK, sw=0.1)
    w.dim((25000, 2300), (26500, 2300), 3.0, "1,50")
    for lab, tgt, at in (("1", (-750, 1500), (14, 50)), ("2", (5000, 500), (60, 98)), ("3", (5000, 975), (90, 60)), ("4", (8000, 450), (90, 98)),
                         ("5", (21200 + 5800 * 0 + 5300, 525), (190, 66)), ("6", (6000, 5200), (90, 46))):
        tgtp = v.P(*tgt) if lab != "5" else w.P(27200, 525)
        sh.callout(tgtp, at, lab)
    y = legend(sh, 12, 108, ["1 Cabezal (muerto) de anclaje de H°A° en cada extremo", "2 Molde metálico (encofrado de acero, > 500 usos)",
                             "3 Pieza TT hormigonada", "4 Cordones Ø12,7 tesados de cabezal a cabezal", "5 Gato hidráulico de tesado + bomba",
                             "6 Pórtico grúa de planta (desmolde y acopio)"], w=92)
    # molde 1:25
    sh.title_drawing(12, 150, "MOLDE METÁLICO DEL TT (sección)", "esc. 1:25", TT)
    m = sh.view(30 + 150 / 25, 197, 25)
    m.poly([(-150, 650), (-150, -200), (2550, -200), (2550, 650), (2400, 650), (2400, 600), (1890, 600), (1860, 0), (1740, 0),
            (1710, 600), (690, 600), (660, 0), (540, 0), (510, 600), (0, 600), (0, 650)], fill=MOLD, sw=0.25)
    m.poly(geo.perfil_TT(), mat="HA", sw=0.3)
    for xc in (600, 1800):
        for z in (40, 90, 140): m.dot(xc, z, 0.4, "#000")
    for x in (-150, 2550): m.rect(x - 60 if x < 0 else x, 100, x if x < 0 else x + 60, 260, fill=YEL, sw=0.1)
    m.rect(-300, -400, 2700, -200, fill="#888", sw=0.15)
    sh.note(m.P(2610, 180), (160, 183), "vibrador externo")
    sh.note(m.P(2000, -300), (160, 200), "bastidor / bancada")
    sh.note(m.P(2000, 300), (160, 166), "chapa de molde 8 mm")
    # gato 1:20
    sh.title_drawing(108, 104, "GATO DE TESADO UNIFILAR", "esc. 1:20", TT)
    g = sh.view(114, 128, 20)
    g.rect(0, -150, 300, 150, mat="HA", sw=0.25)
    g.rect(300, -50, 360, 50, fill="#999", sw=0.1)
    g.poly([(360, -25), (420, -15), (420, 15), (360, 25)], fill=DARK, sw=0.1)
    g.rect(430, -120, 1100, 120, fill=YEL, sw=0.25); g.rect(1100, -70, 1250, 70, fill="#777", sw=0.15)
    g.line(-100, 0, 1500, 0, stroke=REB, sw=0.35)
    sh.note(g.P(390, 0), (125, 140), "cuñas + anclaje")
    sh.note(g.P(800, 120), (160, 116), "cilindro hidráulico")
    sh.para(108, 146, 92, "Fuerza por cordón Ø12,7: 0,75 · 1860 MPa · 98,7 mm² ≈ 138 kN (14 t); se controla presión y alargamiento.", TS, 1.25)
    spec(sh, 12, 222, 186, "PROCESO DE MOLDEO", [
        ("1", "limpieza del molde y desmoldante."), ("2", "colocación y tesado de cordones con el gato."),
        ("3", "armadura pasiva, insertos, vainas y riel embutido."), ("4", "hormigonado H-45 con vibradores externos."),
        ("5", "curado a vapor 12-16 h (60 °C máx.)."), ("6", "destesado con f'c ≥ 30 MPa; corte de cordones."),
        ("7", "desmolde con pórtico grúa, marcado de la pieza y acopio s/ tacos."),
    ], size=TS, lead=1.25, tsize=2.9)
    return sh


def mcell(sh, i, j, lab, title, sub):
    x0, y0 = 10 + i * (CW + 2), 28 + j * (CH + 2)
    sh.rect(x0, y0, x0 + CW, y0 + CH, stroke="#888", sw=0.15, layer="MARCO")
    sh.ball(x0 + 5, y0 + 5.5, lab, r=3.3, fill="#fde8b0")
    sh.text(x0 + 10.5, y0 + 6.2, title, 2.8, bold=True)
    sh.text(x0 + 3, y0 + 12.5, sub, TS, color="#333")
    return x0, y0, (x0 + 3, y0 + 16, x0 + CW - 3, y0 + 88)


def mtext(sh, x0, y0, items):
    sh.bullets(x0 + 3, y0 + 94, CW - 6, items, TS, 1.22, 0.6)


@page("M5 a M8 · Dispositivos de anclaje en obra")
def anclaje(num, total):
    sh = Sheet(num, total, "M5-M8 · Anclaje en obra", escalas="puntales y plataforma 1:150 · grouteo 1:50 · herramientas 1:20", fname="M5_M8_Anclaje")
    heading(sh, "3º DISPOSITIVOS DE ANCLAJE · M5 A M8", "Equipos para aplomar, fijar, inyectar y ajustar las uniones durante y después del montaje")
    # M5 puntales
    x0, y0, box = mcell(sh, 0, 0, "M5", "Puntales telescópicos", "Vista 1:150 · arriostre provisorio de columnas")
    p = fitview(sh, box, (-4800, 4800, -1450, 8915), 150)
    p.poly([(-525, -510), (525, -510), (525, -1450), (-525, -1450)], fill=geo.C_FUND, sw=0.12)
    p.rect(-200, -1300, 200, geo.COL_TOP, fill="#cfd3d7", sw=0.2)
    for s in (-1, 1):
        p.poly([(s * 200, 3495), (s * 530, 3495), (s * 530, 3335), (s * 200, 3025)], fill="#cfd3d7", sw=0.12)
        p.line(s * 200, 6200, s * 3800, 0, sw=0.5, stroke=STEEL)
        p.line(s * 2000, 3100, s * 2100, 2950, sw=0.8, stroke=YEL)
        p.rect(s * 3800 - 400, -300, s * 3800 + 400, 0, mat="H", sw=0.1)
    ground(sh, p.P(-4800, 0)[0], p.P(4800, 0)[0], p.P(0, 0)[1])
    p.dim((4600, 0), (4600, 6200), 0, "≈ 2/3 h")
    mtext(sh, x0, y0, ["2 puntales regulables (4-7 m) por columna, a 90° entre sí, anclados a muertos de H° o placas con brocas.",
                       "Se retiran cuando el grout del cáliz alcanza su resistencia (24-48 h)."])
    # M6 plataforma
    x0, y0, box = mcell(sh, 1, 0, "M6", "Plataforma elevadora articulada", "Vista 1:150 · montaje y sellado de fachada")
    e = fitview(sh, box, (-300, 10200, -100, 10800), 150)
    e.rect(0, 400, 2400, 1300, fill=YEL, sw=0.15)
    for x in (400, 2000): e.circle(x, 400, 400, fill="#222", sw=0.08)
    e.rect(600, 1300, 1800, 2100, fill="#777", sw=0.12)
    pts = [(1500, 2000), (3800, 6200), (6000, 4500), (7400, 9200)]
    for a, b in zip(pts, pts[1:]): e.line(*a, *b, sw=1.0, stroke=YEL); e.line(*a, *b, sw=0.15)
    e.rect(7000, 9200, 8400, 10300, fill="none", sw=0.3); e.line(7000, 9700, 8400, 9700, sw=0.12)
    e.rect(9000, 0, 9300, 10800, fill="#bfe3f0", sw=0.15)
    ground(sh, e.P(-300, 0)[0], e.P(10200, 0)[0], e.P(0, 0)[1])
    e.dim((9800, 0), (9800, 10300), -2.0, "≈ 12 m")
    sh.note(e.P(7700, 10000), (x0 + 6, y0 + 22), "canasto 2 personas · 230 kg")
    mtext(sh, x0, y0, ["Brazo articulado de 12 m de trabajo: colocación de vidrios, presores y sellados del muro cortina y juntas de paneles.",
                       "Se alquila sin operador: lo maneja personal capacitado."])
    # M7 grouteo
    x0, y0, box = mcell(sh, 0, 1, "M7", "Equipo de grouteo", "1:50 · mezcladora + bomba + manguera")
    q = fitview(sh, box, (-200, 2950, -200, 1450), 50)
    q.rect(0, 300, 900, 1200, fill="#4a90c2", sw=0.15); q.rect(100, 1200, 800, 1400, fill="#2c5f86", sw=0.12)
    q.rect(0, 0, 1000, 300, fill=DARK, sw=0.12)
    for x in (150, 850): q.circle(x, 0, 150, fill="#222", sw=0.08)
    q.rect(1200, 100, 2300, 700, fill="#d35400", sw=0.15); q.circle(1450, 400, 180, fill="#777", sw=0.1)
    q.pline([(2300, 400), (2500, 400), (2600, 900), (2700, 900)], sw=0.5)
    q.line(900, 800, 1300, 700, sw=0.45)
    q.rect(2700, 600, 2900, 1300, fill="#cfd3d7", sw=0.12)
    ground(sh, q.P(-200, 0)[0], q.P(2950, 0)[0], q.P(0, -150)[1])
    sh.note(q.P(450, 900), (x0 + 6, y0 + 22), "mezcladora de paleta 200 l")
    sh.note(q.P(1750, 650), (x0 + 50, y0 + 30), "bomba de tornillo 2-3 m³/h")
    mtext(sh, x0, y0, ["Inyecta el grout sin retracción en cálices, vainas de pernos y juntas.",
                       "Se inyecta desde abajo hasta que sale por el purgador (sin aire atrapado)."])
    # M8 herramientas
    x0, y0, box = mcell(sh, 1, 1, "M8", "Herramientas de anclaje", "1:20")
    t = sh.view(x0 + 10, y0 + 26, 20)
    t.rect(0, 0, 450, 40, fill="#888", sw=0.12); t.rect(450, -30, 520, 70, fill=DARK, sw=0.1); t.circle(485, 20, 40, fill="none", sw=0.12)
    t.rect(-60, 5, 0, 35, fill="#555", sw=0.08)
    sh.text(x0 + 46, y0 + 26, "llave dinamométrica", TS)
    t2 = sh.view(x0 + 10, y0 + 46, 20)
    t2.rect(0, 0, 300, 150, fill="#2e86c1", sw=0.15); t2.rect(60, -200, 160, 0, fill="#2e86c1", sw=0.12); t2.line(300, 75, 560, 75, sw=0.6)
    sh.text(x0 + 46, y0 + 44, "taladro percutor + broca", TS)
    t3 = sh.view(x0 + 72, y0 + 86, 20)
    for s_ in (-1, 1): t3.line(0, 450, s_ * 220, 0, sw=0.25)
    t3.line(0, 0, 0, 450, sw=0.18)
    t3.rect(-100, 450, 100, 650, fill=YEL, sw=0.12); t3.circle(0, 690, 40, fill="#e74c3c", sw=0.05)
    t3.rect(-1150, 0, -550, 70, fill="#d4ac0d", sw=0.12); t3.circle(-850, 35, 22, fill="#5dade2", sw=0.05)
    sh.text(x0 + 10, y0 + 79, "nivel láser y de burbuja", TS)
    mtext(sh, x0, y0, ["Llave dinamométrica: aprieta bulones M12-M20 al torque de proyecto.",
                       "Taladro + brocas Ø9,5; nivel láser / estación total: replanteo y aplomado ± 5 mm."])
    return sh


PAGES = [moldeo, anclaje]
