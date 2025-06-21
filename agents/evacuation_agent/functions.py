import agentpy as ap
from azure.storage.blob import BlobServiceClient, ContainerClient, BlobClient
import matplotlib.pyplot as plt
import json
import folium

def generate_folium_map_from_coordinates(
    lat1: float, lon1: float,
    lat2: float, lon2: float,
    map_zoom_start: int = 4
):
    center_lat = (lat1 + lat2) / 2
    center_lon = (lon1 + lon2) / 2

    # Crear un objeto de mapa de Folium
    m = folium.Map(location=[center_lat, center_lon], zoom_start=map_zoom_start)

    # Añadir un marcador para el primer punto
    folium.Marker(
        location=[lat1, lon1],
        popup=f"Coordenada 1: ({lat1:.2f}, {lon1:.2f})",
        icon=folium.Icon(color="red")
    ).add_to(m)

    # Añadir un marcador para el segundo punto
    folium.Marker(
        location=[lat2, lon2],
        popup=f"Coordenada 2: ({lat2:.2f}, {lon2:.2f})",
        icon=folium.Icon(color="blue")
    ).add_to(m)

    # Añadir una línea entre los dos puntos
    folium.PolyLine(
        locations=[[lat1, lon1], [lat2, lon2]],
        color="green",
        weight=2.5,
        opacity=1
    ).add_to(m)

    return m



def upload_json_to_blob_storage(
    json_data: dict,
    blob_name: str,
    connection_string: str = None,
    container_name: str = "container-name"
) -> str:

    if connection_string is None:
        connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        if not connection_string:
            raise ValueError
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        container_client = blob_service_client.get_container_client(container_name)

        try:
            container_client.create_container()
            print(f"Contenedor '{container_name}' creado (si no existía).")
        except Exception as e:
            if "ContainerAlreadyExists" not in str(e):
                print(f"Advertencia al crear el contenedor (posiblemente ya existe): {e}")

        blob_client = container_client.get_blob_client(blob_name)

        json_string = json.dumps(json_data, indent=4) # indent=4 para una salida JSON legible

        blob_client.upload_blob(json_string, overwrite=True) # overwrite=True para reemplazar si ya existe


        return blob_client.url

    except Exception as e:
        print(f"Error al subir el JSON a Blob Storage: {e}")
        return ""