from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional, List, Any
from datetime import datetime
import swisseph as swe
import logging

from .charts import calculate_d1_chart
from .models import (
    ChartRequest,
    ChartResponse,
    ChartHouse,
    NakshatraInfo,
    DashaInfo,
    DashaPeriod,
    PlanetStrength
)
from .llm_query import generate_astrology_report
from .utils import get_coordinates_from_location

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/charts", response_model=ChartResponse)
async def generate_chart(request: ChartRequest):
    try:
        # Convert location to coordinates
        latitude, longitude = get_coordinates_from_location(request.location)
        
        # Calculate chart
        chart_data = calculate_d1_chart(
            name=request.name,
            dob=request.dob,
            tob=request.tob,
            latitude=latitude,
            longitude=longitude
        )
        return chart_data
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error generating chart: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/generate-report")
async def generate_report(request: ChartRequest):
    try:
        # Convert location to coordinates
        latitude, longitude = get_coordinates_from_location(request.location)
        
        # Calculate chart
        chart_data = calculate_d1_chart(
            name=request.name,
            dob=request.dob,
            tob=request.tob,
            latitude=latitude,
            longitude=longitude
        )
        
        # Generate report
        report = generate_astrology_report(chart_data)
        return report
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy", "version": "1.0.0"}

@router.post("/d1", response_model=ChartResponse)
async def get_d1_chart(request: ChartRequest):
    try:
        result = calculate_d1_chart(
            name=request.name,
            dob=request.dob,
            tob=request.tob,
            latitude=request.latitude,
            longitude=request.longitude
        )
        
        if not result:
            raise HTTPException(status_code=400, detail="Failed to calculate chart data")
        
        return ChartResponse(
            houses=result["houses"],
            nakshatra=NakshatraInfo(**result["nakshatra"]),
            dasha=DashaInfo(**result["dasha"]) if "dasha" in result else None,
            ascendant=result["ascendant"],
            aspects=result["aspects"]
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input data: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating chart: {str(e)}") 