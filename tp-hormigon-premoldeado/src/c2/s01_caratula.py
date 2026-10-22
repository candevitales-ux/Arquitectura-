# -*- coding: utf-8 -*-
"""Lámina 01 – Carátula, índice y axonometría del sistema con la lista gráfica de elementos E1…E11."""
from lib import Sheet, Iso
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
    ("E11", "Viga portapanel pretensada 20x85 (arranque panel)"),
]
INDICE = [
    ("01", "Carátula · sistema y lista de elementos"),
    ("02", "Elementos 1 · fundación cáliz y columna"),
    ("03", "Elementos 2 · vigas VL, L de borde y VP"),
    ("04", "Elementos 3 · panel TT, capa y accesorios"),
    ("05", "Juntas y uniones 1 · ubicación y clasificación"),
    ("06", "Juntas y uniones 2 · estructura"),
    ("07", "Juntas y uniones 3 · cerramientos"),
    ("08", "Máquinas 1 · montaje (grúa, transporte, izaje)"),
    ("09", "Máquinas 2 · moldeo y anclaje"),
    ("10", "Máquinas 3 · alquiler, armado y acceso a obra"),
    ("11", "Cerramiento 1 · muro cortina"),
    ("12", "Cerramiento 2 · panel sándwich opaco"),
    ("13", "Cerramiento 3 · comparación y justificación"),
]


def muro_cortina(S, x0, x1, y_ext):
    """montantes 50x150 c/ 1,25 m y travesaños (sin vidrios para dejar ver la estructura)"""
    yb = y_ext - 180
    x = x0
    while x <= x1 + 1:
        S.box(x - 25, x + 25, yb, yb + 150, -150, 9420, "#8d99a4", sw=0.1)
        x += 1250
    for z in (40, 3250, 4710, 7750, 9390):
        S.box(x0 - 25, x1 + 25, yb + 10, yb + 140, z, z + 50, "#8d99a4", sw=0.1)


def paneles(S, x0, x1, y_ext):
    x = x0
    while x + 2490 <= x1 + 5:
        S.box(x, x + 2490, y_ext - 200, y_ext, -40, 9440, "#cfc8bb", sw=0.14)
        x += 2500
    S.box(x0, x1, y_ext - 200, y_ext, -500, -50, geo.C_VP, sw=0.14)     # viga portapanel


def make(num, total):
    sh = Sheet(num, total, "Carátula · sistema premoldeado", "Lista gráfica de elementos e índice de láminas",
               "Axonometría isométrica 1:250 (longitudes verdaderas sobre los ejes)")
    # ---------------------------------------------------------------- título e índice
    sh.text(12, 20, "PRÁCTICA EN CLASE", 6.0, bold=True)
    sh.text(12, 28, "GRANDES LUCES DE HORMIGÓN PREMOLDEADO", 4.0, bold=True)
    sh.text(12, 34, "Ejercicio de estudio para el 2º parcial · sistema elegido en el TP Hormigón", 2.3, color="#333")
    y = sh.para(12, 42, 98,
                "Sistema: estructura de hormigón premoldeado y pretensado de grandes luces. Columnas 40x40 empotradas en "
                "fundaciones tipo cáliz; vigas portantes VP T invertida (luz 15,00 m) y vigas de fachada VL doble T (luz 10,00 m); "
                "entrepiso y cubierta con paneles TT h 0,65 m y capa de compresión in situ. Cerramientos: muro cortina "
                "stick (fachada vidriada) y panel sándwich premoldeado (fachada opaca). 2 niveles: ±0,00 / +4,50 / cubierta +9,09.", 2.05, 1.35)
    y += 3
    sh.text(12, y, "CONSIGNA RESUELTA", 2.6, bold=True); y += 4
    for t in ("1º Elementos constructivos: croquis a escala + medidas, función y especificación técnica (Láms. 02–04).",
              "2º Juntas y uniones enumeradas gráficamente (Láms. 05–07).",
              "3º Dispositivos y máquinas de montaje, moldeo y anclaje + planificación de alquiler, armado y acceso (Láms. 08–10).",
              "4º Muro cortina y cerramiento opaco: croquis proporcionados, comparación y justificación (Láms. 11–13)."):
        y = sh.para(14, y, 96, t, 1.9, 1.3); y += 0.6
    y += 2.5
    sh.text(12, y, "ÍNDICE DE LÁMINAS (A4)", 2.6, bold=True); y += 1.5
    rows = [("Lám.", "Contenido")] + INDICE
    sh.table(12, y, [12, 86], rows, size=1.75, rowh=3.55)
    # ---------------------------------------------------------------- axonometría
    S = Iso((1, -1, 1))
    q = {("TT", 0, 0, k, "cub") for k in range(1, 6)} | {("TT", 1, 0, k, "cub") for k in range(0, 6)} | \
        {("TT", 1, 0, k, "ent") for k in range(2, 6)}
    geo.estructura(S, nx=2, ny=1, quitar=q, vl_y=(0,))
    # capa de compresión en el paño 0 del entrepiso (parcial)
    S.box(210, LUZ_X - 210, -30, 7200, ENT_TT, ENT_TT + 50, geo.C_CAPA, sw=0.12)
    muro_cortina(S, 0, LUZ_X, -200 - 32)
    paneles(S, LUZ_X + 5, 2 * LUZ_X - 5, -220)
    S.box(-1500, 2 * LUZ_X + 1500, -1500, LUZ_Y + 1500, -2160, -2150, "#efe9de", sw=0.08)   # plano de fundación (referencia)
    sc = 250
    ox, oy = S.fit((124, 22, 262, 146), sc)
    S.draw(sh, ox, oy, sc)
    P = lambda x, y, z: S.P2((x, y, z), ox, oy, sc)
    # referencias E1..E11
    R = [("E1", (2 * LUZ_X + 1000, 0, -1900), (284, 140)),
         ("E2", (2 * LUZ_X + 200, LUZ_Y, 2500), (284, 66)),
         ("E3", (5000, -200, ENT_TT - 600), (120, 98)),
         ("E4", (3000, -200, CUB_TT - 50), (120, 60)),
         ("E5", (2 * LUZ_X + 200, 9000, CUB_TT - 400), (284, 40)),
         ("E6", (6000, 7000, CUB_TT - 30), (200, 24)),
         ("E7", (5000, 6500, ENT_TT + 50), (222, 26)),
         ("E8", (LUZ_X + 200, 3000, ENT_TT - 760), (284, 100)),
         ("E9", (2500, -400, 1500), (120, 128)),
         ("E10", (LUZ_X + 6000, -420, 2500), (200, 146)),
         ("E11", (2 * LUZ_X - 3000, -420, -300), (250, 146))]
    for lab, p3, at in R:
        sh.callout(P(*p3), at, lab, r=2.6)
    # leyenda
    x0, y0 = 214, 133
    sh.text(x0 - 90, 150, "REFERENCIAS · ELEMENTOS DEL SISTEMA", 2.2, bold=True)
    yy = 155
    for i, (c, t) in enumerate(ELEM):
        col, row = divmod(i, 6)
        xx = 124 + col * 84; ty = yy + row * 3.3
        sh.text(xx, ty, c, 1.8, bold=True); sh.text(xx + 6, ty, t, 1.7)
    sh.text(124, 177.5, "Isometría sin cubierta parcial ni vidrios para mostrar el armado. Paño izquierdo: muro cortina (E9); paño derecho: panel sándwich (E10).", 1.6, ital=True, color="#333")
    sh.title_drawing(124, 14, "AXONOMETRÍA DEL SISTEMA ESTRUCTURAL", "Isométrica esc. 1:250 · módulo 10,00 x 15,00 m")
    return sh
