# -*- coding: utf-8 -*-
"""E10 Panel sándwich premoldeado (croquis) y E11 viga portapanel + especificaciones."""
from lib import Sheet, page, spec, heading, breakline, ground, fitview, autocallouts, REB, TB, TS, TD, TT
from s02_fundacion_columna import legend
import geo

PANEL = "#d9d3c7"


@page("E10 · Panel sándwich: alzado, corte y sección")
def croquis(num, total):
    sh = Sheet(num, total, "E10 · Panel sándwich · croquis", escalas="alzado y corte 1:100 · sección del panel 1:25", fname="E10_Panel_Sandwich_Croquis")
    heading(sh, "4º CERRAMIENTOS · E10 PANEL SÁNDWICH PREMOLDEADO", "Panel de H°A° con aislación incorporada, colgado de la VL con bulones (fija panel) y apoyado en la viga portapanel")
    sh.title_drawing(12, 32, "ALZADO (2 paneles)", "Vista exterior 1:100", TT)
    v = sh.view(26, 140, 100)
    for k in range(2):
        x0 = k * 2520
        v.rect(x0, -40, x0 + 2500, 9440, fill=PANEL, sw=0.3)
        for z in (4140, 8640):
            for xb in (500, 2000): v.circle(x0 + xb, z, 60, fill="#777", sw=0.08)
    v.rect(-200, -500, 5240, -50, fill=geo.C_VP, sw=0.15, dash="1 0.4")
    for z, t in ((0, "±0,00"), (4500, "+4,50"), (9090, "+9,09")):
        v.line(-400, z, 5600, z, sw=0.12, dash="1.5 0.5", stroke="#666"); sh.level(*v.P(6100, z), t)
    ground(sh, v.P(-600, 0)[0], v.P(5600, 0)[0], v.P(0, -150)[1])
    v.dim((0, 9440), (2500, 9440), 3.0, "2,50")
    v.dim((0, -40), (0, 9440), 4.0, "9,48")
    for lab, tgt, at in (("1", (1250, 6000), (92, 76)), ("2", (2000, 8640), (92, 54)), ("3", (2510, 2000), (92, 112)), ("4", (2500, -275), (92, 146))):
        sh.callout(v.P(*tgt), at, lab)
    legend(sh, 12, 154, ["1 Panel sándwich 2,50 x 9,48 x 0,20 m (≈ 8,3 t)", "2 Fija panel: bulón M20 (rehundido tapado)", "3 Junta vertical 20 mm (J15)",
                         "4 Viga portapanel E11 (bajo el nivel de piso)"], w=92)
    sh.title_drawing(108, 32, "CORTE", "esc. 1:100", TT)
    c = sh.view(118, 140, 100)
    c.rect(30, -40, 90, 9440, mat="HA", sw=0.12); c.rect(90, -40, 150, 9440, mat="epsv", sw=0.06); c.rect(150, -40, 230, 9440, mat="HA", sw=0.18)
    c.rect(30, -500, 230, -50, mat="HA", sw=0.15)
    c.rect(250, -1300, 650, 8915, fill="#eceeef", sw=0.12, dash="0.8 0.4")
    for yt in (4415, 8915):
        c.poly(geo.perfil_VL(250, yt - 910), mat="HA", sw=0.18)
        c.poly(geo.perfil_L(250, yt - 210), mat="HA", sw=0.18)
        c.rect(420, yt - 50, 6000, yt + 50, mat="HA", sw=0.12)
    for z in (4140, 8640): c.line(30, z, 680, z, sw=0.35)
    ground(sh, c.P(-800, 0)[0], c.P(6000, 0)[0], c.P(0, -150)[1])
    sh.text(*c.P(-200, 9700), "EXT.", TS, bold=True, anchor="middle"); sh.text(*c.P(3500, 9700), "INT.", TS, bold=True, anchor="middle")
    sh.note(c.P(500, 4140), (150, 86), "bulón a la VL (J13)")
    sh.note(c.P(130, -275), (150, 132), "viga portapanel (J14)")
    sh.note(c.P(3000, 4415), (150, 72), "entrepiso (VL + L + TT)")
    # sección horizontal 1:20
    sh.title_drawing(12, 184, "SECCIÓN HORIZONTAL DEL PANEL", "esc. 1:20 · zona de anclaje maciza y junta entre paneles (se muestra 1 panel y la junta)", TT)
    box = (12, 196, 198, 236)
    p = fitview(sh, (26, 196, 184, 236), (-100, 2520 + 300, -20, 260), 20)
    for x0 in (-700, 0, 2520):
        a, b = max(x0, -100), min(x0 + 2500, 2820)
        p.rect(a, 0, b, 60, mat="HA", sw=0.25); p.rect(a, 60, b, 120, mat="eps", sw=0.1); p.rect(a, 120, b, 200, mat="HA", sw=0.25)
    for xm in (500, 2000):
        p.rect(xm - 150, 60, xm + 150, 120, mat="HA", sw=0.12)
        p.line(xm, -10, xm, 260, sw=0.5); p.rect(xm - 50, -15, xm + 50, 0, mat="mort", sw=0.05)
    for x in range(200, 2400, 300):
        if abs(x - 500) > 200 and abs(x - 2000) > 200: p.line(x - 30, 20, x + 30, 180, sw=0.25, stroke="#2e7d32")
    for xj in (-10, 2510): p.rect(xj, 5, xj + 10, 15, mat="neo", stroke=None)
    breakline(sh, p.P(-100, -30), p.P(-100, 230)); breakline(sh, p.P(2820, -30), p.P(2820, 230))
    p.dim((0, 0), (2500, 0), -5.0, "2,50")
    p.dim((2820, 0), (2820, 200), -4.0, "0,20")
    sh.text(*p.P(1250, -170), "EXTERIOR", TS, bold=True, anchor="middle"); sh.text(*p.P(1250, 330), "INTERIOR", TS, bold=True, anchor="middle")
    autocallouts(sh, [(l, p.P(*q)) for l, q in (("a", (1250, 30)), ("b", (1150, 90)), ("c", (1250, 160)), ("d", (500, 90)), ("e", (800, 100)), ("f", (2515, 10)))],
                 (12, 196, 198, 238))
    y = 244
    items = ["a Hoja exterior H°A° 6 cm (texturada)", "b Alma EPS 6 cm (20 kg/m³)", "c Hoja interior PORTANTE H°A° 8 cm",
             "d Zona maciza 30x30 en cada anclaje", "e Conectores de fibra de vidrio", "f Junta 20 mm: cordón + sellador PU"]
    for k, t in enumerate(items):
        lab, txt = t.split(" ", 1)
        col, row = divmod(k, 3)
        xx, yy = 12 + col * 93, y + row * 6.2
        sh.ball(xx + 2.2, yy - 0.8, lab, r=2.0); sh.text(xx + 6, yy, txt, TS)
    return sh


@page("E10 + E11 · Especificación panel y viga portapanel")
def especificacion(num, total):
    sh = Sheet(num, total, "E10 · E11 · especificación", escalas="viga portapanel: elevación 1:100 · sección 1:20", fname="E10_E11_Especificacion")
    heading(sh, "4º CERRAMIENTOS · E10 PANEL Y E11 VIGA PORTAPANEL", "Especificación del panel sándwich y de la viga que lo recibe en el arranque")
    sh.title_drawing(12, 32, "E11 · VIGA PORTAPANEL 20x85", "Elevación 1:100 entre cuellos de base · sección 1:20", TT)
    e = sh.view(26, 70, 100)
    for xc in (0, 10000): e.rect(xc - 525, -1450, xc + 525, -510, mat="HAis", sw=0.15)
    e.poly([(535, -510), (1200, -510), (1200, -900), (8800, -900), (8800, -510), (9465, -510), (9465, -50), (535, -50)], mat="HA", sw=0.3)
    e.line(1300, -850, 8700, -850, stroke=REB, sw=0.2)
    e.dim((535, -50), (9465, -50), 3.0, "8,93")
    sh.note(e.P(870, -400), (40, 92), "diente 20x45 s/ neopreno en el cuello")
    sh.note(e.P(5000, -880), (80, 84), "cordones de pretensado")
    s = sh.view(170, 42 + 850 / 20, 20)
    s.rect(0, -850, 200, 0, mat="HA", sw=0.35)
    for x, z in ((40, -810), (100, -810), (160, -810), (40, -40), (160, -40)): s.dot(x, z, 0.5, "#000")
    s.rect(20, -830, 180, -20, fill="none", stroke=REB, sw=0.15)
    s.line(-6, -850, -6, -400, sw=0.5)
    s.dim((0, 0), (200, 0), 3.0, "0,20"); s.dim((200, 0), (200, -850), -3.0, "0,85")
    sh.note(s.P(-6, -600), (162, 98), "pintura asfáltica", anchor="end")
    y = spec(sh, 12, 132, 186, "E10 · PANEL SÁNDWICH", [
        ("Función:", "cerramiento opaco autoportante en altura: aislación térmica y acústica, resistencia al fuego y al impacto; NO es estructura (su peso baja a la viga portapanel)."),
        ("Medidas:", "2,50 x 9,48 x 0,20 m (1 pieza por fachada); ≈ 0,14 m³/m² → 350 kg/m²; máximos de catálogo 3,00 x 12-14 m."),
        ("Capas:", "hoja exterior H°A° 6 cm + EPS 6 cm + hoja interior portante H°A° 8 cm, unidas con conectores de fibra de vidrio (sin puente térmico)."),
        ("Prestaciones:", "K ≈ 0,5-0,6 W/m²K · aislación acústica ≈ 55 dB · F120 · vida útil > 50 años; renovación de sellos c/ 10-15 años."),
        ("Montaje:", "volteo e izaje con 2 insertos y balancín → asiento en mortero s/ viga portapanel + pasador → bulones a la VL con ojal vertical → sellado de juntas."),
    ], size=TB, lead=1.3)
    spec(sh, 12, y + 4, 186, "E11 · VIGA PORTAPANEL", [
        ("Función:", "recibir el peso de los paneles y llevarlo a los cuellos de las bases; cierra el perímetro bajo el piso (barrera contra agua y roedores)."),
        ("Medidas:", "0,20 x 0,85 pretensada, diente 0,20 x 0,45 en los extremos, largo 8,93 m entre cuellos · ≈ 3,8 t."),
        ("Especificación:", "H-40, 5 cordones Ø12,7; apoyo s/ neopreno; junta EPS 2 cm con la columna; caras enterradas c/ pintura asfáltica."),
    ], size=TB, lead=1.3)
    return sh


PAGES = [croquis, especificacion]
