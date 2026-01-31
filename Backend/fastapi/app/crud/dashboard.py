import pymongo
from datetime import datetime, timedelta
from app.models.mysql_models import User
from .database import SessionLocal
from sqlalchemy import func
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["chatbot_conversation"]

def get_summary():
    collection = mydb["daily_stats"]
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
    result = list(collection.aggregate(pipeline))

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
    

    # sql
    #นับแยก platform
    stats = db.query(
        User.platform, 
        func.count(User.id).label('count')
    ).group_by(User.platform).all()

    platform_stats = {row.platform: row.count for row in stats}
    #นับรวม
    total_users = db.query(func.count(User.id)).scalar()
    return {
        "total_chat_web": summary.get("total_chat_web", 0),
        "total_chat_line": summary.get("total_chat_line", 0),
        "total_success": summary.get("total_success", 0),
        "total_fallback": summary.get("total_fallback", 0),
        "total_agencies": total_agencies
    }

def get_user_trend(range):
    collection = mydb["daily_stats"]

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
    print(f"มีข้อมูลทั้งหมด: {len(results)}")
    chart_data = [
        {
            "label": item["_id"],
            "web_count": item["web_count"],
            "line_count": item["line_count"]
        } for item in results
    ]
    # for item in chart_data:
    #     print(f"Label: {item['label']}, Web: {item['web_count']}, Line: {item['line_count']}")
    return {"data": chart_data}