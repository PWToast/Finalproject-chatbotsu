from fastapi import APIRouter, Query
from datetime import datetime
from collections import defaultdict
from datetime import datetime, timedelta
from pymongo import MongoClient

from app.schemas.chat import ListConversationResponse

router = APIRouter(prefix="/admin", tags=["web_conversation"])

client = MongoClient("mongodb://localhost:27017/")
db = client["chatbot_conversation"]
collection = db["chat_history"]

@router.get("/conversation",response_model=ListConversationResponse)
def get_conversation(filter: str = Query("กองบริหารวิชาการ"),page: int = Query(default=1, ge=1) ):
    page_size = 10
    skip_value = (page - 1) * page_size

    pipeline = [
        { "$match": { "question_agency": filter } },
        { "$sort": { "timestamp": 1 } },#-1เก่าไปใหม่ ,1 ใหม่ไปเก่า

        { "$skip": skip_value },#ข้ามตามจำนวนรายการแรกที่หาเจอ
        
        { "$limit": page_size },#ดึง10อัน
        {
            "$project": {
                "_id": 0,
                "user_message": 1,
                "ai_message": 1,
                "timestamp": 1,
                "platform": 1,
                "question_agency": 1,
                "rewrite_message": 1,
                "is_fallback": 1
            }
        }
    ]
    results = list(collection.aggregate(pipeline))
    print(results)
    return {"items":results}