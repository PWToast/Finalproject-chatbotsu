from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from llm_service import LLMChat
class MessageInput(BaseModel):
    message : str


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

"""allow_origins=["*"] เฉพาะตอน dev เท่านั้น"""

@app.get("/")
def hello():
    return {"message": "hello"}


@app.post("/response")
def create_response(input: MessageInput):
    LLMmessage = LLMChat(input.message)
    return {"response": LLMmessage}

