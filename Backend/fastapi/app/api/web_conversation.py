from fastapi import APIRouter, Query

from app.schemas.chat import ListConversationResponse
from app.crud.update_history import get_conversations

router = APIRouter(prefix="/admin", tags=["web_conversation"])

#ต้องแก้เป็น schemas
@router.get("/conversation",response_model=ListConversationResponse)
def get_conversation(agency: str = Query(None),platform: str = Query(None),
                     status_fallback: str = Query(None),timeRange: str = Query("7"), 
                     sortDate: str = Query("new"),page: int = Query(default=1, ge=1) ):
    
    results,total_pages = get_conversations(agency, platform,status_fallback,timeRange,sortDate,page)

    return {"items":results, "total_pages":total_pages}