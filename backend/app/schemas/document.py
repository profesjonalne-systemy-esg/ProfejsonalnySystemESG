from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DocumentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    filename: str
    status: str
    mime_type: str | None
    size_bytes: int | None
    error: str | None
    uploaded_at: datetime
