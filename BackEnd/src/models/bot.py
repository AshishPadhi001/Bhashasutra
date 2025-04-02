from sqlalchemy import Column, Integer, String, Text, DateTime, func,Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BotResponse(Base):
    __tablename__ = "bot_responses"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String(500), index=True)
    response = Column(Text)
    category = Column(String(100), index=True)
    is_faq = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())