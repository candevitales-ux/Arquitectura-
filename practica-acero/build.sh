#!/bin/bash
# Genera las 15 láminas A4 (sin rótulo, letra mín. 2 mm): DXF (mm de papel, hoja 1:1) -> PDF + PNG + DWG, y un PDF único.
set -e
cd "$(dirname "$0")"
B="$PWD/build/v15"
export OUT="$B"
mkdir -p "$B/dwg_in" "$B/dwg_out"
cd src
for f in l01 l02 l03 l04 l05 l06 l07 l08 l09 l10 l11 l12 l13 l14 l15; do python3 $f.py; done
for d in "$B"/L*_*.dxf; do
  n=$(basename "$d" .dxf)
  python3 dxf2pdf.py "$d" "$B/$n.pdf" -
  pdftoppm -r 110 -png -singlefile "$B/$n.pdf" "$B/$n"
  cp "$d" "$B/dwg_in/"
done
cd ..
python3 -c "
import pymupdf, glob, sys
out = pymupdf.open()
for f in sorted(glob.glob(sys.argv[1] + '/L??_*.pdf')): out.insert_pdf(pymupdf.open(f))
out.save(sys.argv[1] + '/Practica_Acero_C2_A4_completa.pdf')" "$B"
xvfb-run -a ODAFileConverter "$B/dwg_in" "$B/dwg_out" ACAD2018 DWG 0 1 "*.DXF"
ls "$B/dwg_out"
