from fastapi import APIRouter,Depends
from typing import Annotated
from app.schemas.chat import ListConversationResponse,QueryFilters
from app.crud.conversation import get_conversations

router = APIRouter(prefix="/admin", tags=["web_conversation"])

@router.get("/conversation",response_model=ListConversationResponse)
def get_conversation(filters: Annotated[QueryFilters, Depends()]):
    results,total_pages = get_conversations(filters)
    return {"items":results, "total_pages":total_pages}