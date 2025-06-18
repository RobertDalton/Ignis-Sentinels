from pydantic import BaseModel

class EvacuationAgent(BaseModel):
    id: str
    evacuation_route: str
    accuracy: float
    
