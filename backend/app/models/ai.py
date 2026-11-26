from pgvector.sqlalchemy import Vector
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.sql import func

from app.database import Base

EMBEDDING_DIM = 768


class Chunk(Base):
    __tablename__ = "chunks"

    id = Column(Integer, primary_key=True)
    document_id = Column(
        Integer, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True
    )
    page = Column(Integer, nullable=False)
    position = Column(Integer, nullable=False)
    text = Column(Text, nullable=False)
    embedding_model = Column(String(80), nullable=False)
    embedding = Column(Vector(EMBEDDING_DIM), nullable=False)


class LLMCall(Base):
    __tablename__ = "llm_calls"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    task = Column(String(40), nullable=False)
    model = Column(String(80), nullable=False)
    prompt_tokens = Column(Integer, nullable=False, server_default="0")
    completion_tokens = Column(Integer, nullable=False, server_default="0")
    cost_usd = Column(Float, nullable=False, server_default="0")
    cached = Column(Boolean, nullable=False, server_default="false")
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())


class LLMCache(Base):
    __tablename__ = "llm_cache"

    key = Column(String(64), primary_key=True)
    model = Column(String(80), nullable=False)
    response = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
