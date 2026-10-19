# -*- coding: utf-8 -*-
"""Lámina 4 - Catálogo de cerramientos: OPACO (panel sándwich 80 mm, ref. 24 del corte integral de acero).
Todo se dibuja en un único DXF en milímetros de papel (hoja A3 vertical 297x420, escala 1:1 de la hoja);
cada detalle se dibuja en mm reales y se lleva a la hoja con su escala. Del DXF salen el DWG y el PDF."""
import math, sys, os
import ezdxf
from ezdxf.enums import TextEntityAlignment as TA

OUT = sys.argv[1] if len(sys.argv) > 1 else "build"
os.makedirs(OUT, exist_ok=True)
W, H = 297.0, 420.0

doc = ezdxf.new("R2018", setup=True); doc.units = ezdxf.units.MM
doc.styles.add("ARIAL", font="arial.ttf"); doc.styles.add("ARIAL-NEGRITA", font="arialbd.ttf")
msp = doc.modelspace()
LAY = {"0-MARCO": 7, "1-CONTORNO": 7, "1-CHAPA": 7, "1-NUCLEO-PUR": 8, "1-ACERO": 7, "1-HORMIGON": 8, "1-SUELO": 8,
       "1-SELLADOS": 250, "1-TORNILLERIA": 7, "1-RAYADOS": 8, "1-VISTA": 8, "1-OCULTAR": 7, "2-COTAS": 7,
       "3-REFERENCIAS": 7, "3-TEXTOS": 7, "3-TITULOS": 7, "3-TABLAS": 7}
for n, c in LAY.items(): doc.layers.add(n, color=c)
doc.layers.get("1-RAYADOS").dxf.color = 8

# ------------------------------------------------------------------ primitivas en mm de papel
def pl(pts, layer="1-CONTORNO", lw=25, close=False, lt=None):
    a = {"layer": layer, "lineweight": lw}
    if lt: a["linetype"] = lt
    return msp.add_lwpolyline(pts, close=close, dxfattribs=a)

def hatch(pts, pat="SOLID", sc=1.0, ang=0, layer="1-RAYADOS", rgb=None, color=8):
    h = msp.add_hatch(color=color, dxfattribs={"layer": layer})
    if pat == "SOLID":
        h.set_solid_fill(color=color, rgb=rgb)
    else:
        h.set_pattern_fill(pat, color=color, scale=sc, angle=ang)
    h.paths.add_polyline_path(pts, is_closed=True)
    return h

def txt(s, x, y, h=2.5, align=TA.LEFT, layer="3-TEXTOS", bold=False, rot=0):
    t = msp.add_text(s, height=h, rotation=rot,
                     dxfattribs={"layer": layer, "style": "ARIAL-NEGRITA" if bold else "ARIAL", "width": 0.9})
    t.set_placement((x, y), align=align)
    return t

def mtxt(s, x, y, h=2.2, width=100, layer="3-TEXTOS", spacing=1.35):
    m = msp.add_mtext(s, dxfattribs={"layer": layer, "style": "ARIAL", "char_height": h, "width": width,
                                     "line_spacing_factor": spacing})
    m.set_location((x, y), attachment_point=1)
    return m

def circle(c, r, layer="1-CONTORNO", lw=18):
    return msp.add_circle(c, r, dxfattribs={"layer": layer, "lineweight": lw})

def globo(n, at, cpos, r=2.4):
    """Referencia numerada: círculo en cpos, línea hasta el punto 'at' con punto final."""
    dx, dy = at[0] - cpos[0], at[1] - cpos[1]; d = math.hypot(dx, dy) or 1
    s = (cpos[0] + dx / d * r, cpos[1] + dy / d * r)
    pl([s, at], "3-REFERENCIAS", 13)
    msp.add_circle(at, 0.35, dxfattribs={"layer": "3-REFERENCIAS"})
    hh = msp.add_hatch(color=256, dxfattribs={"layer": "3-REFERENCIAS"}); hh.set_solid_fill(color=256)
    hh.paths.add_edge_path().add_arc(at, 0.35, 0, 360)
    circle(cpos, r, "3-REFERENCIAS", 18)
    txt(str(n), cpos[0], cpos[1], 2.4, TA.MIDDLE_CENTER, "3-REFERENCIAS")

class V:
    """Ventana de dibujo: coordenadas reales (mm) -> papel (mm) con escala 1:s y origen (ox, oy)."""
    def __init__(self, s, ox, oy): self.s, self.ox, self.oy = s, ox, oy
    def p(self, x, y): return (self.ox + x / self.s, self.oy + y / self.s)
    def P(self, pts): return [self.p(*q) for q in pts]
    def rect(self, x0, y0, x1, y1): return self.P([(x0, y0), (x1, y0), (x1, y1), (x0, y1)])
    def dim(self, a, b, off, vertical=False, text=None):
        """Cota lineal asociativa (DIMENSION) mostrando mm reales: dimlfac = escala."""
        pa, pb = self.p(*a), self.p(*b)
        if vertical:
            base = (pa[0] + off, pa[1]); ang = 90
        else:
            base = (pa[0], pa[1] + off); ang = 0
        d = msp.add_linear_dim(base=base, p1=pa, p2=pb, angle=ang, dimstyle="CATALOGO", text=text or "<>",
                               override={"dimlfac": self.s}, dxfattribs={"layer": "2-COTAS"})
        d.render()

ds = doc.dimstyles.new("CATALOGO")
ds.dxf.dimtxt = 2.0; ds.dxf.dimasz = 1.4; ds.dxf.dimblk = "ARCHTICK"; ds.dxf.dimexe = 1.0; ds.dxf.dimexo = 0.8
ds.dxf.dimgap = 0.6; ds.dxf.dimtad = 1; ds.dxf.dimdec = 0; ds.dxf.dimtxsty = "ARIAL"; ds.dxf.dimtih = 0; ds.dxf.dimtoh = 0
ds.dxf.dimclrd = 7; ds.dxf.dimclre = 7; ds.dxf.dimclrt = 7; ds.dxf.dimtmove = 0

def titulo_detalle(num, t1, esc, x, y, w=60):
    """Título tipo catálogo: número en círculo negro + nombre + escala, subrayado."""
    circle((x + 3, y + 1.2), 3, "3-TITULOS", 35)
    txt(num, x + 3, y + 1.2, 2.8, TA.MIDDLE_CENTER, "3-TITULOS", True)
    txt(t1, x + 8, y + 0.2, 2.8, TA.LEFT, "3-TITULOS", True)
    if esc: txt(esc, x + w, y + 0.2, 2.4, TA.RIGHT, "3-TITULOS")
    pl([(x, y - 2), (x + w, y - 2)], "3-TITULOS", 35)

def corte_rotura(v, a, b, layer="1-CONTORNO"):
    """Línea de corte con zigzag entre a y b (coords reales)."""
    (x0, y0), (x1, y1) = a, b
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2; dx, dy = x1 - x0, y1 - y0; L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L; nx, ny = -uy, ux; k = 6 * v.s / 5
    pts = [(x0 - ux * k, y0 - uy * k), (mx - ux * k, my - uy * k), (mx - ux * k * .4 + nx * k, my - uy * k * .4 + ny * k),
           (mx + ux * k * .4 - nx * k, my + uy * k * .4 - ny * k), (mx + ux * k, my + uy * k), (x1 + ux * k, y1 + uy * k)]
    pl(v.P(pts), layer, 13)

# ------------------------------------------------------------------ geometría del panel (mm reales)
T = 80.0         # espesor del panel
G = 2.0          # holgura de la junta
def perfil_macho(Y):
    """Borde superior (macho) de x=0 (cara exterior) a x=80 (cara interior)."""
    return [(0, Y - 4), (5, Y), (28, Y), (29, Y + 16), (47, Y + 16), (48, Y), (76, Y), (80, Y - 4)]
def perfil_hembra(Y):
    """Borde inferior (hembra) del panel superior, de x=0 a x=80."""
    return [(0, Y + G + 4), (5, Y + G), (26, Y + G), (26, Y + G + 21), (50, Y + G + 21), (50, Y + G), (76, Y + G), (80, Y + G + 4)]

def panel_poly(ybot, ytop, macho=True, hembra=True):
    """Contorno del panel en corte vertical: abajo hembra (en ybot), arriba macho (en ytop)."""
    bot = perfil_hembra(ybot - G) if hembra else [(0, ybot), (80, ybot)]
    top = perfil_macho(ytop) if macho else [(0, ytop), (80, ytop)]
    return bot + list(reversed(top))

def dibujar_panel(v, poly, cortes=(), chapa_lw=40, sc_nucleo=None):
    """Núcleo rayado (HONEY, como en el corte integral) + chapas exterior/interior marcadas con línea gruesa.
    'cortes': y reales donde el panel termina en línea de rotura (sin chapa)."""
    hatch(v.P(poly), "HONEY", sc_nucleo or 0.55 / v.s * 5, 0, "1-NUCLEO-PUR", color=8)
    pl(v.P(poly), "1-CONTORNO", 13, close=True)
    # chapas: todo el contorno salvo los bordes horizontales de rotura
    n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        if any(abs(a[1] - c) < .01 and abs(b[1] - c) < .01 for c in cortes): continue
        pl(v.P([a, b]), "1-CHAPA", chapa_lw)

def tornillo_h(v, x0, x1, y, cabeza_ext=True):
    """Tornillo autoperforante horizontal (de x0 a x1) con arandela EPDM en la cabeza (x0)."""
    pl(v.P([(x0, y), (x1, y)]), "1-TORNILLERIA", 35)
    for k in range(int(abs(x1 - x0 - 8) // 4)):
        xx = x0 + 8 + 4 * k + 2
        pl(v.P([(xx, y - 3), (xx + 2, y + 3)]), "1-TORNILLERIA", 9)
    pl(v.P([(x0 - 3, y - 8), (x0 - 3, y + 8), (x0 - 1, y + 7), (x0 - 1, y - 7)]), "1-TORNILLERIA", 25, True)  # cabeza
    pl(v.P([(x0 - 1, y - 9), (x0, y - 9), (x0, y + 9), (x0 - 1, y + 9)]), "1-SELLADOS", 25, True)           # arandela EPDM

# ==================================================================================== HOJA
pl([(10, 10), (W - 10, 10), (W - 10, H - 10), (10, H - 10)], "0-MARCO", 50, True)

# encabezado
txt("CATÁLOGO DE CERRAMIENTOS", 15, 398, 7.5, TA.LEFT, "3-TITULOS", True)
txt("OPACOS  |  PANEL SÁNDWICH METÁLICO 80 mm", 15, 389.5, 4.2, TA.LEFT, "3-TITULOS")
txt("LÁMINA 4", W - 15, 398, 7.5, TA.RIGHT, "3-TITULOS", True)
txt("CORTE INTEGRAL ACERO (OPACO) - REF. 24 PANEL OPACO", W - 15, 389.5, 2.6, TA.RIGHT, "3-TITULOS")
pl([(15, 386), (W - 15, 386)], "3-TITULOS", 70)

# ---------------------------------------------------------------- 01 AXONOMETRÍA DEL PANEL (S/E)
titulo_detalle("1", "EL PANEL - AXONOMETRÍA", "S/E", 15, 378, 128)
C30, S30 = math.cos(math.radians(30)), math.sin(math.radians(30))
HP, LP = 520.0, 1100.0                    # alto del trozo de panel y largo dibujado
AS = 1 / 15.0
# encuadre: el panel ocupa x 18..140, y 300..372 de la hoja
_raw = [((z - x) * C30, y + (x + z) * S30) for x in (0, T) for y in (0, HP + 16) for z in (0, LP)]
AX0 = 80 - (min(p[0] for p in _raw) + max(p[0] for p in _raw)) / 2 * AS
AY0 = 336 - (min(p[1] for p in _raw) + max(p[1] for p in _raw)) / 2 * AS
def iso(x, y, z): return (AX0 + (z - x) * C30 * AS, AY0 + (y + (x + z) * S30) * AS)

def prisma(poly, z0, z1, layer, lw=18, fill=(255, 255, 255), rayas=None):
    """Extrusión del perfil 'poly' (plano x-y) entre z0 y z1, con caras ocultas por pintor."""
    n = len(poly); caras = []
    sa = sum(poly[i][0] * poly[(i + 1) % n][1] - poly[(i + 1) % n][0] * poly[i][1] for i in range(n))
    for i in range(n):
        (xa, ya), (xb, yb) = poly[i], poly[(i + 1) % n]
        nx, ny = (yb - ya, xa - xb) if sa > 0 else (ya - yb, xb - xa)   # normal exterior
        if -nx + ny > 1e-9:
            f = [iso(xa, ya, z0), iso(xb, yb, z0), iso(xb, yb, z1), iso(xa, ya, z1)]
            caras.append(((-(xa + xb) / 2 + (ya + yb) / 2), f, (nx, ny)))
    for _, f, nrm in sorted(caras, key=lambda c: c[0]):
        hatch(f, "SOLID", layer="1-OCULTAR", rgb=fill, color=7)
        pl(f, layer, lw, True)
        if rayas and nrm[0] < 0 and abs(nrm[1]) < 1e-6:     # nervaduras de la cara exterior
            for yy in rayas: pl([iso(0, yy, z0), iso(0, yy, z1)], "1-VISTA", 9)
    cap = [iso(x, y, z0) for x, y in poly]
    hatch(cap, "SOLID", layer="1-OCULTAR", rgb=fill, color=7)
    pl(cap, layer, 25, True)
    return cap

# corte escalonado: chapa interior (atrás), núcleo con macho, chapa exterior (adelante)
E = 3.0  # espesor de chapa exagerado para que se lea en la axonometría
prisma([(T - E, 0), (T, 0), (T, HP), (T - E, HP)], 0, LP, "1-CHAPA", 25)
nuc = [(E, 0), (T - E, 0), (T - E, HP), (48, HP), (47, HP + 16), (29, HP + 16), (28, HP), (E, HP)]
cap = prisma(nuc, 200, LP, "1-CONTORNO", 18, (250, 250, 250))
hatch(cap, "HONEY", 0.3, 0, "1-NUCLEO-PUR", color=8); pl(cap, "1-CONTORNO", 25, True)
prisma([(0, 0), (E, 0), (E, HP), (0, HP)], 430, LP, "1-CHAPA", 25, (225, 225, 225), rayas=[HP * k / 8 for k in range(1, 8)])
pl([iso(38, HP + 16, 200), iso(38, HP + 16, LP)], "1-SELLADOS", 50)          # burlete sobre el macho
pl([iso(0, HP - 90, LP - 10), iso(-20, HP - 40, LP - 90), iso(0, HP - 5, LP - 150)], "1-VISTA", 13)  # film levantado
globo(1, iso(0, 280, 800), (138, 330))
globo(2, iso(40, HP * 0.5, 200), (22, 352))
globo(3, iso(T, 120, 90), (22, 318))
globo(4, iso(30, HP + 10, 330), (40, 372))
globo(5, iso(38, HP + 16, 700), (82, 375))
globo(17, iso(-10, HP - 50, LP - 90), (138, 362))
txt("e = 80 mm", 18, 304, 2.2)
txt("ancho útil 1000 mm  ·  largo a medida", 140, 302, 2.2, TA.RIGHT)

# ---------------------------------------------------------------- 02 FICHA TÉCNICA
titulo_detalle("2", "FICHA TÉCNICA", "", 152, 378, 130)
filas = [("Producto", "Panel sándwich de fachada, junta machihembrada"),
         ("Uso en el corte", "Cerramiento opaco (ref. 24) s/ estructura de acero"),
         ("Espesor nominal", "80 mm"),
         ("Ancho útil / total", "1000 mm / 1030 mm"),
         ("Largo", "a medida: 2,00 a 12,00 m"),
         ("Chapa ext. / int.", "acero galv. Z275 prepintado, e = 0,5 mm"),
         ("Terminación ext.", "microperfilada, poliéster 25 µm"),
         ("Núcleo", "poliuretano inyectado (PUR) 40 kg/m³"),
         ("Conductividad núcleo λ", "0,022 W/m·K"),
         ("Transmitancia K", "0,27 W/m²·K"),
         ("Peso propio", "≈ 11,5 kg/m²"),
         ("Aislación acústica Rw", "≈ 25 dB"),
         ("Luz máx. entre apoyos", "4,50 m (viento 100 kg/m²)"),
         ("Fijación", "tornillo autoperforante Ø6,3 + arandela EPDM"),
         ("Sellado de juntas", "burlete EPDM + sellador poliuretánico"),
         ("Colocación", "horizontal (también vertical)"),
         ("Colores", "blanco, gris, a elección (carta RAL)"),
         ("Tolerancias", "espesor ±2 mm · largo ±5 mm")]
fx0, fx1, fx2, fy = 152, 196, 282, 373
rh = 4.2
pl([(fx0, fy), (fx2, fy)], "3-TABLAS", 35)
for i, (a, b) in enumerate(filas):
    y = fy - (i + 1) * rh
    if i % 2 == 0: hatch([(fx0, y), (fx2, y), (fx2, y + rh), (fx0, y + rh)], "SOLID", layer="3-TABLAS", rgb=(238, 238, 238), color=254)
    txt(a, fx0 + 1.2, y + 1.4, 2.1, TA.LEFT, "3-TABLAS", True)
    txt(b, fx1 + 1.2, y + 1.4, 2.1, TA.LEFT, "3-TABLAS")
yb = fy - len(filas) * rh
pl([(fx0, yb), (fx2, yb)], "3-TABLAS", 35); pl([(fx1, fy), (fx1, yb)], "3-TABLAS", 13)
txt("Valores de referencia de catálogo: verificar con el fabricante elegido.", fx0, yb - 3.5, 2.0)

# ---------------------------------------------------------------- 03 SECCIÓN DEL PANEL 1:20 + JUNTA 1:2
titulo_detalle("3", "SECCIÓN", "ESC. 1:20", 15, 286, 44)
v = V(20, 33, 216)
sec = panel_poly(0, 1000)
dibujar_panel(v, sec, chapa_lw=35, sc_nucleo=0.16)
for xx in (0, 80):   # paneles contiguos sugeridos
    pl(v.P([(xx, -160), (xx, -6)]), "1-VISTA", 13); pl(v.P([(xx, 1030 + 140), (xx, 1030)]), "1-VISTA", 13)
v.dim((0, 1016), (80, 1016), 4, text="80")
v.dim((0, -2), (0, 1000), -6, vertical=True, text="1000 ÚTIL")
v.dim((80, -2 - G), (80, 1016), 6, vertical=True, text="1030 TOTAL")
txt("EXT.", v.p(0, 0)[0] - 15, v.p(0, 300)[1], 2.0, TA.MIDDLE_CENTER, rot=90)
txt("INT.", v.p(80, 0)[0] + 15, v.p(0, 300)[1], 2.0, TA.MIDDLE_CENTER, rot=90)
pl(v.rect(-20, 920, 100, 1060), "3-REFERENCIAS", 13, True, lt="DASHED")
txt("3a", v.p(100, 1060)[0] + 1, v.p(0, 1060)[1] - 1, 2.2, layer="3-REFERENCIAS")

# junta ampliada 1:2
titulo_detalle("3a", "JUNTA HORIZONTAL", "ESC. 1:2", 64, 286, 79)
v2 = V(2, 96, 241)
sup = perfil_hembra(0) + [(80, 44), (0, 44)]
inf = [(0, -40), (80, -40)] + list(reversed(perfil_macho(0)))
dibujar_panel(v2, inf, cortes=(-40,), chapa_lw=40, sc_nucleo=0.13)
dibujar_panel(v2, sup, cortes=(44,), chapa_lw=40, sc_nucleo=0.13)
for yy in (-40, 44): corte_rotura(v2, (-6, yy), (86, yy))
b1 = [(32, 16), (44, 16), (44, 22.5), (32, 22.5)]                     # burlete EPDM sobre el macho
hatch(v2.P(b1), "SOLID", layer="1-SELLADOS", color=250); pl(v2.P(b1), "1-SELLADOS", 18, True)
hatch(v2.P([(58, 0), (68, 0), (68, G), (58, G)]), "SOLID", layer="1-SELLADOS", color=250)   # sellador interior
v2.dim((0, -40), (80, -40), -5, text="80")
v2.dim((26, 23), (50, 23), 7, text="24")
v2.dim((80, 0), (80, 16), 6, vertical=True, text="16")
txt("EXT.", v2.p(0, 0)[0] - 9, v2.p(0, 0)[1], 2.0, TA.MIDDLE_CENTER, rot=90)
txt("INT.", v2.p(80, 0)[0] + 13, v2.p(0, 0)[1], 2.0, TA.MIDDLE_CENTER, rot=90)
globo(1, v2.p(0, 30), (76, 268)); globo(2, v2.p(20, -25), (76, 228)); globo(3, v2.p(80, 32), (140, 270))
globo(4, v2.p(28, 8), (76, 245)); globo(5, v2.p(38, 21), (110, 276)); globo(6, v2.p(63, 1), (140, 232))

# ---------------------------------------------------------------- 04 JUNTA VERTICAL SOBRE COLUMNA (PLANTA 1:5)
titulo_detalle("4", "JUNTA VERTICAL Y FIJACIÓN A COLUMNA - PLANTA", "ESC. 1:5", 152, 286, 130)
v4 = V(5, 217, 266)     # origen: eje de columna, cara exterior del panel; y real negativa hacia el interior
for s in (-1, 1):
    x_a, x_b = s * 10, s * 330
    poly = [(min(x_a, x_b), 0), (max(x_a, x_b), 0), (max(x_a, x_b), -80), (min(x_a, x_b), -80)]
    hatch(v4.P(poly), "HONEY", 0.11, 0, "1-NUCLEO-PUR", color=8)
    pl(v4.P([(x_b, 0), (x_a, 0), (x_a, -80), (x_b, -80)]), "1-CHAPA", 35)
    corte_rotura(v4, (x_b, 15), (x_b, -95))
# montante tubo 100x20x2 soldado al ala
tb = [(-50, -80), (50, -80), (50, -100), (-50, -100)]
hatch(v4.P(tb), "ANSI31", 0.12, 0, "1-ACERO", color=7)
hatch(v4.P([(-48, -82), (48, -82), (48, -98), (-48, -98)]), "SOLID", layer="1-OCULTAR", rgb=(255, 255, 255), color=7)
pl(v4.P(tb), "1-ACERO", 35, True); pl(v4.P([(-48, -82), (48, -82), (48, -98), (-48, -98)]), "1-ACERO", 18, True)
# columna IPN 300 (h 300, b 125, tw 10.8, tf 16.2) cortada
ipn = [(-62.5, -100), (62.5, -100), (62.5, -116.2), (5.4, -122), (5.4, -378), (62.5, -383.8), (62.5, -400),
       (-62.5, -400), (-62.5, -383.8), (-5.4, -378), (-5.4, -122), (-62.5, -116.2)]
ipn = [q for q in ipn if q[1] >= -200] + [(5.4, -200), (-5.4, -200)]
ipn = [(-62.5, -100), (62.5, -100), (62.5, -116.2), (5.4, -122), (5.4, -205), (-5.4, -205), (-5.4, -122), (-62.5, -116.2)]
hatch(v4.P(ipn), "ANSI31", 0.12, 0, "1-ACERO", color=7); pl(v4.P(ipn), "1-ACERO", 50, True)
corte_rotura(v4, (-30, -205), (30, -205))
# soldadura de filete (triángulos negros)
for s in (-1, 1):
    hatch(v4.P([(s * 50, -100), (s * 56, -100), (s * 50, -94)]), "SOLID", layer="1-ACERO", color=7)
# junta: cordón de respaldo + sellador, interior y exterior
for y0, y1 in ((0, -14), (-66, -80)):
    sel = [(-10, y0), (10, y0), (10, y0 + (y1 - y0) * 0.45), (-10, y0 + (y1 - y0) * 0.45)]
    hatch(v4.P(sel), "SOLID", layer="1-SELLADOS", color=250)
    cy = y0 + (y1 - y0) * 0.75
    circle(v4.p(0, cy), 1.6, "1-SELLADOS", 18)
pl(v4.P([(-10, -20), (-10, -60)]), "1-VISTA", 13)
# tornillos (cabeza exterior) hacia el montante
for s in (-1, 1):
    x = s * 30
    pl(v4.P([(x, 5), (x, -98)]), "1-TORNILLERIA", 35)
    for k in range(10): pl(v4.P([(x - 3, -55 - 4 * k), (x + 3, -53 - 4 * k)]), "1-TORNILLERIA", 9)
    pl(v4.P([(x - 9, 1), (x + 9, 1), (x + 9, 2), (x - 9, 2)]), "1-SELLADOS", 18, True)
    pl(v4.P([(x - 7, 2), (x + 7, 2), (x + 6, 5), (x - 6, 5)]), "1-TORNILLERIA", 25, True)
# tapajunta de chapa plegada
tj = [(-62, 1), (-62, 7), (62, 7), (62, 1)]
pl(v4.P([(-62, 0.5), (-60, 7), (60, 7), (62, 0.5)]), "1-CHAPA", 40)
v4.dim((-62.5, -116.2), (62.5, -116.2), -22, text="125 (ALA IPN 300)")
v4.dim((-10, 0), (10, 0), 9, text="20")
v4.dim((330, 0), (330, -80), 6, vertical=True, text="80")
v4.dim((330, -80), (330, -100), 6, vertical=True, text="20")
txt("EXTERIOR", v4.p(-200, 30)[0], v4.p(0, 30)[1], 2.2, TA.MIDDLE_CENTER)
txt("INTERIOR", v4.p(-200, -140)[0], v4.p(0, -140)[1], 2.2, TA.MIDDLE_CENTER)
globo(10, v4.p(-40, 7), (190, 270)); globo(7, v4.p(30, 4), (240, 272)); globo(6, v4.p(0, -4), (208, 274))
globo(1, v4.p(150, 0), (262, 270)); globo(2, v4.p(170, -40), (274, 260)); globo(3, v4.p(250, -80), (276, 248))
globo(8, v4.p(-40, -90), (174, 246)); globo(9, v4.p(-30, -160), (186, 232))

# ---------------------------------------------------------------- 05 REMATE SUPERIOR (CORTE 1:5)
titulo_detalle("5", "REMATE CON CUPERTINA", "ESC. 1:5", 15, 196, 86)
v5 = V(5, 26, 172)    # origen: cara ext. del panel, borde superior del panel
p5 = [(0, -260), (80, -260), (80, 0), (0, 0)]
dibujar_panel(v5, p5, cortes=(-260,), chapa_lw=35, sc_nucleo=0.11)
# montante tubo 100x20 (visto) y columna IPN 300 en corte longitudinal (recortada)
pl(v5.P([(80, -260), (80, -12), (100, -12), (100, -260)]), "1-ACERO", 25)
pl(v5.P([(82, -260), (82, -14), (98, -14), (98, -260)]), "1-VISTA", 9)
pl(v5.P([(100, -12), (260, -12)]), "1-ACERO", 35)
pl(v5.P([(116.2, -260), (116.2, -12)]), "1-VISTA", 13)
txt("IPN 300", v5.p(190, -140)[0], v5.p(0, -140)[1], 2.0, TA.MIDDLE_CENTER)
corte_rotura(v5, (-10, -260), (270, -260))
corte_rotura(v5, (260, -300), (260, 40))
tp = [(96, -12), (260, -12), (260, -4), (96, -4)]                       # tapa de columna 8 mm
hatch(v5.P(tp), "ANSI31", 0.12, 0, "1-ACERO", color=7); pl(v5.P(tp), "1-ACERO", 35, True)
hatch(v5.P([(4, 0), (76, 0), (76, 3), (4, 3)]), "SOLID", layer="1-SELLADOS", color=250)   # cinta butílica
cup = [(-22, -70), (-14, -62), (-14, 24), (260, 12)]                    # cupertina con pendiente al interior
pl(v5.P(cup), "1-CHAPA", 50)
pl(v5.P([(110, -4), (110, 19.5), (250, 13.4), (250, -4)]), "1-VISTA", 13)  # soporte de cupertina
tornillo_h(v5, -14, 95, -45)
pl(v5.P([(200, 14.5), (200, -12)]), "1-TORNILLERIA", 35)
pl(v5.P([(192, 18), (208, 17.4), (208, 15.4), (192, 16)]), "1-SELLADOS", 18, True)
v5.dim((0, -260), (80, -260), -6, text="80")
v5.dim((-14, 24), (-14, -62), -7, vertical=True, text="86")
txt("i = 5%", v5.p(170, 34)[0], v5.p(0, 34)[1], 2.0, TA.MIDDLE_CENTER)
txt("EXT.", v5.p(-60, -170)[0], v5.p(0, -170)[1], 2.0, TA.MIDDLE_CENTER, rot=90)
globo(11, v5.p(60, 21.5), (40, 189)); globo(18, v5.p(40, 2), (24, 185)); globo(7, v5.p(-14, -45), (18, 152))
globo(1, v5.p(0, -150), (18, 135)); globo(2, v5.p(40, -200), (24, 116)); globo(8, v5.p(90, -200), (52, 112))
globo(9, v5.p(150, -200), (80, 118)); globo(19, v5.p(200, -8), (90, 185))

# ---------------------------------------------------------------- 06 ARRANQUE SOBRE VIGA PORTAPANEL (CORTE 1:5)
titulo_detalle("6", "ARRANQUE S/ VIGA PORTAPANEL", "ESC. 1:5", 107, 196, 88)
v6 = V(5, 135, 124)   # origen: cara ext. del panel, nivel superior de fundación
fu = [(-60, 0), (260, 0), (260, -180), (-60, -180)]
hatch(v6.P(fu), "ANSI31", 0.35, 0, "1-HORMIGON", color=8)
pl(v6.P([(-60, -180), (-60, 0), (260, 0)]), "1-HORMIGON", 35)
corte_rotura(v6, (-70, -180), (270, -180)); corte_rotura(v6, (260, -190), (260, 10))
ce = [(-130, -100), (-62, -100), (-62, 22), (-130, 19)]                  # contrapiso exterior
hatch(v6.P(ce), "AR-CONC", 0.04, 0, "1-HORMIGON", color=8); pl(v6.P(ce), "1-HORMIGON", 18, True)
pl(v6.P([(-130, 25), (-62, 28), (-62, 22)]), "1-CONTORNO", 25)          # solado exterior c/ pendiente
corte_rotura(v6, (-130, 35), (-130, -110))
hatch(v6.P([(-12, 0), (92, 0), (92, 10), (-12, 10)]), "AR-SAND", 0.03, 0, "1-HORMIGON", color=8)   # mortero de nivelación
tube = [(-10, 10), (90, 10), (90, 70), (-10, 70)]
tin = [(-6.8, 13.2), (86.8, 13.2), (86.8, 66.8), (-6.8, 66.8)]
hatch(v6.P(tube), "ANSI31", 0.12, 0, "1-ACERO", color=7)
hatch(v6.P(tin), "SOLID", layer="1-OCULTAR", rgb=(255, 255, 255), color=7)
pl(v6.P(tube), "1-ACERO", 50, True); pl(v6.P(tin), "1-ACERO", 18, True)
pl(v6.P([(40, -120), (40, 30)]), "1-TORNILLERIA", 35)                   # anclaje químico Ø12
pl(v6.P([(30, 16), (50, 16), (50, 24), (30, 24)]), "1-TORNILLERIA", 25, True)
for k in range(14): pl(v6.P([(35, -115 + 8 * k), (45, -111 + 8 * k)]), "1-TORNILLERIA", 9)
pb = [(96, 0), (260, 0), (260, 22), (96, 22)]                           # placa base de columna
hatch(v6.P(pb), "ANSI31", 0.12, 0, "1-ACERO", color=7); pl(v6.P(pb), "1-ACERO", 35, True)
pl(v6.P([(100, 22), (100, 240)]), "1-ACERO", 35); pl(v6.P([(116.2, 22), (116.2, 240)]), "1-VISTA", 13)
pl(v6.P([(80, 74), (80, 240)]), "1-VISTA", 13)
txt("IPN 300", v6.p(190, 140)[0], v6.p(0, 140)[1], 2.0, TA.MIDDLE_CENTER)
corte_rotura(v6, (95, 240), (270, 240)); corte_rotura(v6, (260, 30), (260, 250))
pl(v6.P([(-1, 110), (-1, 71), (81, 71), (81, 110)]), "1-CHAPA", 40)   # perfil U de arranque
pl(v6.P([(-1, 72), (-15, 72), (-15, 28), (-24, 20)]), "1-CHAPA", 40)  # babeta con gotero
pl(v6.P([(30, 71), (30, 50)]), "1-TORNILLERIA", 35)
hatch(v6.P([(4, 72), (76, 72), (76, 75), (4, 75)]), "SOLID", layer="1-SELLADOS", color=250)
p6 = [(0, 75), (80, 75), (80, 240), (0, 240)]
dibujar_panel(v6, p6, cortes=(240,), chapa_lw=35, sc_nucleo=0.11)
corte_rotura(v6, (-20, 240), (95, 240))
tornillo_h(v6, -1, 100, 150)
v6.dim((-10, 10), (90, 10), -26, text="100")
v6.dim((-10, 10), (-10, 70), -9, vertical=True, text="60")
txt("±0,00", v6.p(-128, 45)[0], v6.p(0, 45)[1] + 0.8, 2.0, TA.LEFT)
globo(12, v6.p(-15, 50), (114, 150)); globo(13, v6.p(20, 60), (110, 128)); globo(14, v6.p(40, -60), (114, 92))
globo(15, v6.p(200, -100), (176, 86)); globo(16, v6.p(-100, -40), (112, 112)); globo(18, v6.p(60, 73.5), (170, 120))
globo(7, v6.p(-1, 150), (114, 168)); globo(2, v6.p(40, 200), (128, 186)); globo(9, v6.p(180, 180), (180, 186))

# ---------------------------------------------------------------- 07 MODULACIÓN (S/E) + MONTAJE
titulo_detalle("7", "MODULACIÓN EN FACHADA", "S/E", 199, 196, 83)
mx0, my0, mw, mh = 206, 152, 68, 30
cols = [mx0 + mw * k / 2 for k in range(3)]
for i in range(1, 6):
    pl([(mx0, my0 + i * mh / 6), (mx0 + mw, my0 + i * mh / 6)], "1-CONTORNO", 13)
pl([(mx0, my0), (mx0 + mw, my0), (mx0 + mw, my0 + mh), (mx0, my0 + mh)], "1-CONTORNO", 25, True)
for c in cols:
    pl([(c - 1.2, my0), (c - 1.2, my0 + mh)], "1-CHAPA", 18); pl([(c + 1.2, my0), (c + 1.2, my0 + mh)], "1-CHAPA", 18)
pl([(mx0 - 1.5, my0 + mh + 1.2), (mx0 + mw + 1.5, my0 + mh + 1.2)], "1-CHAPA", 50)       # cupertina
pl([(mx0 - 1.5, my0 - 0.8), (mx0 + mw + 1.5, my0 - 0.8)], "1-CHAPA", 50)                  # babeta
pl([(mx0 - 4, my0 - 2), (mx0 + mw + 4, my0 - 2)], "1-CONTORNO", 35)
txt("L ≤ 4,50 m", (cols[0] + cols[1]) / 2, my0 + mh + 4, 2.0, TA.MIDDLE_CENTER)
txt("L ≤ 4,50 m", (cols[1] + cols[2]) / 2, my0 + mh + 4, 2.0, TA.MIDDLE_CENTER)
pl([(mx0 + mw + 1, my0 + mh * 5 / 6), (mx0 + mw + 3, my0 + mh * 5 / 6)], "2-COTAS", 13)
pl([(mx0 + mw + 1, my0 + mh), (mx0 + mw + 3, my0 + mh)], "2-COTAS", 13)
txt("1,00", mx0 + mw + 2, my0 + mh * 11 / 12, 2.0, TA.MIDDLE_LEFT)
globo(11, (mx0 + 8, my0 + mh + 1.2), (mx0 - 2, my0 + mh + 7))
globo(10, (cols[1] + 1.2, my0 + mh * 0.3), (cols[1] + 9, my0 + mh * 0.18))
txt("Paneles horizontales de 1,00 m; juntas verticales sobre columnas (4).", 199, 145, 2.0)

txt("SECUENCIA DE MONTAJE", 199, 136, 2.6, TA.LEFT, "3-TITULOS", True)
pl([(199, 134), (282, 134)], "3-TITULOS", 25)
pasos = ["1. Nivelar y anclar la viga portapanel (13) a la fundación (15).",
         "2. Soldar los montantes (8) a las alas de las columnas IPN 300 (9).",
         "3. Fijar el perfil U de arranque con babeta (12) y colocar la cinta butílica (18).",
         "4. Montar los paneles de abajo hacia arriba, con el macho hacia arriba (4).",
         "5. Fijar cada panel en cada apoyo con 2 tornillos (7), sin aplastar el núcleo.",
         "6. Sellar las juntas verticales (6) y colocar los tapajuntas (10).",
         "7. Colocar la cupertina (11) y retirar el film protector (17)."]
import textwrap
yy = 130
for p in pasos:
    for j, ln in enumerate(textwrap.wrap(p, 62)):
        txt(ln if j == 0 else "    " + ln, 199, yy, 2.0); yy -= 3.3
    yy -= 0.9

# ---------------------------------------------------------------- REFERENCIAS
txt("REFERENCIAS", 15, 69, 2.8, TA.LEFT, "3-TITULOS", True)
pl([(15, 67), (W - 15, 67)], "3-TITULOS", 25)
refs = ["Chapa exterior acero galv. prepintado e=0,5 mm", "Núcleo de poliuretano inyectado (PUR) 80 mm",
        "Chapa interior acero galv. prepintado e=0,5 mm", "Junta machihembrada (macho / hembra)",
        "Burlete de EPDM", "Sellador poliuretánico + cordón de respaldo", "Tornillo autoperforante Ø6,3 c/ arandela EPDM",
        "Montante tubo 100x20x2 soldado al ala", "Columna IPN 300 (ref. 10 del corte)", "Tapajunta de chapa plegada prepintada",
        "Cupertina chapa galv. plegada c/ gotero (ref. 1)", "Perfil U de arranque + babeta c/ gotero",
        "Viga portapanel tubo 100x60x3,2 (ref. 28)", "Anclaje químico Ø12 mm", "Fundación base H°A° (ref. 21)",
        "Contrapiso + solado exterior (refs. 19 y 12)", "Film protector (se retira al terminar)", "Cinta butílica de sellado",
        "Tapa de columna e=8 mm + soporte de cupertina"]
cw = (W - 30) / 3
for i, r in enumerate(refs):
    col, row = divmod(i, 7)
    x, y = 15 + col * cw, 62 - row * 4.3
    circle((x + 2.2, y + 0.9), 1.9, "3-REFERENCIAS", 18)
    txt(str(i + 1), x + 2.2, y + 0.9, 2.0, TA.MIDDLE_CENTER, "3-REFERENCIAS")
    txt(r, x + 5.5, y, 2.0)

# ---------------------------------------------------------------- RÓTULO (mismo formato que el corte integral)
ry0, ry1 = 13, 33
xs = [15, 62, 175, 225, 282]
pl([(xs[0], ry0), (xs[-1], ry0), (xs[-1], ry1), (xs[0], ry1)], "0-MARCO", 50, True)
for x in xs[1:-1]: pl([(x, ry0), (x, ry1)], "0-MARCO", 25)
txt("LÁMINA 4", (xs[0] + xs[1]) / 2, 24.5, 5.0, TA.MIDDLE_CENTER, "3-TITULOS", True)
txt("FECHA: 19/10/26", xs[0] + 2, 15.5, 2.0)
txt("DOCENTE: Arq. Tucci y Arq. Cardozo", xs[1] + 2, 28.5, 2.0)
txt("ALUMNOS: Azcona Karina, Gómez Karen, Rosales Abril,", xs[1] + 2, 24.5, 2.0)
txt("Vitale Candelaria", xs[1] + 18.5, 21, 2.0)
txt("GRUPO: 13", xs[1] + 2, 15.5, 2.0)
txt("NIVEL:", xs[2] + 2, 28.5, 2.0); txt("OBS:", xs[2] + 2, 24.5, 2.0)
txt("CONSTRUCCIONES II", xs[3] + 2, 26.5, 2.4)
txt("CATEDRA: ARQ. TUCCI", xs[3] + 2, 20.5, 2.4)
txt("A3 - imprimir al 100%", xs[3] + 2, 15.2, 2.0)

doc.saveas(f"{OUT}/Lamina4_Catalogo_Opaco_A3.dxf")
print("ok")
