"""
Vedic AI Backend Package
"""

__version__ = "1.0.0" 

d9_asc_long = (ascendant_sidereal * 9) % 360
d9_asc_sign = int(d9_asc_long // 30) 

sign_num = (d9_asc_sign + i) % 12 

house_planets.append("Ketu" if planet == "KETU" else PLANET_NAMES.get(planet, str(planet))) 

"ascendant": ZODIAC_SIGNS[d9_asc_sign] 