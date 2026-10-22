# -*- coding: utf-8 -*-
"""Comparación muro cortina vs. panel sándwich: cortes a la misma escala + ubicación (una lámina);
cuadro, valoración y justificación (otra lámina)."""
from lib import Sheet, page, spec, heading, breakline, TB, TS, TD, TT
import geo

GLASS, ALU, SPAN, NEO = "#bfe3f0", "#9aa3ab", "#6f8796", "#111111"
C_MC, C_PS = "#5dade2", "#c8b48a"
Z0, Z1, XR = 3250, 4720, 900


def estructura(v):
    yt = 4415
    v.poly(geo.perfil_VL(250, yt - 910), mat="HA", sw=0.3)
    v.rect(250, yt - 210, 650, yt - 202, mat="mort", sw=0.05)
    v.poly(geo.perfil_L(250, yt - 202), mat="HA", sw=0.3)
    v.rect(420, yt - 50, XR, yt, mat="HA", sw=0.3)
    v.rect(400, yt, XR, yt + 50, mat="HAis", sw=0.2)
    v.rect(250, yt + 50, XR, yt + 85, mat="mort", sw=0.08)


@page("Comparación: cortes a la misma escala y ubicación")
def cortes(num, total):
    sh = Sheet(num, total, "Comparación · cortes", escalas="cortes 1:15 · planta 1:750", fname="Comparacion_1_Cortes")
    heading(sh, "4º COMPARACIÓN DE CERRAMIENTOS · CORTES", "Ambos cerramientos sobre el MISMO nudo de entrepiso (VL + viga L + TT), dibujados a la misma escala")
    for k, titulo in enumerate(("E9 MURO CORTINA", "E10 PANEL SÁNDWICH")):
        ox = 22 + k * 96
        sh.title_drawing(ox - 10, 32, titulo, "Corte vertical 1:15", TT)
        v = sh.view(ox + 30 / 15, 48 + Z1 / 15 - 3250 / 15 + 3250 / 15, 15)
        estructura(v)
        if k == 0:
            v.rect(32, Z0, 182, Z1, fill="#e3e7ea", sw=0.12); v.line(150, Z0, 150, Z1, sw=0.08)
            v.rect(-30, Z0, -14, Z1, fill="#e9ecee", sw=0.12)
            v.rect(0, 3320, 6, Z1, fill=SPAN, sw=0.1)
            v.rect(40, 3320, 87, Z1, mat="lanav", sw=0.06); v.rect(87, 3316, 93, Z1, fill="#888", sw=0.05)
            v.rect(32, Z0, 150, Z0 + 60, fill=ALU, sw=0.12)
            v.rect(93, 4365, 250, 4458, mat="lana", sw=0.1)
            v.poly([(238, 4040), (246, 4040), (246, 4133), (182, 4133), (182, 4125), (238, 4125)], mat="acero", sw=0.05)
            v.rect(0, Z1 - 20, 182, Z1, fill="#fff", sw=0.06)
            refs = [("1", (3, 3500), "Spandrel vidrio esmaltado 6 mm"), ("2", (64, 3700), "Lana 50 mm en bandeja galv."),
                    ("3", (110, 4410), "Barrera cortafuego (lana s/ ángulo)"), ("4", (215, 4128), "Grapa regulable al riel de la VL"),
                    ("5", (100, 3280), "Travesaño 50x120 / montante 50x150"), ("6", (90, Z1 - 10), "Junta de dilatación 20 mm (J11)")]
        else:
            v.rect(30, Z0, 90, Z1, mat="HA", sw=0.2); v.rect(90, Z0, 150, Z1, mat="epsv", sw=0.08); v.rect(150, Z0, 230, Z1, mat="HA", sw=0.2)
            v.rect(90, 4105, 150, 4175, mat="HA", sw=0.06)
            v.rect(230, Z0, 250, Z1, mat="lanav", sw=0.05)
            v.line(55, 4140, 690, 4140, sw=0.7); v.rect(650, 4105, 662, 4175, mat="acero", sw=0.05)
            v.rect(30, 4090, 60, 4190, mat="mort", sw=0.06)
            refs = [("1", (60, 3500), "Hoja exterior H°A° 6 cm"), ("2", (120, 3700), "EPS 6 cm (aislación continua)"),
                    ("3", (190, 3900), "Hoja interior portante 8 cm"), ("4", (500, 4160), "Bulón pasante M20 (ojal vertical)"),
                    ("5", (240, 4330), "Junta 2 cm lana + sellador"), ("6", (45, 4050), "Rehundido tapado c/ mortero")]
        for z in (Z0, Z1): breakline(sh, v.P(-60, z), v.P(XR, z))
        breakline(sh, v.P(XR, Z0 - 30), v.P(XR, Z1 + 30))
        sh.text(*v.P(-20, Z1 + 80), "EXT.", TS, bold=True, anchor="middle"); sh.text(*v.P(750, Z1 + 80), "INT.", TS, bold=True, anchor="middle")
        for i, (lab, tgt, txt) in enumerate(refs):
            tx, ty = v.P(*tgt)
            sh.callout((tx, ty), (ox - 7, ty), lab, r=2.1)
        yy = 152
        for lab, _, txt in refs:
            sh.ball(ox - 7, yy - 0.8, lab, r=2.0); sh.text(ox - 3, yy, txt, TS); yy += 5.6
    # ubicación 1:750
    sh.title_drawing(12, 192, "UBICACIÓN DE CADA CERRAMIENTO", "Planta 1:750", TT)
    u = sh.view(26, 246, 750)
    u.rect(0, 0, 30000, 30000, fill="#f3f0ea", sw=0.15)
    for i in range(4):
        for j in range(3): u.rect(i * 10000 - 250, j * 15000 - 250, i * 10000 + 250, j * 15000 + 250, fill="#555", stroke=None)
    u.rect(-300, -1000, 30300, -300, fill=C_MC, sw=0.1)
    for r in ((-1000, -300, -300, 30300), (30300, -300, 31000, 30300), (-1000, 30300, 31000, 31000)): u.rect(*r, fill=C_PS, sw=0.1)
    sh.text(*u.P(15000, -4000), "calle · fachada principal (norte)", TS, anchor="middle")
    sh.bullets(80, 206, 118, [
        "Muro cortina (azul): fachada principal hacia la calle y al norte, con parasoles / aleros para controlar la ganancia solar.",
        "Panel sándwich (beige): fachadas este, oeste (sol bajo de la tarde) y posterior / medianera, donde se exige aislación y F120.",
        "Superficie vidriada ≈ 25 % de la envolvente: buen balance entre luz natural y consumo energético.",
    ], TB, 1.3, 1.2)
    return sh


@page("Comparación: cuadro, valoración y justificación")
def cuadro(num, total):
    sh = Sheet(num, total, "Comparación · cuadro y justificación", escalas="s/ escala", fname="Comparacion_2_Cuadro_Justificacion")
    heading(sh, "4º COMPARACIÓN Y JUSTIFICACIÓN DE LOS CERRAMIENTOS", "Muro cortina stick (E9) vs. panel sándwich premoldeado (E10)")
    rows = [("Criterio", "Muro cortina (E9)", "Panel sándwich (E10)"),
            ("Función", "cerramiento vidriado NO portante", "opaco autoportante en altura"),
            ("Espesor / módulo", "≈ 0,21 m · módulo 1,25 m", "0,20 m · panel 2,50 x 9,48 m"),
            ("Peso", "45-50 kg/m²", "≈ 350 kg/m² (8,3 t/panel)"),
            ("Transmitancia K", "2,8 W/m²K (1,8 c/ low-e)", "0,5-0,6 W/m²K"),
            ("Aislación acústica", "≈ 35 dB", "≈ 55 dB"),
            ("Resistencia al fuego", "nula: barrera en cada losa", "F120"),
            ("Luz natural / visuales", "máxima", "nula"),
            ("Ganancia solar", "alta: requiere control solar", "baja (masa térmica)"),
            ("Montaje", "en obra pieza por pieza (M6)", "1 izaje por panel (≈ 30 min)"),
            ("Tolerancias", "grapa regulable ± 25 mm", "ojal vertical + junta 20 mm"),
            ("Mantenimiento", "limpieza; sellos c/ 10 años", "mínimo; sellos c/ 10-15 años"),
            ("Costo relativo / m²", "alto (≈ 2 a 3 veces)", "medio"),
            ("Vida útil", "30-40 años", "> 50 años")]
    y = sh.table(12, 30, [46, 70, 70], rows, size=TS, rowh=4.8)
    y += 7
    sh.text(12, y, "VALORACIÓN (1 = desfavorable · 5 = favorable)", TT, bold=True)
    crit = [("Luz natural", 5, 1), ("Aislación térmica", 2, 5), ("Aislación acústica", 2, 5), ("Resistencia al fuego", 1, 5),
            ("Peso propio liviano", 5, 2), ("Rapidez de montaje", 3, 4), ("Costo", 2, 4), ("Mantenimiento", 3, 5)]
    x0, bw = 58, 17
    yy = y + 4
    for name, a, b in crit:
        sh.text(x0 - 2, yy + 3.2, name, TS, anchor="end")
        sh.rect(x0, yy, x0 + a * bw, yy + 2.2, fill=C_MC, stroke=None, layer="TABLAS")
        sh.rect(x0, yy + 2.4, x0 + b * bw, yy + 4.6, fill=C_PS, stroke=None, layer="TABLAS")
        yy += 6
    for k in range(6):
        sh.line(x0 + k * bw, y + 3, x0 + k * bw, yy, sw=0.1, stroke="#999", layer="TABLAS")
        sh.text(x0 + k * bw, yy + 3, str(k), TS, anchor="middle", layer="TABLAS")
    sh.rect(150, y + 8, 156, y + 11, fill=C_MC, stroke=None); sh.text(158, y + 10.6, "Muro cortina 23/40", TS, bold=True)
    sh.rect(150, y + 15, 156, y + 18, fill=C_PS, stroke=None); sh.text(158, y + 17.6, "Panel sándwich 31/40", TS, bold=True)
    spec(sh, 12, yy + 12, 186, "JUSTIFICACIÓN DE LA ELECCIÓN", [
        ("Muro cortina en la fachada principal:", "la estructura de grandes luces libera la fachada: la VL perimetral permite una piel vidriada continua que lleva luz natural "
         "hasta el fondo de la planta (15 m de luz de VP) y da imagen y visuales. Se elige STICK porque son sólo 2 niveles (el unitizado no se amortiza) "
         "y sus grapas regulables absorben las tolerancias del premoldeado."),
        ("Panel sándwich en el resto:", "sigue la misma lógica industrial (premoldeado en planta, mismo proveedor, misma grúa y plan de montaje); "
         "con un solo izaje cierra 23,7 m² con aislación continua (K 5 veces menor que el vidrio), F120 en medianeras, resistencia al impacto y mínimo mantenimiento."),
        ("Resultado:", "vidrio sólo donde aporta luz y visuales y envolvente opaca aislada en el resto: mejor balance energético y de costo; ambos absorben "
         "sus movimientos con juntas (J11 / J15) y se fijan a la VL sin cargar a la estructura con esfuerzos no previstos."),
    ], size=TB, lead=1.28)
    return sh


PAGES = [cortes, cuadro]
