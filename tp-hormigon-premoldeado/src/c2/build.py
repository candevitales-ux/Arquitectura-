# -*- coding: utf-8 -*-
"""Genera las láminas A4 de la práctica C2: PDF (único + por lámina), DXF y DWG (por lámina + conjunto).
uso:  python3 src/c2/build.py [n ...]   (sin argumentos: todas)"""
import os, sys, subprocess, shutil, importlib, glob
sys.path.insert(0, os.path.dirname(__file__))
import ezdxf
from lib import W, H

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
B = os.path.join(ROOT, "build", "c2")
OUT = os.path.abspath(os.path.join(ROOT, "..", "entregables", "C2_PRACTICA_HORMIGON_A4"))
MODS = ["s01_caratula", "s02_fundacion_columna", "s03_vigas", "s04_panel_tt", "s05_juntas_ubicacion", "s06_juntas_estructura",
        "s07_juntas_cerramientos", "s08_maquinas_montaje", "s09_maquinas_moldeo_anclaje", "s10_planificacion",
        "s11_muro_cortina", "s12_opaco", "s13_comparacion"]


def all_pages():
    """cada módulo expone PAGES = [funciones (num, total) -> Sheet]; la numeración es correlativa"""
    out = []
    for m in MODS:
        out += getattr(importlib.import_module(m), "PAGES", [])
    return out


LAYERS = {"ESTUDIO": 7, "MARCO": 7, "CONTORNOS": 7, "LINEAS": 7, "TEXTOS": 7, "REFERENCIAS": 7, "COTAS": 7, "TABLAS": 7, "ISO": 7, "ARMADURAS": 14}


def new_doc():
    doc = ezdxf.new("R2018", setup=True); doc.units = ezdxf.units.MM
    doc.styles.add("ARIAL", font="arial.ttf"); doc.styles.add("ARIAL-NEGRITA", font="arialbd.ttf"); doc.styles.add("ARIAL-CURSIVA", font="ariali.ttf")
    for n, c in LAYERS.items():
        doc.layers.add(n, color=c); doc.layers.add(n + "-RELLENO", color=9); doc.layers.add(n + "-RAYADO", color=8)
    return doc


def layout_a4(doc, name, cx):
    lay = doc.layouts.new(name)
    lay.page_setup(size=(W, H), margins=(0, 0, 0, 0), units="mm", scale=(1, 1))
    lay.add_viewport(center=(W / 2, H / 2), size=(W, H), view_center_point=(cx, H / 2), view_height=H)
    if "Layout1" in doc.layouts: doc.layouts.delete("Layout1")


FACTORS = (1.3, 1.25, 1.2, 1.15, 1.1, 1.05)


def make_sheet(fn, i, total, f):
    import lib, estudio
    lib.FLOW = f
    try:
        sh = fn(i, total)
        if sh.fname in estudio.NOTAS: sh.estudiar(estudio.NOTAS[sh.fname])
    finally:
        lib.FLOW = 1.0
    return sh


def geoms(sh):
    """(es_flow, capa, geometría) de cada primitiva en papel; textos como rectángulo aproximado"""
    from shapely.geometry import box, LineString, Polygon, Point
    from lib import CW
    out = []
    for o in sh.ops:
        if o["layer"] == "MARCO": continue
        if o["t"] == "text":
            if o["rot"]: continue
            x, y = o["p"]; w = len(o["s"]) * o["size"] * CW * (1.05 if o["bold"] else 1.0); h = o["size"] * 0.72
            x0 = x - (w / 2 if o["anchor"] == "middle" else (w if o["anchor"] == "end" else 0))
            g = box(x0, y - h, x0 + w, y + 0.15 * o["size"]); kind = "T"
        elif o["t"] == "circ":
            g = Point(o["c"]).buffer(o["r"], 8); kind = "C"
        else:
            if len(o["pts"]) < 2: continue
            g = Polygon(o["pts"]).buffer(0) if (o["closed"] and len(o["pts"]) >= 3) else LineString(o["pts"])
            if o["closed"] and (o["bg"] or o["hat"]) and len(o["pts"]) >= 3: kind = "F"     # relleno
            else: g = g.boundary if g.geom_type == "Polygon" else g; kind = "L"
        out.append((o.get("flow", False), o["layer"], kind, g))
    return out


def score(sh):
    """choques del texto corrido con todo lo que no es texto corrido + desbordes de página"""
    from shapely.strtree import STRtree
    from lib import W, H
    G = geoms(sh)
    flow = [g for g in G if g[0] and g[2] == "T"]
    other = [g for g in G if not g[0]]
    hits = 0
    if other:
        tree = STRtree([g[3] for g in other])
        for _, _, _, t in flow:
            tt = t.buffer(-0.25)
            for j in tree.query(tt):
                if other[int(j)][3].intersects(tt): hits += 1
    T = [g[3].buffer(-0.2) for g in G if g[2] == "T"]
    if T:
        tt = STRtree(T)
        for k, t in enumerate(T):
            for j in tt.query(t):
                if int(j) > k and T[int(j)].intersects(t): hits += 1
    out = sum(1 for g in G if g[3].bounds[2] > W - 7 or g[3].bounds[3] > H - 10.5 or g[3].bounds[0] < 7)
    estudio = any(o["layer"] == "ESTUDIO" for o in sh.ops)
    return hits, out, estudio


def best_sheet(fn, i, total):
    base = make_sheet(fn, i, total, 1.0)
    h0, o0, e0 = score(base)
    for f in FACTORS:
        sh = make_sheet(fn, i, total, f)
        h, o, e = score(sh)
        if h <= h0 and o <= o0 and (e or not e0):
            sh.flow = f
            return sh
    base.flow = 1.0
    return base


def main():
    pages = all_pages()
    total = len(pages)
    sel = [int(a) for a in sys.argv[1:]] or list(range(1, total + 1))
    shutil.rmtree(os.path.join(B, "dwg_in"), ignore_errors=True)
    os.makedirs(B, exist_ok=True); os.makedirs(os.path.join(B, "dwg_in"), exist_ok=True)
    sheets = {}
    for i in sel:
        sh = best_sheet(pages[i - 1], i, total)
        sh.frame()
        sheets[i] = sh
        print("lámina", i, sh.fname, "texto x", sh.flow)
    # ---- HTML -> PDF
    pages = "".join(f'<div class="pg" id="pg{k + 1}">{sheets[i].svg_doc()}</div>' for k, i in enumerate(sel))
    html = ('<!doctype html><html><head><meta charset="utf-8"><style>@page{size:210mm 297mm;margin:0}html,body{margin:0;padding:0}'
            '.pg{width:210mm;height:297mm;page-break-after:always;overflow:hidden}.pg svg{display:block}</style></head><body>' + pages + '</body></html>')
    hp = os.path.join(B, "laminas.html"); open(hp, "w", encoding="utf-8").write(html)
    pdf = os.path.join(B, "laminas.pdf")
    subprocess.run(["node", os.path.join(ROOT, "src", "c2", "render_a4.js"), hp, pdf, os.path.join(B, "lam"), str(len(sel))], check=True, cwd=ROOT)
    # ---- DXF por lámina + conjunto
    allg = new_doc()
    for k, i in enumerate(sel):
        doc = new_doc(); sheets[i].to_dxf(doc.modelspace()); layout_a4(doc, f"LAMINA {i:02d}", W / 2)
        doc.saveas(os.path.join(B, "dwg_in", f"L{i:02d}_{sheets[i].fname}.dxf"))
        dx = (i - 1) * (W + 30)
        sheets[i].to_dxf(allg.modelspace(), dx=dx); layout_a4(allg, f"LAMINA {i:02d}", dx + W / 2)
    if not sys.argv[1:]:
        allg.saveas(os.path.join(B, "dwg_in", "C2_PRACTICA_HORMIGON_A4_CONJUNTO.dxf"))
    if not sys.argv[1:]:
        publish(sel, sheets)


def publish(sel, sheets):
    dwg_out = os.path.join(B, "dwg_out"); shutil.rmtree(dwg_out, ignore_errors=True); os.makedirs(dwg_out)
    subprocess.run(["xvfb-run", "-a", "ODAFileConverter", os.path.join(B, "dwg_in"), dwg_out, "ACAD2018", "DWG", "0", "1", "*.DXF"], check=True)
    leeme = os.path.join(OUT, "LEEME.txt"); txt = open(leeme, encoding="utf-8").read() if os.path.exists(leeme) else None
    shutil.rmtree(OUT, ignore_errors=True)
    for d in ("PDF", "DWG", "DXF", "vistas_previas"): os.makedirs(os.path.join(OUT, d))
    if txt: open(leeme, "w", encoding="utf-8").write(txt)
    shutil.copy(os.path.join(B, "laminas.pdf"), os.path.join(OUT, "C2_PRACTICA_HORMIGON_A4_COMPLETA.pdf"))
    for k, i in enumerate(sel):
        nm = f"L{i:02d}_{sheets[i].fname}"
        subprocess.run(["pdfseparate", "-f", str(k + 1), "-l", str(k + 1), os.path.join(B, "laminas.pdf"), os.path.join(OUT, "PDF", nm + ".pdf")], check=True)
        shutil.copy(os.path.join(B, f"lam{k + 1:02d}.png"), os.path.join(OUT, "vistas_previas", nm + ".png"))
    for fpath in glob.glob(os.path.join(dwg_out, "*.dwg")):
        shutil.copy(fpath, os.path.join(OUT, "DWG"))
    for fpath in glob.glob(os.path.join(B, "dwg_in", "*.dxf")):
        shutil.copy(fpath, os.path.join(OUT, "DXF"))
    shutil.move(os.path.join(OUT, "DWG", "C2_PRACTICA_HORMIGON_A4_CONJUNTO.dwg"), os.path.join(OUT, "C2_PRACTICA_HORMIGON_A4_CONJUNTO.dwg"))
    print("publicado en", OUT)  # (LEEME.txt se mantiene aparte en el repo)


if __name__ == "__main__":
    main()
