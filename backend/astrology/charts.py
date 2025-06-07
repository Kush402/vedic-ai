#!/usr/bin/env python3
import swisseph as swe
print('swisseph loaded from:', swe.__file__)
from datetime import datetime, timezone, timedelta
import pytz
from timezonefinder import TimezoneFinder
from typing import List, Dict, Any
from .models import ChartHouse, NakshatraInfo, DashaInfo, DashaPeriod
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

# Nakshatra list in order
NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira",
    "Ardra", "Punarvasu", "Pushya", "Ashlesha", "Magha",
    "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati",
    "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha",
    "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
    "Uttara Bhadrapada", "Revati"
]

# Vimshottari Dasha constants
DASHA_ORDER = [
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu",
    "Jupiter", "Saturn", "Mercury"
]

DASHA_YEARS = {
    "Ketu": 7, "Venus": 20, "Sun": 6, "Moon": 10,
    "Mars": 7, "Rahu": 18, "Jupiter": 16, "Saturn": 19, "Mercury": 17
}

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

# Planetary Strength Constants
EXALTATION_SIGNS = {
    swe.SUN: "Aries",
    swe.MOON: "Taurus",
    swe.MARS: "Capricorn",
    swe.MERCURY: "Virgo",
    swe.JUPITER: "Cancer",
    swe.VENUS: "Pisces",
    swe.SATURN: "Libra"
}

DEBILITATION_SIGNS = {
    swe.SUN: "Libra",
    swe.MOON: "Scorpio",
    swe.MARS: "Cancer",
    swe.MERCURY: "Pisces",
    swe.JUPITER: "Capricorn",
    swe.VENUS: "Virgo",
    swe.SATURN: "Aries"
}

OWN_SIGNS = {
    swe.SUN: ["Leo"],
    swe.MOON: ["Cancer"],
    swe.MARS: ["Aries", "Scorpio"],
    swe.MERCURY: ["Gemini", "Virgo"],
    swe.JUPITER: ["Sagittarius", "Pisces"],
    swe.VENUS: ["Taurus", "Libra"],
    swe.SATURN: ["Capricorn", "Aquarius"]
}

COMBUSTION_LIMITS = {
    swe.MERCURY: 12,
    swe.VENUS: 10,
    swe.MARS: 17,
    swe.JUPITER: 11,
    swe.SATURN: 15
}

# Graha Drishti rules (based on sign distance)
ASPECT_RULES = {
    swe.SUN:    [7],
    swe.MOON:   [7],
    swe.MERCURY:[7],
    swe.JUPITER:[5, 7, 9],
    swe.VENUS:  [7],
    swe.SATURN: [3, 7, 10],
    swe.MARS:   [4, 7, 8]
}

# --- Helper Functions ---

def get_nakshatra_info(longitude: float) -> dict:
    """Returns nakshatra name and pada from moon longitude."""
    index = int(longitude / (360 / 27))
    nakshatra = NAKSHATRAS[index]
    pada = int((longitude % (360 / 27)) / (360 / 108)) + 1  # 4 padas per nakshatra
    return {
        "nakshatra": nakshatra,
        "pada": pada
    }

from datetime import datetime, timedelta

def calculate_vimshottari_dasha(moon_long: float, dob: str) -> dict:
    """Returns current Maha Dasha and sequence from birth using Moon longitude."""
    # Find nakshatra index and corresponding Mahadasha lord
    nakshatra_index = int(moon_long / (360 / 27))
    dasha_lord = DASHA_ORDER[nakshatra_index % 9]
    dasha_years = DASHA_YEARS[dasha_lord]

    # How far Moon has progressed in current nakshatra
    nak_start = nakshatra_index * (360 / 27)
    nak_offset = (moon_long - nak_start) / (360 / 27)
    balance_years = (1 - nak_offset) * dasha_years
    elapsed_years = dasha_years - balance_years

    # Base: date of birth
    dob_dt = datetime.strptime(dob, "%Y-%m-%d")
    current_dasha_start = dob_dt - timedelta(days=elapsed_years * 365.25)

    # Build full Dasha timeline (9 periods)
    sequence = []
    dasha_index = DASHA_ORDER.index(dasha_lord)
    running_date = current_dasha_start

    for i in range(9):
        lord = DASHA_ORDER[(dasha_index + i) % 9]
        span = DASHA_YEARS[lord]
        start = running_date
        end = start + timedelta(days=span * 365.25)
        sequence.append({
            "lord": lord,
            "start_year": float(start.year + start.month/12 + start.day/365.25),
            "end_year": float(end.year + end.month/12 + end.day/365.25)
        })
        running_date = end

    # Find the current Mahadasha at DOB
    for dasha in sequence:
        start_year = dasha['start_year']
        end_year = dasha['end_year']
        dob_year = dob_dt.year + dob_dt.month/12 + dob_dt.day/365.25
        if start_year <= dob_year < end_year:
            current = dasha
            years_remaining = end_year - dob_year
            break

    return {
        "current_maha_dasha": current["lord"],
        "years_remaining": round(years_remaining, 2),
        "sequence": sequence[:3]  # or full 9 if needed
    }


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
    """Convert local datetime to Julian Day UT."""
    # Calculate timezone offset based on longitude
    timezone_offset = longitude / 15.0  # 15 degrees per hour
    
    # Adjust the time for timezone
    dt_object_utc = dt_object_local - timedelta(hours=timezone_offset)
    
    # Convert to Julian Day
    jd = swe.julday(
        dt_object_utc.year,
        dt_object_utc.month,
        dt_object_utc.day,
        dt_object_utc.hour + dt_object_utc.minute/60.0
    )
    
    return jd

def is_combust(planet: int, sun_long: float, planet_long: float) -> bool:
    """Check if a planet is combust (too close to the Sun)."""
    if planet in COMBUSTION_LIMITS:
        diff = abs(sun_long - planet_long) % 360
        if diff > 180:
            diff = 360 - diff
        return diff < COMBUSTION_LIMITS[planet]
    return False

def calculate_planet_strengths(jd_ut: float, latitude: float, longitude: float) -> dict:
    """Calculate planetary strength indicators."""
    flags = swe.FLG_SWIEPH | swe.FLG_NONUT
    strength = {}

    # Get ayanamsa
    ayanamsa = swe.get_ayanamsa_ut(jd_ut)

    # Get Sun longitude for combustion checks
    sun_data = swe.calc_ut(jd_ut, swe.SUN, flags)
    sun_long = sun_data[0][0]  # First element of first tuple is longitude
    sun_sidereal = (sun_long - ayanamsa) % 360

    for planet in [
        swe.SUN, swe.MOON, swe.MARS, swe.MERCURY,
        swe.JUPITER, swe.VENUS, swe.SATURN
    ]:
        planet_data = swe.calc_ut(jd_ut, planet, flags)
        long_tropical = planet_data[0][0]  # First element of first tuple is longitude
        retrograde = planet_data[3][0] < 0 if len(planet_data) > 3 else False  # Speed is fourth element if available
        sidereal_long = (long_tropical - ayanamsa) % 360
        sign = get_sign_from_longitude(sidereal_long)

        dignity = "Neutral"
        if sign == EXALTATION_SIGNS.get(planet):
            dignity = "Exalted"
        elif sign == DEBILITATION_SIGNS.get(planet):
            dignity = "Debilitated"
        elif sign in OWN_SIGNS.get(planet, []):
            dignity = "Own Sign"

        strength[str(planet)] = {
            "name": PLANET_NAMES.get(planet, str(planet)),
            "sign": sign,
            "longitude": round(sidereal_long, 2),
            "dignity": dignity,
            "retrograde": retrograde,
            "combust": is_combust(planet, sun_sidereal, sidereal_long)
        }

    return strength

def get_sidereal_longitude(jd_ut: float, planet: int) -> float:
    """Get the sidereal longitude of a planet."""
    flags = swe.FLG_SWIEPH | swe.FLG_NONUT
    pos = swe.calc_ut(jd_ut, planet, flags)[0][0]
    ayanamsa = swe.get_ayanamsa_ut(jd_ut)
    return (pos - ayanamsa) % 360

def calculate_aspects(jd_ut: float) -> dict:
    """Calculate planetary aspects based on sign positions."""
    positions = {}
    aspects = {}

    # Get sign positions for all classical planets
    for planet in ASPECT_RULES.keys():
        long = get_sidereal_longitude(jd_ut, planet)
        positions[planet] = {
            "longitude": round(long, 2),
            "sign": int(long // 30)
        }

    # Loop through planets and apply aspect rules
    for planet, data in positions.items():
        planet_sign = data["sign"]
        aspect_list = []

        for other_planet, other_data in positions.items():
            if other_planet == planet:
                continue
            other_sign = other_data["sign"]
            sign_diff = (other_sign - planet_sign) % 12

            # Calculate aspects based on traditional rules
            if planet == swe.JUPITER:  # Jupiter aspects 5th, 7th, and 9th houses
                if sign_diff in [4, 6, 8]:  # 5th, 7th, 9th house aspects
                    aspect_list.append(PLANET_NAMES.get(other_planet, str(other_planet)))
            elif planet == swe.SATURN:  # Saturn aspects 3rd, 7th, and 10th houses
                if sign_diff in [2, 6, 9]:  # 3rd, 7th, 10th house aspects
                    aspect_list.append(PLANET_NAMES.get(other_planet, str(other_planet)))
            elif planet == swe.MARS:  # Mars aspects 4th, 7th, and 8th houses
                if sign_diff in [3, 6, 7]:  # 4th, 7th, 8th house aspects
                    aspect_list.append(PLANET_NAMES.get(other_planet, str(other_planet)))
            else:  # Sun, Moon, Mercury, Venus only aspect 7th house
                if sign_diff == 6:  # 7th house aspect
                    aspect_list.append(PLANET_NAMES.get(other_planet, str(other_planet)))

        aspects[PLANET_NAMES.get(planet, str(planet))] = aspect_list

    return aspects

# --- Core Chart Logic ---

def calculate_d1_chart(name: str, dob: str, tob: str, latitude: float, longitude: float) -> Dict[str, Any]:
    """Calculate D1 (Lagna) chart using Swiss Ephemeris."""
    # Parse date and time
    date_time = datetime.strptime(f"{dob} {tob}", "%Y-%m-%d %H:%M")
    
    # Convert to Julian Day UT using proper timezone handling
    julian_day = convert_to_jd_ut(date_time, latitude, longitude)

    # Calculate Ayanamsa
    ayanamsa = swe.get_ayanamsa_ut(julian_day)
    
    # Calculate Ascendant with proper flags
    flags = swe.FLG_SWIEPH | swe.FLG_NONUT
    houses_data = swe.houses(julian_day, latitude, longitude)
    ascendant = houses_data[0][0]  # First element of first tuple is Ascendant
    ascendant_sidereal = (ascendant - ayanamsa) % 360
    ascendant_sign = int(ascendant_sidereal / 30)
    
    # Calculate planet positions (including outer planets and nodes)
    planets = {}
    for planet in PLANET_IDS:
        if planet == swe.TRUE_NODE:
            rahu_data = swe.calc_ut(julian_day, swe.TRUE_NODE, flags)
            rahu_pos = rahu_data[0][0]
            rahu_sidereal = (rahu_pos - ayanamsa) % 360
            planets[swe.TRUE_NODE] = rahu_sidereal
            ketu_sidereal = (rahu_sidereal + 180) % 360
            planets['KETU'] = ketu_sidereal
        else:
            planet_data = swe.calc_ut(julian_day, planet, flags)
            planet_pos = planet_data[0][0]
            planets[planet] = (planet_pos - ayanamsa) % 360

    # Calculate Moon's Nakshatra
    moon_longitude = planets[swe.MOON]
    nakshatra_info = get_nakshatra_info(moon_longitude)

    # Calculate Vimshottari Dasha
    dasha_info = calculate_vimshottari_dasha(moon_longitude, dob)

    # Calculate planetary aspects
    positions = {}
    aspects = {}
    for planet in ASPECT_RULES.keys():
        if planet in planets:
            positions[planet] = {
                "longitude": round(planets[planet], 2),
                "sign": int(planets[planet] / 30)
            }

    # Calculate aspects
    for planet, data in positions.items():
        planet_sign = data["sign"]
        rules = ASPECT_RULES.get(planet, [])
        aspect_list = []

        for other_planet, other_data in positions.items():
            if other_planet == planet:
                continue
            other_sign = other_data["sign"]
            sign_diff = (other_sign - planet_sign) % 12

            if sign_diff in rules:
                aspect_list.append(PLANET_NAMES.get(other_planet, str(other_planet)))

        aspects[PLANET_NAMES.get(planet, str(planet))] = aspect_list

    # Create chart houses
    houses = []
    for i in range(12):
        sign_num = (ascendant_sign + i) % 12
        sign_name = ZODIAC_SIGNS[sign_num]
        
        # Find planets in this house
        house_planets = []
        for planet, pos in planets.items():
            planet_sign = int(pos / 30)
            if planet_sign == sign_num:
                if planet == 'KETU':
                    house_planets.append('Ketu')
                else:
                    house_planets.append(PLANET_NAMES.get(planet, str(planet)))
        
        # Sort planets in the order they appear in PLANET_NAMES
        sorted_planets = []
        for planet_id in PLANET_IDS:
            planet_name = PLANET_NAMES.get(planet_id, str(planet_id))
            if planet_name in house_planets:
                sorted_planets.append(planet_name)
        if 'Ketu' in house_planets:
            sorted_planets.append('Ketu')
        
        houses.append(ChartHouse(
            house=f"{i+1}st",
            sign=sign_name,
            planets=", ".join(sorted_planets) if sorted_planets else ""
        ))
    
    # Debug information
    print(f"Debug - Ascendant: {ascendant_sidereal}° ({ZODIAC_SIGNS[ascendant_sign]})")
    print("Debug - Planet Positions:")
    for planet, pos in planets.items():
        planet_name = PLANET_NAMES.get(planet, str(planet))
        planet_sign = int(pos / 30)
        print(f"{planet_name}: {pos}° ({ZODIAC_SIGNS[planet_sign]})")
    
    return {
        "houses": houses,
        "nakshatra": nakshatra_info,
        "dasha": dasha_info,
        "planet_strengths": None,  # We'll calculate this separately
        "aspects": aspects,
        "ascendant": ZODIAC_SIGNS[ascendant_sign]  # Added ascendant
    }

def get_planet_name(planet: int) -> str:
    """Get the name of a planet from its Swiss Ephemeris ID."""
    return PLANET_NAMES.get(planet, str(planet))

def get_sign_name(longitude: float) -> str:
    """Get the name of a zodiac sign from a longitude."""
    sign_index = int(longitude / 30)
    return ZODIAC_SIGNS[sign_index % 12]

def get_sign_number(sign_name: str) -> int:
    """Get the number of a zodiac sign (0-11) from its name."""
    return ZODIAC_SIGNS.index(sign_name)

def print_chart_as_markdown(chart_data, name, chart_type="Lagna"):
    """Print a chart in a markdown table format."""
    print(f"\n## {name}'s {chart_type} Chart")
    print("\n| House | Sign | Planets |")
    print("|-------|------|---------|")
    for house in chart_data["houses"]:
        print(f"| {house.house} | {house.sign} | {house.planets or '-'} |")
    if "nakshatra" in chart_data:
        print(f"\nMoon's Nakshatra: {chart_data['nakshatra']['nakshatra']} (Pada {chart_data['nakshatra']['pada']})")
    if "dasha" in chart_data:
        print("\n### Vimshottari Dasha")
        print(f"Current Maha Dasha: {chart_data['dasha']['current_maha_dasha']}")
        print(f"Years Remaining: {chart_data['dasha']['years_remaining']}")
        print("\nUpcoming Dashas:")
        for dasha in chart_data['dasha']['sequence']:
            print(f"- {dasha['lord']}: {dasha['start_year']} to {dasha['end_year']}")

# Example usage
if __name__ == "__main__":
    # Example data
    name_kush = "Kush"
    dob_kush = "2003-03-13"
    tob_kush = "13:00"
    latitude_kush = 28.6692
    longitude_kush = 77.4538

    # Calculate D1 (Lagna) chart
    d1_chart_kush = calculate_d1_chart(name_kush, dob_kush, tob_kush, latitude_kush, longitude_kush)
    if d1_chart_kush:
        print_chart_as_markdown(d1_chart_kush, name_kush, "Lagna (D1)")

    print("\n\n--- Notes ---")
    print("1. All calculations use Lahiri Ayanamsa")
    print("2. D9 chart positions are calculated by multiplying D1 positions by 9")
    print("3. Ketu is calculated as 180 degrees from Rahu")
    print("4. Vimshottari Dasha is calculated based on Moon's Nakshatra")
