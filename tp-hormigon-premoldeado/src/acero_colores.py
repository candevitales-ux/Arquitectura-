HA, TIERRA, CONTRA, MORT, PORC = "#d3d6d9", "#ece3d2", "#e6e4df", "#e9e9e9", "#cdbb9c"
EPS, PUR, ACERO, VIDRIO, YESO = "#fff5bf", "#fbe2a8", "#b9c6d4", "#cfe6f2", "#f1ebe2"
XL, XR = 42.2, 152.9
WALLS = [(XL, 28, XL, 362), (XR, 28, XR, 362)]
BIG_MM2 = 1500
MAT = [
 ("flood", TIERRA, [(60, 320), (140, 320)], [(XL, 270, XR, 362)]),
 # fundación (cabezal, tronco y base): lo que queda dentro del contorno, después del terreno
 ("rest", HA, [(90.4, 273.5, 114.7, 294.3), (91.4, 294.0, 113.9, 329.0), (52.5, 328.3, 152.6, 358.6)], 1e9),
 # piso planta baja: interior (izq.) y exterior (der.)
 ("rest", CONTRA, [(XL, 274.9, 90.5, 277.7), (114.6, 277.7, XR, 280.2)]),
 ("rest", MORT, [(XL, 273.8, 90.5, 274.9), (114.6, 277.2, XR, 277.7)]),
 # losas steel deck (H°A°)
 ("rest", HA, [(XL, 56.6, 105.7, 60.4), (XL, 165.6, 105.7, 169.6)]),
 # contrapisos livianos EPS (cubierta y entrepiso) y carpeta/solado del entrepiso
 ("rest", EPS, [(XL, 50.0, 98.0, 56.6), (XL, 162.4, 105.7, 165.6)]),
 ("rest", MORT, [(XL, 160.8, 105.7, 162.4)]),
 # columna HEB (hasta la cupertina) y vigas en vista bajo las losas (acero)
 ("rest", ACERO, [(97.8, 40.0, 105.6, 273.5), (XL, 60.4, 97.8, 66.9), (XL, 169.6, 97.8, 176.0)]),
 # cielorrasos de roca de yeso
 ("rest", YESO, [(XL, 83.3, 97.8, 85.1), (XL, 192.2, 97.8, 194.0)]),
 # panel sándwich PUR y vidrio
 ("rest", VIDRIO, [(107.55, 86.0, 108.8, 139.0), (107.55, 194.0, 108.8, 246.3)]),
 ("rest", PUR, [(107.9, 36.0, 110.1, 272.0)]),
 # cupertina: aislación EPS
 ("rest", EPS, [(97.5, 38.2, 110.6, 40.4)]),
]
