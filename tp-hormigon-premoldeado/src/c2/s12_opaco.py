# -*- coding: utf-8 -*-
"""Lámina 12 – E10 Panel sándwich premoldeado (cerramiento opaco) + E11 viga portapanel."""
from lib import Sheet, spec, heading, breakline, ground, REB
import geo

PANEL = "#d9d3c7"


def make(num, total):
    sh = Sheet(num, total, "Cerramientos 2 · panel opaco", "E10 Panel sándwich premoldeado y E11 viga portapanel: croquis, medidas y especificación",
               "Alzado y corte 1:100 · sección del panel 1:25 · viga portapanel 1:100 y 1:20")
    heading(sh, "4º CERRAMIENTO OPACO: PANEL SÁNDWICH PREMOLDEADO  ·  2/3", "Panel de fachada de H°A° con aislación incorporada, colgado de la VL con bulones (fija panel) y apoyado en viga portapanel")

    # ============================================================ ALZADO 1:100
    sh.title_drawing(10, 26, "ALZADO (2 paneles)", "Vista exterior 1:100", 2.0)
    v = sh.view(16, 136, 100)
    for k in range(2):
        x0 = k * 2520
        v.rect(x0, -40, x0 + 2500, 9440, fill=PANEL, sw=0.25)
        for z in (4140, 8640):
            for xb in (500, 2000): v.circle(x0 + xb, z, 50, fill="#777", sw=0.08)
    v.rect(-200, -500, 5240, -50, fill=geo.C_VP, sw=0.15, dash="1 0.4")
    for z, t in ((0, "±0,00"), (4500, "+4,50"), (9090, "+9,09")):
        v.line(-400, z, 5600, z, sw=0.1, dash="1.5 0.5", stroke="#666"); sh.level(*v.P(5700, z), t, 1.3)
    ground(sh, v.P(-600, 0)[0], v.P(5600, 0)[0], v.P(0, -150)[1])
    v.dim((0, 9440), (2500, 9440), 2.0, "2,50", size=1.2); v.dim((2500, 9440), (2520, 9440), 5.0, "0,02", size=1.0)
    v.dim((0, -40), (0, 9440), 3.0, "9,48", size=1.3)
    for lab, tgt, at in (("1", (1250, 6000), (73, 48)), ("2", (2000, 8640), (73, 40)), ("3", (2510, 2000), (73, 100)), ("4", (2500, -275), (73, 128))):
        sh.callout(v.P(*tgt), at, lab, r=1.4)
    yy = 151
    for t in ("1 Panel sándwich 2,50 x 9,48 x 0,20 (≈ 8,3 t)", "2 Fija panel: bulón M20 (rehundido tapado)", "3 Junta vertical 20 mm (J15)", "4 Viga portapanel E11 (bajo NPT)"):
        sh.text(12, yy, t, 1.35); yy += 2.4

    # ============================================================ CORTE 1:100
    sh.title_drawing(80, 26, "CORTE", "1:100", 2.0)
    c = sh.view(84, 136, 100)
    c.rect(30, -40, 90, 9440, mat="HA", sw=0.1); c.rect(90, -40, 150, 9440, mat="epsv", sw=0.05); c.rect(150, -40, 230, 9440, mat="HA", sw=0.15)
    c.rect(30, -500, 230, -50, mat="HA", sw=0.15)
    c.rect(250, -1300, 650, 8915, fill="#eceeef", sw=0.1, dash="0.8 0.4")
    for yt in (4415, 8915):
        c.poly(geo.perfil_VL(250, yt - 910), mat="HA", sw=0.15)
        c.poly(geo.perfil_L(250, yt - 210), mat="HA", sw=0.15)
        c.rect(420, yt - 50, 1800, yt + 50, mat="HA", sw=0.1)
    for z in (4140, 8640): c.line(30, z, 680, z, sw=0.3)
    ground(sh, c.P(-800, 0)[0], c.P(1800, 0)[0], c.P(0, -150)[1])
    sh.text(*c.P(-500, 9600), "EXT.", 1.2, bold=True); sh.text(*c.P(1000, 9600), "INT.", 1.2, bold=True)

    # ============================================================ SECCIÓN HORIZONTAL DEL PANEL 1:25
    sh.title_drawing(112, 26, "SECCIÓN HORIZONTAL DEL PANEL", "1:25 · zona de anclaje (maciza) y junta entre paneles", 2.0)
    p = sh.view(120, 52, 25)
    for x0 in (-600, 0, 2520):
        a, b = max(x0, -600), min(x0 + 2500, 3120)
        p.rect(a, 0, b, 60, mat="HA", sw=0.2); p.rect(a, 60, b, 120, mat="eps", sw=0.08); p.rect(a, 120, b, 200, mat="HA", sw=0.2)
    for xm in (500, 2000):
        p.rect(xm - 150, 60, xm + 150, 120, mat="HA", sw=0.1)
        p.line(xm, -10, xm, 260, sw=0.4); p.rect(xm - 50, -15, xm + 50, 0, mat="mort", sw=0.05)
    for x in range(200, 2400, 300):
        if abs(x - 500) > 200 and abs(x - 2000) > 200: p.line(x - 30, 20, x + 30, 180, sw=0.2, stroke="#2e7d32")
    for xj in (-10, 2510):
        p.rect(xj, 5, xj + 10, 15, mat="neo", stroke=None)
    breakline(sh, p.P(-600, -30), p.P(-600, 230)); breakline(sh, p.P(3120, -30), p.P(3120, 230))
    p.dim((0, 0), (2500, 0), -3.0, "2,50", size=1.3)
    p.dim((3120, 0), (3120, 60), -2.0, "6", size=1.1); p.dim((3120, 60), (3120, 120), -2.0, "6", size=1.1); p.dim((3120, 120), (3120, 200), -2.0, "8", size=1.1)
    sh.text(*p.P(-600, -100), "EXTERIOR", 1.3, bold=True); sh.text(*p.P(-600, 260), "INTERIOR", 1.3, bold=True)
    for lab, tgt, at in (("a", (1200, 30), (150, 66)), ("b", (1200, 90), (165, 66)), ("c", (1200, 160), (180, 35)), ("d", (500, 90), (130, 66)),
                         ("e", (800, 100), (195, 35)), ("f", (2515, 10), (230, 66))):
        sh.callout(p.P(*tgt), at, lab, r=1.3)
    yy = 72
    for t in ("a Hoja exterior H°A° 6 cm (terminación texturada / lavada)", "b Alma aislante EPS 6 cm (20 kg/m³, λ = 0,035)",
              "c Hoja interior PORTANTE H°A° 8 cm (recibe los anclajes)", "d Zona maciza 30 x 30 en cada anclaje",
              "e Conectores de fibra de vidrio (sin puente térmico)", "f Junta 20 mm: cordón + sellador PU"):
        sh.text(112, yy, t, 1.35); yy += 2.35

    # ============================================================ VIGA PORTAPANEL
    sh.title_drawing(112, 90, "E11 · VIGA PORTAPANEL 20x85", "Elevación 1:100 entre cuellos de base · sección 1:20", 2.0)
    e = sh.view(118, 112, 100)
    for xc in (0, 10000):
        e.rect(xc - 525, -1450, xc + 525, -510, mat="HAis", sw=0.15)
    e.poly([(525 + 10, -510), (1200, -510), (1200, -900), (8800, -900), (8800, -510), (9475 - 10, -510), (9475 - 10, -50), (525 + 10, -50)], mat="HA", sw=0.25)
    e.poly([(10, -500), (525, -500), (525, -50), (10, -50)], fill="none", sw=0.01)
    e.line(1300, -850, 8700, -850, stroke=REB, sw=0.15)
    e.dim((535, -50), (9465, -50), 2.0, "8,93", size=1.2)
    e.dim((9465, -510), (9465, -900), 0, "", size=1)
    sh.note(e.P(1000, -500), (150, 131), "diente 20x45 s/ neopreno en el cuello", 1.3)
    sh.note(e.P(5000, -880), (180, 108), "cordones de pretensado", 1.3)
    s = sh.view(268, 98, 20)
    s.rect(0, -850, 200, 0, mat="HA", sw=0.3)
    for x, z in ((40, -810), (100, -810), (160, -810), (40, -40), (160, -40)): s.dot(x, z, 0.35, "#000")
    s.rect(20, -830, 180, -20, fill="none", stroke=REB, sw=0.12)
    s.line(-6, -850, -6, -400, sw=0.4)
    s.dim((0, 0), (200, 0), 2.0, "0,20", size=1.2); s.dim((200, 0), (200, -850), -2.0, "0,85", size=1.2)
    sh.note(s.P(-6, -600), (264, 136), "pintura asfáltica", 1.2, anchor="end")

    # ============================================================ ESPECIFICACIONES
    spec(sh, 112, 144, 86, "E10 · Panel sándwich", [
        ("Función:", "cerramiento opaco autoportante en altura: aislación térmica y acústica, resistencia al fuego e impacto; NO es estructura (el peso propio baja a la viga portapanel)."),
        ("Medidas:", "2,50 x 9,48 x 0,20 m (1 pieza por fachada); ≈ 0,14 m³/m² → 350 kg/m²; máx. de catálogo 3,00 x 12-14 m."),
        ("Prestaciones:", "K ≈ 0,5-0,6 W/m²K · aislación acústica ≈ 55 dB · F120 · durabilidad > 50 años, mantenimiento mínimo (sellos c/ 10-15 años)."),
        ("Montaje:", "volteo e izaje con 2 insertos y balancín → asiento en mortero s/ viga portapanel + pasador → bulones a la VL (ojal vertical) → sellado de juntas."),
    ], size=1.38, lead=1.22, tsize=1.9)
    spec(sh, 203, 144, 86, "E11 · Viga portapanel", [
        ("Función:", "recibir el peso de los paneles y transmitirlo a los cuellos de las bases; cierra el perímetro bajo el piso (barrera contra roedores y agua)."),
        ("Medidas:", "0,20 x 0,85 pretensada, diente 0,20 x 0,45 en los extremos, largo 8,93 m (entre cuellos) · ≈ 3,8 t."),
        ("Especificación:", "H-40, 5 cordones Ø12,7; apoyo s/ neopreno; junta EPS 2 cm con la columna; caras enterradas c/ pintura asfáltica."),
    ], size=1.38, lead=1.22, tsize=1.9)
    return sh
