# -*- coding: utf-8 -*-
"""Lámina 13 – Comparación muro cortina vs. panel sándwich: cortes a la misma escala, tabla, gráfico y justificación."""
from lib import Sheet, spec, heading, breakline, REB
import geo

GLASS, ALU, SPAN, NEO = "#bfe3f0", "#9aa3ab", "#6f8796", "#111111"
C_MC, C_PS = "#5dade2", "#c8b48a"
Z0, Z1, XR = 3250, 4720, 900


def estructura(v):
    yt = 4415
    v.poly(geo.perfil_VL(250, yt - 910), mat="HA", sw=0.25)
    v.rect(250, yt - 210, 650, yt - 202, mat="mort", sw=0.05)
    v.poly(geo.perfil_L(250, yt - 202), mat="HA", sw=0.25)
    v.rect(420, yt - 50, XR, yt, mat="HA", sw=0.25)
    v.rect(400, yt, XR, yt + 50, mat="HAis", sw=0.2)
    v.rect(250, yt + 50, XR, yt + 85, mat="mort", sw=0.08)


def make(num, total):
    sh = Sheet(num, total, "Cerramientos 3 · comparación", "Muro cortina vs. panel sándwich: comparación y justificación de la elección",
               "Cortes comparativos 1:20 (misma escala) · gráfico s/ escala")
    heading(sh, "4º COMPARACIÓN Y JUSTIFICACIÓN DE LOS CERRAMIENTOS  ·  3/3", "Ambos cerramientos sobre el MISMO nudo de entrepiso (VL + viga L + TT), dibujados a la misma escala")

    # ============================================================ CORTE MURO CORTINA 1:20
    for k, titulo in enumerate(("E9 MURO CORTINA", "E10 PANEL SÁNDWICH")):
        ox = 16 + k * 56
        sh.title_drawing(ox - 2, 26, titulo, "Corte vertical 1:20 · entrepiso", 1.9)
        v = sh.view(ox + 2, 34 + Z1 / 20, 20)
        estructura(v)
        if k == 0:
            v.rect(32, Z0, 182, Z1, fill="#e3e7ea", sw=0.12); v.line(150, Z0, 150, Z1, sw=0.06)
            v.rect(-30, Z0, -14, Z1, fill="#e9ecee", sw=0.1)
            v.rect(0, 3320, 6, Z1, fill=SPAN, sw=0.1)
            v.rect(40, 3320, 87, Z1, mat="lanav", sw=0.05); v.rect(87, 3316, 93, Z1, fill="#888", sw=0.04)
            v.rect(32, Z0, 150, Z0 + 60, fill=ALU, sw=0.1)
            v.rect(93, 4365, 250, 4458, mat="lana", sw=0.08)
            v.poly([(238, 4040), (246, 4040), (246, 4133), (182, 4133), (182, 4125), (238, 4125)], mat="acero", sw=0.04)
            v.rect(0, Z1 - 20, 182, Z1, fill="#fff", sw=0.05)
            refs = [("1", (3, 3500), "Spandrel vidrio esmaltado 6 mm"), ("2", (64, 3700), "Lana 50 mm en bandeja galv."),
                    ("3", (110, 4400), "Barrera cortafuego (lana s/ ángulo)"), ("4", (215, 4128), "Grapa regulable al riel de la VL"),
                    ("5", (100, 3280), "Travesaño 50x120 · montante 50x150"), ("6", (90, Z1 - 30), "Junta de dilatación 20 mm (J11)")]
        else:
            v.rect(30, Z0, 90, Z1, mat="HA", sw=0.15); v.rect(90, Z0, 150, Z1, mat="epsv", sw=0.06); v.rect(150, Z0, 230, Z1, mat="HA", sw=0.15)
            v.rect(90, 4105, 150, 4175, mat="HA", sw=0.05)
            v.rect(230, Z0, 250, Z1, mat="lanav", sw=0.05)
            v.line(55, 4140, 690, 4140, sw=0.6); v.rect(650, 4105, 662, 4175, mat="acero", sw=0.04)
            v.rect(30, 4090, 60, 4190, mat="mort", sw=0.05)
            refs = [("1", (60, 3500), "Hoja exterior H°A° 6 cm"), ("2", (120, 3700), "EPS 6 cm (aislación continua)"),
                    ("3", (190, 3900), "Hoja interior portante 8 cm"), ("4", (500, 4141), "Bulón pasante M20 (ojal vertical)"),
                    ("5", (240, 4330), "Junta 2 cm lana + sellador"), ("6", (45, 4085), "Rehundido tapado c/ mortero")]
        for z in (Z0, Z1): breakline(sh, v.P(-60, z), v.P(XR, z))
        breakline(sh, v.P(XR, Z0 - 30), v.P(XR, Z1 + 30))
        sh.text(*v.P(-50, Z1 + 60), "EXT.", 1.2, bold=True); sh.text(*v.P(700, Z1 + 60), "INT.", 1.2, bold=True)
        for i, (lab, tgt, txt) in enumerate(refs):
            tx, ty = v.P(*tgt)
            sh.callout((tx, ty), (ox - 6.5, ty), lab, r=1.15)
        yy = 113
        for lab, _, txt in refs:
            sh.text(ox - 2, yy, f"{lab} {txt}", 1.3); yy += 2.3

    # ============================================================ UBICACIÓN EN EL EDIFICIO 1:1000
    sh.title_drawing(10, 133, "UBICACIÓN DE CADA CERRAMIENTO", "Planta 1:1000", 1.9)
    u = sh.view(22, 175, 1000)
    u.rect(0, 0, 30000, 30000, fill="#f3f0ea", sw=0.15)
    for i in range(4):
        for j in range(3): u.rect(i * 10000 - 250, j * 15000 - 250, i * 10000 + 250, j * 15000 + 250, fill="#555", stroke=None)
    u.rect(-300, -900, 30300, -300, fill=C_MC, sw=0.1)
    for r in ((-900, -300, -300, 30300), (30300, -300, 30900, 30300), (-900, 30300, 30900, 30900)):
        u.rect(*r, fill=C_PS, sw=0.1)
    sh.text(*u.P(15000, -3500), "calle · fachada principal", 1.25, anchor="middle")
    nx, ny = u.P(36000, 26000)
    sh.poly([(nx, ny + 12), (nx - 1.5, ny + 7), (nx, ny + 8), (nx + 1.5, ny + 7)], fill="#000", sw=0.1); sh.line(nx, ny + 2, nx, ny + 8, sw=0.2)
    sh.text(nx, ny + 15, "N", 1.4, anchor="middle", bold=True)
    sh.bullets(64, 141, 54, [
        "Muro cortina (azul): fachada principal hacia la calle y al norte, con parasoles / aleros p/ controlar la ganancia solar.",
        "Panel sándwich (beige): fachadas este, oeste (sol bajo de la tarde) y posterior / medianera, donde se exige aislación y F120.",
        "Superficie vidriada ≈ 25 % de la envolvente: buen balance entre luz natural y consumo energético.",
    ], size=1.32, lead=1.22, gap=0.5)

    # ============================================================ TABLA COMPARATIVA
    sh.text(124, 26, "CUADRO COMPARATIVO", 2.1, bold=True)
    rows = [("Criterio", "Muro cortina stick (E9)", "Panel sándwich (E10)"),
            ("Función", "cerramiento vidriado NO portante", "cerramiento opaco autoportante en altura"),
            ("Espesor / módulo", "≈ 0,21 m · módulo 1,25 m", "0,20 m · panel 2,50 x 9,48 m"),
            ("Peso", "45-50 kg/m²", "≈ 350 kg/m² (8,3 t por panel)"),
            ("Transmitancia K", "2,8 W/m²K (1,8 c/ low-e)", "0,5-0,6 W/m²K"),
            ("Aislación acústica", "≈ 35 dB", "≈ 55 dB"),
            ("Resistencia al fuego", "nula: barrera cortafuego en cada losa", "F120"),
            ("Luz natural / visuales", "máxima", "nula"),
            ("Ganancia solar", "alta: requiere control solar", "baja (masa térmica interior)"),
            ("Montaje", "en obra pieza por pieza, plataforma (M6)", "1 izaje por panel c/ grúa (≈ 30 min)"),
            ("Tolerancias", "grapa regulable ± 25 mm", "ojal vertical + junta 20 mm"),
            ("Mantenimiento", "limpieza periódica; sellos c/ 10 años", "mínimo; sellos c/ 10-15 años"),
            ("Costo relativo / m²", "alto (≈ 2 a 3 veces)", "medio"),
            ("Vida útil", "30-40 años (sellos y burletes)", "> 50 años")]
    sh.table(124, 28, [30, 67, 68], rows, size=1.35, rowh=3.15)

    # ============================================================ GRÁFICO
    gy = 76.5
    sh.text(124, gy, "VALORACIÓN (1 = desfavorable · 5 = favorable)", 1.9, bold=True)
    crit = [("Luz natural", 5, 1), ("Aislación térmica", 2, 5), ("Aislación acústica", 2, 5), ("Resistencia al fuego", 1, 5),
            ("Peso propio liviano", 5, 2), ("Rapidez de montaje", 3, 4), ("Costo", 2, 4), ("Mantenimiento", 3, 5)]
    x0, bw = 156, 11.5
    yy = gy + 3
    for name, a, b in crit:
        sh.text(x0 - 1.5, yy + 2.0, name, 1.3, anchor="end")
        sh.rect(x0, yy, x0 + a * bw, yy + 1.4, fill=C_MC, stroke=None, layer="TABLAS")
        sh.rect(x0, yy + 1.5, x0 + b * bw, yy + 2.9, fill=C_PS, stroke=None, layer="TABLAS")
        yy += 3.6
    for k in range(6):
        sh.line(x0 + k * bw, gy + 2.5, x0 + k * bw, yy, sw=0.08, stroke="#999", layer="TABLAS")
        sh.text(x0 + k * bw, yy + 2.2, str(k), 1.2, anchor="middle", layer="TABLAS")
    sh.rect(222, gy + 5, 226, gy + 7, fill=C_MC, stroke=None); sh.text(227.5, gy + 6.8, "Muro cortina", 1.3)
    sh.rect(222, gy + 9, 226, gy + 11, fill=C_PS, stroke=None); sh.text(227.5, gy + 10.8, "Panel sándwich", 1.3)
    sh.text(222, gy + 16, "Totales: muro cortina 23/40", 1.3, bold=True); sh.text(222, gy + 18.4, "panel sándwich 31/40", 1.3, bold=True)

    # ============================================================ JUSTIFICACIÓN
    spec(sh, 124, 116, 165, "JUSTIFICACIÓN DEL USO Y LA ELECCIÓN DE CADA UNO", [
        ("Muro cortina en la fachada principal:", "la estructura de grandes luces retira las columnas y deja la VL perimetral libre: permite una piel vidriada continua que lleva luz natural "
         "hasta el fondo de la planta (15 m de luz de VP) y da la imagen y las visuales del edificio. Se elige STICK porque son sólo 2 niveles (el unitizado no se amortiza) "
         "y porque sus grapas regulables (± 25 mm) absorben las tolerancias de la estructura premoldeada. Se limita a una fachada y se complementa con DVH low-e / control solar."),
        ("Panel sándwich en fachadas posterior y laterales:", "sigue la misma lógica industrial del sistema (premoldeado en planta, mismo proveedor, misma grúa y mismo plan de montaje); "
         "con un solo izaje cierra 23,7 m² con aislación continua (K 5 veces menor que el vidrio), F120 en medianeras y lados expuestos, resistencia al impacto y mantenimiento mínimo."),
        ("Resultado:", "la combinación optimiza el balance energético (vidrio sólo donde aporta luz y visuales, envolvente opaca aislada en el resto) y el costo; ambos cerramientos "
         "resuelven sus movimientos con juntas (J11 / J15) y se fijan a la VL sin cargar a la estructura con esfuerzos no previstos."),
    ], size=1.42, lead=1.24, tsize=2.0)
    return sh
