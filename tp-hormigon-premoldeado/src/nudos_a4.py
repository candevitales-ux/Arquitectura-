# -*- coding: utf-8 -*-
"""Práctica en clase NUDOS (Construcciones II - UNM): 6 nudos en corte, escala 1:20, hojas A4 verticales.
Los nudos son ventanas del MISMO corte integral de los TP (src/opaco_corte.py y src/tp_corte.py): la geometría se toma
de esos scripts y solo se agregan encuadre, niveles, cotas, referencias (denominación / especificación / función) y rótulo.
Salidas: build/nudos/Nudos_A4.html (-> PDF con Chromium) y build/nudos/dxf/*.dxf (1 por lámina, modelo en mm reales,
presentación A4 c/ ventana a 1:20 -> DWG con ODAFileConverter)."""
import os, math, html, json
from PIL import ImageFont
import ezdxf
from ezdxf.enums import TextEntityAlignment
import nudos_refs as NR

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = "build/nudos"
os.makedirs(OUT + "/dxf", exist_ok=True)
for _d in ("dxf", "dwg", "png"):
    os.makedirs(f"{OUT}/{_d}", exist_ok=True)
    for _f in os.listdir(f"{OUT}/{_d}"): os.remove(f"{OUT}/{_d}/{_f}")

def load(fn):
    g = {"__file__": os.path.join(HERE, fn), "__name__": "nudos_src"}
    exec(compile(open(g["__file__"], encoding="utf-8").read(), fn, "exec"), g)
    return g
V = load("tp_corte.py")
O = load("opaco_corte.py")

FONT = {False: ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 100),
        True: ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 100)}
def tw(s, size, bold=False): return FONT[bold].getlength(s) * size / 100.0
def wrap(s, size, width, bold=False):
    out, cur = [], ""
    for w in s.split():
        t = (cur + " " + w).strip()
        if tw(t, size, bold) <= width or not cur: cur = t
        else: out.append(cur); cur = w
    if cur: out.append(cur)
    return out

W, H = 210.0, 297.0
FECHA = "22/10/2026"
f = lambda v: f"{v:.3f}"

class Sheet:
    def __init__(self, code, title):
        self.code, self.title, self.A, self.geo = code, title, [], []
    # primitivas en mm de papel (y hacia abajo)
    def line(self, pts, sw=0.15, stroke="#000", dash=None, layer="X-TEXTOS"):
        self.A.append(dict(t="line", pts=pts, sw=sw, stroke=stroke, dash=dash, layer=layer))
    def rect(self, x, y, w, h, fill="none", stroke="#000", sw=0.2, layer="X-ROTULO"):
        self.A.append(dict(t="rect", x=x, y=y, w=w, h=h, fill=fill, stroke=stroke, sw=sw, layer=layer))
    def poly(self, pts, fill="#000", layer="X-NIVELES"):
        self.A.append(dict(t="poly", pts=pts, fill=fill, layer=layer))
    def circle(self, x, y, r, fill="#fff", stroke="#000", sw=0.2, layer="X-REFERENCIAS"):
        self.A.append(dict(t="circle", x=x, y=y, r=r, fill=fill, stroke=stroke, sw=sw, layer=layer))
    def text(self, x, y, s, size=2.5, anchor="start", bold=False, ital=False, rot=0, fill="#000", layer="X-TEXTOS"):
        self.A.append(dict(t="text", x=x, y=y, s=s, size=size, anchor=anchor, bold=bold, ital=ital, rot=rot, fill=fill, layer=layer))

# ===================================================================== marco + rótulo
SHEETS = []
def frame(sh, n_tot):
    sh.rect(0.3, 0.3, W - 0.6, H - 0.6, sw=0.3, layer="X-MARCO")
    sh.rect(10, 10, W - 20, H - 20, sw=0.5, layer="X-MARCO")
    y0, y1 = 268.0, 287.0
    sh.rect(10, y0, 190, y1 - y0, sw=0.5)
    for x in (62, 120, 168): sh.line([(x, y0), (x, y1)], 0.25, layer="X-ROTULO")
    sh.text(12, y0 + 5.0, "PRÁCTICA EN CLASE · NUDOS", 3.2, bold=True, layer="X-ROTULO")
    for k, s in enumerate(wrap(sh.title, 2.3, 48)[:3]):
        sh.text(12, y0 + 9.6 + k * 3.0, s, 2.3, layer="X-ROTULO")
    sh.text(64, y0 + 5.0, "DOCENTE: Arq. Tucci y Arq. Cardozo", 2.4, layer="X-ROTULO")
    sh.text(64, y0 + 9.3, "ALUMNA: Candelaria Vitale", 2.4, layer="X-ROTULO")
    sh.text(64, y0 + 13.6, "GRUPO: 13", 2.4, layer="X-ROTULO")
    sh.text(122, y0 + 5.0, "CONSTRUCCIONES II · UNM", 2.4, bold=True, layer="X-ROTULO")
    sh.text(122, y0 + 9.3, "CÁTEDRA: ARQ. TUCCI", 2.4, layer="X-ROTULO")
    sh.text(122, y0 + 13.6, f"FECHA: {FECHA}", 2.4, layer="X-ROTULO")
    sh.text(170, y0 + 5.0, "LÁMINA", 2.2, layer="X-ROTULO")
    sh.text(198, y0 + 9.6, f"{sh.code}/{n_tot:02d}", 4.2, "end", bold=True, layer="X-ROTULO")
    sh.text(170, y0 + 15.5, sh.scale_txt, 2.4, bold=True, layer="X-ROTULO")

# ===================================================================== nudos
NUDOS = [
 dict(n=1, ns=O, refs=NR.N1, t="CUBIERTA CON CERRAMIENTO EXTERIOR OPACO", win=(-350, 7440, 1900, 9560),
      sub="Panel sándwich premoldeado H°A como parapeto · canaleta H°A in situ · VL + viga de borde + losa TT",
      niv=[(9472, "+9,47", -300, "r", ""), (9092, "+9,09", 1830, "l", "Cubierta terminada"), (8915, "+8,92", 1830, "l", ""),
           (7500, "+7,50", 1830, "l", "Cielorraso")],
      cv=[(8005, 8705, 900, "0,70"), (8705, 8965, 900, "0,26"), (8265, 8915, 1580, "0,65"), (9092, 9440, -60, "0,35")],
      ch=[(30, 230, 7640, "20"), (230, 250, 7640, "2"), (250, 650, 7640, "40")],
      notes=[(980, 7640, "Columna, ménsula de la VP y VP en vista")]),
 dict(n=2, ns=V, refs=NR.N2, t="CUBIERTA CON CERRAMIENTO EXTERIOR VIDRIADO", win=(-350, 7440, 1900, 9560),
      sub="Muro cortina stick (aluminio + DVH) colgado de la estructura · zócalo H°A in situ · VL + viga L + losa TT",
      niv=[(9472, "+9,47", -300, "r", ""), (9092, "+9,09", 1830, "l", "Cubierta terminada"), (8915, "+8,92", 1830, "l", ""),
           (7500, "+7,50", 1830, "l", "Cielorraso")],
      cv=[(8005, 8705, 900, "0,70"), (8705, 8965, 900, "0,26"), (8265, 8915, 1580, "0,65"), (8968, 9440, 220, "0,47")],
      ch=[(-32, 182, 7640, "21"), (182, 250, 7640, "7"), (250, 650, 7640, "40")],
      notes=[(980, 7640, "Columna, ménsula de la VP y VP en vista")]),
 dict(n=3, ns=O, refs=NR.N3, t="ENTREPISO CON CERRAMIENTO EXTERIOR OPACO", win=(-350, 2940, 1900, 4850),
      sub="Panel sándwich fijado a la VL con bulón pasante · viga L de borde + losa TT + capa de compresión",
      niv=[(4500, "+4,50", 1250, "r", "N.P.T. P. Alta"), (3000, "+3,00", 1830, "l", "Cielorraso P. Baja")],
      cv=[(3505, 4205, 900, "0,70"), (4205, 4465, 900, "0,26"), (3765, 4415, 1580, "0,65")],
      ch=[(30, 230, 3120, "20"), (230, 250, 3120, "2"), (250, 650, 3120, "40")],
      notes=[(980, 3140, "Columna, ménsula de la VP y VP en vista")]),
 dict(n=4, ns=V, refs=NR.N4, t="ENTREPISO CON CERRAMIENTO EXTERIOR VIDRIADO", win=(-350, 2940, 1900, 4850),
      sub="Muro cortina stick: grapa al riel de la viga L, junta de dilatación y barrera cortafuego en el frente de losa",
      niv=[(4500, "+4,50", 1250, "r", "N.P.T. P. Alta"), (3000, "+3,00", 1830, "l", "Cielorraso P. Baja")],
      cv=[(3505, 4205, 900, "0,70"), (4205, 4465, 900, "0,26"), (3765, 4415, 1580, "0,65")],
      ch=[(-32, 182, 3120, "21"), (182, 250, 3120, "7"), (250, 650, 3120, "40")],
      notes=[(980, 3140, "Columna, ménsula de la VP y VP en vista")]),
 dict(n=5, ns=O, refs=NR.N5, t="PISO SOBRE TERRENO NATURAL CON CERRAMIENTO EXTERIOR OPACO Y FUNDACIÓN", win=(-800, -2200, 1600, 820),
      sub="Panel apoyado en viga portapanel s/ cuello · base aislada H°A in situ c/ cuello (anclaje mecánico húmedo)",
      niv=[(0, "±0,00", 1250, "r", "N.P.T. P. Baja"), (-150, "-0,15", -700, "r", "Vereda"), (-510, "-0,51", 1530, "l", "Sup. cuello"),
           (-2150, "-2,15", -300, "r", "Fundación")],
      cv=[(-2050, -1750, 1540, "0,30"), (-1350, -510, 1150, "0,84"), (-2150, 0, -740, "2,15")],
      ch=[(-550, 1450, -2170, "2,00", True), (-75, 975, -1420, "1,05", False), (30, 230, 760, "20", False)],
      notes=[(1050, -1480, "Fundación cortada por el eje de columna")]),
 dict(n=6, ns=V, refs=NR.N6, t="PISO SOBRE TERRENO NATURAL CON CERRAMIENTO EXTERIOR VIDRIADO Y FUNDACIÓN", win=(-800, -2200, 1600, 820),
      sub="Muro cortina colgado del entrepiso con perfil guía deslizante · base aislada H°A in situ c/ cuello",
      niv=[(0, "±0,00", 1250, "r", "N.P.T. P. Baja"), (-150, "-0,15", -700, "r", "Vereda"), (-510, "-0,51", 1530, "l", "Sup. cuello"),
           (-2150, "-2,15", -300, "r", "Fundación")],
      cv=[(-2050, -1750, 1540, "0,30"), (-1350, -510, 1150, "0,84"), (-2150, 0, -740, "2,15")],
      ch=[(-550, 1450, -2170, "2,00", True), (-75, 975, -1420, "1,05", False), (-32, 182, 760, "21", False)],
      notes=[(1050, -1480, "Fundación cortada por el eje de columna")]),
]

DEN = 20.0
AREA = (12.0, 36.0, 198.0, 250.0)     # zona de dibujo (x0, y0, x1, y1) en papel

def place(L, gap, ymin, ymax):
    """etiquetas 1D: grupos que se solapan se centran en la media de sus puntos, dentro de [ymin, ymax]"""
    cl = [[p] for p in L]
    def pos(c):
        m = sum(p["ay"] for p in c) / len(c); y0 = m - gap * (len(c) - 1) / 2
        return min(max(y0, ymin), ymax - gap * (len(c) - 1))
    while True:
        done = True
        for i in range(len(cl) - 1):
            if pos(cl[i]) + gap * len(cl[i]) > pos(cl[i + 1]) + 1e-6:
                cl[i] = cl[i] + cl.pop(i + 1); done = False; break
        if done: break
    for c in cl:
        y0 = pos(c)
        for k, p in enumerate(c): p["by"] = y0 + k * gap

def drawing_sheet(nd, code):
    sh = Sheet(code, f"Nudo {nd['n']}: {nd['t'].capitalize()} - corte 1:20"); sh.scale_txt = "ESC. 1:20"
    wx0, wy0, wx1, wy1 = nd["win"]
    dw, dh = (wx1 - wx0) / DEN, (wy1 - wy0) / DEN
    ax = AREA[0] + (AREA[2] - AREA[0] - dw) / 2
    ay = AREA[1] + 14
    sh.geo.append(dict(ns=nd["ns"], win=nd["win"], at=(ax, ay), den=DEN))
    P = lambda x, y: (ax + (x - wx0) / DEN, ay + (wy1 - y) / DEN)
    # encabezado
    sh.text(14, 19, f"NUDO {nd['n']}", 6.0, bold=True)
    sh.text(42, 19, nd["t"], 3.6 if len(nd["t"]) < 46 else 3.0, bold=True)
    sh.text(42, 24.5, "Corte vertical por la zona de apoyo de la viga VL · ESCALA 1:20", 2.6)
    sh.text(42, 29.0, nd["sub"], 2.2, ital=True, fill="#333")
    sh.line([(10, 32.5), (200, 32.5)], 0.25)
    sh.rect(ax, ay, dw, dh, fill="none", stroke="#999", sw=0.08, layer="X-TEXTOS")
    # eje de columna
    x0p, y0p = P(450, wy1); _, y1p = P(450, wy0)
    sh.line([(x0p, y0p - 4), (x0p, y1p)], 0.13, "#c00", dash="4 0.8 0.6 0.8", layer="X-EJES")
    sh.circle(x0p, y0p - 6.4, 2.4, fill="#fff", stroke="#c00", sw=0.18, layer="X-EJES")
    sh.text(x0p, y0p - 5.4, "C", 2.6, "middle", bold=True, fill="#c00", layer="X-EJES")
    # exterior / interior
    exx = P(wx0 + 40, 0)[0]; inx = P(wx1 - 40, 0)[0]
    sh.text(exx, ay - 1.6, "EXTERIOR", 2.6, fill="#555")
    sh.text(inx, ay - 1.6, "INTERIOR", 2.6, "end", fill="#555")
    # niveles
    for y, txt, xr, side, sub in nd["niv"]:
        px, py = P(xr, y)
        sh.poly([(px, py), (px - 1.2, py - 2), (px + 1.2, py - 2)])
        sh.line([(px - 3.6, py), (px + 3.6, py)], 0.15, layer="X-NIVELES")
        tx = px + 1.7 if side == "r" else px - 1.7; an = "start" if side == "r" else "end"
        sh.text(tx, py - 2.4, txt, 2.6, an, bold=True, layer="X-NIVELES")
        if sub: sh.text(tx, py + 3.0, sub, 2.0, an, ital=True, layer="X-NIVELES")
    # cotas
    def tick(x, y): sh.line([(x - 0.7, y + 0.7), (x + 0.7, y - 0.7)], 0.25, layer="X-COTAS")
    for y0, y1, xr, txt in nd["cv"]:
        (px, p0), (_, p1) = P(xr, y0), P(xr, y1)
        sh.line([(px, p0), (px, p1)], 0.12, layer="X-COTAS")
        for p in (p0, p1): tick(px, p); sh.line([(px - 1.1, p), (px + 1.4, p)], 0.1, layer="X-COTAS")
        sh.text(px - 0.8, (p0 + p1) / 2, txt, 2.2, "middle", rot=-90, layer="X-COTAS")
    for c in nd["ch"]:
        x0, x1, yr, txt = c[:4]; below = c[4] if len(c) > 4 else False
        (a, py), (b, _) = P(x0, yr), P(x1, yr)
        sh.line([(a, py), (b, py)], 0.12, layer="X-COTAS")
        for p in (a, b): tick(p, py); sh.line([(p, py - 1.1), (p, py + 1.1)], 0.1, layer="X-COTAS")
        sh.text((a + b) / 2, py + (2.8 if below else -0.8), txt, 2.2 if len(txt) > 2 else 1.9, "middle", layer="X-COTAS")
    for xr, yr, s in nd.get("notes", []):
        px, py = P(xr, yr); sh.text(px, py, s, 2.0, ital=True, fill="#333")
    # referencias (globos): izquierda = cerramiento (x < 250), derecha = estructura e interior
    pts = []; TOPK = set(NR.TOP[nd["n"]])
    for k, x, y in nd["refs"]:
        px, py = P(x, y); pts.append(dict(k=k, ax=px, ay=py, side="T" if k in TOPK else ("L" if x < 250 else "R")))
    gap = 5.3; ymin, ymax = ay - 6, ay + dh + 6
    num = 0; order = []
    for side in ("L", "T", "R"):
        if side == "T":
            L = sorted([p for p in pts if p["side"] == "T"], key=lambda p: p["ax"])
            tmp = [{"ay": p["ax"]} for p in L]; place(tmp, 5.8, ax + dw * 0.42, inx - 16)
            byt = ay - 9.5
            for p, t in zip(L, tmp):
                num += 1; p["n"] = num; order.append(p)
                sh.line([(p["ax"], p["ay"]), (t["by"], byt + 2.35)], 0.11, layer="X-REFERENCIAS")
                sh.circle(p["ax"], p["ay"], 0.35, fill="#000", stroke="none", sw=0)
                sh.circle(t["by"], byt, 2.35)
                sh.text(t["by"], byt + 1.0, str(num), 2.6, "middle", bold=True, layer="X-REFERENCIAS")
            continue
        L = sorted([p for p in pts if p["side"] == side], key=lambda p: p["ay"])
        place(L, gap, ymin, ymax); side = side == "L"
        bx = ax - 9 if side else ax + dw + 9
        for p in L:
            num += 1; p["n"] = num; order.append(p)
            ex = bx + 6 if side else bx - 6
            sh.line([(p["ax"], p["ay"]), (ex, p["by"]), (bx + (2.35 if side else -2.35), p["by"])], 0.11, layer="X-REFERENCIAS")
            sh.circle(p["ax"], p["ay"], 0.35, fill="#000", stroke="none", sw=0)
            sh.circle(bx, p["by"], 2.35)
            sh.text(bx, p["by"] + 1.0, str(num), 2.6, "middle", bold=True, layer="X-REFERENCIAS")
    # leyenda: denominaciones (la especificación y la función van en la planilla)
    ly = ay + dh + 14
    sh.text(14, ly, "REFERENCIAS", 2.8, bold=True)
    sh.text(42, ly, "denominación (especificación técnica y función: ver planilla de la lámina siguiente)", 2.1, ital=True, fill="#333")
    nrow = math.ceil(len(order) / 3); size = 2.15
    lh = min(3.1, (250 - ly - 4) / max(nrow, 1))
    for i, p in enumerate(order):
        col, row = divmod(i, nrow); x = 14 + col * 62.5; y = ly + 4.2 + row * lh
        sh.text(x + 3.5, y, str(p["n"]), size, "end", bold=True)
        d = NR.R[p["k"]][0]
        while tw(d, size) > 57 and " " in d: d = d.rsplit(" ", 1)[0]
        sh.text(x + 4.6, y, d, size)
    # escala gráfica
    gx, gy = 14, 258.5
    sh.text(gx, gy - 2.0, "ESCALA GRÁFICA 1:20", 2.2, bold=True)
    for i in range(10):
        sh.rect(gx + i * 5, gy, 5, 1.6, fill="#000" if i % 2 == 0 else "#fff", stroke="#000", sw=0.12, layer="X-TEXTOS")
    for i, lab in ((0, "0"), (5, "0,50"), (10, "1,00 m")):
        sh.text(gx + i * 5, gy + 4.6, lab, 2.0, "middle" if i < 10 else "start")
    sh.text(198, 257.0, "Cotas en m (secciones en cm) · niveles en m respecto del N.P.T. P. Baja ±0,00", 2.0, "end", ital=True)
    sh.text(198, 265.0, "Hormigón premoldeado de grandes luces (sistema Pi) · mismo edificio del corte integral del TP", 2.0, "end", ital=True)
    return sh, [(p["n"], p["k"]) for p in order]

COLS = [("N°", 8), ("DENOMINACIÓN", 40), ("ESPECIFICACIÓN TÉCNICA DE MATERIALES", 78), ("FUNCIÓN", 60)]
def table_sheets(nd, items, code0):
    out = []; size, lh = 2.25, 2.8
    rows = []
    for n, k in items:
        d, e, fn = NR.R[k]
        cells = [[str(n)], wrap(d, size, COLS[1][1] - 2.4, True), wrap(e, size, COLS[2][1] - 2.4), wrap(fn, size, COLS[3][1] - 2.4)]
        rows.append((cells, max(len(c) for c in cells) * lh + 1.5))
    ytop, ybot = 41.0, 264.0
    i = 0; part = 0
    while i < len(rows):
        part += 1
        sh = Sheet(f"{code0 + part - 1:02d}", f"Nudo {nd['n']}: planilla de referencias" + (" (cont.)" if part > 1 else "")); sh.scale_txt = "SIN ESCALA"
        sh.text(14, 19, f"NUDO {nd['n']}", 6.0, bold=True)
        sh.text(42, 19, nd["t"], 3.6 if len(nd["t"]) < 46 else 3.0, bold=True)
        sh.text(42, 24.5, "REFERENCIAS: denominación, especificación técnica de materiales y función" + (" (cont.)" if part > 1 else ""), 2.6)
        sh.text(42, 29.0, f"Corresponde al dibujo en escala 1:20 de la lámina {int(code0) - 1:02d}", 2.2, ital=True, fill="#333")
        sh.line([(10, 32.5), (200, 32.5)], 0.25)
        x = 12.0; hh = 6.0
        sh.rect(12, ytop - hh, 186, hh, fill="#d9d9d9", stroke="#000", sw=0.25, layer="X-TABLA")
        for name, w in COLS:
            sh.text(x + (w / 2 if name == "N°" else 1.2), ytop - 2.0, name, 2.3, "middle" if name == "N°" else "start", bold=True, layer="X-TABLA")
            x += w
        y = ytop
        while i < len(rows) and y + rows[i][1] <= ybot:
            cells, rh = rows[i]
            if i % 2 == 1: sh.rect(12, y, 186, rh, fill="#f2f2f2", stroke="none", sw=0, layer="X-TABLA")
            x = 12.0
            for ci, (c, (name, w)) in enumerate(zip(cells, COLS)):
                for li, s in enumerate(c):
                    if ci == 0:
                        sh.circle(x + w / 2, y + 2.15, 1.75, layer="X-TABLA")
                        sh.text(x + w / 2, y + 2.95, s, 2.2, "middle", bold=True, layer="X-TABLA")
                    else:
                        sh.text(x + 1.2, y + 2.85 + li * lh, s, size, bold=(ci == 1), layer="X-TABLA")
                x += w
            y += rh
            sh.line([(12, y), (198, y)], 0.1, layer="X-TABLA")
            i += 1
        x = 12.0
        for name, w in COLS[:-1]:
            x += w; sh.line([(x, ytop - hh), (x, y)], 0.15, layer="X-TABLA")
        sh.rect(12, ytop - hh, 186, y - ytop + hh, fill="none", stroke="#000", sw=0.3, layer="X-TABLA")
        out.append(sh)
    return out

# ===================================================================== carátula
def caratula():
    sh = Sheet("01", "Carátula, consigna e índice; ubicación de los nudos en los cortes integrales"); sh.scale_txt = "ESC. 1:100"
    sh.text(14, 24, "CONSTRUCCIONES II · UNM", 4.0, bold=True)
    sh.text(14, 36, "NUDOS", 11.0, bold=True)
    sh.text(14, 44, "PRÁCTICA EN CLASE · HORMIGÓN PREMOLDEADO DE GRANDES LUCES", 3.2)
    sh.line([(14, 48), (196, 48)], 0.3)
    cons = ["Nudos pertenecientes al proyecto del trabajo práctico, dibujados en forma proporcionada a escala 1:20,",
            "con referencias que incluyen función, denominación y especificación técnica de los materiales."]
    for k, s in enumerate(cons): sh.text(14, 54 + k * 3.6, s, 2.5)
    sh.text(14, 66, "ÍNDICE DE LÁMINAS (A4)", 3.0, bold=True)
    # cortes integrales esquemáticos a 1:100 c/ ubicación de nudos
    den = 100.0; win = (-800, -2250, 2000, 9600)
    dw, dh = (win[2] - win[0]) / den, (win[3] - win[1]) / den
    for j, (ns, lab) in enumerate(((O, "CERRAMIENTO OPACO"), (V, "CERRAMIENTO VIDRIADO"))):
        ax = 128 + j * 36; ay = 140
        sh.geo.append(dict(ns=ns, win=win, at=(ax, ay), den=den))
        sh.text(ax + dw / 2, ay - 6.5, "CORTE INTEGRAL", 2.2, "middle", bold=True)
        sh.text(ax + dw / 2, ay - 3.2, lab, 2.0, "middle")
        for nd in NUDOS:
            if nd["ns"] is not ns: continue
            x0, y0, x1, y1 = nd["win"]
            px0 = ax + (max(x0, win[0]) - win[0]) / den; px1 = ax + (min(x1, win[2]) - win[0]) / den
            py0 = ay + (win[3] - min(y1, win[3])) / den; py1 = ay + (win[3] - max(y0, win[1])) / den
            sh.rect(px0, py0, px1 - px0, py1 - py0, fill="none", stroke="#c00", sw=0.3, layer="X-REFERENCIAS")
            sh.circle(px0 - 3.2 if j == 0 else px1 + 3.2, (py0 + py1) / 2, 2.6, fill="#fff", stroke="#c00", sw=0.25)
            sh.text(px0 - 3.2 if j == 0 else px1 + 3.2, (py0 + py1) / 2 + 1.0, str(nd["n"]), 2.6, "middle", bold=True, fill="#c00", layer="X-REFERENCIAS")
    sh.text(160, 265.0, "Cortes integrales esquemáticos esc. 1:100 · en rojo, el encuadre de cada nudo", 2.0, "middle", ital=True)
    # descripción del sistema
    sis = [("SISTEMA CONSTRUCTIVO", True),
           ("Estructura de hormigón premoldeado de grandes", False), ("luces (sistema Pi): columnas 40x40 c/ ménsulas,", False),
           ("vigas VL doble T pretensadas en fachada, vigas VP", False), ("T invertida interiores y losas TT h 0,65 con capa", False),
           ("de compresión in situ. Bases aisladas de H°A", False), ("in situ con cuello (anclaje mecánico húmedo).", False),
           ("", False), ("CERRAMIENTOS", True),
           ("Opaco: panel sándwich premoldeado de H°A", False), ("(6 + EPS 6 + 8 cm) fijado a la VL con bulón", False),
           ("pasante y apoyado en viga portapanel.", False),
           ("Vidriado: muro cortina stick de aluminio con DVH", False), ("y spandrel, colgado de la estructura c/ grapas.", False)]
    for k, (s, b) in enumerate(sis): sh.text(14, 160 + k * 3.6, s, 2.4, bold=b)
    sh.text(14, 222, "CONVENCIONES", 2.6, bold=True)
    conv = [("url(#pHA)", "H° premoldeado (cortado)"), ("url(#pHAis)", "H°A in situ"), ("url(#pH)", "H° pobre / contrapiso"),
            ("url(#pEPS)", "EPS / H° liviano c/ EPS"), ("url(#pLana)", "Lana mineral"), ("url(#pTierra)", "Terreno natural"),
            ("#bfe3f0", "Vidrio"), ("#9aa3ab", "Aluminio")]
    for k, (fl, s) in enumerate(conv):
        x = 14 + (k % 2) * 52; y = 226 + (k // 2) * 7.5
        sh.rect(x, y, 9, 5, fill=fl, stroke="#000", sw=0.15, layer="X-TEXTOS")
        sh.text(x + 11, y + 3.7, s, 2.2)
    return sh

# ===================================================================== armado de láminas
sheets = [caratula()]
c = 2
for nd in NUDOS:
    sd, items = drawing_sheet(nd, f"{c:02d}")
    tabs = table_sheets(nd, items, c + 1)
    sheets += [sd] + tabs; c += 1 + len(tabs)
NTOT = len(sheets)
for k, s_ in enumerate(sheets):
    y = 71.5 + k * 3.55
    t_ = s_.title.split(" - ")[0]
    sheets[0].text(14, y, s_.code, 2.3, bold=True); sheets[0].text(22, y, t_, 2.3)
    sheets[0].text(196, y, {"SIN ESCALA": "—"}.get(s_.scale_txt, s_.scale_txt.replace("ESC. ", "")), 2.3, "end")
for sh in sheets: frame(sh, NTOT)

# ===================================================================== SVG / HTML (-> PDF)
def esc(s): return html.escape(s, quote=False)
def svg_prim(a):
    if a["t"] == "line":
        d = " ".join(f"{f(x)},{f(y)}" for x, y in a["pts"])
        da = f' stroke-dasharray="{a["dash"]}"' if a["dash"] else ""
        return f'<polyline points="{d}" fill="none" stroke="{a["stroke"]}" stroke-width="{a["sw"]}" stroke-linecap="round" stroke-linejoin="round"{da}/>'
    if a["t"] == "rect":
        return f'<rect x="{f(a["x"])}" y="{f(a["y"])}" width="{f(a["w"])}" height="{f(a["h"])}" fill="{a["fill"]}" stroke="{a["stroke"]}" stroke-width="{a["sw"]}"/>'
    if a["t"] == "poly":
        return f'<polygon points="{" ".join(f"{f(x)},{f(y)}" for x, y in a["pts"])}" fill="{a["fill"]}"/>'
    if a["t"] == "circle":
        return f'<circle cx="{f(a["x"])}" cy="{f(a["y"])}" r="{a["r"]}" fill="{a["fill"]}" stroke="{a["stroke"]}" stroke-width="{a["sw"]}"/>'
    if a["t"] == "text":
        r = f' transform="rotate({a["rot"]},{f(a["x"])},{f(a["y"])})"' if a["rot"] else ""
        return (f'<text x="{f(a["x"])}" y="{f(a["y"])}" font-size="{a["size"]}" text-anchor="{a["anchor"]}" fill="{a["fill"]}"'
                f'{" font-weight=\"bold\"" if a["bold"] else ""}{" font-style=\"italic\"" if a["ital"] else ""}{r}>{esc(a["s"])}</text>')

def svg_sheet(sh, idx):
    body = []
    for gi, g in enumerate(sh.geo):
        ns = g["ns"]; wx0, wy0, wx1, wy1 = g["win"]; ax, ay = g["at"]; k = 20.0 / g["den"]
        cid = f"c{idx}_{gi}"; ref = "full_o" if ns is O else "full_v"
        body.append(f'<clipPath id="{cid}"><rect x="{f(ax)}" y="{f(ay)}" width="{f((wx1-wx0)/g["den"])}" height="{f((wy1-wy0)/g["den"])}"/></clipPath>')
        body.append(f'<g clip-path="url(#{cid})"><g transform="translate({f(ax)},{f(ay)}) scale({k}) translate({f(-ns["X"](wx0))},{f(-ns["YC"](wy1))})"><use href="#{ref}"/></g></g>')
    body += [svg_prim(a) for a in sh.A]
    return (f'<div class="pg"><svg xmlns="http://www.w3.org/2000/svg" width="210mm" height="297mm" viewBox="0 0 210 297" '
            f'font-family="Liberation Sans, Arial, sans-serif"><rect width="210" height="297" fill="#fff"/>{"".join(body)}</svg></div>')

defs = "".join(V["defs"])
HTML = f'''<!doctype html><html><head><meta charset="utf-8"><title>Nudos A4</title><style>
@page {{ size: 210mm 297mm; margin: 0 }} html,body {{ margin:0; padding:0; background:#fff }}
.pg {{ width:210mm; height:297mm; overflow:hidden; page-break-after:always; break-after:page }} .pg svg {{ display:block }}
</style></head><body>
<svg xmlns="http://www.w3.org/2000/svg" width="0" height="0" style="position:absolute"><defs>{defs}
<g id="full_v">{"".join(V["full"])}</g><g id="full_o">{"".join(O["full"])}</g></defs></svg>
{"".join(svg_sheet(sh, i) for i, sh in enumerate(sheets))}
</body></html>'''
open(f"{OUT}/Nudos_A4.html", "w", encoding="utf-8").write(HTML)

# ===================================================================== DXF (1 por lámina)
LAYERS = {
    "A-HORMIGON-PREMOLDEADO": 8, "A-HORMIGON-INSITU": 33, "A-HORMIGON-SIMPLE": 9, "A-MORTERO-CARPETAS": 252, "A-GROUT": 251,
    "A-TERRENO": 32, "A-TOSCA": 42, "A-AISLACION-EPS": 50, "A-AISLACION-LANA": 40, "A-SOLADOS": 31, "A-VIDRIO": 4,
    "A-ALUMINIO": 253, "A-ACERO": 250, "A-NEOPRENO-SELLADORES": 7, "A-BARRERAS-MEMBRANAS": 7, "A-SELLADOR-INTUMESCENTE": 1,
    "A-YESO-CIELORRASO": 254, "A-ARMADURAS": 14, "A-VISTA": 8, "A-PROYECCION-OCULTO": 8, "A-CONTORNOS": 7,
    "X-EJES": 1, "X-COTAS": 3, "X-NIVELES": 7, "X-REFERENCIAS": 1, "X-TEXTOS": 7, "X-TABLA": 7, "X-ROTULO": 7, "X-MARCO": 7,
}
FILL = {
    "url(#pHA)": ("A-HORMIGON-PREMOLDEADO", "ANSI31", 8, 0), "url(#pHAis)": ("A-HORMIGON-INSITU", "AR-CONC", 1.2, 0),
    "url(#pH)": ("A-HORMIGON-SIMPLE", "AR-CONC", 0.8, 0), "url(#pMort)": ("A-MORTERO-CARPETAS", "AR-SAND", 0.6, 0),
    "url(#pHid)": ("A-MORTERO-CARPETAS", "AR-SAND", 0.4, 0), "url(#pGrout)": ("A-GROUT", "AR-SAND", 0.4, 0),
    "url(#pTierra)": ("A-TERRENO", "EARTH", 12, 45), "url(#pTosca)": ("A-TOSCA", "GRAVEL", 8, 0),
    "url(#pEPS)": ("A-AISLACION-EPS", "ZIGZAG", 6, 0), "url(#pEPSv)": ("A-AISLACION-EPS", "ZIGZAG", 6, 90),
    "url(#pLana)": ("A-AISLACION-LANA", "INSUL", 3, 0), "url(#pLanaV)": ("A-AISLACION-LANA", "INSUL", 3, 90),
    "url(#pPorc)": ("A-SOLADOS", "SOLID", 1, 0),
}
SOLID = {
    "#9aa3ab": ("A-ALUMINIO", (154, 163, 171)), "#b9c0c6": ("A-ALUMINIO", (185, 192, 198)), "#bfe3f0": ("A-VIDRIO", (191, 227, 240)),
    "#6f8796": ("A-VIDRIO", (111, 135, 150)), "#3b3b3b": ("A-ACERO", (59, 59, 59)), "#333": ("A-ACERO", (51, 51, 51)),
    "#555": ("A-ACERO", (85, 85, 85)), "#111": ("A-NEOPRENO-SELLADORES", (17, 17, 17)), "#222": ("A-NEOPRENO-SELLADORES", (34, 34, 34)),
    "#000": ("A-BARRERAS-MEMBRANAS", (0, 0, 0)), "#8d8d8d": ("A-MORTERO-CARPETAS", (141, 141, 141)), "#888": ("A-ACERO", (136, 136, 136)),
    "#c0392b": ("A-SELLADOR-INTUMESCENTE", (192, 57, 43)), "#cdbb9c": ("A-SOLADOS", (205, 187, 156)),
}
def lw(sw):
    for k in (13, 18, 20, 25, 30, 35, 40, 50):
        if sw * 100 <= k + 2: return k
    return 50
def hexrgb(c):
    c = c.lstrip("#")
    if len(c) == 3: c = "".join(ch * 2 for ch in c)
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))

def solid(h, fill):
    if fill == "#000": h.set_solid_fill(color=7)
    else: h.set_solid_fill(color=256, rgb=hexrgb(fill))
def ngon(c, r, n=20): return [(c[0] + r * math.cos(2 * math.pi * k / n), c[1] + r * math.sin(2 * math.pi * k / n)) for k in range(n)]
def tcol(c):
    """color propio solo para lo rojo (ejes, ubicación de nudos); el resto toma el color de la capa"""
    return {"true_color": ezdxf.rgb2int(hexrgb(c))} if c in ("#c00",) else {}

def clip_poly(pts, r):
    x0, y0, x1, y1 = r
    def clip(P, inside, inter):
        out = []
        for i in range(len(P)):
            a, b = P[i - 1], P[i]
            if inside(b):
                if not inside(a): out.append(inter(a, b))
                out.append(b)
            elif inside(a): out.append(inter(a, b))
        return out
    def ix(xc):
        return lambda a, b: (xc, a[1] + (b[1] - a[1]) * (xc - a[0]) / (b[0] - a[0]))
    def iy(yc):
        return lambda a, b: (a[0] + (b[0] - a[0]) * (yc - a[1]) / (b[1] - a[1]), yc)
    P = list(pts)
    for ins, it in ((lambda p: p[0] >= x0, ix(x0)), (lambda p: p[0] <= x1, ix(x1)), (lambda p: p[1] >= y0, iy(y0)), (lambda p: p[1] <= y1, iy(y1))):
        if not P: break
        P = clip(P, ins, it)
    return P
def clip_seg(a, b, r):
    x0, y0, x1, y1 = r; t0, t1 = 0.0, 1.0; dx, dy = b[0] - a[0], b[1] - a[1]
    for p, q in ((-dx, a[0] - x0), (dx, x1 - a[0]), (-dy, a[1] - y0), (dy, y1 - a[1])):
        if p == 0:
            if q < 0: return None
        else:
            t = q / p
            if p < 0: t0 = max(t0, t)
            else: t1 = min(t1, t)
    if t0 > t1: return None
    return (a[0] + t0 * dx, a[1] + t0 * dy), (a[0] + t1 * dx, a[1] + t1 * dy)
def clip_pline(pts, r):
    out, cur = [], []
    for a, b in zip(pts, pts[1:]):
        s = clip_seg(a, b, r)
        if s is None:
            if len(cur) > 1: out.append(cur)
            cur = []; continue
        if cur and math.dist(cur[-1], s[0]) < 1e-6: cur.append(s[1])
        else:
            if len(cur) > 1: out.append(cur)
            cur = [s[0], s[1]]
    if len(cur) > 1: out.append(cur)
    return out

def put_geometry(msp, DX, tf, rect=None, k=1.0):
    """DX del corte (mm reales) -> entidades; tf(x, y) -> coordenada de modelo; rect = recorte (mm reales)"""
    for e in DX:
        hidden = "dasharray" in (e.get("extra") or "")
        red = e.get("stroke") == "#7a1f1f"
        if e["t"] == "poly":
            pts = [tuple(p) for p in e["pts"]]
            if rect: pts = clip_poly(pts, rect)
            if len(pts) < 3: continue
            P = [tf(*p) for p in pts]
            fill = e["fill"]
            if fill in FILL:
                layer, pat, sc, ang = FILL[fill]
                h = msp.add_hatch(color=256, dxfattribs={"layer": layer})
                if pat == "SOLID": h.set_solid_fill(color=256, rgb=(205, 187, 156))
                else: h.set_pattern_fill(pat, color=256, scale=sc, angle=ang)
                h.paths.add_polyline_path(P, is_closed=True)
            elif fill in SOLID:
                layer, rgb = SOLID[fill]
                h = msp.add_hatch(color=256, dxfattribs={"layer": layer}); h.set_solid_fill(color=256, rgb=rgb)
                h.paths.add_polyline_path(P, is_closed=True)
            elif fill not in ("none", "#fff") and fill.startswith("#"):
                h = msp.add_hatch(color=256, dxfattribs={"layer": "A-VISTA"}); h.set_solid_fill(color=256, rgb=hexrgb(fill))
                h.paths.add_polyline_path(P, is_closed=True)
            if e["stroke"] != "none" and e["sw"] > 0:
                ol = "A-PROYECCION-OCULTO" if hidden else ("A-ARMADURAS" if red else ("A-VISTA" if e["stroke"] in ("#444", "#666", "#222") else "A-CONTORNOS"))
                msp.add_lwpolyline(P, close=True, dxfattribs={"layer": ol, "lineweight": lw(e["sw"])})
        elif e["t"] == "pline":
            ol = "A-ARMADURAS" if red else ("A-PROYECCION-OCULTO" if hidden else "A-CONTORNOS")
            parts = clip_pline([tuple(p) for p in e["pts"]], rect) if rect else [[tuple(p) for p in e["pts"]]]
            for q in parts: msp.add_lwpolyline([tf(*p) for p in q], dxfattribs={"layer": ol, "lineweight": lw(e["sw"])})
        elif e["t"] == "circ":
            cx, cy = e["c"]
            if rect and not (rect[0] <= cx <= rect[2] and rect[1] <= cy <= rect[3]): continue
            c = tf(cx, cy); r = e["r"] * k
            msp.add_circle(c, r, dxfattribs={"layer": "A-ARMADURAS"})
            if e["fill"] not in ("#fff", "none"):
                h = msp.add_hatch(color=256, dxfattribs={"layer": "A-ARMADURAS"}); h.set_solid_fill(color=256)
                h.paths.add_polyline_path(ngon(c, r), is_closed=True)

K = 20.0      # 1 mm de papel = 20 mm de modelo (la lámina se plotea a 1:20)
def dxf_sheet(sh, path):
    doc = ezdxf.new("R2018", setup=True); doc.units = ezdxf.units.MM
    doc.header["$LTSCALE"] = 20; doc.header["$PSLTSCALE"] = 1
    msp = doc.modelspace()
    doc.styles.add("ARIAL", font="arial.ttf"); doc.styles.add("ARIAL-B", font="arialbd.ttf")
    for n, cc in LAYERS.items():
        doc.layers.add(n, color=cc, linetype="DASHED" if n == "A-PROYECCION-OCULTO" else ("DASHDOT" if n == "X-EJES" else "CONTINUOUS"))
    M = lambda x, y: (x * K, (H - y) * K)
    for g in sh.geo:
        ns = g["ns"]; wx0, wy0, wx1, wy1 = g["win"]; ax, ay = g["at"]; den = g["den"]
        s = K / den
        tf = (lambda x, y, ax=ax, ay=ay, s=s, wx0=wx0, wy1=wy1: (ax * K + (x - wx0) * s, (H - ay) * K - (wy1 - y) * s))
        put_geometry(msp, ns["DX"], tf, (wx0, wy0, wx1, wy1), s)
    AL = {"start": TextEntityAlignment.LEFT, "middle": TextEntityAlignment.CENTER, "end": TextEntityAlignment.RIGHT}
    for a in sh.A:
        L = a["layer"]
        if a["t"] == "line":
            at = {"layer": L, "lineweight": lw(a["sw"])}
            at.update(tcol(a["stroke"]))
            msp.add_lwpolyline([M(*p) for p in a["pts"]], dxfattribs=at)
        elif a["t"] == "rect":
            P = [M(a["x"], a["y"]), M(a["x"] + a["w"], a["y"]), M(a["x"] + a["w"], a["y"] + a["h"]), M(a["x"], a["y"] + a["h"])]
            fl = a["fill"]
            if fl in FILL:
                layer, pat, sc, ang = FILL[fl]
                h = msp.add_hatch(color=256, dxfattribs={"layer": L}); h.set_pattern_fill(pat, color=256, scale=sc, angle=ang)
                h.paths.add_polyline_path(P, is_closed=True)
            elif fl not in ("none", "#fff"):
                h = msp.add_hatch(color=256, dxfattribs={"layer": L}); solid(h, fl)
                h.paths.add_polyline_path(P, is_closed=True)
            if a["stroke"] != "none":
                at = {"layer": L, "lineweight": lw(a["sw"])}
                at.update(tcol(a["stroke"]))
                msp.add_lwpolyline(P, close=True, dxfattribs=at)
        elif a["t"] == "poly":
            h = msp.add_hatch(color=256, dxfattribs={"layer": L}); solid(h, a["fill"])
            h.paths.add_polyline_path([M(*p) for p in a["pts"]], is_closed=True)
        elif a["t"] == "circle":
            c = M(a["x"], a["y"]); r = a["r"] * K
            if a["fill"] not in ("none", "#fff"):
                h = msp.add_hatch(color=256, dxfattribs={"layer": L}); solid(h, a["fill"])
                h.paths.add_polyline_path(ngon(c, r), is_closed=True)
            if a["stroke"] != "none":
                at = {"layer": L, "lineweight": lw(a["sw"])}
                at.update(tcol(a["stroke"]))
                msp.add_circle(c, r, dxfattribs=at)
        elif a["t"] == "text":
            at = {"layer": L, "style": "ARIAL-B" if a["bold"] else "ARIAL"}
            at.update(tcol(a["fill"]))
            t = msp.add_text(a["s"], height=a["size"] * 0.716 * K, rotation=-a["rot"], dxfattribs=at)
            if a["ital"]: t.dxf.oblique = 12
            t.set_placement(M(a["x"], a["y"]), align=AL[a["anchor"]])
    # presentación A4 con ventana a escala 1:20 sobre el modelo
    lay = doc.layouts.new(f"A4 {sh.code}")
    lay.page_setup(size=(210, 297), margins=(0, 0, 0, 0), units="mm", scale=(1, 1), name="ISO_full_bleed_A4_(210.00_x_297.00_MM)")
    vp = lay.add_viewport(center=(105, 148.5), size=(210, 297), view_center_point=(105 * K, 148.5 * K), view_height=297 * K)
    vp.dxf.layer = "X-MARCO"
    if "Layout1" in doc.layouts: doc.layouts.delete("Layout1")
    doc.set_modelspace_vport(height=297 * K, center=(105 * K, 148.5 * K))
    doc.saveas(path)

names = []
for sh in sheets:
    import unicodedata
    t_ = unicodedata.normalize("NFKD", sh.title.split(" - ")[0]).encode("ascii", "ignore").decode()
    slug = "_".join("".join(ch if ch.isalnum() else " " for ch in t_).split())
    nm = f"Lamina_{sh.code}_{slug}"[:70].rstrip("_")
    names.append(nm)
    dxf_sheet(sh, f"{OUT}/dxf/{nm}.dxf")
json.dump(dict(sheets=[dict(code=s.code, title=s.title, file=n) for s, n in zip(sheets, names)]), open(f"{OUT}/index.json", "w"), ensure_ascii=False, indent=1)
print("láminas:", NTOT); [print(" ", n) for n in names]
