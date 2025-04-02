from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BotResponseBase(BaseModel):
    question: str
    response: str
    category: str
    is_faq: bool = False

class BotResponseCreate(BotResponseBase):
    pass

class BotResponseUpdate(BaseModel):
    question: Optional[str] = None
    response: Optional[str] = None
    category: Optional[str] = None
    is_faq: Optional[bool] = None

class BotResponse(BotResponseBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class BotQuery(BaseModel):
    query: str