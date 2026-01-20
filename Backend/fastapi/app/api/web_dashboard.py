from fastapi import APIRouter, Query
from datetime import datetime
from collections import defaultdict
from datetime import datetime, timedelta
from pymongo import MongoClient

from app.models.mongo_models import DailyStats
from app.schemas.dashboard import StatsSummaryResponse,UserTrendResponse

router = APIRouter(prefix="/admin", tags=["web_dashboard"])

client = MongoClient("mongodb://localhost:27017/")
db = client["chatbot_conversation"]
collection = db["daily_stats"]

@router.get("/summary",response_model=StatsSummaryResponse)
def get_stats_summary():
    pipeline = [
        {
            "$group": {
                "_id": None,
                "total_chat_web": { "$sum": "$chat_web_count" },
                "total_chat_line": { "$sum": "$chat_line_count" },
                "total_fallback": { "$sum": "$chat_fallback_count" },
                "total_success": { "$sum": "$chat_success_count" },
            }
        }
    ]
    
    cursor = collection.aggregate(pipeline)
    result = list(cursor)

    if not result:
        print("not found result!")
        return {
            "total_chat_web": 0,
            "total_chat_line": 0,
            "total_fallback": 0,
            "total_success": 0,
            "total_agencies": {}
        }
    
    summary = result[0]

    all_data =  collection.find().to_list(None)
    total_agencies = {}
    for day in all_data:
        for agency, count in day.get("agencies", {}).items():
            total_agencies[agency] = total_agencies.get(agency, 0) + count

    return {
        "total_chat_web": summary.get("total_chat_web", 0),
        "total_chat_line": summary.get("total_chat_line", 0),
        "total_success": summary.get("total_success", 0),
        "total_fallback": summary.get("total_fallback", 0),
        "total_agencies": total_agencies
    }

@router.get("/user-trend", response_model=UserTrendResponse)
def get_user_trend(range: str = Query("7days")): #มี7วันล่าสุด,30วันล่าสุด,ปีนี้
    now = datetime.now()
    start_date = None
    group_format = "%Y-%m-%d"
    print(range)
    if range == "7days":
        start_date = now - timedelta(days=7)
    elif range == "30days":
        start_date = now - timedelta(days=30)
    elif range == "year":
        start_date = datetime(now.year, 1, 1)
        group_format = "%Y-%m"

    pipeline = [
        { "$match": { "date": { "$gte": start_date } } },
        {
            "$group": {
                "_id": { "$dateToString": { "format": group_format, "date": "$date" } },
                "web_count": { "$sum": "$chat_web_count" },
                "line_count": { "$sum": "$chat_line_count" }
            }
        },
        { "$sort": { "_id": 1 } } #เรียงจากเก่าไปใหม่
    ]

    results = list(collection.aggregate(pipeline))
    print(f"DEBUG: Found {len(results)} records from MongoDB")
    chart_data = [
        {
            "label": item["_id"],
            "web_count": item["web_count"],
            "line_count": item["line_count"]
        } for item in results
    ]
    for item in chart_data:
        print(f"Label: {item['label']}, Web: {item['web_count']}, Line: {item['line_count']}")
    return {"data": chart_data}

