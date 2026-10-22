# -*- coding: utf-8 -*-
"""Lámina 07 - Juntas y uniones: esquema general sobre el corte transversal y clasificación."""
from lib import *
from geom import *

UNIONES = [
    ("U1", "Columna - fundación", "placa base soldada + 4 pernos M20 + grout", "abulonada + húmeda", "articulada", "taller / obra", "08"),
    ("U2", "Viga principal - columna", "placa de corte soldada al ala + 4 M20", "seca, abulonada", "articulada (corte)", "taller / obra", "08"),
    ("U3", "Viga secundaria - principal", "doble ángulo L76 + 2+2 M16", "seca, abulonada", "articulada", "obra", "08"),
    ("U4", "Losa - viga (conexión de corte)", "studs Ø19 soldados + hormigón", "soldada + húmeda", "rígida (sección compuesta)", "obra", "09"),
    ("U5", "Chapa - chapa y chapa - viga", "solape + autoperforantes / clavos", "seca, mecánica", "diafragma", "obra", "09"),
    ("U6", "Borde de losa - viga de borde", "cenefa fijada + hormigón", "seca + húmeda", "rígida", "obra", "09"),
    ("U7", "Arriostramiento - columna", "cartela soldada + horquilla y pasador", "abulonada (pasador)", "articulada, solo tracción", "taller / obra", "09"),
    ("U8", "Panel sándwich - estructura", "autoperforante + junta machihembrada", "seca + sellado", "junta móvil (dilatación)", "obra", "10"),
    ("U9", "Muro cortina - losa", "grapa regulable + bulón en riel", "seca, regulable", "junta móvil 20 mm por piso", "obra", "10"),
    ("U10", "Cubierta - parapeto", "membrana + babeta + cupertina", "junta de estanqueidad", "junta móvil sellada", "obra", "10"),
]

if __name__ == "__main__":
    sh = Sheet(7, "Juntas y uniones: esquema general y clasificación", "PUNTO 2 - JUNTAS Y UNIONES", "Corte 1:125")
    y0 = sh.encabezado("2° JUNTAS Y UNIONES DEL SISTEMA",
                       "Ubicación de cada encuentro entre elementos (U1 a U10) y su clasificación")
    L, R = sh.L + 3, sh.R - 3
    Y1 = y0 - 3.5
    sh.titulo_dib(L, Y1, 1, "CORTE TRANSVERSAL CON LAS UNIONES", "1:125", w=118)
    v = sh.view_in((L, Y1 - 92, L + 118, Y1 - 8), (-1700, -1700, 13000, 8300), 125)
    # suelo, fundaciones, contrapiso
    v.ln((-1500, -150), (ANCHO + 1000, -150), "1-VISTA", 25)
    v.hatch([(-1500, -150), (ANCHO + 1000, -150), (ANCHO + 1000, -1650), (-1500, -1650)], "tierra")
    for cy in (0, ANCHO):
        base = [(cy - 700, FUND), (cy + 700, FUND), (cy + 700, FUND + 400), (cy + 250, FUND + 400), (cy + 250, -330),
                (cy - 250, -330), (cy - 250, FUND + 400), (cy - 700, FUND + 400)]
        v.hatch(base, "gris"); v.pl(base, "1-SECCION", 35, True)
        v.rect(cy - 225, -300, cy + 225, -278, "1-SECCION", 25)
    v.hatch([(0, -150), (ANCHO, -150), (ANCHO, 0), (0, 0)], "hormigon"); v.rect(0, -150, ANCHO, 0, "1-SECCION", 25)
    # arriostramiento del fondo (eje 6, vano B-C) en línea fina
    for zl, zh in ((0, N1 - LOSA - 500), (N1, N2 - LOSA - 500)):
        v.ln((4150, zl + 200), (7850, zh), "1-OCULTO", 9); v.ln((7850, zl + 200), (4150, zh), "1-OCULTO", 9)
    for cy in (4000, 8000): v.rect(cy - 62, -300, cy + 62, N2 - LOSA, "1-OCULTO", 9)
    # columnas, vigas y losas
    for cy in (0, ANCHO): ipn_vertical(v, COL, cy, -278, N2 - LOSA, False, 25)
    for nl in (N1, N2):
        ipn_lateral(v, VP, 160, ANCHO - 160, nl - LOSA, 25)
        v.rect(-60, nl - LOSA, ANCHO + 60, nl, "1-SECCION", 25)
        v.hatch([(-60, nl - LOSA), (ANCHO + 60, nl - LOSA), (ANCHO + 60, nl), (-60, nl)], "hormigon")
        for k in range(7):
            p = xf(ipn_poly(*IPN[VS]), k * SEC, nl - LOSA - 100); v.pl(p, "1-SECCION", 13, True); v.hatch(p, "negro")
    # muro cortina (frente A) y panel (contrafrente D)
    for x in (-230, -180): v.ln((x, -150), (x, N2 + 600), "1-VISTA", 18)
    for z in range(0, int(N2), 1250): v.ln((-230, z), (-180, z), "1-VISTA", 13)
    v.rect(ANCHO + 150, -150, ANCHO + 230, CUP, "1-VISTA", 25)
    v.hatch([(ANCHO + 150, -150), (ANCHO + 230, -150), (ANCHO + 230, CUP), (ANCHO + 150, CUP)], "gris")
    v.rect(-260, N2 + 600, ANCHO + 260, CUP, "1-VISTA", 18) if False else None
    v.pl([(-280, CUP - 60), (-280, CUP), (60, CUP), (60, N2)], "1-VISTA", 25)
    v.pl([(ANCHO - 60, N2), (ANCHO - 60, CUP), (ANCHO + 280, CUP), (ANCHO + 280, CUP - 60)], "1-VISTA", 25)
    v.nivel(ANCHO + 700, N2, "+7,40"); v.nivel(ANCHO + 700, N1, "+3,80"); v.nivel(ANCHO + 700, 0, "±0,00")
    v.nivel(ANCHO + 700, CUP, "+8,00")
    # marcas de uniones
    marcas = [(1, (0, -290), (-12, -6)), (2, (ANCHO - 160, N1 - LOSA - 250), (-12, -10)), (3, (6000, N1 - LOSA - 100), (4, -12)),
              (4, (3000, N1 - LOSA), (0, 9)), (5, (9000, N2), (0, 7)), (6, (-60, N1 - 70), (-11, 7)),
              (7, (4150, 200), (6, 10)), (8, (ANCHO + 190, 2500), (11, 0)), (9, (-205, N1 - 70), (-12, -5)),
              (10, (ANCHO + 100, CUP), (8, 6))]
    for n, at, off in marcas:
        marca_u(sh, n, v.p(*at), off)
    v.label("frente A: muro cortina", -300, 4800, 1.5, TA.RIGHT)
    v.label("D: panel 80", ANCHO + 300, 5600, 1.5)
    v.label("en el fondo: cruz eje 6", 6000, 2900, 1.4, TA.MIDDLE_CENTER)

    # teoría
    xt = L + 122
    sh.titulo_dib(xt, Y1, "T", "CONCEPTOS", w=R - xt)
    ficha_spec(sh, xt, Y1 - 6, R - xt, [
        ("Unión:", "vínculo que transmite esfuerzos entre dos elementos (vigas, columnas, losa)."),
        ("Junta:", "encuentro con separación que absorbe movimientos (térmicos, cargas, montaje) y debe ser estanca."),
        ("Seca:", "se arma sin agua: bulones, tornillos, clavos, encastres; desmontable y rápida."),
        ("Húmeda:", "con hormigón, grout o mortero: monolítica, necesita fragüe."),
        ("Soldada:", "continuidad del material; en taller (controlada) o en obra (studs)."),
        ("Articulada:", "transmite corte, gira libre; la estabilidad la dan los arriostramientos."),
        ("Rígida:", "transmite corte y momento (empotramiento)."),
        ("Dilatación:", "el edificio mide 20 m (< 40 m): no lleva junta estructural; los cerramientos sí tienen juntas móviles."),
    ], h=1.6, lead=1.36)

    # tabla
    yt = Y1 - 98
    sh.titulo_dib(L, yt, 2, "CLASIFICACIÓN DE LAS JUNTAS Y UNIONES", w=R - L)
    cols = [("N°", 9), ("Encuentro", 30), ("Medio de unión", 42), ("Tipo", 28), ("Vínculo / movimiento", 34), ("Taller / obra", 18), ("Lám.", R - L - 161)]
    sh.tabla(L, yt - 5, cols, [list(u) for u in UNIONES], h=1.65, lead=1.3, pad=0.6)
    sh.save("L07_Esquema_uniones")
