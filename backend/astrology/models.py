from pydantic import BaseModel
from typing import List, Optional

class Planet(BaseModel):
    name: str
    sign: int
    degree: float
    isRetrograde: bool = False

class ChartHouse(BaseModel):
    house: str  # e.g., "1st", "2nd", etc.
    sign: str   # e.g., "Aries", "Taurus", etc.
    planets: str  # Comma-separated list of planets

class ChartResponse(BaseModel):
    houses: List[ChartHouse]
    ascendant: Optional[dict[str, float]] = None  # {sign: number, degree: number}

class ChartRequest(BaseModel):
    name: str
    dob: str  # Format: YYYY-MM-DD
    tob: str  # Format: HH:MM
    latitude: float
    longitude: float 