# -*- coding: utf-8 -*-
"""Lámina 14 - Muro exterior opaco: integral panel sándwich PUR 80 mm (elevación 1:200, panel 1:10, junta 1:2)."""
from lib import *
from geom import *

sh = Sheet(NUM["panel"], "Muro exterior opaco: integral panel sándwich 80 mm", "PUNTO 4 - MURO EXTERIOR", "1:200 - 1:12,5 - 1:2", hmin=2.8)
y0 = sh.encabezado("4° MURO EXTERIOR OPACO: PANEL SÁNDWICH (INTEGRAL)",
                   "Panel metálico autoportante con núcleo aislante, colocado horizontal entre columnas - laterales y contrafrente")
L, R = sh.L + 3, sh.R - 3
Y1 = y0 - 3.5
EP = 80

# =============================================================== 1. ELEVACIÓN LATERAL
sh.titulo_dib(L, Y1, 1, "ELEVACIÓN LATERAL (EJE 1)", "1:200", w=86)
v = sh.view_in((L, Y1 - 62, L + 86, Y1 - 8), (-1800, -1300, 12900, 8300), 200)
v.ln((-1000, 0), (12900, 0), "1-VISTA", 35)
v.rect(0, 0, ANCHO, CUP, "1-SECCION", 35)
for z in range(1000, int(CUP), 1000): v.ln((0, z), (ANCHO, z), "1-VISTA", 13)
for yy in EJES_Y[1:-1]: v.ln((yy, 0), (yy, CUP), "1-VISTA", 25)
for zl, zh in ((0, N1 - LOSA - 500), (N1, N2 - LOSA - 500)):
    v.ln((4000, zl + 200), (8000, zh), "1-OCULTO", 9); v.ln((8000, zl + 200), (4000, zh), "1-OCULTO", 9)
for z in (N1, N2): v.ln((0, z), (ANCHO, z), "1-OCULTO", 9)
v.dim((0, 0), (4000, 0), -4); v.dim((4000, 0), (8000, 0), -4); v.dim((8000, 0), (ANCHO, 0), -4)
v.dim((ANCHO, 0), (ANCHO, 1000), 4); v.dim((ANCHO, 0), (ANCHO, CUP), 9)
v.nivel(-300, N1, "+3,80", -1); v.nivel(-300, N2, "+7,40", -1); v.nivel(-300, CUP, "+8,00", -1)
v.ley("panel 1,00 x 4,00 m (8 hileras)", (2000, 6500), (4, 8), 1.4)
v.ley("junta vertical sobre columna", (4000, 2500), (6, -3), 1.4)

# =============================================================== 2. PANEL COMPLETO 1:10
xr = L + 92
sh.titulo_dib(xr, Y1, 2, "SECCIÓN DE UN PANEL (TRANSVERSAL)", "1:12,5", w=R - xr)
v = sh.view_in((xr, Y1 - 62, R, Y1 - 8), (-60, -260, 1060, 320), 12.5)
# panel acostado: x = ancho (abajo hembra a la izquierda, macho a la derecha), y = espesor (y=EP exterior)
v.pl([(z, EP + (2 if (z // 25) % 2 else 0)) for z in range(0, 1001, 25)], "1-SECCION", 25)
v.pl([(0, 0), (1000, 0)], "1-SECCION", 25)
v.hatch([(15, 0), (985, 0), (985, EP), (15, EP)], "aislacion")
v.pl([(1000, 0), (1000, 25), (1030, 30), (1030, 50), (1000, 55), (1000, EP)], "1-SECCION", 25)
v.pl([(0, 0), (0, 25), (30, 30), (30, 50), (0, 55), (0, EP)], "1-SECCION", 25)
v.dim((0, EP + 2), (1000, EP + 2), 6, txt="ancho útil 1000")
v.dim((1030, 0), (1030, EP), 4)
v.ley("chapa ext. 0,5 microperfilada", (300, EP + 2), (-4, 12), 1.4)
v.ley("núcleo PUR 40 kg/m³", (300, 40), (2, -14), 1.4)
v.ley("chapa int. 0,5", (850, 0), (-4, -20), 1.4)
v.ley("macho", (1030, 40), (-4, -14), 1.4)
v.ley("hembra", (20, 40), (-2, -14), 1.4)
v.label("EXTERIOR", 500, 260, 1.4, TA.MIDDLE_CENTER, True); v.label("INTERIOR", 300, -240, 1.4, TA.MIDDLE_CENTER, True)

# =============================================================== 3. JUNTA MACHIHEMBRADA 1:2
Y2 = Y1 - 70
sh.titulo_dib(L, Y2, 3, "JUNTA HORIZONTAL MACHIHEMBRADA", "1:2", w=86)
v = sh.view_in((L, Y2 - 92, L + 86, Y2 - 7), (-55, -85, 115, 85), 2)
# panel inferior (macho arriba)
low = [(0, -85), (0, -2), (25, -2), (30, 28), (50, 28), (55, -2), (EP, -2), (EP, -85)]
up = [(0, 85), (0, 2), (24, 2), (29, 32), (51, 32), (56, 2), (EP, 2), (EP, 85)]
for p in (low, up):
    v.hatch(p, "aislacion")
v.pl(low, "1-SECCION", 35); v.pl(up, "1-SECCION", 35)
for x in (0, EP):
    v.ln((x - 0.5, -85), (x - 0.5, -2), "1-SECCION", 35); v.ln((x - 0.5, 2), (x - 0.5, 85), "1-SECCION", 35)
v.pl([(-4, 2), (-4, 10), (0, 14)], "1-SECCION", 25)                         # labio de goteo de la chapa ext.
v.rect(EP - 14, -2, EP - 6, 2, "1-VISTA", 13); v.hatch([(EP - 14, -2), (EP - 6, -2), (EP - 6, 2), (EP - 14, 2)], "negro")
v.circ((40, 30), 3, "1-VISTA", 13)
v.rect(EP, -85, EP + 20, 85, "1-VISTA", 18)                                     # montante 100x20
bulon(v, (-6, 50), (EP + 18, 50), 6.3, cab=4, tuerca=False, lw=13)
v.rect(-8, 44, -4, 56, "1-VISTA", 13); v.hatch([(-8, 44), (-4, 44), (-4, 56), (-8, 56)], "negro")
v.ley("chapa exterior con labio de goteo", (-4, 8), (10, -34), 1.4)
v.ley("burlete EPDM", (EP - 10, 0), (2, -12), 1.4)
v.ley("cordón PUR", (40, 30), (4, -34), 1.4)
v.ley("montante 100x20x2", (EP + 10, -60), (2, -16), 1.4)
v.ley("autoperf. Ø6,3 + EPDM", (-6, 50), (8, 8), 1.4)
v.label("EXTERIOR", -40, -75, 1.4, TA.MIDDLE_CENTER, True)

# =============================================================== 4. ESPECIFICACIÓN
xs = L + 92
sh.titulo_dib(xs, Y2, 4, "ESPECIFICACIÓN TÉCNICA", w=R - xs)
filas = [["Chapas", "acero galv. Z275 prepintado e = 0,5 mm; poliéster 25 µm"],
         ["Núcleo", "poliuretano inyectado PUR 40 kg/m³ (opción PIR por fuego)"],
         ["Espesor", "80 mm (hay 30 a 150 mm)"],
         ["Ancho útil", "1,00 m; largo a medida hasta 12 m (adoptado 4,00 m)"],
         ["Luz máx.", "4,50 m entre apoyos con viento 100 kg/m²"],
         ["Peso", "≈ 11 kg/m²"],
         ["Aislación", "λ 0,022 W/m·K -> U ≈ 0,27 W/m²·K"],
         ["Acústica", "Rw ≈ 25 dB"],
         ["Fijación", "2 autoperforantes Ø6,3 + EPDM por panel y apoyo"],
         ["Juntas", "machihembrada horiz.; vertical 10 mm sellada + tapajunta"],
         ["Colores", "carta RAL; film protector que se retira al final"],
         ["Tolerancia", "espesor ±2 mm; largo ±5 mm"]]
yb = sh.tabla(xs, Y2 - 5, [("Ítem", 18), ("Valor", R - xs - 18)], filas, h=1.55, lead=1.28, pad=0.55)

# =============================================================== 5. MONTAJE
Y3 = min(yb, Y2 - 98) - 5
sh.titulo_dib(L, Y3, 5, "MONTAJE Y FUNCIÓN", w=R - L)
w2 = (R - L - 6) / 2
pasos = ["1. Nivelar y anclar la viga portapanel a la fundación.", "2. Soldar los montantes 100x20 a las alas de las columnas.",
         "3. Fijar el perfil U de arranque con babeta y la cinta butílica.", "4. Montar de abajo hacia arriba, macho arriba, con ventosa/pinza.",
         "5. Fijar cada panel en cada apoyo con 2 tornillos sin aplastar el núcleo.", "6. Sellar juntas verticales, tapajuntas, cupertina; retirar el film."]
yy = Y3 - 6
for p_ in pasos: yy = sh.para(L, yy, w2, p_, 1.55, lead=1.34) - 0.3
ficha_spec(sh, L + w2 + 6, Y3 - 6, w2, [
    ("Función:", "cerramiento integral: en una sola pieza resuelve terminación exterior, aislación térmica, barrera de vapor y terminación interior."),
    ("Ventajas:", "liviano, rápido (≈ 150 m²/día por cuadrilla), muy aislante, montaje en seco."),
    ("Desventajas:", "opaco; sensible a golpes; PUR combustible (usar PIR o lana mineral si se exige fuego)."),
], h=1.55, lead=1.34)
sh.save(f"L{lam('panel')}_Panel_sandwich")
