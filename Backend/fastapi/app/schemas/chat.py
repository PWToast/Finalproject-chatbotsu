from pydantic import BaseModel,Field
from typing import Dict, List,Optional
from datetime import datetime

class ConversationResponse(BaseModel):
    timestamp: datetime
    platform: str
    user_message: str  
    ai_message: str
    question_agency : str
    is_fallback: bool
    rewritten_question: Optional[str] = None

class ListConversationResponse(BaseModel):
    items: List[ConversationResponse]
    total_pages: int

class QueryFilters(BaseModel):
    agency: Optional[str] = None
    platform: Optional[str] = None
    statusFallback: Optional[str] = None
    timeRange: str = "7"
    sortDate: str = "new"
    page: int = Field(default=1, ge=1)

    class Config:
        populate_by_name = True