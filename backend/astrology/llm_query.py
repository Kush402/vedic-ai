import os
import json
import requests
from typing import Dict, Any, List
from fastapi import HTTPException
from dotenv import load_dotenv
import logging
from datetime import datetime
import google.generativeai as genai

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

def generate_astrology_report(chart_data: Dict[str, Any]) -> Dict[str, str]:
    """
    Generate an astrological report using Gemini AI based on chart data.
    
    Args:
        chart_data (Dict[str, Any]): The calculated chart data
        
    Returns:
        Dict[str, str]: Generated report sections
    """
    try:
        # Create a prompt based on chart data
        prompt = f"""
        Based on the following Vedic astrology chart data, provide a detailed analysis:
        
        Name: {chart_data['name']}
        Ascendant: {chart_data['ascendant']}
        Moon Nakshatra: {chart_data['nakshatra']['nakshatra']} (Pada {chart_data['nakshatra']['pada']})
        Current Dasha: {chart_data['dasha']['current_maha_dasha']} ({chart_data['dasha']['years_remaining']} years remaining)
        
        House Placements:
        {format_houses(chart_data['houses'])}
        
        Please provide a comprehensive analysis including:
        1. Overall personality and life path
        2. Career and professional life
        3. Relationships and family life
        4. Health and well-being
        5. Current dasha period analysis
        6. Recommendations for personal growth
        """
        
        # Log the prompt being sent to Gemini
        logger.info("Sending prompt to Gemini:\n%s", prompt)
        
        # Generate response using Gemini
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        
        # Log the response from Gemini
        logger.info("Received response from Gemini:\n%s", response.text)
        
        # Parse and structure the response
        report = {
            "overall_analysis": response.text,
            "chart_data": chart_data
        }
        
        return report
        
    except Exception as e:
        logger.error(f"Error generating astrology report: {str(e)}")
        raise

def format_houses(houses: list) -> str:
    """Format house data for the prompt."""
    return "\n".join([
        f"House {i+1}: {house['sign']} {house['planets']}"
        for i, house in enumerate(houses)
    ])

class GeminiAPI:
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        self.headers = {
            'Content-Type': 'application/json'
        }
        if not self.api_key:
            logger.warning("GEMINI_API_KEY not found in environment variables")

    def generate_astrology_report(self, chart_data: Dict[str, Any]) -> Dict[str, str]:
        """
        Generate an astrological report using Gemini AI based on chart data.
        
        Args:
            chart_data (Dict[str, Any]): The calculated chart data
            
        Returns:
            Dict[str, str]: Generated report sections
        """
        try:
            # Create a prompt based on chart data
            prompt = f"""
            Based on the following Vedic astrology chart data, provide a detailed analysis:
            
            Name: {chart_data['name']}
            Ascendant: {chart_data['ascendant']}
            Moon Nakshatra: {chart_data['nakshatra']['nakshatra']} (Pada {chart_data['nakshatra']['pada']})
            Current Dasha: {chart_data['dasha']['current_maha_dasha']} ({chart_data['dasha']['years_remaining']} years remaining)
            
            House Placements:
            {self.format_houses(chart_data['houses'])}
            
            Please provide a comprehensive analysis including:
            1. Overall personality and life path
            2. Career and professional life
            3. Relationships and family life
            4. Health and well-being
            5. Current dasha period analysis
            6. Recommendations for personal growth
            """
            
            # Log the prompt being sent to Gemini
            logger.info("Sending prompt to Gemini:\n%s", prompt)
            
            # Generate response using Gemini
            model = genai.GenerativeModel('gemini-2.0-flash')
            response = model.generate_content(prompt)
            
            # Log the response from Gemini
            logger.info("Received response from Gemini:\n%s", response.text)
            
            # Parse and structure the response
            report = {
                "overall_analysis": response.text,
                "chart_data": chart_data
            }
            
            return report
            
        except Exception as e:
            logger.error(f"Error generating astrology report: {str(e)}")
            raise

    def _format_chart_prompt(self, chart_data: Dict[str, Any]) -> str:
        """
        Format the chart data into a prompt for the Gemini API
        """
        # Extract relevant information from chart data
        houses = chart_data.get('houses', [])
        planets = chart_data.get('planets', {})
        ascendant = chart_data.get('ascendant', '')
        nakshatra = chart_data.get('nakshatra', {})
        dasha = chart_data.get('dasha', {})
        
        # Extract birth details
        name = chart_data.get('name', '')
        dob = chart_data.get('dob', '')
        tob = chart_data.get('tob', '')
        latitude = chart_data.get('latitude', '')
        longitude = chart_data.get('longitude', '')

        # Format dasha sequence
        dasha_sequence = []
        if 'sequence' in dasha:
            for period in dasha['sequence']:
                dasha_sequence.append(
                    f"- {period['lord']} Dasha: {period['start_year']:.2f} to {period['end_year']:.2f}"
                )

        # Create a structured prompt
        prompt = f"""Act as a master Vedic astrologer and analyze this Vedic astrology chart and provide a detailed interpretation of the D1 chart and given properties, make sure to use Current on-going Maha Dasha, also take into account of upcoming astrological events and their impact on the chart.

Birth Details:
Name: {name}
Date of Birth: {dob}
Time of Birth: {tob}
Location: {latitude}°N, {longitude}°E

Ascendant: {ascendant}
Nakshatra: {nakshatra.get('nakshatra', '')} (Pada {nakshatra.get('pada', '')})

Planetary Positions:
{self._format_planets(planets)}

House Placements:
{self._format_houses(houses)}

Dasha Periods:
Complete Dasha Sequence:
{chr(10).join(dasha_sequence)}

Please provide:
1. A general personality analysis based on the ascendant and planetary positions
2. Key strengths and challenges indicated by the chart
3. Career and life path insights
4. Relationship dynamics
5. Current dasha period analysis and its implications
6. Recommendations for personal growth and development

Please keep the analysis real, with no sugar coating, and focused on Self, career, relationships, health, finance, family, children, travel, education."""

        return prompt

    def _format_planets(self, planets: Dict[str, Any]) -> str:
        """Format planetary positions into a readable string"""
        formatted = []
        for planet, data in planets.items():
            if isinstance(data, dict):
                sign = data.get('sign', '')
                house = data.get('house', '')
                formatted.append(f"{planet}: {sign} (House {house})")
        return "\n".join(formatted)

    def _format_houses(self, houses: List[Dict[str, Any]]) -> str:
        """Format house placements into a readable string"""
        formatted = []
        for house in houses:
            house_num = house.house if hasattr(house, 'house') else ''
            sign = house.sign if hasattr(house, 'sign') else ''
            planets = house.planets if hasattr(house, 'planets') else ''
            formatted.append(f"House {house_num}: {sign} - Planets: {planets}")
        return "\n".join(formatted)

    def _extract_response_text(self, response: Dict[str, Any]) -> str:
        """
        Extract the response text from the Gemini API response
        """
        try:
            # Get the text from the response
            text = response.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')
            
            # Replace markdown formatting with HTML
            text = text.replace('**', '<strong>').replace('*', '<em>')
            
            # Split into sections and format
            sections = text.split('\n\n')
            formatted_sections = []
            
            for section in sections:
                if section.strip():
                    # Handle bullet points
                    if section.startswith('*'):
                        points = section.split('\n')
                        formatted_points = []
                        for point in points:
                            if point.strip():
                                formatted_points.append(f"<li>{point.strip('* ')}</li>")
                        formatted_sections.append(f"<ul>{''.join(formatted_points)}</ul>")
                    else:
                        formatted_sections.append(f"<p>{section}</p>")
            
            return ''.join(formatted_sections)
            
        except Exception as e:
            logger.error(f"Error extracting response text: {str(e)}")
            return "Error processing the response"

    def format_house_placements(self, houses: List[Dict[str, str]]) -> str:
        """Format house placements for the prompt."""
        formatted = []
        for house in houses:
            # Extract house number and convert to integer
            house_num = int(house['house'].rstrip('stndrdth'))
            
            # Format house number with correct suffix
            if house_num == 1:
                house_str = "1st"
            elif house_num == 2:
                house_str = "2nd"
            elif house_num == 3:
                house_str = "3rd"
            else:
                house_str = f"{house_num}th"
                
            planets = house['planets'] if house['planets'] else "No planets"
            formatted.append(f"House {house_str} ({house['sign']}): {planets}")
        return "\n".join(formatted)

    def format_dasha_sequence(self, sequence: List[Dict[str, Any]]) -> str:
        """Format dasha sequence for the prompt."""
        formatted = []
        for dasha in sequence:
            formatted.append(f"- {dasha['lord']} Dasha: {dasha['start_year']:.2f} to {dasha['end_year']:.2f}")
        return "\n".join(formatted)

    def format_houses(self, houses: list) -> str:
        """Format house data for the prompt."""
        return "\n".join([
            f"House {i+1}: {house['sign']} {house['planets']}"
            for i, house in enumerate(houses)
        ])

# Create a singleton instance
gemini_api = GeminiAPI() 