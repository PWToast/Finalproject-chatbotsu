from pymongo import MongoClient
from app.config.prompt import DEFAULT_PROMPTS

client = MongoClient("mongodb://localhost:27017/")
db = client["chatbot_conversation"]
collection = db["prompts"]

def get_db_prompt(node_id: str):

    return collection.find_one({"node_id": node_id})

def upsert_db_prompt(data: dict):
    node_id = data.get("node_id")
    messages = data.get("messages")

    return collection.update_one(
        {"node_id": node_id},
        {"$set": {"messages": messages}},
        upsert=True
    )

def delete_db_prompt(node_id: str):
    return collection.delete_one({"node_id": node_id})

def get_final_prompt(node_id: str):
    # prompt ที่ llm ใช้
    db_data = get_db_prompt(node_id)
    if db_data:
        
        messages = db_data.get("messages", [])
        system = next((m["content"] for m in messages if m["role"] == "system"), "")
        human = next((m["content"] for m in messages if m["role"] == "human"), "")
        return system, human

    # ถ้าไม่มีใน DB ให้ใช้ Default
    default = DEFAULT_PROMPTS.get(node_id)
    return default["system"], default["human"]