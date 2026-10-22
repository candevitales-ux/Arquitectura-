# -*- coding: utf-8 -*-
"""Juntas y uniones: ubicación (planta 1:250 + corte 1:250) y cuadro de clasificación."""
from lib import Sheet, page, heading, TB, TS, TD, TT
import geo

JY = "#fff1a8"
JUNTAS = [
    ("J1", "Columna / cáliz", "Húmeda · empotramiento", "Grout sin retracción + llaves de corte; cuñas p/ aplomar", "11"),
    ("J2", "VL / ménsula de columna", "Seca · articulada", "Neopreno 10 mm + 2 pernos Ø20 en vainas c/ grout", "11"),
    ("J3", "VP / ménsula de columna", "Seca · articulada", "Neopreno 10 mm + perno Ø20 en vaina c/ grout", "11"),
    ("J4", "Viga L / VL", "Húmeda · rígida", "Cama de mortero 8 mm + barras Ø12 en vainas c/ grout", "11"),
    ("J5", "Nervio TT / talón VP", "Seca · apoyo simple", "Rebaje (dap) del nervio s/ neopreno 10 mm", "12"),
    ("J6", "Ala TT / talón viga L", "Seca + grout · apoyo", "Neopreno 10 mm + junta 2 cm c/ grout", "12"),
    ("J7", "TT / TT (longitudinal)", "Seca + húmeda", "Llave de corte c/ grout + chapas soldadas c/ 1,50 m", "12"),
    ("J8", "Capa / TT, VP y viga L", "Húmeda · continuidad", "Malla Ø6 c/15 + estribos salientes + barras de negativo", "12"),
    ("J9", "Piso / columna", "Junta de movimiento", "EPS 2 cm + sellador; contrapiso independiente", "13"),
    ("J10", "Muro cortina / viga L", "Seca · regulable", "Grapa galv. regulable + bulón T M12 en riel embutido", "13"),
    ("J11", "Montante / montante", "Junta de dilatación", "Manguito interior 20 mm + sellador (absorbe flechas)", "13"),
    ("J12", "Muro cortina / piso", "Seca · deslizante", "Perfil guía de arranque + sellador + babeta", "13"),
    ("J13", "Panel sándwich / VL", "Seca · deslizante", "Bulón pasante M20, agujero ovalado vertical + vaina", "14"),
    ("J14", "Panel / viga portapanel", "Húmeda · apoyo", "Mortero de asiento + pasador Ø16 en vaina c/ grout", "14"),
    ("J15", "Panel / panel", "Junta de movimiento", "Fondo de junta + sellador PU; lana cortafuego en losas", "14"),
]


def jb(sh, x, y, lab):
    sh.ball(x, y, lab, r=2.9, fill=JY)


@page("Juntas y uniones · ubicación en planta y corte")
def ubicacion(num, total):
    sh = Sheet(num, total, "Juntas y uniones · ubicación", escalas="planta 1:250 · corte 1:250", fname="Juntas_1_Ubicacion")
    heading(sh, "2º JUNTAS Y UNIONES · UBICACIÓN J1 A J15", "Cada junta / unión detectada se numera en planta y en corte; los detalles a escala están en las láminas 11 a 14")
    sh.title_drawing(12, 32, "PLANTA ESTRUCTURAL (nivel +4,50)", "esc. 1:250 · 3 x 10,00 m (VL / TT) por 2 x 15,00 m (VP)", TT)
    v = sh.view(44, 174, 250)
    X, Y = 30000, 30000
    for i in range(3):
        for j in range(2):
            x0, x1 = i * 10000 + 210, (i + 1) * 10000 - 210
            yy = j * 15000 + (170 if j == 0 else 360)
            while yy + 2400 <= (j + 1) * 15000 - 150:
                v.rect(x0, yy, x1, yy + 2400, fill="#efeadc", sw=0.08); yy += 2410
            v.rect(x0, yy, x1, (j + 1) * 15000 - 360 if j == 0 else (j + 1) * 15000 - 170, fill="#e3dccb", sw=0.08)
    for i in range(4):
        v.rect(i * 10000 - 350, 200, i * 10000 + 350, 14800, fill=geo.C_VP, sw=0.15)
        v.rect(i * 10000 - 350, 15200, i * 10000 + 350, 29800, fill=geo.C_VP, sw=0.15)
    for yv in (-200, Y - 200):
        for i in range(3):
            v.rect(i * 10000 + 210, yv, (i + 1) * 10000 - 210, yv + 400, fill=geo.C_VL, sw=0.15)
    for i in range(4):
        for j in range(3):
            v.rect(i * 10000 - 200, j * 15000 - 200, i * 10000 + 200, j * 15000 + 200, fill="#555", sw=0.15)
    v.rect(-350, -432, X + 350, -232, fill="#bfe3f0", sw=0.12)
    for x in range(0, X + 1, 1250): v.line(x, -432, x, -232, sw=0.1)
    v.rect(-420, Y + 220, X + 420, Y + 420, fill="#cfc8bb", sw=0.12)
    for xs in (-420, X + 220): v.rect(xs, -232, xs + 200, Y + 220, fill="#cfc8bb", sw=0.12)
    for i, c in enumerate("ABCD"):
        x = i * 10000
        v.line(x, -2500, x, Y + 1200, stroke="#b22", sw=0.1, dash="2 0.6 0.4 0.6")
        sh.circle(*v.P(x, -3300), 2.4, stroke="#b22", sw=0.18); sh.text(v.P(x, 0)[0], v.P(0, -3300)[1] + 0.9, c, TS, anchor="middle", color="#b22")
    for j, c in enumerate("123"):
        y = j * 15000
        v.line(-2500, y, X + 1200, y, stroke="#b22", sw=0.1, dash="2 0.6 0.4 0.6")
        sh.circle(*v.P(-3300, y), 2.4, stroke="#b22", sw=0.18); sh.text(v.P(-3300, y)[0], v.P(0, y)[1] + 0.9, c, TS, anchor="middle", color="#b22")
    for k in range(3): v.dim((k * 10000, Y + 1500), ((k + 1) * 10000, Y + 1500), 0, "10,00")
    v.dim((X + 1800, 0), (X + 1800, 15000), 0, "15,00"); v.dim((X + 1800, 15000), (X + 1800, 30000), 0, "15,00")
    sh.text(*v.P(15000, -1500), "FACHADA VIDRIADA (muro cortina)", TS, anchor="middle", bold=True)
    sh.text(v.P(0, 0)[0], v.P(0, Y)[1] - 9.5, "FACHADA OPACA (panel sándwich)", TS, anchor="start", bold=True)
    for lab, (x, y), (dx, dy) in [("J1", (20000, 15000), (6, -6)), ("J2", (10200, 0), (5, -7)), ("J3", (10000, 15200), (-6, 7)),
                                  ("J4", (5000, 0), (0, -7)), ("J5", (20350, 7000), (7, 0)), ("J6", (15000, 300), (0, -7)),
                                  ("J7", (5000, 4985), (0, 6)), ("J8", (25000, 22000), (0, 0)), ("J9", (10000, 30000), (6, 6)),
                                  ("J10", (2500, -330), (-3, 8)), ("J11", (7500, -330), (3, 8)), ("J13", (25000, Y + 320), (0, -7)),
                                  ("J15", (X + 320, 22500), (-7, 0)), ("J15", (17500, Y + 320), (0, -7))]:
        px, py = v.P(x, y)
        if dx or dy: sh.leader([(px, py), (px + dx * 0.6, py + dy * 0.6)], sw=0.15)
        jb(sh, px + dx, py + dy, lab)

    sh.title_drawing(12, 194, "CORTE A-A (por eje B, a lo largo de la VP)", "esc. 1:250", TT)
    c = sh.view(30, 256, 250)
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
    c.rect(-432, -150, -232, 9420, fill="#bfe3f0", sw=0.12)
    c.rect(30220, -40, 30420, 9440, fill="#cfc8bb", sw=0.12)
    c.rect(30220, -500, 30420, -50, fill=geo.C_VP, sw=0.12)
    for yt, t in ((0, "±0,00"), (4500, "+4,50"), (9090, "+9,09")):
        sh.level(*c.P(32500, yt), t)
    for lab, (x, z), (dx, dy) in [("J1", (15000, -900), (6, 4)), ("J2", (0, 3495), (7, 4)), ("J3", (15000, 3655), (6, 6)),
                                  ("J4", (0, 4205), (6, -4)), ("J5", (14700, 3815), (-6, -3)), ("J8", (8000, 4440), (0, -6)),
                                  ("J9", (15000, -80), (-7, 4)), ("J10", (-332, 4100), (-6, -3)), ("J11", (-332, 4710), (-6, -9)),
                                  ("J12", (-332, -100), (-6, 3)), ("J13", (30320, 8640), (6, 0)), ("J14", (30320, -45), (6, 4)),
                                  ("J15", (30320, 4500), (6, 3))]:
        px, py = c.P(x, z)
        sh.leader([(px, py), (px + dx * 0.6, py + dy * 0.6)], sw=0.15)
        jb(sh, px + dx, py + dy, lab)
    return sh


@page("Juntas y uniones · clasificación y criterios")
def clasificacion(num, total):
    sh = Sheet(num, total, "Juntas y uniones · clasificación", escalas="s/ escala", fname="Juntas_2_Clasificacion")
    heading(sh, "2º JUNTAS Y UNIONES · CLASIFICACIÓN", "Tipo de vínculo de cada encuentro entre elementos y cómo se resuelve (numeración de la lámina 09)")
    rows = [("N°", "Encuentro", "Tipo", "Resolución", "Lám.")] + JUNTAS
    y = sh.table(12, 32, [13, 44, 42, 75, 12], rows, size=TB, lead=1.2)
    y += 8
    sh.text(12, y, "CRITERIOS (teórica de Juntas y Uniones)", TT, bold=True); y += 6
    sh.bullets(12, y, 186, [
        "UNIÓN: vincula dos piezas transmitiendo esfuerzos. Articulada = transmite corte y permite el giro; rígida o empotrada = transmite también momento.",
        "JUNTA: separa piezas para absorber movimientos (dilatación térmica, retracción, flechas, sismo) manteniendo la estanqueidad.",
        "SECA: abulonada, soldada o por simple apoyo (montaje inmediato, desmontable). HÚMEDA: hormigón, mortero o grout colado en obra (monolítica, requiere fragüe).",
        "En el sistema premoldeado las vigas apoyan articuladas (neopreno) y la estabilidad la dan las columnas empotradas en el cáliz (J1) y el diafragma de la capa de compresión (J8).",
    ], TB, 1.3, 1.2)
    return sh


PAGES = [ubicacion, clasificacion]
