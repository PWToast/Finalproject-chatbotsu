from datetime import datetime
from pymongo import MongoClient
from pydantic import BaseModel
from fastapi import APIRouter
from dotenv import load_dotenv

router = APIRouter(prefix="", tags=["web_history"])

load_dotenv()

client = MongoClient("mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.5.10")
db = client["mydb"]
collection = db["web_chat_history"]

class Historyschema(BaseModel):
    email: str
    session_id: str
    platform: str
    timestamp: datetime
    user_message: str
    ai_message: str
    question_agency: str
    is_fallback: bool

#@router.post("/insertchat")
def insert_chat(schema: Historyschema):
    message = schema.model_dump()
    result = collection.insert_one(message)
    print("insert ok")

def fetch_by_sessionId(email: str, session_id: str):
    cursor = collection.find(
        {"email": email, "session_id": session_id},
        {"_id": 0, "user_message": 1, "ai_message":1}
        ).sort("timestamp", 1)
    result = []
    for doc in cursor:
        #doc["_id"] = str(doc["_id"])  # แปลง ObjectId เป็น string ก่อน เพราะ objectId แปลงเป็น json ตรงๆไม่ได้
        #if "timestamp" in doc:
        #    doc["timestamp"] = doc["timestamp"].isoformat()  # แปลง datetime เป็น string
        result.append(doc)
        
    return result