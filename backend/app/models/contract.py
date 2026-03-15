from sqlalchemy import Column, String, Numeric, DateTime, Date, Boolean, Integer, text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
import uuid


class Contract(Base):
    __tablename__ = "contracts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    contract_number = Column(String(200), unique=True, nullable=False)
    process_id = Column(UUID(as_uuid=True), ForeignKey("processes.id"))
    supplier_id = Column(UUID(as_uuid=True), ForeignKey("suppliers.id"))
    supplier_name = Column(String(500), nullable=False)
    buyer_name = Column(String(500), nullable=False)
    buyer_id = Column(String(100))
    title = Column(String(1000), nullable=False)
    description = Column(String)
    category = Column(String(200))
    status = Column(String(50), nullable=False, default="draft")
    amount = Column(Numeric(20, 2), nullable=False)
    currency = Column(String(10), default="USD")
    original_amount = Column(Numeric(20, 2))
    signed_at = Column(Date)
    start_date = Column(Date)
    end_date = Column(Date)
    has_amendments = Column(Boolean, default=False)
    amendments_count = Column(Integer, default=0)
    amendment_amount_increase = Column(Numeric(20, 2), default=0.00)
    created_at = Column(DateTime(timezone=True), server_default=text("NOW()"))
    updated_at = Column(DateTime(timezone=True), server_default=text("NOW()"))
    status_changed_at = Column(DateTime(timezone=True))


class ContractAmendment(Base):
    __tablename__ = "contract_amendments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    contract_id = Column(UUID(as_uuid=True),
                         ForeignKey("contracts.id", ondelete="CASCADE"), nullable=False)
    amendment_number = Column(Integer, nullable=False)
    description = Column(String)
    original_amount = Column(Numeric(20, 2))
    new_amount = Column(Numeric(20, 2))
    amount_change = Column(Numeric(20, 2))
    original_end_date = Column(Date)
    new_end_date = Column(Date)
    signed_at = Column(Date)
    created_at = Column(DateTime(timezone=True), server_default=text("NOW()"))


class ContractPayment(Base):
    __tablename__ = "contract_payments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    contract_id = Column(UUID(as_uuid=True),
                         ForeignKey("contracts.id", ondelete="CASCADE"), nullable=False)
    payment_number = Column(Integer, nullable=False)
    amount = Column(Numeric(20, 2), nullable=False)
    currency = Column(String(10), default="USD")
    status = Column(String(50), default="paid")
    payment_date = Column(Date)
    description = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=text("NOW()"))
