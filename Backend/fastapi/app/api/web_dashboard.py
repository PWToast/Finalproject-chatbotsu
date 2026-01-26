from fastapi import APIRouter, Query
from app.schemas.dashboard import StatsSummaryResponse,UserTrendResponse
from app.crud.dashboard import get_summary,get_user_trend

router = APIRouter(prefix="/admin", tags=["web_dashboard"])

@router.get("/summary",response_model=StatsSummaryResponse)
def get_stats_summary(): #overview,กราฟแท่ง
    summary_data = get_summary()
    return summary_data

@router.get("/user-trend", response_model=UserTrendResponse)
def get_stats_user_trend(range: str = Query("7days")): #มี7วันล่าสุด,30วันล่าสุด,ปีนี้
    trend_data = get_user_trend(range)
    return trend_data

