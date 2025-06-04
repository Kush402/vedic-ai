#!/usr/bin/env python3
import swisseph as swe
print('swisseph loaded from:', swe.__file__)
from datetime import datetime, timezone
import pytz
from timezonefinder import TimezoneFinder
from typing import List, Dict, Any
from .models import ChartHouse
import os

# --- Configuration & Constants ---

# Path to Swiss Ephemeris data files.
# Create this directory and download ephemeris files (e.g., from ftp.astro.com/pub/swisseph/ephe/)
# Or, if you have SWEPH_PATH environment variable set, swisseph might find them automatically.
# If you leave it as None, swisseph will try to use its default search paths or download.
EPHE_PATH = os.getenv('SWEPH_PATH', os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'ephe'))  # Use project root/ephe directory

if EPHE_PATH:
    if not os.path.exists(EPHE_PATH):
        raise ValueError(
            f"Swiss Ephemeris data directory not found at {EPHE_PATH}. "
            "Please ensure the directory exists and contains the required ephemeris files. "
            "You can download them from https://www.astro.com/swisseph/swephfiles.htm "
            "or set the SWEPH_PATH environment variable to point to your ephemeris files."
        )
    
    # Check for both naming patterns (with and without _18 suffix)
    required_files = ['sepl.se1', 'semo.se1', 'seas.se1']
    required_files_alt = ['sepl_18.se1', 'semo_18.se1', 'seas_18.se1']
    
    files_present = os.listdir(EPHE_PATH)
    has_required_files = (
        all(f in files_present for f in required_files) or
        all(f in files_present for f in required_files_alt)
    )
    
    if not has_required_files:
        raise ValueError(
            f"Swiss Ephemeris data directory at {EPHE_PATH} is missing required files. "
            "Please ensure you have downloaded and placed the following files: "
            "sepl.se1 (or sepl_18.se1) for Planetary Ephemeris, "
            "semo.se1 (or semo_18.se1) for Moon Ephemeris, and "
            "seas.se1 (or seas_18.se1) for Asteroid Ephemeris. "
            "You can download them from https://www.astro.com/swisseph/swephfiles.htm"
        )
    
    swe.set_ephe_path(EPHE_PATH)

# Vedic Astrology uses Lahiri Ayanamsa
swe.set_sid_mode(swe.SIDM_LAHIRI)

PLANET_NAMES = {
    swe.SUN: "Sun",
    swe.MOON: "Moon",
    swe.MARS: "Mars",
    swe.MERCURY: "Mercury",
    swe.JUPITER: "Jupiter",
    swe.VENUS: "Venus",
    swe.SATURN: "Saturn",
    swe.TRUE_NODE: "Rahu", # Using True Node for Rahu
    # Ketu is calculated as 180 degrees from Rahu
    swe.URANUS: "Uranus",
    swe.NEPTUNE: "Neptune",
    swe.PLUTO: "Pluto" # Note: Pluto_adj sometimes used, but swe.PLUTO is fine
}
PLANET_IDS = [
    swe.SUN, swe.MOON, swe.MARS, swe.MERCURY, swe.JUPITER,
    swe.VENUS, swe.SATURN, swe.TRUE_NODE, swe.URANUS, swe.NEPTUNE, swe.PLUTO
]

ZODIAC_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

# --- Helper Functions ---

def get_sign_from_longitude(longitude_deg):
    """Determines the zodiac sign for a given sidereal longitude."""
    sign_index = int(longitude_deg / 30)
    return ZODIAC_SIGNS[sign_index % 12]

def get_d9_sign_from_longitude(longitude_deg):
    """Determines the D9 (Navamsa) sign for a given sidereal longitude."""
    # Multiply by 9 and get the sign
    d9_longitude = (longitude_deg * 9) % 360
    sign_index = int(d9_longitude / 30)
    return ZODIAC_SIGNS[sign_index % 12]

def calculate_ketu_longitude(rahu_longitude_deg):
    """Ketu is 180 degrees opposite Rahu."""
    ketu_longitude = (rahu_longitude_deg + 180) % 360
    return ketu_longitude

def extract_chart_tables(chart_data):
    """
    Extracts just the table data from the chart calculations.
    Returns a list of dictionaries with house, sign, and planets.
    """
    if not chart_data:
        return None
    
    return [
        {
            "house": row["house"],
            "sign": row["sign"],
            "planets": row["planets"]
        }
        for row in chart_data
    ]

def convert_to_jd_ut(dt_object_local, latitude, longitude):
    """Converts a local datetime object to Julian Day UT."""
    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lng=longitude, lat=latitude)

    if not timezone_str:
        raise ValueError(f"Could not determine timezone for lat={latitude}, lon={longitude}")

    local_tz = pytz.timezone(timezone_str)
    aware_local_dt = local_tz.localize(dt_object_local)
    utc_dt = aware_local_dt.astimezone(pytz.utc)

    # Use correct signature: year, month, day, hour, minute, second, cal
    jd_ut_tuple = swe.utc_to_jd(
        int(utc_dt.year),
        int(utc_dt.month),
        int(utc_dt.day),
        int(utc_dt.hour),
        int(utc_dt.minute),
        float(utc_dt.second),
        swe.GREG_CAL
    )
    return jd_ut_tuple[1] # jd_ut is the second element

# --- Core Chart Logic ---

def calculate_d1_chart(name: str, dob: str, tob: str, latitude: float, longitude: float) -> List[ChartHouse]:
    """Calculate D1 (Lagna) chart using Swiss Ephemeris."""
    # Parse date and time
    date_time = datetime.strptime(f"{dob} {tob}", "%Y-%m-%d %H:%M")
    
    # Convert to Julian Day UT using proper timezone handling
    julian_day = convert_to_jd_ut(date_time, latitude, longitude)

    # Calculate Ayanamsa
    ayanamsa = swe.get_ayanamsa_ut(julian_day)
    
    # Calculate Ascendant with proper flags
    flags = swe.FLG_SWIEPH | swe.FLG_NONUT
    houses = swe.houses(julian_day, latitude, longitude)
    ascendant = houses[0][0]  # First cusp (Ascendant)
    ascendant_sidereal = (ascendant - ayanamsa) % 360
    ascendant_sign = int(ascendant_sidereal / 30)

    # Calculate planet positions (including outer planets and nodes)
    planets = {}
    for planet in PLANET_IDS:
        if planet == swe.TRUE_NODE:
            rahu_pos = swe.calc_ut(julian_day, swe.TRUE_NODE, flags)[0][0]
            rahu_sidereal = (rahu_pos - ayanamsa) % 360
            planets[swe.TRUE_NODE] = rahu_sidereal
            ketu_sidereal = (rahu_sidereal + 180) % 360
            planets['KETU'] = ketu_sidereal
        else:
            planet_pos = swe.calc_ut(julian_day, planet, flags)[0][0]
            planets[planet] = (planet_pos - ayanamsa) % 360

    # Create chart houses using whole sign system
    houses = []
    for i in range(12):
        sign_num = (ascendant_sign + i) % 12
        house_start = sign_num * 30
        house_end = (sign_num + 1) * 30
        
        # Find planets in this house
        house_planets = []
        for planet, pos in planets.items():
            if house_start <= pos < house_end:
                if planet == 'KETU':
                    house_planets.append('Ketu')
                else:
                    house_planets.append(PLANET_NAMES.get(planet, str(planet)))
        
        houses.append(ChartHouse(
            house=f"{i+1}st",
            sign=ZODIAC_SIGNS[sign_num],
            planets=", ".join(house_planets) if house_planets else ""
        ))
    
    return houses

def calculate_d9_chart(name: str, dob: str, tob: str, latitude: float, longitude: float) -> List[ChartHouse]:
    """Calculate D9 (Navamsa) chart using Swiss Ephemeris."""
    # Parse date and time
    date_time = datetime.strptime(f"{dob} {tob}", "%Y-%m-%d %H:%M")
    
    # Convert to Julian Day UT using proper timezone handling
    julian_day = convert_to_jd_ut(date_time, latitude, longitude)

    # Calculate Ayanamsa
    ayanamsa = swe.get_ayanamsa_ut(julian_day)
    
    # Calculate Ascendant for D9
    flags = swe.FLG_SWIEPH | swe.FLG_NONUT
    houses = swe.houses(julian_day, latitude, longitude)
    ascendant = houses[0][0]  # First cusp (Ascendant)
    ascendant_sidereal = (ascendant - ayanamsa) % 360
    # Multiply by 9 for D9 and get the sign
    d9_ascendant = (ascendant_sidereal * 9) % 360
    ascendant_sign = int(d9_ascendant / 30)
    
    # Calculate planet positions for D9
    planets = {}
    for planet in PLANET_IDS:
        if planet == swe.TRUE_NODE:
            rahu_pos = swe.calc_ut(julian_day, swe.TRUE_NODE, flags)[0][0]
            rahu_sidereal = ((rahu_pos - ayanamsa) * 9) % 360  # Multiply by 9 for D9
            planets[swe.TRUE_NODE] = rahu_sidereal
            ketu_sidereal = (rahu_sidereal + 180) % 360
            planets['KETU'] = ketu_sidereal
        else:
            planet_pos = swe.calc_ut(julian_day, planet, flags)[0][0]
            planets[planet] = ((planet_pos - ayanamsa) * 9) % 360  # Multiply by 9 for D9

    # Create D9 chart houses
    houses = []
    for i in range(12):
        sign_num = (ascendant_sign + i) % 12
        house_start = sign_num * 30
        house_end = (sign_num + 1) * 30
        
        # Find planets in this house
        house_planets = []
        for planet, pos in planets.items():
            if house_start <= pos < house_end:
                if planet == 'KETU':
                    house_planets.append('Ketu')
                else:
                    house_planets.append(PLANET_NAMES.get(planet, str(planet)))
        
        houses.append(ChartHouse(
            house=f"{i+1}st",
            sign=ZODIAC_SIGNS[sign_num],
            planets=", ".join(house_planets) if house_planets else ""
        ))
    
    return houses

def get_planet_name(planet: int) -> str:
    """Convert planet number to name."""
    planet_names = {
        swe.SUN: "Sun",
        swe.MOON: "Moon",
        swe.MARS: "Mars",
        swe.MERCURY: "Mercury",
        swe.JUPITER: "Jupiter",
        swe.VENUS: "Venus",
        swe.SATURN: "Saturn"
    }
    return planet_names.get(planet, "Unknown")

def get_sign_name(longitude: float) -> str:
    """Convert longitude to sign name."""
    signs = [
        "Aries", "Taurus", "Gemini", "Cancer",
        "Leo", "Virgo", "Libra", "Scorpio",
        "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]
    sign_num = int(longitude / 30)
    return signs[sign_num]

def get_sign_number(sign_name: str) -> int:
    """Convert sign name to number (1-12)."""
    signs = {
        "Aries": 1, "Taurus": 2, "Gemini": 3, "Cancer": 4,
        "Leo": 5, "Virgo": 6, "Libra": 7, "Scorpio": 8,
        "Sagittarius": 9, "Capricorn": 10, "Aquarius": 11, "Pisces": 12
    }
    return signs.get(sign_name, 1)

# --- Output Formatting ---

def print_chart_as_markdown(chart_data, name, chart_type="Lagna"):
    if not chart_data:
        return

    print(f"## ✅ Your Provided {chart_type} Chart for {name}")
    print()
    print("| House | Sign        | Planets              |")
    print("| ----- | ----------- | -------------------- |")
    for row in chart_data:
        print(f"| {row.house:<5} | {row.sign:<11} | {row.planets:<20} |")
    print("\n---")

# --- Main Execution ---

if __name__ == "__main__":
    # Test case based on your example
    name_kush = "Kush Sharma"
    dob_kush = "2003-03-13"
    tob_kush = "13:00" # Local time
    latitude_kush = 28.6692  # North
    longitude_kush = 77.4538 # East

    # Calculate D1 (Lagna) chart
    d1_chart_kush = calculate_d1_chart(name_kush, dob_kush, tob_kush, latitude_kush, longitude_kush)
    if d1_chart_kush:
        print_chart_as_markdown(d1_chart_kush, name_kush, "Lagna (D1)")

    # Calculate D9 (Navamsa) chart
    d9_chart_kush = calculate_d9_chart(name_kush, dob_kush, tob_kush, latitude_kush, longitude_kush)
    if d9_chart_kush:
        print_chart_as_markdown(d9_chart_kush, name_kush, "Navamsa (D9)")

    print("\n\n--- Notes ---")
    print("1. Ensure Swiss Ephemeris data files are accessible (see EPHE_PATH or SWEPH_PATH).")
    print("2. Uses Lahiri Ayanamsa for Vedic calculations.")
    print("3. Planets include Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu (True), Ketu (True), Uranus, Neptune, Pluto.")
    print("4. House system is whole sign (Rasi chart), where Lagna sign is the 1st house.")
    print("5. Timezone is automatically determined from latitude/longitude.")
    print("   For historical dates, especially before standard timezones, results might need cross-verification.")
    print("6. Planetary positions from swe.calc_ut are geocentric ecliptical longitude, J2000 if swe.FLG_J2000 used,")
    print("   otherwise apparent positions (frame of date). For sidereal, this difference is less critical for sign placement.")
    print("7. D9 (Navamsa) chart is calculated by multiplying the longitude by 9 and finding the resulting sign.")
