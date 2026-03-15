from pydantic import BaseModel
from typing import Optional, List, Any, Dict, Literal
from datetime import datetime
import uuid


class RiskAlertResponse(BaseModel):
    id: uuid.UUID
    type: str
    severity: str
    status: str
    score: float
    contract_id: Optional[uuid.UUID] = None
    process_id: Optional[uuid.UUID] = None
    supplier_id: Optional[uuid.UUID] = None
    explanation: List[str] = []
    supporting_data: Dict[str, Any] = {}
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    review_notes: Optional[str] = None
    generated_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class RiskAlertUpdate(BaseModel):
    status: Optional[Literal["open", "reviewed", "dismissed"]] = None
    reviewed_by: Optional[str] = None
    review_notes: Optional[str] = None
