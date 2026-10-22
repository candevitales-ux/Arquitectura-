# -*- coding: utf-8 -*-
"""Lámina 10 – Planificación del alquiler, armado y acceso a obra de los equipos: implantación 1:500 + cronograma."""
import math
from lib import Sheet, spec, heading, wrap
import geo

YEL = "#f2c230"


def make(num, total):
    sh = Sheet(num, total, "Máquinas y dispositivos 3", "Planificación del alquiler, armado y acceso a obra de los equipos de montaje",
               "Implantación de obra 1:500 · cronograma s/ escala")
    heading(sh, "3º MÁQUINAS: ALQUILER, ARMADO Y ACCESO A OBRA  ·  3/3", "Cómo se planifica la grúa (y equipos menores) desde la contratación hasta el retiro")

    # ============================================================ IMPLANTACIÓN 1:500
    sh.title_drawing(10, 26, "IMPLANTACIÓN DE OBRA Y LOGÍSTICA DE MONTAJE", "Planta 1:500 · lote 60 x 48 m · montaje en retroceso (de fondo a frente)", 2.0)
    v = sh.view(14, 134, 500)
    v.rect(-2000, -5500, 62000, -2500, fill="#d5d8dc", sw=0.1)                      # calzada
    v.rect(-2000, -2500, 62000, 0, fill="#eeeeee", sw=0.1)                          # vereda
    sh.text(*v.P(30000, -4600), "CALLE (corte parcial autorizado durante el montaje de VP)", 1.3, anchor="middle")
    v.rect(0, 0, 60000, 48000, fill="#f7f4ec", sw=0.3, dash="2 0.6 0.4 0.6")
    # camino de acceso (tosca compactada)
    v.poly([(26000, 0), (34000, 0), (34000, 12000), (26000, 12000)], fill="#efe4c8", sw=0.15)
    v.rect(3000, 3000, 26000, 9000, fill="#efe4c8", sw=0.15)
    v.rect(3000, 3000, 9000, 45000, fill="#efe4c8", sw=0.15)
    # edificio
    v.rect(15000, 12000, 45000, 42000, fill="#ffffff", sw=0.3)
    for i in range(4):
        for j in range(3):
            v.rect(15000 + i * 10000 - 200, 12000 + j * 15000 - 200, 15000 + i * 10000 + 200, 12000 + j * 15000 + 200, fill="#555", sw=0.1)
    for i in range(4): v.line(15000 + i * 10000, 12000, 15000 + i * 10000, 42000, sw=0.12, stroke="#888")
    sh.text(*v.P(22000, 40000), "EDIFICIO 30 x 30 m", 1.4, anchor="middle", bold=True)
    # estaciones de grúa (interiores, en retroceso) + radio 14 m
    for k, (x, y) in enumerate(((30000, 36500), (30000, 27000), (30000, 17500)), start=1):
        v.circle(x, y, 14000, sw=0.15, stroke="#c0392b", dash="1.2 0.6")
        v.rect(x - 1300, y - 4200, x + 1300, y + 4200, fill=YEL, sw=0.15)
        sh.ball(*v.P(x, y), f"G{k}", r=2.0, fill="#fff")
    sh.text(*v.P(44500, 49000), "R trabajo 14 m", 1.3, color="#c0392b")
    # camión y recorrido
    v.pline([(30000, -4000), (30000, 9000), (30000, 33000)], sw=0.3, dash="1.5 0.6", stroke="#1f618d")
    v.rect(33000, 14000, 35500, 35800, fill="#c0392b", sw=0.15)
    sh.text(*v.P(36200, 24000), "carretón (descarga directa)", 1.25, rot=90, color="#1f618d")
    # acopio y obrador
    v.rect(48000, 6000, 57000, 38000, fill="#e3dccb", sw=0.15)
    for y in range(7000, 37000, 3000): v.line(48500, y, 56500, y, sw=0.08)
    sh.text(*v.P(52500, 22000), "ACOPIO DE PIEZAS", 1.25, anchor="middle", rot=90, bold=True)
    sh.text(*v.P(52500, 39200), "s/ tacos, por orden de montaje", 1.1, anchor="middle")
    for k in range(3): v.rect(48000 + k * 3000, 41500, 50500 + k * 3000, 47000, fill="#aab7b8", sw=0.12)
    sh.text(*v.P(52500, 44000), "OBRADOR", 1.25, anchor="middle", bold=True)
    v.rect(3500, 38000, 8500, 44500, fill="#d6eaf8", sw=0.12)
    sh.text(*v.P(6000, 41000), "plataforma y", 1.1, anchor="middle"); sh.text(*v.P(6000, 39700), "grouteo", 1.1, anchor="middle")
    # portón y radios de giro
    v.rect(25000, -300, 35000, 300, fill="#000", sw=0.05)
    v.dim((26000, 0), (34000, 0), 2.0, "portón 8,00", size=1.2)
    v.dim((9000, 20000), (3000, 20000), 2.0, "6,00", size=1.2)
    for lab, tgt, at in (("A", (30000, 1500), (98, 125)), ("B", (6000, 25000), (8, 100)), ("C", (52500, 30000), (140, 88)),
                         ("D", (30000, 36500), (100, 40)), ("E", (34250, 25000), (140, 72))):
        sh.callout(v.P(*tgt), at, lab, r=1.6)
    yy = 149
    for t in ("A Acceso: portón 8 m, camino de tosca compactada 30 cm, ancho ≥ 6 m, pendiente ≤ 8 %",
              "B Calle interna p/ equipos menores y hormigón de la capa (mixer + bomba)",
              "C Acopio mínimo, piezas en orden de montaje · D Estaciones de grúa G1 → G3 (en retroceso hacia el acceso)",
              "E Carretón junto a la grúa: izaje directo desde el camión (just in time)"):
        sh.text(12, yy, t, 1.35); yy += 2.4

    # ============================================================ PLANIFICACIÓN (texto)
    y = spec(sh, 150, 26, 139, "PLANIFICACIÓN DEL ALQUILER", [
        ("1 Relevamiento:", "lista de piezas c/ peso, largo y posición (VP 12,6 t / 14,58 m es la crítica; TT 7,2 t; VL 4,4 t; columna 4,5 t)."),
        ("2 Selección:", "con la tabla de carga se busca el equipo que levante la pieza crítica al radio máximo de su estación (13,6 t a 14 m → grúa 90 t; uso ≤ 75 %)."),
        ("3 Contrato:", "alquiler por jornada de 8 h c/ operador habilitado, mínimo de horas, traslado ida y vuelta del equipo y del contrapeso, seguro de RC; se reserva con 2-3 semanas."),
        ("4 Permisos:", "municipal (ocupación / corte de calle), tránsito de cargas excepcionales (piezas > 12 m), aviso a la empresa eléctrica si hay líneas aéreas."),
        ("5 Suelo:", "presión por estabilizador ≈ 30-40 t → placas de reparto 0,9 x 0,9 + madera s/ tosca compactada; nunca sobre rellenos ni cerca de excavaciones."),
        ("6 Coordinación:", "la planta despacha en el orden de montaje (TT y VP de un paño por viaje); rendimiento ≈ 15-20 piezas por jornada."),
    ], size=1.42, lead=1.22, tsize=2.0)
    y = spec(sh, 150, y + 1.5, 139, "ARMADO Y RETIRO DEL EQUIPO EN OBRA", [
        ("Llegada:", "la grúa llega autopropulsada; el contrapeso en camión aparte. Ingresa por el acceso A hasta la estación G1 (fondo)."),
        ("Armado (1-2 h):", "nivelar, extender estabilizadores y placas, montar contrapeso con su propio sistema, desplegar pluma, check-list y prueba sin carga."),
        ("Operación:", "señalero + 2 montadores + soldador; zona de exclusión balizada; se suspende con viento > 50 km/h."),
        ("Retiro:", "pluma recogida, contrapeso desmontado, sale por el mismo acceso; se verifica la reparación del camino y vereda."),
    ], size=1.42, lead=1.22, tsize=2.0)

    # ============================================================ CRONOGRAMA
    y0 = y + 4
    sh.text(150, y0, "CRONOGRAMA DE MONTAJE Y ALQUILERES (semanas)", 2.0, bold=True)
    tasks = [("Fundaciones in situ (cálices)", 1, 3, "#b9a77c"), ("Fabricación en planta", 1, 5, "#7d8a96"),
             ("Columnas + aplomado", 4, 4, "#5d6d7e"), ("VP, VL y viga L", 4, 5, "#7aa36b"), ("Paneles TT", 5, 5, "#c9b98f"),
             ("Capa de compresión", 6, 6, "#a3a3a3"), ("Cerramientos", 6, 8, "#5dade2"),
             ("ALQUILER GRÚA 90 t", 4, 5, "#c0392b"), ("ALQ. plataforma + grouteo", 6, 8, "#e67e22")]
    x0, wl, ww, rh = 150, 42, 12, 3.0
    yy = y0 + 2
    for k in range(8):
        sh.rect(x0 + wl + k * ww, yy, x0 + wl + (k + 1) * ww, yy + rh, fill="#e2e6ea", sw=0.12, layer="TABLAS")
        sh.text(x0 + wl + k * ww + ww / 2, yy + 2.2, f"S{k + 1}", 1.35, anchor="middle", bold=True, layer="TABLAS")
    sh.rect(x0, yy, x0 + wl, yy + rh, fill="#e2e6ea", sw=0.12, layer="TABLAS"); sh.text(x0 + 1, yy + 2.2, "Tarea", 1.35, bold=True, layer="TABLAS")
    yy += rh
    for name, a, b, col in tasks:
        sh.rect(x0, yy, x0 + wl + 8 * ww, yy + rh, stroke="#999", sw=0.08, layer="TABLAS")
        sh.text(x0 + 1, yy + 2.15, name, 1.3, bold=name.startswith("ALQ"), layer="TABLAS")
        sh.rect(x0 + wl + (a - 1) * ww + 0.6, yy + 0.6, x0 + wl + b * ww - 0.6, yy + rh - 0.6, fill=col, stroke=None, layer="TABLAS")
        yy += rh
    for k in range(9): sh.line(x0 + wl + k * ww, y0 + 2, x0 + wl + k * ww, yy, sw=0.08, stroke="#999", layer="TABLAS")
    sh.text(x0, yy + 3, "La grúa se alquila sólo 2 semanas: se concentran todas las piezas pesadas; el resto usa equipos menores.", 1.3, ital=True)
    yy += 7
    sh.text(x0, yy, "EQUIPOS: MODALIDAD DE ALQUILER", 2.0, bold=True)
    rows = [("Equipo", "Modalidad", "Período", "Incluye / condición"),
            ("Grúa telescópica 90 t", "por jornada c/ operador", "S4-S5 (10 jorn.)", "traslado, contrapeso, seguro RC"),
            ("Tractor + carretón", "por viaje (fabricante)", "S4-S5", "permiso de tránsito y escolta"),
            ("Plataforma articulada 12 m", "mensual sin operador", "S6-S8", "operario capacitado, carga diaria"),
            ("Equipo de grouteo", "semanal", "S4-S6", "mezcladora + bomba + mangueras"),
            ("Puntales telescópicos", "por unidad y semana", "S4-S5", "2 por columna (24 u)"),
            ("Topografía / herramientas", "propias o por día", "S1-S8", "estación total, llave de torque")]
    sh.table(x0, yy + 1.5, [36, 32, 24, 47], rows, size=1.3, rowh=3.0)
    yy = yy + 1.5 + 7 * 3.0 + 6
    spec(sh, x0, yy, 139, "CONDICIONES DE ACCESO A OBRA (verificar antes de contratar)", [
        ("Camino:", "ancho libre ≥ 6 m (carretón 2,60 m + maniobra), radio de giro exterior ≥ 15 m, pendiente ≤ 8 %, base de tosca compactada 30 cm."),
        ("Gálibo:", "altura libre ≥ 4,50 m en todo el recorrido; sin líneas aéreas a menos de 5 m de la pluma; árboles podados."),
        ("Playa de maniobra:", "superficie firme junto a cada estación de grúa p/ que el carretón descargue sin retroceder por la calle."),
        ("Calle:", "señalización, banderilleros y corte parcial en el horario autorizado por el municipio (piezas > 12 m)."),
    ], size=1.38, lead=1.22, tsize=1.9)
    sh.scalebar(14, 166, 500, 20, 5)
    return sh
