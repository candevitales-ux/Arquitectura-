# -*- coding: utf-8 -*-
"""Exporta los tres nudos 3D (Lámina 2) a DXF como entidades MESH por material,
en verdadera magnitud (mm), Z hacia arriba. Incluye números de referencia y planillas."""
import json, sys, ezdxf
from ezdxf.enums import TextEntityAlignment

IN = sys.argv[1] if len(sys.argv) > 1 else "build/lamina2_3d.json"
OUT = sys.argv[2] if len(sys.argv) > 2 else "build/dwg_in/Lamina2_Detalles_3D_Nudos.dxf"
TITLE = sys.argv[3] if len(sys.argv) > 3 else "LAMINA 2 - DETALLES 3D DE NUDOS - Hormigon premoldeado de grandes luces con muro cortina (mm, verdadera magnitud, Z arriba)"
D = json.load(open(IN))
doc = ezdxf.new("R2018", setup=True)
doc.units = ezdxf.units.MM
doc.styles.add("ARIAL", font="arial.ttf")
msp = doc.modelspace()

NAMES = {"pre": "H-PREMOLDEADO", "insitu": "H-INSITU", "hs": "H-SIMPLE", "mort": "MORTERO-CARPETAS", "hid": "CARPETA-HIDROFUGA",
         "grout": "GROUT", "eps": "AISLACION-EPS", "lana": "AISLACION-LANA-MINERAL", "tosca": "TOSCA", "tierra": "TERRENO",
         "glass": "VIDRIO", "spandrel": "VIDRIO-SPANDREL", "alu": "ALUMINIO", "alu2": "ALUMINIO-TAPAS", "steel": "ACERO",
         "galv": "ACERO-GALVANIZADO", "neo": "NEOPRENO", "memb": "MEMBRANA", "porc": "PORCELANATO", "yeso": "CIELORRASO-YESO",
         "film": "BARRERA-VAPOR-FILM", "red": "ARMADURAS", "seal": "SELLADORES", "intum": "SELLADOR-INTUMESCENTE"}

def rgb(h):
    h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

for k, n in NAMES.items():
    pass
made = set()
def layer(key, color):
    name = "3D-" + NAMES.get(key, key.upper())
    if name not in made:
        l = doc.layers.add(name); l.rgb = rgb(color)
        if key == "glass": l.transparency = 0.6
        made.add(name)
    return name
for nm in ("3D-REFERENCIAS", "3D-TEXTOS"):
    doc.layers.add(nm, color=1 if "REF" in nm else 7)

DX = 4200   # separación entre detalles
for i, det in enumerate(D):
    ox = i * DX
    ymin = min(v[1] for m in det["meshes"] for v in m["V"])
    to = lambda p: (p[0] + ox, -p[2], p[1] - ymin)   # three (x, y, z) -> CAD (X, Y, Z), Z arriba, apoyado en Z = 0
    for m in det["meshes"]:
        lay = layer(m["key"], m["color"])
        mesh = msp.add_mesh(dxfattribs={"layer": lay})
        with mesh.edit_data() as md:
            md.vertices = [to(v) for v in m["V"]]
            md.faces = m["F"]
    # referencias: número junto a cada ancla + línea guía vertical corta
    for a in det["anchors"]:
        p = to(a["p"]); q = (p[0] - 120, p[1] + 120, p[2] + 160)
        msp.add_line(p, q, dxfattribs={"layer": "3D-REFERENCIAS"})
        t = msp.add_text(str(a["n"]), height=45, dxfattribs={"layer": "3D-REFERENCIAS", "style": "ARIAL"})
        t.set_placement(q, align=TextEntityAlignment.BOTTOM_LEFT)
    # título y planilla en el plano del suelo, delante del detalle
    base_z = 0
    t = msp.add_text(det["t"].replace("·", "-"), height=90, dxfattribs={"layer": "3D-TEXTOS", "style": "ARIAL"})
    t.set_placement((ox - 600, -350, base_z))
    txt = r"\P".join(f"{k + 1}. {s}" for k, s in enumerate(det["refs"]))
    mt = msp.add_mtext(det["st"] + r"\P\P" + txt, dxfattribs={"layer": "3D-TEXTOS", "char_height": 32, "style": "ARIAL", "width": 3400})
    mt.set_location((ox - 600, -500, base_z))

t = msp.add_text(TITLE,
                 height=110, dxfattribs={"layer": "3D-TEXTOS", "style": "ARIAL"})
t.set_placement((-600, -100, 2600))
vp = doc.viewports.get("*Active")[0]
vp.dxf.direction = (1, -1.2, 0.9)
vp.dxf.target = (DX, 0, 800)
vp.dxf.height = 12000
vp.dxf.center = (0, 0)
doc.saveas(OUT)
print("ok")
