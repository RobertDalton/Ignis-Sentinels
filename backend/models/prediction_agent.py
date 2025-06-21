from pydantic import BaseModel

class PredictionAgent(BaseModel):
    id: str
    intensity: dict[str, float]
    spread: dict[str, float]
