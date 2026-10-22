# -*- coding: utf-8 -*-
"""Lámina 05 – Enumeración gráfica de juntas y uniones: planta 1:300, corte 1:250 y tabla de clasificación."""
from lib import Sheet, spec, heading, wrap
import geo

JY = "#fff1a8"
JUNTAS = [
    ("J1", "Columna / cáliz", "Húmeda · empotramiento", "Grout sin retracción + llaves de corte; cuñas p/ aplomar", "06"),
    ("J2", "VL / ménsula de columna", "Seca · articulada", "Neopreno 10 mm + 2 pernos Ø20 en vainas c/ grout", "06"),
    ("J3", "VP / ménsula de columna", "Seca · articulada", "Neopreno 10 mm + perno Ø20 en vaina c/ grout", "06"),
    ("J4", "Viga L / VL", "Húmeda · rígida", "Cama de mortero 8 mm + barras Ø12 en vainas c/ grout", "06"),
    ("J5", "Nervio TT / talón VP", "Seca · apoyo simple", "Rebaje (dap) del nervio s/ neopreno 10 mm", "06"),
    ("J6", "Ala TT / talón viga L", "Seca + grout · apoyo", "Neopreno 10 mm + junta 2 cm c/ grout", "06"),
    ("J7", "TT / TT (longitudinal)", "Seca + húmeda", "Llave de corte c/ grout + chapas soldadas c/ 1,50 m", "06"),
    ("J8", "Capa / TT, VP y viga L", "Húmeda · continuidad", "Malla Ø6 c/15 + estribos salientes + barras de negativo", "06"),
    ("J9", "Piso / columna", "Junta de movimiento", "EPS 2 cm + sellador; contrapiso independiente", "07"),
    ("J10", "Muro cortina / viga L", "Seca · regulable", "Grapa galv. regulable + bulón T M12 en riel embutido", "07"),
    ("J11", "Montante / montante", "Junta de dilatación", "Manguito interior 20 mm + sellador (absorbe flechas)", "07"),
    ("J12", "Muro cortina / piso (arranque)", "Seca · deslizante", "Perfil guía de arranque + sellador + babeta", "07"),
    ("J13", "Panel sándwich / VL", "Seca · deslizante", "Bulón pasante M20, agujero ovalado vertical + vaina", "07"),
    ("J14", "Panel / viga portapanel", "Húmeda · apoyo", "Mortero de asiento + pasador Ø16 en vaina c/ grout", "07"),
    ("J15", "Panel / panel", "Junta de movimiento", "Fondo de junta + sellador PU; lana cortafuego en losas", "07"),
]


def jb(sh, x, y, lab):
    sh.ball(x, y, lab, r=2.1, fill=JY)


def make(num, total):
    sh = Sheet(num, total, "Juntas y uniones 1", "Enumeración gráfica y clasificación de cada junta / unión del sistema",
               "Planta 1:300 · corte 1:250")
    heading(sh, "2º JUNTAS Y UNIONES DEL SISTEMA  ·  1/3", "Ubicación de las 15 juntas y uniones detectadas (J1…J15) · detalles en láminas 06 y 07")

    # ============================================================ PLANTA 1:300
    sh.title_drawing(10, 26, "PLANTA ESTRUCTURAL ESQUEMÁTICA (nivel +4,50)", "esc. 1:300 · 3 x 10,00 m (VL / TT) por 2 x 15,00 m (VP)", 2.2)
    S = 300
    v = sh.view(18, 146, S)
    X, Y = 30000, 30000
    # paneles TT
    for i in range(3):
        for j in range(2):
            x0, x1 = i * 10000 + 210, (i + 1) * 10000 - 210
            yy = j * 15000 + (170 if j == 0 else 360)
            while yy + 2400 <= (j + 1) * 15000 - 150:
                v.rect(x0, yy, x1, yy + 2400, fill="#efeadc", sw=0.08); yy += 2410
            v.rect(x0, yy, x1, (j + 1) * 15000 - 360 if j == 0 else (j + 1) * 15000 - 170, fill="#e3dccb", sw=0.08)
    # VP
    for i in range(4):
        v.rect(i * 10000 - 350, 200, i * 10000 + 350, 14800, fill=geo.C_VP, sw=0.15)
        v.rect(i * 10000 - 350, 15200, i * 10000 + 350, 29800, fill=geo.C_VP, sw=0.15)
    # VL + viga L (fachadas frontal y posterior)
    for yv in (-200, Y - 200):
        for i in range(3):
            v.rect(i * 10000 + 210, yv, (i + 1) * 10000 - 210, yv + 400, fill=geo.C_VL, sw=0.15)
    for i in range(4):
        for j in range(3):
            v.rect(i * 10000 - 200, j * 15000 - 200, i * 10000 + 200, j * 15000 + 200, fill="#555", sw=0.15)
    # cerramientos
    v.rect(-350, -432, X + 350, -232, fill="#bfe3f0", sw=0.12)
    for x in range(0, X + 1, 1250): v.line(x, -432, x, -232, sw=0.1)
    v.rect(-420, Y + 220, X + 420, Y + 420, fill="#cfc8bb", sw=0.12)
    for xs in (-420, X + 220):
        v.rect(xs, -232, xs + 200, Y + 220, fill="#cfc8bb", sw=0.12)
    for x in range(0, X + 1, 2500): v.line(x, Y + 220, x, Y + 420, sw=0.1)
    # ejes
    for i, c in enumerate("ABCD"):
        x = i * 10000
        v.line(x, -1600, x, Y + 1200, stroke="#b22", sw=0.08, dash="2 0.6 0.4 0.6")
        v.line(x, -1600, x, -3260, stroke="#b22", sw=0.08)
        sh.circle(*v.P(x, -3800), 1.8, stroke="#b22", sw=0.15); sh.text(v.P(x, 0)[0], v.P(0, -3800)[1] + 0.6, c, 1.6, anchor="middle", color="#b22")
    for j, c in enumerate("123"):
        y = j * 15000
        v.line(-1600, y, X + 1200, y, stroke="#b22", sw=0.08, dash="2 0.6 0.4 0.6")
        sh.circle(*v.P(-2600, y), 1.8, stroke="#b22", sw=0.15); sh.text(v.P(-2600, y)[0], v.P(-2600, y)[1] + 0.6, c, 1.6, anchor="middle", color="#b22")
    v.dim((0, Y + 1000), (10000, Y + 1000), 1.5, "10,00", size=1.4)
    v.dim((10000, Y + 1000), (20000, Y + 1000), 1.5, "10,00", size=1.4)
    v.dim((20000, Y + 1000), (30000, Y + 1000), 1.5, "10,00", size=1.4)
    v.dim((X + 1000, 0), (X + 1000, 15000), -1.5, "15,00", size=1.4)
    v.dim((X + 1000, 15000), (X + 1000, 30000), -1.5, "15,00", size=1.4)
    sh.text(*v.P(15000, -1300), "FACHADA VIDRIADA (muro cortina)", 1.5, anchor="middle", bold=True)
    sh.text(v.P(15000, 0)[0], v.P(0, Y)[1] - 8.5, "FACHADA OPACA (panel sándwich)", 1.5, anchor="middle", bold=True)
    # marcas J
    for lab, (x, y), (dx, dy) in [("J1", (20000, 15000), (5, -5)), ("J2", (10200, 0), (4, -6)), ("J3", (10000, 15200), (-5, 6)),
                                  ("J4", (5000, 0), (0, -5.5)), ("J5", (20350, 7000), (5, 0)), ("J6", (15000, 300), (0, -5)),
                                  ("J7", (5000, 4985), (-0.5, 4.5)), ("J8", (25000, 22000), (0, 0)), ("J9", (10000, 30000), (5, -5)),
                                  ("J10", (2500, -330), (-3, 6)), ("J11", (7500, -330), (3, 6)), ("J13", (25000, Y + 320), (0, -5)),
                                  ("J15", (X + 320, 22500), (-6, 0)), ("J15", (17500, Y + 320), (0, -5))]:
        px, py = v.P(x, y)
        if dx or dy: sh.leader([(px, py), (px + dx * 0.6, py + dy * 0.6)], sw=0.12)
        jb(sh, px + dx, py + dy, lab)

    # ============================================================ CORTE 1:250
    sh.title_drawing(130, 26, "CORTE ESQUEMÁTICO A-A (por eje B, a lo largo de la VP)", "esc. 1:250", 2.2)
    c = sh.view(142, 76, 250)
    c.rect(-1600, -2300, 31600, -150, mat="tierra", stroke=None)
    sh.line(*c.P(-1600, -150), *c.P(31600, -150), sw=0.2)
    c.rect(-200, -177, 30200, 0, fill="#d9d4c8", sw=0.12)
    for xc in (0, 15000, 30000):
        c.poly([(xc - 1000, -2050), (xc + 1000, -2050), (xc + 1000, -1750), (xc + 525, -1450), (xc + 525, -510), (xc - 525, -510),
                (xc - 525, -1450), (xc - 1000, -1750)], fill=geo.C_FUND, sw=0.15)
        c.rect(xc - 200, -1300, xc + 200, geo.COL_TOP, fill="#9aa3ab", sw=0.18)
    for yt in (geo.ENT_TT, geo.CUB_TT):
        for (xa, xb) in ((200, 14800), (15200, 29800)):
            c.rect(xa + 10, yt - 750, xb - 10, yt, fill=geo.C_VP, sw=0.15)
        for xc in (0, 15000, 30000):
            for sd in (-1, 1):
                if (xc == 0 and sd < 0) or (xc == 30000 and sd > 0): continue
                c.poly([(xc + sd * 200, yt - 760), (xc + sd * 550, yt - 760), (xc + sd * 550, yt - 920), (xc + sd * 200, yt - 1230)], fill="#9aa3ab", sw=0.12)
        c.rect(0, yt, 30000, yt + 50, fill="#d9d2c4", sw=0.1)
        for xc in (0, 30000):
            c.poly(geo.perfil_VL(xc - 200, yt - 910), fill=geo.C_VL, sw=0.12)
            c.poly(geo.perfil_L(xc - 200, yt - 210, flip=(xc > 0)), fill=geo.C_L, sw=0.12)
    # cerramientos
    c.rect(-432, -150, -232, 9420, fill="#bfe3f0", sw=0.12)
    c.rect(30220, -40, 30420, 9440, fill="#cfc8bb", sw=0.12)
    c.rect(30220, -500, 30420, -50, fill=geo.C_VP, sw=0.12)
    for yt, t in ((0, "±0,00"), (4500, "+4,50"), (9090, "+9,09")):
        sh.level(*c.P(31400, yt), t, 1.4)
    for lab, (x, z), (dx, dy) in [("J1", (15000, -900), (5, 3)), ("J2", (0, 3495), (6, 3)), ("J3", (15000, 3655), (5, 5)),
                                  ("J4", (0, 4205), (5, -3)), ("J5", (14700, 3815), (-5, -2)), ("J8", (8000, 4440), (0, -5)),
                                  ("J9", (15000, -80), (5, 3)), ("J10", (-332, 4100), (-4, -3)), ("J11", (-332, 4710), (-4, -7)),
                                  ("J12", (-332, -100), (-4, 3)), ("J13", (30320, 8640), (5, 0)), ("J14", (30320, -45), (5, 3)),
                                  ("J15", (30320, 4500), (5, 0))]:
        px, py = c.P(x, z)
        sh.leader([(px, py), (px + dx * 0.6, py + dy * 0.6)], sw=0.12)
        jb(sh, px + dx, py + dy, lab)

    # ============================================================ TABLA
    sh.text(130, 90, "CLASIFICACIÓN DE JUNTAS Y UNIONES", 2.2, bold=True)
    rows = [("N°", "Encuentro", "Tipo", "Resolución", "Lám.")] + JUNTAS
    fills = [None] + [None] * len(JUNTAS)
    sh.table(130, 92, [9, 37, 31, 68, 9], rows, size=1.45, lead=1.15, fills=fills)

    # ============================================================ TEORÍA
    y = 166
    sh.text(10, y, "CRITERIOS (teórica de Juntas y Uniones)", 2.1, bold=True); y += 3.6
    y = sh.bullets(10, y, 114, [
        "UNIÓN: vincula dos piezas transmitiendo esfuerzos (articulada = transmite corte, permite giro; rígida / empotrada = transmite momento).",
        "JUNTA: separa piezas para absorber movimientos (dilatación térmica, retracción, flechas, sismo) manteniendo estanqueidad.",
        "SECA: abulonada, soldada o por apoyo (montaje inmediato, desmontable). HÚMEDA: hormigón, mortero o grout colado en obra (monolítica, requiere fragüe).",
        "En el sistema premoldeado las vigas apoyan articuladas (neopreno) y la estabilidad la dan las columnas empotradas en el cáliz (J1) y el diafragma de la capa (J8).",
    ], size=1.5, lead=1.25, gap=0.6)
    return sh
