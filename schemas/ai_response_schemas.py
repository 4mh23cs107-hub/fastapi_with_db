from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AIRequest(BaseModel):
    message: str
    system_prompt: str = "You are a helpful assistant." 
    conversation_id: Optional[int] = None

class ConversationSchema(BaseModel):
    id: int
    title: Optional[str] = None
    created_at: datetime
    class Config:
        from_attributes = True 

class AIResponse(BaseModel):
    response: str
    conversation_id: int

from datetime import datetime

class ChatMessage(BaseModel):
    role: str
    content: str
    timestamp: datetime

    class Config:
        from_attributes = True

