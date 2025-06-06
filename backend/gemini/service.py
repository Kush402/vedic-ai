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

# Configure the API
genai.configure(api_key=API_KEY)

# List available models and print them for debugging
available_models = genai.list_models()
print("Available models:", [model.name for model in available_models])

# Use the correct model name with the models/ prefix
MODEL_NAME = "models/gemini-2.0-flash"  # This matches the model name from the available models list

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
    try:
        # Initialize the model
        model = genai.GenerativeModel(MODEL_NAME)
        
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
        
        # Generate content
        response = await model.generate_content_async(prompt)
        
        if not response.text:
            raise ValueError("Empty response from Gemini API")
            
        return response.text

    except Exception as e:
        print(f"Error details: {str(e)}")  # Add more detailed error logging
        raise Exception(f"Failed to generate report: {str(e)}")