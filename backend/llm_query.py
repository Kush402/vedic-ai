import os
import json
import requests
from typing import Dict, Any, List
from fastapi import HTTPException

class GeminiAPI:
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set")
        
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        self.headers = {
            'Content-Type': 'application/json'
        }

    def generate_astrology_report(self, chart_data: Dict[str, Any]) -> str:
        """
        Generate an astrology report using the chart data
        """
        try:
            # Format the chart data into a prompt
            prompt = self._format_chart_prompt(chart_data)
            
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
            return self._extract_response_text(result)

        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Error calling Gemini API: {str(e)}")
        except Exception as e:
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

        # Create a structured prompt
        prompt = f"""Please analyze this Vedic astrology chart and provide a detailed interpretation:

Ascendant: {ascendant}
Nakshatra: {nakshatra.get('name', '')} (Pada {nakshatra.get('pada', '')})

Planetary Positions:
{self._format_planets(planets)}

House Placements:
{self._format_houses(houses)}

Current Dasha Period:
- Maha Dasha: {dasha.get('current_maha_dasha', '')}
- Years Remaining: {dasha.get('years_remaining', '')}

Please provide:
1. A general personality analysis based on the ascendant and planetary positions
2. Key strengths and challenges indicated by the chart
3. Career and life path insights
4. Relationship dynamics
5. Current dasha period analysis and its implications
6. Recommendations for personal growth and development

Please keep the analysis balanced, constructive, and focused on personal growth opportunities."""

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
            house_num = house.get('house', '')
            sign = house.get('sign', '')
            planets = house.get('planets', '')
            formatted.append(f"House {house_num}: {sign} - Planets: {planets}")
        return "\n".join(formatted)

    def _extract_response_text(self, response: Dict[str, Any]) -> str:
        """Extract the generated text from the Gemini API response"""
        try:
            # Navigate through the response structure to get the generated text
            candidates = response.get('candidates', [])
            if not candidates:
                raise ValueError("No response candidates found")
            
            parts = candidates[0].get('content', {}).get('parts', [])
            if not parts:
                raise ValueError("No response parts found")
            
            return parts[0].get('text', '')
        except Exception as e:
            raise ValueError(f"Error extracting response text: {str(e)}")

# Create a singleton instance
gemini_api = GeminiAPI() 