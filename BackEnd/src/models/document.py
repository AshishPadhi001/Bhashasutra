from sqlalchemy import Column, String, Text, DateTime, Boolean
from sqlalchemy.sql import func
from src.database.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True, index=True)
    filename = Column(String, index=True)
    content = Column(Text)
    embedding_status = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
