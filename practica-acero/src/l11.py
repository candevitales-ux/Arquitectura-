# -*- coding: utf-8 -*-
"""Lámina 11 - Máquinas y herramientas de montaje, moldeo y anclaje (croquis a escala)."""
from lib import *
from geom import *

sh = Sheet(NUM["maq"], "Máquinas y herramientas de montaje, moldeo y anclaje", "PUNTO 3 - MÁQUINAS Y HERRAMIENTAS",
           "1:400 - 1:200 - 1:20")
y0 = sh.encabezado("3° MÁQUINAS Y HERRAMIENTAS", "Equipos para izar, montar, soldar, fijar y anclar los elementos prefabricados de acero")
L, R = sh.L + 3, sh.R - 3
W2 = (R - L - 6) / 2
XA, XB = L, L + W2 + 6
Y1 = y0 - 3.5


def rueda(v, c, r):
    v.circ(c, r, "1-VISTA", 25); v.circ(c, r * 0.45, "1-VISTA", 13)


# =============================================================== 1. GRÚA TELESCÓPICA
sh.titulo_dib(L, Y1, 1, "GRÚA AUTOPROPULSADA TELESCÓPICA 50 t (HIDRÁULICA)", "1:400", w=R - L)
v = sh.view_in((L, Y1 - 80, L + 96, Y1 - 7), (-2000, -1200, 34000, 28000), 400)
v.ln((-2000, 0), (34000, 0), "1-VISTA", 25)
v.hatch([(-2000, -600), (34000, -600), (34000, 0), (-2000, 0)], "tierra")
car = [(0, 900), (12500, 900), (12500, 2600), (9000, 2600), (9000, 3300), (2600, 3300), (2600, 2600), (0, 2600)]
v.pl(car, "1-SECCION", 35, True); v.hatch(car, "gris")
v.pl([(10200, 2600), (10200, 3900), (12300, 3900), (12500, 2600)], "1-VISTA", 25)     # cabina
for x in (1500, 3200, 7600, 9300, 11000): rueda(v, (x, 600), 600)
for x in (500, 11800):
    v.ln((x, 1200), (x - 1500 if x < 5000 else x + 1500, 1200), "1-VISTA", 25)
    v.rect((x - 1500 if x < 5000 else x + 1500) - 300, 0, (x - 1500 if x < 5000 else x + 1500) + 300, 1200, "1-VISTA", 25)
v.rect(-1300, -80, -700, 0, "1-SECCION", 18); v.rect(13000, -80, 13600, 0, "1-SECCION", 18)
# pluma telescópica a 58°
a = math.radians(58); px, py = 4200, 3600; Lb = 28000
ux, uy = math.cos(a), math.sin(a)
for w, l0, l1 in ((700, 0, 10000), (560, 9000, 18500), (430, 17500, 25000), (320, 24000, Lb)):
    nx, ny = -uy * w / 2, ux * w / 2
    v.pl([(px + ux * l0 + nx, py + uy * l0 + ny), (px + ux * l1 + nx, py + uy * l1 + ny),
          (px + ux * l1 - nx, py + uy * l1 - ny), (px + ux * l0 - nx, py + uy * l0 - ny)], "1-VISTA", 25, True)
v.ln((6500, 2600), (px + ux * 7000, py + uy * 7000), "1-VISTA", 35)                  # cilindro de elevación
tx, ty = px + ux * Lb, py + uy * Lb
v.ln((tx, ty), (tx, 9500), "1-VISTA", 13)
v.pl([(tx - 300, 9500), (tx + 300, 9500), (tx, 9000)], "1-VISTA", 18, True)
v.ln((tx, 9000), (tx - 2500, 7900), "1-VISTA", 13); v.ln((tx, 9000), (tx + 2500, 7900), "1-VISTA", 13)
v.rect(tx - 6000, 7400, tx + 6000, 7900, "1-SECCION", 25); v.hatch([(tx - 6000, 7400), (tx + 6000, 7400), (tx + 6000, 7900), (tx - 6000, 7900)], "gris")
v.ln((tx - 6000, 7650), (tx - 7500, 5500), "1-OCULTO", 9)
v.dim((px, 0), (tx, 0), -4, txt="radio 15,2 m")
v.ley("pluma 4 tramos (11 a 40 m)", (px + ux * 16000, py + uy * 16000), (8, 4), 1.5)
v.ley("viga IPN 500 de 11,68 m (1,65 t) con balancín", (tx + 4000, 7650), (2, 10), 1.5)
v.ley("estabilizadores + placas de reparto", (13300, -40), (40, 3), 1.5)
v.ley("cable guía (viento)", (tx - 7000, 6200), (10, -8), 1.5)
ficha_spec(sh, L + 98, Y1 - 8, R - L - 98, [
    ("Función:", "izar y posicionar columnas, vigas principales (pieza más pesada: IPN 500, 1,65 t) y paquetes de chapa; descargar los camiones."),
    ("Características:", "capacidad 50 t a 3 m; con 16 m de radio levanta ~4,5 t (la pieza más pesada es de 1,65 t); 3 ejes, 12,5 x 2,55 m; base de estabilizadores 6,5 x 6,6 m."),
    ("Accesorios:", "balancín, eslingas de faja, grilletes, cables guía; operador y señalero habilitados."),
    ("Armado:", "llega por sus medios; en 30-45 min despliega estabilizadores sobre placas de reparto en suelo compactado y nivela; tabla de cargas y limitador de momento."),
], h=1.55, lead=1.36)

# =============================================================== 2. PLATAFORMAS ELEVADORAS
Y2 = Y1 - 86
sh.titulo_dib(XA, Y2, 2, "PLATAFORMAS ELEVADORAS", "1:200", w=W2)
v = sh.view_in((XA, Y2 - 60, XA + W2, Y2 - 7), (-1000, -400, 16500, 10500), 200)
v.ln((-1000, 0), (16500, 0), "1-VISTA", 25)
# articulada (brazo)
v.rect(0, 400, 2500, 1600, "1-SECCION", 25); v.hatch([(0, 400), (2500, 400), (2500, 1600), (0, 1600)], "gris")
rueda(v, (500, 400), 400); rueda(v, (2000, 400), 400)
v.rect(-300, 1600, 900, 2400, "1-VISTA", 18)
pts = [(600, 2000), (4000, 7000), (5200, 6000), (7800, 9200)]
v.pl(pts[:2], "1-VISTA", 35); v.pl(pts[1:3], "1-VISTA", 35); v.pl(pts[2:], "1-VISTA", 35)
v.rect(7600, 9200, 9400, 10300, "1-VISTA", 25)
v.label("articulada 12 m", 4000, -350, 1.4, TA.MIDDLE_CENTER)
# tijera
x0 = 11500
v.rect(x0, 300, x0 + 2500, 900, "1-SECCION", 25); v.hatch([(x0, 300), (x0 + 2500, 300), (x0 + 2500, 900), (x0, 900)], "gris")
rueda(v, (x0 + 400, 300), 300); rueda(v, (x0 + 2100, 300), 300)
zz = 900
for i in range(5):
    v.ln((x0 + 200, zz), (x0 + 2300, zz + 1500), "1-VISTA", 18); v.ln((x0 + 2300, zz), (x0 + 200, zz + 1500), "1-VISTA", 18); zz += 1500
v.rect(x0 - 200, zz, x0 + 2700, zz + 150, "1-SECCION", 25); v.pl([(x0 - 200, zz + 150), (x0 - 200, zz + 1250), (x0 + 2700, zz + 1250), (x0 + 2700, zz + 150)], "1-VISTA", 18)
v.label("tijera 10 m", x0 + 1250, -350, 1.4, TA.MIDDLE_CENTER)
ficha_spec(sh, XA, Y2 - 62, W2, [
    ("Función:", "llevar a los montadores a los nudos para abulonar, soldar studs y colocar cerramientos sin andamios."),
    ("Uso:", "articulada (diesel, 4x4) para el exterior y los nudos a +7,40; tijera eléctrica sobre losa o contrapiso; operario con arnés."),
], h=1.55, lead=1.36)

# =============================================================== 3. SOLDADORA DE PERNOS
sh.titulo_dib(XB, Y2, 3, "EQUIPO DE SOLDADURA DE PERNOS", "1:20", w=W2)
v = sh.view_in((XB, Y2 - 60, XB + W2, Y2 - 7), (-100, -100, 1650, 700), 20)
v.ln((-100, 0), (1650, 0), "1-VISTA", 25)
fu = [(0, 60), (700, 60), (700, 600), (0, 600)]
v.pl(fu, "1-SECCION", 35, True); v.hatch(fu, "gris")
rueda(v, (120, 60), 60); rueda(v, (580, 60), 60)
v.rect(80, 420, 300, 540, "1-VISTA", 13); v.circ((450, 480), 40, "1-VISTA", 13); v.circ((580, 480), 40, "1-VISTA", 13)
v.pl([(700, 300), (900, 250), (1100, 380), (1250, 330)], "1-VISTA", 25)
gun = [(1250, 300), (1450, 300), (1450, 380), (1330, 380), (1330, 520), (1270, 520), (1270, 380), (1250, 380)]
v.pl(gun, "1-SECCION", 35, True); v.hatch(gun, "negro")
v.rect(1450, 320, 1520, 360, "1-VISTA", 18)
v.rect(1520, 300, 1600, 380, "1-VISTA", 18)
v.ley("rectificador 2000 A", (350, 300), (-4, 22), 1.5)
v.ley("pistola + férula cerámica", (1400, 380), (-2, 14), 1.5)
v.ley("cable de masa a la viga", (800, 260), (4, -12), 1.5)
ficha_spec(sh, XB, Y2 - 62, W2, [
    ("Función:", "soldar los conectores Ø19 a través de la chapa galvanizada en una descarga de ~1 s (arco con férula)."),
    ("Uso:", "requiere alimentación trifásica o grupo electrógeno de 150 kVA; alas sin pintura; 1 operario + ayudante (~400 studs/día)."),
], h=1.55, lead=1.36)

# =============================================================== 4. LLAVES DE IMPACTO Y TORQUE

Y3 = Y2 - 84
sh.titulo_dib(XA, Y3, 4, "LLAVES DE IMPACTO Y TORQUE", "1:10", w=W2)
v = sh.view_in((XA, Y3 - 27, XA + W2, Y3 - 8), (-40, -75, 850, 100), 10)
b = [(0, 0), (220, 0), (240, 30), (240, 80), (0, 80)]
v.pl(b, "1-SECCION", 35, True); v.hatch(b, "gris")
v.pl([(60, 0), (40, -120 + 60), (110, -60), (130, 0)], "1-VISTA", 25)
v.rect(240, 25, 300, 55, "1-VISTA", 25); v.rect(300, 15, 345, 65, "1-VISTA", 25)
v.ley("dado M20 (30 mm)", (322, 65), (2, 6), 1.5)
v.pl([(450, 30), (800, 30), (800, 50), (450, 50)], "1-VISTA", 25, True)
v.rect(410, 20, 450, 60, "1-VISTA", 25); v.rect(700, 25, 800, 55, "1-SECCION", 25); v.hatch([(700, 25), (800, 25), (800, 55), (700, 55)], "negro")
v.rect(560, 50, 640, 70, "1-VISTA", 13)
v.ley("escala N·m", (600, 70), (2, 6), 1.5)
ficha_spec(sh, XA, Y3 - 29, W2, [
    ("Impacto:", "neumática o a batería 1/2\" - 3/4\", 1000 N·m: aprieta los bulones de vigas y columnas."),
    ("Torque:", "de click 100-600 N·m: controla el 10 % de los bulones (M20 ≈ 400 N·m) y la tuerca de los pernos de anclaje."),
], h=1.55, lead=1.36)

# =============================================================== 5. FIJADORA DE PÓLVORA
sh.titulo_dib(XB, Y3, 5, "FIJADORA Y ATORNILLADOR", "1:10", w=W2)
v = sh.view_in((XB, Y3 - 27, XB + W2, Y3 - 8), (-40, -75, 850, 100), 10)
b = [(0, 10), (380, 10), (380, 70), (0, 70)]
v.pl(b, "1-SECCION", 35, True); v.hatch(b, "gris")
v.pl([(260, 10), (240, -110 + 60), (310, -50), (320, 10)], "1-VISTA", 25)
v.rect(-40, 25, 0, 55, "1-VISTA", 25); v.rect(380, 20, 430, 60, "1-VISTA", 18)
v.ley("cargador de clavos", (200, 70), (2, 6), 1.5)
b2 = [(520, 20), (720, 20), (720, 70), (520, 70)]
v.pl(b2, "1-SECCION", 35, True); v.hatch(b2, "gris")
v.pl([(560, 20), (550, -50), (600, -50), (610, 20)], "1-VISTA", 25)
v.rect(720, 35, 800, 55, "1-VISTA", 18); v.ln((800, 45), (840, 45), "1-VISTA", 18)
v.ley("atornillador c/ tope", (760, 55), (-4, 8), 1.5)
ficha_spec(sh, XB, Y3 - 29, W2, [
    ("Fijadora:", "tipo Hilti DX 76: clava la chapa colaborante al ala (1 clavo/2 s); carga de pólvora según espesor del ala; con protección auditiva."),
    ("Atornillador:", "2500 rpm con tope de profundidad para autoperforantes de costura y de panel."),
], h=1.55, lead=1.36)

# =============================================================== otros equipos
Y4 = Y3 - 50
sh.titulo_dib(L, Y4, 6, "OTROS EQUIPOS DE MONTAJE, MOLDEO Y ANCLAJE", w=R - L)
otros = [
    ["Camión semirremolque 12,5 m", "traslado de perfiles, chapas y paneles desde el taller", "montaje"],
    ["Autobomba de hormigón con pluma 28 m", "hormigonado de las losas colaborantes (moldeo in situ sobre la chapa)", "moldeo"],
    ["Perfiladora / plegadora (en fábrica)", "conformado en frío de chapa colaborante, cenefas, babetas y cupertinas", "moldeo"],
    ["Taladro magnético + amoladora", "agujeros y ajustes en obra; corte de chapa", "montaje"],
    ["Estación total / nivel láser", "replanteo de ejes y pernos; aplomado de columnas", "anclaje"],
    ["Plantilla de pernos + vibrador", "posición de los pernos al hormigonar las bases", "anclaje"],
    ["Puntales metálicos regulables", "apuntalamiento de la chapa si la luz supera la máxima", "moldeo"],
]
sh.tabla(L, Y4 - 5, [("Equipo", 56), ("Uso", R - L - 56 - 20), ("Tarea", 20)], otros, h=2.0, lead=1.25, pad=0.5)
sh.save(f"L{lam('maq')}_Maquinas_herramientas")
