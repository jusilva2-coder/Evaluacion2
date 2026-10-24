# Evaluacion2

Planificador de rutas en Python que usa la API de GraphHopper.

## Descripción
El script pide un tipo de vehículo, un origen y un destino, y muestra la
distancia, la duración y la narrativa del viaje en español. Las cantidades
se muestran con máximo dos decimales. Para terminar, escribe "s" o "salir".

## Requisitos
- Python 3
- Librería requests (`pip3 install requests`)
- Un token (API key) de GraphHopper

## Cómo ejecutar
1. Define tu token en la terminal:
   `export GRAPHHOPPER_KEY="tu_token"`
2. Ejecuta el script:
   `python3 graphhopper_es.py`