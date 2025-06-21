from pydantic import BaseModel


class ActivePoints(BaseModel):
    id: str
    location_name: str
    location_coordinates: dict
