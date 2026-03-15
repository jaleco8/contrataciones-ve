from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid


class SupplierBase(BaseModel):
    rif: str
    name: str
    legal_name: Optional[str] = None
    sector: Optional[str] = None
    type: str = "company"
    sanction_status: str = "active"
    state: Optional[str] = None


class SupplierResponse(SupplierBase):
    id: uuid.UUID
    awards_count_12m: int = 0
    total_awarded_12m: float = 0.0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
