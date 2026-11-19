"""Genera el esquema unifilar de tableros (SVG dentro de HTML, A4 apaisado)."""
import sys

W, H = 1400, 990
INK = "#1d2430"
GREY = "#5b6470"
DASH = "#8b929b"
RED = "#d23a3a"
PINK = "#fbe1e3"
PE = "#c07a1e"

out = []
def a(s): out.append(s)

def line(x1, y1, x2, y2, c=INK, w=2, extra=""):
    a(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}" {extra}/>')

def text(x, y, s, size=12, c=GREY, weight=400, anchor="start"):
    a(f'<text x="{x}" y="{y}" font-size="{size}" fill="{c}" font-weight="{weight}" text-anchor="{anchor}">{s}</text>')

def label(x, y, title, subs=(), anchor="start", tsize=13.5):
    text(x, y, title, tsize, INK, 600, anchor)
    for i, s in enumerate(subs):
        text(x, y + 17 + i * 15, s, 11.5, GREY, 400, anchor)

def ticks_v(x, y, n, c=INK):
    """n trazos oblicuos sobre un conductor vertical (cantidad de conductores)."""
    gap = 5
    y0 = y - (n - 1) * gap / 2
    for i in range(n):
        yy = y0 + i * gap
        line(x - 7, yy + 4, x + 7, yy - 4, c, 1.6)

def ticks_h(x, y, n, c=INK):
    gap = 5
    x0 = x - (n - 1) * gap / 2
    for i in range(n):
        xx = x0 + i * gap
        line(xx - 4, y + 7, xx + 4, y - 7, c, 1.6)

def breaker(cx, cy, s=24):
    """Interruptor termomagnético: cuadrado con X."""
    x, y = cx - s / 2, cy - s / 2
    a(f'<rect x="{x}" y="{y}" width="{s}" height="{s}" fill="#fff" stroke="{INK}" stroke-width="2"/>')
    line(x + 4, y + 4, x + s - 4, y + s - 4, INK, 1.6)
    line(x + s - 4, y + 4, x + 4, y + s - 4, INK, 1.6)

def fuse(cx, y, w=28, h=40):
    x = cx - w / 2
    a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#fff" stroke="{INK}" stroke-width="2"/>')
    a(f'<rect x="{cx-4}" y="{y+9}" width="8" height="{h-18}" fill="none" stroke="{INK}" stroke-width="1.5"/>')
    line(cx, y + 6, cx, y + h - 6, INK, 1.2)

def meter(cx, y, w=44, h=52):
    x = cx - w / 2
    a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{PINK}" stroke="{RED}" stroke-width="2"/>')
    line(x, y + 12, x + w, y + 12, RED, 1.6)

def board(cx, y, w, h, cross=False):
    """Tablero: rectángulo con diagonal (TS) o con X (TP)."""
    x = cx - w / 2
    a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#fff" stroke="{INK}" stroke-width="2"/>')
    line(x + 6, y + h - 5, x + w - 6, y + 5, INK, 1.6)
    if cross:
        line(x + 6, y + 5, x + w - 6, y + h - 5, INK, 1.6)

def dashed(x, y, w, h, title=None, sub=None, bottom=False):
    a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="{DASH}" stroke-width="1.5" stroke-dasharray="7 5" rx="2"/>')
    ty = y + h - 32 if bottom else y + 24
    if title:
        text(x + 14, ty, title, 15, INK, 700)
    if sub:
        text(x + 14, ty + 16, sub, 11.5, GREY)

def ground(x, y):
    line(x, y, x, y + 10, PE, 2)
    for i, half in enumerate((14, 9, 4)):
        line(x - half, y + 10 + i * 5, x + half, y + 10 + i * 5, PE, 2)

# ------------------------------------------------------------------ layout
NX = 600                      # acometida
XA, XB, XC = 170, 450, 1000   # ramas: viviendas, dúplex, servicios generales
BUS_Y = 228

a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
  f'font-family="Inter, Helvetica, Arial, sans-serif">')
a(f'<rect width="{W}" height="{H}" fill="#fff"/>')

# Red y acometida
line(NX, 26, NX, 100)
ticks_v(NX, 64, 4)
label(NX + 16, 44, "Red de distribución de BT · 3 × 380/220 V")
text(NX + 16, 70, "acometida · 3F + N", 11.5)
fuse(NX, 100, 30, 46)
label(NX + 24, 118, "Caja general de toma", ["con fusibles (de la distribuidora)"])
line(NX, 146, NX, BUS_Y)

# Sala de medidores
dashed(110, 172, 1110, 222, "SALA DE MEDIDORES", "medición individual por unidad + servicios generales")
a(f'<line x1="{XA}" y1="{BUS_Y}" x2="{XC}" y2="{BUS_Y}" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>')
a(f'<circle cx="{NX}" cy="{BUS_Y}" r="4.5" fill="{INK}"/>')
text(XC + 14, BUS_Y + 4, "barra de distribución a medidores", 11.5)

for x in (XA, XB, XC):
    line(x, BUS_Y, x, 300)
    fuse(x, 240, 24, 34)
    meter(x, 300)
    line(x, 352, x, 450 if x != XC else 430)
text(XA + 18, 262, "fusibles", 11.5)
text(XB + 18, 262, "fusibles", 11.5)
text(XC + 18, 262, "fusible tripolar NH", 11.5)

label(XA + 34, 318, "Medidor monofásico ×18", ["viviendas · 6 por fase R · S · T"])
label(XB + 34, 318, "Medidor monofásico ×3", ["viviendas dúplex · 1 por fase"])
label(XC + 34, 318, "Medidor trifásico", ["servicios generales"])

ticks_v(XA, 412, 2); text(XA + 14, 416, "F + N", 11.5)
ticks_v(XB, 412, 2); text(XB + 14, 416, "F + N", 11.5)

# Jabalina y PE
JX, JY = 74, 300
line(110, 270, JX, 270, PE, 2)
a(f'<circle cx="{JX}" cy="270" r="3.5" fill="{PE}"/>')
line(JX, 270, JX, 840, PE, 2)
line(JX, 270, 40, 270, PE, 2)
line(40, 270, 40, 286, PE, 2)
ground(40, 286)
text(22, 236, "jabalina", 12, PE, 600)
text(22, 251, "PE", 12, PE, 600)

# ---- Rama A: viviendas ×18
dashed(110, 436, 270, 300, "VIVIENDA TIPO", "una por unidad · ×18", bottom=True)
line(XA, 450, XA, 584)
board(XA, 470, 80, 34, cross=True)
label(XA + 52, 482, "TP-V · ×18", ["tablero principal", "de vivienda"], tsize=12.5)
ticks_v(XA, 544, 2)
board(XA, 584, 80, 34)
label(XA + 52, 596, "TS-V · ×18", ["tablero seccional", "de vivienda"], tsize=12.5)

# ---- Rama B: dúplex ×3
dashed(395, 436, 255, 300, "VIVIENDA DÚPLEX", "una por unidad · ×3", bottom=True)
line(XB, 450, XB, 624)
board(XB, 470, 80, 34, cross=True)
label(XB + 52, 482, "TP-D · ×3", ["tablero principal", "dúplex"], tsize=12.5)
ticks_v(XB, 528, 2)
board(XB, 552, 80, 34)
label(XB + 52, 564, "TS-D · ×3", ["tablero seccional", "dúplex"], tsize=12.5)
ticks_v(XB, 610, 2)
board(XB, 634, 80, 34)
label(XB + 52, 646, "TSS-D · ×3", ["tablero subseccional", "dúplex"], tsize=12.5)
line(XB, 586, XB, 634)

# ---- Rama C: TP servicios generales
ticks_v(XC, 384, 4); text(XC + 14, 388, "3F + N + PE", 11.5)
dashed(670, 436, 705, 172, "TP-SG · TABLERO PRINCIPAL", "servicios generales")
breaker(XC, 470)
text(XC + 20, 474, "TM general tetrapolar + ID", 12)
line(XC, 482, XC, 516)
OUT = [
    ("TS-1", ["Subsuelo"], "bipolar", "fase R", 2),
    ("TS-2", ["Planta baja"], "bipolar", "fase S", 2),
    ("TS-3", ["SUM"], "bipolar", "fase T", 2),
    ("TS-4", ["Bomba", "cloacal"], "tetrapolar", "R · S · T", 4),
    ("TS-5", ["Bombeo", "de agua"], "tetrapolar", "R · S · T", 4),
    ("TS-6", ["Ascensores"], "tetrapolar", "R · S · T", 4),
    ("TS-7", ["Caldera"], "bipolar", "fase R", 2),
    ("TS-8", ["Termotanque"], "bipolar", "fase S", 2),
]
x0, dx = 716, 88
xs = [x0 + i * dx for i in range(len(OUT))]
a(f'<line x1="{xs[0]}" y1="516" x2="{xs[-1]}" y2="516" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>')
for x, (name, desc, pol, ph, n) in zip(xs, OUT):
    line(x, 516, x, 660)
    breaker(x, 540)
    text(x + 4, 572, pol, 11, GREY)
    text(x + 4, 586, ph, 11, RED, 500)
    ticks_v(x, 630, n)
    board(x, 660, 70, 38)
    text(x, 718, name, 13.5, INK, 600, "middle")
    for j, d in enumerate(desc):
        text(x, 734 + j * 14, d, 11.5, GREY, 400, "middle")

# PE a cada grupo
PEY = 840
line(JX, PEY, 1388, PEY, PE, 2)
for x in (245, 522):
    line(x, PEY, x, 736, PE, 2)
line(1388, PEY, 1388, 520, PE, 2)
line(1388, 520, 1375, 520, PE, 2)
text(700, PEY - 8, "PE · puesta a tierra (jabalina)", 12.5, PE, 600, "middle")

# ---- Referencias
LY = 890
text(110, LY - 16, "REFERENCIAS", 12, INK, 700)
items = []
cx = 120
fuse(cx + 6, LY - 2, 18, 26); text(cx + 26, LY + 15, "fusible", 11.5)
breaker(cx + 106, LY + 11, 20); text(cx + 124, LY + 15, "interruptor termomagnético", 11.5)
meter(cx + 300, LY - 2, 22, 26); text(cx + 320, LY + 15, "medidor", 11.5)
board(cx + 410, LY, 44, 22, cross=True); text(cx + 440, LY + 15, "tablero principal", 11.5)
board(cx + 570, LY, 44, 22); text(cx + 600, LY + 15, "tablero seccional / subseccional", 11.5)
line(cx + 820, LY - 2, cx + 820, LY + 26); ticks_v(cx + 820, LY + 11, 2)
text(cx + 834, LY + 15, "n.º de conductores activos (2 = F + N · 4 = 3F + N)", 11.5)
text(110, LY + 56, "TP: tablero principal · TS: tablero seccional · TSS: tablero subseccional · ID: interruptor diferencial · PE: conductor de protección", 11.5)

a('</svg>')
svg = "\n".join(out)

html = f"""<!doctype html><html><head><meta charset="utf-8"><title>Esquema unifilar</title>
<style>@page {{ size: A4 landscape; margin: 0; }}
html,body {{ margin:0; padding:0; background:#fff; }}
.page {{ width:297mm; height:210mm; display:flex; align-items:center; justify-content:center; }}
.page svg {{ width:287mm; height:auto; }}</style></head>
<body><div class="page">{svg}</div></body></html>"""
open(sys.argv[1], "w").write(html)
