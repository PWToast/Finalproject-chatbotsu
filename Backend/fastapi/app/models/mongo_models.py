from typing import Optional
from datetime import datetime, date
from beanie import Document
from pydantic import Field, BaseModel
from typing import Dict

class ChatHistory(Document):
    user_id: str
    platform: str  #web, line
    timestamp: datetime = Field(default_factory=datetime.now)
    user_message: str
    ai_message: str
    question_agency: str
    is_fallback: bool = False
    
    #ฟิลด์ที่เว็บมี แต่ไลน์ไม่มี
    message_id: Optional[str] = None
    session_id: Optional[str] = None

    class Settings:
        name = "chat_history"

class DailyStats(Document):
    date: date  
    chat_web_count: int = 0
    chat_line_count: int = 0
    chat_fallback_count: int = 0
    chat_success_count: int = 0

    agencies: Dict[str, int] = {} # "กองบริหาร": 1, "กองกิจ": 20: "สำนักดิจิ": 3"

    class Settings:
        name = "daily_stats"


class Historyschema(BaseModel):
    email: str
    session_id: str
    platform: str
    timestamp: datetime
    user_message: str
    ai_message: str
    question_agency: str
    is_fallback: bool