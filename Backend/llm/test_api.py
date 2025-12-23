from pydantic import BaseModel
from fastapi import FastAPI
import chromadb
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from test_chat_rag_memory import chat_rag_memory
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


client = chromadb.PersistentClient(path="./chroma_db")
embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-m3")
vector_store_from_client = Chroma(
    client=client,
    collection_name="chatbot_rag_documents",
    embedding_function=embedding_model,
)

class Item(BaseModel):
    message: str

@app.get("/")
def hello():
    return {"message": "hello"}

@app.post("/chat_rag_memory")
def llm_chat(item: Item):
    #ส่งคำถาม,ตัว embedding, user_id(คือthread_id)
    answer,agency = chat_rag_memory(item.message,vector_store_from_client,"test_user_id")
    #เรียกฟังชันเก็บลง db ได้ตรงนี้
    #
    return {"response": answer}

#.venv\Scripts\activate
#uvicorn test_api:app --reload