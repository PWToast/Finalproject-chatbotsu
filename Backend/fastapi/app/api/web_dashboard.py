from fastapi import APIRouter, Query,Depends
from app.schemas.dashboard import StatsSummaryResponse,UserTrendResponse
from app.crud.dashboard import get_summary,get_user_trend
from app.api.auth import admin_required
router = APIRouter(prefix="/admin", tags=["web_dashboard"])

@router.get("/summary",response_model=StatsSummaryResponse)
def get_stats_summary(current_admin: dict = Depends(admin_required)): #overview,กราฟแท่ง
    print(current_admin["email"])
    summary_data = get_summary()
    return summary_data

@router.get("/user-trend", response_model=UserTrendResponse)
def get_stats_user_trend(range: str = Query("7days"),current_admin: dict = Depends(admin_required)): #มี7วันล่าสุด,30วันล่าสุด,ปีนี้
    print(current_admin["email"])
    trend_data = get_user_trend(range)
    return trend_data

