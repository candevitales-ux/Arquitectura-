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
SISTEMA = os.environ.get("SISTEMA", "hormigon")          # "hormigon" | "acero"
if SISTEMA == "acero":
    import acero_refs as NR
else:
    import nudos_refs as NR

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = "build/nudos" if SISTEMA == "hormigon" else "build/nudos_acero"
os.makedirs(OUT + "/dxf", exist_ok=True)
for _d in ("dxf", "dwg", "png"):
    os.makedirs(f"{OUT}/{_d}", exist_ok=True)
    for _f in os.listdir(f"{OUT}/{_d}"): os.remove(f"{OUT}/{_d}/{_f}")

def load(fn, **kw):
    g = {"__file__": os.path.join(HERE, fn), "__name__": "nudos_src", **kw}
    exec(compile(open(g["__file__"], encoding="utf-8").read(), fn, "exec"), g)
    return g
if SISTEMA == "acero":
    V = load("acero_corte.py", VARIANTE="vidriado")
    O = load("acero_corte.py", VARIANTE="opaco")
else:
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
TMIN = 2.8      # font-size mínimo: altura de mayúscula impresa = 0,716 x 2,8 = 2,0 mm
FECHA = "22/10/2026"
SIS = [("SISTEMA CONSTRUCTIVO", True),
       ("Estructura de hormigón premoldeado de grandes luces (sistema Pi): columnas 40x40 c/ ménsulas, vigas VL doble T "
        "pretensadas en fachada, vigas VP T invertida interiores y losas TT h 0,65 con capa de compresión in situ. "
        "Bases aisladas de H°A in situ con cuello (anclaje mecánico húmedo).", False), ("", False),
       ("CERRAMIENTOS", True),
       ("Opaco: panel sándwich premoldeado de H°A (6 + EPS 6 + 8 cm) fijado a la VL con bulón pasante y apoyado en viga portapanel.", False),
       ("Vidriado: muro cortina stick de aluminio con DVH y spandrel, colgado de la estructura c/ grapas.", False)]
SISTEMA_TXT = "Hormigón premoldeado de grandes luces (sistema Pi) · mismo edificio del TP"
SUBT = "PRÁCTICA EN CLASE · HORMIGÓN PREMOLDEADO DE GRANDES LUCES"
HDR = "Corte vertical por la zona de apoyo de la viga VL · ESCALA 1:20"
KEYWIN = (-800, -2250, 2000, 9600)
CONV = [("url(#pHA)", "H° premoldeado (cortado)"), ("url(#pHAis)", "H°A in situ"), ("url(#pH)", "H° pobre / contrapiso"),
        ("url(#pEPS)", "EPS / H° liviano c/ EPS"), ("url(#pLana)", "Lana mineral"), ("url(#pTierra)", "Terreno natural"),
        ("#bfe3f0", "Vidrio"), ("#9aa3ab", "Aluminio")]
if SISTEMA == "acero":
    SIS = [("SISTEMA CONSTRUCTIVO", True),
           ("Estructura de perfiles laminados de acero F-24: columnas HEB 240, vigas principales IPE 400 c/ 2,50 m unidas a la "
            "columna c/ placa extrema y bulones M20 8.8, vigas de borde IPE 300 c/ doble ángulo. Losa colaborante (steel deck "
            "h 75 + H-25, e 13 cm) c/ conectores de corte. Bases: placa base c/ pernos de anclaje Ø24 y grout sobre cuello y "
            "zapata de H°A in situ. Antióxido + pintura intumescente F60.", False), ("", False),
           ("CERRAMIENTOS", True),
           ("Opaco: panel sándwich metálico PIR 100 mm atornillado a correas C 160 galv. (c/ tensores) fijadas a las columnas.", False),
           ("Vidriado: muro cortina stick de aluminio c/ DVH y spandrel, colgado de la losa c/ grapas s/ placa embebida.", False)]
    SISTEMA_TXT = "Estructura de acero (perfiles laminados) + losa colaborante · corte integral láms. 02–03"
    SUBT = "PRÁCTICA EN CLASE · ESTRUCTURA DE ACERO"
    HDR = "Corte vertical entre columnas (columna y viga IPE 400 en vista) · ESCALA 1:20"
    KEYWIN = (-800, -1950, 2000, 9000)
    CONV = [("#4d545c", "Acero cortado"), ("#dfe3e7", "Acero en vista"), ("url(#pHAis)", "H°A in situ / losa"),
            ("url(#pH)", "H° pobre / contrapiso"), ("url(#pPIR)", "Espuma PIR (panel)"), ("url(#pEPS)", "H° liviano c/ EPS"),
            ("url(#pLana)", "Lana mineral"), ("url(#pTierra)", "Terreno natural"), ("#bfe3f0", "Vidrio"), ("#9aa3ab", "Aluminio")]
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
        size = max(size, TMIN)
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
    for k, s in enumerate(wrap(sh.title, TMIN, 48)[:3]):
        sh.text(12, y0 + 9.0 + k * 3.4, s, TMIN, layer="X-ROTULO")
    sh.text(64, y0 + 5.0, "DOCENTE: Arq. Tucci y Arq. Cardozo", 2.4, layer="X-ROTULO")
    sh.text(64, y0 + 9.3, "ALUMNA: Candelaria Vitale", 2.4, layer="X-ROTULO")
    sh.text(64, y0 + 13.6, "GRUPO: 13", 2.4, layer="X-ROTULO")
    sh.text(122, y0 + 5.0, "CONSTRUCCIONES II · UNM", 2.4, bold=True, layer="X-ROTULO")
    sh.text(122, y0 + 9.3, "CÁTEDRA: ARQ. TUCCI", 2.4, layer="X-ROTULO")
    sh.text(122, y0 + 13.6, f"FECHA: {FECHA}", 2.4, layer="X-ROTULO")
    sh.text(170, y0 + 5.0, "LÁMINA", 2.2, layer="X-ROTULO")
    sh.text(198, y0 + 9.6, f"{sh.code}/{n_tot:02d}", 4.2, "end", bold=True, layer="X-ROTULO")
    sh.text(170, y0 + 16.0, sh.scale_txt, TMIN, bold=True, layer="X-ROTULO")

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

if SISTEMA == "acero":
    _nc = [(-32, 182, "21")]
    NUDOS = []
    for n, ns, t, win, sub, niv, cv, ch, notes in (
        (1, O, "CUBIERTA CON CERRAMIENTO EXTERIOR OPACO", (-350, 7000, 1900, 9000),
         "Panel sándwich metálico PIR 100 s/ correas C 160 · parapeto c/ montantes UPN 160 · losa colaborante s/ IPE 400 / IPE 300",
         [(8890, "+8,89", -300, "r", ""), (8118, "+8,12", 1830, "l", "Cubierta terminada"), (7200, "+7,20", 1830, "l", "Cielorraso")],
         [(7470, 7870, 900, "0,40"), (7870, 8000, 1580, "0,13"), (8000, 8890, -80, "0,89")],
         [(0, 100, 7080, "10"), (100, 260, 7080, "16"), (330, 570, 7080, "24")], [(1000, 7400, "Columna, IPE 400 y placa"), (1000, 7300, "extrema en vista")]),
        (2, V, "CUBIERTA CON CERRAMIENTO EXTERIOR VIDRIADO", (-350, 7000, 1900, 9000),
         "Muro cortina stick (aluminio + DVH) colgado c/ grapas s/ placa embebida · parapeto c/ montantes tubo · losa colaborante",
         [(8890, "+8,89", -300, "r", ""), (8118, "+8,12", 1830, "l", "Cubierta terminada"), (7200, "+7,20", 1830, "l", "Cielorraso")],
         [(7470, 7870, 900, "0,40"), (7870, 8000, 1580, "0,13"), (8000, 8880, -80, "0,88")],
         [(-32, 182, 7080, "21"), (330, 570, 7080, "24")], [(1000, 7400, "Columna, IPE 400 y placa"), (1000, 7300, "extrema en vista")]),
        (3, O, "ENTREPISO CON CERRAMIENTO EXTERIOR OPACO", (-350, 3000, 1900, 4800),
         "Correas C 160 fijadas a las columnas c/ clips · barrera cortafuego en el borde de losa · losa colaborante + IPE 300 / IPE 400",
         [(4000, "+4,00", 1250, "r", "N.P.T. P. Alta"), (3200, "+3,20", 1830, "l", "Cielorraso P. Baja")],
         [(3440, 3840, 900, "0,40"), (3840, 3970, 1580, "0,13")],
         [(0, 100, 3100, "10"), (100, 260, 3100, "16"), (330, 570, 3100, "24")], [(1000, 3400, "Columna, IPE 400 y placa"), (1000, 3300, "extrema en vista")]),
        (4, V, "ENTREPISO CON CERRAMIENTO EXTERIOR VIDRIADO", (-350, 3000, 1900, 4800),
         "Muro cortina: grapa s/ placa embebida en la losa, junta de dilatación del montante y barrera cortafuego en el borde de losa",
         [(4000, "+4,00", 1250, "r", "N.P.T. P. Alta"), (3200, "+3,20", 1830, "l", "Cielorraso P. Baja")],
         [(3440, 3840, 900, "0,40"), (3840, 3970, 1580, "0,13")],
         [(-32, 182, 3100, "21"), (330, 570, 3100, "24")], [(1000, 3400, "Columna, IPE 400 y placa"), (1000, 3300, "extrema en vista")]),
        (5, O, "PISO SOBRE TERRENO NATURAL CON CERRAMIENTO EXTERIOR OPACO Y FUNDACIÓN", (-650, -2000, 1500, 900),
         "Panel s/ perfil de arranque en viga de fundación · placa base c/ pernos de anclaje y grout s/ cuello y zapata de H°A",
         [(0, "±0,00", 1250, "r", "N.P.T. P. Baja"), (-150, "-0,15", -550, "r", "Vereda"), (-350, "-0,35", 1450, "l", "Sup. cuello"), (-1850, "-1,85", -300, "r", "Fundación")],
         [(-1800, -1350, 1430, "0,45"), (-1350, -350, 800, "1,00"), (-1850, 0, -600, "1,85")],
         [(-480, 1380, -1880, "1,80", True), (150, 750, -1290, "0,60", False), (0, 100, 300, "10", False)],
         [(840, -1150, "Fundación cortada"), (840, -1250, "por el eje de columna")]),
        (6, V, "PISO SOBRE TERRENO NATURAL CON CERRAMIENTO EXTERIOR VIDRIADO Y FUNDACIÓN", (-650, -2000, 1500, 900),
         "Muro cortina colgado del entrepiso c/ perfil guía deslizante · placa base c/ pernos de anclaje s/ cuello y zapata de H°A",
         [(0, "±0,00", 1250, "r", "N.P.T. P. Baja"), (-150, "-0,15", -550, "r", "Vereda"), (-350, "-0,35", 1450, "l", "Sup. cuello"), (-1850, "-1,85", -300, "r", "Fundación")],
         [(-1800, -1350, 1430, "0,45"), (-1350, -350, 800, "1,00"), (-1850, 0, -600, "1,85")],
         [(-480, 1380, -1880, "1,80", True), (150, 750, -1290, "0,60", False), (-32, 182, 300, "21", False)],
         [(840, -1150, "Fundación cortada"), (840, -1250, "por el eje de columna")])):
        NUDOS.append(dict(n=n, ns=ns, refs=getattr(NR, f"N{n}"), t=t, win=win, sub=sub, niv=niv, cv=cv, ch=ch, notes=notes))
for nd in NUDOS:
    nd["c"] = ["Cubierta · opaco", "Cubierta · vidriado", "Entrepiso · opaco", "Entrepiso · vidriado",
               "Piso + fundación · opaco", "Piso + fundación · vidriado"][nd["n"] - 1]

DEN = 20.0
AREA = (12.0, 39.0, 198.0, 250.0)     # zona de dibujo (x0, y0, x1, y1) en papel

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
    sh = Sheet(code, f"Nudo {nd['n']}: {nd['t'].capitalize()} - corte 1:20"); sh.scale_txt = "ESC. 1:20"; sh.short = f"Nudo {nd['n']} · {nd['c']}"
    wx0, wy0, wx1, wy1 = nd["win"]
    dw, dh = (wx1 - wx0) / DEN, (wy1 - wy0) / DEN
    ax = AREA[0] + (AREA[2] - AREA[0] - dw) / 2
    ay = AREA[1] + 15
    sh.geo.append(dict(ns=nd["ns"], win=nd["win"], at=(ax, ay), den=DEN))
    P = lambda x, y: (ax + (x - wx0) / DEN, ay + (wy1 - y) / DEN)
    # encabezado
    sh.text(14, 19, f"NUDO {nd['n']}", 6.0, bold=True)
    sh.text(42, 19, nd["t"], 3.6 if len(nd["t"]) < 46 else 3.0, bold=True)
    sh.text(42, 24.5, HDR, 2.6)
    for k, s_ in enumerate(wrap(nd["sub"], TMIN, 156)[:2]): sh.text(42, 29.3 + k * 3.6, s_, TMIN, ital=True, fill="#333")
    sh.line([(10, 35.5), (200, 35.5)], 0.25)
    sh.rect(ax, ay, dw, dh, fill="none", stroke="#999", sw=0.08, layer="X-TEXTOS")
    # eje de columna
    x0p, y0p = P(450, wy1); _, y1p = P(450, wy0)
    sh.line([(x0p, y0p - 4), (x0p, y1p)], 0.13, "#c00", dash="4 0.8 0.6 0.8", layer="X-EJES")
    sh.circle(x0p, y0p - 6.4, 2.4, fill="#fff", stroke="#c00", sw=0.18, layer="X-EJES")
    sh.text(x0p, y0p - 5.4, "C", TMIN, "middle", bold=True, fill="#c00", layer="X-EJES")
    # exterior / interior
    exx = P(wx0 + 40, 0)[0]; inx = P(wx1 - 40, 0)[0]
    sh.text(exx, ay - 1.6, "EXTERIOR", 3.0, fill="#555")
    sh.text(inx, ay - 1.6, "INTERIOR", 3.0, "end", fill="#555")
    # niveles
    for y, txt, xr, side, sub in nd["niv"]:
        px, py = P(xr, y)
        sh.poly([(px, py), (px - 1.2, py - 2), (px + 1.2, py - 2)])
        sh.line([(px - 3.6, py), (px + 3.6, py)], 0.15, layer="X-NIVELES")
        tx = px + 1.7 if side == "r" else px - 1.7; an = "start" if side == "r" else "end"
        sh.text(tx, py - 2.4, txt, 3.0, an, bold=True, layer="X-NIVELES")
        if sub: sh.text(tx, py + 3.4, sub, TMIN, an, ital=True, layer="X-NIVELES")
    # cotas
    def tick(x, y): sh.line([(x - 0.7, y + 0.7), (x + 0.7, y - 0.7)], 0.25, layer="X-COTAS")
    for y0, y1, xr, txt in nd["cv"]:
        (px, p0), (_, p1) = P(xr, y0), P(xr, y1)
        sh.line([(px, p0), (px, p1)], 0.12, layer="X-COTAS")
        for p in (p0, p1): tick(px, p); sh.line([(px - 1.1, p), (px + 1.4, p)], 0.1, layer="X-COTAS")
        sh.text(px - 0.9, (p0 + p1) / 2, txt, TMIN, "middle", rot=-90, layer="X-COTAS")
    for c in nd["ch"]:
        x0, x1, yr, txt = c[:4]; below = c[4] if len(c) > 4 else False
        (a, py), (b, _) = P(x0, yr), P(x1, yr)
        sh.line([(a, py), (b, py)], 0.12, layer="X-COTAS")
        for p in (a, b): tick(p, py); sh.line([(p, py - 1.1), (p, py + 1.1)], 0.1, layer="X-COTAS")
        if tw(txt, TMIN) < abs(b - a) - 0.6:
            sh.text((a + b) / 2, py + (3.2 if below else -0.9), txt, TMIN, "middle", layer="X-COTAS")
        else:   # tramo corto: texto arriba, con línea de llamada
            sh.line([((a + b) / 2, py), ((a + b) / 2, py - 3.4)], 0.1, layer="X-COTAS")
            sh.text((a + b) / 2, py - 4.0, txt, TMIN, "middle", layer="X-COTAS")
    for xr, yr, s in nd.get("notes", []):
        px, py = P(xr, yr); sh.text(px, py, s, TMIN, ital=True, fill="#333")
    # referencias (globos): izquierda = cerramiento (x < 250), derecha = estructura e interior
    pts = []; TOPK = set(NR.TOP[nd["n"]])
    for k, x, y in nd["refs"]:
        px, py = P(x, y); pts.append(dict(k=k, ax=px, ay=py, side="T" if k in TOPK else ("L" if x < 250 else "R")))
    gap = 5.4; ymin, ymax = ay - 6, ay + dh + 6
    num = 0; order = []
    for side in ("L", "T", "R"):
        if side == "T":
            L = sorted([p for p in pts if p["side"] == "T"], key=lambda p: p["ax"])
            tmp = [{"ay": p["ax"]} for p in L]; place(tmp, 5.8, ax + dw * 0.42, inx - 18)
            byt = ay - 9.5
            for p, t in zip(L, tmp):
                num += 1; p["n"] = num; order.append(p)
                sh.line([(p["ax"], p["ay"]), (t["by"], byt + 2.35)], 0.11, layer="X-REFERENCIAS")
                sh.circle(p["ax"], p["ay"], 0.35, fill="#000", stroke="none", sw=0)
                sh.circle(t["by"], byt, 2.35)
                sh.text(t["by"], byt + 1.0, str(num), TMIN, "middle", bold=True, layer="X-REFERENCIAS")
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
            sh.text(bx, p["by"] + 1.0, str(num), TMIN, "middle", bold=True, layer="X-REFERENCIAS")
    # leyenda: denominaciones (la especificación y la función van en la planilla)
    ly = ay + dh + 11
    sh.text(14, ly, "REFERENCIAS", 2.8, bold=True)
    sh.text(42, ly, "denominación · especificación técnica y función en la planilla siguiente", TMIN, ital=True, fill="#333")
    size = TMIN
    for ncol, lh in ((2, 3.6), (3, 3.6), (3, 3.3)):
        cw = 186 / ncol
        lines = [wrap(NR.R[p["k"]][0], size, cw - 7.5) for p in order]
        per = math.ceil(sum(len(l) for l in lines) / ncol)
        cols, cur, cnt = [], [], 0
        for p, l in zip(order, lines):
            if cnt + len(l) > per and cur and len(cols) < ncol - 1: cols.append(cur); cur, cnt = [], 0
            cur.append((p, l)); cnt += len(l)
        cols.append(cur)
        need = max(sum(len(l) for _, l in c) for c in cols) * lh
        if ly + 4.5 + need <= 253: break
    for ci, c in enumerate(cols):
        x = 14 + ci * cw; y = ly + 4.6
        for p, l in c:
            sh.text(x + 4.2, y, str(p["n"]), size, "end", bold=True)
            for li, s_ in enumerate(l): sh.text(x + 5.4, y + li * lh, s_, size)
            y += len(l) * lh
    # escala gráfica
    gx, gy = 14, 258.0
    sh.text(gx, gy - 1.6, "ESCALA GRÁFICA 1:20", TMIN, bold=True)
    for i in range(10):
        sh.rect(gx + i * 5, gy, 5, 1.6, fill="#000" if i % 2 == 0 else "#fff", stroke="#000", sw=0.12, layer="X-TEXTOS")
    for i, lab in ((0, "0"), (5, "0,50"), (10, "1,00 m")):
        sh.text(gx + i * 5, gy + 5.0, lab, TMIN, "middle" if i < 10 else "start")
    sh.text(198, 258.5, "Cotas en m (secciones en cm) · niveles en m s/ N.P.T. P. Baja ±0,00", TMIN, "end", ital=True)
    sh.text(198, 263.5, SISTEMA_TXT, TMIN, "end", ital=True)
    return sh, [(p["n"], p["k"]) for p in order]

COLS = [("N°", 8), ("DENOMINACIÓN", 40), ("ESPECIFICACIÓN TÉCNICA DE MATERIALES", 80), ("FUNCIÓN", 58)]
def table_sheets(nd, items, code0):
    out = []; size, lh = TMIN, 3.45
    rows = []
    for n, k in items:
        d, e, fn = NR.R[k]
        cells = [[str(n)], wrap(d, size, COLS[1][1] - 2.4, True), wrap(e, size, COLS[2][1] - 2.4), wrap(fn, size, COLS[3][1] - 2.4)]
        rows.append((cells, max(len(c) for c in cells) * lh + 1.6))
    ytop, ybot = 45.0, 265.0
    i = 0; part = 0
    while i < len(rows):
        part += 1
        sh = Sheet(f"{code0 + part - 1:02d}", f"Nudo {nd['n']}: planilla de referencias" + (" (cont.)" if part > 1 else "")); sh.scale_txt = "SIN ESCALA"; sh.short = f"Nudo {nd['n']} · planilla" + (" (cont.)" if part > 1 else "")
        sh.text(14, 19, f"NUDO {nd['n']}", 6.0, bold=True)
        sh.text(42, 19, nd["t"], 3.6 if len(nd["t"]) < 46 else 3.0, bold=True)
        sh.text(42, 24.5, "REFERENCIAS: denominación, especificación técnica de materiales y función" + (" (cont.)" if part > 1 else ""), 2.6)
        sh.text(42, 29.3, f"Corresponde al dibujo en escala 1:20 de la lámina {int(code0) - 1:02d}", TMIN, ital=True, fill="#333")
        sh.line([(10, 35.5), (200, 35.5)], 0.25)
        x = 12.0; hh = 6.0
        sh.rect(12, ytop - hh, 186, hh, fill="#d9d9d9", stroke="#000", sw=0.25, layer="X-TABLA")
        for name, w in COLS:
            sh.text(x + (w / 2 if name == "N°" else 1.2), ytop - 2.0, name, TMIN, "middle" if name == "N°" else "start", bold=True, layer="X-TABLA")
            x += w
        y = ytop
        while i < len(rows) and y + rows[i][1] <= ybot:
            cells, rh = rows[i]
            if i % 2 == 1: sh.rect(12, y, 186, rh, fill="#f2f2f2", stroke="none", sw=0, layer="X-TABLA")
            x = 12.0
            for ci, (c, (name, w)) in enumerate(zip(cells, COLS)):
                for li, s in enumerate(c):
                    if ci == 0:
                        sh.circle(x + w / 2, y + 2.55, 2.15, layer="X-TABLA")
                        sh.text(x + w / 2, y + 3.55, s, TMIN, "middle", bold=True, layer="X-TABLA")
                    else:
                        sh.text(x + 1.2, y + 3.3 + li * lh, s, size, bold=(ci == 1), layer="X-TABLA")
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
    sh = Sheet("01", "Carátula, consigna e índice; ubicación de los nudos en los cortes integrales"); sh.scale_txt = "ESC. 1:100"; sh.short = "Carátula · consigna · índice"
    sh.text(14, 24, "CONSTRUCCIONES II · UNM", 4.0, bold=True)
    sh.text(14, 36, "NUDOS", 11.0, bold=True)
    sh.text(14, 44, SUBT, 3.2)
    sh.line([(14, 48), (196, 48)], 0.3)
    cons = ["Nudos pertenecientes al proyecto del trabajo práctico, dibujados en forma proporcionada a escala 1:20,",
            "con referencias que incluyen función, denominación y especificación técnica de los materiales."]
    for k, s in enumerate(cons): sh.text(14, 54 + k * 4.0, s, TMIN)
    sh.text(14, 66, "ÍNDICE DE LÁMINAS (A4)", 3.0, bold=True)
    # cortes integrales esquemáticos a 1:100 c/ ubicación de nudos
    den = 100.0; win = KEYWIN
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
    sh.text(198, 261.0, "Cortes integrales esquemáticos esc. 1:100", TMIN, "end", ital=True)
    sh.text(198, 265.0, "en rojo: encuadre de cada nudo", TMIN, "end", ital=True)
    # descripción del sistema
    sis = SIS
    yy = 146
    for s_, b in sis:
        for l_ in (wrap(s_, TMIN, 100) if s_ else [""]): sh.text(14, yy, l_, TMIN, bold=b); yy += 3.9
    sh.text(14, 222, "CONVENCIONES", TMIN, bold=True)
    conv = CONV
    for k, (fl, s) in enumerate(conv):
        x = 14 + (k % 2) * 52; y = 226 + (k // 2) * 6.6
        sh.rect(x, y, 9, 5, fill=fl, stroke="#000", sw=0.15, layer="X-TEXTOS")
        sh.text(x + 11, y + 3.7, s, 2.2)
    return sh

# ===================================================================== corte integral 1:50 (sistema sin corte previo)
def integral_sheet(ns, code, lab):
    den = 50.0; win = (-750, -1950, 2700, 9000)
    sh = Sheet(code, f"Corte integral {lab.lower()} - esc. 1:50"); sh.scale_txt = "ESC. 1:50"; sh.short = f"Corte integral · {lab.lower()}"
    dw, dh = (win[2] - win[0]) / den, (win[3] - win[1]) / den
    ax, ay = 26.0, 43.0
    sh.geo.append(dict(ns=ns, win=win, at=(ax, ay), den=den))
    P = lambda x, y: (ax + (x - win[0]) / den, ay + (win[3] - y) / den)
    sh.text(14, 19, "CORTE INTEGRAL", 6.0, bold=True)
    sh.text(14, 24.5, f"ESTRUCTURA DE ACERO · CERRAMIENTO {lab.upper()} · ESCALA 1:50", 3.2, bold=True)
    sh.text(14, 29.3, "Corte vertical entre columnas; fundación cortada por el eje de columna. Base de los 6 nudos 1:20.", TMIN, ital=True, fill="#333")
    sh.line([(10, 35.5), (200, 35.5)], 0.25)
    sh.text(ax, ay - 1.6, "EXTERIOR", 3.0, fill="#555"); sh.text(ax + dw, ay - 1.6, "INTERIOR", 3.0, "end", fill="#555")
    x0p = P(450, 0)[0]
    sh.line([(x0p, ay - 3), (x0p, ay + dh)], 0.13, "#c00", dash="4 0.8 0.6 0.8", layer="X-EJES")
    # niveles (a la derecha del dibujo)
    for y, txt, sub in ((8890, "+8,89", "Cupertina"), (8118, "+8,12", "Cub. terminada"), (7200, "+7,20", "Cielorraso"), (4000, "+4,00", "N.P.T. P. Alta"),
                        (3200, "+3,20", "Cielorraso"), (0, "±0,00", "N.P.T. P. Baja"), (-350, "-0,35", "Sup. cuello"), (-1850, "-1,85", "Fundación")):
        px, py = P(2700, y); px += 2
        sh.poly([(px, py), (px - 1.2, py - 2), (px + 1.2, py - 2)])
        sh.line([(px - 3.6, py), (px + 3.6, py)], 0.15, layer="X-NIVELES")
        sh.text(px + 2.0, py + 1.0, txt, TMIN, bold=True, layer="X-NIVELES")
        sh.text(px + 12.5, py + 1.0, sub, TMIN, ital=True, layer="X-NIVELES")
    # cotas generales (lado exterior)
    for y0, y1, txt in ((-1850, 0, "1,85"), (0, 4000, "4,00"), (4000, 8000, "4,00"), (8000, 8890, "0,89")):
        (px, p0), (_, p1) = P(-600, y0), P(-600, y1)
        sh.line([(px, p0), (px, p1)], 0.12, layer="X-COTAS")
        for p in (p0, p1): sh.line([(px - 0.7, p + 0.7), (px + 0.7, p - 0.7)], 0.25, layer="X-COTAS"); sh.line([(px - 1.1, p), (px + 1.4, p)], 0.1, layer="X-COTAS")
        sh.text(px - 0.9, (p0 + p1) / 2, txt, TMIN, "middle", rot=-90, layer="X-COTAS")
    # encuadre de los nudos
    for nd in NUDOS:
        if nd["ns"] is not ns: continue
        x0, y0, x1, y1 = nd["win"]
        (a, b), (c_, d) = P(max(x0, win[0]), min(y1, win[3])), P(min(x1, win[2]), max(y0, win[1]))
        sh.rect(a, b, c_ - a, d - b, fill="none", stroke="#c00", sw=0.3, layer="X-REFERENCIAS")
        sh.circle(a - 4.0, (b + d) / 2, 2.8, fill="#fff", stroke="#c00", sw=0.25)
        sh.text(a - 4.0, (b + d) / 2 + 1.0, str(nd["n"]), TMIN, "middle", bold=True, fill="#c00", layer="X-REFERENCIAS")
    # memoria
    xm, ym = 134.0, 46.0
    txt = [("ESTRUCTURA", True),
           ("Columnas HEB 240 (F-24) c/ placa base 450x450x25, cartelas y 4 pernos de anclaje Ø24 + grout 30 mm, s/ cuello 60x60 y zapata 1,80x1,80x0,45 de H°A.", False),
           ("Vigas principales IPE 400 c/ 2,50 m (placa extrema 20 mm + 6 M20 8.8 al ala de la columna).", False),
           ("Vigas de borde IPE 300 (doble ángulo L 90x90x9 + M16 al alma de la columna).", False),
           ("Losa colaborante: chapa trapezoidal galv. h 75 e 0,9 + H-25, e = 13 cm, malla Q188, conectores Nelson Ø19 c/30.", False),
           ("Arriostramiento vertical en cruz (fuera del corte). Antióxido + pintura intumescente F60.", False), ("", False),
           ("CERRAMIENTO", True)]
    if ns is O:
        txt += [("Panel sándwich metálico PIR 100 vertical, atornillado a correas C 160x60x20x2,5 galv. c/ 1,45–1,80 m, fijadas c/ clips a las columnas; tensores Ø10 a media luz.", False),
                ("Revestimiento interior placa de yeso 12,5. Parapeto c/ montantes UPN 160 c/ 1,25 m y placa cementicia.", False)]
    else:
        txt += [("Muro cortina stick de aluminio (montante 50x150) c/ DVH 6+12+3+3 y spandrel esmaltado c/ bandeja de lana.", False),
                ("Montantes colgados de cada losa c/ grapa regulable s/ placa embebida; junta de dilatación 20 mm c/ manguito; guía deslizante en PB.", False)]
    txt += [("", False), ("CUBIERTA", True), ("Barrera de vapor, contrapiso liviano c/ EPS pend. 2 % al parapeto, carpeta y membrana c/ aluminio; embudo y caño de lluvia interior.", False),
            ("", False), ("NUDOS (en rojo)", True)]
    for nd in NUDOS:
        if nd["ns"] is ns: txt.append((f"Nudo {nd['n']}: {nd['c']} · esc. 1:20", False))
    for s_, b in txt:
        for l_ in (wrap(s_, TMIN, 198 - xm) if s_ else [""]): sh.text(xm, ym, l_, TMIN, bold=b); ym += 3.8
    sh.text(198, 263.5, "Cotas y niveles en m s/ N.P.T. P. Baja ±0,00", TMIN, "end", ital=True)
    return sh

# ===================================================================== armado de láminas
sheets = [caratula()]
if SISTEMA == "acero":
    sheets += [integral_sheet(O, "02", "Opaco"), integral_sheet(V, "03", "Vidriado")]
c = len(sheets) + 1
for nd in NUDOS:
    sd, items = drawing_sheet(nd, f"{c:02d}")
    tabs = table_sheets(nd, items, c + 1)
    sheets += [sd] + tabs; c += 1 + len(tabs)
NTOT = len(sheets)
_nr = math.ceil(NTOT / 2)
for k, s_ in enumerate(sheets):
    col, row = divmod(k, _nr); x = 14 + col * 92; y = 71.5 + row * 3.9
    sheets[0].text(x, y, s_.code, TMIN, bold=True); sheets[0].text(x + 7, y, s_.short, TMIN)
    sheets[0].text(x + 88, y, {"SIN ESCALA": "—"}.get(s_.scale_txt, s_.scale_txt.replace("ESC. ", "")), TMIN, "end")
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
    "A-AISLACION-PIR": 50, "A-PLACA-CEMENTICIA": 252, "A-ACERO-CORTADO": 250, "A-ACERO-VISTA": 8, "A-CHAPA-GALVANIZADA": 253,
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
    "url(#pPIR)": ("A-AISLACION-PIR", "HONEY", 4, 0), "url(#pYeso)": ("A-YESO-CIELORRASO", "AR-SAND", 0.3, 0),
    "url(#pCem)": ("A-PLACA-CEMENTICIA", "AR-SAND", 0.4, 0),
}
SOLID = {
    "#9aa3ab": ("A-ALUMINIO", (154, 163, 171)), "#b9c0c6": ("A-ALUMINIO", (185, 192, 198)), "#bfe3f0": ("A-VIDRIO", (191, 227, 240)),
    "#6f8796": ("A-VIDRIO", (111, 135, 150)), "#3b3b3b": ("A-ACERO", (59, 59, 59)), "#333": ("A-ACERO", (51, 51, 51)),
    "#555": ("A-ACERO", (85, 85, 85)), "#111": ("A-NEOPRENO-SELLADORES", (17, 17, 17)), "#222": ("A-NEOPRENO-SELLADORES", (34, 34, 34)),
    "#000": ("A-BARRERAS-MEMBRANAS", (0, 0, 0)), "#8d8d8d": ("A-MORTERO-CARPETAS", (141, 141, 141)), "#888": ("A-ACERO", (136, 136, 136)),
    "#c0392b": ("A-SELLADOR-INTUMESCENTE", (192, 57, 43)),
    "#4d545c": ("A-ACERO-CORTADO", (77, 84, 92)), "#dfe3e7": ("A-ACERO-VISTA", (223, 227, 231)), "#8f989f": ("A-CHAPA-GALVANIZADA", (143, 152, 159)), "#cdbb9c": ("A-SOLADOS", (205, 187, 156)),
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
            elif fl not in ("none", "#fff") and fl.startswith("#"):
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
