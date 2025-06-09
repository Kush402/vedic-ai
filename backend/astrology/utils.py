from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import logging

logger = logging.getLogger(__name__)

def get_coordinates_from_location(location: str) -> tuple[float, float]:
    """
    Convert a location string to latitude and longitude coordinates.
    
    Args:
        location (str): Location string (e.g., "New Delhi, India")
        
    Returns:
        tuple[float, float]: (latitude, longitude)
        
    Raises:
        ValueError: If location cannot be found or geocoding fails
    """
    try:
        geolocator = Nominatim(user_agent="vedic-ai")
        location_data = geolocator.geocode(location)
        
        if location_data is None:
            raise ValueError(f"Could not find coordinates for location: {location}")
            
        logger.info(f"Found coordinates for {location}: {location_data.latitude}, {location_data.longitude}")
        return location_data.latitude, location_data.longitude
        
    except (GeocoderTimedOut, GeocoderUnavailable) as e:
        logger.error(f"Geocoding error for {location}: {str(e)}")
        raise ValueError(f"Error geocoding location: {location}. Please try again.")
    except Exception as e:
        logger.error(f"Unexpected error geocoding {location}: {str(e)}")
        raise ValueError(f"Error processing location: {location}. Please try again.") 