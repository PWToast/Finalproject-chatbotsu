
from fastapi import APIRouter
from pydantic import BaseModel

import chromadb
from datetime import datetime, timezone
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from app.services.llm.test_chat_rag_memory import chat_rag_memory
from app.api.web_history import insert_chat, fetch_by_sessionId, Historyschema
from app.crud.conversation import update_daily_stats

router = APIRouter(prefix="", tags=["chatbot"])

client = chromadb.PersistentClient(path="app/services/llm/chroma_db")  #ดู path folderให้ถูกต้อง
embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-m3")
vector_store_from_client = Chroma(
    client=client,
    collection_name="chatbot_rag_documents",
    embedding_function=embedding_model,
)

class Item(BaseModel):
    message: str
    email: str
    session_id: str


@router.get("/")
def hello():
    return {"message": "hello"}

@router.post("/chat_rag_memory")
def llm_chat(item: Item):
    #ส่งคำถาม,ตัว embedding, user_id(คือthread_id)
    #answer,agency,is_fallback
    response = chat_rag_memory(item.message,vector_store_from_client, item.session_id)
    answer = response["ai_message"]
    agency = response["question_agency"]
    is_fallback = response["is_fallback"]
    # ต้องรับ message, email(jwt), session_id(frontend) จาก api 
    message_to_database = Historyschema(
        email = item.email,
        session_id = item.session_id,
        platform = "Website",
        timestamp = datetime.now(timezone.utc),
        user_message = item.message,
        ai_message = answer,
        question_agency = agency,
        is_fallback = is_fallback
    )
    insert_chat(message_to_database)
    update_daily_stats("WEB",response)
    #เรียกฟังชันเก็บลง db ได้ตรงนี้
    return {"response": answer}

@router.get("/fetch/{email}/{session_id}")
def fecthHistory(email: str, session_id: str):
    result = fetch_by_sessionId(email, session_id)
    return {"response" : result}

