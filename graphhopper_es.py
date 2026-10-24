import os
import requests
import urllib.parse

ruta_url = "https://graphhopper.com/api/1/route?"
geocode_url = "https://graphhopper.com/api/1/geocode?"
clave = os.environ.get("GRAPHHOPPER_KEY", "")

if not clave:
    print("Falta el token. Defínelo en la terminal con:")
    print('export GRAPHHOPPER_KEY="tu_token_aqui"')
    raise SystemExit

def salir(texto):
    return texto.strip().lower() in ("s", "salir")

def geocodificar(lugar):
    url = geocode_url + urllib.parse.urlencode({"q": lugar, "limit": "1", "key": clave})
    r = requests.get(url)
    datos = r.json()
    if r.status_code == 200 and datos.get("hits"):
        p = datos["hits"][0]["point"]
        return p["lat"], p["lng"], datos["hits"][0].get("name", lugar)
    print("No se pudo ubicar:", lugar, "| Estado:", r.status_code)
    return None, None, lugar

print("Planificador de rutas (escribe 's' o 'salir' para terminar)")
while True:
    perfil = input("\nVehículo (auto, bici, a pie) o 's' para salir: ")
    if salir(perfil):
        break
    vehiculo = {"auto": "car", "bici": "bike", "a pie": "foot"}.get(perfil.lower(), "car")

    origen = input("Ciudad o lugar de origen: ")
    if salir(origen):
        break
    destino = input("Ciudad o lugar de destino: ")
    if salir(destino):
        break

    lat1, lon1, nom1 = geocodificar(origen)
    lat2, lon2, nom2 = geocodificar(destino)
    if lat1 is None or lat2 is None:
        continue

    url = ruta_url + urllib.parse.urlencode({"key": clave, "vehicle": vehiculo, "locale": "es"})
    url += f"&point={lat1},{lon1}&point={lat2},{lon2}"
    r = requests.get(url)
    datos = r.json()

    if r.status_code != 200:
        print("Error al obtener la ruta:", datos.get("message", r.status_code))
        continue

    camino = datos["paths"][0]
    km = camino["distance"] / 1000
    millas = km / 1.609344
    seg = camino["time"] / 1000
    h, m, s = int(seg // 3600), int((seg % 3600) // 60), seg % 60

    print("\n=================================================")
    print(f"Ruta de {nom1} a {nom2} en {perfil}")
    print(f"Distancia: {km:.2f} km ({millas:.2f} millas)")
    print(f"Duración: {h:02d}:{m:02d}:{s:05.2f}")
    print("=================================================")
    print("Narrativa del viaje:")
    for paso in camino["instructions"]:
        print(f"- {paso['text']} ({paso['distance'] / 1000:.2f} km)")
    print("=================================================")