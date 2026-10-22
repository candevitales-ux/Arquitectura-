#!/bin/bash
# Genera las 15 láminas A4: DXF (mm de papel, hoja 1:1) -> PDF + PNG + DWG, y un PDF único.
set -e
cd "$(dirname "$0")"
export OUT="$PWD/build"
mkdir -p build/dwg_in build/dwg_out
cd src
for f in l01 l02 l03 l04 l05 l06 l07 l08 l09 l10 l11 l12 l13 l14 l15; do python3 $f.py; done
for d in ../build/L*_*.dxf; do
  n=$(basename "$d" .dxf)
  python3 dxf2pdf.py "$d" "../build/$n.pdf" -
  pdftoppm -r 110 -png -singlefile "../build/$n.pdf" "../build/$n"
  cp "$d" ../build/dwg_in/
done
cd ..
python3 -c "
import pymupdf, glob
out = pymupdf.open()
for f in sorted(glob.glob('build/L??_*.pdf')): out.insert_pdf(pymupdf.open(f))
out.save('build/Practica_Acero_C2_A4_completa.pdf')"
xvfb-run -a ODAFileConverter "$PWD/build/dwg_in" "$PWD/build/dwg_out" ACAD2018 DWG 0 1 "*.DXF"
ls build/dwg_out
