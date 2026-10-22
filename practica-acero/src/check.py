# -*- coding: utf-8 -*-
"""Control de una lámina DXF: altura mínima de letra, textos superpuestos y contenido fuera del marco.
Uso: python3 check.py archivo.dxf [más archivos]"""
import sys
import ezdxf
from ezdxf.enums import TextEntityAlignment as TA
from ezdxf import bbox
from lib import tw

def caja(e):
    h = e.dxf.height
    bold = "NEGRITA" in e.dxf.style
    w = tw(e.dxf.text, h, bold) * e.dxf.width / 0.9 if e.dxf.text else 0
    al, p, _ = e.get_placement() if len(e.get_placement()) == 3 else (*e.get_placement(), None)
    x, y = p[0], p[1]
    n = al.name if al else "LEFT"
    if "CENTER" in n: x -= w / 2
    elif "RIGHT" in n: x -= w
    if "MIDDLE" in n: y -= h / 2
    elif n.startswith("TOP"): y -= h
    return (x, y, x + w, y + h)

for f in sys.argv[1:]:
    d = ezdxf.readfile(f); m = d.modelspace()
    ts = [e for e in m.query("TEXT") if e.dxf.text.strip() and abs(e.dxf.rotation) < 1]
    cajas = [(caja(e), e.dxf.text) for e in ts]
    hmin = min(e.dxf.height for e in ts)
    sup = []
    for i in range(len(cajas)):
        a, ta = cajas[i]
        for j in range(i + 1, len(cajas)):
            b, tb = cajas[j]
            ox = min(a[2], b[2]) - max(a[0], b[0]); oy = min(a[3], b[3]) - max(a[1], b[1])
            if ox > 0.4 and oy > 0.4: sup.append((ta[:28], tb[:28]))
    fuera = [t[:28] for (c, t) in cajas if c[0] < 15.2 or c[2] > 202.8 or c[1] < 7.2 or c[3] > 289.8]
    ext = bbox.extents(e for e in m if e.dxf.layer != "0-MARCO")
    print(f"{f.split('/')[-1]}: letra mín {hmin:.2f} | superpuestos {len(sup)} | fuera del marco {len(fuera)} | "
          f"contenido y {ext.extmin.y:.0f}..{ext.extmax.y:.0f}")
    for s in sup[:12]: print("    pisa:", s)
    for s in fuera[:6]: print("    fuera:", s)
