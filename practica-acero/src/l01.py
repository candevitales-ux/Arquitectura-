# -*- coding: utf-8 -*-
"""Lámina 01 - Sistema adoptado: memoria, planta estructural 1:200, corte transversal 1:125, índice."""
from lib import *
from geom import *

sh = Sheet(NUM["sistema"], "Sistema adoptado: memoria, planta y corte", "SISTEMA DEL TP6 ACERO",
           "Planta 1:200 - Corte 1:125")
y = sh.encabezado("SISTEMA ESTRUCTURAL ADOPTADO - TP6 ACERO",
                  "Estructura metálica de grandes luces con entrepiso y cubierta de losa colaborante (steel deck)")
L, R = sh.L + 3, sh.R - 3

# ------------------------------------------------------------------ memoria
sh.titulo_dib(L, y - 3.5, "M", "MEMORIA DESCRIPTIVA", w=R - L)
yy = y - 9
mem = [
    ("Edificio: ", "planta libre rectangular de 20,00 x 12,00 m, dos niveles (entrepiso +3,80 y cubierta +7,40), cupertina +8,00. Uso: oficinas / comercio."),
    ("Grandes luces: ", "pórticos transversales cada 4,00 m que salvan 12,00 m sin apoyos intermedios. Viga principal IPN 500 de alma llena, trabajando en sección compuesta con la losa (conectores de corte)."),
    ("Columnas: ", "HEB 200 (alas paralelas) sobre bases aisladas de H°A° de 1,60 x 1,60 m, con placa base 380 x 250 x 20 y 4 pernos de anclaje M20. Columnas de fachada en los lados cortos (ejes B y C)."),
    ("Entrepiso y cubierta: ", "vigas secundarias IPN 200 cada 2,00 m (luz 4,00 m) y losa colaborante: chapa de acero galvanizado trapezoidal h = 76 mm + hormigón H-25, e total = 140 mm, malla Q188."),
    ("Estabilidad: ", "uniones viga-columna abulonadas; cruces de San Andrés (barras Ø20 con tensor) en laterales y contrafrente; la losa actúa como diafragma rígido horizontal."),
    ("Cerramientos: ", "frente (eje A) muro cortina de aluminio tipo stick con DVH; laterales y contrafrente con panel sándwich metálico PUR 80 mm (integral opaco)."),
]
yy = sh.bullets(L, yy, R - L, mem, h=2.0, lead=1.45, gap=0.4)

# ------------------------------------------------------------------ planta 1:200
yp = yy - 5
sh.titulo_dib(L, yp, 1, "PLANTA ESTRUCTURAL DE ENTREPISO (+3,80)", "1:200", w=128)
v = sh.view(L + 18, yp - 76, 200)
# ejes
for i, x in enumerate(EJES_X):
    v.eje((x, -1600), (x, ANCHO + 1200), str(i + 1), at_end=False)
for j, yv in enumerate(EJES_Y):
    v.eje((LARGO + 1200, yv), (-1400, yv), "ABCD"[j], at_end=True)
# vigas principales (pórticos) en los ejes 1..6
for x in EJES_X:
    v.ln((x, 0), (x, ANCHO), "1-SECCION", 60)
# vigas de borde y secundarias
for k in range(0, 7):
    yv = k * SEC
    v.ln((0, yv), (LARGO, yv), "1-VISTA", 35 if k in (0, 6) else 18)
# columnas
cols = [(x, 0) for x in EJES_X] + [(x, ANCHO) for x in EJES_X] + [(0, 4000), (0, 8000), (LARGO, 4000), (LARGO, 8000)]
for (cx, cy) in cols:
    rot = 0 if cy in (0, ANCHO) else 90           # alma en el plano del pórtico; columnas de fachada corta giradas
    pts = xf(perfil_poly(COL), cx, cy, rot)
    v.pl(pts, "1-SECCION", 25, True); v.hatch(pts, "negro")
# chapa colaborante: un paño con la dirección de los nervios
v.pl([(4000, 2000), (8000, 2000), (8000, 8000), (4000, 8000)], "1-OCULTO", 13, True)
v.ln((4000, 2000), (8000, 8000), "1-OCULTO", 13)
for yy2 in range(2300, 8000, 600):
    pass
pa, pb = v.p(6000, 2400), v.p(6000, 7600)
sh.pl([pa, pb], "3-TEXTOS", 18)
for p, d in ((pa, 1), (pb, -1)):
    sh.pl([(p[0] - 0.9, p[1] + d * 2), p, (p[0] + 0.9, p[1] + d * 2)], "3-TEXTOS", 18)
v.label("nervios", 6400, 5300, 1.8); v.label("chapa", 6400, 4500, 1.8)
# referencias
v.ref("VP", (12000, 7000), (9, 0)) if False else None
# cotas
v.dim((0, ANCHO), (LARGO, ANCHO), 9)
for i in range(5):
    v.dim((EJES_X[i], ANCHO), (EJES_X[i + 1], ANCHO), 4)
v.dim((0, 0), (0, ANCHO), -15)
for k in range(6):
    v.dim((LARGO, k * SEC), (LARGO, (k + 1) * SEC), 9)
# leyenda
lx, ly = L + 136, yp - 10
sh.txt("REFERENCIAS", lx, yp - 1, 2.2, bold=True)
items = [("1-SECCION", 60, "Viga ppal. IPN 500 (luz 12 m)"), ("1-VISTA", 35, "Viga de borde IPN 200"),
         ("1-VISTA", 18, "Viga sec. IPN 200 c/ 2,00 m"), ("1-OCULTO", 13, "Paño de chapa colaborante")]
for i, (lay, lw, s) in enumerate(items):
    yl = ly - i * 4.4
    sh.pl([(lx, yl), (lx + 8, yl)], lay, lw); sh.txt(s, lx + 10, yl - 0.9, 1.9)
ly2 = ly - 4 * 4.4
sh.solid([(lx + 2.7, ly2 - 1), (lx + 5.3, ly2 - 1), (lx + 5.3, ly2 + 1), (lx + 2.7, ly2 + 1)], 60)
sh.txt("Columna HEB 200", lx + 10, ly2 - 0.9, 1.9)
sh.txt("Flecha: nervios de la chapa", lx, ly2 - 6, 1.9); sh.txt("en sentido A-D (luz 2,00 m)", lx, ly2 - 9.4, 1.9)

# ------------------------------------------------------------------ corte transversal 1:125
yc = yp - 94
sh.titulo_dib(L, yc, 2, "CORTE TRANSVERSAL POR PÓRTICO (EJE 3)", "1:125", w=R - L)
v = sh.view(L + 38, yc - 12 - 8000 / 125, 125)
# terreno y fundaciones
v.ln((-2200, PB - 150), (ANCHO + 2200, PB - 150), "1-VISTA", 25)
v.hatch([(-2200, -150), (ANCHO + 2200, -150), (ANCHO + 2200, -1650), (-2200, -1650)], "tierra")
for cy in (0, ANCHO):
    base = [(cy - 800, FUND), (cy + 800, FUND), (cy + 800, FUND + BASE_E), (cy + 250, FUND + BASE_E), (cy + 250, -300), (cy - 250, -300), (cy - 250, FUND + BASE_E), (cy - 800, FUND + BASE_E)]
    v.hatch(base, "gris"); v.pl(base, "1-SECCION", 35, True)
# contrapiso PB
v.hatch([(0, -150), (ANCHO, -150), (ANCHO, 0), (0, 0)], "hormigon"); v.rect(0, -150, ANCHO, 0, "1-SECCION", 25)
# columnas (se ve el alma: ancho 300)
for cy in (0, ANCHO):
    ipn_vertical(v, COL, cy, -300, N2 - LOSA, False, 25)
# vigas principales IPN 500 y losas
for nl in (N1, N2):
    ipn_lateral(v, VP, 150, ANCHO - 150, nl - LOSA, 25)
    v.rect(-150, nl - LOSA, ANCHO + 150, nl, "1-SECCION", 25); v.hatch([(-150, nl - LOSA), (ANCHO + 150, nl - LOSA), (ANCHO + 150, nl), (-150, nl)], "hormigon")
    for k in range(0, 7):
        yy3 = k * SEC
        p = xf(perfil_poly(VS), yy3, nl - LOSA - 100)
        v.pl(p, "1-SECCION", 18, True); v.hatch(p, "negro")
# parapeto, cerramientos
v.rect(-200, N2, -120, CUP, "1-VISTA", 25); v.rect(ANCHO + 120, N2, ANCHO + 200, CUP, "1-VISTA", 25)
v.hatch([(-200, N2), (-120, N2), (-120, CUP), (-200, CUP)], "gris"); v.hatch([(ANCHO + 120, N2), (ANCHO + 200, N2), (ANCHO + 200, CUP), (ANCHO + 120, CUP)], "gris")
# frente: CW (eje A) - línea doble
for x in (-260, -200):
    v.ln((x, 0), (x, N2), "1-VISTA", 18)
# contrafrente: panel con ventana
v.rect(ANCHO + 120, 0, ANCHO + 200, N2, "1-VISTA", 25)
v.hatch([(ANCHO + 120, 0), (ANCHO + 200, 0), (ANCHO + 200, N2), (ANCHO + 120, N2)], "gris")
# arriostramiento visto en el fondo (lateral eje 6, vano B-C): no se ve en este corte
# niveles
v.nivel(ANCHO + 900, CUP, "+8,00 cupertina")
v.nivel(ANCHO + 900, N2, "+7,40 losa cubierta")
v.nivel(ANCHO + 900, N1, "+3,80 losa entrepiso")
v.nivel(ANCHO + 900, PB, "±0,00 NPT")
v.nivel(ANCHO + 900, FUND, "-1,50 fondo base")
# cotas
v.dim((0, N2 + 700), (ANCHO, N2 + 700), 3)
v.dim((-700, PB), (-700, N1), -6); v.dim((-700, N1), (-700, N2), -6); v.dim((-700, N2), (-700, CUP), -6)
# rótulos
px, py = v.p(-260, 2500); sh.txt("CW", px - 1, py, 1.9, TA.RIGHT, rot=0)
px, py = v.p(-260, 2000); sh.txt("frente A", px - 1, py, 1.9, TA.RIGHT)
px, py = v.p(ANCHO + 200, 2500); sh.txt("panel 80", px + 1, py + 6, 1.9)
labs = [("Viga principal IPN 500 - luz 12,00 m", (6000, N1 - 390), (0, 4)), ("Losa colaborante e = 140", (3000, N2 - 70), (0, 6)),
        ("Viga sec. IPN 200 c/ 2,00", (8000, N1 - 240), (2, -7)), ("Columna HEB 200", (ANCHO, 5600), (-28, 0)),
        ("Base aislada H°A° 1,60 x 1,60 + pedestal", (ANCHO - 800, FUND + 200), (-30, 0))]
for s, at, off in labs:
    pa = v.p(*at); c = (pa[0] + off[0], pa[1] + off[1])
    sh.pl([pa, c], "3-REFS", 13)
    sh.txt(s, c[0] + (0.6 if off[0] >= 0 else -0.6), c[1] + 0.5, 1.8, TA.LEFT if off[0] >= 0 else TA.RIGHT)
# ------------------------------------------------------------------ índice (sin carátula)
yi = yc - 12 - 8000 / 125 - 1650 / 125 - 3
sh.titulo_dib(L, yi, "i", "ÍNDICE DE LÁMINAS", w=R - L)
rows = [[f"{n:02d}", t, p] for n, t, p in LAMINAS]
wt = (R - L - 4) / 2
cols = [("N°", 8), ("Contenido", wt - 8 - 12), ("Punto", 12)]
sh.tabla(L, yi - 5, cols, rows[:8], h=2.0, lead=1.3, pad=0.25)
sh.tabla(L + wt + 4, yi - 5, cols, rows[8:], h=2.0, lead=1.3, pad=0.25)
sh.save(f"L{lam('sistema')}_Sistema_adoptado")
