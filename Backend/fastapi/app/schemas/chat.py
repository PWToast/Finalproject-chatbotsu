from pydantic import BaseModel
from typing import Dict, List,Optional
from datetime import datetime

class ConversationResponse(BaseModel):
    timestamp: datetime
    platform: str
    user_message: str  
    ai_message: str
    question_agency : str
    is_fallback: bool
    rewrite_message: Optional[str] = None

class ListConversationResponse(BaseModel):
    items: List[ConversationResponse]