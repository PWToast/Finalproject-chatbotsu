# schemas/prompt_schema.py
from pydantic import BaseModel
from typing import List

class MessageItem(BaseModel):
    role: str  # system / human
    content: str

class UpdatePromptRequest(BaseModel):
    node_id: str
    messages: List[MessageItem]

class PromptResponse(BaseModel):
    node_id: str
    messages: List[MessageItem]