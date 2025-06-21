
import requests
from typing import Any, Callable, Set, Dict, List, Optional
import json
import os
from azure.storage.blob import BlobServiceClient, ContainerClient, BlobClient
from dotenv import load_dotenv
load_dotenv()

def get_weather_by_location(location):
    """
    Fetches the weather information for the specified location.

    :param location (str): The location to fetch weather for.
    :return: Weather information as a string of characters.
    :rtype: str
    """
    
    api_key = os.getenv("WEATHER_KEY")
    url = "http://api.openweathermap.org/geo/1.0/direct?q=" + location + f"&limit=1&appid={api_key}"
    response=requests.get(url)
    get_response=response.json()
    latitude=get_response[0]['lat']
    longitude = get_response[0]['lon']

    url_final = "https://api.openweathermap.org/data/2.5/weather?lat=" + str(latitude) + "&lon=" + str(longitude) + "&appid=YOUR_API_KEY"
    final_response = requests.get(url_final)
    final_response_json = final_response.json()
    weather=final_response_json['weather'][0]['description']
    return weather

def get_weather_by_coordenates(latitude:float,longitude:float):
    """
    Fetches the weather information for the specified location.

    :param location (str): The location to fetch weather for.
    :return: Weather information as a string of characters.
    :rtype: str
    """
    
    api_key = os.getenv("WEATHER_KEY")

    url_final = "https://api.openweathermap.org/data/2.5/weather?lat=" + str(latitude) + "&lon=" + str(longitude) + f"&appid={api_key}"
    final_response = requests.get(url_final)
    final_response_json = final_response.json()
    weather=final_response_json['weather'][0]['description']
    return weather

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

user_functions: Set[Callable[..., Any]] = {
    get_weather_by_location,
    get_weather_by_coordenates,
    upload_json_to_blob_storage
}