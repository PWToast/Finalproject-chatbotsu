import pymongo
from datetime import datetime, timezone

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["chatbot_conversation"]

def save_conversation(user_id,platform,response):
    mycol = mydb["chat_history"]
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
    mycol.insert_one(mydict)

def update_daily_stats(platform,response):
    mycol = mydb["daily_stats"]
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
    
    mycol.update_one(
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