from pydantic import BaseModel
from typing import Dict, List

class StatsSummaryResponse(BaseModel):
    total_chat_web: int
    total_chat_line: int
    total_success: int  
    total_fallback: int
    total_agencies: Dict[str, int]

from pydantic import BaseModel
from typing import List

class TrendData(BaseModel):
    label: str       # range 7 30 years
    web_count: int   # เส้นที่ 1
    line_count: int  # เส้นที่ 2

class UserTrendResponse(BaseModel):
    data: List[TrendData]