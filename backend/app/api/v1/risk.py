from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional
from datetime import date, datetime, timezone
import math
import uuid

from app.core.database import get_db
from app.core.security import require_api_key
from app.models.risk_alert import RiskAlert
from app.schemas.risk_alert import RiskAlertResponse, RiskAlertUpdate
from app.schemas.common import PaginatedResponse, PaginationMeta

router = APIRouter()

ALLOWED_SORT_ALERT = frozenset({
    "generated_at", "updated_at", "score"
})


@router.get("/alerts", response_model=PaginatedResponse, summary="Listar alertas de riesgo")
async def list_alerts(
    type: Optional[str] = Query(None),
    severity: Optional[str] = Query(None, description="low|medium|high|critical"),
    status: Optional[str] = Query(None, description="open|reviewed|dismissed"),
    contract_id: Optional[str] = Query(None),
    supplier_id: Optional[str] = Query(None),
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    time_field: str = Query("generated_at"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    sort: str = Query("generated_at"),
    order: str = Query("desc"),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(RiskAlert)

    if type:
        stmt = stmt.where(RiskAlert.type == type)
    if severity:
        stmt = stmt.where(RiskAlert.severity == severity)
    if status:
        stmt = stmt.where(RiskAlert.status == status)
    if contract_id:
        stmt = stmt.where(RiskAlert.contract_id == contract_id)
    if supplier_id:
        stmt = stmt.where(RiskAlert.supplier_id == supplier_id)

    time_col = RiskAlert.updated_at if time_field == "updated_at" else RiskAlert.generated_at
    if date_from:
        stmt = stmt.where(time_col >= date_from)
    if date_to:
        stmt = stmt.where(time_col < date_to)

    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = (await db.execute(count_stmt)).scalar()

    sort_field = sort if sort in ALLOWED_SORT_ALERT else "generated_at"
    sort_col = getattr(RiskAlert, sort_field)
    stmt = stmt.order_by(sort_col.asc() if order == "asc" else sort_col.desc())

    offset = (page - 1) * page_size
    stmt = stmt.offset(offset).limit(page_size)

    result = await db.execute(stmt)
    alerts = result.scalars().all()

    return PaginatedResponse(
        meta=PaginationMeta(
            page=page, page_size=page_size,
            total_results=total,
            total_pages=math.ceil(total / page_size),
            sort=sort, order=order,
        ),
        data=[RiskAlertResponse.model_validate(a) for a in alerts]
    )


@router.get("/alerts/{alert_id}", response_model=RiskAlertResponse)
async def get_alert(alert_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(RiskAlert).where(RiskAlert.id == alert_id))
    alert = result.scalar_one_or_none()
    if not alert:
        raise HTTPException(status_code=404, detail="Alerta no encontrada")
    return RiskAlertResponse.model_validate(alert)


@router.patch("/alerts/{alert_id}", response_model=RiskAlertResponse,
              summary="Revisar o desestimar alerta (human-in-the-loop)")
async def update_alert(
    alert_id: uuid.UUID,
    update_data: RiskAlertUpdate,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(require_api_key),
):
    result = await db.execute(select(RiskAlert).where(RiskAlert.id == alert_id))
    alert = result.scalar_one_or_none()
    if not alert:
        raise HTTPException(status_code=404, detail="Alerta no encontrada")

    if update_data.status:
        alert.status = update_data.status
        if update_data.status in ("reviewed", "dismissed"):
            alert.reviewed_at = datetime.now(timezone.utc)
    if update_data.reviewed_by:
        alert.reviewed_by = update_data.reviewed_by
    if update_data.review_notes:
        alert.review_notes = update_data.review_notes

    await db.commit()
    await db.refresh(alert)
    return RiskAlertResponse.model_validate(alert)


@router.post("/run", summary="Ejecutar motor de detección de riesgos")
async def run_risk_engine(
    db: AsyncSession = Depends(get_db),
    _: None = Depends(require_api_key),
):
    from app.services.risk_engine import RiskEngine
    engine = RiskEngine(db)
    results = await engine.run_all_checks()
    all_alerts = [a for checks in results.values() for a in checks]
    saved = await engine.save_alerts(all_alerts)
    return {"status": "ok", "alerts_saved": saved, "checks": {k: len(v) for k, v in results.items()}}
