from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional
from datetime import datetime
import swisseph as swe

from .charts import calculate_d1_chart, calculate_d9_chart
from .models import (
    ChartRequest,
    ChartResponse,
    CombinedChartResponse,
    ChartHouse,
    NakshatraInfo,
    DashaInfo,
    DashaPeriod,
    PlanetStrength
)

router = APIRouter()

@router.post("/charts", response_model=CombinedChartResponse)
async def calculate_charts(request: ChartRequest):
    try:
        # Calculate D1 chart
        d1_result = calculate_d1_chart(
            name=request.name,
            dob=request.dob,
            tob=request.tob,
            latitude=request.latitude,
            longitude=request.longitude
        )
        # Calculate D9 chart
        d9_result = calculate_d9_chart(
            name=request.name,
            dob=request.dob,
            tob=request.tob,
            latitude=request.latitude,
            longitude=request.longitude
        )
        # Create response
        response = CombinedChartResponse(
            d1_chart=ChartResponse(
                houses=d1_result["houses"],
                nakshatra=d1_result["nakshatra"],
                dasha=d1_result["dasha"],
                planet_strengths=None,  # Remove from individual charts
                ascendant=None,
                aspects=d1_result["aspects"]
            ),
            d9_chart=ChartResponse(
                houses=d9_result["houses"],
                nakshatra=d9_result["nakshatra"],
                dasha=None,
                planet_strengths=None,  # Remove from individual charts
                ascendant=None,
                aspects=d9_result["aspects"]
            ),
            planet_strengths=d1_result["planet_strengths"]  # Keep only at root level
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating charts: {str(e)}")

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
            ascendant=None
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input data: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating chart: {str(e)}")

@router.post("/d9", response_model=ChartResponse)
async def get_d9_chart(request: ChartRequest):
    try:
        result = calculate_d9_chart(
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
            ascendant=None
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