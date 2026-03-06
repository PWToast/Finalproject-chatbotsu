from datetime import datetime
from pymongo import MongoClient
from pydantic import BaseModel
from fastapi import APIRouter
import os
from dotenv import load_dotenv
from app.models.mongo_models import Historyschema
import pymongo
router = APIRouter(prefix="", tags=["web_history"])

load_dotenv()
#mongo = "mongodb://localhost:27017/"
Mongo_host = os.getenv("MONGO_URL")
myclient = pymongo.MongoClient(Mongo_host)
db = myclient["chatbot_conversation"]
collection = db["chat_history"]

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