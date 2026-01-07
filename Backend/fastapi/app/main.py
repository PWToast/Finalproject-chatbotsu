from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.web_chatbot import router as chatbot_router
from app.api.line_webhook import router as line_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chatbot_router)
app.include_router(line_router)

#.venv\Scripts\activate
#uvicorn app.main:app --reload

#ถ้าใช้ไลน์ด้วยรัน ngrok http --url=suzan-uneloquent-grossly.ngrok-free.dev 8000
#ไม่ต้องเปลี่ยนที่ line console แล้ว