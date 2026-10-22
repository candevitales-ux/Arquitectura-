# -*- coding: utf-8 -*-
"""Lámina 15 - Comparación muro cortina vs. panel sándwich (croquis a la misma escala 1:20) y justificación."""
from lib import *
from geom import *

sh = Sheet(15, "Comparación CW vs. panel y justificación de la elección", "PUNTO 4 - MURO EXTERIOR", "1:20")
y0 = sh.encabezado("4° COMPARACIÓN: VIDRIADO (CW) vs. OPACO (PANEL)",
                   "Los dos cerramientos dibujados a la misma escala frente a la losa de entrepiso (+3,80)")
L, R = sh.L + 3, sh.R - 3
W2 = (R - L - 6) / 2
XA, XB = L, L + W2 + 6
Y1 = y0 - 3.5
REAL = (-750, -1060, 900, 620)


def estructura(v, borde_txt=True):
    v.hatch([(-750, -LOSA), (-60, -LOSA), (-60, 0), (-750, 0)], "hormigon"); v.rect(-750, -LOSA, -60, 0, "1-SECCION", 35)
    v.pl([(-60, 0), (-63, 0), (-63, -LOSA - 15), (-150, -LOSA - 15)], "1-SECCION", 25)
    pts = xf(ipn_poly(*IPN[VS]), -100, -LOSA - 100); v.pl(pts, "1-SECCION", 25, True); v.hatch(pts, "acero")
    v.rect(-750, 0, -200, 30, "1-VISTA", 13)
    v.pl([(-750, -LOSA - 600), (-200, -LOSA - 600)], "1-OCULTO", 13)
    v.nivel(-650, 0, "+3,80", 1)


# =============================================================== CW
sh.titulo_dib(XA, Y1, "A", "VIDRIADO: MURO CORTINA STICK", "1:20", w=W2)
v = sh.view_in((XA, Y1 - 92, XA + W2, Y1 - 8), REAL, 20)
estructura(v)
MX0 = 60
v.rect(MX0, -1050, MX0 + 150, 560, "1-VISTA", 25)
v.ln((MX0, -200), (MX0 + 150, -200), "1-SECCION", 25)
gz = [(-45, -100), (50, -100), (50, 0), (40, 0), (40, -90), (-45, -90)]
v.pl(gz, "1-SECCION", 25, True); v.hatch(gz, "acero")
z0, z1 = -LOSA - 760, -LOSA - 760 + 900
for zz in (z0, z1):
    v.rect(MX0, zz - 60, MX0 + 180, zz, "1-SECCION", 25); v.hatch([(MX0, zz - 60), (MX0 + 180, zz - 60), (MX0 + 180, zz), (MX0, zz)], "gris")
for za, zb in ((-1050, z0 - 60), (z1, 560)):
    v.rect(MX0 + 180, za, MX0 + 205, zb, "1-SECCION", 25); v.hatch([(MX0 + 180, za), (MX0 + 205, za), (MX0 + 205, zb), (MX0 + 180, zb)], "vidrio")
v.rect(MX0 + 185, z0, MX0 + 191, z1 - 60, "1-SECCION", 25); v.hatch([(MX0 + 185, z0), (MX0 + 191, z0), (MX0 + 191, z1 - 60), (MX0 + 185, z1 - 60)], "negro")
v.rect(MX0 + 100, z0, MX0 + 150, z1 - 60, "1-VISTA", 13); v.hatch([(MX0 + 100, z0), (MX0 + 150, z0), (MX0 + 150, z1 - 60), (MX0 + 100, z1 - 60)], "lana")
v.hatch([(-60, -LOSA), (MX0, -LOSA), (MX0, 0), (-60, 0)], "lana")
v.dim((MX0, 560), (MX0 + 205, 560), 3)
v.ley("montante alum. 50x150", (MX0 + 75, 500), (12, 4), 1.4)
v.ley("DVH 24,8 mm", (MX0 + 192, -1100), (6, 0), 1.4)
v.ley("spandrel + lana mineral", (MX0 + 188, z0 + 400), (6, 0), 1.4)
v.ley("grapa al borde de losa", (0, -95), (-4, -18), 1.4)
v.ley("cortafuego", (0, -40), (-14, -26), 1.4)

# =============================================================== PANEL
sh.titulo_dib(XB, Y1, "B", "OPACO: PANEL SÁNDWICH 80", "1:20", w=W2)
v = sh.view_in((XB, Y1 - 92, XB + W2, Y1 - 8), REAL, 20)
estructura(v)
PX = 120
v.rect(PX - 20, -1050, PX, 560, "1-OCULTO", 13)                                    # montante (detrás, en columna)
for zj in range(-1300, 751, 1000):
    pass
v.rect(PX, -1050, PX + 80, 560, "1-SECCION", 35); v.hatch([(PX, -1050), (PX + 80, -1050), (PX + 80, 560), (PX, 560)], "aislacion")
for zj in (-650, 350):
    v.ln((PX, zj), (PX + 80, zj), "1-SECCION", 35)
v.hatch([(-60, -LOSA), (PX - 20, -LOSA), (PX - 20, 0), (-60, 0)], "lana")
v.dim((PX, 560), (PX + 80, 560), 3)
v.ley("panel PUR 80 (junta c/ 1,00 m)", (PX + 40, 500), (10, 4), 1.4)
v.ley("montante 100x20 (en columna)", (PX - 10, -900), (-6, -10), 1.4)
v.ley("relleno lana mineral + sello", (30, -60), (-4, -26), 1.4)
v.ley("junta machihembrada", (PX + 80, 350), (6, -6), 1.4)

# =============================================================== TABLA COMPARATIVA
Y2 = Y1 - 98
sh.titulo_dib(L, Y2, 1, "CUADRO COMPARATIVO", w=R - L)
filas = [["Tipo", "semi-industrializado: perfiles y vidrios armados en obra", "integral, industrializado: llega terminado"],
         ["Ubicación en el edificio", "frente A (20,00 x 7,40 m), acceso y vidriera", "laterales, contrafrente y parapeto"],
         ["Espesor total", "≈ 205 mm (montante 150 + vidrio)", "80 mm"],
         ["Peso", "≈ 45 kg/m²", "≈ 11 kg/m²"],
         ["Transmitancia U", "2,8 W/m²K (visión) / 0,6 (spandrel)", "0,27 W/m²K"],
         ["Aislación acústica", "Rw ≈ 35 dB (laminado)", "Rw ≈ 25 dB"],
         ["Luz y visuales", "total", "nula"],
         ["Apoyo en la estructura", "cuelga de cada losa: grapas c/ 1,00 m", "montantes en columnas c/ 4,00 m + portapanel"],
         ["Juntas y movimientos", "junta 20 mm por piso + burletes; drenada", "machihembrada + vertical sellada 10 mm"],
         ["Fuego", "barrera cortafuego en cada losa", "PUR combustible (usar PIR o lana mineral)"],
         ["Montaje", "≈ 15-20 m²/día; plataforma articulada", "≈ 150 m²/día; plataforma o grúa"],
         ["Costo relativo", "alto (≈ 4 a 5 veces)", "bajo (1)"],
         ["Mantenimiento", "limpieza; sellados c/ 10-15 años", "lavado; repintado c/ 15-20 años"]]
yb = sh.tabla(L, Y2 - 5, [("Característica", 36), ("A - Muro cortina", (R - L - 36) / 2), ("B - Panel sándwich", (R - L - 36) / 2)], filas, h=1.6, lead=1.3, pad=0.55)

# =============================================================== JUSTIFICACIÓN
Y3 = yb - 5
sh.titulo_dib(L, Y3, 2, "JUSTIFICACIÓN DEL USO Y LA ELECCIÓN", w=R - L)
ficha_spec(sh, L, Y3 - 6, W2, [
    ("Muro cortina en el frente:", "es la cara pública (acceso y vidriera); da luz natural a la planta libre de 12 m de profundidad y muestra la estructura de grandes luces. El sistema stick se adapta a la modulación de 4,00 m de los pórticos (4 módulos de 1,00 m) y se cuelga de las losas, sin cargar."),
    ("Compatibilidad:", "ambos se montan en seco, igual que la estructura; las juntas móviles absorben las flechas de las vigas y la dilatación del acero."),
], h=1.55, lead=1.34)
ficha_spec(sh, XB, Y3 - 6, W2, [
    ("Panel en laterales y contrafrente:", "fachadas sin vistas importantes; el panel aísla 10 veces más que el vidrio, pesa 4 veces menos (menos carga en vigas y fundaciones), es barato y se coloca muy rápido."),
    ("Resultado:", "se combina lo mejor de cada uno: transparencia donde hace falta y eficiencia térmica y económica en el resto (≈ 75 % de la envolvente es opaca)."),
], h=1.55, lead=1.34)
Y4 = Y3 - 31
sh.titulo_dib(L, Y4, 3, "MATRIZ DE DECISIÓN POR FACHADA (1 = malo, 5 = muy bueno; peso según la fachada)", w=R - L)
crit = [("Luz natural y visuales", 5, 1, 3, 1), ("Aislación térmica", 2, 5, 1, 3), ("Peso sobre la estructura", 2, 5, 1, 2),
        ("Costo", 1, 5, 2, 3), ("Velocidad de montaje", 2, 5, 1, 2), ("Mantenimiento", 2, 4, 1, 2), ("Imagen / representatividad", 5, 2, 3, 1)]
filas = []
tA = [0, 0]; tB = [0, 0]
for c, a, b, pf, pl in crit:
    filas.append([c, str(a), str(b), str(pf), str(pl), str(a * pf), str(b * pf), str(a * pl), str(b * pl)])
    tA[0] += a * pf; tB[0] += b * pf; tA[1] += a * pl; tB[1] += b * pl
filas.append(["TOTAL", "", "", "", "", str(tA[0]), str(tB[0]), str(tA[1]), str(tB[1])])
wc = (R - L - 52) / 8
ybm = sh.tabla(L, Y4 - 5, [("Criterio", 52), ("CW", wc), ("Panel", wc), ("Peso frente", wc), ("Peso lat./contraf.", wc),
                     ("Frente CW", wc), ("Frente panel", wc), ("Lat. CW", wc), ("Lat. panel", wc)], filas, h=1.55, lead=1.28, pad=0.5)
sh.para(L, ybm - 2, R - L, f"Resultado: en el frente gana el muro cortina ({tA[0]} contra {tB[0]}) porque pesan la luz y la imagen; en laterales y contrafrente gana el panel ({tB[1]} contra {tA[1]}) por aislación, costo y velocidad.", 1.6, bold=True, lead=1.36)
sh.save("L15_Comparacion_CW_panel")
