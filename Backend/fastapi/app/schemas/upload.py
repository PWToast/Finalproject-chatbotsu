from pydantic import BaseModel

class Metadata(BaseModel):
    topic: str
    category: str
    agency: str
    source: str
    added_at: str

class FormToSend(BaseModel):
    content: str
    metadata: Metadata
