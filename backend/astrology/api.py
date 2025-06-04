from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from .charts import calculate_d1_chart, calculate_d9_chart
from .models import ChartRequest, ChartResponse, ChartHouse

router = APIRouter()

@router.post("/d1", response_model=ChartResponse)
async def get_d1_chart(request: ChartRequest):
    try:
        houses_data = calculate_d1_chart(
            name=request.name,
            dob=request.dob,
            tob=request.tob,
            latitude=request.latitude,
            longitude=request.longitude
        )
        
        if not houses_data:
            raise HTTPException(status_code=400, detail="Failed to calculate chart data")
        
        # The houses_data is already in the correct format
        return ChartResponse(houses=houses_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input data: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating chart: {str(e)}")

@router.post("/d9", response_model=ChartResponse)
async def get_d9_chart(request: ChartRequest):
    try:
        houses_data = calculate_d9_chart(
            name=request.name,
            dob=request.dob,
            tob=request.tob,
            latitude=request.latitude,
            longitude=request.longitude
        )
        
        if not houses_data:
            raise HTTPException(status_code=400, detail="Failed to calculate chart data")
        
        # The houses_data is already in the correct format
        return ChartResponse(houses=houses_data)
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