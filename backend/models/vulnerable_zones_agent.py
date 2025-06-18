from pydantic import BaseModel
from typing import List

class VulnerableZonesAgent(BaseModel):
    id: str
    vulnerable_zones: List[dict]
    extra_zone_details: List[dict]
