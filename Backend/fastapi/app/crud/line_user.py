from app.crud.mysql import get_connection
from mysql.connector import Error
import pymongo
from datetime import datetime, timezone

# def ensure_line_user(line_user_id: str) -> bool: 
#     # ถ้าไม่มี return True ถ้ามีอยู่แล้ว return False
    
#     conn = get_connection()
#     cursor = conn.cursor()
#     timestamp = datetime.now()
#     try:
#         cursor.execute("""INSERT INTO line_users (line_user_id,created_at) 
#             VALUES (%s,%s)""",(line_user_id,timestamp)
#         )
#         conn.commit()
#         return True

#     except Error as e:
#         if e.errno == 1062:
#             return False
#         else:
#             raise e

#     finally:
#         cursor.close()
#         conn.close()


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["chatbot_conversation"]


def save_conversation(user_id,platform,response):
    mycol = mydb["chat_history"]
    mydict = { "user_id": user_id,
               "platform": platform,
               "timestamp": datetime.now(timezone.utc),
               "user_message": response["user_message"],
               "ai_message": response["ai_message"], 
               "question_agency": response["question_agency"],
               "is_fallback": response["is_fallback"]
            }#เว็บมี session_id กับ message_idด้วย
    print(mydict)
    mycol.insert_one(mydict)