from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from .service import generate_astrology_report
from ..astrology.models import ChartHouse

router = APIRouter()

class ReportRequest(BaseModel):
    name: str
    dob: str
    tob: str
    pob: str
    lagna_chart: List[ChartHouse]
    navamsa_chart: List[ChartHouse]
    chart_image_base64: Optional[str] = None

@router.post("/generate-report")
async def generate_report(request: ReportRequest):
    """
    Generate an astrological report using the provided chart data and Gemini AI.
    """
    try:
        report = await generate_astrology_report(
            name=request.name,
            dob=request.dob,
            tob=request.tob,
            pob=request.pob,
            lagna_chart=request.lagna_chart,
            navamsa_chart=request.navamsa_chart,
            chart_image_base64=request.chart_image_base64
        )
        return {"report": report}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 