import pymongo
from datetime import datetime, timezone, timedelta
import math

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["chatbot_conversation"]

def save_conversation(user_id,platform,response):
    collection = mydb["chat_history"]
    mydict = { "user_id": user_id,
               "platform": platform,
               "timestamp": datetime.now(timezone.utc),
               "user_message": response["user_message"],
               "rewritten_question": response["rewritten_question"],
               "ai_message": response["ai_message"], 
               "question_agency": response["question_agency"],
               "is_fallback": response["is_fallback"]
            }#เว็บมี session_id กับ message_idด้วย
    print(mydict)
    collection.insert_one(mydict)

def update_daily_stats(platform,response):
    collection = mydb["daily_stats"]
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    inc_data = {}
    if platform.lower() == "line":
        platform_to_inc = "chat_line_count"
    else:
        platform_to_inc = "chat_web_count"

    if response.get("is_fallback") is False:
        status_to_inc = "chat_success_count"
    else:
        status_to_inc = "chat_fallback_count"

    agency = response.get("question_agency","อื่นๆ")
    inc_data[f"agencies.{agency}"] = 1 #agencies.กองบริหารวิชาการ / สำนัก/ กองกิจ
    
    agencies_default = {
        "กองบริหารวิชาการ": 0,
        "สำนักดิจิทัลเทคโนโลยี": 0,
        "กองกิจการนักศึกษา": 0,
        "อื่นๆ": 0
    }
    if agency in agencies_default:
        agencies_default.pop(agency)

    set_default_log = {
        "date": today,
        "chat_line_count": 0,
        "chat_web_count": 0,
        "chat_success_count": 0,
        "chat_fallback_count": 0,
    }
    #popออกค่าเก่าเพื่อเตรียมอัปเดต
    set_default_log.pop(platform_to_inc)
    set_default_log.pop(status_to_inc)

    for name, value in agencies_default.items():
        set_default_log[f"agencies.{name}"] = value
    
    collection.update_one(
        {"date": today},
        {
            "$inc": {
                platform_to_inc: 1,
                status_to_inc: 1,
                f"agencies.{agency}": 1
            },
            "$setOnInsert": set_default_log
        },
        upsert=True
    )
    print("updated")

def get_conversations(agency, platform, is_fallback, time_range,sortDate, page):
    collection = mydb["chat_history"]
    query = {}

    if agency:
        query["question_agency"] = agency 
    if platform:
        query["platform"] = platform
    if is_fallback == "true":
        query["is_fallback"] = True
    elif is_fallback == "false":
        query["is_fallback"] = False

    if time_range and str(time_range).isdigit():  
        days = int(time_range)
    else:
        days = 7
    start_date = datetime.now(timezone.utc) - timedelta(days=days)
    query["timestamp"] = {"$gte": start_date}

    if sortDate == "new":
        sort = -1
    else:
        sort = 1


    page_size = 10
    skip_value = (page - 1) * page_size

    count = collection.count_documents(query)
    total_pages = math.ceil(count / page_size)
    # print(f"Total docs: {count}")

    pipeline = [
        { "$match": query },
        { "$sort": { "timestamp": sort } },#-1ใหม่ไปเก่า ,1 เก่าไปใหม่
        { "$skip": skip_value },#ข้ามตามจำนวนรายการแรกที่หาเจอ
        { "$limit": page_size },#ดึง10อัน
        { "$project": {
                "_id": 0,
                "user_message": 1,
                "ai_message": 1,
                "timestamp": { 
                    "$dateToString": { "format": "%Y-%m-%dT%H:%M:%SZ", "date": "$timestamp" } 
                },
                "platform": 1,
                "question_agency": 1,
                "rewritten_question": 1,
                "is_fallback": 1
            }
        }
    ]
    results = list(collection.aggregate(pipeline))
    # print(results)
    return results,total_pages