#!/usr/bin/env python3
import swisseph as swe
print('swisseph loaded from:', swe.__file__)
from datetime import datetime, timezone, timedelta
import pytz
from timezonefinder import TimezoneFinder
from typing import List, Dict, Any
from .models import ChartHouse, NakshatraInfo, DashaInfo, DashaPeriod
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define planet numbers for Swiss Ephemeris
PLANET_NUMBERS = {
    'Sun': swe.SUN,
    'Moon': swe.MOON,
    'Mercury': swe.MERCURY,
    'Venus': swe.VENUS,
    'Mars': swe.MARS,
    'Jupiter': swe.JUPITER,
    'Saturn': swe.SATURN,
    'Rahu': swe.MEAN_NODE,  # Mean Node for Rahu
    'Uranus': swe.URANUS,
    'Neptune': swe.NEPTUNE,
    'Pluto': swe.PLUTO
}

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

def calculate_vimshottari_dasha(moon_long: float, dob: str) -> Dict[str, Any]:
    """Calculate Vimshottari dasha periods based on Moon's longitude."""
    try:
        # Parse date of birth
        dob_dt = datetime.strptime(dob, "%Y-%m-%d")
        
        # Get current date
        current_date = datetime.now()
        
        # Calculate nakshatra and pada
        nakshatra, pada = get_nakshatra_pada(moon_long)
        
        # Get dasha lord for the nakshatra
        dasha_lord = get_dasha_lord_from_nakshatra(nakshatra)
        
        # Calculate offset within nakshatra (0-13.333333 degrees)
        nak_offset = (moon_long % 13.333333) / 13.333333
        
        # Vimshottari dasha periods (in years)
        dasha_periods = {
            'Ketu': 7,
            'Venus': 20,
            'Sun': 6,
            'Moon': 10,
            'Mars': 7,
            'Rahu': 18,
            'Jupiter': 16,
            'Saturn': 19,
            'Mercury': 17
        }
        
        # Calculate balance of first dasha
        dasha_years = dasha_periods[dasha_lord]
        balance_years = (1 - nak_offset) * dasha_years
        elapsed_years = dasha_years - balance_years
        
        # Calculate start date of first dasha
        current_dasha_start = dob_dt - timedelta(days=elapsed_years * 365.25)
        
        # Calculate sequence of dashas
        dasha_sequence = []
        current_date_float = current_dasha_start.year + (current_dasha_start.month - 1) / 12 + (current_dasha_start.day - 1) / 365.25
        
        # Get the order of dasha lords starting from the birth dasha
        dasha_lords = list(dasha_periods.keys())
        start_index = dasha_lords.index(dasha_lord)
        ordered_lords = dasha_lords[start_index:] + dasha_lords[:start_index]
        
        # Calculate sequence
        for lord in ordered_lords:
            years = dasha_periods[lord]
            end_date_float = current_date_float + years
            dasha_sequence.append({
                "lord": lord,
                "start_year": current_date_float,
                "end_year": end_date_float
            })
            current_date_float = end_date_float
            
            # If we've covered the current year, we can stop
            if end_date_float > current_date.year:
                break
        
        # Find current dasha and remaining years
        current_dasha = None
        years_remaining = 0
        current_year_float = current_date.year + (current_date.month - 1) / 12 + (current_date.day - 1) / 365.25
        
        for dasha in dasha_sequence:
            if dasha["start_year"] <= current_year_float < dasha["end_year"]:
                current_dasha = dasha["lord"]
                years_remaining = dasha["end_year"] - current_year_float
                break
        
        return {
            "current_maha_dasha": current_dasha,
            "years_remaining": years_remaining,
            "sequence": dasha_sequence
        }
    except Exception as e:
        logger.error(f"Error calculating Vimshottari dasha: {str(e)}")
        raise

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
    # Different planets have different combustion ranges
    combustion_ranges = {
        swe.MERCURY: 14.0,  # Mercury combust within 14 degrees
        swe.VENUS: 10.0,    # Venus combust within 10 degrees
        swe.MARS: 17.0,     # Mars combust within 17 degrees
        swe.JUPITER: 11.0,  # Jupiter combust within 11 degrees
        swe.SATURN: 15.0,   # Saturn combust within 15 degrees
        swe.MOON: 12.0      # Moon combust within 12 degrees
    }
    
    if planet not in combustion_ranges:
        return False
        
    # Calculate angular distance
    diff = abs(planet_long - sun_long)
    if diff > 180:
        diff = 360 - diff
        
    return diff <= combustion_ranges[planet]

def calculate_planet_strengths(jd_ut: float, latitude: float, longitude: float) -> Dict[str, Dict[str, Any]]:
    """Calculate detailed planetary conditions and strengths."""
    try:
        # Get ayanamsa
        ayanamsa = swe.get_ayanamsa_ut(jd_ut)
        
        # Get Sun's position for combustion check
        sun_data = swe.calc_ut(jd_ut, int(PLANET_NUMBERS['Sun']))
        sun_long = (sun_data[0][0] - ayanamsa) % 360
        
        strengths = {}
        
        # Calculate for each planet
        for planet_name, planet_number in PLANET_NUMBERS.items():
            if planet_name in ['Rahu', 'Ketu']:
                continue
                
            # Get planet position
            planet_data = swe.calc_ut(jd_ut, int(planet_number))
            planet_long = (planet_data[0][0] - ayanamsa) % 360
            is_retrograde = planet_data[0][3] < 0
            
            # Check combustion
            combust = is_combust(int(planet_number), sun_long, planet_long)
            
            # Calculate dignity
            sign_index = int(planet_long // 30)
            sign = ZODIAC_SIGNS[sign_index]
            
            # Determine dignity status
            dignity = "Neutral"
            if planet_name in EXALTATION_SIGNS and sign == EXALTATION_SIGNS[planet_name]:
                dignity = "Exalted"
            elif planet_name in DEBILITATION_SIGNS and sign == DEBILITATION_SIGNS[planet_name]:
                dignity = "Debilitated"
            elif planet_name in OWN_SIGNS and sign in OWN_SIGNS[planet_name]:
                dignity = "Own Sign"
            
            # Calculate numerical strength for reference
            strength = 0.0
            if dignity == "Exalted":
                strength = 1.0
            elif dignity == "Debilitated":
                strength = -1.0
            elif dignity == "Own Sign":
                strength = 0.5
                
            if combust:
                strength -= 0.5
            if is_retrograde:
                strength -= 0.25
            
            strengths[planet_name] = {
                "sign": sign,
                "longitude": round(planet_long, 2),
                "dignity": dignity,
                "retrograde": is_retrograde,
                "combust": combust,
                "strength": round(strength, 2),
                "condition": "Strong" if strength > 0.25 else "Weak" if strength < -0.25 else "Moderate"
            }
            
        return strengths
        
    except Exception as e:
        logger.error(f"Error calculating planet strengths: {str(e)}")
        raise

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

def get_dasha_lord_from_nakshatra(nakshatra: str) -> str:
    """Get the dasha lord based on nakshatra."""
    nakshatra_dasha_map = {
        'Ashwini': 'Ketu',
        'Bharani': 'Venus',
        'Krittika': 'Sun',
        'Rohini': 'Moon',
        'Mrigashira': 'Mars',
        'Ardra': 'Rahu',
        'Punarvasu': 'Jupiter',
        'Pushya': 'Saturn',
        'Ashlesha': 'Mercury',
        'Magha': 'Ketu',
        'Purva Phalguni': 'Venus',
        'Uttara Phalguni': 'Sun',
        'Hasta': 'Moon',
        'Chitra': 'Mars',
        'Swati': 'Rahu',
        'Vishakha': 'Jupiter',
        'Anuradha': 'Saturn',
        'Jyeshtha': 'Mercury',
        'Mula': 'Ketu',
        'Purva Ashadha': 'Venus',
        'Uttara Ashadha': 'Sun',
        'Shravana': 'Moon',
        'Dhanishta': 'Mars',
        'Shatabhisha': 'Rahu',
        'Purva Bhadrapada': 'Jupiter',
        'Uttara Bhadrapada': 'Saturn',
        'Revati': 'Mercury'
    }
    return nakshatra_dasha_map.get(nakshatra)

def calculate_d1_chart(name: str, dob: str, tob: str, latitude: float, longitude: float) -> Dict[str, Any]:
    """Calculate D1 (Rashi) chart using Swiss Ephemeris with Whole Sign House system."""
    try:
        # Parse date and time
        dt_str = f"{dob} {tob}"
        try:
            # Try parsing as 24-hour format first
            dt_object_local = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
        except ValueError:
            # If that fails, try 12-hour format
            dt_object_local = datetime.strptime(dt_str, "%Y-%m-%d %I:%M")
            
        logger.info(f"Parsed datetime: {dt_object_local}")
        
        # Convert to UTC
        utc_dt = convert_to_utc(dt_object_local, latitude, longitude)
        
        # Convert to Julian day
        jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, 
                       utc_dt.hour + utc_dt.minute/60.0)
        
        # Calculate planet positions
        planet_positions = {}
        nakshatras = []
        
        # First calculate Rahu's position
        rahu_data = swe.calc_ut(jd, int(PLANET_NUMBERS['Rahu']))
        rahu_pos = (rahu_data[0][0] - swe.get_ayanamsa_ut(jd)) % 360
        planet_positions['Rahu'] = rahu_pos
        planet_positions['Ketu'] = (rahu_pos + 180) % 360
        
        # Calculate other planet positions
        for planet_name, planet_number in PLANET_NUMBERS.items():
            if planet_name in ['Rahu', 'Ketu']:
                continue
                
            # Calculate tropical position
            planet_data = swe.calc_ut(jd, int(planet_number))
            tropical_pos = planet_data[0][0]
            ayanamsa = swe.get_ayanamsa_ut(jd)
            
            # Convert to sidereal
            sidereal_pos = (tropical_pos - ayanamsa) % 360
            planet_positions[planet_name] = sidereal_pos
            
            # Calculate nakshatra
            nakshatra, pada = get_nakshatra_pada(sidereal_pos)
            nakshatras.append({
                "planet": planet_name,
                "nakshatra": nakshatra,
                "pada": pada,
                "sign": get_sign(sidereal_pos),
                "degree": sidereal_pos
            })
        
        # Calculate ascendant using Whole Sign system
        asc_tropical = swe.houses(jd, latitude, longitude)[0][0]
        ayanamsa = swe.get_ayanamsa_ut(jd)
        asc_sidereal = (asc_tropical - ayanamsa) % 360
        asc_sign_index = int(asc_sidereal // 30)
        
        # Initialize house data
        houses = []
        house_planets = {i: [] for i in range(12)}  # 0 = house 1
        
        # Assign planets to houses based on their sign
        for planet, lon in planet_positions.items():
            sign_index = int(lon // 30)
            rel_house_index = (sign_index - asc_sign_index) % 12
            house_planets[rel_house_index].append(planet)
        
        # Generate house data
        for i in range(12):
            sign_index = (asc_sign_index + i) % 12
            sign_name = ZODIAC_SIGNS[sign_index]
            planets_in_house = house_planets[i]
            houses.append({
                "house": f"{i+1}st",
                "sign": sign_name,
                "planets": ", ".join(planets_in_house) if planets_in_house else ""
            })
        
        # Calculate aspects
        aspects = {}
        for p1_name, p1_pos in planet_positions.items():
            aspects[p1_name] = []
            for p2_name, p2_pos in planet_positions.items():
                if p1_name != p2_name:
                    diff = abs(p1_pos - p2_pos)
                    if diff > 180:
                        diff = 360 - diff
                    
                    # Check for major aspects
                    if abs(diff - 0) < 8:  # Conjunction
                        aspects[p1_name].append(p2_name)
                    elif abs(diff - 60) < 8:  # Sextile
                        aspects[p1_name].append(p2_name)
                    elif abs(diff - 90) < 8:  # Square
                        aspects[p1_name].append(p2_name)
                    elif abs(diff - 120) < 8:  # Trine
                        aspects[p1_name].append(p2_name)
                    elif abs(diff - 180) < 8:  # Opposition
                        aspects[p1_name].append(p2_name)
        
        # Get Moon's nakshatra and position
        moon_nakshatra = next(n["nakshatra"] for n in nakshatras if n["planet"] == "Moon")
        moon_long = planet_positions["Moon"]
        
        # Calculate dashas properly using moon longitude
        dasha_result = calculate_vimshottari_dasha(moon_long, dob)
        
        logger.info(f"Calculated ascendant: {get_sign(asc_sidereal)} {asc_sidereal}°")
        logger.info(f"Calculated planet positions: {planet_positions}")
        
        # Calculate planet strengths
        planet_strengths = calculate_planet_strengths(jd, latitude, longitude)
        
        return {
            "name": name,
            "ascendant": get_sign(asc_sidereal),
            "houses": houses,
            "nakshatra": {
                "nakshatra": moon_nakshatra,
                "pada": next(n["pada"] for n in nakshatras if n["planet"] == "Moon")
            },
            "dasha": {
                "current_maha_dasha": dasha_result["current_maha_dasha"],
                "years_remaining": dasha_result["years_remaining"],
                "sequence": dasha_result["sequence"]
            },
            "planet_strengths": planet_strengths,
            "aspects": aspects
        }
    except Exception as e:
        logger.error(f"Error calculating D1 chart: {str(e)}")
        raise

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

def convert_to_utc(dt_object_local: datetime, latitude: float, longitude: float) -> datetime:
    """Convert local datetime to UTC."""
    try:
        # Get timezone from coordinates
        tf = TimezoneFinder()
        timezone_str = tf.timezone_at(lat=latitude, lng=longitude)
        if not timezone_str:
            raise ValueError(f"Could not determine timezone for coordinates: {latitude}, {longitude}")
        
        # Convert to UTC
        local_tz = pytz.timezone(timezone_str)
        local_dt = local_tz.localize(dt_object_local)
        utc_dt = local_dt.astimezone(pytz.UTC)
        
        logger.info(f"Converted datetime {dt_object_local} to UTC {utc_dt}")
        return utc_dt
    except Exception as e:
        logger.error(f"Error converting datetime to UTC: {str(e)}")
        raise

def get_nakshatra_pada(longitude: float) -> tuple[str, int]:
    """Calculate Nakshatra and Pada from longitude."""
    nak_index = int(longitude // 13.3333)
    nakshatra = NAKSHATRAS[nak_index]
    offset_in_nak = longitude % 13.3333
    pada = int(offset_in_nak // 3.3333) + 1
    return nakshatra, pada

def get_sign(longitude: float) -> str:
    """Get sign name from longitude."""
    sign_index = int(longitude // 30)
    return ZODIAC_SIGNS[sign_index]

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
