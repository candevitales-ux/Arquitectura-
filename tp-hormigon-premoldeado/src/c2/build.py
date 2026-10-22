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


LAYERS = {"MARCO": 7, "CONTORNOS": 7, "LINEAS": 7, "TEXTOS": 7, "REFERENCIAS": 7, "COTAS": 7, "TABLAS": 7, "ISO": 7, "ARMADURAS": 14}


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


def main():
    pages = all_pages()
    total = len(pages)
    sel = [int(a) for a in sys.argv[1:]] or list(range(1, total + 1))
    shutil.rmtree(os.path.join(B, "dwg_in"), ignore_errors=True)
    os.makedirs(B, exist_ok=True); os.makedirs(os.path.join(B, "dwg_in"), exist_ok=True)
    sheets = {}
    for i in sel:
        sh = pages[i - 1](i, total)
        sh.frame()
        sheets[i] = sh
        print("lámina", i, sh.fname, len(sh.ops), "entidades")
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
    shutil.rmtree(OUT, ignore_errors=True)
    for d in ("PDF", "DWG", "DXF", "vistas_previas"): os.makedirs(os.path.join(OUT, d))
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
    print("publicado en", OUT)


if __name__ == "__main__":
    main()
