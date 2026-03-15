from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from typing import Optional
from datetime import date
import math
import uuid

from app.core.database import get_db
from app.models.contract import Contract
from app.schemas.contract import ContractResponse
from app.schemas.common import PaginatedResponse, PaginationMeta

router = APIRouter()

ALLOWED_SORT_CONTRACT = frozenset({
    "signed_at", "amount", "updated_at", "created_at",
    "start_date", "end_date", "amendments_count"
})


@router.get("", response_model=PaginatedResponse, summary="Listar contratos")
async def list_contracts(
    query: Optional[str] = Query(None),
    buyer_name: Optional[str] = Query(None),
    supplier_name: Optional[str] = Query(None),
    status: Optional[str] = Query(None, description="draft|active|completed|terminated|cancelled"),
    category: Optional[str] = Query(None),
    has_amendments: Optional[bool] = Query(None),
    min_amount: Optional[float] = Query(None),
    max_amount: Optional[float] = Query(None),
    currency: Optional[str] = Query(None),
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    time_field: str = Query("signed_at", description="signed_at|updated_at"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    sort: str = Query("signed_at"),
    order: str = Query("desc"),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Contract)

    if query:
        stmt = stmt.where(
            or_(
                Contract.title.ilike(f"%{query}%"),
                Contract.supplier_name.ilike(f"%{query}%"),
                Contract.buyer_name.ilike(f"%{query}%"),
                Contract.contract_number.ilike(f"%{query}%"),
            )
        )
    if buyer_name:
        stmt = stmt.where(Contract.buyer_name.ilike(f"%{buyer_name}%"))
    if supplier_name:
        stmt = stmt.where(Contract.supplier_name.ilike(f"%{supplier_name}%"))
    if status:
        stmt = stmt.where(Contract.status == status)
    if category:
        stmt = stmt.where(Contract.category == category)
    if has_amendments is not None:
        stmt = stmt.where(Contract.has_amendments == has_amendments)
    if min_amount is not None:
        stmt = stmt.where(Contract.amount >= min_amount)
    if max_amount is not None:
        stmt = stmt.where(Contract.amount <= max_amount)
    if currency:
        stmt = stmt.where(Contract.currency == currency)

    # Filtro temporal
    time_col = Contract.updated_at if time_field == "updated_at" else Contract.signed_at
    if date_from:
        stmt = stmt.where(time_col >= date_from)
    if date_to:
        stmt = stmt.where(time_col < date_to)

    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = (await db.execute(count_stmt)).scalar()

    sort_field = sort if sort in ALLOWED_SORT_CONTRACT else "signed_at"
    sort_col = getattr(Contract, sort_field)
    stmt = stmt.order_by(sort_col.asc() if order == "asc" else sort_col.desc())

    offset = (page - 1) * page_size
    stmt = stmt.offset(offset).limit(page_size)

    result = await db.execute(stmt)
    contracts = result.scalars().all()

    return PaginatedResponse(
        meta=PaginationMeta(
            page=page, page_size=page_size,
            total_results=total,
            total_pages=math.ceil(total / page_size),
            sort=sort, order=order,
        ),
        data=[ContractResponse.model_validate(c) for c in contracts]
    )


@router.get("/{contract_id}", response_model=ContractResponse, summary="Obtener contrato por ID")
async def get_contract(contract_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Contract).where(Contract.id == contract_id))
    contract = result.scalar_one_or_none()
    if not contract:
        raise HTTPException(status_code=404, detail="Contrato no encontrado")
    return ContractResponse.model_validate(contract)
