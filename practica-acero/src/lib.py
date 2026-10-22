# -*- coding: utf-8 -*-
"""Librería de dibujo para las láminas A4 de la práctica de acero.
Todo se dibuja en mm de papel (hoja A4 a escala 1:1). Cada dibujo se ubica con una View que
convierte mm reales a mm de papel con escala 1:s; las cotas muestran mm reales (dimlfac = s)."""
import math, os
import ezdxf
from ezdxf.enums import TextEntityAlignment as TA

OUT = os.environ.get("OUT", "build")
HMIN = 2.0                       # altura mínima de letra en la hoja impresa (mm)
TOTAL = 15
FECHA = "22/10/26"

LAYERS = {
    "0-MARCO": (7, "Continuous"), "1-SECCION": (7, "Continuous"), "1-VISTA": (7, "Continuous"),
    "1-OCULTO": (8, "DASHED2"), "1-EJES": (1, "CENTER2"), "2-RAYADO": (8, "Continuous"),
    "3-COTAS": (7, "Continuous"), "3-TEXTOS": (7, "Continuous"), "3-TITULOS": (7, "Continuous"),
    "3-REFS": (7, "Continuous"), "3-TABLAS": (7, "Continuous"),
}


from ezdxf.fonts import fonts as _fonts
_FC = {}


def tw(s, h, bold=False, wf=0.9):
    """Ancho real (mm) del texto con la fuente usada para dibujar (métricas de Arial = Liberation Sans)."""
    h = max(h, HMIN)
    k = (h, bold, wf)
    if k not in _FC:
        _FC[k] = _fonts.make_font("LiberationSans-Bold.ttf" if bold else "LiberationSans-Regular.ttf", h, wf)
    return _FC[k].text_width(s)


def wrap(s, w, h, bold=False):
    """Corta el texto en líneas de ancho w (mm) para altura h, midiendo con la fuente."""
    h = max(h, HMIN)
    out = []
    for par in s.split("\n"):
        line = ""
        for word in par.split(" "):
            cand = (line + " " + word) if line else word
            if not line or tw(cand, h, bold) <= w:
                line = cand
            else:
                out.append(line); line = word
        out.append(line)
    return out


class Sheet:
    def __init__(self, num, titulo, punto, escalas="", orient="P"):
        self.num, self.titulo, self.punto, self.escalas = num, titulo, punto, escalas
        self.W, self.H = (210.0, 297.0) if orient == "P" else (297.0, 210.0)
        d = ezdxf.new("R2018", setup=True); d.units = ezdxf.units.MM
        d.header["$LTSCALE"] = 0.35; d.header["$PSLTSCALE"] = 0
        d.styles.add("ARIAL", font="arial.ttf"); d.styles.add("ARIAL-NEGRITA", font="arialbd.ttf")
        for n, (c, lt) in LAYERS.items():
            d.layers.add(n, color=c, linetype=lt)
        ds = d.dimstyles.new("A4")
        ds.dxf.dimtxsty = "ARIAL"; ds.dxf.dimtxt = 2.0; ds.dxf.dimasz = 1.1; ds.dxf.dimtsz = 0.9
        ds.dxf.dimexe = 0.8; ds.dxf.dimexo = 0.6; ds.dxf.dimgap = 0.5; ds.dxf.dimdec = 0; ds.dxf.dimtad = 1
        ds.dxf.dimclrd = 7; ds.dxf.dimclre = 7; ds.dxf.dimclrt = 7; ds.dxf.dimlwd = 13; ds.dxf.dimlwe = 13
        ds.dxf.dimtih = 0; ds.dxf.dimtoh = 0; ds.dxf.dimjust = 0; ds.dxf.dimtmove = 0; ds.dxf.dimzin = 8
        self.doc, self.msp = d, d.modelspace()
        self.marco()

    # ------------------------------------------------------------------ primitivas en papel
    def pl(self, pts, layer="1-VISTA", lw=25, close=False, color=None, lt=None):
        a = {"layer": layer, "lineweight": lw}
        if color is not None: a["color"] = color
        if lt: a["linetype"] = lt
        return self.msp.add_lwpolyline(pts, close=close, dxfattribs=a)

    def circ(self, c, r, layer="1-VISTA", lw=25, color=None):
        a = {"layer": layer, "lineweight": lw}
        if color is not None: a["color"] = color
        return self.msp.add_circle(c, r, dxfattribs=a)

    def txt(self, s, x, y, h=2.0, align=TA.LEFT, layer="3-TEXTOS", bold=False, rot=0, color=None, maxw=None):
        h = max(h, HMIN)
        wf = 0.9
        if maxw and tw(s, h, bold) > maxw: wf = 0.9 * maxw / tw(s, h, bold)
        a = {"layer": layer, "style": "ARIAL-NEGRITA" if bold else "ARIAL", "width": wf, "rotation": rot}
        if color is not None: a["color"] = color
        t = self.msp.add_text(s, height=h, dxfattribs=a)
        t.set_placement((x, y), align=align); return t

    def solid(self, pts, gray=225, layer="2-RAYADO"):
        h = self.msp.add_hatch(color=8, dxfattribs={"layer": layer})
        h.set_solid_fill(color=8, rgb=(gray, gray, gray))
        h.paths.add_polyline_path(pts, is_closed=True); return h

    def para(self, x, y, w, s, h=2.0, bold=False, lead=1.55):
        """Párrafo con corte automático; devuelve la y debajo del último renglón."""
        h = max(h, HMIN)
        for ln in wrap(s, w, h, bold):
            self.txt(ln, x, y - h, h, bold=bold); y -= h * lead
        return y

    def bullets(self, x, y, w, items, h=2.0, lead=1.5, gap=0.6):
        h = max(h, HMIN)
        for it in items:
            if isinstance(it, tuple):              # (rótulo en negrita, texto)
                b, s = it
                self.txt(b, x, y - h, h, bold=True)
                bw = tw(b, h, True) + 1.0
                lines = wrap(s, w - bw, h)
                self.txt(lines[0], x + bw, y - h, h)
                y -= h * lead
                rest = " ".join(lines[1:])
                if rest: y = self.para(x + 2.5, y, w - 2.5, rest, h, lead=lead)
            else:
                self.txt("-", x, y - h, h)
                y = self.para(x + 2.5, y, w - 2.5, it, h, lead=lead)
            y -= gap
        return y

    def titulo_dib(self, x, y, n, s, esc="", w=None, h=2.6):
        """Título de dibujo: número en círculo negro + nombre + escala, subrayado."""
        r = 2.4
        c = self.msp.add_hatch(color=7, dxfattribs={"layer": "3-TITULOS"}); c.set_solid_fill(color=7)
        ep = c.paths.add_edge_path(); ep.add_arc((x + r, y), r, 0, 360)
        t = self.txt(str(n), x + r, y, 2.4, TA.MIDDLE_CENTER, "3-TITULOS", True)
        t.dxf.true_color = ezdxf.colors.rgb2int((255, 255, 255))     # número en blanco sobre el círculo
        self.txt(s, x + 2 * r + 1.5, y, h, TA.MIDDLE_LEFT, "3-TITULOS", True)
        wt = tw(s, h, True)
        if esc:
            if w: self.txt("ESC. " + esc, x + w, y - 0.1, 2.0, TA.MIDDLE_RIGHT, "3-TITULOS")
            else: self.txt("ESC. " + esc, x + 2 * r + 4 + wt, y - 0.1, 2.0, TA.MIDDLE_LEFT, "3-TITULOS")
            wt += tw("ESC. " + esc, 2.0) + 3
        ww = w if w else 2 * r + 2.5 + wt
        self.pl([(x, y - r - 0.8), (x + ww, y - r - 0.8)], "3-TITULOS", 35)

    def tabla(self, x, y, cols, filas, h=1.9, head=True, lead=1.45, pad=0.9):
        """cols = [(encabezado, ancho)]; las celdas se cortan en renglones. Devuelve y inferior."""
        h = max(h, HMIN)
        x1 = x + sum(c[1] for c in cols)
        rows = ([[c[0] for c in cols]] if head else []) + filas
        yy = y
        self.pl([(x, y), (x1, y)], "3-TABLAS", 35)
        for i, f in enumerate(rows):
            cells = [wrap(str(f[j]), cols[j][1] - 2 * pad, h) for j in range(len(cols))]
            nl = max(len(c) for c in cells)
            rh = nl * h * lead + 2 * pad - (lead - 1) * h
            if head and i == 0:
                self.solid([(x, yy), (x1, yy), (x1, yy - rh), (x, yy - rh)], 230, "3-TABLAS")
            xx = x
            for j, c in enumerate(cells):
                for k, ln in enumerate(c):
                    self.txt(ln, xx + pad, yy - pad - h - k * h * lead, h, layer="3-TABLAS",
                             bold=(head and i == 0) or (j == 0 and len(cols) > 2 and False))
                xx += cols[j][1]
            yy -= rh
            self.pl([(x, yy), (x1, yy)], "3-TABLAS", 35 if (head and i == 0) or i == len(rows) - 1 else 13)
        xx = x
        for j in range(len(cols) + 1):
            self.pl([(xx, y), (xx, yy)], "3-TABLAS", 35 if j in (0, len(cols)) else 13)
            if j < len(cols): xx += cols[j][1]
        return yy

    def globo(self, n, cpos, at=None, r=2.5, h=2.0):
        x, y = cpos
        if at is not None:
            dx, dy = at[0] - x, at[1] - y; L = math.hypot(dx, dy)
            if L > r:
                self.pl([(x + dx / L * r, y + dy / L * r), at], "3-REFS", 13)
                d = self.msp.add_hatch(color=7, dxfattribs={"layer": "3-REFS"}); d.set_solid_fill(color=7)
                ep = d.paths.add_edge_path(); ep.add_arc(at, 0.45, 0, 360)
        self.circ(cpos, r, "3-REFS", 25)
        self.txt(str(n), x, y, h, TA.MIDDLE_CENTER, "3-REFS", True, maxw=2 * r - 0.6)

    def view(self, ox, oy, s):
        return View(self, ox, oy, s)

    def view_in(self, box, real, s, ha="c", va="c"):
        """Ubica el rectángulo real (rx0, ry0, rx1, ry1) a escala 1:s dentro de la caja de papel
        box = (px0, py0, px1, py1), centrado (o alineado: ha l/c/r, va b/c/t)."""
        px0, py0, px1, py1 = box; rx0, ry0, rx1, ry1 = real
        w, h = (rx1 - rx0) / s, (ry1 - ry0) / s
        if w > px1 - px0 + 0.5 or h > py1 - py0 + 0.5:
            print(f"  AVISO lám {self.num}: dibujo {w:.0f}x{h:.0f} no entra en caja {px1 - px0:.0f}x{py1 - py0:.0f} (1:{s})")
        x = {"l": px0, "c": (px0 + px1 - w) / 2, "r": px1 - w}[ha]
        y = {"b": py0, "c": (py0 + py1 - h) / 2, "t": py1 - h}[va]
        if os.environ.get("DEBUG_BOX"):
            self.pl([(px0, py0), (px1, py0), (px1, py1), (px0, py1)], "0-MARCO", 0, True, color=3)
            self.pl([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], "0-MARCO", 0, True, color=5)
        return View(self, x - rx0 / s, y - ry0 / s, s)

    def leyenda(self, s, at, off, h=1.7):
        """Texto con línea de llamada: at en papel; el texto se ubica en at+off (izq. o der. según off)."""
        h = max(h, HMIN)
        c = (at[0] + off[0], at[1] + off[1])
        self.pl([at, c], "3-REFS", 13)
        d = self.msp.add_hatch(color=7, dxfattribs={"layer": "3-REFS"}); d.set_solid_fill(color=7)
        ep = d.paths.add_edge_path(); ep.add_arc(at, 0.35, 0, 360)
        right = off[0] >= 0
        self.pl([c, (c[0] + (1 if right else -1) * (tw(s, h) + 1), c[1])], "3-REFS", 13)
        self.txt(s, c[0] + (0.5 if right else -0.5), c[1] + 0.5, h, TA.LEFT if right else TA.RIGHT)

    # ------------------------------------------------------------------ marco y rótulo
    def marco(self):
        W, H = self.W, self.H
        self.L, self.R, self.T, self.B = 15.0, W - 7.0, H - 7.0, 7.0
        self.pl([(0, 0), (W, 0), (W, H), (0, H)], "0-MARCO", 0, True, color=9)
        self.pl([(self.L, self.B), (self.R, self.B), (self.R, self.T), (self.L, self.T)], "0-MARCO", 50, True)
        self.rotulo_top = self.B          # sin rótulo: el dibujo puede llegar hasta el marco

    def encabezado(self, s, sub=None):
        """Título general de la lámina arriba a la izquierda; devuelve la y libre."""
        self.txt(f"LÁMINA {self.num:02d}/{TOTAL}", self.R - 3, self.T - 6.5, 3.2, TA.LEFT if False else TA.RIGHT, "3-TITULOS", True)
        self.txt(s, self.L + 3, self.T - 6.5, 4.0, bold=True, layer="3-TITULOS", maxw=self.R - self.L - 40)
        y = self.T - 9.5
        if sub:
            self.txt(sub, self.L + 3, y - 2.2, 2.2, layer="3-TITULOS"); y -= 4
        self.pl([(self.L + 3, y), (self.R - 3, y)], "3-TITULOS", 50)
        return y - 2

    def save(self, name):
        os.makedirs(OUT, exist_ok=True)
        p = os.path.join(OUT, name + ".dxf")
        self.doc.saveas(p); return p


class View:
    """Ventana de dibujo: coordenadas reales (mm) -> papel (mm) con escala 1:s y origen (ox, oy)."""

    def __init__(self, sh, ox, oy, s):
        self.sh, self.ox, self.oy, self.s = sh, ox, oy, s

    def p(self, x, y): return (self.ox + x / self.s, self.oy + y / self.s)
    def P(self, pts): return [self.p(*q) for q in pts]

    def pl(self, pts, layer="1-VISTA", lw=25, close=False, **k):
        return self.sh.pl(self.P(pts), layer, lw, close, **k)

    def ln(self, a, b, layer="1-VISTA", lw=25, **k): return self.pl([a, b], layer, lw, **k)

    def rect(self, x0, y0, x1, y1, layer="1-VISTA", lw=25, **k):
        return self.pl([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], layer, lw, True, **k)

    def circ(self, c, r, layer="1-VISTA", lw=25, **k): return self.sh.circ(self.p(*c), r / self.s, layer, lw, **k)

    def arc(self, c, r, a0, a1, layer="1-VISTA", lw=25):
        return self.sh.msp.add_arc(self.p(*c), r / self.s, a0, a1, dxfattribs={"layer": layer, "lineweight": lw})

    def hatch(self, pts, kind="acero", holes=()):
        """kind: acero | hormigon | tierra | aislacion | gris | negro | mortero | vidrio | lana"""
        sh = self.sh
        if kind in ("gris", "negro", "vidrio"):
            g = {"gris": 215, "negro": 60, "vidrio": 235}[kind]
            h = sh.msp.add_hatch(color=8, dxfattribs={"layer": "2-RAYADO"})
            h.set_solid_fill(color=8, rgb=(g, g, g))
        else:
            pat, sc, ang = {"acero": ("ANSI31", 0.18, 0), "hormigon": ("AR-CONC", 0.035, 0),
                            "tierra": ("EARTH", 0.6, 45), "aislacion": ("ANSI37", 0.22, 0),
                            "mortero": ("AR-SAND", 0.02, 0), "lana": ("ANSI37", 0.35, 0),
                            "madera": ("ANSI36", 0.3, 0)}[kind]
            h = sh.msp.add_hatch(color=8, dxfattribs={"layer": "2-RAYADO"})
            h.set_pattern_fill(pat, color=8, scale=sc, angle=ang)
        h.paths.add_polyline_path(self.P(pts), is_closed=True)
        for hl in holes: h.paths.add_polyline_path(self.P(hl), is_closed=True)
        return h

    def dim(self, a, b, dist, ang=None, txt=None):
        """Cota lineal entre a y b (reales). ang None -> alineada horizontal/vertical según el par."""
        pa, pb = self.p(*a), self.p(*b)
        if ang is None: ang = 0 if abs(pb[0] - pa[0]) >= abs(pb[1] - pa[1]) else 90
        if ang == 0: base = (pa[0], (pa[1] if dist >= 0 else min(pa[1], pb[1])) + dist + (max(pa[1], pb[1]) - pa[1] if dist >= 0 else 0))
        else: base = ((pa[0] if dist < 0 else max(pa[0], pb[0])) + dist if dist >= 0 else min(pa[0], pb[0]) + dist, pa[1])
        ov = {"dimlfac": self.s}
        d = self.sh.msp.add_linear_dim(base=base, p1=pa, p2=pb, angle=ang, dimstyle="A4", override=ov,
                                      text=txt if txt else "<>", dxfattribs={"layer": "3-COTAS"})
        d.render(); return d

    def eje(self, a, b, label=None, at_end=True):
        self.ln(a, b, "1-EJES", 13)
        if label:
            pb = self.p(*(b if at_end else a)); pa = self.p(*(a if at_end else b))
            dx, dy = pb[0] - pa[0], pb[1] - pa[1]; L = math.hypot(dx, dy)
            c = (pb[0] + dx / L * 2.6, pb[1] + dy / L * 2.6)
            self.sh.circ(c, 2.6, "1-EJES", 18, color=7)
            self.sh.txt(label, c[0], c[1], 2.0, TA.MIDDLE_CENTER, "1-EJES", True, color=7)

    def nivel(self, x, y, s, lado=1):
        """Cota de nivel: triángulo + texto a la derecha (lado=1) o izquierda."""
        px, py = self.p(x, y)
        self.sh.pl([(px, py), (px - 1.2, py + 1.6), (px + 1.2, py + 1.6)], "3-COTAS", 18, True)
        self.sh.pl([(px - 1.2 if lado > 0 else px + 1.2, py + 1.6), (px + lado * 12, py + 1.6)], "3-COTAS", 13)
        self.sh.txt(s, px + lado * 2, py + 2.1, 1.9, TA.LEFT if lado > 0 else TA.RIGHT, "3-COTAS")

    def ref(self, n, at, cpos_paper_offset):
        """Globo con referencia: at en coords reales, desplazamiento del globo en mm de papel."""
        pa = self.p(*at)
        self.sh.globo(n, (pa[0] + cpos_paper_offset[0], pa[1] + cpos_paper_offset[1]), pa)

    def ley(self, s, at, off, h=1.7):
        self.sh.leyenda(s, self.p(*at), off, h)

    def label(self, s, x, y, h=1.9, align=TA.LEFT, bold=False, rot=0):
        px, py = self.p(x, y); return self.sh.txt(s, px, py, h, align, bold=bold, rot=rot)


# ====================================================================== perfiles y piezas
IPN = {200: (200, 90, 7.5, 11.3), 300: (300, 125, 10.8, 16.2), 450: (450, 170, 16.2, 24.3), 500: (500, 185, 18.0, 27.0),
       "HEB200": (200, 200, 9.0, 15.0)}
TAPER = {"HEB200": 0.0}                    # los HEB tienen alas paralelas; los IPN, pendiente 14 %


def ipn_poly(h, b, tw, tf, taper=0.14):
    """Contorno de un perfil doble T centrado en (0,0), alma vertical (IPN: alas con pendiente 14 %)."""
    q = (b - tw) / 4.0
    t_in = tf + taper * q           # espesor del ala junto al alma
    t_out = tf - taper * q          # espesor del ala en la punta
    y = h / 2
    half = [(b / 2, y), (b / 2, y - t_out), (tw / 2, y - t_in), (tw / 2, -y + t_in), (b / 2, -y + t_out), (b / 2, -y)]
    left = [(-px, py) for px, py in reversed(half)]
    return half + left


def perfil_poly(n):
    return ipn_poly(*IPN[n], taper=TAPER.get(n, 0.14))


def xf(pts, dx=0, dy=0, rot=0, sx=1):
    c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    return [(dx + sx * x * c - y * s, dy + sx * x * s + y * c) for x, y in pts]


def seccion_ipn(v, n, cx, cy, rot=0, hatch=True, lw=35):
    pts = xf(perfil_poly(n), cx, cy, rot)
    v.pl(pts, "1-SECCION", lw, True)
    if hatch: v.hatch(pts, "acero")
    return pts


def ipn_lateral(v, n, x0, x1, ytop, lw=35, layer="1-VISTA", hidden_web=False):
    """Vista lateral (alma de frente) de un IPN horizontal: contorno + líneas de ala."""
    h, b, tw, tf = IPN[n]
    v.rect(x0, ytop - h, x1, ytop, layer, lw)
    v.ln((x0, ytop - tf), (x1, ytop - tf), layer, 18)
    v.ln((x0, ytop - h + tf), (x1, ytop - h + tf), layer, 18)


def ipn_vertical(v, n, xc, y0, y1, frente=False, lw=35, layer="1-VISTA"):
    """Columna IPN vertical. frente=False: se ve el alma (ancho h); True: se ve el ala (ancho b)."""
    h, b, tw, tf = IPN[n]
    if frente:
        v.rect(xc - b / 2, y0, xc + b / 2, y1, layer, lw)
        v.ln((xc - tw / 2, y0), (xc - tw / 2, y1), "1-OCULTO", 13); v.ln((xc + tw / 2, y0), (xc + tw / 2, y1), "1-OCULTO", 13)
    else:
        v.rect(xc - h / 2, y0, xc + h / 2, y1, layer, lw)
        v.ln((xc - h / 2 + tf, y0), (xc - h / 2 + tf, y1), layer, 18)
        v.ln((xc + h / 2 - tf, y0), (xc + h / 2 - tf, y1), layer, 18)


def angular(v, x, y, a, e, rot=0, hatch=True, lw=35):
    """Sección de un angular L a x a x e con vértice en (x,y)."""
    pts = xf([(0, 0), (a, 0), (a, e), (e, e), (e, a), (0, a)], x, y, rot)
    v.pl(pts, "1-SECCION", lw, True)
    if hatch: v.hatch(pts, "acero")
    return pts


def bulon(v, a, b, d=16, cab=None, tuerca=True, lw=25):
    """Bulón de a hasta b (reales) visto de costado: cabeza hexagonal en a, tuerca y arandela en b."""
    ax, ay = a; bx, by = b
    L = math.hypot(bx - ax, by - ay); ux, uy = (bx - ax) / L, (by - ay) / L; nx, ny = -uy, ux
    k = cab or 0.65 * d; s = 1.6 * d
    def q(t, w): return (ax + ux * t + nx * w, ay + uy * t + ny * w)
    v.pl([q(-k, -s / 2), q(0, -s / 2), q(0, s / 2), q(-k, s / 2)], "1-VISTA", lw, True)
    v.ln(q(-k, -s / 4), q(0, -s / 4), "1-VISTA", 13); v.ln(q(-k, s / 4), q(0, s / 4), "1-VISTA", 13)
    ext = 0.8 * d + 6 + d * 0.4
    v.pl([q(0, -d / 2), q(L + ext, -d / 2), q(L + ext, d / 2), q(0, d / 2)], "1-VISTA", 18)
    if tuerca:
        v.pl([q(L, -1.1 * d), q(L + 3, -1.1 * d), q(L + 3, 1.1 * d), q(L, 1.1 * d)], "1-VISTA", 18, True)
        v.pl([q(L + 3, -s / 2), q(L + 3 + 0.8 * d, -s / 2), q(L + 3 + 0.8 * d, s / 2), q(L + 3, s / 2)], "1-VISTA", lw, True)
        v.ln(q(L + 3, -s / 4), q(L + 3 + 0.8 * d, -s / 4), "1-VISTA", 13)
        v.ln(q(L + 3, s / 4), q(L + 3 + 0.8 * d, s / 4), "1-VISTA", 13)


def bulon_planta(v, c, d=16, lw=18):
    v.circ(c, d * 0.8, "1-VISTA", lw)
    v.ln((c[0] - d, c[1]), (c[0] + d, c[1]), "1-EJES", 9); v.ln((c[0], c[1] - d), (c[0], c[1] + d), "1-EJES", 9)
    # hexágono de la tuerca
    r = d * 0.92
    v.pl([(c[0] + r * math.cos(math.radians(30 + 60 * i)), c[1] + r * math.sin(math.radians(30 + 60 * i))) for i in range(6)], "1-VISTA", lw, True)


def filete(v, p, a, dirx, diry):
    """Cordón de soldadura en ángulo (triángulo negro) de cateto a en el rincón p."""
    x, y = p
    v.hatch([(x, y), (x + dirx * a, y), (x, y + diry * a)], "negro")
    v.pl([(x, y), (x + dirx * a, y), (x, y + diry * a)], "1-SECCION", 13, True)


def deck_perfil(x0, n, paso=305, h=76, ts=120, bi=140, e=0):
    """Polilínea de la chapa colaborante trapezoidal (nervio hacia abajo), y=0 en la cresta superior.
    ts: ancho de la cresta superior; bi: ancho del valle inferior."""
    pts = []
    for i in range(n):
        x = x0 + i * paso
        # cresta (arriba) centrada en x + paso/2 ; valle (abajo) centrado en x
        pts += [(x - bi / 2, -h), (x + bi / 2, -h), (x + paso / 2 - ts / 2, 0), (x + paso / 2 + ts / 2, 0)]
    x = x0 + n * paso
    pts += [(x - bi / 2, -h), (x + bi / 2, -h)]
    return pts


def iso(x, y, z, k=1.0):
    """Proyección isométrica (x a la derecha-abajo... estándar) de coordenadas reales."""
    c, s = math.cos(math.radians(30)), math.sin(math.radians(30))
    return ((x - y) * c * k, ((x + y) * s + z) * k)


class IsoView:
    """Axonometría isométrica: (x, y, z) reales -> papel, escala 1:s, origen (ox, oy)."""

    def __init__(self, sh, ox, oy, s):
        self.sh, self.ox, self.oy, self.s = sh, ox, oy, s

    def p(self, x, y, z):
        u, w = iso(x, y, z)
        return (self.ox + u / self.s, self.oy + w / self.s)

    def P(self, pts): return [self.p(*q) for q in pts]

    def pl(self, pts, layer="1-VISTA", lw=25, close=False, **k):
        return self.sh.pl(self.P(pts), layer, lw, close, **k)

    def ln(self, a, b, layer="1-VISTA", lw=25, **k): return self.pl([a, b], layer, lw, **k)

    def face(self, pts, gray=235, lw=18, layer="1-VISTA"):
        pp = self.P(pts)
        if gray is not None: self.sh.solid(pp, gray)
        self.sh.pl(pp, layer, lw, True)

    def box(self, x0, y0, z0, x1, y1, z1, grays=(250, 225, 200), lw=18):
        """Prisma: caras visibles en isométrica = superior (z1), frente y=y0 y lateral x=x0."""
        self.face([(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)], grays[0], lw)
        self.face([(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)], grays[1], lw)
        self.face([(x0, y0, z0), (x0, y1, z0), (x0, y1, z1), (x0, y0, z1)], grays[2], lw)

    def ref(self, n, at3, off):
        pa = self.p(*at3)
        self.sh.globo(n, (pa[0] + off[0], pa[1] + off[1]), pa)


def ficha_spec(sh, x, y, w, items, h=1.8, lead=1.42):
    """Bloque de especificación: [(rótulo, texto)] con rótulo en negrita en su propio renglón-cabecera."""
    h = max(h, HMIN)
    for b, s in items:
        sh.txt(b, x, y - h, h, bold=True)
        bw = tw(b + " ", h, True)
        lines = wrap(s, w - bw, h)
        sh.txt(lines[0], x + bw, y - h, h)
        y -= h * lead
        rest = " ".join(lines[1:])
        if rest:
            for ln in wrap(rest, w, h):
                sh.txt(ln, x, y - h, h); y -= h * lead
        y -= 0.5
    return y


def clip_x(pts, x0, x1):
    """Recorta una polilínea monótona en x al intervalo [x0, x1]."""
    out = []
    for i in range(len(pts) - 1):
        (ax, ay), (bx, by) = pts[i], pts[i + 1]
        if bx < x0 or ax > x1: continue
        def at(x): return (x, ay + (by - ay) * (x - ax) / (bx - ax)) if bx != ax else (x, ay)
        a = (ax, ay) if ax >= x0 else at(x0)
        b = (bx, by) if bx <= x1 else at(x1)
        if not out or out[-1] != a: out.append(a)
        out.append(b)
    return out


PASO, H_NERV, CRESTA, VALLE = 305, 76, 120, 140


def losa_transversal(v, x0, x1, ztop, xvalle=0, e=140, malla=True, hatch=True, lw_chapa=35):
    """Losa colaborante cortada en sentido transversal a los nervios (se ven los trapecios).
    xvalle: x de un valle (apoyo sobre la viga). Devuelve la polilínea de la chapa."""
    zc = ztop - e + H_NERV                       # cota de la cresta
    n0 = int((x0 - xvalle) // PASO) - 2
    prof = deck_perfil(xvalle + n0 * PASO, int((x1 - x0) // PASO) + 5, PASO, H_NERV, CRESTA, VALLE)
    prof = [(x, zc + y) for x, y in prof]
    ch = clip_x(prof, x0, x1)
    if hatch:
        v.hatch([(x0, ztop)] + ch + [(x1, ztop)], "hormigon")
    v.pl(ch, "1-SECCION", lw_chapa)
    v.pl([(x0, ztop), (x1, ztop)], "1-SECCION", 35)
    v.ln((x0, ztop), ch[0], "1-VISTA", 13); v.ln((x1, ztop), ch[-1], "1-VISTA", 13)
    if malla:
        v.ln((x0 + 10, ztop - 30), (x1 - 10, ztop - 30), "1-VISTA", 18)
        x = x0 + 75
        while x < x1 - 20:
            v.circ((x, ztop - 34), 3, "1-VISTA", 13); x += 150
    return ch


def losa_longitudinal(v, x0, x1, ztop, e=140, malla=True, hatch=True):
    """Losa colaborante cortada en el sentido de los nervios: chapa en el valle (apoyo) y cresta oculta."""
    zb = ztop - e
    if hatch: v.hatch([(x0, zb), (x1, zb), (x1, ztop), (x0, ztop)], "hormigon")
    v.pl([(x0, zb), (x1, zb)], "1-SECCION", 35)
    v.pl([(x0, ztop), (x1, ztop)], "1-SECCION", 35)
    v.ln((x0, zb + H_NERV), (x1, zb + H_NERV), "1-OCULTO", 13)
    v.ln((x0, zb), (x0, ztop), "1-VISTA", 13); v.ln((x1, zb), (x1, ztop), "1-VISTA", 13)
    if malla:
        v.ln((x0 + 10, ztop - 30), (x1 - 10, ztop - 30), "1-VISTA", 18)


def stud(v, x, zb, h=125, d=19):
    """Conector de corte tipo perno con cabeza (Nelson) soldado desde zb hacia arriba."""
    v.rect(x - d / 2, zb, x + d / 2, zb + h - 10, "1-VISTA", 25)
    v.rect(x - 16, zb + h - 10, x + 16, zb + h, "1-VISTA", 25)
    v.hatch([(x - d / 2, zb), (x + d / 2, zb), (x + d / 2, zb + h - 10), (x - d / 2, zb + h - 10)], "gris")
    v.hatch([(x - 16, zb + h - 10), (x + 16, zb + h - 10), (x + 16, zb + h), (x - 16, zb + h)], "gris")


def marca_u(sh, n, at, off, r=3.3):
    """Marca de unión: hexágono con 'U n' y línea de llamada al punto at (papel)."""
    c = (at[0] + off[0], at[1] + off[1])
    dx, dy = at[0] - c[0], at[1] - c[1]; Lr = math.hypot(dx, dy)
    if Lr > r:
        sh.pl([(c[0] + dx / Lr * r, c[1] + dy / Lr * r), at], "3-REFS", 18)
        d = sh.msp.add_hatch(color=7, dxfattribs={"layer": "3-REFS"}); d.set_solid_fill(color=7)
        ep = d.paths.add_edge_path(); ep.add_arc(at, 0.5, 0, 360)
    pts = [(c[0] + r * math.cos(math.radians(60 * i)), c[1] + r * math.sin(math.radians(60 * i))) for i in range(6)]
    sh.solid(pts, 40, "3-REFS")
    sh.pl(pts, "3-REFS", 25, True)
    t = sh.txt(f"U{n}", c[0], c[1], 2.0, TA.MIDDLE_CENTER, "3-REFS", True, maxw=2 * r - 0.8)
    t.dxf.true_color = ezdxf.colors.rgb2int((255, 255, 255))
