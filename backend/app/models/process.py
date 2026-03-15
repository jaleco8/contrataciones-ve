from sqlalchemy import Column, String, Integer, Numeric, DateTime, Date, text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
import uuid


class Process(Base):
    __tablename__ = "processes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ocid = Column(String(100), unique=True)
    title = Column(String(1000), nullable=False)
    description = Column(String)
    status = Column(String(50), nullable=False, default="planned")
    procurement_method = Column(String(100))
    buyer_name = Column(String(500), nullable=False)
    buyer_id = Column(String(100))
    buyer_entity_type = Column(String(100))
    tender_amount = Column(Numeric(20, 2))
    tender_currency = Column(String(10), default="USD")
    awarded_amount = Column(Numeric(20, 2))
    awarded_currency = Column(String(10), default="USD")
    awarded_supplier_id = Column(UUID(as_uuid=True), ForeignKey("suppliers.id"))
    awarded_supplier_name = Column(String(500))
    published_at = Column(DateTime(timezone=True))
    tender_start_date = Column(Date)
    tender_end_date = Column(Date)
    award_date = Column(Date)
    category = Column(String(200))
    cpv_code = Column(String(50))
    bidders_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=text("NOW()"))
    updated_at = Column(DateTime(timezone=True), server_default=text("NOW()"))
