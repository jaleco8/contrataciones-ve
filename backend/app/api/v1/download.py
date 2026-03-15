from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import csv
import io
import json
from datetime import datetime, timezone
from typing import AsyncGenerator

from app.core.database import get_db
from app.models.contract import Contract
from app.models.process import Process

router = APIRouter()

CHUNK_SIZE = 500


async def _generate_contracts_csv(db: AsyncSession) -> AsyncGenerator[str, None]:
    yield "id,contract_number,title,buyer_name,supplier_name,amount,currency,status,category,signed_at,start_date,end_date,has_amendments,amendments_count\n"
    offset = 0
    while True:
        result = await db.execute(
            select(Contract).order_by(Contract.signed_at.desc())
            .offset(offset).limit(CHUNK_SIZE)
        )
        batch = result.scalars().all()
        if not batch:
            break
        buf = io.StringIO()
        writer = csv.writer(buf)
        for c in batch:
            writer.writerow([
                str(c.id), c.contract_number, c.title, c.buyer_name, c.supplier_name,
                float(c.amount), c.currency, c.status, c.category,
                c.signed_at, c.start_date, c.end_date, c.has_amendments, c.amendments_count
            ])
        yield buf.getvalue()
        offset += CHUNK_SIZE


@router.get("/contracts.csv", summary="Descarga masiva de contratos en CSV")
async def download_contracts_csv(db: AsyncSession = Depends(get_db)):
    return StreamingResponse(
        _generate_contracts_csv(db),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=contratos-ve.csv"}
    )


@router.get("/ocds/releases.json", summary="Exportación OCDS JSON")
async def download_ocds_json(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Process).order_by(Process.published_at.desc()))
    processes = result.scalars().all()

    releases = []
    for p in processes:
        release = {
            "ocid": p.ocid or f"ocds-ve-{str(p.id)[:8]}",
            "id": f"{p.ocid or str(p.id)}-{int(p.published_at.timestamp()) if p.published_at else 0}",
            "date": p.published_at.isoformat() if p.published_at else None,
            "tag": [p.status],
            "initiationType": "tender",
            "buyer": {
                "id": p.buyer_id or "",
                "name": p.buyer_name
            },
            "tender": {
                "id": str(p.id),
                "title": p.title,
                "description": p.description,
                "status": p.status,
                "value": {
                    "amount": float(p.tender_amount) if p.tender_amount else None,
                    "currency": p.tender_currency
                },
                "procurementMethod": p.procurement_method,
                "numberOfTenderers": p.bidders_count
            }
        }
        if p.awarded_amount:
            release["awards"] = [{
                "id": f"award-{str(p.id)[:8]}",
                "status": "active",
                "value": {
                    "amount": float(p.awarded_amount),
                    "currency": p.awarded_currency
                },
                "suppliers": [{"name": p.awarded_supplier_name}]
            }]
        releases.append(release)

    ocds_package = {
        "uri": "https://contrataciones.ve/api/v1/download/ocds/releases.json",
        "version": "1.1",
        "publishedDate": datetime.now(timezone.utc).isoformat(),
        "publisher": {
            "name": "Plataforma Abierta Anticorrupción Venezuela",
            "scheme": "VE-RIF"
        },
        "releases": releases
    }

    return StreamingResponse(
        iter([json.dumps(ocds_package, ensure_ascii=False, indent=2)]),
        media_type="application/json",
        headers={"Content-Disposition": "attachment; filename=ocds-releases.json"}
    )
