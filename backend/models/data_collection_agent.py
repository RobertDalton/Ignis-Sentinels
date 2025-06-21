from pydantic import BaseModel
from typing import Dict

class DataCollectionAgent(BaseModel):
    wildfire_id: int
    location_name: str
    weather_conditions: Dict[str, str]
    location_coordinates: Dict[str, float]
    location_details: Dict[str, float]
    satellite_wildfire_image: str
    vegetation_distribution: str
