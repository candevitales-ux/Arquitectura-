#!/bin/bash
# prev.sh NAME : dxf -> pdf + png (pdftoppm)
set -e
cd "$(dirname "$0")"
python3 dxf2pdf.py ../build/$1.dxf ../build/$1.pdf - 
pdftoppm -r ${2:-110} -png -singlefile ../build/$1.pdf ../build/$1
