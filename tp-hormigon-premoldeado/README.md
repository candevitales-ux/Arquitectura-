# TP Construcciones II – Hormigón premoldeado de grandes luces con cerramiento vidriado

## Entregables (`../entregables/`)
- `PDF_para_imprimir/` – Lámina 1 (corte integral 1:20, A3 vertical) y Lámina 2 (3 nudos en 3D, A3 apaisada). Imprimir al 100 %.
- `DWG_AutoCAD/`
  - `Lamina1_Corte_Integral_1-20.dwg` – corte completo en verdadera magnitud (1 unidad = 1 mm, sin interrupciones), capas por material,
    rayados AutoCAD (ANSI31, AR-CONC, AR-SAND, EARTH, GRAVEL, INSUL, ZIGZAG), cotas asociativas (estilo `CORTE_1-20`),
    niveles, eje, referencias numeradas, planilla de referencias y rótulo. Plotear a 1:20.
  - `Lamina2_Detalles_3D_Nudos.dwg` – los 3 nudos como sólidos MESH por material (Z arriba), con números de referencia y planillas.
    Usar `VSCURRENT` → Realista/Conceptual y `3DORBIT` para verlos.
  - `Lamina3_Detalles_Uniones_Corte_1-5.dwg` – detalles en corte (ventanas del mismo corte integral): columna–viga, vidrio–viga de entrepiso y vidrio–muro (panel). Plotear a 1:5.
  - `Lamina4_Detalles_Uniones_Isometrica.dwg` – los mismos 3 detalles de la Lámina 3 en isometría (MESH por material).
- `DXF_alternativo/` – mismos dibujos en DXF.

## Regenerar
```
npm install && pip install ezdxf
python3 src/lamina1.py && node render.js build/lamina1.html build/lamina1 portrait
node render.js src/lamina2.html build/lamina2 landscape build/lamina2_3d.json
python3 src/lamina3.py && node render.js build/lamina3.html build/lamina3 landscape && python3 src/dxf_lamina3.py
node render.js src/lamina4.html build/lamina4 landscape build/lamina4_3d.json
python3 src/dxf_detalles3d.py build/lamina4_3d.json build/dwg_in/Lamina4_Detalles_Uniones_Isometrica.dxf "LAMINA 4"
python3 src/dxf_lamina1.py && python3 src/dxf_detalles3d.py
xvfb-run -a ODAFileConverter build/dwg_in build/dwg_out ACAD2018 DWG 0 1 "*.DXF"
```
