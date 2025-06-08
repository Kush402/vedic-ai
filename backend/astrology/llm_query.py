import os
import json
import requests
from typing import Dict, Any, List
from fastapi import HTTPException
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

class GeminiAPI:
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        self.headers = {
            'Content-Type': 'application/json'
        }

    def generate_astrology_report(self, chart_data: Dict[str, Any]) -> str:
        """
        Generate an astrology report using the chart data
        """
        if not self.api_key:
            return "Gemini API key not configured. Please set GEMINI_API_KEY environment variable to enable AI-generated reports."

        try:
            # Format the chart data into a prompt
            prompt = self._format_chart_prompt(chart_data)
            
            # Log the prompt being sent to LLM
            logger.info("=== Prompt sent to LLM ===")
            logger.info(prompt)
            logger.info("========================")
            
            # Prepare the request payload
            payload = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": prompt
                            }
                        ]
                    }
                ]
            }

            # Make the API request
            response = requests.post(
                f"{self.base_url}?key={self.api_key}",
                headers=self.headers,
                json=payload
            )

            # Check for successful response
            response.raise_for_status()
            
            # Parse and return the response
            result = response.json()
            response_text = self._extract_response_text(result)
            
            # Log the response from LLM
            logger.info("=== Response from LLM ===")
            logger.info(response_text)
            logger.info("========================")
            
            return response_text

        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling Gemini API: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error calling Gemini API: {str(e)}")
        except Exception as e:
            logger.error(f"Error generating report: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")

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

# Create a singleton instance
gemini_api = GeminiAPI() 