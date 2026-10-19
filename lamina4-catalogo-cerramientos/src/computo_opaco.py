# -*- coding: utf-8 -*-
"""Lámina 4 - Cómputo de materiales (cerramiento opaco + cubiertas + carpinterías), A3 vertical.
Sin planos con medidas: se adopta un edificio estándar coherente con el corte integral de acero.
Todo en mm de papel (escala 1:1 de la hoja). Las cantidades se calculan acá, no se escriben a mano."""
import sys, os
import ezdxf
from ezdxf.enums import TextEntityAlignment as TA

OUT = sys.argv[1] if len(sys.argv) > 1 else "build"
os.makedirs(OUT, exist_ok=True)
W, H = 297.0, 420.0
doc = ezdxf.new("R2018", setup=True); doc.units = ezdxf.units.MM
doc.styles.add("ARIAL", font="arial.ttf"); doc.styles.add("ARIAL-NEGRITA", font="arialbd.ttf")
msp = doc.modelspace()
for n in ("0-MARCO", "3-TEXTOS", "3-TITULOS", "3-TABLAS"): doc.layers.add(n, color=7)

def pl(pts, layer="3-TABLAS", lw=25, close=False):
    return msp.add_lwpolyline(pts, close=close, dxfattribs={"layer": layer, "lineweight": lw})
def txt(s, x, y, h=2.5, align=TA.LEFT, layer="3-TEXTOS", bold=False):
    t = msp.add_text(s, height=h, dxfattribs={"layer": layer, "style": "ARIAL-NEGRITA" if bold else "ARIAL", "width": 0.9})
    t.set_placement((x, y), align=align); return t
def gris(x0, y0, x1, y1):
    h = msp.add_hatch(color=254, dxfattribs={"layer": "3-TABLAS"}); h.set_solid_fill(color=254, rgb=(232, 232, 232))
    h.paths.add_polyline_path([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], is_closed=True)
def num(v, d=2):
    s = f"{v:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return s

def tabla(x0, ytop, titulo, cols, filas, total=None, h=7.0, th=2.8):
    """cols = [(encabezado, ancho, 'l'|'c')]; encabezados de 2 líneas separados por '|'."""
    x1 = x0 + sum(c[1] for c in cols)
    filas = filas + ([total] if total else [])
    hh = 2 * h                                   # alto de la fila de encabezados
    yb = ytop - h - hh - len(filas) * h
    gris(x0, ytop - h - hh, x1, ytop)
    if total: gris(x0, yb, x1, yb + h)
    txt(titulo, (x0 + x1) / 2, ytop - h / 2, 3.0, TA.MIDDLE_CENTER, "3-TABLAS", True)
    pl([(x0, ytop - h), (x1, ytop - h)], lw=18)
    for i in range(len(filas) + 1):
        y = ytop - h - hh - i * h
        pl([(x0, y), (x1, y)], lw=35 if i in (0, len(filas)) or (total and i == len(filas) - 1) else 13)
    xx = x0
    for j, (enc, w, al) in enumerate(cols):
        if j: pl([(xx, ytop - h), (xx, yb)], lw=13)
        ls = enc.split("|")
        for k, l in enumerate(ls):
            txt(l, xx + w / 2, ytop - h - hh / 2 + (len(ls) - 1) * 1.7 - k * 3.4, th, TA.MIDDLE_CENTER, "3-TABLAS", True)
        for i, f in enumerate(filas):
            y = ytop - h - hh - (i + 0.5) * h
            bold = total is not None and i == len(filas) - 1
            if al == "c": txt(f[j], xx + w / 2, y, th, TA.MIDDLE_CENTER, "3-TABLAS", bold)
            else: txt(f[j], xx + 1.5, y, th, TA.MIDDLE_LEFT, "3-TABLAS", bold)
        xx += w
    pl([(x0, ytop), (x1, ytop), (x1, yb), (x0, yb)], lw=50, close=True)
    return yb

# ============================================================== DATOS ADOPTADOS (EDIFICIO ESTÁNDAR)
LARGO, ANCHO = 20.0, 12.0          # planta rectangular (m)
VANO = 4.0                         # separación de columnas = largo del panel (luz máx. del panel 4,50 m)
HILERAS = 8                        # paneles horizontales de 1,00 m: arranque ±0,00 a cupertina +8,00
ANCHO_UTIL = 1.0
ESP = "0,08"
CW_ALTO = 7.0                      # frente vidriado: curtain wall de ±0,00 a +7,00; arriba 1 hilera de panel (parapeto)
VENT_A, VENT_H = 2.0, 1.0          # ventana corrediza
PUERTA_A, PUERTA_H = 1.0, 2.0      # puerta de servicio
VENT_POR_PISO = 4                  # en el contrafrente, una por vano (salvo el vano central)
DECK_LARGO, DECK_ANCHO = 6.0, 1.0  # chapa colaborante: 2 tramos de 6,00 m cubren los 12,00 m

nv_largo, nv_ancho = int(LARGO / VANO), int(ANCHO / VANO)

# paneles por fachada: lista de (largo_pieza, cantidad, función)
piezas = []
# laterales: sin aberturas
piezas.append((VANO, 2 * HILERAS * nv_ancho, "Muro perimetral - laterales"))
# frente: solo la hilera del parapeto sobre el curtain wall
piezas.append((VANO, (HILERAS - int(CW_ALTO)) * nv_largo, "Muro perimetral - frente (parapeto)"))
# contrafrente: ventanas en la hilera 2 (PB) y en la 5 (PA) en 4 vanos; puerta en el vano central, hileras 1 y 2
central = nv_largo // 2
hil_vent = (2, 5)
completos = 0; cortos_v = 0; cortos_p = 0
for fila in range(1, HILERAS + 1):
    for b in range(nv_largo):
        if fila in hil_vent and b != central: cortos_v += 2              # panel cortado a cada lado de la ventana
        elif b == central and fila <= int(PUERTA_H): cortos_p += 2      # panel cortado a cada lado de la puerta
        else: completos += 1
piezas.append((VANO, completos, "Muro perimetral - contrafrente"))
piezas.append(((VANO - VENT_A) / 2, cortos_v, "Contrafrente - a los lados de ventanas"))
piezas.append(((VANO - PUERTA_A) / 2, cortos_p, "Contrafrente - a los lados de la puerta"))

filas_m = []; tot_cant = tot_m2 = tot_ml = 0
for largo, cant, func in piezas:
    m2 = largo * ANCHO_UTIL * cant; ml = largo * cant
    tot_cant += cant; tot_m2 += m2; tot_ml += ml
    filas_m.append(("Panel sándwich", num(ANCHO_UTIL), num(largo), ESP, str(cant), num(m2, 2), num(ml, 2), func, ""))
deck_cant = int(LARGO / DECK_ANCHO) * int(ANCHO / DECK_LARGO)
filas_d = []
for nivel in ("Entrepiso (losa +3,80)", "Cubierta (losa +7,40)"):
    m2 = deck_cant * DECK_LARGO * DECK_ANCHO
    filas_d.append(("Chapa colaborante", num(DECK_ANCHO), num(DECK_LARGO), "0,9 mm", str(deck_cant), num(m2, 2),
                    num(deck_cant * DECK_LARGO, 2), nivel, ""))
m2_panel = tot_m2

# control: m² de panel = superficie opaca bruta - aberturas
bruto = 2 * ANCHO * HILERAS + LARGO * HILERAS + LARGO * (HILERAS - CW_ALTO)
aberturas = len(hil_vent) * VENT_POR_PISO * VENT_A * VENT_H + PUERTA_A * PUERTA_H
assert abs(m2_panel - (bruto - aberturas)) < 1e-6, (m2_panel, bruto, aberturas)

carp = [("Aluminio", num(VENT_A), num(VENT_H), "Corrediza", len(hil_vent) * VENT_POR_PISO),
        ("Aluminio", num(PUERTA_A), num(PUERTA_H), "Puerta de servicio", 1),
        ("Aluminio", num(LARGO), num(CW_ALTO), "Curtain wall (frente)", 1)]
filas_c = []; tot_c = 0
for mat, a, h, tipo, n in carp:
    m2 = float(a.replace(",", ".")) * float(h.replace(",", ".")) * n; tot_c += m2
    filas_c.append((mat, a, h, tipo, str(n), num(m2, 2), ""))

# ============================================================== HOJA
pl([(10, 10), (W - 10, 10), (W - 10, H - 10), (10, H - 10)], "0-MARCO", 50, True)
txt("CÓMPUTO DE MATERIALES", W / 2, 392, 8.0, TA.MIDDLE_CENTER, "3-TITULOS", True)
txt("CERRAMIENTOS: OPACOS Y VIDRIADOS  -  CORTE INTEGRAL ACERO", W / 2, 381, 3.4, TA.MIDDLE_CENTER, "3-TITULOS")
pl([(15, 375), (W - 15, 375)], "3-TITULOS", 70)

COLS = [("Material", 36, "l"), ("Ancho|del panel", 19, "c"), ("Largo|del panel", 19, "c"), ("Espesor", 18, "c"),
        ("Cantidad|de piezas", 21, "c"), ("m²|necesarios", 23, "c"), ("Metros lineales|necesarios", 31, "c"),
        ("Función", 80, "l"), ("Precio|por m²", 20, "c")]
yb = tabla(15, 366, "CÓMPUTO DE MUROS - PANEL OPACO 80 mm", COLS, filas_m,
           total=("TOTAL", "", "", "", str(tot_cant), num(m2_panel, 2), num(tot_ml, 2), "", ""))
yb = tabla(15, yb - 14, "CÓMPUTO DE ENTREPISO Y CUBIERTA", COLS, filas_d,
           total=("TOTAL", "", "", "", str(2 * deck_cant), num(2 * deck_cant * DECK_LARGO * DECK_ANCHO, 2),
                  num(2 * deck_cant * DECK_LARGO, 2), "", ""))
yb2 = tabla(15, yb - 14, "CÓMPUTO DE CARPINTERÍA DE ALUMINIO",
            [("Material", 36, "l"), ("Ancho", 22, "c"), ("Alto", 22, "c"), ("Tipo", 60, "l"),
             ("Cantidad de|carpinterías", 32, "c"), ("m²|necesarios", 32, "c"), ("Precio|por m²", 63, "c")],
            filas_c, total=("TOTAL", "", "", "", str(sum(c[4] for c in carp)), num(tot_c, 2), ""))

# datos adoptados
y = yb2 - 16
txt("DATOS ADOPTADOS (edificio estándar, sin planos acotados)", 15, y, 3.2, TA.LEFT, "3-TITULOS", True)
pl([(15, y - 2), (W - 15, y - 2)], "3-TITULOS", 25)
notas = [f"Planta rectangular {num(LARGO)} x {num(ANCHO)} m; columnas IPN 300 cada {num(VANO)} m ({nv_largo} vanos en el largo, {nv_ancho} en el ancho).",
         f"Dos niveles: entrepiso +3,80 y cubierta +7,40, losas con chapa colaborante. Cupertina a +8,00.",
         f"Panel sándwich PUR 80 mm, ancho útil 1,00 m, colocado horizontal entre columnas: piezas de {num(VANO)} m, {HILERAS} hileras por fachada.",
         f"Frente: curtain wall de {num(LARGO)} x {num(CW_ALTO)} m y una hilera de panel arriba (parapeto). Laterales: panel completo.",
         f"Contrafrente: {VENT_POR_PISO} ventanas corredizas {num(VENT_A)} x {num(VENT_H)} m por planta y una puerta de servicio {num(PUERTA_A)} x {num(PUERTA_H)} m.",
         f"Control: superficie opaca bruta {num(bruto)} m² - aberturas {num(aberturas)} m² = {num(m2_panel)} m² de panel.",
         "Medidas en metros. m² = ancho x largo x cantidad; metros lineales = largo x cantidad. Sin desperdicio."]
for i, n in enumerate(notas):
    txt(f"{i + 1}. {n}", 15, y - 8 - i * 6.0, 2.8)

# rótulo
ry0, ry1 = 12, 30
xs = [15, 62, 175, 225, 282]
pl([(xs[0], ry0), (xs[-1], ry0), (xs[-1], ry1), (xs[0], ry1)], "0-MARCO", 50, True)
for x in xs[1:-1]: pl([(x, ry0), (x, ry1)], "0-MARCO", 25)
txt("LÁMINA 4", (xs[0] + xs[1]) / 2, 22.5, 5.0, TA.MIDDLE_CENTER, "3-TITULOS", True)
txt("FECHA: 19/10/26", xs[0] + 2, 14, 2.0)
txt("DOCENTE: Arq. Tucci y Arq. Cardozo", xs[1] + 2, 26, 2.0)
txt("ALUMNOS: Azcona Karina, Gómez Karen, Rosales Abril,", xs[1] + 2, 22, 2.0)
txt("Vitale Candelaria", xs[1] + 18.5, 18.6, 2.0)
txt("GRUPO: 13", xs[1] + 2, 14, 2.0)
txt("NIVEL:", xs[2] + 2, 26, 2.0); txt("OBS:", xs[2] + 2, 22, 2.0)
txt("CONSTRUCCIONES II", xs[3] + 2, 24.5, 2.4)
txt("CATEDRA: ARQ. TUCCI", xs[3] + 2, 19, 2.4)
txt("A3 - imprimir al 100%", xs[3] + 2, 14, 2.0)

doc.saveas(f"{OUT}/Lamina4_Computo_Materiales_A3.dxf")
print("panel", tot_cant, m2_panel, "carp", tot_c)
