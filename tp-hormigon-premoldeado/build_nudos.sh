#!/bin/sh
# Práctica en clase NUDOS: láminas A4 (PDF) + DWG por lámina.
# Uso: sh build_nudos.sh            (hormigón premoldeado)
#      SISTEMA=acero sh build_nudos.sh   (estructura de acero)
set -e
cd "$(dirname "$0")"
if [ "${SISTEMA:-hormigon}" = "acero" ]; then B="$PWD/build/nudos_acero"; else B="$PWD/build/nudos"; fi
python3 src/nudos_a4.py
/opt/pw-browsers/chromium-1194/chrome-linux/chrome --headless=new --no-sandbox --disable-gpu --no-pdf-header-footer \
  --virtual-time-budget=20000 --print-to-pdf="$B/Nudos_A4.pdf" "file://$B/Nudos_A4.html" 2>/dev/null
mkdir -p "$B/png" "$B/dwg"
pdftoppm -r 110 -png "$B/Nudos_A4.pdf" "$B/png/p"
xvfb-run -a ODAFileConverter "$B/dxf" "$B/dwg" ACAD2018 DWG 0 1 "*.dxf" >/dev/null 2>&1 || true
ls "$B/dwg" | wc -l
