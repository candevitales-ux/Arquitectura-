# -*- coding: utf-8 -*-
"""Lámina 02 - Axonometría estructural (isométrica 1:160) con los elementos del sistema y su listado."""
from lib import *
from geom import *

ELEMENTOS = [
    (1, "Base aislada de H°A° con pedestal", "Transmitir las cargas de la columna al suelo", lam("fund")),
    (2, "Pernos de anclaje M20 (4 por columna)", "Fijar la placa base a la fundación", lam("fund")),
    (3, "Placa base 380x250x20 + mortero de nivelación", "Repartir la carga y nivelar la columna", lam("fund")),
    (4, "Columna HEB 200", "Bajar cargas verticales; parte del pórtico", lam("fund")),
    (5, "Viga principal IPN 500 (luz 12,00 m)", "Salvar la gran luz; recibe las secundarias", lam("vigas")),
    (6, "Viga secundaria IPN 200 c/ 2,00 m", "Apoyo de la chapa colaborante (luz 4,00 m)", lam("vigas")),
    (7, "Viga de borde IPN 200", "Borde de losa; anclaje de los cerramientos", lam("vigas")),
    (8, "Placas de corte y angulares de unión", "Vincular vigas entre sí y con columnas", lam("vigas")),
    (9, "Chapa colaborante h = 76 mm, e = 0,9 mm", "Encofrado perdido y armadura inferior", lam("deck")),
    (10, "Conectores de corte (stud Ø19 x 125)", "Hacer trabajar juntos losa y viga", lam("deck2")),
    (11, "Malla Q188 + armadura de negativos", "Retracción, temperatura y continuidad", lam("deck")),
    (12, "Hormigón H-25 (losa e = 140 mm)", "Losa de compresión; diafragma rígido", lam("deck")),
    (13, "Cenefa de borde (chapa galv. e = 1,6)", "Encofrado del borde de la losa", lam("deck2")),
    (14, "Tapas de cierre de nervios", "Evitar fugas de hormigón en extremos", lam("deck2")),
    (15, "Arriostramiento: barra Ø20 + tensor", "Estabilidad lateral (viento / sismo)", lam("arr")),
    (16, "Bulones ISO 8.8 (ASTM A325) M16 / M20", "Uniones abulonadas de obra", lam("arr")),
    (17, "Soldadura (electrodo E7018)", "Uniones de taller y studs", lam("arr")),
    (18, "Fijaciones: clavos de pólvora / autoperforantes", "Fijar y coser la chapa colaborante", lam("fij")),
    (19, "Protección: antióxido + esmalte / intumescente", "Corrosión y resistencia al fuego", lam("fij")),
    (20, "Subestructura de fachada (montantes, portapanel)", "Soporte de cerramientos", lam("cw") + "/" + lam("panel")),
]

if __name__ == "__main__":
    sh = Sheet(NUM["axo"], "Axonometría estructural y elementos del sistema", "PUNTO 1 - ELEMENTOS CONSTRUCTIVOS",
               "Axonometría isométrica 1:190", hmin=2.4)
    y = sh.encabezado("1° ELEMENTOS CONSTRUCTIVOS DEL SISTEMA",
                      "Axonometría estructural del edificio adoptado con la referencia de cada elemento")
    L, R = sh.L + 3, sh.R - 3
    sh.txt("Ejes en rojo. Globos negros: N° de elemento (ver listado).", L, y - 12, 1.8)
    sh.titulo_dib(L, y - 3.5, 1, "AXONOMETRÍA ESTRUCTURAL (ISOMÉTRICA)", "1:190", w=R - L)
    v = IsoView(sh, L + 66, y - 134, 190)

    # fundaciones
    cols = [(x, 0) for x in EJES_X] + [(x, ANCHO) for x in EJES_X] + [(0, 4000), (0, 8000), (LARGO, 4000), (LARGO, 8000)]
    for cx, cy in sorted(cols, key=lambda c: -(c[0] + c[1])):
        v.box(cx - 800, cy - 800, FUND, cx + 800, cy + 800, FUND + BASE_E, lw=13)
        v.box(cx - 250, cy - 250, FUND + BASE_E, cx + 250, cy + 250, -300, lw=13)
    # contorno de PB (proyección del contrapiso)
    v.pl([(0, 0, 0), (LARGO, 0, 0), (LARGO, ANCHO, 0), (0, ANCHO, 0)], "1-OCULTO", 13, True)
    # entrepiso: paño 1-2 con chapa colaborante, paño 2-3 con hormigón
    zf = N1
    v.face([(0, 0, zf), (VANO, 0, zf), (VANO, ANCHO, zf), (0, ANCHO, zf)], 242, 13)
    for k in range(0, int(VANO / 305) + 1):
        xx = 150 + k * 305
        if xx < VANO: v.ln((xx, 0, zf), (xx, ANCHO, zf), "1-VISTA", 9)
    for yy in range(1000, ANCHO, 2000):                      # studs sobre las secundarias
        pass
    for ys in range(0, ANCHO + 1, SEC):
        for xx in range(300, VANO, 600):
            c = v.p(xx, ys, zf); sh.circ(c, 0.35, "1-VISTA", 13)
    v.face([(VANO, 0, zf), (2 * VANO, 0, zf), (2 * VANO, ANCHO, zf), (VANO, ANCHO, zf)], 205, 13)
    v.face([(VANO, 0, zf - LOSA), (2 * VANO, 0, zf - LOSA), (2 * VANO, 0, zf), (VANO, 0, zf)], 150, 13)
    # columnas
    for cx, cy in cols:
        v.ln((cx, cy, -300), (cx, cy, N2), "1-SECCION", 50)
    # vigas
    for nl in (N1, N2):
        for x in EJES_X:
            v.ln((x, 0, nl), (x, ANCHO, nl), "1-SECCION", 50)
        for k in range(7):
            v.ln((0, k * SEC, nl), (LARGO, k * SEC, nl), "1-VISTA", 35 if k in (0, 6) else 18)
    # arriostramientos: laterales (ejes 1 y 6, vano B-C) y contrafrente (eje D, vanos 1-2 y 5-6)
    for nlo, nhi in ((0, N1), (N1, N2)):
        for xe in (0, LARGO):
            v.ln((xe, 4000, nlo), (xe, 8000, nhi), "1-VISTA", 18); v.ln((xe, 8000, nlo), (xe, 4000, nhi), "1-VISTA", 18)
        for x0 in (0, 16000):
            v.ln((x0, ANCHO, nlo), (x0 + VANO, ANCHO, nhi), "1-VISTA", 18); v.ln((x0 + VANO, ANCHO, nlo), (x0, ANCHO, nhi), "1-VISTA", 18)
    # parapeto (montantes de fachada sobre cubierta) esquemático
    for cx, cy in cols:
        v.ln((cx, cy, N2), (cx, cy, CUP), "1-VISTA", 13)
    v.pl([(0, 0, CUP), (LARGO, 0, CUP), (LARGO, ANCHO, CUP), (0, ANCHO, CUP)], "1-VISTA", 13, True)
    # muro cortina sugerido en el frente (vano 3-4)
    for xx in range(8000, 12001, 1500):
        v.ln((xx, -150, 0), (xx, -150, N2), "1-OCULTO", 9)
    # ejes
    for i, x in enumerate(EJES_X):
        a = v.p(x, -2600, FUND); sh.circ(a, 2.3, "1-EJES", 18, color=1); sh.txt(str(i + 1), a[0], a[1], 1.9, TA.MIDDLE_CENTER, "1-EJES", True, color=1)
        sh.pl([v.p(x, -300, FUND), v.p(x, -2000, FUND)], "1-EJES", 9)
    for j, yv in enumerate(EJES_Y):
        a = v.p(-2600, yv, FUND); sh.circ(a, 2.3, "1-EJES", 18, color=1); sh.txt("ABCD"[j], a[0], a[1], 1.9, TA.MIDDLE_CENTER, "1-EJES", True, color=1)
        sh.pl([v.p(-300, yv, FUND), v.p(-2000, yv, FUND)], "1-EJES", 9)
    # referencias
    refs = [(1, (700, 0, FUND + 200), (14, -2)), (2, (0, 0, -300), (-22, -6)), (3, (0, 0, -250), (-22, 0)),
            (4, (0, 0, 1500), (-16, 0)), (5, (0, 8000, N2), (-12, 10)), (6, (12000, 10000, N2), (2, 10)),
            (7, (14000, 0, N2), (10, -6)), (8, (VANO, 0, N1), (8, -16)), (9, (1500, 6000, N1), (-20, 10)),
            (10, (300, 10000, N1), (-16, 6)), (11, (6000, 9000, N1), (-4, 14)), (12, (6000, 3000, N1), (14, -6)),
            (13, (5500, 0, N1 - 70), (24, -8)), (14, (2 * VANO, 300, N1 - 40), (14, -10)),
            (15, (LARGO, 6000, 1900), (12, 0)), (16, (VANO * 4, 0, N1), (12, -8)), (17, (VANO * 3, 0, N2), (10, -6)),
            (19, (VANO * 5, 0, 1500), (12, -4)), (20, (LARGO, 0, 7700), (12, 6)), (18, (2500, 12000, N1), (-14, 10))]
    for n, at, off in refs:
        v.ref(n, at, off)
    a = v.p(12000, -150, 3000); sh.txt(f"muro cortina (lám. {lam('cw')})", a[0] + 3, a[1] - 1, 1.8)
    a = v.p(LARGO, 0, 7700); sh.txt(f"fachadas y parapeto: panel 80 (lám. {lam('panel')})", R, a[1] + 11, 1.8, TA.RIGHT)

    # ------------------------------------------------------------- listado
    yt = y - 160
    sh.titulo_dib(L, yt, 2, "LISTADO DE ELEMENTOS DEL SISTEMA", w=R - L)
    rows = [[str(n), e, f, l] for n, e, f, l in ELEMENTOS]
    half = 10
    wcol = (R - L - 3) / 2
    cols_t = [("N°", 6), ("Elemento", 37), ("Función", wcol - 6 - 37 - 9), ("Lám.", 9)]
    yb = sh.tabla(L + wcol + 3, yt - 5, cols_t, rows[half:], h=1.7, lead=1.3, pad=0.6)
    yb = min(yb, sh.tabla(L, yt - 5, cols_t, rows[:half], h=1.7, lead=1.3, pad=0.6)) - 3
    sh.txt("ESPECIFICACIONES GENERALES", L, yb - 2, 2.0, bold=True)
    sh.para(L, yb - 3.5, R - L, "Perfiles laminados IPN de acero F-24 (ASTM A36, fy = 240 MPa); chapas y placas F-24; bulones ISO 8.8; "
            "barras de anclaje F-24 roscadas; chapa colaborante de acero galvanizado Z275 (fy = 280 MPa); hormigón H-25; malla ADN 420. "
            "Todas las piezas se fabrican, perforan y pintan en taller y se montan en obra con uniones abulonadas (montaje en seco); "
            "en obra solo se suelda el conector de corte y se hormigona la losa.", 1.8, lead=1.45)
    sh.save(f"L{lam('axo')}_Axonometria_elementos")
