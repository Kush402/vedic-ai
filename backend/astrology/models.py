from pydantic import BaseModel
from typing import List, Optional, Dict

class Planet(BaseModel):
    name: str
    sign: int
    degree: float
    isRetrograde: bool = False

class ChartHouse(BaseModel):
    house: str  # e.g., "1st", "2nd", etc.
    sign: str   # e.g., "Aries", "Taurus", etc.
    planets: str  # Comma-separated list of planets

class NakshatraInfo(BaseModel):
    nakshatra: str
    pada: int

class DashaPeriod(BaseModel):
    lord: str
    start_year: float
    end_year: float

class DashaInfo(BaseModel):
    current_maha_dasha: str
    years_remaining: float
    sequence: List[DashaPeriod]

class PlanetStrength(BaseModel):
    name: str
    sign: str
    longitude: float
    dignity: str
    retrograde: bool
    combust: bool

class ChartResponse(BaseModel):
    name: str
    dob: str
    tob: str
    latitude: float
    longitude: float
    houses: List[ChartHouse]
    nakshatra: NakshatraInfo
    dasha: Optional[DashaInfo] = None
    planet_strengths: Optional[Dict[str, PlanetStrength]] = None
    ascendant: Optional[str] = None
    aspects: Optional[Dict[str, List[str]]] = None

class ChartRequest(BaseModel):
    name: str
    dob: str  # Format: YYYY-MM-DD
    tob: str  # Format: HH:MM
    latitude: float
    longitude: float 