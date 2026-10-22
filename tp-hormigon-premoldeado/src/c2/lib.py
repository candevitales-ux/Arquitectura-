# -*- coding: utf-8 -*-
"""Práctica C2 – librería de dibujo para láminas A4.
Cada primitiva se registra UNA vez y se emite a SVG (PDF vía Chromium) y a DXF (DWG vía ODA) en milímetros de papel
(escala 1:1 de la hoja). Las vistas (View) convierten mm reales -> mm de papel según la escala del dibujo."""
import math
import numpy as np
from shapely.geometry import Polygon, Point
from shapely.strtree import STRtree

W, H = 297.0, 210.0          # A4 apaisada
FONT = "Arial, 'Liberation Sans', Helvetica, sans-serif"
CW = 0.53                    # ancho medio de carácter / tamaño de fuente (Arial)

# ------------------------------------------------------------------ materiales (relleno SVG, color de fondo DXF, rayado DXF)
MAT = {
    "HA":    ("url(#pHA)",   "#d3d6d9", ("ANSI31", 0.25, 0)),     # H°A° premoldeado / pretensado
    "HAis":  ("url(#pHAis)", "#dedad2", ("AR-CONC", 0.03, 0)),    # H°A° in situ
    "H":     ("url(#pH)",    "#e6e4df", ("AR-CONC", 0.025, 0)),   # H° simple / limpieza
    "mort":  ("url(#pMort)", "#e9e9e9", ("AR-SAND", 0.015, 0)),
    "grout": ("url(#pGrout)", "#bdbdbd", ("AR-SAND", 0.01, 0)),
    "tierra": ("url(#pTierra)", "#ece3d2", ("EARTH", 0.4, 45)),
    "tosca": ("url(#pTosca)", "#efe4c8", ("GRAVEL", 0.25, 0)),
    "eps":   ("url(#pEPS)",  "#fff5bf", ("ZIGZAG", 0.2, 0)),
    "epsv":  ("url(#pEPSv)", "#fff5bf", ("ZIGZAG", 0.2, 90)),
    "lana":  ("url(#pLana)", "#fbe2a8", ("INSUL", 0.08, 0)),
    "lanav": ("url(#pLanaV)", "#fbe2a8", ("INSUL", 0.08, 90)),
    "acero": ("#3b3b3b", "#3b3b3b", None),
    "neo":   ("#111111", "#111111", None),
    "vidrio": ("#bfe3f0", "#bfe3f0", None),
    "alu":   ("#9aa3ab", "#9aa3ab", None),
    "vista": ("#eceeef", "#eceeef", None),
    "blanco": ("#ffffff", None, None),
}
DEFS = '''
<pattern id="pHA" patternUnits="userSpaceOnUse" width="1.1" height="1.1" patternTransform="rotate(45)">
 <rect width="1.1" height="1.1" fill="#d3d6d9"/><line x1="0" y1="0" x2="0" y2="1.1" stroke="#4a4f55" stroke-width="0.08"/></pattern>
<pattern id="pHAis" patternUnits="userSpaceOnUse" width="2" height="2" patternTransform="rotate(45)">
 <rect width="2" height="2" fill="#dedad2"/><line x1="0" y1="0" x2="0" y2="2" stroke="#4a4f55" stroke-width="0.08"/>
 <circle cx="1" cy="0.5" r="0.12" fill="#4a4f55"/><circle cx="1.3" cy="1.5" r="0.08" fill="#4a4f55"/></pattern>
<pattern id="pH" patternUnits="userSpaceOnUse" width="2.4" height="2.4">
 <rect width="2.4" height="2.4" fill="#e6e4df"/><circle cx="0.5" cy="0.6" r="0.13" fill="#666"/><circle cx="1.7" cy="1.5" r="0.1" fill="#666"/>
 <path d="M1.4 0.3 l0.3 0.45 h-0.6z" fill="none" stroke="#666" stroke-width="0.06"/><circle cx="2.1" cy="0.4" r="0.06" fill="#666"/></pattern>
<pattern id="pMort" patternUnits="userSpaceOnUse" width="1" height="1">
 <rect width="1" height="1" fill="#e9e9e9"/><circle cx="0.25" cy="0.25" r="0.07" fill="#777"/><circle cx="0.75" cy="0.7" r="0.05" fill="#777"/></pattern>
<pattern id="pGrout" patternUnits="userSpaceOnUse" width="0.7" height="0.7">
 <rect width="0.7" height="0.7" fill="#bdbdbd"/><circle cx="0.18" cy="0.18" r="0.07" fill="#333"/><circle cx="0.52" cy="0.52" r="0.07" fill="#333"/></pattern>
<pattern id="pTierra" patternUnits="userSpaceOnUse" width="5" height="5">
 <rect width="5" height="5" fill="#ece3d2"/><g stroke="#8a7350" stroke-width="0.1"><line x1="0.4" y1="1.7" x2="1.7" y2="0.4"/>
 <line x1="0.9" y1="1.9" x2="2" y2="0.8"/><line x1="2.9" y1="4.3" x2="4.2" y2="3"/></g><circle cx="3.8" cy="1" r="0.13" fill="#8a7350"/></pattern>
<pattern id="pTosca" patternUnits="userSpaceOnUse" width="1.8" height="1.8">
 <rect width="1.8" height="1.8" fill="#efe4c8"/><circle cx="0.45" cy="0.45" r="0.16" fill="#9b8459"/><circle cx="1.35" cy="1.3" r="0.1" fill="#9b8459"/></pattern>
<pattern id="pEPS" patternUnits="userSpaceOnUse" width="1.4" height="1.4">
 <rect width="1.4" height="1.4" fill="#fff5bf"/><path d="M0 0.7 L0.35 0.25 L0.7 0.7 L1.05 1.15 L1.4 0.7" fill="none" stroke="#a08a1a" stroke-width="0.08"/></pattern>
<pattern id="pEPSv" patternUnits="userSpaceOnUse" width="1.4" height="1.4" patternTransform="rotate(90)">
 <rect width="1.4" height="1.4" fill="#fff5bf"/><path d="M0 0.7 L0.35 0.25 L0.7 0.7 L1.05 1.15 L1.4 0.7" fill="none" stroke="#a08a1a" stroke-width="0.08"/></pattern>
<pattern id="pLana" patternUnits="userSpaceOnUse" width="1.8" height="1.1">
 <rect width="1.8" height="1.1" fill="#fbe2a8"/><path d="M0 0.55 C0.45 0 0.45 0 0.9 0.55 S1.35 1.1 1.8 0.55" fill="none" stroke="#b07b18" stroke-width="0.08"/></pattern>
<pattern id="pLanaV" patternUnits="userSpaceOnUse" width="1.8" height="1.1" patternTransform="rotate(90)">
 <rect width="1.8" height="1.1" fill="#fbe2a8"/><path d="M0 0.55 C0.45 0 0.45 0 0.9 0.55 S1.35 1.1 1.8 0.55" fill="none" stroke="#b07b18" stroke-width="0.08"/></pattern>
<marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse" markerUnits="userSpaceOnUse">
 <path d="M0,1 L10,5 L0,9 z" fill="#000"/></marker>
'''
REB = "#7a1f1f"


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def f(v):
    return f"{v:.3f}".rstrip("0").rstrip(".")


def rgb(h):
    h = h.strip().lstrip("#")
    if len(h) == 3: h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def shade(hexcol, k):
    r, g, b = rgb(hexcol)
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(c * k))) for c in (r, g, b))


def lw(sw):
    for k in (9, 13, 18, 25, 35, 50, 70):
        if sw * 100 <= k + 2: return k
    return 70


def wrap(text, width, size):
    """corte de líneas por ancho estimado (mismo resultado en SVG y DXF)"""
    maxc = max(4, int(width / (size * CW)))
    out = []
    for para in str(text).split("\n"):
        line = ""
        for w in para.split(" "):
            t = (line + " " + w).strip()
            if len(t) > maxc and line:
                out.append(line); line = w
            else:
                line = t
        out.append(line)
    return out


class Sheet:
    def __init__(self, num, total, title, subtitle="", escalas=""):
        self.num, self.total, self.title, self.subtitle, self.escalas = num, total, title, subtitle, escalas
        self.ops = []        # registro de primitivas en papel (y hacia abajo)
        self.svg = []

    # ---------------------------------------------------------- primitivas en papel
    def poly(self, pts, fill=None, mat=None, stroke="#000", sw=0.25, dash=None, closed=True, layer="CONTORNOS", opacity=None):
        pts = [(float(x), float(y)) for x, y in pts]
        if mat:
            fsvg, bg, hat = MAT[mat]
        else:
            fsvg, bg, hat = (fill or "none"), (fill if fill and fill not in ("none",) else None), None
        d = " ".join(f"{f(x)},{f(y)}" for x, y in pts)
        tag = "polygon" if closed else "polyline"
        ex = f' stroke-dasharray="{dash}"' if dash else ""
        op = f' fill-opacity="{opacity}"' if opacity is not None else ""
        st = stroke if stroke else "none"
        self.svg.append(f'<{tag} points="{d}" fill="{fsvg if closed else "none"}"{op} stroke="{st}" stroke-width="{f(sw)}" '
                        f'stroke-linejoin="round" stroke-linecap="round"{ex}/>')
        self.ops.append(dict(t="poly", pts=pts, bg=bg if closed else None, hat=hat if closed else None, stroke=stroke, sw=sw,
                             dash=dash, closed=closed, layer=layer, mat=mat))

    def rect(self, x0, y0, x1, y1, **k):
        self.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], **k)

    def line(self, x0, y0, x1, y1, stroke="#000", sw=0.18, dash=None, layer="LINEAS"):
        self.poly([(x0, y0), (x1, y1)], stroke=stroke, sw=sw, dash=dash, closed=False, layer=layer)

    def pline(self, pts, stroke="#000", sw=0.18, dash=None, layer="LINEAS"):
        self.poly(pts, stroke=stroke, sw=sw, dash=dash, closed=False, layer=layer)

    def circle(self, x, y, r, fill="none", stroke="#000", sw=0.18, layer="LINEAS", dash=None):
        ex = f' stroke-dasharray="{dash}"' if dash else ""
        self.svg.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="{fill}" stroke="{stroke or "none"}" stroke-width="{f(sw)}"{ex}/>')
        self.ops.append(dict(t="circ", c=(x, y), r=r, fill=None if fill in (None, "none") else fill, stroke=stroke, sw=sw, layer=layer, dash=dash))

    def arc(self, cx, cy, r, a0, a1, n=24, **k):
        pts = [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy - r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]
        self.pline(pts, **k)
        return pts

    def text(self, x, y, s, size=2.2, anchor="start", bold=False, ital=False, color="#000", rot=0, layer="TEXTOS"):
        s = str(s)
        a = {"start": "start", "middle": "middle", "end": "end"}[anchor]
        tr = f' transform="rotate({f(-rot)} {f(x)} {f(y)})"' if rot else ""
        self.svg.append(f'<text x="{f(x)}" y="{f(y)}" font-family="{FONT}" font-size="{f(size)}" text-anchor="{a}"'
                        f'{" font-weight=\"bold\"" if bold else ""}{" font-style=\"italic\"" if ital else ""} fill="{color}"{tr}>{esc(s)}</text>')
        self.ops.append(dict(t="text", p=(x, y), s=s, size=size, anchor=anchor, bold=bold, ital=ital, color=color, rot=rot, layer=layer))

    def para(self, x, y, width, text, size=2.0, lead=1.3, **k):
        for ln in wrap(text, width, size):
            self.text(x, y, ln, size, **k); y += size * lead
        return y

    def bullets(self, x, y, width, items, size=2.0, lead=1.3, gap=0.4, mark="•", **k):
        for it in items:
            lines = wrap(it, width - size * 1.2, size)
            self.text(x, y, mark, size, **k)
            for ln in lines:
                self.text(x + size * 1.1, y, ln, size, **k); y += size * lead
            y += gap
        return y

    def ball(self, x, y, label, r=2.0, size=None, fill="#fff", color="#000", layer="REFERENCIAS"):
        self.circle(x, y, r, fill=fill, stroke=color, sw=0.22, layer=layer)
        self.text(x, y + (size or r * 0.95) * 0.36, label, size or r * 0.95, anchor="middle", bold=True, color=color, layer=layer)

    def leader(self, pts, dot=True, sw=0.15, layer="REFERENCIAS", color="#000"):
        self.pline(pts, sw=sw, layer=layer, stroke=color)
        if dot: self.circle(pts[0][0], pts[0][1], 0.35, fill=color, stroke=None, sw=0, layer=layer)

    def callout(self, target, at, label, r=2.0, **k):
        """globo en 'at' con línea al punto 'target'"""
        tx, ty = target; ax, ay = at
        d = math.hypot(tx - ax, ty - ay)
        if d > r:
            self.leader([target, (ax + (tx - ax) * r / d, ay + (ty - ay) * r / d)], **k)
        self.ball(ax, ay, label, r)

    def note(self, target, at, txt, size=1.9, anchor="start", **k):
        """texto con línea de referencia"""
        tx, ty = target; ax, ay = at
        self.leader([target, (ax, ay)])
        self.line(ax, ay, ax + (len(txt) * size * CW + 0.6) * (1 if anchor == "start" else -1), ay, sw=0.15, layer="REFERENCIAS")
        self.text(ax + (0.3 if anchor == "start" else -0.3), ay - 0.6, txt, size, anchor=anchor, **k)

    def dim(self, p1, p2, off, txt, size=1.8, ext=True, layer="COTAS"):
        """cota alineada en papel: p1-p2, desplazada 'off' (mm papel, + a la izquierda del vector p1->p2)"""
        (x1, y1), (x2, y2) = p1, p2
        L = math.hypot(x2 - x1, y2 - y1)
        if L < 1e-6: return
        ux, uy = (x2 - x1) / L, (y2 - y1) / L
        nx, ny = uy, -ux                      # normal (izquierda en pantalla con y abajo)
        a1 = (x1 + nx * off, y1 + ny * off); a2 = (x2 + nx * off, y2 + ny * off)
        s = 1 if off >= 0 else -1
        if ext:
            self.line(x1 + nx * s * 0.6, y1 + ny * s * 0.6, a1[0] + nx * s * 1.0, a1[1] + ny * s * 1.0, sw=0.1, layer=layer)
            self.line(x2 + nx * s * 0.6, y2 + ny * s * 0.6, a2[0] + nx * s * 1.0, a2[1] + ny * s * 1.0, sw=0.1, layer=layer)
        self.line(a1[0] - ux * 1.0, a1[1] - uy * 1.0, a2[0] + ux * 1.0, a2[1] + uy * 1.0, sw=0.12, layer=layer)
        for (ax, ay) in (a1, a2):
            k = 0.7
            self.line(ax - (ux + nx) * k, ay - (uy + ny) * k, ax + (ux + nx) * k, ay + (uy + ny) * k, sw=0.28, layer=layer)
        ang = math.degrees(math.atan2(-(y2 - y1), x2 - x1))
        if ang > 90.1: ang -= 180
        if ang < -89.9: ang += 180
        mx, my = (a1[0] + a2[0]) / 2, (a1[1] + a2[1]) / 2
        # texto del lado exterior de la línea de cota
        tx, ty = mx + nx * s * 0.6, my + ny * s * 0.6
        if abs(ang - 90) < 1 or abs(ang + 90) < 1:
            ang = 90
            tx = mx - 0.6
            ty = my
        self.text(tx, ty, txt, size, anchor="middle", rot=ang, layer=layer)

    def level(self, x, y, txt, size=1.8, side=1, layer="COTAS"):
        """marca de nivel (triángulo) + texto"""
        self.poly([(x - 1.2, y - 1.6), (x + 1.2, y - 1.6), (x, y)], fill="#000", stroke="#000", sw=0.1, layer=layer)
        self.line(x - 3 * side, y, x + 8 * side, y, sw=0.12, layer=layer)
        self.text(x + 1.8 * side, y - 1.0, txt, size, anchor="start" if side > 0 else "end", bold=True, layer=layer)

    def scalebar(self, x, y, scale, total_m, step_m, size=1.6):
        L = total_m * 1000 / scale
        n = int(round(total_m / step_m))
        for i in range(n):
            x0 = x + L * i / n; x1 = x + L * (i + 1) / n
            self.rect(x0, y, x1, y + 1.0, fill="#000" if i % 2 == 0 else "#fff", stroke="#000", sw=0.12, layer="COTAS")
        for i in range(n + 1):
            v = step_m * i
            self.text(x + L * i / n, y + 3.0, (f"{v:g}" if v else "0"), size * 0.9, anchor="middle", layer="COTAS")
        self.text(x + L + 1.2, y + 1.0, "m", size * 0.9, layer="COTAS")

    def title_drawing(self, x, y, title, scale_txt=None, size=2.6):
        self.text(x, y, title, size, bold=True)
        w = len(title) * size * 0.6
        self.line(x, y + 0.9, x + w, y + 0.9, sw=0.3)
        if scale_txt: self.text(x, y + size * 1.25 + 0.6, scale_txt, size * 0.72, color="#222")

    def table(self, x, y, colw, rows, size=1.75, rowh=None, head=True, lead=1.22, fills=None):
        """tabla con ajuste de texto por celda; devuelve y final"""
        for ri, row in enumerate(rows):
            cells = [wrap(c, colw[i] - 1.6, size) for i, c in enumerate(row)]
            nl = max(len(c) for c in cells)
            h = rowh or (nl * size * lead + size * 0.75)
            xx = x
            bg = "#e2e6ea" if (head and ri == 0) else (fills[ri] if fills and fills[ri] else None)
            for ci, c in enumerate(cells):
                self.rect(xx, y, xx + colw[ci], y + h, fill=bg or "none", stroke="#000", sw=0.15, layer="TABLAS")
                yy = y + size * 1.05 + 0.3
                for ln in c:
                    self.text(xx + 0.8, yy, ln, size, bold=(head and ri == 0) or (ci == 0 and not head), layer="TABLAS"); yy += size * lead
                xx += colw[ci]
            y += h
        return y

    # ---------------------------------------------------------- marco + rótulo
    def frame(self):
        self.rect(5, 5, W - 5, H - 5, stroke="#000", sw=0.5, layer="MARCO")
        y0 = H - 17
        self.rect(5, y0, W - 5, H - 5, stroke="#000", sw=0.4, layer="MARCO")
        xs = [5, 52, 112, 168, 232, W - 5]
        for xx in xs[1:-1]: self.line(xx, y0, xx, H - 5, sw=0.3, layer="MARCO")
        self.text(7, y0 + 4.6, "C2 · PRÁCTICA EN CLASE", 2.3, bold=True, layer="MARCO")
        self.text(7, y0 + 8.3, "Hormigón premoldeado de grandes luces", 1.6, layer="MARCO")
        self.text(7, y0 + 10.9, "Fecha: 22/10/2026", 1.6, layer="MARCO")
        self.text(54, y0 + 3.6, "DOCENTE: Arq. Tucci y Arq. Cardozo", 1.6, layer="MARCO")
        self.text(54, y0 + 6.6, "ALUMNA: Candelaria Vitale", 1.6, layer="MARCO")
        self.text(54, y0 + 9.6, "GRUPO: 13", 1.6, layer="MARCO")
        self.text(114, y0 + 3.6, self.title.upper(), 1.9, bold=True, layer="MARCO")
        yy = y0 + 6.6
        for ln in wrap(self.subtitle, 52, 1.5)[:2]:
            self.text(114, yy, ln, 1.5, layer="MARCO"); yy += 2.6
        self.text(170, y0 + 3.6, "ESCALAS:", 1.6, bold=True, layer="MARCO")
        yy = y0 + 6.6
        for ln in wrap(self.escalas, 60, 1.5)[:2]:
            self.text(170, yy, ln, 1.5, layer="MARCO"); yy += 2.6
        self.text(234, y0 + 3.6, "CONSTRUCCIONES II", 1.8, bold=True, layer="MARCO")
        self.text(234, y0 + 6.6, "CÁTEDRA: ARQ. TUCCI", 1.6, layer="MARCO")
        self.text(234, y0 + 10.2, "Hoja A4 · imprimir al 100 %", 1.4, layer="MARCO")
        self.text(W - 7, y0 + 10.6, f"LÁMINA {self.num:02d}/{self.total:02d}", 2.6, anchor="end", bold=True, layer="MARCO")

    def view(self, ox, oy, scale):
        return View(self, ox, oy, scale)

    # ---------------------------------------------------------- salida
    def svg_doc(self):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">'
                f'<defs>{DEFS}</defs><rect width="{W}" height="{H}" fill="#fff"/>' + "\n".join(self.svg) + "</svg>")

    def to_dxf(self, msp, dx=0.0, dy=0.0):
        from ezdxf.enums import TextEntityAlignment
        P = lambda x, y: (x + dx, H - y + dy)
        for o in self.ops:
            L = o["layer"]
            if o["t"] == "poly":
                pts = [P(*p) for p in o["pts"]]
                if o["closed"] and len(pts) >= 3:
                    try:
                        g = Polygon(pts)
                        okpoly = g.is_valid and g.area > 1e-5
                    except Exception:
                        okpoly = False
                    if okpoly and o["bg"] and o["bg"].lower() not in ("#fff", "#ffffff", "none", "white"):
                        h = msp.add_hatch(color=256, dxfattribs={"layer": L + "-RELLENO"})
                        h.set_solid_fill(color=256, rgb=rgb(o["bg"]))
                        h.paths.add_polyline_path(pts, is_closed=True)
                    if okpoly and o["hat"]:
                        pat, sc, ang = o["hat"]
                        h = msp.add_hatch(color=8, dxfattribs={"layer": L + "-RAYADO"})
                        h.set_pattern_fill(pat, color=8, scale=sc, angle=ang)
                        h.paths.add_polyline_path(pts, is_closed=True)
                if o["stroke"]:
                    at = {"layer": L, "lineweight": lw(o["sw"])}
                    if o["dash"]: at["linetype"] = "DASHED"; at["ltscale"] = 0.15
                    c = rgb(o["stroke"])
                    e = msp.add_lwpolyline(pts, close=o["closed"] and len(pts) > 2, dxfattribs=at)
                    if c != (0, 0, 0): e.rgb = c
            elif o["t"] == "circ":
                c = P(*o["c"])
                if o["fill"]:
                    h = msp.add_hatch(color=256, dxfattribs={"layer": L + "-RELLENO"})
                    h.set_solid_fill(color=256, rgb=rgb(o["fill"]))
                    h.paths.add_edge_path().add_arc(c, o["r"], 0, 360)
                if o["stroke"]:
                    at = {"layer": L, "lineweight": lw(o["sw"])}
                    if o.get("dash"): at["linetype"] = "DASHED"; at["ltscale"] = 0.15
                    e = msp.add_circle(c, o["r"], dxfattribs=at)
                    cc = rgb(o["stroke"])
                    if cc != (0, 0, 0): e.rgb = cc
            elif o["t"] == "text":
                st = "ARIAL-NEGRITA" if o["bold"] else "ARIAL"
                if o["ital"]: st = "ARIAL-CURSIVA"
                e = msp.add_text(o["s"], height=o["size"] * 0.716, rotation=o["rot"], dxfattribs={"layer": L, "style": st})
                al = {"start": TextEntityAlignment.LEFT, "middle": TextEntityAlignment.CENTER, "end": TextEntityAlignment.RIGHT}[o["anchor"]]
                e.set_placement(P(*o["p"]), align=al)
                cc = rgb(o["color"])
                if cc != (0, 0, 0): e.rgb = cc


class View:
    """dibujo a escala: mm reales (x der., y arriba) -> mm de papel"""
    def __init__(self, sh, ox, oy, scale):
        self.sh, self.ox, self.oy, self.s = sh, ox, oy, scale

    def P(self, x, y):
        return (self.ox + x / self.s, self.oy - y / self.s)

    def poly(self, pts, **k):
        self.sh.poly([self.P(x, y) for x, y in pts], **k)

    def rect(self, x0, y0, x1, y1, **k):
        self.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], **k)

    def line(self, x0, y0, x1, y1, **k):
        self.sh.line(*self.P(x0, y0), *self.P(x1, y1), **k)

    def pline(self, pts, **k):
        self.sh.pline([self.P(x, y) for x, y in pts], **k)

    def circle(self, x, y, r, **k):
        self.sh.circle(*self.P(x, y), r / self.s, **k)

    def dot(self, x, y, r=0.35, color=REB):
        self.sh.circle(*self.P(x, y), r, fill=color, stroke=None, sw=0, layer="ARMADURAS")

    def dim(self, p1, p2, off, txt=None, **k):
        if txt is None:
            d = math.hypot(p2[0] - p1[0], p2[1] - p1[1])
            txt = fmt_m(d)
        self.sh.dim(self.P(*p1), self.P(*p2), off, txt, **k)

    def text(self, x, y, s, size=2.0, **k):
        self.sh.text(*self.P(x, y), s, size, **k)

    def callout(self, target, at_paper, label, **k):
        self.sh.callout(self.P(*target), at_paper, label, **k)

    def note(self, target, at_paper, txt, **k):
        self.sh.note(self.P(*target), at_paper, txt, **k)


def fmt_m(mm):
    """cota en metros con 2 decimales (convención argentina, coma decimal)"""
    v = mm / 1000.0
    if mm < 1000 and abs(mm / 10 - round(mm / 10)) > 1e-6:
        return f"{mm / 10:.1f}".replace(".", ",")           # cm con decimal
    return f"{v:.2f}".replace(".", ",")


# ====================================================================== ISOMETRÍA con ocultamiento exacto por orden de caras
class Iso:
    """Escena de prismas (mm reales, z arriba). Proyección isométrica con escala verdadera sobre los ejes."""
    LIGHT = np.array([-0.45, -0.75, 0.95])

    def __init__(self, view_dir=(1, -1, 1)):
        D = np.array(view_dir, float); D /= np.linalg.norm(D)
        R = np.cross([0, 0, 1], D); R /= np.linalg.norm(R)
        U = np.cross(D, R)
        self.D, self.R, self.U = D, R, U
        self.k = 1 / 0.8164966  # dibujo isométrico: longitudes verdaderas en los ejes
        self.faces = []
        self.L = self.LIGHT / np.linalg.norm(self.LIGHT)
        self.labels = []

    def proj(self, p):
        p = np.asarray(p, float)
        return (p @ self.R * self.k, p @ self.U * self.k, p @ self.D * self.k)

    def face(self, pts, col, edge="#000", sw=0.16):
        P = np.array(pts, float)
        n = np.zeros(3)
        for i in range(len(P)):
            a, b = P[i], P[(i + 1) % len(P)]
            n += [(a[1] - b[1]) * (a[2] + b[2]), (a[2] - b[2]) * (a[0] + b[0]), (a[0] - b[0]) * (a[1] + b[1])]
        nn = np.linalg.norm(n)
        if nn < 1e-9: return
        n /= nn
        if n @ self.D <= 1e-6: return            # cara posterior
        self.faces.append(dict(P=P, n=n, col=col, edge=edge, sw=sw))

    def prism(self, poly2d, axis, a0, a1, col, **k):
        """poly2d en el plano perpendicular a 'axis' (coordenadas (u,v) = las otras dos en orden x,y,z), extruido de a0 a a1"""
        def P3(u, v, w):
            if axis == "x": return (w, u, v)
            if axis == "y": return (u, w, v)
            return (u, v, w)
        pts = list(poly2d)
        # orientación CCW en (u,v)
        area = sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1] for i in range(len(pts)))
        if area < 0: pts = pts[::-1]
        lo, hi = min(a0, a1), max(a0, a1)
        sgn = 1 if axis != "y" else -1          # (x,y,z): eje y invierte la terna (u=x, v=z)
        top = [P3(u, v, hi) for u, v in pts]
        bot = [P3(u, v, lo) for u, v in pts]
        if sgn > 0:
            self.face(top, col, **k); self.face(bot[::-1], col, **k)
        else:
            self.face(top[::-1], col, **k); self.face(bot, col, **k)
        n = len(pts)
        for i in range(n):
            j = (i + 1) % n
            q = [bot[i], bot[j], top[j], top[i]]
            self.face(q if sgn > 0 else q[::-1], col, **k)

    def box(self, x0, x1, y0, y1, z0, z1, col, **k):
        self.prism([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], "z", z0, z1, col, **k)

    def cyl(self, axis, cu, cv, r, a0, a1, col, n=14, **k):
        self.prism([(cu + r * math.cos(2 * math.pi * i / n), cv + r * math.sin(2 * math.pi * i / n)) for i in range(n)], axis, a0, a1, col, **k)

    def fit(self, box, scale):
        """origen de papel para centrar la escena en box = (x0, y0, x1, y1)"""
        us, vs = [], []
        for fc in self.faces:
            for p in fc["P"]:
                u, v, w = self.proj(p); us.append(u); vs.append(v)
        cx = (box[0] + box[2]) / 2 - (min(us) + max(us)) / 2 / scale
        cy = (box[1] + box[3]) / 2 + (min(vs) + max(vs)) / 2 / scale
        return cx, cy

    def label(self, p3, txt):
        self.labels.append((p3, txt))

    def draw(self, sh, ox, oy, scale, sort=True):
        """dibuja en la hoja con origen de papel (ox, oy) para el punto real (0,0,0)"""
        items = []
        for fc in self.faces:
            uvw = np.array([self.proj(p) for p in fc["P"]])
            pts2 = [(ox + u / scale, oy - v / scale) for u, v, w in uvw]
            try:
                g = Polygon(pts2)
                if not g.is_valid: g = g.buffer(0)
            except Exception:
                continue
            if g.area < 1e-4: continue
            # plano en (X_papel, Y_papel, w)
            nn = np.array([fc["n"] @ self.R, -(fc["n"] @ self.U), fc["n"] @ self.D])  # normal en coords de papel (y abajo)
            p0 = np.array([pts2[0][0], pts2[0][1], uvw[0][2] / scale])
            items.append(dict(g=g, pts=pts2, nn=nn, p0=p0, fc=fc))
        n = len(items)
        order = list(range(n))
        if sort and n:
            tree = STRtree([it["g"] for it in items])
            succ = [set() for _ in range(n)]; indeg = [0] * n

            def depth(it, x, y):
                a, b, c = it["nn"]
                if abs(c) < 1e-9: return it["p0"][2]
                return it["p0"][2] - (a * (x - it["p0"][0]) + b * (y - it["p0"][1])) / c
            for i in range(n):
                for j in tree.query(items[i]["g"]):
                    j = int(j)
                    if j <= i: continue
                    try:
                        inter = items[i]["g"].intersection(items[j]["g"])
                    except Exception:
                        continue
                    if inter.area < 2e-4: continue
                    p = inter.representative_point()
                    di, dj = depth(items[i], p.x, p.y), depth(items[j], p.x, p.y)
                    if abs(di - dj) < 1e-6: continue
                    a, b = (i, j) if di < dj else (j, i)      # a detrás de b
                    if b not in succ[a]:
                        succ[a].add(b); indeg[b] += 1
            avg = [float(np.mean([self.proj(p)[2] for p in it["fc"]["P"]])) for it in items]
            import heapq
            ready = [(avg[i], i) for i in range(n) if indeg[i] == 0]; heapq.heapify(ready)
            done = [False] * n; order = []
            while len(order) < n:
                if not ready:
                    rest = [i for i in range(n) if not done[i]]
                    i = min(rest, key=lambda q: (indeg[q], avg[q])); indeg[i] = 0
                    heapq.heappush(ready, (avg[i], i))
                _, i = heapq.heappop(ready)
                if done[i]: continue
                done[i] = True; order.append(i)
                for j in succ[i]:
                    indeg[j] -= 1
                    if indeg[j] == 0 and not done[j]: heapq.heappush(ready, (avg[j], j))
        for i in order:
            it = items[i]; fc = it["fc"]
            k = 0.62 + 0.38 * max(0.0, float(fc["n"] @ self.L))
            col = fc["col"]
            if isinstance(col, str) and col.startswith("#"):
                sh.poly(it["pts"], fill=shade(col, k), stroke=fc["edge"], sw=fc["sw"], layer="ISO")
            else:
                sh.poly(it["pts"], mat=col, stroke=fc["edge"], sw=fc["sw"], layer="ISO")
        return [(self.P2(p3, ox, oy, scale), t) for p3, t in self.labels]

    def P2(self, p3, ox, oy, scale):
        u, v, w = self.proj(p3)
        return (ox + u / scale, oy - v / scale)


# ====================================================================== bloques de texto técnicos
def spec(sh, x, y, w, title, kv, size=1.75, lead=1.3, tsize=2.2):
    """bloque de especificación: título + pares (clave, texto); devuelve y final"""
    if title:
        sh.text(x, y, title, tsize, bold=True)
        sh.line(x, y + 0.8, x + w, y + 0.8, sw=0.2)
        y += tsize * 1.25 + 0.8
    for k, v in kv:
        kw = (len(k) + 1) * size * 0.58
        first = wrap(v, w - kw, size)[0] if v else ""
        rest = v[len(first):].strip() if v else ""
        sh.text(x, y, k, size, bold=True)
        sh.text(x + kw, y, first, size)
        y += size * lead
        for ln in (wrap(rest, w, size) if rest else []):
            sh.text(x, y, ln, size); y += size * lead
        y += 0.35
    return y


def heading(sh, txt, sub=None):
    sh.text(10, 13.5, txt, 3.4, bold=True)
    if sub: sh.text(10, 18.0, sub, 1.9, color="#333")


def breakline(sh, p1, p2, sw=0.15):
    """línea de interrupción con zeta al medio (papel)"""
    (x1, y1), (x2, y2) = p1, p2
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    L = math.hypot(x2 - x1, y2 - y1); ux, uy = (x2 - x1) / L, (y2 - y1) / L; nx, ny = -uy, ux
    sh.pline([(x1, y1), (mx - ux * 1.0, my - uy * 1.0), (mx - ux * 0.4 + nx * 1.6, my - uy * 0.4 + ny * 1.6),
              (mx + ux * 0.4 - nx * 1.6, my + uy * 0.4 - ny * 1.6), (mx + ux * 1.0, my + uy * 1.0), (x2, y2)], sw=sw)


def ground(sh, x0, x1, y, sw=0.25):
    """línea de terreno natural con achurado corto (papel)"""
    sh.line(x0, y, x1, y, sw=sw)
    x = x0 + 0.8
    while x < x1:
        sh.line(x, y, x - 1.2, y + 1.2, sw=0.1); x += 1.6
