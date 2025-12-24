
from fastapi import APIRouter
from pydantic import BaseModel

import chromadb
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from app.services.llm.test_chat_rag_memory import chat_rag_memory

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

@router.get("/")
def hello():
    return {"message": "hello"}

@router.post("/chat_rag_memory")
def llm_chat(item: Item):
    #ส่งคำถาม,ตัว embedding, user_id(คือthread_id)
    answer,agency = chat_rag_memory(item.message,vector_store_from_client,"test_user_id")
    #เรียกฟังชันเก็บลง db ได้ตรงนี้
    #
    return {"response": answer}
