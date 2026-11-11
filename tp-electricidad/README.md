# TP Instalaciones – Electricidad: esquema unifilar (edificio PB + 4 pisos)

Lámina A3 apaisada `../entregables/TP_ELECTRICIDAD_UNIFILAR_A3/`:
- `ESQUEMA_UNIFILAR_A3.pdf` – imprimir al 100 % en A3 apaisado.
- `ESQUEMA_UNIFILAR_A3.dxf` – la misma lámina en mm de papel (1:1), capas por sistema (acometida, deptos, servicios generales, PE, palier, tableros, textos). Abre en AutoCAD (guardar como DWG).

Contenido: 1) esquema de montantes (corte esquemático), 2) unifilar general acometida → CT → barra → medidores → TP-PB…TP-4° y TPSG,
3) TS típico de departamento con planilla de circuitos, 4) seccionales TSG, TB, TA, TR. Leyenda de símbolos, abreviaturas, notas y rótulo.

## Regenerar
```
pip install ezdxf
python3 src/unifilar.py && node render.js build/unifilar.html build/ESQUEMA_UNIFILAR_A3
```
