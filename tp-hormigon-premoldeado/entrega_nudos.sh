#!/bin/sh
# Copia las láminas generadas por build_nudos.sh a ../entregables.  Uso: sh entrega_nudos.sh hormigon|acero
set -e
cd "$(dirname "$0")"
if [ "$1" = "acero" ]; then B=build/nudos_acero; E=../entregables/PRACTICA_NUDOS_ACERO_A4; N=PRACTICA_NUDOS_ACERO_A4
else B=build/nudos; E=../entregables/PRACTICA_NUDOS_A4; N=PRACTICA_NUDOS_A4; fi
mkdir -p $E/DWG_AutoCAD $E/DXF_alternativo $E/PDF_por_lamina $E/vistas_previas
cp $B/Nudos_A4.pdf $E/${N}_completa.pdf
cp $B/dwg/*.dwg $E/DWG_AutoCAD/; cp $B/dxf/*.dxf $E/DXF_alternativo/
for f in $B/dxf/*.dxf; do n=$(basename $f .dxf); p=$(echo $n | cut -c8-9 | sed 's/^0//')
  pdfseparate -f $p -l $p $B/Nudos_A4.pdf "$E/PDF_por_lamina/$n.pdf"
  case "$n" in *planilla*) ;; *) cp $B/png/p-$(echo $n | cut -c8-9).png $E/vistas_previas/Lamina_$(echo $n | cut -c8-9).png ;; esac
done
