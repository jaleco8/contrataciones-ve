from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from typing import Optional
from datetime import date
import math
import uuid

from app.core.database import get_db
from app.models.process import Process
from app.schemas.process import ProcessResponse
from app.schemas.common import PaginatedResponse, PaginationMeta

router = APIRouter()

ALLOWED_SORT_PROCESS = frozenset({
    "published_at", "award_date", "tender_amount", "awarded_amount", "bidders_count", "created_at"
})


@router.get("", response_model=PaginatedResponse, summary="Listar procesos de contratación")
async def list_processes(
    query: Optional[str] = Query(None, description="Buscar por título o descripción"),
    status: Optional[str] = Query(None, description="planned|tender|awarded|cancelled|complete"),
    buyer_name: Optional[str] = Query(None),
    category: Optional[str] = Query(None, description="obras|bienes|servicios|consultoria"),
    procurement_method: Optional[str] = Query(None),
    date_from: Optional[date] = Query(None, description="Fecha desde (published_at)"),
    date_to: Optional[date] = Query(None, description="Fecha hasta exclusiva (published_at)"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    sort: str = Query("published_at"),
    order: str = Query("desc"),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Process)

    if query:
        stmt = stmt.where(
            or_(
                Process.title.ilike(f"%{query}%"),
                Process.description.ilike(f"%{query}%"),
                Process.buyer_name.ilike(f"%{query}%"),
            )
        )
    if status:
        stmt = stmt.where(Process.status == status)
    if buyer_name:
        stmt = stmt.where(Process.buyer_name.ilike(f"%{buyer_name}%"))
    if category:
        stmt = stmt.where(Process.category == category)
    if procurement_method:
        stmt = stmt.where(Process.procurement_method == procurement_method)
    if date_from:
        stmt = stmt.where(Process.published_at >= date_from)
    if date_to:
        stmt = stmt.where(Process.published_at < date_to)

    # Count
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = (await db.execute(count_stmt)).scalar()

    # Sort
    sort_field = sort if sort in ALLOWED_SORT_PROCESS else "published_at"
    sort_col = getattr(Process, sort_field)
    if order == "asc":
        stmt = stmt.order_by(sort_col.asc())
    else:
        stmt = stmt.order_by(sort_col.desc())

    # Paginate
    offset = (page - 1) * page_size
    stmt = stmt.offset(offset).limit(page_size)

    result = await db.execute(stmt)
    processes = result.scalars().all()

    return PaginatedResponse(
        meta=PaginationMeta(
            page=page,
            page_size=page_size,
            total_results=total,
            total_pages=math.ceil(total / page_size),
            sort=sort,
            order=order,
        ),
        data=[ProcessResponse.model_validate(p) for p in processes]
    )


@router.get("/{process_id}", response_model=ProcessResponse, summary="Obtener proceso por ID")
async def get_process(process_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Process).where(Process.id == process_id))
    process = result.scalar_one_or_none()
    if not process:
        raise HTTPException(status_code=404, detail="Proceso no encontrado")
    return ProcessResponse.model_validate(process)
