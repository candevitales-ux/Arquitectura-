# -*- coding: utf-8 -*-
"""Lámina 05 - Elementos 3: chapa colaborante (perfil, solape, máximos y mínimos, colocación),
conector de corte, cenefa, tapa de cierre, malla y hormigón."""
from lib import *
from geom import *

sh = Sheet(NUM["deck"], "Chapa colaborante: perfil, límites, colocación, malla y hormigón", "PUNTO 1 - ELEMENTOS CONSTRUCTIVOS",
           "1:10 - 1:5 - 1:50")
y0 = sh.encabezado("1° ELEMENTOS: LOSA COLABORANTE (STEEL DECK)", "Chapa de acero galvanizado que es encofrado perdido y armadura inferior de la losa")
L, R = sh.L + 3, sh.R - 3
Y1 = y0 - 3.5

# =============================================================== 9. CHAPA COLABORANTE
sh.titulo_dib(L, Y1, 9, "CHAPA COLABORANTE h = 76 mm - PERFIL TRANSVERSAL", "1:10 / 1:5", w=R - L)
v = sh.view_in((L, Y1 - 46, L + 112, Y1 - 8), (-120, -230, 1000, 150), 10)
prof = deck_perfil(0, 3, PASO, H_NERV, CRESTA, VALLE)
prof = [(-70, 0 - 76)] + prof[1:]                      # arranca en medio valle (hembra)
prof = [(x, y + 76) for x, y in prof]
prof = clip_x(prof, -70, 915 + 70)
v.pl(prof, "1-SECCION", 35)
for i in range(3):                                     # indentaciones (embossments) en las almas
    xa = i * PASO + VALLE / 2
    for t in (0.3, 0.55, 0.8):
        xx = xa + 22.5 * t; yy = 76 * t
        v.ln((xx - 6, yy), (xx + 6, yy), "1-VISTA", 13)
v.ln((-70, -40), (-70, 110), "1-EJES", 9); v.ln((915 - 70, -40), (915 - 70, 110), "1-EJES", 9)
v.dim((-70, 76), (915 - 70, 76), 5, txt="ancho útil 915")
v.dim((0, 0), (PASO, 0), -5)
v.dim((PASO, 0), (2 * PASO, 0), -5)
v.dim((915 - 70, 0), (915 + 70, 0), -5, txt="solape")
v.dim((915 + 70, 0), (915 + 70, 76), 4)
v.ley("cresta 120", (PASO / 2 + 30, 76), (6, -14), 1.6)
v.ley("valle 140 (apoyo)", (PASO, 0), (4, -12), 1.6)
v.ley("indentaciones (adherencia)", (PASO + VALLE / 2 + 12, 38), (24, 6), 1.6)
v.label("PERFIL 1:10", 400, -195, 1.7, TA.MIDDLE_CENTER, True)
# detalle de solape lateral 1:2,5
v = sh.view_in((L + 114, Y1 - 46, R, Y1 - 8), (-70, -60, 120, 130), 5)
a = [(-60, 76), (-22.5, 76), (0, 0), (70, 0)]                       # chapa 1 (termina en valle)
bb = [(-60, 76 + 1.5), (-22.5, 76 + 1.5), (0 - 1.2, 0 + 1.5), (70, 1.5)]
v.pl([(x, y) for x, y in [(-60, 76), (-22.5, 76), (0, 0), (80, 0)]], "1-SECCION", 35)
v.pl([(10, 1.8), (80, 1.8), (102.5, 76 + 1.8), (110, 76 + 1.8)], "1-SECCION", 35)
v.ln((45, -22), (45, 20), "1-VISTA", 25); v.rect(38, 4, 52, 10, "1-VISTA", 25)
v.ley("autoperforante #10 c/ 900 máx.", (45, 10), (-6, 8), 1.5)
v.ley("chapa 1 (hembra)", (-40, 76), (-2, 8), 1.5)
v.ley("chapa 2 (macho)", (106, 77.8), (-2, 8), 1.5)
v.label("SOLAPE LATERAL 1:5", 25, -45, 1.7, TA.MIDDLE_CENTER, True)
# tabla de máximos y mínimos
yt = Y1 - 49
sh.txt("DIMENSIONES MÁXIMAS Y MÍNIMAS Y LÍMITES DE USO (valores de catálogo de chapa h 76 mm)", L, yt - 1.8, 1.8, bold=True)
filas = [
    ["Espesor de chapa", "0,75 mm (BWG 22)", "1,20 mm (BWG 18)", "0,90 mm"],
    ["Peso propio de la chapa", "8,1 kg/m²", "12,9 kg/m²", "9,7 kg/m²"],
    ["Largo de chapa", "1,50 m", "12,00 m (transporte)", "6,00 m (3 tramos)"],
    ["Luz sin apuntalar (3 tramos)", "-", "2,60 / 3,00 / 3,40 m", "2,00 m (sin puntales)"],
    ["Apoyo de extremo s/ acero", "40 mm", "-", "50 mm (2 x 50 continuo)"],
    ["H° sobre la cresta", "50 mm", "-", "64 mm"],
    ["Espesor total de losa", "126 mm", "200 mm", "140 mm"],
    ["Separación de fijaciones", "-", "300 mm en extremos, 450 mm int.", "en cada valle de extremo"],
    ["Costura lateral (#10)", "-", "900 mm", "c/ 600 mm"],
    ["Sobrecarga de montaje", "-", "150 kg/m² (sin acopios)", "-"],
]
yb = sh.tabla(L, yt - 3.5, [("Parámetro", 46), ("Mínimo", 32), ("Máximo", 50), ("Adoptado", R - L - 128)], filas, h=2.0, lead=1.3, pad=0.6)
# colocación
yc = yb - 4
sh.txt("COLOCACIÓN (secuencia de obra)", L, yc - 2.2, 2.2, bold=True)
pasos = ["1. Verificar nivel de vigas; alas superiores sin pintura donde se sueldan los studs.",
         "2. Izar los paquetes con grúa y apoyarlos sobre las vigas principales, cerca de las columnas.",
         "3. Desplegar las chapas con los nervios perpendiculares a las secundarias, desde un borde, con un valle sobre cada viga principal; solape macho-hembra.",
         "4. Fijar a cada viga: clavo de pólvora (o soldadura de tapón Ø16) en cada valle de los extremos.",
         "5. Coser los solapes laterales con autoperforantes #10; colocar cenefas y tapas de cierre.",
         "6. Soldar los studs a través de la chapa; colocar malla sobre separadores y negativos sobre las vigas.",
         "7. Hormigonar por paños, vibrar y curar 7 días; si la luz supera la máxima, apuntalar a L/2."]
yy = yc - 5
colw = (R - L - 6) / 2
fin = []
for i, p in enumerate(pasos):
    x = L if i < 4 else L + colw + 6
    if i == 4: fin.append(yy); yy = yc - 5
    yy = sh.para(x, yy, colw, p, 2.0, lead=1.38) - 0.8
fin.append(yy)
y2 = min(fin) - 4

# =============================================================== 11/12 malla y hormigón
Y3 = y2 - 2
W2 = (R - L - 6) / 2
sh.titulo_dib(L, Y3, 11, "MALLA Q188 Y NEGATIVOS", "1:50", w=W2)
v = sh.view_in((L, Y3 - 34, L + 40, Y3 - 6), (-100, -150, 1900, 1150), 50)
for i in range(0, 13):
    v.ln((0, i * 150 * 0 + i * 90), (1800, i * 90), "1-VISTA", 9) if i * 90 <= 1050 else None
for j in range(0, 13):
    v.ln((j * 150, 0), (j * 150, 1050), "1-VISTA", 9)
v.rect(0, 0, 1800, 1050, "1-VISTA", 18)
v.dim((0, 0), (300, 0), -4)
ficha_spec(sh, L + 42, Y3 - 6, W2 - 42, [
    ("Malla:", "Q188 = Ø6 c/15 en ambas direcciones, ADN 420; paneles 2,40 x 6,00 m; solape 1 cuadrícula + 50 mm."),
    ("Ubicación:", "a 25 mm de la cara superior, sobre separadores plásticos."),
    ("Negativos:", "Ø8 c/15 de 1,20 m sobre vigas principales (continuidad y fisuras)."),
], h=1.6, lead=1.38)
sh.titulo_dib(L + W2 + 6, Y3, 12, "HORMIGÓN DE LA LOSA", w=W2)
ficha_spec(sh, L + W2 + 6, Y3 - 6, W2, [
    ("Clase:", "H-25, agregado grueso máx. 19 mm, asentamiento 10 a 12 cm (bombeable)."),
    ("Volumen:", "0,102 m³ por m² de losa (140 mm menos el volumen de nervios)."),
    ("Colocación:", "con bomba, en paños; vibrado de inmersión; curado húmedo 7 días; habilitar al tránsito a los 7 días y a la carga total a los 28."),
], h=1.6, lead=1.38)

# =============================================================== 10/13/14 fichas chicas
W3 = (R - L - 8) / 3
X = [L, L + W3 + 4, L + 2 * W3 + 8]
Y2 = Y3 - 43
sh.titulo_dib(X[0], Y2, 10, "CONECTOR", "1:5", w=W3)
v = sh.view_in((X[0], Y2 - 55, X[0] + W3, Y2 - 9), (-115, -40, 110, 150), 5)
v.rect(-100, -27, 100, 0, "1-SECCION", 35); v.hatch([(-100, -27), (100, -27), (100, 0), (-100, 0)], "acero")
v.pl([(-100, 1), (100, 1)], "1-SECCION", 35)
v.hatch([(-100, 1.5), (100, 1.5), (100, 140), (-100, 140)], "hormigon")
v.ln((-100, 140), (100, 140), "1-SECCION", 25)
stud(v, 0, 1.5)
v.pl([(-15, 1.5), (-9.5, 10), (9.5, 10), (15, 1.5)], "1-SECCION", 18, True); v.hatch([(-15, 1.5), (-9.5, 10), (9.5, 10), (15, 1.5)], "negro")
v.dim((-16, 126.5), (16, 126.5), 4)
v.dim((9.5, 1.5), (9.5, 126.5), 14)
v.dim((-9.5, 40), (9.5, 40), 0.01)
v.ley("collar de soldadura", (13, 6), (5, 3), 1.5)
v.ley("chapa e = 0,9", (-70, 1), (-2, 5), 1.5)
v.ley("ala de la viga", (-60, -14), (-2, -5), 1.5)
ficha_spec(sh, X[0], Y2 - 57, W3, [
    ("Medidas:", "Ø19 x 125 mm, cabeza Ø32 x 10; altura mín. = h nervio + 40 = 116 mm."),
    ("Especificación:", "acero ASTM A108 (fu 450 MPa); soldado por arco con férula cerámica, a través de la chapa galvanizada."),
    ("Separación:", "mín. 6 Ø (114 mm), máx. 8 veces la losa; adoptado 1 por nervio (c/ 305)."),
], h=2.0, lead=1.4)

sh.titulo_dib(X[1], Y2, 13, "CENEFA DE BORDE", "1:5", w=W3)
v = sh.view_in((X[1], Y2 - 55, X[1] + W3, Y2 - 9), (-110, -60, 175, 180), 5)
v.pl([(-3, 160), (0, 160), (0, 0), (105, 0), (105, -3), (-3, -3)], "1-SECCION", 35, True)
v.pl([(0, 160), (30, 160)], "1-SECCION", 25)
v.ln((105, -3), (105, -40), "1-OCULTO", 9); v.rect(-3, -40, 160, -3, "1-OCULTO", 9)
v.ln((0, 140), (170, 140), "1-OCULTO", 9)
v.dim((-3, -3), (-3, 160), -5); v.dim((-3, -3), (105, -3), -10 + 0.01)
v.dim((0, 160), (30, 160), 4)
v.ley("labio superior", (20, 160), (6, 4), 1.5)
v.ley("fijación a viga c/ 300", (60, -3), (4, -4), 1.5)
v.ley("ala viga de borde", (140, -20), (1, 8), 1.5)
ficha_spec(sh, X[1], Y2 - 57, W3, [
    ("Función:", "encofrado perdido del borde de la losa; define el espesor y el vuelo."),
    ("Medidas:", "chapa galv. plegada e = 1,6 mm (BWG 16), L de 160 x 105 mm, tiras de 3,00 m."),
    ("Colocación:", "fijada al ala con clavos o soldadura c/ 300 mm; riendas de fleje a la cresta c/ 600 mm."),
], h=2.0, lead=1.4)

sh.titulo_dib(X[2], Y2, 14, "TAPA DE CIERRE", "1:5", w=W3)
v = sh.view_in((X[2], Y2 - 55, X[2] + W3, Y2 - 9), (-140, -95, 140, 100), 5)
prof = [(x - PASO / 2 - 152.5, y + 76) for x, y in deck_perfil(0, 2, PASO, H_NERV, CRESTA, VALLE)]
prof = clip_x(prof, -135, 135)
v.pl(prof, "1-SECCION", 25)
tapa = [(-60, 76), (60, 76), (82.5, 0), (-82.5, 0)]
tapa = [(-70 + 10, 76 - 1), (70 - 10, 76 - 1), (82.5 - 1, 1), (-82.5 + 1, 1)]
cx = 0
v.pl([(-60, 75), (60, 75), (81, 1), (-81, 1)], "1-SECCION", 35, True)
v.hatch([(-60, 75), (60, 75), (81, 1), (-81, 1)], "gris")
for xx in (-40, 40): v.circ((xx, 55), 4, "1-VISTA", 13)
v.dim((-81, 1), (81, 1), -6); v.dim((81, 1), (81, 75), 6)
v.label("VISTA DEL EXTREMO", 0, -85, 1.5, TA.MIDDLE_CENTER, True)
ficha_spec(sh, X[2], Y2 - 57, W3, [
    ("Función:", "cerrar los nervios abiertos en los bordes A y D y en huecos, para que no escape el hormigón."),
    ("Medidas:", "chapa galv. e = 0,6 mm con la forma del nervio (162 x 74 mm) y pestaña de 30 mm."),
    ("Colocación:", "a presión dentro del nervio y 2 autoperforantes por tapa."),
], h=2.0, lead=1.4)

sh.save(f"L{lam('deck')}_Losa_colaborante")
