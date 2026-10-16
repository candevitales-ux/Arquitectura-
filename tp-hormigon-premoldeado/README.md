# TP Construcciones II – Hormigón premoldeado de grandes luces con cerramiento vidriado

Entregables (A3, listos para imprimir al 100 %): carpeta `../entregables/`.

- **Lámina 1** – Corte integral esc. 1:20 (portrait A3) con 67 referencias numeradas, niveles, cotas y convenciones.
- **Lámina 2** – Tres detalles de nudos en axonometría 3D (cubierta, entrepiso, piso sobre terreno).

## Regenerar
```
npm install
python3 src/lamina1.py && node render.js build/lamina1.html build/lamina1 portrait
node render.js src/lamina2.html build/lamina2 landscape
```
