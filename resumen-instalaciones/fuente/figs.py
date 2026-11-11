# Helpers SVG + todas las figuras redibujadas de los apuntes
K = "#2b2b3a"; R = "#e0453a"; B = "#2f6fde"; O = "#f08a24"; P = "#6b4fd8"; G = "#1f9d6b"; LB = "#56a8e8"

def svg(w, h, body, maxw=None):
    style = f' style="max-width:{w*1.2:.0f}px"'
    return f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg"{style}>{body}</svg>'

def t(x, y, s, c=K, a="start", size=11, w=400, it=False):
    st = ' font-style="italic"' if it else ""
    return f'<text x="{x}" y="{y}" fill="{c}" text-anchor="{a}" font-size="{size}" font-weight="{w}"{st}>{s}</text>'

def tl(x, y, lines, c=K, a="start", size=11, lh=13, w=400):
    return "".join(t(x, y + i * lh, s, c, a, size, w) for i, s in enumerate(lines))

def ln(x1, y1, x2, y2, c=K, w=1.6, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"{d} stroke-linecap="round"/>'

MK = {K: "aK", R: "aR", B: "aB", O: "aO", P: "aP", G: "aG", LB: "aL"}

def ar(x1, y1, x2, y2, c=K, w=1.6, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"{d} marker-end="url(#{MK[c]})" stroke-linecap="round"/>'

def pa(d, c=K, w=1.6, fill="none", dash=None, arrow=False, extra=""):
    da = f' stroke-dasharray="{dash}"' if dash else ""
    m = f' marker-end="url(#{MK[c]})"' if arrow else ""
    return f'<path d="{d}" stroke="{c}" stroke-width="{w}" fill="{fill}"{da}{m} stroke-linejoin="round" stroke-linecap="round"{extra}/>'

def rc(x, y, w, h, c=K, sw=1.6, fill="none", rx=0, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" stroke="{c}" stroke-width="{sw}" fill="{fill}"{d}/>'

def ci(x, y, r, c=K, sw=1.6, fill="none"):
    return f'<circle cx="{x}" cy="{y}" r="{r}" stroke="{c}" stroke-width="{sw}" fill="{fill}"/>'

def coil_v(x, y, h, n=6, amp=6, c=K, w=1.6):
    d = f"M{x},{y}"; step = h / n
    for i in range(n):
        yy = y + step * (i + 0.5); xx = x + (amp if i % 2 == 0 else -amp)
        d += f" Q{xx},{yy} {x},{y + step * (i + 1)}"
    return pa(d, c, w)

def coil_h(x, y, wdt, n=6, amp=6, c=K, w=1.6):
    d = f"M{x},{y}"; step = wdt / n
    for i in range(n):
        xx = x + step * (i + 0.5); yy = y - amp
        d += f" Q{xx},{yy - 4} {x + step * (i + 1)},{y}"
    return pa(d, c, w)

def zig_v(x, y, h, n=5, amp=7, c=K, w=1.6):
    pts = [f"{x},{y}"]
    for i in range(1, n * 2):
        pts.append(f"{x + (amp if i % 2 else -amp)},{y + h * i / (n * 2)}")
    pts.append(f"{x},{y + h}")
    return pa("M" + " L".join(pts), c, w)

def gnd(x, y, c=K):
    return ln(x, y, x, y + 8, c) + ln(x - 9, y + 8, x + 9, y + 8, c) + ln(x - 6, y + 12, x + 6, y + 12, c) + ln(x - 3, y + 16, x + 3, y + 16, c)

def valve(x, y, c=K, vertical=False, s=7):
    if vertical:
        return pa(f"M{x-s},{y-s} L{x+s},{y-s} L{x-s},{y+s} L{x+s},{y+s} Z", c, 1.6, "#fff")
    return pa(f"M{x-s},{y-s} L{x-s},{y+s} L{x+s},{y-s} L{x+s},{y+s} Z", c, 1.6, "#fff")

def xcirc(x, y, r=8, c=K):
    k = r * 0.7
    return ci(x, y, r, c, 1.6, "#fff") + ln(x - k, y - k, x + k, y + k, c, 1.4) + ln(x - k, y + k, x + k, y - k, c, 1.4)

def pump(x, y, r=12, c=K):
    return ci(x, y, r, c, 1.6, "#fff") + pa(f"M{x-r*0.55},{y-r*0.75} L{x+r},{y} L{x-r*0.55},{y+r*0.75} Z", c, 1, c)

def comp(x, y, r=10, c=K):
    return ci(x, y, r, c, 1.6, "#fff") + t(x, y + 4, "C", c, "middle", 11, 700)

def fan(x, y, r=9, c=K):
    return (f'<ellipse cx="{x-r/2}" cy="{y}" rx="{r/2}" ry="{r/4}" stroke="{c}" stroke-width="1.3" fill="none"/>'
            f'<ellipse cx="{x+r/2}" cy="{y}" rx="{r/2}" ry="{r/4}" stroke="{c}" stroke-width="1.3" fill="none"/>')

def bolt(x, y, s=1, c=O):
    d = f"M{x},{y} l{8*s},{10*s} l{-5*s},{1*s} l{9*s},{12*s} l{-14*s},{-10*s} l{5*s},{-1*s} l{-8*s},{-9*s} Z"
    return pa(d, c, 1.2, c)

def board(x, y, w=26, h=12, c=K):
    return rc(x, y, w, h, c, 1.5, "#fff") + ln(x, y, x + w, y + h, c, 1.2) + ln(x, y + h, x + w, y, c, 1.2)

def sboard(x, y, w=22, h=10, c=K):
    return rc(x, y, w, h, c, 1.5, "#fff") + ln(x + 3, y + h - 2, x + w - 3, y + 2, c, 1.2)

def radiator(x, y, w=22, h=14, c=R):
    s = rc(x, y, w, h, c, 1.4, "#fff")
    for i in range(1, 5):
        s += ln(x + i * w / 5, y + 2, x + i * w / 5, y + h - 2, c, 1.1)
    return s

def hatch(x, y, w, h, c=R, gap=8, idn="h"):
    s = f'<clipPath id="{idn}"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath><g clip-path="url(#{idn})">'
    for i in range(-int(h), int(w) + int(h), gap):
        s += ln(x + i, y + h, x + i + h, y, c, 1)
    return s + "</g>" + rc(x, y, w, h, c, 1.4)

DEFS = ('<svg width="0" height="0" style="position:absolute"><defs>' +
        "".join(f'<marker id="{v}" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
                f'<path d="M0,1 L9,5 L0,9 Z" fill="{k}"/></marker>' for k, v in MK.items()) +
        '</defs></svg>')

# ---------------------------------------------------------------- FIGURAS
F = {}

# 1 Casa verano / invierno
b = ""
# sol
b += ci(70, 52, 11, O, 1.8) + "".join(ln(70 + 17 * c, 52 + 17 * s, 70 + 23 * c, 52 + 23 * s, O, 1.6) for c, s in [(1,0),(-1,0),(0,1),(0,-1),(.7,.7),(-.7,.7),(.7,-.7),(-.7,-.7)])
b += t(70, 100, "Verano 36° ext.", K, "middle", 12, 600)
b += ar(40, 150, 182, 150, R, 2) + tl(20, 172, ["El calor entra", "a la vivienda."], R)
# casa
b += pa("M190,105 L260,45 L330,105", K, 2) + ln(190, 105, 190, 215, K, 2) + ln(330, 105, 330, 215, K, 2) + ln(180, 215, 345, 215, K, 2)
b += ci(198, 112, 11, B, 1.8, "#eaf2ff") + t(198, 116, "AA", B, "middle", 9, 700)
b += ar(198, 99, 198, 30, K, 1.6) + t(205, 28, "A.A. – saca calor", K, "start", 11, 600)
# persona
b += ci(260, 158, 6, K, 1.5) + ln(260, 164, 260, 186, K, 1.5) + ln(250, 172, 270, 172, K, 1.5) + ln(260, 186, 252, 200, K, 1.5) + ln(260, 186, 268, 200, K, 1.5)
b += ar(260, 220, 260, 240, B, 1.6) + t(260, 256, "Confort = 22° a 24° – 50 HR", K, "middle", 12, 700)
# calefactor
b += rc(312, 190, 22, 18, R, 1.6, "#ffece9") + t(323, 203, "≋", R, "middle", 12, 700)
b += ar(336, 199, 372, 199, K) + t(376, 203, "Pongo algo que aporta calor", K)
# invierno
for a in range(0, 180, 30):
    import math
    c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
    b += ln(470 - 12 * c, 48 - 12 * s, 470 + 12 * c, 48 + 12 * s, B, 1.6)
b += t(470, 86, "Invierno 0° ext.", K, "middle", 12, 600)
b += pa("M300,140 Q345,120 425,128", B, 2, arrow=True) + t(372, 150, "La vivienda pierde calor", B)
F[1] = svg(560, 266, b, 560)

# 2 Ciclo de compresión
b = ""
L, Rr, T, Bt = 150, 400, 45, 215
b += ar(L, 130, L, T + 2, R) + ln(L, T, 250, T, R, 1.8) + rc(250, T - 12, 70, 24, K, 1.6, "#fff") + t(285, T + 4, "Compresor", K, "middle", 11, 600)
b += ci(285, T - 26, 9, P, 1.4) + t(285, T - 22, "2", P, "middle", 11, 700)
b += ar(320, T, Rr - 2, T, R) + ln(Rr, T, Rr, 100, R, 1.8) + ar(Rr, T, Rr, 100, R)
b += rc(Rr - 18, 100, 36, 54, K, 1.2, "none", 0, "4 3") + zig_v(Rr, 100, 54, 4, 8, K)
b += ar(Rr, 154, Rr, Bt - 2, B) + ar(Rr, Bt, 236, Bt, B)
b += xcirc(225, Bt) + ar(214, Bt, L + 2, Bt, B) + ar(L, Bt, L, 160, B)
b += rc(L - 18, 102, 36, 54, K, 1.2, "none", 0, "4 3") + zig_v(L, 102, 54, 4, 8, K)
b += ln(L, 156, L, 160, B)
b += tl(60, 40, ["Gas a", "baja presión."], B) + t(330, 30, "Gas a alta presión y temp.", B, "start", 11)
b += ci(40, 128, 9, P, 1.4) + t(40, 132, "1", P, "middle", 11, 700) + t(54, 132, "Evaporador", K, "start", 11, 600)
b += t(426, 132, "Condensador", K, "start", 11, 600) + ci(514, 128, 9, P, 1.4) + t(514, 132, "3", P, "middle", 11, 700)
b += tl(40, 178, ["Líquido a baja pres.", "y temp."], B) + tl(414, 178, ["Líquido a alta", "presión y temp."], B)
b += t(214, 242, "Válvula de expansión", K, "middle", 11, 600) + ci(290, 238, 9, P, 1.4) + t(290, 242, "4", P, "middle", 11, 700)
F[2] = svg(540, 252, b, 540)

# 3 Equipo de ventana
b = rc(160, 30, 230, 150, K, 2, "#fff") + ln(300, 30, 300, 180, K, 1.6)
b += pa("M175,45 L285,45 Q300,45 300,60", R, 1.4) + pa("M300,60 Q300,45 330,45 L370,45 L370,165 L190,165 L175,165 L175,45", R, 1.4)
b += coil_v(180, 55, 100, 7, 7, K) + f'<ellipse cx="215" cy="105" rx="7" ry="38" stroke="{K}" stroke-width="1.5" fill="none"/>'
b += rc(240, 95, 22, 18, K, 1.5, "#fff") + ln(262, 104, 318, 104, R, 1.3)
b += rc(318, 88, 18, 34, K, 1.4, "#fff") + t(327, 110, "8", K, "middle", 13)
b += coil_v(355, 55, 100, 7, 7, K) + rc(376, 50, 6, 110, K, 1.4, "#fff")
b += comp(270, 165)
b += ar(250, 95, 262, 22, B) + t(266, 18, "MOTOR", P, "start", 11, 700)
b += ar(330, 88, 380, 18, LB) + t(384, 18, "Ventilador", LB)
b += ar(395, 45, 440, 45, P) + t(444, 49, "aire 15°", P, "start", 12, 600)
b += ar(385, 62, 420, 66, LB) + t(424, 70, "Filtro", LB)
b += ar(368, 120, 440, 120, P) + t(444, 124, "Evaporador", P)
b += ar(470, 150, 405, 150, R) + t(444, 170, "aire 45°", R, "start", 12, 600)
b += ar(150, 72, 120, 72, R) + t(80, 62, "aire 45°", R, "start", 12, 600)
b += ar(170, 100, 120, 100, R) + t(40, 104, "Condensador", R)
b += ar(212, 130, 140, 200, LB) + t(100, 214, "Ventilador", LB)
b += ar(270, 176, 270, 200, P) + t(270, 214, "Compresor", P, "middle")
F[3] = svg(540, 222, b, 520)

# 4 Roof top
b = ""
b += pa("M150,80 L330,80 L330,170 L150,170 Z", K, 1.8, "#fff") + pa("M150,80 L190,48 L370,48 L330,80", K, 1.8, "#fff") + pa("M330,170 L370,138 L370,48", K, 1.8)
b += coil_h(185, 98, 60, 5, 5, K) + coil_h(190, 150, 50, 5, 5, K) + fan(272, 70) + fan(220, 125)
b += comp(300, 120, 9) + valve(162, 120, K, True, 5) + ln(162, 98, 162, 145, K, 1.2) + rc(255, 112, 16, 12, K, 1.3, "#fff")
b += ar(210, 98, 230, 15, B) + t(234, 15, "Condensador", B)
b += ar(285, 70, 360, 30, B) + t(364, 30, "Ventilador (calor al ext.)", B)
b += ar(268, 116, 400, 70, B) + t(404, 72, "Motor", B)
b += ar(305, 120, 400, 92, B) + t(404, 96, "Compresor", B)
b += ar(500, 82, 375, 82, R) + tl(504, 80, ["ingreso de", "aire ext."], R)
b += ar(240, 152, 400, 132, B) + t(404, 136, "Evaporador", B)
b += ar(220, 132, 210, 215, B) + t(200, 228, "Ventilador", B)
b += ar(158, 120, 85, 112, B) + tl(40, 98, ["Válv.", "exp."], B)
b += tl(95, 52, ["Líq. alta", "P. y T°"], K, "start", 10) + t(95, 145, "baja P y T", K, "start", 10)
b += rc(60, 160, 34, 16, K, 1.4, "#fff") + t(77, 172, "art.", K, "middle", 10)
b += ln(160, 170, 160, 195, R, 1.6, "4 3") + pa("M160,195 L100,195 L100,176", R, 1.6, dash="4 3") + t(108, 188, "mando", R, "start", 11, 600)
b += pa("M300,170 L300,195 L180,195", R, 1.6, dash="4 3") + t(306, 194, "retorno", R, "start", 11, 600)
F[4] = svg(580, 236, b, 540)

# 5 VRV
b = ""
b += pa("M120,150 L120,120 L170,120 L170,45 L240,45", K, 1.6) + coil_h(240, 45, 80, 6, 6, K) + pa("M320,45 L370,45 L370,108", K, 1.6)
b += comp(370, 118) + pa("M370,128 L370,190 L170,190", K, 1.6)
b += rc(95, 175, 72, 26, K, 1.6, "#fff") + coil_h(105, 193, 52, 4, 5, K) + fan(130, 181)
b += pa("M120,150 L120,175", K, 1.6) + valve(170, 80, K, True)
b += fan(258, 28) + ar(270, 20, 300, 12, B) + t(304, 14, "Ventilador", B)
b += ar(325, 38, 360, 26, B) + t(364, 28, "Condensador", B)
b += ar(382, 118, 410, 118, B) + t(414, 122, "Compresor", B)
b += ar(160, 80, 120, 80, B) + tl(78, 60, ["Válv.", "exp."], B)
b += ar(110, 172, 60, 158, B) + t(20, 154, "Ventilador", B)
b += ar(110, 202, 100, 225, B) + t(100, 238, "Evaporador", B, "middle")
F[5] = svg(500, 246, b, 470)

# 6 Mixto fancoil + MEL
b = ""
b += rc(40, 85, 90, 42, K, 1.6, "#fff") + ln(40, 100, 130, 100, K, 1.2) + ln(40, 112, 130, 112, K, 1.2)
b += ci(80, 106, 9, K, 1.4) + "".join(ln(80, 106, 80 + 9 * math.cos(math.radians(a)), 106 + 9 * math.sin(math.radians(a)), K, 1) for a in range(0, 360, 45))
b += rc(130, 82, 30, 48, K, 1.6, "#fff") + coil_v(145, 87, 38, 5, 7, K)
b += pa("M160,95 Q195,95 195,125", K, 1.4) + pa("M160,105 Q185,105 185,125", K, 1.4)
b += pa("M160,88 L178,88 L178,62 L215,62 L215,190 L360,190", P, 2, arrow=True)
b += pa("M160,125 L172,125 L172,220 L420,220 L420,176", R, 2)
b += t(185, 56, "ingresa", P, "start", 11, 700) + t(240, 236, "vuelve", R, "start", 11, 700)
b += pa("M330,180 L330,80 L370,80", K, 1.6) + coil_h(370, 80, 60, 5, 5, K) + pa("M430,80 L460,80 L460,140", K, 1.6) + comp(460, 150)
b += pa("M460,160 L460,182 L432,182", K, 1.6) + rc(360, 168, 72, 24, K, 1.6, "#fff") + coil_h(368, 184, 56, 5, 5, K) + ln(330, 180, 360, 180, K, 1.6)
b += valve(330, 125, K, True)
b += ar(145, 82, 155, 30, B) + t(140, 24, "Serpentina", B)
b += ar(60, 40, 75, 75, P) + t(30, 34, "Fancoil", P, "start", 12, 700)
b += ar(80, 116, 70, 160, B) + t(40, 172, "Ventilador", B)
b += fan(386, 62) + ar(398, 56, 430, 38, B) + t(434, 40, "Ventilador", B)
b += ar(420, 72, 450, 60, B) + t(454, 62, "Condensador", B)
b += ar(472, 150, 494, 150, B) + t(498, 154, "Compresor", B)
b += ar(320, 125, 296, 120, B) + tl(262, 104, ["Válv.", "exp."], B)
b += ar(432, 195, 452, 206, B) + t(456, 212, "Evaporador", B)
F[6] = svg(570, 244, b, 540)

# 7 Edificio: BR, torre, UTA/fancoil, MEL, caldera
b = t(20, 18, "La bomba recirculatoria va en el retorno", P, "start", 13, 700)
b += rc(110, 90, 270, 160, K, 1.8, "#fff")
for y in (130, 170, 210):
    b += ln(110, y, 380, y, K, 1.2)
for y in (100, 140, 180, 220):
    b += rc(122, y, 12, 16, K, 1.2, "#fff") + rc(356, y, 12, 16, K, 1.2, "#fff")
b += ln(40, 270, 470, 270, K, 1.6)
b += rc(110, 250, 270, 20, K, 1.6, "#f6f4ff")
b += rc(140, 253, 24, 14, K, 1.2, "#fff") + t(152, 264, "≋", K, "middle", 10) + ci(198, 260, 9, P, 1.4, "#fff") + t(198, 264, "BR", P, "middle", 8, 700)
b += rc(246, 253, 18, 14, K, 1.2, "#fff") + ci(300, 260, 9, R, 1.4, "#fff") + t(300, 264, "VE", R, "middle", 8, 700) + rc(330, 253, 26, 14, K, 1.2, "#fff")
b += pa("M90,260 L90,60 L170,60", R, 1.8) + pa("M100,250 L100,72 L140,72", R, 1.4, dash="5 3")
b += rc(170, 45, 26, 26, K, 1.4, "#fff") + ln(170, 71, 196, 45, K, 1.2) + pump(140, 72, 8) + ci(140, 50, 10, K, 1.3, "#fff") + t(140, 54, "BR", K, "middle", 8, 700)
b += ln(390, 100, 390, 255, K, 1.4, "5 3") + xcirc(400, 262, 7) + t(412, 266, "BR", K, "start", 10, 700)
b += ln(130, 104, 380, 104, B, 1.2, "4 3") + ln(130, 144, 380, 144, B, 1.2, "4 3") + ln(130, 184, 380, 184, B, 1.2, "4 3")
b += ar(210, 60, 197, 56, LB) + t(214, 60, "Torre de enfriamiento", LB)
b += pa("M330,82 Q300,70 290,96", B, 1.4, arrow=False) + rc(300, 66, 56, 26, P, 1.3, "#fff", 12) + tl(328, 77, ["UTA", "Fancoil"], P, "middle", 9, 10, 700)
b += ar(290, 96, 140, 120, LB)
b += ar(152, 270, 150, 296, B) + t(150, 308, "MEL", B, "middle", 11, 700)
b += ar(198, 270, 196, 318, P) + t(196, 330, "V.Ex", P, "middle", 11, 700)
b += ar(300, 270, 292, 296, P) + t(292, 308, "V.E", P, "middle", 11, 700)
b += ar(343, 268, 360, 292, B) + t(364, 300, "Caldera", B, "start", 11, 700)
F[7] = svg(500, 336, b, 470)

# 8 Fancoil + MEL enfriada por agua + torre
b = ""
b += rc(30, 120, 80, 40, K, 1.6, "#fff") + ln(30, 134, 110, 134, K, 1.1) + ln(30, 146, 110, 146, K, 1.1) + ci(66, 140, 8, K, 1.3)
b += rc(110, 116, 28, 48, K, 1.6, "#fff") + coil_v(124, 121, 38, 5, 7, K)
b += pa("M138,124 L170,124 L170,92 L210,92 L210,210 L290,210", P, 2, arrow=True) + t(150, 86, "ingresa", P, "start", 11, 700)
b += pa("M138,158 L150,158 L150,236 L330,236 L330,214", R, 2) + t(210, 252, "vuelve", R, "start", 11, 700)
b += rc(290, 198, 62, 24, K, 1.6, "#fff") + coil_h(298, 214, 46, 4, 5, K)
b += rc(290, 120, 62, 24, K, 1.6, "#fff") + coil_h(298, 136, 46, 4, 5, K)
b += pa("M290,132 L262,132 L262,210 L290,210", K, 1.6) + valve(262, 170, K, True)
b += pa("M352,132 L380,132 L380,160", K, 1.6) + comp(380, 170) + pa("M380,180 L380,210 L352,210", K, 1.6)
b += rc(280, 40, 80, 32, K, 1.6, "#fff")
b += pa("M300,120 L300,72", P, 2) + t(258, 30, "ingresa", P, "start", 11, 700) + pa("M268,30 L268,56 L280,56", P, 1.4)
b += pa("M340,120 L340,72", R, 2) + t(346, 100, "vuelve", R, "start", 11, 700)
b += ar(362, 56, 392, 56, LB) + t(396, 60, "Torre de enfriamiento", LB)
b += ar(352, 126, 392, 126, LB) + t(396, 130, "Condensador", LB)
b += ar(392, 170, 410, 170, LB) + t(414, 174, "Compresor", LB)
b += ar(352, 218, 392, 232, LB) + t(396, 238, "Evaporador", LB)
b += tl(222, 150, ["Válv.", "exp."], LB, "start", 10)
b += ar(50, 160, 40, 190, LB) + t(20, 202, "Fancoil", LB)
F[8] = svg(520, 262, b, 500)

# 9 Distribución por difusores
b = rc(30, 70, 52, 30, K, 1.6, "#fff") + t(56, 89, "EQUIPO", K, "middle", 9, 700)
b += ln(82, 85, 110, 85, R, 3) + t(84, 66, "CAM", R, "start", 11, 700)
b += pa("M110,78 L330,78 M110,92 L330,92", K, 1.6)
for x in (150, 220, 290):
    b += pa(f"M{x-6},78 L{x-6},50 M{x+6},78 L{x+6},50", K, 1.4) + ci(x, 44, 8, R, 1.6, "#fff")
    b += pa(f"M{x-6},92 L{x-6},120 M{x+6},92 L{x+6},120", K, 1.4) + ci(x, 126, 8, R, 1.6, "#fff")
b += pa("M330,78 L330,92", K, 1.6)
b += t(300, 30, "200 m³/h", K, "start", 11, 600) + ar(298, 128, 340, 136, R) + t(344, 140, "Difusores", R, "start", 11, 600)
F[9] = svg(420, 152, b, 400)

# 10 Tabla sala máquinas
F[10] = ""  # se hace como tabla HTML

# 11 Caldera 3 pasos
b = rc(110, 50, 170, 130, K, 1.8, "#fff") + rc(130, 62, 130, 108, K, 1.4, "#fff")
for y in range(80, 168, 8):
    b += pa(f"M132,{y} q8,-3 16,0 t16,0 t16,0 t16,0 t16,0 t16,0 t16,0 t16,0", LB, 1)
b += t(195, 74, "Vapor", P, "middle", 10, 700)
b += rc(150, 88, 92, 10, K, 1.1, "#fff") + t(196, 96, "3° paso", K, "middle", 8)
b += rc(150, 108, 58, 10, K, 1.1, "#fff") + t(179, 116, "2° paso", K, "middle", 8)
b += rc(150, 130, 72, 16, K, 1.1, "#fff8ef") + t(240, 142, "Paso", K, "middle", 8) + t(190, 165, "Agua", P, "middle", 9, 700)
b += pa("M168,138 q6,-8 12,0 q6,-8 12,0 q6,-8 12,0", O, 1.6) + pa("M226,138 Q250,128 236,112 Q220,106 210,113", R, 3, arrow=True)
b += pa("M150,113 Q122,100 140,92", R, 3, arrow=True)
b += ln(195, 50, 195, 30, K, 2) + ar(195, 30, 195, 12, K) + t(203, 18, "Vapor", P, "start", 11, 700)
b += rc(280, 70, 14, 16, K, 1.3, "#fff") + ln(294, 78, 300, 78, K, 1.3)
b += ar(305, 76, 340, 70, P) + tl(344, 66, ["Chimenea", "regulador de", "presurización"], P, "start", 10, 12)
b += rc(92, 128, 38, 12, K, 1.3, "#fff") + ci(84, 150, 9, K, 1.4, "#fff") + ln(93, 150, 130, 140, K, 1.3)
b += t(60, 126, "Mufla", P, "end", 11, 700) + t(70, 172, "Quemador", P, "end", 11, 700)
b += rc(120, 180, 14, 16, K, 1.3) + rc(250, 180, 14, 16, K, 1.3)
b += ar(257, 220, 257, 200, P) + t(244, 232, "Retorno", P, "start", 11, 700)
b += ar(232, 140, 344, 150, P) + tl(348, 146, ["Cámara de retorno de", "gases de combustión", "sumergida"], P, "start", 10, 12)
F[11] = svg(480, 240, b, 440)

# 12 Corte edificio radiadores (principal)
def bldg(x, y, w, floors, fh):
    s = rc(x, y, w, floors * fh, K, 1.6, "#fff")
    for i in range(1, floors):
        s += ln(x, y + i * fh, x + w, y + i * fh, K, 1.1)
    return s
b = bldg(90, 110, 260, 4, 72)
b += ln(70, 398, 370, 398, K, 1.6)
b += pa("M138,388 Q138,368 150,368 Q162,368 162,388 Z", K, 1.6, "#fff") + rc(126, 388, 48, 10, K, 1.4, "#fff") + t(150, 418, "Caldera", K, "middle", 10, 700)
b += pa("M150,368 L150,30 L210,30", R, 1.8) + rc(210, 22, 36, 26, K, 1.6, "#fff") + ln(214, 44, 242, 26, K, 1.1) + ci(228, 36, 3, K, 1, K)
b += pa("M228,48 L228,70 L262,70", K, 1.3) + pa("M245,48 L245,58 L276,58", K, 1.3) + pa("M276,58 L276,26 Q276,16 286,16", K, 1.3) + t(282, 34, "desde TR", K, "start", 10)
b += pa("M120,394 L120,52", B, 1.6) + ln(112, 52, 128, 52, B, 1.6) + tl(60, 30, ["Ventilación de", "caldera a los", "4 vientos"], K, "start", 10, 11)
b += pa("M318,90 L318,16 Q318,8 326,8", B, 1.6)
b += ln(238, 48, 238, 392, B, 1.6, "6 4")
for i, y in enumerate((140, 212, 284)):
    b += radiator(272, y, 26, 18) + ln(266, y + 2, 272, y + 2, K, 1.3) + ln(298, y + 16, 305, y + 16, K, 1.3)
    b += t(270, y - 8, "LLDR", K, "start", 9, 600) + t(308, y + 14, "LLDR", K, "start", 9, 600)
b += pa("M190,370 L190,124 L262,124 L262,284", R, 1.8) + "".join(ln(262, y + 2, 266, y + 2, R, 1.8) for y in (140, 212, 284))
b += ln(305, 160, 305, 392, R, 1.6, "6 4") + t(312, 352, "Retorno", K, "start", 10, 600)
b += pa("M174,393 L210,393", K, 1.3) + t(198, 378, "VP", K, "middle", 9, 700) + xcirc(222, 382, 5) + t(222, 370, "VR", K, "middle", 8, 700) + t(186, 424, "BDA", K, "middle", 8, 700)
b += rc(250, 356, 12, 10, B, 1.3, "#fff") + t(256, 350, "RA", K, "middle", 9, 700) + ln(256, 366, 256, 400, B, 1.4) + ln(262, 366, 262, 400, B, 1.4)
b += t(276, 372, "CV", G, "start", 9, 700) + ln(272, 376, 272, 400, G, 1.4)
b += pa("M178,402 L178,408 L240,408 L240,432 L282,432 L282,408 L300,408", O, 2.2) + rc(240, 412, 60, 20, O, 1.6, "#fff4e8")
b += t(306, 404, "TI", K, "start", 9, 700) + t(330, 404, "PPA", K, "start", 9, 700) + rc(318, 405, 10, 6, O, 1.4) + ln(300, 408, 360, 408, O, 2)
b += t(350, 422, "A PPA o CI", K, "start", 9, 700) + t(270, 450, "Pozo de enfriamiento", K, "middle", 10, 700)
F[12] = svg(430, 458, b, 330)

# 12b detalles a la derecha
b = ""
b += pa("M40,60 L40,20", B, 1.6) + ln(32, 20, 48, 20, B, 1.6) + pa("M80,90 L80,20 L100,20", R, 1.8)
b += rc(100, 12, 30, 22, K, 1.6, "#fff") + ln(104, 30, 126, 16, K, 1) + pa("M115,34 L115,52 L140,52", K, 1.2) + pa("M128,34 L128,44 L150,44 L150,10 Q150,2 158,2", K, 1.2)
b += pa("M190,90 L190,10 Q190,2 198,2", B, 1.6) + ar(200, 30, 222, 30, K) + tl(226, 26, ["Ventilación de", "radiadores"], K, "start", 10, 11)
b += t(84, 8, "Desde caldera", K, "start", 10, 600) + ar(40, 70, 26, 100, K) + tl(0, 110, ["Ventilación de caldera", "a los 4 vientos."], K, "start", 10, 11)
# radiadores
b += pa("M80,250 L80,150 L140,150 L140,230", R, 1.8) + radiator(150, 160, 26, 18) + radiator(150, 210, 26, 18)
b += ln(140, 162, 150, 162, R, 1.6) + ln(140, 212, 150, 212, R, 1.6) + ln(176, 176, 184, 176, K, 1.3) + ln(176, 226, 184, 226, K, 1.3)
b += ln(184, 168, 184, 255, R, 1.6, "5 4") + ar(190, 146, 214, 140, K) + t(218, 144, "Radiador", K, "start", 10)
b += ar(190, 220, 214, 220, K) + t(218, 224, "LLDR", K, "start", 10) + ar(190, 252, 214, 252, K) + t(218, 256, "Retorno", K, "start", 10)
b += tl(20, 220, ["Sube", "de", "caldera"], K, "start", 10, 11)
# caldera se divide
b += pa("M60,330 Q60,312 72,312 Q84,312 84,330 Z", K, 1.6, "#fff") + rc(50, 330, 44, 9, K, 1.3, "#fff")
b += pa("M72,312 L72,298 M60,298 L84,298 M60,298 L60,288 M84,298 L84,288", R, 1.8) + t(92, 292, "se divide en 2", K, "start", 10)
b += pa("M44,338 L44,290", B, 1.6) + t(0, 316, "Ventilación", K, "start", 9) + ln(94, 334, 120, 334, K, 1.3) + t(124, 328, "retorno", K, "start", 10)
b += ar(72, 345, 66, 362, K) + t(66, 374, "caldera", K, "middle", 10)
b += pa("M110,345 Q130,370 160,385", K, 1.3, arrow=True) + t(130, 358, "esto baja a =", K, "start", 10, 600)
b += rc(162, 384, 10, 7, O, 1.4) + t(158, 380, "BDA", K, "start", 8, 700) + pa("M167,391 L167,420 L215,420", O, 2) + rc(195, 400, 40, 20, O, 1.5, "#fff4e8")
b += rc(196, 372, 10, 8, B, 1.3) + ln(199, 380, 199, 418, B, 1.3) + ln(204, 380, 204, 418, B, 1.3) + t(210, 378, "RA", K, "start", 8, 700) + t(216, 390, "CV", K, "start", 8, 700)
b += pa("M228,410 L228,396 L280,396", O, 2) + rc(244, 391, 10, 6, O, 1.4) + rc(266, 391, 10, 6, O, 1.4) + t(244, 388, "TI", K, "start", 8, 700) + t(266, 388, "PPA", K, "start", 8, 700)
b += t(276, 410, "A PPA o CI", K, "start", 8, 700) + t(214, 436, "Pozo de enfriamiento", K, "middle", 9, 700)
F[121] = svg(320, 444, b, 300)

# 13 Caldera horizontal
b = rc(120, 50, 170, 70, K, 1.8, "#fff") + rc(134, 58, 142, 54, B, 2, "#f2f6ff")
b += pa("M150,85 Q190,70 230,85 Q260,90 270,85 Q250,95 230,92 Q190,100 150,85 Z", O, 1.6, "#ffe4c6")
b += pa("M160,84 l12,-4 l-6,6 l14,-3 l-6,6 l16,-3 l-8,6 l18,-2", R, 1.2)
b += rc(150, 40, 12, 12, K, 1.4, K) + rc(250, 40, 12, 12, K, 1.4, K)
b += pa("M290,70 L320,70 L330,92 L330,112 L300,112", K, 1.6, "#fff") + pa("M312,96 q6,8 12,0", K, 1.3)
b += rc(132, 120, 10, 10, K, 1.4) + rc(268, 120, 10, 10, K, 1.4) + ln(120, 75, 112, 75, R, 1.6) + ln(120, 95, 112, 95, R, 1.6)
b += ar(150, 26, 155, 38, B) + tl(130, 10, ["Conexión de", "retorno"], B, "start", 10, 11)
b += ar(264, 44, 340, 36, B) + t(344, 40, "Conexión de salida", B)
b += ar(296, 56, 340, 56, B) + tl(344, 56, ["Aislación de la", "puerta"], B, "start", 11, 12)
b += ar(320, 104, 340, 92, B) + tl(344, 90, ["Visor de llama", "del quemador"], B, "start", 11, 12)
b += ar(290, 126, 340, 126, B) + t(344, 130, "Conexión con drenaje", B)
b += ar(112, 85, 80, 100, B) + tl(40, 114, ["Salida", "de", "humos"], B, "middle", 11, 12)
F[13] = svg(480, 150, b, 460)

# 14 Bombas paralelo
b = ar(20, 60, 50, 60, B) + pa("M60,30 L60,90", K, 1.6) + pa("M60,30 L400,30 L400,90 L60,90", K, 1.6) + ar(400, 60, 440, 60, B) + ln(400, 60, 400, 60)
for y in (30, 90):
    b += valve(100, y, B) + ln(140, y - 7, 140, y + 7, K, 1.4) + ln(146, y - 7, 146, y + 7, K, 1.4) + pump(200, y, 13, P)
    b += ln(255, y - 7, 255, y + 7, K, 1.4) + ln(261, y - 7, 261, y + 7, K, 1.4) + valve(320, y, B)
b += t(100, 16, "VE", K, "middle", 10, 700) + t(143, 16, "UD", K, "middle", 10, 700) + t(258, 16, "UD", K, "middle", 10, 700) + t(320, 16, "VE", K, "middle", 10, 700)
b += t(100, 112, "VE", K, "middle", 10, 700) + t(143, 112, "UD", K, "middle", 10, 700) + t(258, 112, "UD", K, "middle", 10, 700) + t(320, 112, "VE", K, "middle", 10, 700)
b += ln(60, 30, 60, 90, K, 1.6) + ln(56, 60, 60, 60, K, 1.6) + ln(400, 30, 400, 90, K, 1.6)
b += t(60, 138, "• VE = Válvula esclusa", K, "start", 11, 600) + t(60, 154, "• UD = Unión doble", K, "start", 11, 600)
F[14] = svg(460, 162, b, 420)

# 15 Solapa: sistema con TR y 4 pisos
b = bldg(120, 140, 230, 5, 56) + ln(90, 420, 380, 420, K, 1.6)
b += rc(230, 40, 54, 40, K, 1.6, "#fff") + ln(230, 40, 257, 66, K, 1.2) + ln(284, 40, 257, 66, K, 1.2) + t(257, 56, "TR", K, "middle", 10, 700)
b += pa("M257,66 L257,94 L300,94", P, 2) + ln(300, 86, 300, 102, P, 1.8) + t(296, 80, "V.L", P, "start", 10, 700)
b += ln(257, 94, 257, 420, K, 1.4, "6 4")
for i, y in enumerate((158, 214, 270, 326)):
    b += radiator(272, y, 26, 18) + t(270, y - 6, "LLP", R, "start", 9, 700) + t(304, y + 18, "LLP", K, "start", 9, 700)
    b += ln(262, y + 3, 272, y + 3, R, 1.6) + ln(298, y + 15, 332, y + 15, K, 1.3)
b += pa("M180,378 L180,150 L262,150 L262,329", R, 1.8)
b += ln(332, 160, 332, 420, K, 1.4, "6 4") + pa("M344,140 L344,60 Q344,48 358,48", B, 1.8)
b += ar(350, 168, 384, 160) + tl(388, 160, ["Ventilación de", "radiadores"], K, "start", 11, 12)
b += pa("M100,410 L100,36", B, 1.8) + ln(90, 36, 110, 36, B, 1.8) + ln(92, 44, 108, 44, B, 1.8)
b += pa("M100,410 L150,410 L150,384 L170,384", B, 1.4)
b += rc(150, 386, 22, 26, R, 1.4, "#fff") + rc(196, 386, 22, 26, R, 1.4, "#fff") + pa("M161,386 L161,374 L207,374 L207,386", R, 1.6)
b += t(140, 372, "VE", R, "end", 9, 700) + t(214, 370, "VE", R, "start", 9, 700) + valve(246, 400, P) + xcirc(272, 400, 7, P) + t(284, 404, "BR", P, "start", 9, 700)
b += t(232, 420, "VE", P, "start", 9, 700) + ar(240, 410, 170, 452, P) + tl(150, 466, ["Válvula", "limpieza"], P, "middle", 11, 12, 700)
b += pa("M326,420 L326,400 Q326,392 334,392", B, 1.6)
b += rc(230, 430, 14, 10, O, 1.5) + t(208, 440, "BDA", O, "start", 9, 700) + pa("M244,435 L280,446 L280,462 M262,462 L316,462 M300,432 L300,462", O, 2) + t(322, 446, "Pozo enfriamiento", O, "start", 10, 700)
F[15] = svg(500, 484, b, 380)

# 16 Convector de piso
b = pa("M20,60 L110,60 L110,120 L170,120 L170,60 L260,60", K, 1.6) + pa("M20,74 L96,74 L96,134 L184,134 L184,74 L260,74", K, 1.6)
b += pa("M60,40 L230,40 L260,60 M60,40 L20,60", K, 1.3) + "".join(ln(130 + i * 10, 52, 140 + i * 10, 44, K, 1) for i in range(6))
b += rc(118, 80, 44, 36, K, 1.3, "#fff")
for x in (128, 140, 152):
    b += pa(f"M{x},110 q-4,-8 0,-16 q4,-8 0,-16 q-4,-8 0,-14", R, 1.4, arrow=True)
b += pa("M200,24 q6,8 0,14 q-6,8 4,14", B, 1.6, arrow=True)
F[16] = svg(280, 150, b, 250)

# 17 Zocaloducto
b = pa("M40,60 L40,150 L60,140 L60,52 L190,22 L190,40 L60,70", K, 1.6) + pa("M40,60 L170,30 L190,22", K, 1.6)
b += ln(60, 140, 200, 106, K, 1.4) + ln(90, 134, 82, 150, K, 1) + ln(130, 124, 140, 140, K, 1) + ln(170, 114, 180, 130, K, 1)
for i in range(5):
    b += ci(76 + i * 22, 58 - i * 5, 2.4, K, 1.2)
for x, y in ((80, 50), (110, 44), (140, 38)):
    b += pa(f"M{x},{y} q-4,-7 0,-14 q4,-7 0,-14", R, 1.4, arrow=True)
F[17] = svg(220, 160, b, 190)

# 18 Caloventilador
b = pa("M30,40 L110,40 L110,120 L30,120 Z", K, 1.8, "#fff") + pa("M30,40 L48,22 L128,22 L110,40 M110,120 L128,102 L128,22", K, 1.8)
b += rc(46, 56, 48, 48, K, 1.4, "#fff") + "".join(ln(46 + i * 8, 56, 46 + i * 8, 104, K, 1) + ln(46, 56 + i * 8, 94, 56 + i * 8, K, 1) for i in range(1, 6))
F[18] = svg(150, 136, b, 130)

# 19 Convector
b = rc(30, 30, 110, 100, K, 1.8, "#fff") + rc(42, 50, 86, 56, K, 1.2, "#fff")
for x in range(52, 124, 9):
    b += ln(x, 56, x, 66, K, 1) + ln(x, 74, x, 84, K, 1) + ln(x, 92, x, 100, K, 1)
for x in (62, 104):
    b += pa(f"M{x},50 q-4,-8 0,-14 q4,-8 0,-16", R, 1.6, arrow=True) + pa(f"M{x},152 q-4,-8 0,-14 q4,-8 0,-16", B, 1.6, arrow=True)
b += pa("M84,92 q8,-6 0,-10 q-8,-6 0,-10", R, 1.4)
F[19] = svg(170, 160, b, 150)

# 20 Piso radiante esquema
b = rc(40, 30, 70, 26, K, 1.6, "#fff") + t(75, 47, "Caldera", K, "middle", 11, 700)
b += pa("M110,40 L200,40 L200,94", R, 1.8) + pump(200, 104, 10) + t(216, 108, "Bomba", K, "start", 11, 600)
b += pa("M200,114 L200,140", R, 1.8) + rc(170, 140, 54, 14, K, 1.4, "#fff") + t(232, 151, "Colector alimentación", K, "start", 10)
b += pa("M44,56 L44,140", B, 1.8) + pa("M44,140 L72,140", B, 1.8) + rc(72, 140, 54, 14, K, 1.4, "#fff") + tl(30, 178, ["Colector", "retorno"], K, "start", 10, 12)
for x in (82, 96, 110):
    b += ln(x, 154, x, 166, K, 1.2)
for x in (182, 198, 212):
    b += ln(x, 154, x, 166, R, 1.2)
b += pa("M190,154 L190,226 L150,226", R, 1.6) + pa("M100,154 L100,218 L140,218", B, 1.6)
b += rc(146, 206, 110, 64, K, 1.4, "#fff")
d = "M150,214"
for i in range(7):
    y = 214 + i * 7
    d += f" L248,{y} Q254,{y+3.5} 248,{y+7}" if i % 2 == 0 else f" L156,{y} Q150,{y+3.5} 156,{y+7}"
b += pa(d, K, 1.2)
F[20] = svg(380, 284, b, 330)

# 21 Caja de colectores
b = pa("M30,50 L30,240 M44,50 L44,240", K, 1.4) + t(10, 28, "De", B, "start", 11, 700) + t(10, 40, "caldera", B, "start", 11, 700)
b += rc(30, 44, 300, 14, K, 1.6, "#fff") + rc(30, 128, 300, 14, K, 1.6, "#fff")
b += rc(52, 40, 12, 22, K, 1.4, "#fff") + ci(80, 51, 5, K, 1.3, "#fff") + ci(94, 51, 5, K, 1.3, "#fff")
b += rc(52, 124, 12, 22, K, 1.4, "#fff") + ci(80, 135, 5, K, 1.3, "#fff") + ci(94, 135, 5, K, 1.3, "#fff")
for x in (150, 175, 200):
    b += pa(f"M{x},58 L{x},128 M{x+8},58 L{x+8},128", K, 1.2) + ci(x + 4, 92, 3, K, 1, "#fff")
for x in (160, 186):
    b += pa(f"M{x},142 L{x},230 M{x+8},142 L{x+8},230", K, 1.2) + ci(x + 4, 172, 3, K, 1, "#fff")
b += pa("M318,44 L312,22 L334,22 L328,44 Z", K, 1.4, "#fff") + pa("M318,128 L312,106 L334,106 L328,128 Z", K, 1.4, "#fff")
b += ar(56, 34, 62, 40) + t(56, 12, "Llave de entrada", P, "start", 10, 700) + ar(96, 30, 92, 44) + t(100, 26, "Termómetro de entrada", P, "start", 10, 700)
b += ar(338, 24, 360, 22, P) + tl(364, 22, ["Válvula de", "desaire"], P, "start", 11, 12)
b += ar(332, 52, 360, 58, P) + t(364, 62, "Colector de alimen.", P)
b += ar(332, 108, 360, 92, P) + t(364, 96, "Válvula de regulación", P)
b += ar(332, 136, 360, 130, P) + t(364, 134, "Colector de retorno", P)
b += ar(332, 142, 360, 160, P) + t(364, 164, "Válvula de retorno", P)
b += ar(58, 148, 58, 166, P) + tl(52, 178, ["Llave de", "salida"], P, "start", 10, 11, 700)
b += ar(94, 142, 200, 206, P) + t(204, 214, "Termómetro de salida", P, "start", 10, 700)
b += t(20, 256, "A intercambiador de calor o caldera", P, "start", 11, 700)
F[21] = svg(500, 264, b, 470)

# 22 / 23 cortes losa y piso radiante
def layers(rows, label_rows, tubes_row, caption):
    s = ""; y = 20
    for i, (h, fill) in enumerate(rows):
        s += rc(40, y, 170, h, K, 1.3, fill)
        if i == tubes_row:
            for x in (70, 120, 170):
                s += ci(x, y + h / 2, 5, K, 1.4, "#fff")
            s += ln(40, y + h / 2, 210, y + h / 2, K, 1.1)
        y += h
    return s
b = rc(40, 20, 170, 10, K, 1.3, "#fff") + rc(40, 30, 170, 14, K, 1.3, "#f4efe8") + "".join(ci(60 + i * 18, 37, 0.8, K, 1, K) for i in range(9))
b += hatch(40, 44, 170, 8, K, 6, "h22") + rc(40, 52, 170, 30, K, 1.3, "#ece8f6") + "".join(ci(x, 66, 5, K, 1.4, "#fff") for x in (70, 120, 170)) + ln(40, 74, 210, 74, K, 1)
for lbl, y in (("Piso", 24), ("Contrapiso", 38), ("Aisl. térmica", 50), ("Tubería", 66), ("Hierro", 76)):
    b += pa(f"M210,{y} L232,{y}", K, 1.2) + t(236, y + 4, lbl, P, "start", 10, 600)
b += pa("M100,82 L100,100 L80,100", K, 1.2) + t(30, 112, "Losa H°A°", P, "start", 10, 600)
F[22] = svg(330, 120, b, 300)
b = rc(40, 20, 170, 10, K, 1.3, "#fff") + rc(40, 30, 170, 14, K, 1.3, "#f4efe8") + "".join(ci(60 + i * 18, 37, 0.8, K, 1, K) for i in range(9))
b += rc(40, 44, 170, 16, K, 1.3, "#efefef") + "".join(ci(x, 52, 5, K, 1.4, "#fff") for x in (70, 120, 170)) + ln(40, 52, 210, 52, K, 1)
b += hatch(40, 60, 170, 8, K, 6, "h23") + rc(40, 68, 170, 26, K, 1.3, "#ece8f6") + ln(40, 86, 210, 86, K, 1)
for lbl, y in (("Piso", 24), ("Contrapiso", 38), ("Tubería en capa de H° 1:3", 52), ("Ais. térmico", 64), ("Hierro", 86)):
    b += pa(f"M210,{y} L232,{y}", K, 1.2) + t(236, y + 4, lbl, P, "start", 10, 600)
b += pa("M100,94 L100,108 L120,108", K, 1.2) + t(124, 112, "Losa H°A°", P, "start", 10, 600)
F[23] = svg(390, 120, b, 340)

# 24 Red de distribución domiciliaria
b = ln(20, 30, 380, 30, K, 1.8) + t(200, 20, "RED DE DISTRIBUCIÓN", R, "middle", 11, 700)
for x in (110, 210, 310):
    b += ln(x, 30, x, 52, K, 1.4) + rc(x - 6, 52, 12, 12, K, 1.4, "#fff") + ln(x, 64, x, 90, K, 1.4) + rc(x - 9, 90, 18, 18, K, 1.4, "#fff") + ln(x - 9, 96, x + 9, 96, K, 1)
    b += ln(x, 108, x, 148, K, 1.4) + board(x - 18, 148, 36, 14)
    b += ln(x - 10, 162, x - 10, 182, K, 1.2) + ln(x + 10, 162, x + 10, 182, K, 1.2) + sboard(x - 20, 182, 18, 10) + sboard(x + 2, 182, 18, 10)
    for dx in (-17, -11, -5, 5, 11, 17):
        b += ln(x + dx, 192, x + dx, 204, K, 1)
b += ln(60, 126, 360, 126, K, 1.2, "10 8")
b += t(84, 58, "Caja", R, "end", 10, 600) + t(84, 70, "toma", R, "end", 10, 600) + t(84, 103, "Medidor", R, "end", 10, 600) + t(84, 160, "TP", R, "end", 11, 700) + t(84, 192, "TS", R, "end", 11, 700)
b += t(110, 220, "Circuitos", R, "middle", 10, 600) + t(330, 120, "L.M", K, "start", 11, 700)
b += pa("M392,40 Q402,40 402,60 L402,76 Q402,82 410,84 Q402,86 402,92 L402,108 Q402,124 392,124", B, 1.6) + tl(416, 78, ["Responsabilidad", "compañía"], B, "start", 11, 13)
b += pa("M392,128 Q402,128 402,148 L402,160 Q402,166 410,168 Q402,170 402,176 L402,190 Q402,206 392,206", B, 1.6) + tl(416, 164, ["Responsabilidad", "del propietario."], B, "start", 11, 13)
F[24] = svg(520, 228, b, 470)

# 25 Esquema montante
b = rc(110, 30, 170, 210, K, 1.6, "#fff")
fl = ["4°P", "3°P", "2°P", "1°P", "PB"]
for i, f in enumerate(fl):
    y = 60 + i * 34
    b += ln(110, y, 280, y, K, 1.1) + t(96, y + 22 if i < 4 else y + 22, f, K, "end", 10, 700)
b += rc(200, 8, 50, 22, K, 1.4, "#fff") + ln(40, 230, 330, 230, K, 1.5)
b += t(96, 248, "S", K, "end", 10, 700)
for i in range(4):
    y = 72 + i * 34
    b += rc(118, y, 9, 9, R, 1.3, "#fff") + ln(127, y + 5, 180, y + 5, R, 1.2, "4 3")
b += ln(180, 60, 180, 228, R, 1.2, "4 3") + ln(196, 40, 196, 228, R, 1.2, "4 3") + ln(204, 40, 204, 228, R, 1.2, "4 3") + ln(196, 40, 232, 40, R, 1.2, "4 3")
b += rc(190, 12, 8, 10, R, 1.3, "#fff") + rc(252, 12, 8, 10, R, 1.3, "#fff") + ln(256, 22, 256, 34, R, 1.2, "4 3")
b += t(186, 12, "TS azot.", R, "end", 9, 700) + t(264, 18, "Sala máquinas", B, "start", 10, 700) + t(264, 34, "TS ascensor (Asc.)", B, "start", 9, 700)
b += t(116, 66, "TS dom.", R, "start", 8, 700)
b += rc(122, 234, 24, 14, B, 1.3, "#fff") + rc(176, 234, 44, 14, B, 1.3, "#fff") + ar(134, 250, 130, 272, B) + t(130, 284, "Bomba", B, "middle", 10, 700) + ar(198, 250, 196, 272, B) + t(196, 284, "Medidores", B, "middle", 10, 700)
b += rc(228, 222, 10, 10, R, 1.3, "#fff") + rc(242, 222, 10, 10, R, 1.3, "#fff") + rc(228, 236, 24, 10, R, 1.3, "#fff")
b += t(240, 214, "TPSD", R, "middle", 8, 700) + t(258, 232, "T.P.S.G", R, "start", 9, 700) + t(258, 246, "Toma", R, "start", 9, 700)
b += pa("M252,246 L252,262 L330,262 L330,150", R, 1.6) + rc(324, 140, 12, 10, R, 1.4, "#fff") + t(342, 149, "CTP", R, "start", 10, 700)
F[25] = svg(420, 292, b, 340)

# 26 Esquema unifilar múltiples usuarios
b = ci(300, 20, 8, K, 1.4) + ci(300, 32, 8, K, 1.4) + t(316, 30, "Transformador", K, "start", 12, 600)
b += ln(300, 40, 300, 52, K, 1.4) + pa("M300,52 l-6,4 l12,4 l-12,4 l6,4", K, 1.4) + ln(300, 68, 300, 74, K, 1.4) + t(316, 66, "Acometida", K, "start", 12, 600)
b += rc(292, 74, 16, 16, K, 1.4, "#fff") + t(316, 87, "Toma principal", K, "start", 12, 600) + ln(300, 90, 300, 102, K, 1.4)
b += rc(292, 102, 16, 16, K, 1.4, "#fff") + t(316, 115, "Toma secundaria", K, "start", 12, 600) + ln(300, 118, 300, 132, K, 1.4)
b += ln(130, 132, 430, 132, K, 1.6) + t(220, 126, "Gabinetes monofásicos", K, "end", 11, 600) + t(470, 126, "Medidor trifásico", K, "middle", 11, 600)
b += rc(70, 142, 220, 70, K, 1.5, "#fff")
for i, x in enumerate((95, 145, 195, 245)):
    b += ln(x, 132, x, 152, K, 1.3) + rc(x - 13, 152, 26, 40, K, 1.4, "#fff") + ln(x - 13, 160, x + 13, 160, K, 1) + t(x, 174, "M", K, "middle", 10, 700) + t(x, 186, f"V{i+1}", K, "middle", 10, 700)
    b += ln(x, 192, x, 228, K, 1.3) + board(x - 16, 228, 32, 12) + t(x - 10, 224, "TPD", K, "middle", 9, 700)
    b += ln(x, 240, x, 268, K, 1.3) + sboard(x - 12, 268, 24, 10) + t(x, 292, "TSD", K, "middle", 10, 700)
b += rc(70, 218, 220, 32, K, 1.3, "none")
b += pa("M70,190 L40,190 L40,300", B, 1.6) + gnd(40, 300, B) + t(54, 318, "Jabalina", B, "start", 12, 700)
b += ar(70, 232, 44, 222, K) + tl(0, 210, ["Tableros", "principales", "domiciliarios"], K, "start", 10, 11, 600)
b += rc(352, 142, 56, 60, K, 1.5, "#fff") + ln(380, 132, 380, 152, K, 1.3) + rc(366, 152, 28, 40, K, 1.4, "#fff") + t(380, 174, "M", K, "middle", 10, 700) + t(380, 186, "SG", K, "middle", 10, 700)
b += ln(394, 176, 420, 176, K, 1) + t(424, 180, "Servicios grales.", K, "start", 11, 600)
b += ln(380, 202, 380, 228, K, 1.3) + board(360, 228, 40, 14) + t(408, 240, "TPSG", K, "start", 11, 700)
b += ln(380, 242, 380, 262, K, 1.3) + ln(330, 262, 430, 262, K, 1.3)
for x in (330, 380, 430):
    b += ln(x, 262, x, 270, K, 1.3) + sboard(x - 14, 270, 28, 10)
b += t(450, 280, "TS 220V", K, "start", 11, 700) + ar(424, 280, 420, 304, K) + ar(436, 280, 440, 304, K) + t(448, 306, "luces", K, "start", 11)
b += t(380, 296, "TS", K, "middle", 10, 700) + t(380, 308, "ASC", K, "middle", 10, 700) + t(326, 296, "TS", K, "middle", 10, 700) + t(326, 308, "380V", K, "middle", 10, 700)
for i in range(5):
    b += sboard(290, 318 + i * 10, 14, 7) + ln(304, 322 + i * 10, 336 + i, 322 + i * 10, K, 1)
b += ln(336, 280, 340, 362, K, 1) + t(272, 340, "(5)", K, "end", 11, 700)
b += tl(250, 380, ["Bombas recirculadoras", "Bomba cloacal, pluvial, TB", "Caldera"], K, "start", 11, 13, 600)
F[26] = svg(590, 420, '<g transform="translate(30,0)">' + b + "</g>", 520)

# 27 Corte edificio eléctrico (solapa)
b = rc(140, 110, 280, 220, K, 1.6, "#fff") + ln(345, 110, 345, 330, K, 1.2) + ln(110, 330, 470, 330, K, 1.6)
for i, f in enumerate(["4°P", "3°P", "2°P", "1°P"]):
    y = 110 + i * 44
    b += ln(140, y + 44, 420, y + 44, K, 1.1) + t(410, y + 20, f, K, "end", 10, 700)
    b += sboard(150, y + 14, 18, 12, B) + t(172, y + 24, "TS", B, "start", 10, 700) + pa(f"M168,{y+20} L200,{y+20} L{204 + i*5},{y+24} L{204+i*5},300", B, 1.3)
    b += pa(f"M262,{y+30} L278,{y+30} M278,{y+30} L278,{y+30}", O, 1.4) + ci(286, y + 30, 7, O, 1.4, "#fff")
b += t(380, 304, "PB", K, "start", 10, 700)
b += ln(262, 140, 262, 300, O, 1.6)
b += rc(200, 30, 70, 50, K, 1.6, "#fff") + ln(200, 30, 235, 60, K, 1.2) + ln(270, 30, 235, 60, K, 1.2) + t(235, 48, "TR", K, "middle", 11, 700)
b += rc(330, 40, 90, 70, K, 1.6, "#fff") + tl(375, 60, ["Sala de", "máquinas"], K, "middle", 10, 12, 600) + sboard(372, 86, 22, 12, R) + t(400, 96, "TA", R, "start", 10, 700)
b += sboard(222, 84, 18, 12, R) + t(222, 108, "TBA", R, "start", 8, 700) + ln(240, 90, 372, 90, R, 1.4) + ln(256, 90, 236, 296, R, 1.4)
b += rc(160, 298, 50, 30, K, 1.6, "#fff") + tl(168, 310, ["T.S", "G×5", "TP×5"], K, "start", 8, 9, 700)
b += sboard(212, 304, 22, 16, R) + t(214, 298, "TPSG", R, "start", 9, 700) + rc(250, 304, 18, 16, R, 1.3, "#fff") + t(252, 298, "TSG ilum.", R, "start", 9, 700) + ln(234, 312, 250, 312, R, 1.2)
b += rc(100, 296, 26, 26, K, 1.6, "#fff") + rc(108, 302, 10, 14, K, 1.2) + t(100, 288, "CTP", K, "start", 10, 700) + ln(126, 309, 160, 309, K, 1.3)
b += pa("M86,340 L113,340 L113,322", K, 1.3) + t(76, 352, "acometida", K, "start", 10, 600)
b += ln(186, 328, 186, 358, LB, 1.6) + gnd(186, 358, LB) + t(200, 374, "Jabalina", LB, "start", 11, 700)
b += pa("M194,328 L194,342 L366,342 L366,316", B, 1.5) + sboard(356, 306, 20, 12, B) + t(340, 304, "TS PB", B, "end", 9, 700)
b += pa("M258,320 L258,336 L432,336 L432,320", R, 1.5) + sboard(424, 308, 18, 12, R) + t(446, 318, "TB", R, "start", 10, 700)
F[27] = svg(490, 384, b, 420)

# 28 Sistema separado
b = pa("M60,140 L60,40 L230,40 L230,140", K, 1.8) + gnd(60, 140) + gnd(230, 140) + hatch(110, 90, 70, 40, R, 7, "h28") + ln(40, 130, 250, 130, K, 1.3)
b += bolt(160, 4, 1) + t(186, 20, "Rayo", K, "start", 11, 600) + bolt(76, 76, 0.8, O)
b += tl(4, 16, ["Sistema de", "protección"], K, "start", 10, 11, 600) + ar(30, 24, 58, 40) + tl(0, 80, ["Descargas", "laterales"], K, "start", 10, 11, 600)
b += ar(146, 130, 140, 160, R) + tl(140, 172, ["Volumen a", "proteger"], R, "middle", 11, 12, 700)
F[28] = svg(270, 192, b, 250)

# 29 Parcialmente separado
b = pa("M20,80 Q20,60 50,50 L120,20 L190,50 Q220,60 220,80", K, 1.8) + ln(120, 20, 120, 4, K, 1.6) + t(128, 12, "Rayo", K, "start", 11, 600)
b += pa("M50,140 L50,80 L120,40 L190,80 L190,140 Z", R, 1.4) + hatch(52, 80, 136, 60, R, 9, "h29") + pa("M52,80 L120,42 L188,80", R, 1.4, "#fff")
b += ln(40, 80, 40, 150, K, 1.6) + ln(200, 80, 200, 150, K, 1.6) + gnd(40, 150) + gnd(200, 150) + ln(20, 150, 230, 150, K, 1.3)
b += ar(206, 40, 236, 30) + tl(240, 30, ["Sistema de", "protección"], K, "start", 10, 11, 600) + t(208, 120, "Bajada", K, "start", 10, 600)
b += ar(118, 140, 112, 166, R) + t(112, 180, "Volumen a proteger", R, "middle", 11, 700)
F[29] = svg(310, 188, b, 290)

# 30 Varilla con punta captora
b = pa("M30,120 L170,120 L190,104 L190,136 L170,152 L30,152 Z", K, 1.6, "#fff") + pa("M30,120 L50,104 L190,104", K, 1.6)
b += pa("M90,104 L90,82 L130,82 L140,74 L140,96 L130,104 M90,82 L100,74 L140,74", K, 1.4, "#fff")
b += ln(122, 78, 122, 30, K, 3) + ln(126, 78, 126, 38, R, 2.4)
b += pa("M126,90 L126,110 L176,110 L176,140 L182,160", R, 1.8) + pa("M182,160 l-4,6 l8,-2 l-2,10", R, 1.6)
b += pa("M70,8 l14,8 l-6,2 l12,8", P, 1.6) + pa("M98,30 l8,4 m4,4 l6,4", K, 1.4, dash="3 4")
b += ar(66, 4, 82, 20, P) + t(40, 12, "Rayo", P, "end", 11, 700) + ar(132, 36, 190, 30, P) + t(194, 34, "Varilla", P, "start", 11, 700)
F[30] = svg(260, 180, b, 240)

# 31 Hilo de guardia
b = pa("M30,100 L60,60 Q160,10 260,60 L290,100", K, 1.4) + ln(70, 50, 70, 110, K, 2) + ln(250, 50, 250, 110, K, 2)
b += ci(30, 100, 3, K, 1, K) + ci(290, 100, 3, K, 1, K)
b += pa("M120,80 L160,60 L200,80 L200,120 L160,138 L120,120 Z M160,60 L160,138 M120,80 L160,98 L200,80", K, 1.4, "#fff")
b += rc(128, 100, 10, 14, K, 1.1) + rc(176, 96, 14, 8, K, 1.1)
b += t(160, 22, "Hilo de guardia", K, "middle", 11, 600) + tl(20, 122, ["Toma a", "tierra"], K, "start", 10, 11, 600) + t(240, 122, "Toma a tierra", K, "start", 10, 600)
F[31] = svg(330, 140, b, 300)

# 32 Malla captora
b = pa("M60,60 L120,30 L200,40 L260,60 L180,80 L60,60", R, 1.8, "#fff") + pa("M60,60 L60,130 L180,150 L260,124 L260,60 M180,80 L180,150", R, 1.8)
b += ln(90, 45, 170, 62, R, 1.4) + ln(120, 30, 120, 70, R, 1.4) + ln(160, 36, 230, 50, R, 1.4) + ln(150, 74, 230, 50, R, 1.2)
for x, y in ((60, 130), (180, 150), (260, 124)):
    b += pa(f"M{x},{y} L{x-14},{y+10} L{x-14},{y+22}", R, 1.6)
for y in range(72, 126, 12):
    b += ln(60, y, 54, y, R, 1.1) + ln(260, y - 2, 266, y - 2, R, 1.1) + ln(180, y + 10, 186, y + 10, R, 1.1)
b += rc(80, 108, 7, 12, K, 1.1) + rc(140, 120, 7, 12, K, 1.1) + rc(220, 110, 7, 12, K, 1.1)
b += ar(120, 26, 110, 12, R) + t(84, 10, "Malla captora", R, "start", 11, 700) + t(268, 50, "Bajada", R, "start", 11, 700)
F[32] = svg(330, 174, b, 300)

# 33 Método del ángulo
b = ln(20, 130, 300, 130, K, 1.6) + ln(60, 30, 60, 130, K, 1.8) + ln(260, 30, 260, 130, K, 1.8)
b += ln(60, 30, 10, 80, K, 1.3, "5 4") + ln(60, 30, 175, 100, K, 1.3, "5 4") + ln(260, 30, 145, 100, K, 1.3, "5 4") + ln(260, 30, 300, 70, K, 1.3, "5 4")
b += rc(120, 92, 80, 18, K, 1.6, "#fff") + rc(132, 110, 56, 20, K, 1.6, "#fff")
b += ar(156, 92, 164, 66, R) + t(150, 60, "Intersección", R, "start", 11, 600) + t(140, 14, "Método del ángulo", R, "middle", 12, 700) + ar(220, 14, 254, 30, R)
b += ar(262, 116, 296, 116, R) + tl(300, 112, ["Captor de", "asta"], R, "start", 10, 11, 600) + ar(160, 132, 158, 150, R) + t(158, 162, "Vivienda", R, "middle", 11, 600)
b += ci(390, 76, 38, K, 1.3) + ci(450, 76, 38, K, 1.3)
b = b.replace(f'<circle cx="390" cy="76" r="38" stroke="{K}" stroke-width="1.3" fill="none"/>', f'<circle cx="390" cy="76" r="38" stroke="{K}" stroke-width="1.3" fill="none" stroke-dasharray="5 4"/>')
b = b.replace(f'<circle cx="450" cy="76" r="38" stroke="{K}" stroke-width="1.3" fill="none"/>', f'<circle cx="450" cy="76" r="38" stroke="{K}" stroke-width="1.3" fill="none" stroke-dasharray="5 4"/>')
b += rc(400, 64, 40, 24, K, 1.6, "#fff") + ln(400, 76, 440, 76, K, 1.2)
F[33] = svg(500, 170, b, 470)

# 34 Esquema pasadizo
b = rc(60, 40, 160, 50, K, 3, "#fff") + ln(60, 90, 60, 420, K, 3) + ln(120, 90, 120, 420, K, 1.4) + ln(60, 420, 150, 420, K, 3) + ln(150, 420, 150, 90, K, 3)
b += ln(150, 90, 220, 90, K, 3)
b += ci(80, 64, 12, K, 1.4, "#fff") + ln(72, 56, 88, 72, K, 1) + ln(72, 72, 88, 56, K, 1) + rc(120, 62, 22, 12, K, 1.4, "#fff")
b += ln(70, 76, 70, 330, K, 1.1) + ln(90, 76, 90, 230, K, 1.1)
b += rc(84, 230, 40, 70, K, 1.4, "#fff") + rc(80, 222, 48, 8, K, 1.4) + rc(94, 300, 20, 8, K, 1.2)
b += rc(64, 320, 12, 26, K, 1.4, "#fff")
for y in (210, 280, 350):
    b += ln(150, y, 280, y, K, 4)
b += pa("M70,404 l-4,4 l8,4 l-8,4 l4,4", K, 1.2) + pa("M104,404 l-4,4 l8,4 l-8,4 l4,4", K, 1.2)
b += pa("M30,64 Q120,40 240,64", B, 1.6, arrow=True) + tl(244, 64, ["Ventilación", "cruzada y", "mecánica"], B, "start", 11, 12, 600)
b += ar(80, 52, 70, 22, R) + t(54, 16, "Polea", R, "start", 11, 700) + ar(134, 62, 168, 40, R) + t(172, 40, "Motor", R, "start", 11, 700)
b += ar(190, 40, 214, 14, R) + t(218, 14, "Sala de máquinas", R, "start", 11, 700)
b += ar(126, 226, 170, 196, R) + t(174, 196, "Bastidor de cabina", R, "start", 11, 700) + ar(124, 262, 170, 262, R) + t(174, 266, "Cabina", R, "start", 11, 700)
b += ar(66, 336, 30, 352, R) + t(0, 366, "Contrapeso", R, "start", 11, 700) + ar(112, 414, 170, 404, R) + t(174, 408, "Paragolpes", R, "start", 11, 700)
b += pa("M44,92 L44,150", P, 1.4) + t(36, 124, "Claro sup.", P, "middle", 10, 700).replace("<text", '<text transform="rotate(-90 36 124)"')
b += pa("M44,154 L44,370", P, 1.4) + t(36, 262, "Recorrido", P, "middle", 10, 700).replace("<text", '<text transform="rotate(-90 36 262)"')
b += pa("M44,374 L44,418", P, 1.4) + t(36, 396, "Claro inf.", P, "middle", 9, 700).replace("<text", '<text transform="rotate(-90 36 396)"')
F[34] = svg(330, 446, '<g transform="translate(0,16)">' + b + "</g>", 270)

# 35 Esquema cabina (planta)
b = rc(40, 30, 200, 150, K, 2.4, "#fff") + rc(60, 46, 160, 118, K, 1, "none")
b += rc(100, 38, 70, 8, K, 1.4, "#fff") + rc(94, 36, 8, 12, K, 1.2) + rc(168, 36, 8, 12, K, 1.2)
b += rc(90, 70, 100, 76, K, 1.8, "#fff") + ln(98, 92, 182, 92, K, 1, "5 4") + ln(98, 110, 182, 110, K, 1, "5 4")
b += rc(74, 96, 12, 24, K, 1.3, "#fff") + rc(194, 96, 12, 24, K, 1.3, "#fff") + rc(206, 100, 8, 16, K, 1.3)
b += ci(96, 136, 6, K, 1.3, "#fff") + ci(100, 168, 6, K, 1.3, "#fff")
b += ar(138, 46, 146, 18, R) + t(110, 12, "Contrapeso c/guía", R, "start", 11, 700) + ar(170, 40, 190, 22, R) + t(194, 24, "Grapa contrapeso", R, "start", 11, 700)
b += ar(214, 108, 250, 100, R) + tl(254, 100, ["Grapa guía", "cabina"], R, "start", 11, 12, 700) + ar(206, 118, 250, 132, R) + t(254, 136, "Guía cabina", R, "start", 11, 700)
b += ar(94, 142, 60, 190, R) + ar(100, 174, 62, 192, R) + tl(30, 206, ["Botones", "de llamado"], R, "start", 11, 12, 700)
b += ar(140, 146, 160, 196, R) + t(150, 210, "Protección bastidor", R, "start", 11, 700)
F[35] = svg(350, 222, b, 330)

# 36 Sala de máquinas
b = rc(50, 30, 320, 260, K, 2.6, "#fff") + rc(62, 42, 296, 236, K, 1, "none")
b += hatch(70, 22, 30, 8, K, 5, "h36") + ar(108, 26, 150, 12, R) + t(154, 14, "Ventilación mecánica", R, "start", 11, 700)
b += rc(90, 80, 150, 80, K, 1.2, "none", 0, "6 4")
b += rc(110, 100, 22, 18, K, 1.4, "#fff") + rc(176, 100, 30, 18, K, 1.4, "#fff") + ln(132, 109, 176, 109, K, 1.4) + t(154, 104, "0,5", K, "middle", 9, 600)
b += rc(118, 126, 14, 20, K, 1.3, "#fff") + rc(186, 126, 14, 20, K, 1.3, "#fff")
b += t(104, 108, "Polea", R, "end", 10, 700) + t(160, 94, "Regul.", R, "middle", 10, 700) + tl(246, 136, ["Freno", "Motor"], R, "start", 10, 11, 700)
b += pa("M20,210 Q180,250 260,170 Q300,130 380,120", B, 1.6, arrow=True) + t(384, 108, "Ventilación", R, "start", 11, 700) + t(384, 120, "cruzada", R, "start", 11, 700)
b += ln(300, 50, 300, 270, B, 1.4) + ar(300, 160, 300, 52, B) + ar(300, 160, 300, 268, B) + t(292, 180, "mín. 3,20 m", B, "middle", 10, 700).replace("<text", '<text transform="rotate(-90 292 180)"')
b += rc(348, 160, 10, 26, K, 1.3, "#fff") + ar(360, 172, 390, 168, R) + t(394, 172, "T.S ascensor", R, "start", 11, 700)
b += pa("M358,226 L330,206", K, 1.4) + pa("M330,206 A28,28 0 0 1 358,252", K, 1, dash="3 3") + ln(358, 226, 410, 226, K, 1.4) + ln(358, 254, 410, 254, K, 1.4)
b += ar(366, 240, 366, 228, B) + ar(366, 240, 366, 252, B) + t(372, 244, "mín. 0,7", B, "start", 10, 700)
b += rc(186, 262, 24, 14, K, 1.4, "#fff") + pa("M226,276 L232,262 L238,276 Z", K, 1.2, K)
b += ar(196, 278, 186, 300, R) + tl(170, 312, ["Control", "maniob."], R, "middle", 11, 12, 700) + ar(232, 278, 240, 300, R) + t(240, 312, "Matafuego", R, "start", 11, 700)
F[36] = svg(470, 336, b, 420)
