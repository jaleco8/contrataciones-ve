from sqlalchemy import Column, String, Numeric, DateTime, text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.core.database import Base
import uuid


class RiskAlert(Base):
    __tablename__ = "risk_alerts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = Column(String(100), nullable=False)
    severity = Column(String(20), nullable=False, default="medium")
    status = Column(String(50), nullable=False, default="open")
    score = Column(Numeric(4, 3), nullable=False, default=0.500)
    contract_id = Column(UUID(as_uuid=True), ForeignKey("contracts.id"))
    process_id = Column(UUID(as_uuid=True), ForeignKey("processes.id"))
    supplier_id = Column(UUID(as_uuid=True), ForeignKey("suppliers.id"))
    explanation = Column(JSONB, nullable=False, default=list)
    supporting_data = Column(JSONB, default=dict)
    reviewed_by = Column(String(200))
    reviewed_at = Column(DateTime(timezone=True))
    review_notes = Column(String)
    generated_at = Column(DateTime(timezone=True), server_default=text("NOW()"))
    updated_at = Column(DateTime(timezone=True), server_default=text("NOW()"))
