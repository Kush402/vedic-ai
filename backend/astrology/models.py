from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

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
    sequence: List[Dict[str, Any]]

class PlanetStrength(BaseModel):
    name: str
    sign: str
    longitude: float
    dignity: str
    retrograde: bool
    combust: bool

class ChartResponse(BaseModel):
    name: str
    ascendant: str
    houses: List[Dict[str, str]]
    nakshatra: NakshatraInfo
    dasha: DashaInfo
    planet_strengths: Optional[Dict[str, float]] = None
    aspects: Dict[str, List[str]]

class ChartRequest(BaseModel):
    name: str = Field(..., description="Full name of the person")
    dob: str = Field(..., description="Date of birth in YYYY-MM-DD format")
    tob: str = Field(..., description="Time of birth in HH:MM format (24-hour)")
    location: str = Field(..., description="Place of birth (e.g., 'New Delhi, India')") 