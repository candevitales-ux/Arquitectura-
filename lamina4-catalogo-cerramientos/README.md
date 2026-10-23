# Lámina 4 – Catálogo de cerramientos (opacos / vidriados)

Opaco: panel sándwich metálico 80 mm (ref. 24 del corte integral de acero).
Todo se dibuja en un DXF en mm de papel (A3 vertical 297x420, escala 1:1 de la hoja); de ahí salen el PDF y el DWG.

```
pip install ezdxf pymupdf
python3 src/computo_plantilla.py build   # plantilla en blanco (entrega actual)
python3 src/computo_opaco.py build      # cómputo completado con edificio estándar
python3 src/lamina4_catalogo.py build    # LÁMINA FINAL: vidriado + opaco en una hoja
python3 src/armar_a4.py && python3 src/lamina4_a4.py build vidriado && python3 src/lamina4_a4.py build opaco   # 2 hojas A4
python3 src/dxf2pdf.py build/Lamina4_Catalogo_Vidriado_A4.dxf build/a4_vidriado.pdf build/a4_vidriado.png A4
python3 src/catalogo_vidriado.py build   # catálogo: vidriado (muro cortina)
python3 src/catalogo_opaco.py build     # catálogo: opaco (panel sándwich)
python3 src/dxf2pdf.py build/Lamina4_Catalogo_Opaco_A3.dxf build/l4.pdf build/l4.png
mkdir -p build/dwg_in build/dwg_out && cp build/*.dxf build/dwg_in/
xvfb-run -a ODAFileConverter "$PWD/build/dwg_in" "$PWD/build/dwg_out" ACAD2018 DWG 0 1 "*.DXF"
```
