from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from typing import Optional
import math
import uuid

from app.core.database import get_db
from app.models.supplier import Supplier
from app.schemas.supplier import SupplierResponse
from app.schemas.common import PaginatedResponse, PaginationMeta

router = APIRouter()

ALLOWED_SORT_SUPPLIER = frozenset({
    "total_awarded_12m", "awards_count_12m", "name", "created_at"
})


@router.get("", response_model=PaginatedResponse, summary="Listar proveedores")
async def list_suppliers(
    query: Optional[str] = Query(None, description="Buscar por nombre o RIF"),
    rif: Optional[str] = Query(None),
    sanction_status: Optional[str] = Query(None, description="active|sanctioned|suspended"),
    sector: Optional[str] = Query(None),
    state: Optional[str] = Query(None, description="Estado de Venezuela"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    sort: str = Query("total_awarded_12m"),
    order: str = Query("desc"),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Supplier)

    if query:
        stmt = stmt.where(
            or_(
                Supplier.name.ilike(f"%{query}%"),
                Supplier.rif.ilike(f"%{query}%"),
            )
        )
    if rif:
        stmt = stmt.where(Supplier.rif == rif)
    if sanction_status:
        stmt = stmt.where(Supplier.sanction_status == sanction_status)
    if sector:
        stmt = stmt.where(Supplier.sector.ilike(f"%{sector}%"))
    if state:
        stmt = stmt.where(Supplier.state == state)

    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = (await db.execute(count_stmt)).scalar()

    sort_field = sort if sort in ALLOWED_SORT_SUPPLIER else "total_awarded_12m"
    sort_col = getattr(Supplier, sort_field)
    stmt = stmt.order_by(sort_col.asc() if order == "asc" else sort_col.desc())

    offset = (page - 1) * page_size
    stmt = stmt.offset(offset).limit(page_size)

    result = await db.execute(stmt)
    suppliers = result.scalars().all()

    return PaginatedResponse(
        meta=PaginationMeta(
            page=page, page_size=page_size,
            total_results=total,
            total_pages=math.ceil(total / page_size),
            sort=sort, order=order,
        ),
        data=[SupplierResponse.model_validate(s) for s in suppliers]
    )


@router.get("/{supplier_id}", response_model=SupplierResponse, summary="Obtener proveedor por ID")
async def get_supplier(supplier_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Supplier).where(Supplier.id == supplier_id))
    supplier = result.scalar_one_or_none()
    if not supplier:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return SupplierResponse.model_validate(supplier)
