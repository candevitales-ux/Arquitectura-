# -*- coding: utf-8 -*-
"""Lámina 12 - Planificación: alquiler, armado y acceso de equipos a obra (plano de obrador 1:400 + cronograma)."""
from lib import *
from geom import *

sh = Sheet(12, "Planificación: alquiler, armado y acceso a obra", "PUNTO 3 - MÁQUINAS Y HERRAMIENTAS", "Obrador 1:500")
y0 = sh.encabezado("3° PLANIFICACIÓN DE ALQUILER, ARMADO Y ACCESO", "Cómo se organizan los equipos para montar la estructura en seco")
L, R = sh.L + 3, sh.R - 3
Y1 = y0 - 3.5

# =============================================================== plano de obrador 1:400
sh.titulo_dib(L, Y1, 1, "PLANO DE OBRADOR Y LOGÍSTICA", "1:500", w=96)
LOTE_X, LOTE_Y = 30000, 42000
v = sh.view_in((L, Y1 - 124, L + 96, Y1 - 7), (-3000, -9500, 33000, 42500), 500)
v.rect(0, 0, LOTE_X, LOTE_Y, "1-SECCION", 35)
v.rect(-3000, -9000, 33000, -1500, "1-VISTA", 13); v.hatch([(-3000, -9000), (33000, -9000), (33000, -1500), (-3000, -1500)], "gris")
v.ln((-3000, -5250), (33000, -5250), "1-OCULTO", 9)
v.rect(-3000, -1500, 33000, 0, "1-VISTA", 13)
v.label("CALLE (doble mano, 7,50 m)", 15000, -7500, 1.5, TA.MIDDLE_CENTER)
v.label("vereda", 2000, -900, 1.3)
# edificio
bx, by = 5000, 16000
v.rect(bx, by, bx + LARGO, by + ANCHO, "1-SECCION", 50)
v.hatch([(bx, by), (bx + LARGO, by), (bx + LARGO, by + ANCHO), (bx, by + ANCHO)], "gris")
for x in EJES_X:
    for yy in (0, ANCHO): v.rect(bx + x - 150, by + yy - 150, bx + x + 150, by + yy + 150, "1-SECCION", 18)
v.label("EDIFICIO 20 x 12 m", bx + 10000, by + 6000, 1.6, TA.MIDDLE_CENTER, True)
# portón y circulación
v.ln((9000, 0), (17000, 0), "1-SECCION", 0)
v.rect(9000, -200, 17000, 200, "1-VISTA", 25)
v.pl([(9000, 0), (9000, 13000), (25000, 13000), (25000, 8000)], "1-OCULTO", 13)
v.pl([(17000, 0), (17000, 8000), (25000, 8000)], "1-OCULTO", 13)
v.label("portón 8,00 m", 13000, 700, 1.3, TA.MIDDLE_CENTER)
# camión
v.rect(13700, 1500, 16250, 14000, "1-VISTA", 25); v.ln((13700, 11000), (16250, 11000), "1-VISTA", 13)
v.label("semirremolque", 15400, 6000, 1.3, TA.MIDDLE_CENTER, rot=90)
# grúa: 2 estaciones
for i, (gx, gy) in enumerate(((8000, 12500), (22000, 12500))):
    v.rect(gx - 3300, gy - 3250, gx + 3300, gy + 3250, "1-OCULTO", 9)
    v.rect(gx - 6250, gy - 1275, gx + 6250, gy + 1275, "1-VISTA", 25)
    v.circ((gx, gy), 15200, "1-EJES", 18)
    v.circ((gx, gy), 400, "1-SECCION", 25)
    v.label(f"E{i + 1}", gx + 700, gy + 700, 1.6, bold=True)
# acopios y obrador
for (x0, y0_, x1, y1, s) in ((1000, 1000, 11000, 5500, "acopio perfiles"), (19500, 1000, 29000, 5500, "acopio chapa y paneles"),
                             (1000, 30500, 9000, 40500, "obrador / pañol"), (21000, 33000, 29000, 40500, "contenedores")):
    v.rect(x0, y0_, x1, y1, "1-VISTA", 18)
    v.label(s, (x0 + x1) / 2, (y0_ + y1) / 2, 1.3, TA.MIDDLE_CENTER)
v.circ((27500, 29500), 900, "1-VISTA", 13); v.label("grupo elec.", 27500, 27800, 1.2, TA.MIDDLE_CENTER)
v.dim((0, LOTE_Y), (LOTE_X, LOTE_Y), 3)
v.dim((LOTE_X, 0), (LOTE_X, LOTE_Y), 3)
v.ley("radio de trabajo 15,2 m", (22000 + 10748, 12500 - 10748), (-2, -8), 1.4)
v.ley("estabilizadores s/ placas", (25300, 15750), (-2, 6), 1.4)

# =============================================================== texto: alquiler, armado, acceso
xt = L + 100
sh.titulo_dib(xt, Y1, "A", "ALQUILER", w=R - xt)
yy = ficha_spec(sh, xt, Y1 - 6, R - xt, [
    ("1.", "Del cronograma se sacan los días de uso de cada equipo (grúa: 6 jornadas en 2 etapas) para no pagar días ociosos."),
    ("2.", "Se piden 2-3 presupuestos a empresas de alquiler: grúa por hora con mínimo de 4-8 h + traslado; plataformas y soldadora por semana o mes."),
    ("3.", "Se reserva con 1-2 semanas de anticipación y se confirma 48 h antes, según el pronóstico (no se iza con viento > 40 km/h)."),
    ("4.", "La grúa se alquila con operador habilitado, seguro de responsabilidad civil y tabla de cargas; el señalero lo pone la obra."),
    ("5.", "Se coordina con el taller la entrega de piezas en el orden de montaje (justo a tiempo) para no acopiar de más."),
], h=1.55, lead=1.36)
sh.titulo_dib(xt, yy - 4, "B", "ARMADO EN OBRA", w=R - xt)
yy = ficha_spec(sh, xt, yy - 10, R - xt, [
    ("Grúa:", "llega por sus medios, se ubica en E1, apoya estabilizadores sobre placas de reparto en suelo compactado (o tosca) y nivela; se verifica radio y carga; zona de exclusión."),
    ("Plataformas:", "llegan en camión con rampa; se cargan baterías; recorren terreno firme y nivelado."),
    ("Soldadora:", "grupo electrógeno de 150 kVA junto al obrador; cables de masa a la viga."),
], h=1.55, lead=1.36)
sh.titulo_dib(xt, yy - 4, "C", "ACCESO A LA OBRA", w=R - xt)
yy = ficha_spec(sh, xt, yy - 10, R - xt, [
    ("Ingreso:", "portón de 8 m y radio de giro para semirremolque de 12,5 m; calle con permiso municipal de ocupación para las maniobras."),
    ("Suelo:", "playón de tosca compactada (Proctor 95 %) entre portón y edificio, apto 10 t/m² bajo las placas de la grúa."),
    ("Interferencias:", "verificar cables aéreos y árboles; distancia mínima a líneas eléctricas 5 m."),
], h=1.55, lead=1.36)

# =============================================================== cronograma
yc = Y1 - 130
sh.titulo_dib(L, yc, 2, "CRONOGRAMA DE MONTAJE Y USO DE EQUIPOS (SEMANAS)", w=R - L)
tareas = [("Bases, pernos con plantilla y curado", [1, 2], "retro + hormigón elaborado"),
          ("Montaje columnas y vigas nivel +3,80", [3], "grúa E1/E2 (3 jornadas), plataforma"),
          ("Chapa, studs, malla y hormigón +3,80", [4], "soldadora, fijadora, autobomba"),
          ("Montaje vigas nivel +7,40 y cruces", [5], "grúa E1/E2 (3 jornadas), plataforma"),
          ("Chapa, studs y hormigón cubierta", [6], "soldadora, fijadora, autobomba"),
          ("Panel sándwich y muro cortina", [7, 8], "plataformas articulada y tijera"),
          ("Cubierta, sellados y pintura final", [8, 9], "plataforma tijera")]
x0 = L; wt, wq, wsem = 60, R - L - 60 - 9 * 9, 9
yy = yc - 5
sh.solid([(x0, yy), (R, yy), (R, yy - 5), (x0, yy - 5)], 230, "3-TABLAS")
sh.txt("Tarea", x0 + 1, yy - 3.5, 1.6, bold=True, layer="3-TABLAS")
sh.txt("Equipos", x0 + wt + 1, yy - 3.5, 1.6, bold=True, layer="3-TABLAS")
for k in range(9):
    sh.txt(str(k + 1), x0 + wt + wq + k * wsem + wsem / 2, yy - 2.5, 1.6, TA.MIDDLE_CENTER, "3-TABLAS", True)
for i, (t, sems, eq) in enumerate(tareas):
    y = yy - 5 - i * 4.4
    sh.txt(t, x0 + 1, y - 3.1, 1.55, layer="3-TABLAS", maxw=wt - 2)
    sh.txt(eq, x0 + wt + 1, y - 3.1, 1.55, layer="3-TABLAS", maxw=wq - 2)
    for k in sems:
        xa = x0 + wt + wq + (k - 1) * wsem
        sh.solid([(xa + 0.6, y - 1), (xa + wsem - 0.6, y - 1), (xa + wsem - 0.6, y - 3.4), (xa + 0.6, y - 3.4)], 80, "3-TABLAS")
    sh.pl([(x0, y - 4.4), (R, y - 4.4)], "3-TABLAS", 13)
yb = yy - 5 - len(tareas) * 4.4
for xx in [x0, x0 + wt, x0 + wt + wq] + [x0 + wt + wq + k * wsem for k in range(1, 10)]:
    sh.pl([(xx, yy), (xx, yb)], "3-TABLAS", 13 if L < xx < R else 35)
sh.pl([(x0, yy), (R, yy)], "3-TABLAS", 35); sh.pl([(x0, yb), (R, yb)], "3-TABLAS", 35)
sh.pl([(x0, yy - 5), (R, yy - 5)], "3-TABLAS", 25)
sh.para(L, yb - 2, R - L, "Seguridad: plan de izaje firmado por responsable técnico; zona de exclusión bajo la carga; arnés y línea de vida en altura; no se trabaja con lluvia ni viento fuerte.", 1.6, lead=1.36)
yq = yb - 10
sh.titulo_dib(L, yq, 3, "PLANILLA DE ALQUILER DE EQUIPOS", w=R - L)
filas = [["Grúa telescópica 50 t", "por hora (mín. 8 h) + traslado", "6 jornadas (sem. 3 y 5)", "con operador; seguro RC; plan de izaje"],
         ["Plataforma articulada 12 m", "por semana / mes", "sem. 3 a 8", "operario capacitado; arnés"],
         ["Plataforma tijera 10 m", "por semana", "sem. 7 a 9", "piso firme y nivelado"],
         ["Soldadora de pernos + grupo 150 kVA", "por semana", "sem. 4 y 6", "soldador calificado; combustible"],
         ["Fijadora a pólvora + clavos", "por día o compra de insumos", "sem. 4 y 6", "registro de cartuchos; EPP"],
         ["Autobomba de hormigón", "por servicio (m³ + traslado)", "2 servicios", "acceso del mixer; programación con la hormigonera"],
         ["Llaves de impacto y torque", "propias de la empresa montadora", "sem. 3 a 6", "calibración vigente de la llave de torque"]]
sh.tabla(L, yq - 5, [("Equipo", 46), ("Modalidad", 44), ("Período", 34), ("Requisitos", R - L - 124)], filas, h=1.6, lead=1.3, pad=0.6)
sh.save("L12_Planificacion_obra")
