from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ProjectOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    company_name: str
    year: int
    status: str
    owner_id: int
    created_at: datetime
    updated_at: datetime
