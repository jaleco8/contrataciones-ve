from sqlalchemy import Column, String, Integer, Numeric, DateTime, text
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
import uuid


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    rif = Column(String(20), unique=True, nullable=False)
    name = Column(String(500), nullable=False)
    legal_name = Column(String(500))
    sector = Column(String(200))
    type = Column(String(50), default="company")
    sanction_status = Column(String(50), default="active")
    awards_count_12m = Column(Integer, default=0)
    total_awarded_12m = Column(Numeric(20, 2), default=0.00)
    address = Column(String)
    state = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=text("NOW()"))
    updated_at = Column(DateTime(timezone=True), server_default=text("NOW()"))
