from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql import func

from app.database import Base


class AuditEntry(Base):
    __tablename__ = "audit_log"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String(40), nullable=False)
    entity = Column(String(40), nullable=False)
    entity_id = Column(Integer)
    before = Column(JSON)
    after = Column(JSON)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
