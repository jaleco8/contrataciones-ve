"""
Motor de riesgo — Plataforma Anticorrupción Venezuela
Implementa banderas rojas basadas en OCDS Red Flags for Integrity
Todas las alertas generadas son señales para revisión humana, NO conclusiones.
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.contract import Contract
from app.models.process import Process
from app.models.supplier import Supplier
from app.models.risk_alert import RiskAlert
from datetime import datetime, timezone


class RiskEngine:
    """
    Genera alertas de riesgo explicables siguiendo metodología OCDS.
    Enfoque: banderas rojas + revisión humana obligatoria.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def run_all_checks(self) -> dict:
        """Ejecuta todos los módulos de detección de riesgo."""
        results = {
            "amendments_check": await self.check_systematic_amendments(),
            "sanctioned_check": await self.check_sanctioned_suppliers(),
            "competition_check": await self.check_low_competition(),
            "emergency_check": await self.check_emergency_overprice(),
        }
        return results

    async def check_systematic_amendments(self) -> list[dict]:
        """
        Bandera roja: contratos con múltiples adendas de incremento.
        Patrón: > 1 adenda O incremento > 15% del monto original.
        """
        result = await self.db.execute(
            select(Contract).where(
                Contract.amendments_count >= 2,
                Contract.status.in_(["active", "completed"])
            )
        )
        contracts = result.scalars().all()

        alerts = []
        for contract in contracts:
            if contract.original_amount and contract.original_amount > 0:
                increase_pct = float(contract.amendment_amount_increase or 0) / float(contract.original_amount) * 100
            else:
                increase_pct = 0.0

            if contract.amendments_count >= 2 or increase_pct > 15:
                score = min(0.95, 0.50 + (contract.amendments_count * 0.15) + (increase_pct * 0.005))
                severity = "critical" if score > 0.85 else "high" if score > 0.65 else "medium"

                explanation = [
                    f"Contrato con {contract.amendments_count} adenda(s) de modificación",
                    f"Monto incrementado en {increase_pct:.1f}% sobre el valor original",
                ]
                if increase_pct > 30:
                    explanation.append("Incremento superior al 30% — requiere justificación técnica")
                if contract.amendments_count >= 3:
                    explanation.append("Patrón de adendas múltiples — revisión prioritaria recomendada")

                alerts.append({
                    "type": "systematic_amendments",
                    "severity": severity,
                    "score": round(score, 3),
                    "contract_id": contract.id,
                    "supplier_id": contract.supplier_id,
                    "explanation": explanation,
                    "supporting_data": {
                        "original_amount": float(contract.original_amount or 0),
                        "current_amount": float(contract.amount),
                        "increase_pct": round(increase_pct, 1),
                        "amendments_count": contract.amendments_count,
                    }
                })
        return alerts

    async def check_sanctioned_suppliers(self) -> list[dict]:
        """
        Bandera roja CRÍTICA: proveedor sancionado con contrato activo.
        """
        result = await self.db.execute(
            select(Contract, Supplier)
            .join(Supplier, Contract.supplier_id == Supplier.id)
            .where(
                Supplier.sanction_status.in_(["sanctioned", "suspended"]),
                Contract.status == "active"
            )
        )
        rows = result.all()

        alerts = []
        for contract, supplier in rows:
            alerts.append({
                "type": "repeat_entity",
                "severity": "critical",
                "score": 0.950,
                "contract_id": contract.id,
                "supplier_id": supplier.id,
                "explanation": [
                    f"Proveedor con estatus '{supplier.sanction_status.upper()}' tiene contrato activo",
                    "Adjudicación a proveedor inhabilitado — posible violación del marco legal",
                    "Requiere revisión inmediata por órgano de control"
                ],
                "supporting_data": {
                    "supplier_rif": supplier.rif,
                    "supplier_name": supplier.name,
                    "sanction_status": supplier.sanction_status,
                    "contract_amount": float(contract.amount),
                }
            })
        return alerts

    async def check_low_competition(self) -> list[dict]:
        """
        Bandera roja: procesos con un solo oferente o contratación directa de alto valor.
        """
        result = await self.db.execute(
            select(Process).where(
                Process.status == "awarded",
                Process.bidders_count <= 1,
            )
        )
        processes = result.scalars().all()

        alerts = []
        for process in processes:
            amount = float(process.awarded_amount or process.tender_amount or 0)
            is_direct = process.procurement_method == "direct"

            score = 0.60
            if is_direct and amount > 100000:
                score = 0.75
            if process.bidders_count == 0:
                score += 0.10
            if amount > 500000:
                score += 0.10

            score = min(score, 0.90)
            severity = "high" if score > 0.70 else "medium"

            explanation = []
            if process.bidders_count <= 1:
                explanation.append(f"Solo {process.bidders_count} oferente(s) en proceso de contratación")
            if is_direct:
                explanation.append(f"Modalidad de contratación directa por USD {amount:,.0f}")
            if amount > 500000:
                explanation.append("Monto elevado para modalidad sin competencia abierta")

            if explanation:
                alerts.append({
                    "type": "low_competition",
                    "severity": severity,
                    "score": round(score, 3),
                    "process_id": process.id,
                    "supplier_id": process.awarded_supplier_id,
                    "explanation": explanation,
                    "supporting_data": {
                        "bidders_count": process.bidders_count,
                        "procurement_method": process.procurement_method,
                        "amount": amount,
                    }
                })
        return alerts

    async def check_emergency_overprice(self) -> list[dict]:
        """
        Bandera roja: contratos de emergencia con monto final muy superior al licitado.
        """
        result = await self.db.execute(
            select(Contract, Process)
            .join(Process, Contract.process_id == Process.id, isouter=True)
            .where(Process.procurement_method == "emergency")
        )
        rows = result.all()

        alerts = []
        for contract, process in rows:
            if not process or not process.tender_amount:
                continue

            tender_amount = float(process.tender_amount)
            final_amount = float(contract.amount)
            overprice_pct = (final_amount - tender_amount) / tender_amount * 100

            if overprice_pct > 20:
                score = min(0.95, 0.60 + overprice_pct * 0.003)
                severity = "critical" if overprice_pct > 50 else "high"

                alerts.append({
                    "type": "overprice",
                    "severity": severity,
                    "score": round(score, 3),
                    "contract_id": contract.id,
                    "process_id": process.id,
                    "supplier_id": contract.supplier_id,
                    "explanation": [
                        f"Monto final {overprice_pct:.0f}% superior al monto licitado en emergencia",
                        f"Licitado: USD {tender_amount:,.0f} → Final: USD {final_amount:,.0f}",
                        "Contrataciones de emergencia con ampliaciones sistemáticas — patrón de riesgo",
                    ],
                    "supporting_data": {
                        "tender_amount": tender_amount,
                        "final_amount": final_amount,
                        "overprice_pct": round(overprice_pct, 1),
                    }
                })
        return alerts

    async def save_alerts(self, alerts: list[dict]) -> int:
        """Persiste las alertas generadas en la base de datos, evitando duplicados."""
        count = 0
        for alert_data in alerts:
            # Verificar si ya existe una alerta abierta del mismo tipo para el mismo contrato/proceso
            existing_stmt = select(RiskAlert).where(
                RiskAlert.type == alert_data["type"],
                RiskAlert.status == "open",
            )
            if alert_data.get("contract_id") is not None:
                existing_stmt = existing_stmt.where(RiskAlert.contract_id == alert_data["contract_id"])
            else:
                existing_stmt = existing_stmt.where(RiskAlert.contract_id.is_(None))
            if alert_data.get("process_id") is not None:
                existing_stmt = existing_stmt.where(RiskAlert.process_id == alert_data["process_id"])
            else:
                existing_stmt = existing_stmt.where(RiskAlert.process_id.is_(None))

            existing = await self.db.execute(existing_stmt)
            if existing.scalar_one_or_none() is not None:
                continue  # Ya existe, no duplicar

            alert = RiskAlert(
                type=alert_data["type"],
                severity=alert_data["severity"],
                score=alert_data["score"],
                contract_id=alert_data.get("contract_id"),
                process_id=alert_data.get("process_id"),
                supplier_id=alert_data.get("supplier_id"),
                explanation=alert_data["explanation"],
                supporting_data=alert_data.get("supporting_data", {}),
                generated_at=datetime.now(timezone.utc),
                status="open"
            )
            self.db.add(alert)
            count += 1
        await self.db.commit()
        return count
