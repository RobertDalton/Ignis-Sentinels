import json

input_path = r"D:\Games\_Import\Training_Courses\Microsoft\_Hackathon_Innovation_Challenge\03_Junio_2025\03_Wildfire_resilience\monitoreo_de_incendios_forestales\data\fire_nrt_M-C61_626627.geojson"
output_path = r"D:\Games\_Import\Training_Courses\Microsoft\_Hackathon_Innovation_Challenge\03_Junio_2025\03_Wildfire_resilience\monitoreo_de_incendios_forestales\data\fire_nrt_M-C61_626627.geojson"

with open(input_path, "r", encoding="utf-8") as f:
    data = json.load(f)

features = data["features"]
sampled = features[:150] + features[-150:] if len(features) >= 300 else features

sample_geojson = {
    "type": "FeatureCollection",
    "features": sampled
}

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(sample_geojson, f, ensure_ascii=False, indent=2)

print(f"Archivo reducido guardado como {output_path} con {len(sampled)} registros.")