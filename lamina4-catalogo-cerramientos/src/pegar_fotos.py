# -*- coding: utf-8 -*-
"""Inserta en el PDF las fotos de las fichas (recuadros en mm de papel, origen abajo a la izquierda)."""
import sys, json, pymupdf
pdf, rects, carpeta = sys.argv[1:4]
doc = pymupdf.open(pdf); p = doc[0]; k = 72 / 25.4; H = p.rect.height
for cod, (x0, y0, x1, y1) in json.load(open(rects)).items():
    p.insert_image(pymupdf.Rect(x0 * k, H - y1 * k, x1 * k, H - y0 * k), filename=f"{carpeta}/{cod}.jpg", keep_proportion=False)
doc.save(pdf, incremental=True, encryption=0)
print("fotos ok", len(json.load(open(rects))))
