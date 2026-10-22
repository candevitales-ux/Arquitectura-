# -*- coding: utf-8 -*-
"""Carátula con índice automático + axonometría del sistema con la lista gráfica de elementos E1…E11."""
import importlib
from lib import Sheet, Iso, page, heading, TB, TS, TT
import geo
from geo import LUZ_X, LUZ_Y, ENT_TT, CUB_TT

ELEM = [
    ("E1", "Fundación tipo cáliz (base + cuello H°A° in situ)"),
    ("E2", "Columna premoldeada pretensada 40x40 c/ ménsulas cortas"),
    ("E3", "Viga VL doble T 40x70 pretensada (fachada)"),
    ("E4", "Viga L de borde premoldeada (s/ VL, recibe el TT)"),
    ("E5", "Viga VP T invertida h 0,75 (portante principal, luz 15 m)"),
    ("E6", "Panel TT h 0,65 x 2,40 (entrepiso y cubierta, luz 10 m)"),
    ("E7", "Capa de compresión H°A° in situ e = 5 cm c/ malla"),
    ("E8", "Apoyos y conectores: neopreno, pernos, grout, riel"),
    ("E9", "Muro cortina stick (cerramiento vidriado)"),
    ("E10", "Panel sándwich premoldeado e = 20 cm (opaco)"),
    ("E11", "Viga portapanel pretensada 20x85 (arranque del panel)"),
]


@page("Carátula e índice")
def caratula(num, total):
    sh = Sheet(num, total, "Carátula e índice", escalas="s/ escala", fname="Caratula_Indice")
    sh.text(12, 30, "PRÁCTICA EN CLASE", 9.0, bold=True)
    sh.text(12, 40, "GRANDES LUCES DE", 5.6, bold=True)
    sh.text(12, 47, "HORMIGÓN PREMOLDEADO", 5.6, bold=True)
    sh.text(12, 54, "Ejercicio de estudio para el 2º parcial · sistema elegido en el TP Hormigón", 2.8, color="#333")
    y = sh.para(12, 64, 186,
                "Sistema: estructura de hormigón premoldeado y pretensado de grandes luces. Columnas 40x40 empotradas en "
                "fundaciones tipo cáliz; vigas portantes VP T invertida (luz 15,00 m) y vigas de fachada VL doble T (luz 10,00 m); "
                "entrepiso y cubierta con paneles TT h 0,65 m y capa de compresión in situ. Cerramientos: muro cortina stick "
                "(fachada vidriada) y panel sándwich premoldeado (fachada opaca). Dos niveles: ±0,00 / +4,50 / cubierta +9,09.", TB, 1.35)
    y += 4
    sh.text(12, y, "CONSIGNA RESUELTA", TT, bold=True); y += 5
    y = sh.bullets(12, y, 186, [
        "1º Elementos constructivos: croquis a escala con medidas, función y especificación técnica.",
        "2º Juntas y uniones enumeradas gráficamente, clasificadas y detalladas a escala.",
        "3º Máquinas y dispositivos de montaje, moldeo y anclaje + planificación del alquiler, armado y acceso a obra.",
        "4º Muro cortina y cerramiento opaco: croquis proporcionados, comparación y justificación."], TB, 1.3, 0.8)
    y += 4
    sh.text(12, y, "ÍNDICE DE LÁMINAS", TT, bold=True); y += 2.5
    import build
    rows = [("Lám.", "Contenido")]
    n = 1
    for m in build.MODS:
        for f in getattr(importlib.import_module(m), "PAGES", []):
            rows.append((f"{n:02d}", f.titulo)); n += 1
    half = (len(rows) + 1) // 2
    sh.table(12, y, [12, 81], [rows[0]] + rows[1:half + 1], size=TS, rowh=4.6)
    sh.table(107, y, [12, 81], [rows[0]] + rows[half + 1:], size=TS, rowh=4.6)
    return sh


@page("Axonometría del sistema · lista gráfica de elementos")
def axonometria(num, total):
    sh = Sheet(num, total, "Sistema · lista gráfica de elementos", escalas="axonometría isométrica 1:250 (longitudes verdaderas s/ ejes)",
               fname="Sistema_Axonometria")
    heading(sh, "1º ELEMENTOS DEL SISTEMA · AXONOMETRÍA", "Isométrica 1:250 · módulo 10,00 x 15,00 m · sin parte de la cubierta y sin vidrios para mostrar el armado")
    S = Iso((1, -1, 1))
    q = {("TT", 0, 0, k, "cub") for k in range(1, 6)} | {("TT", 1, 0, k, "cub") for k in range(0, 6)} | \
        {("TT", 1, 0, k, "ent") for k in range(2, 6)}
    geo.estructura(S, nx=2, ny=1, quitar=q, vl_y=(0,))
    S.box(210, LUZ_X - 210, -30, 7200, ENT_TT, ENT_TT + 50, geo.C_CAPA, sw=0.12)
    x = 0
    while x <= LUZ_X + 1:
        S.box(x - 25, x + 25, -412, -262, -150, 9420, "#8d99a4", sw=0.1); x += 1250
    for z in (40, 3250, 4710, 7750, 9390):
        S.box(-25, LUZ_X + 25, -402, -272, z, z + 50, "#8d99a4", sw=0.1)
    x = LUZ_X + 5
    while x + 2490 <= 2 * LUZ_X:
        S.box(x, x + 2490, -420, -220, -40, 9440, "#cfc8bb", sw=0.14); x += 2500
    S.box(LUZ_X + 5, 2 * LUZ_X - 5, -420, -220, -500, -50, geo.C_VP, sw=0.14)
    S.box(-1500, 2 * LUZ_X + 1500, -1500, LUZ_Y + 1500, -2160, -2150, "#efe9de", sw=0.08)
    sc = 250
    ox, oy = S.fit((40, 34, 172, 170), sc)
    S.draw(sh, ox, oy, sc)
    P = lambda x, y, z: S.P2((x, y, z), ox, oy, sc)
    R = [("E1", (2 * LUZ_X + 1000, 0, -1900), (196, 160)), ("E2", (2 * LUZ_X + 200, LUZ_Y, 2500), (196, 82)),
         ("E3", (5000, -200, ENT_TT - 600), (16, 118)), ("E4", (3000, -200, CUB_TT - 50), (16, 76)),
         ("E5", (2 * LUZ_X + 200, 9000, CUB_TT - 400), (196, 50)), ("E6", (6000, 7000, CUB_TT - 30), (110, 32)),
         ("E7", (5000, 6500, ENT_TT + 50), (140, 32)), ("E8", (LUZ_X + 200, 3000, ENT_TT - 760), (196, 122)),
         ("E9", (2500, -400, 1500), (16, 150)), ("E10", (LUZ_X + 6000, -420, 2500), (110, 178)),
         ("E11", (2 * LUZ_X - 3000, -420, -300), (160, 178))]
    for lab, p3, at in R:
        sh.callout(P(*p3), at, lab, r=3.0)
    y = 186
    sh.text(12, y, "REFERENCIAS · ELEMENTOS DEL SISTEMA", TT, bold=True); y += 7.5
    ys = [y, y]
    for k, (c, t) in enumerate(ELEM):
        col = k // 6
        xx, yy = 12 + col * 96, ys[col]
        sh.ball(xx + 3.5, yy - 0.9, c, r=3.2)
        ys[col] = max(sh.para(xx + 9, yy, 85, t, TB, 1.15) + 2.6, yy + 7.6)
    return sh


PAGES = [caratula, axonometria]
