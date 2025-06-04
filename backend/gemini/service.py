import os
import google.generativeai as genai
from typing import List, Dict, Optional
from dotenv import load_dotenv
from astrology.models import ChartHouse

# Load environment variables
load_dotenv()

# Configure Gemini
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not found")

genai.configure(api_key=API_KEY)
MODEL_NAME = "gemini-pro"

def format_chart_data(label: str, chart_data: List[ChartHouse]) -> str:
    """Format chart data into a markdown table."""
    text = f"\n### {label} Chart:\n"
    text += "| House | Sign | Planets |\n"
    text += "| ----- | ----- | -------- |\n"
    for entry in chart_data:
        planets = entry.planets if entry.planets else "—"
        text += f"| {entry.house} | {entry.sign} | {planets} |\n"
    return text

async def generate_astrology_report(
    name: str,
    dob: str,
    tob: str,
    pob: str,
    lagna_chart: List[ChartHouse],
    navamsa_chart: List[ChartHouse],
    chart_image_base64: Optional[str] = None
) -> str:
    """
    Generate an astrological report using Gemini AI.
    
    Args:
        name: Client's name
        dob: Date of birth
        tob: Time of birth
        pob: Place of birth
        lagna_chart: List of houses in the Lagna chart
        navamsa_chart: List of houses in the Navamsa chart
        chart_image_base64: Optional base64 encoded chart image
    
    Returns:
        str: Generated report in markdown format
    """
    # Format the prompt
    prompt = f"""
You are an expert Vedic (Jyotish) astrologer. Generate a comprehensive and insightful astrological report.

## Client Details:
- Name: {name}
- Date of Birth: {dob}
- Time of Birth: {tob}
- Place of Birth: {pob}

## Pre-Calculated Astrological Data:
Utilize the following precise chart data as your primary basis for analysis:
{format_chart_data("Lagna (Ascendant)", lagna_chart)}
{format_chart_data("Navamsa (D9)", navamsa_chart)}

## Instructions:
1. Use provided chart data as authoritative for Lagna/Navamsa analysis.
2. Explain traits, personality, and destiny based on planetary placements.
3. Include detailed commentary on D9 for marriage and spiritual strength.
4. Provide professional, structured insight with markdown headings.
5. Add general advice, remedies, and a short disclaimer.

Generate the report now.
"""

    try:
        # Initialize the model
        model = genai.GenerativeModel(MODEL_NAME)
        
        # Prepare the content
        contents = [{"text": prompt}]
        
        # Add image if provided
        if chart_image_base64:
            contents.append({
                "inline_data": {
                    "mime_type": "image/jpeg",
                    "data": chart_image_base64.split(',')[1] if ',' in chart_image_base64 else chart_image_base64
                }
            })
        
        # Generate content
        response = await model.generate_content_async(contents)
        
        if not response.text:
            raise ValueError("Empty response from Gemini API")
            
        return response.text

    except Exception as e:
        raise Exception(f"Failed to generate report: {str(e)}") 