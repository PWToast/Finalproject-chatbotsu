from fastapi import APIRouter
from app.services.dashboard.dashboard_service import overview_count
router = APIRouter(prefix="/admin", tags=["Admin Dashboard"])

@router.get("/overview")
def get_overview():
    overview_data = overview_count() #ยังเหลือข้อมูล ตอบได้กับ ตอบไม่ได้
    return overview_data