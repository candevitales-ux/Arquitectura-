# -*- coding: utf-8 -*-
"""Planificación del alquiler, armado y acceso a obra: implantación 1:500 (una lámina) y plan + cronograma (otra)."""
from lib import Sheet, page, spec, heading, TB, TS, TD, TT
from s02_fundacion_columna import legend
import geo

YEL = "#f2c230"


@page("Acceso a obra · implantación y logística de montaje")
def implantacion(num, total):
    sh = Sheet(num, total, "Acceso a obra · implantación", escalas="planta 1:500", fname="M9_Implantacion_Acceso_Obra")
    heading(sh, "3º MÁQUINAS · ACCESO A OBRA E IMPLANTACIÓN", "Dónde entra, se arma y trabaja la grúa · montaje en retroceso (de fondo a frente) · lote 60 x 48 m")
    sh.title_drawing(12, 32, "IMPLANTACIÓN DE OBRA", "esc. 1:500", TT)
    v = sh.view(36, 154, 500)
    v.rect(-2000, -5500, 62000, -2500, fill="#d5d8dc", sw=0.1)
    v.rect(-2000, -2500, 62000, 0, fill="#eeeeee", sw=0.1)
    sh.text(*v.P(30000, -4700), "CALLE", TS, anchor="middle", bold=True)
    v.rect(0, 0, 60000, 48000, fill="#f7f4ec", sw=0.3, dash="2 0.6 0.4 0.6")
    v.poly([(26000, 0), (34000, 0), (34000, 12000), (26000, 12000)], fill="#efe4c8", sw=0.15)
    v.rect(3000, 3000, 26000, 9000, fill="#efe4c8", sw=0.15)
    v.rect(3000, 3000, 9000, 45000, fill="#efe4c8", sw=0.15)
    v.rect(15000, 12000, 45000, 42000, fill="#ffffff", sw=0.35)
    for i in range(4):
        for j in range(3):
            v.rect(15000 + i * 10000 - 250, 12000 + j * 15000 - 250, 15000 + i * 10000 + 250, 12000 + j * 15000 + 250, fill="#555", sw=0.1)
    for i in range(4): v.line(15000 + i * 10000, 12000, 15000 + i * 10000, 42000, sw=0.15, stroke="#888")
    sh.text(*v.P(22000, 40000), "EDIFICIO 30 x 30 m", TS, anchor="middle", bold=True)
    for k, (x, y) in enumerate(((30000, 36500), (30000, 27000), (30000, 17500)), start=1):
        v.circle(x, y, 14000, sw=0.2, stroke="#c0392b", dash="1.2 0.6")
        v.rect(x - 1300, y - 4200, x + 1300, y + 4200, fill=YEL, sw=0.15)
        sh.ball(*v.P(x, y), f"G{k}", r=2.8, fill="#fff")
    sh.text(*v.P(46500, 49800), "radio de trabajo 14 m", TS, color="#c0392b")
    v.pline([(30000, -4000), (30000, 9000), (30000, 33000)], sw=0.35, dash="1.5 0.6", stroke="#1f618d")
    v.rect(33000, 14000, 35500, 35800, fill="#c0392b", sw=0.15)
    v.rect(48000, 6000, 57000, 38000, fill="#e3dccb", sw=0.15)
    for y in range(7000, 37000, 3000): v.line(48500, y, 56500, y, sw=0.1)
    sh.text(*v.P(52500, 22000), "ACOPIO", TS, anchor="middle", rot=90, bold=True)
    for k in range(3): v.rect(48000 + k * 3000, 41500, 50500 + k * 3000, 47000, fill="#aab7b8", sw=0.12)
    sh.text(*v.P(52500, 43800), "OBRADOR", TS, anchor="middle", bold=True)
    v.rect(3500, 38000, 8500, 44500, fill="#d6eaf8", sw=0.12)
    v.rect(25000, -300, 35000, 300, fill="#000", sw=0.05)
    v.dim((26000, 0), (34000, 0), 3.0, "portón 8,00")
    v.dim((9000, 20000), (3000, 20000), 3.0, "6,00")
    for lab, tgt, at in (("A", (30000, 1500), (120, 160)), ("B", (6000, 25000), (18, 112)), ("C", (52500, 30000), (190, 110)),
                         ("D", (30000, 36500), (120, 52)), ("E", (34250, 25000), (190, 90)), ("F", (6000, 41000), (18, 70))):
        sh.callout(v.P(*tgt), at, lab, r=2.8)
    sh.scalebar(150, 40, 500, 20, 5)
    y = legend(sh, 12, 172, ["A Acceso: portón 8 m, camino de tosca compactada 30 cm, ancho ≥ 6 m, pendiente ≤ 8 %",
                             "B Calle interna p/ equipos menores y hormigón de la capa (mixer + bomba)",
                             "C Acopio mínimo de piezas, ordenadas según el montaje, sobre tacos",
                             "D Estaciones de la grúa G1 → G2 → G3: monta de fondo a frente y sale por el acceso",
                             "E Carretón junto a la grúa: izaje directo desde el camión (just in time)",
                             "F Plataforma elevadora y equipo de grouteo"], size=TB)
    spec(sh, 12, y + 4, 186, "CONDICIONES DE ACCESO (verificar antes de contratar)", [
        ("Camino:", "ancho libre ≥ 6 m (carretón 2,60 m + maniobra), radio de giro exterior ≥ 15 m, pendiente ≤ 8 %, base compactada."),
        ("Gálibo:", "altura libre ≥ 4,50 m en el recorrido; sin líneas aéreas a menos de 5 m de la pluma."),
        ("Calle:", "señalización, banderilleros y corte parcial en el horario autorizado por el municipio (piezas > 12 m)."),
    ])
    return sh


@page("Planificación del alquiler, armado y cronograma")
def planificacion(num, total):
    sh = Sheet(num, total, "Planificación del alquiler y armado", escalas="s/ escala", fname="M10_Planificacion_Alquiler")
    heading(sh, "3º MÁQUINAS · PLANIFICACIÓN DEL ALQUILER Y ARMADO", "Cómo se elige, contrata, arma y retira la grúa y los equipos menores")
    y = spec(sh, 12, 32, 186, "PLANIFICACIÓN DEL ALQUILER", [
        ("1 Relevamiento:", "lista de piezas con peso, largo y posición (VP 12,6 t / 14,58 m es la crítica; TT 7,2 t; VL 4,4 t; columna 4,5 t)."),
        ("2 Selección:", "con la tabla de carga se busca el equipo que levante la pieza crítica a su radio (13,6 t a 14 m → grúa 90 t; uso ≤ 75 %)."),
        ("3 Contrato:", "por jornada de 8 h con operador, mínimo de horas, traslado del equipo y del contrapeso y seguro; se reserva con 2-3 semanas."),
        ("4 Permisos:", "municipal (ocupación / corte de calle), tránsito de cargas excepcionales; aviso a la empresa eléctrica si hay líneas aéreas."),
        ("5 Suelo:", "≈ 30-40 t por estabilizador → placas de reparto 0,9 x 0,9 + madera s/ tosca compactada; nunca sobre rellenos."),
        ("6 Coordinación:", "la planta despacha en el orden de montaje; rendimiento ≈ 15-20 piezas por jornada."),
    ], size=TB, lead=1.27)
    y = spec(sh, 12, y + 2, 186, "ARMADO Y RETIRO EN OBRA", [
        ("Llegada:", "la grúa llega autopropulsada (contrapeso en camión aparte) y entra por el acceso A hasta la estación G1."),
        ("Armado (1-2 h):", "nivelar, extender estabilizadores y placas, montar contrapeso, desplegar pluma, check-list y prueba sin carga."),
        ("Operación:", "señalero + 2 montadores + soldador; zona de exclusión balizada; se suspende con viento > 50 km/h."),
        ("Retiro:", "pluma recogida, contrapeso desmontado; sale por el mismo acceso y se repara camino y vereda."),
    ], size=TB, lead=1.27)
    y += 3
    sh.text(12, y, "CRONOGRAMA DE MONTAJE Y ALQUILERES (semanas)", TT, bold=True); y += 2.5
    tasks = [("Fundaciones in situ (cálices)", 1, 3, "#b9a77c"), ("Fabricación en planta", 1, 5, "#7d8a96"),
             ("Columnas + aplomado", 4, 4, "#5d6d7e"), ("VP, VL y viga L", 4, 5, "#7aa36b"), ("Paneles TT", 5, 5, "#c9b98f"),
             ("Capa de compresión", 6, 6, "#a3a3a3"), ("Cerramientos", 6, 8, "#5dade2"),
             ("ALQUILER GRÚA 90 t", 4, 5, "#c0392b"), ("ALQ. plataforma + grouteo", 6, 8, "#e67e22")]
    x0, wl, ww, rh = 12, 66, 15, 4.6
    y0 = y
    sh.rect(x0, y, x0 + wl, y + rh, fill="#e2e6ea", sw=0.12, layer="TABLAS"); sh.text(x0 + 1.2, y + 3.3, "Tarea", TS, bold=True, layer="TABLAS")
    for k in range(8):
        sh.rect(x0 + wl + k * ww, y, x0 + wl + (k + 1) * ww, y + rh, fill="#e2e6ea", sw=0.12, layer="TABLAS")
        sh.text(x0 + wl + k * ww + ww / 2, y + 3.3, f"S{k + 1}", TS, anchor="middle", bold=True, layer="TABLAS")
    y += rh
    for name, a, b, col in tasks:
        sh.rect(x0, y, x0 + wl + 8 * ww, y + rh, stroke="#999", sw=0.1, layer="TABLAS")
        sh.text(x0 + 1.2, y + 3.3, name, TS, bold=name.startswith("ALQ"), layer="TABLAS")
        sh.rect(x0 + wl + (a - 1) * ww + 0.8, y + 0.9, x0 + wl + b * ww - 0.8, y + rh - 0.9, fill=col, stroke=None, layer="TABLAS")
        y += rh
    for k in range(9): sh.line(x0 + wl + k * ww, y0, x0 + wl + k * ww, y, sw=0.1, stroke="#999", layer="TABLAS")
    sh.text(x0, y + 4.5, "La grúa se alquila sólo 2 semanas: se concentran las piezas pesadas; el resto usa equipos menores.", TS, ital=True)
    y += 11
    sh.text(12, y, "EQUIPOS · MODALIDAD DE ALQUILER", TT, bold=True)
    rows = [("Equipo", "Modalidad", "Período", "Incluye / condición"),
            ("Grúa telescópica 90 t", "jornada c/ operador", "S4-S5", "traslado, contrapeso, seguro"),
            ("Tractor + carretón", "por viaje", "S4-S5", "permiso de tránsito, escolta"),
            ("Plataforma articulada", "mensual s/ operador", "S6-S8", "operario capacitado"),
            ("Equipo de grouteo", "semanal", "S4-S6", "mezcladora + bomba"),
            ("Puntales telescópicos", "unidad / semana", "S4-S5", "2 por columna (24 u)"),
            ("Topografía / herramientas", "propias o por día", "S1-S8", "estación total, llave de torque")]
    sh.table(12, y + 2.5, [50, 42, 22, 72], rows, size=TS, rowh=4.6)
    return sh


PAGES = [implantacion, planificacion]
