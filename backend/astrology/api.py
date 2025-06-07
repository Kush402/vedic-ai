from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional
from datetime import datetime
import swisseph as swe

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

router = APIRouter()

@router.post("/charts", response_model=ChartResponse)
async def calculate_charts(request: ChartRequest):
    try:
        # Calculate D1 chart
        result = calculate_d1_chart(
            name=request.name,
            dob=request.dob,
            tob=request.tob,
            latitude=request.latitude,
            longitude=request.longitude
        )
        
        # Create response
        response = ChartResponse(
            houses=result["houses"],
            nakshatra=result["nakshatra"],
            dasha=result["dasha"],
            planet_strengths=result["planet_strengths"],
            ascendant=result["ascendant"],
            aspects=result["aspects"]
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating chart: {str(e)}")

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

@router.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy", "version": "1.0.0"} 