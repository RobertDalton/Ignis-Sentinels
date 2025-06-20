import json

def convert_to_geojson(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    features = []
    for item in data:
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [item["longitude"], item["latitude"]]
            },
            "properties": {k: v for k, v in item.items() if k not in ["latitude", "longitude"]}
        })

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(geojson, f, ensure_ascii=False, indent=2)

# Ejemplo de uso:
convert_to_geojson(
    "D:/Games/_Import/Training_Courses/Microsoft/_Hackathon_Innovation_Challenge/03_Junio_2025/03_Wildfire_resilience/monitoreo_de_incendios_forestales/data/fire_archive_SV-C2_626630.json",
    "D:/Games/_Import/Training_Courses/Microsoft/_Hackathon_Innovation_Challenge/03_Junio_2025/03_Wildfire_resilience/monitoreo_de_incendios_forestales/data/fire_archive_SV-C2_626630.geojson"
)