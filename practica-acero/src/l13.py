# -*- coding: utf-8 -*-
"""Lámina 13 - Muro exterior vidriado: muro cortina stick (elevación 1:100, corte vertical 1:20, corte horizontal 1:2,5)."""
from lib import *
from geom import *

sh = Sheet(13, "Muro exterior vidriado: muro cortina (CW) tipo stick", "PUNTO 4 - MURO EXTERIOR", "1:100 - 1:20 - 1:2,5")
y0 = sh.encabezado("4° MURO EXTERIOR VIDRIADO: MURO CORTINA (CW)",
                   "Sistema stick de aluminio (montantes + travesaños armados en obra) colgado de las losas - frente A")
L, R = sh.L + 3, sh.R - 3
Y1 = y0 - 3.5
MOD = 1000                                       # módulo horizontal (4 por vano de 4,00 m)
SPN = 900                                        # spandrel frente a cada losa

# =============================================================== 1. ELEVACIÓN
sh.titulo_dib(L, Y1, 1, "ELEVACIÓN PARCIAL (EJES 1 A 3)", "1:100", w=86)
v = sh.view_in((L, Y1 - 100, L + 86, Y1 - 8), (-500, -900, 8100, 8300), 100)
v.ln((-700, 0), (8300, 0), "1-VISTA", 35)
for nl in (N1, N2):
    v.hatch([(0, nl - LOSA - 500 - 260), (8000, nl - LOSA - 500 - 260), (8000, nl - LOSA - 500 - 260 + SPN), (0, nl - LOSA - 500 - 260 + SPN)], "gris")
for x in range(0, 8001, MOD):
    v.ln((x, 0), (x, N2 + 300), "1-VISTA", 25 if x % VANO else 35)
for z in (0, N1 - LOSA - 760, N1 - LOSA - 760 + SPN, N2 - LOSA - 760, N2 - LOSA - 760 + SPN, N2 + 300):
    v.ln((0, z), (8000, z), "1-VISTA", 25)
v.rect(0, N2 + 300, 8000, CUP, "1-VISTA", 18); v.hatch([(0, N2 + 300), (8000, N2 + 300), (8000, CUP), (0, CUP)], "aislacion")
for i, x in enumerate((0, 4000, 8000)): v.eje((x, -800), (x, -300), str(i + 1), at_end=False) if False else None
v.dim((0, -300), (MOD, -300), -3); v.dim((MOD, -300), (VANO, -300), -3)
v.dim((8000, N1 - LOSA - 760), (8000, N1 - LOSA - 760 + SPN), 4)
v.nivel(-200, N1, "+3,80", -1); v.nivel(-200, N2, "+7,40", -1); v.nivel(-200, 0, "±0,00", -1)
v.ley("spandrel (opaco)", (1500, N1 - LOSA - 500), (0, 8), 1.4)
v.ley("visión DVH", (2500, 1800), (0, 6), 1.4)
v.ley("parapeto panel 80", (5500, CUP - 300), (2, 5), 1.4)

# =============================================================== 2. CORTE VERTICAL POR LOSA 1:20
xc = L + 90
sh.titulo_dib(xc, Y1, 2, "CORTE VERTICAL POR LOSA", "1:20", w=R - xc)
v = sh.view_in((xc, Y1 - 100, R, Y1 - 8), (-700, -1300, 550, 450), 20)
zt = 0                                            # sup. losa entrepiso (+3,80) como origen
v.hatch([(-700, -LOSA), (-60, -LOSA), (-60, 0), (-700, 0)], "hormigon"); v.rect(-700, -LOSA, -60, 0, "1-SECCION", 35)
v.pl([(-60, 0), (-63, 0), (-63, -LOSA - 15), (-150, -LOSA - 15)], "1-SECCION", 25)
v.rect(-145, -LOSA - 200, -55, -LOSA, "1-VISTA", 18)
v.rect(-700, 0, -200, 30, "1-VISTA", 13)
v.pl([(-700, -LOSA - 600), (-120, -LOSA - 600), (-120, -LOSA - 400)], "1-OCULTO", 13)   # cielorraso
MX0 = 60                                           # cara interior del montante
v.rect(MX0, -1300, MX0 + 150, 450, "1-VISTA", 25)                                     # montante (vista)
v.ln((MX0, -200), (MX0 + 150, -200), "1-SECCION", 25)                               # junta de empalme
gz = [(-45, -100), (50, -100), (50, 0), (40, 0), (40, -90), (-45, -90)]
v.pl(gz, "1-SECCION", 25, True); v.hatch(gz, "acero")
z_s0, z_s1 = -LOSA - 760, -LOSA - 760 + SPN
for zz in (z_s0, z_s1):
    v.rect(MX0, zz - 60, MX0 + 150 + 30, zz, "1-SECCION", 35); v.hatch([(MX0, zz - 60), (MX0 + 180, zz - 60), (MX0 + 180, zz), (MX0, zz)], "gris")
v.rect(MX0 + 150 + 30, -1300, MX0 + 150 + 55, z_s0 - 60, "1-SECCION", 25); v.hatch([(MX0 + 180, -1300), (MX0 + 205, -1300), (MX0 + 205, z_s0 - 60), (MX0 + 180, z_s0 - 60)], "vidrio")
v.rect(MX0 + 150 + 30, z_s1, MX0 + 150 + 55, 450, "1-SECCION", 25); v.hatch([(MX0 + 180, z_s1), (MX0 + 205, z_s1), (MX0 + 205, 450), (MX0 + 180, 450)], "vidrio")
v.rect(MX0 + 185, z_s0, MX0 + 191, z_s1 - 60, "1-SECCION", 25); v.hatch([(MX0 + 185, z_s0), (MX0 + 191, z_s0), (MX0 + 191, z_s1 - 60), (MX0 + 185, z_s1 - 60)], "negro")
v.rect(MX0 + 100, z_s0, MX0 + 150, z_s1 - 60, "1-VISTA", 13); v.hatch([(MX0 + 100, z_s0), (MX0 + 150, z_s0), (MX0 + 150, z_s1 - 60), (MX0 + 100, z_s1 - 60)], "lana")
v.hatch([(-60, -LOSA), (MX0, -LOSA), (MX0, 0), (-60, 0)], "lana"); v.ln((-60, 0), (MX0, 0), "1-SECCION", 25)
v.ley("montante 50x150 (1)", (MX0 + 75, 300), (6, 4), 1.4)
v.ley("travesaño 50x120 (2)", (MX0 + 90, z_s1 - 30), (12, 6), 1.4)
v.ley("DVH 6+12+3+3 (6)", (MX0 + 192, 200), (4, -2), 1.4)
v.ley("spandrel templado 6 esmaltado (7)", (MX0 + 188, z_s0 + 300), (4, 4), 1.4)
v.ley("lana mineral 50 + bandeja (7)", (MX0 + 125, z_s0 + 200), (14, -12), 1.4)
v.ley("grapa regulable (8)", (0, -95), (-8, 10), 1.4)
v.ley("junta 20 + manguito (10)", (MX0 + 150, -200), (8, -4), 1.4)
v.ley("cortafuego sellado (12)", (0, -60), (-12, -16), 1.4)
v.ley("losa colaborante", (-500, -70), (-2, 14), 1.4)
v.ley("viga de borde", (-100, -LOSA - 150), (-6, -8), 1.4)

# =============================================================== 3. CORTE HORIZONTAL POR MONTANTE 1:2,5
Y2 = Y1 - 108
sh.titulo_dib(L, Y2, 3, "CORTE HORIZONTAL POR MONTANTE", "1:2,5", w=86)
v = sh.view_in((L, Y2 - 107, L + 86, Y2 - 8), (-100, -40, 100, 205), 2.5)
# montante tubular 50 x 150 con canal
mp = [(-25, 0), (25, 0), (25, 150), (-25, 150)]
v.pl(mp, "1-SECCION", 35, True)
v.pl([(-22.5, 2.5), (22.5, 2.5), (22.5, 147.5), (-22.5, 147.5)], "1-SECCION", 18, True)
v.hatch(mp, "negro", holes=[[(-22.5, 2.5), (22.5, 2.5), (22.5, 147.5), (-22.5, 147.5)]])
v.rect(-6, 150, 6, 168, "1-SECCION", 18); v.hatch([(-6, 150), (6, 150), (6, 168), (-6, 168)], "gris")        # aislador RPT
v.rect(-25, 168, 25, 176, "1-SECCION", 25); v.hatch([(-25, 168), (25, 168), (25, 176), (-25, 176)], "negro")  # presor
v.pl([(-25, 176), (-25, 190), (25, 190), (25, 176)], "1-SECCION", 25)                                      # tapa
bulon(v, (0, 182), (0, 135), 6, cab=4, tuerca=False, lw=13)
for sgn in (-1, 1):
    x0, x1 = sgn * 12, sgn * 100
    for (a, b_, k) in ((150, 156, "vidrio"), (156, 162, "aire"), (162, 168, "vidrio")):
        pass
    v.rect(min(x0, x1), 150 + 2, max(x0, x1), 150 + 8, "1-SECCION", 18); v.hatch([(x0, 152), (x1, 152), (x1, 158), (x0, 158)], "vidrio")
    v.rect(min(x0, x1), 170 - 0, max(x0, x1), 176, "1-SECCION", 18); v.hatch([(x0, 170), (x1, 170), (x1, 176), (x0, 176)], "vidrio")
    v.rect(min(sgn * 14, sgn * 26), 158, max(sgn * 14, sgn * 26), 170, "1-VISTA", 13); v.hatch([(sgn * 14, 158), (sgn * 26, 158), (sgn * 26, 170), (sgn * 14, 170)], "gris")
    v.rect(min(sgn * 26, sgn * 34), 146, max(sgn * 26, sgn * 34), 152, "1-VISTA", 13); v.hatch([(sgn * 26, 146), (sgn * 34, 146), (sgn * 34, 152), (sgn * 26, 152)], "negro")
    v.rect(min(sgn * 18, sgn * 26), 176, max(sgn * 18, sgn * 26), 181, "1-VISTA", 13); v.hatch([(sgn * 18, 176), (sgn * 26, 176), (sgn * 26, 181), (sgn * 18, 181)], "negro")
v.dim((-25, 0), (25, 0), -4); v.dim((25, 0), (25, 150), 6)
v.dim((-100, 152), (-100, 176), -4, txt="24,8")
v.ley("montante alum. 6063-T6 e = 2,5 (1)", (-22, 60), (-2, 14), 1.4)
v.ley("RPT (13)", (6, 160), (12, -14), 1.4)
v.ley("presor + tornillo inox (3)", (20, 172), (16, -2), 1.4)
v.ley("tapa a presión (4)", (20, 190), (14, 6), 1.4)
v.ley("burlete EPDM (5)", (30, 149), (16, -18), 1.4)
v.ley("separador c/ desecante + silicona", (-20, 164), (-8, 10), 1.4)
v.ley("templado 6 ext. / laminado 3+3 int.", (-90, 176), (0, 8), 1.4)
v.label("EXTERIOR", 60, 200, 1.4, TA.MIDDLE_CENTER, True); v.label("INTERIOR", 60, -30, 1.4, TA.MIDDLE_CENTER, True)

# =============================================================== 4. ESPECIFICACIÓN
xs = L + 90
sh.titulo_dib(xs, Y2, 4, "ELEMENTOS DEL SISTEMA", w=R - xs)
filas = [["1", "Montante", "alum. 6063-T6, 50x150, c/ 1,00 m, colgado de cada losa"],
         ["2", "Travesaño", "alum. 50x120, a +0,90 (spandrel) y en cada losa"],
         ["3/4", "Presor y tapa", "alum. extruido; tornillo inox c/ 250; anodizado"],
         ["5", "Burletes", "EPDM; drenaje y ventilación por travesaños"],
         ["6", "DVH visión", "6 templado + 12 aire + 3+3 laminado PVB; U ≈ 2,8"],
         ["7", "Spandrel", "templado 6 esmaltado + lana mineral 50 + bandeja galv."],
         ["8/9", "Anclaje", "grapa acero galv. regulable 3D + riel y bulón T M12"],
         ["10", "Empalme", "manguito de alum.; junta 20 mm por piso"],
         ["11", "Calzos", "EPDM dureza 80, 2 por vidrio a L/4"],
         ["12", "Cortafuego", "lana mineral 100 kg/m³ + sellador intumescente"],
         ["13", "RPT", "aislador de poliamida entre montante y presor"],
         ["14", "Sellados", "silicona neutra en perímetros y babetas"]]
yb = sh.tabla(xs, Y2 - 5, [("N°", 8), ("Pieza", 20), ("Medidas / especificación", R - xs - 28)], filas, h=1.55, lead=1.28, pad=0.55)
sh._last = ficha_spec(sh, xs, yb - 2, R - xs, [
    ("Función:", "cerramiento liviano y transparente que no carga: solo recibe su peso y el viento y los lleva a las losas."),
    ("Límites:", "módulo 0,90-1,50 m; altura de montante = 1 piso (máx. ~4,50 m); deformación por viento L/175; tolerancia ±2 mm."),
    ("Montaje:", "desde plataforma articulada, piso por piso: grapas, montantes, travesaños, vidrios sobre calzos, presores, tapas y sellados."),
], h=1.55, lead=1.34)
yy = ficha_spec(sh, xs, sh._last - 3, R - xs, [
    ("Ventajas:", "transparencia y luz natural; liviano (~45 kg/m²); se monta en seco desde afuera; modulación precisa sobre la estructura metálica."),
    ("Desventajas:", "costo alto; ganancia solar y pérdidas de calor (U 2,8 frente a 0,27 del panel); mantenimiento de sellados y limpieza."),
], h=1.55, lead=1.34)
sh.save("L13_Muro_cortina")
