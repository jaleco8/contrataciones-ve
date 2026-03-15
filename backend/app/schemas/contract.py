from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
import uuid


class ContractResponse(BaseModel):
    id: uuid.UUID
    contract_number: str
    process_id: Optional[uuid.UUID] = None
    supplier_id: Optional[uuid.UUID] = None
    supplier_name: str
    buyer_name: str
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    status: str
    amount: float
    currency: str = "USD"
    original_amount: Optional[float] = None
    signed_at: Optional[date] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    has_amendments: bool = False
    amendments_count: int = 0
    amendment_amount_increase: float = 0.0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
