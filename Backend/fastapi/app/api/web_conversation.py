from fastapi import APIRouter,Depends
from typing import Annotated
from app.schemas.chat import ListConversationResponse,QueryFilters
from app.crud.conversation import get_conversations
from app.api.auth import admin_required

router = APIRouter(prefix="/admin", tags=["web_conversation"])

@router.get("/conversation",response_model=ListConversationResponse)
def get_conversation(filters: Annotated[QueryFilters, Depends()],current_admin: dict = Depends(admin_required)):
    results,total_pages = get_conversations(filters)
    print(current_admin["email"])
    return {"items":results, "total_pages":total_pages}