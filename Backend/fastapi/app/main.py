from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.web_chatbot import router as chatbot_router
from app.api.web_dashboard import router as dashboard_router
from app.api.web_conversation import router as conversation_router
from app.api.insert_and_delete_docs import router as file_router
from app.api.auth import router as auth_router
# from app.api.line_webhook import router as line_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chatbot_router)
app.include_router(dashboard_router)
app.include_router(conversation_router)
app.include_router(file_router)
app.include_router(auth_router)
# app.include_router(line_router)

#cd backend/fastapi
#.venv\Scripts\activate
#uvicorn app.main:app --reload

#ถ้าใช้ไลน์ด้วยรัน ngrok http --url=suzan-uneloquent-grossly.ngrok-free.dev 8000
#ไม่ต้องเปลี่ยนที่ line console แล้ว

