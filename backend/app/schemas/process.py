from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
import uuid


class ProcessResponse(BaseModel):
    id: uuid.UUID
    ocid: Optional[str] = None
    title: str
    description: Optional[str] = None
    status: str
    procurement_method: Optional[str] = None
    buyer_name: str
    buyer_entity_type: Optional[str] = None
    tender_amount: Optional[float] = None
    tender_currency: str = "USD"
    awarded_amount: Optional[float] = None
    awarded_supplier_name: Optional[str] = None
    published_at: Optional[datetime] = None
    award_date: Optional[date] = None
    category: Optional[str] = None
    bidders_count: int = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
