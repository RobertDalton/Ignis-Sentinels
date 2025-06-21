#Usa ijson para procesar por partes y convertir a GeoJSON sin cargar todo en memoria.
#Si necesitas todo el archivo, asegúrate de tener suficiente RAM o procesa por lotes.
import ijson
import json

from decimal import Decimal

input_path = r"D:\Games\_Import\Training_Courses\Microsoft\_Hackathon_Innovation_Challenge\03_Junio_2025\03_Wildfire_resilience\monitoreo_de_incendios_forestales\data\fire_nrt_SV-C2_626630.json"
output_path = r"D:\Games\_Import\Training_Courses\Microsoft\_Hackathon_Innovation_Challenge\03_Junio_2025\03_Wildfire_resilience\monitoreo_de_incendios_forestales\data\fire_nrt_SV-C2_626630_sample.geojson"
N = 150

#Debes convertir los decimales a float porque el formato JSON estándar no soporta el tipo de dato Decimal de Python.
#El módulo json de Python solo puede serializar tipos básicos como int, float, str, bool, list y dict.
#Convertir a float asegura que tus datos numéricos se guarden correctamente y sean compatibles con otras aplicaciones y librerías que usen JSON.
def convert_decimals(obj):
    if isinstance(obj, list):
        return [convert_decimals(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: convert_decimals(v) for k, v in obj.items()}
    elif isinstance(obj, Decimal):
        return float(obj)
    else:
        return obj

first_n = []
last_n = []

with open(input_path, 'r', encoding='utf-8') as f:
    items = ijson.items(f, 'item')
    #buffer mantiene los últimos N (va eliminando el más antiguo cuando supera N).
    buffer = []
    for item in items:
        item = convert_decimals(item)
        if len(first_n) < N:
            first_n.append(item)
        buffer.append(item)
        if len(buffer) > N:
            buffer.pop(0)
    last_n = buffer

#Al final, sample = first_n + last_n te da los primeros y últimos 20.
sample = first_n + last_n if len(first_n) == N and len(last_n) == N else first_n

features = [
    {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [item["longitude"], item["latitude"]],
        },
        "properties": {k: v for k, v in item.items() if k not in ["latitude", "longitude"]},
    }
    for item in sample
]

geojson = {
    "type": "FeatureCollection",
    "features": features,
}

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(geojson, f, ensure_ascii=False, indent=2)

print(f"Archivo reducido guardado como {output_path} con {len(features)} registros.")