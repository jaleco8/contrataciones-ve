"""
Script de seed — datos de demostración ficticios.

Uso:
    cd backend
    python -m app.seed.seed_data

Requiere DATABASE_URL en el archivo .env (o variable de entorno).
Borra y recrea todos los datos de demo cada vez que se ejecuta.
"""

import asyncio
import os
from pathlib import Path
from datetime import date, datetime, timezone

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker  # noqa: E402
from sqlalchemy import text  # noqa: E402

# Importar modelos para que SQLAlchemy los conozca
from app.models.supplier import Supplier  # noqa: E402
from app.models.process import Process  # noqa: E402
from app.models.risk_alert import RiskAlert  # noqa: E402

load_dotenv(Path(__file__).parent.parent.parent / ".env")

# ---------------------------------------------------------------------------
# Conexión
# ---------------------------------------------------------------------------

_raw_url = os.environ["DATABASE_URL"]
DATABASE_URL = (
    _raw_url.replace("postgresql://", "postgresql+asyncpg://")
            .replace("postgres://", "postgresql+asyncpg://")
)

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# ---------------------------------------------------------------------------
# Datos
# ---------------------------------------------------------------------------

SUPPLIERS = [
    dict(id="11111111-1111-1111-1111-111111111111", rif="J-12345678-9",
         name="Constructora Venezuela 2000 C.A.", sector="Construcción e Infraestructura",
         sanction_status="active", awards_count_12m=8, total_awarded_12m=4200000.00, state="Caracas"),
    dict(id="22222222-2222-2222-2222-222222222222", rif="J-98765432-1",
         name="TecnoSol Soluciones Tecnológicas C.A.", sector="Tecnología e Informática",
         sanction_status="active", awards_count_12m=12, total_awarded_12m=2800000.00, state="Caracas"),
    dict(id="33333333-3333-3333-3333-333333333333", rif="J-45678901-2",
         name="Suministros Industriales del Orinoco C.A.", sector="Suministros y Equipos",
         sanction_status="active", awards_count_12m=6, total_awarded_12m=1900000.00, state="Bolívar"),
    dict(id="44444444-4444-4444-4444-444444444444", rif="J-11223344-5",
         name="Grupo Médico Hospitalario Nacional C.A.", sector="Salud y Equipos Médicos",
         sanction_status="active", awards_count_12m=4, total_awarded_12m=3100000.00, state="Miranda"),
    dict(id="55555555-5555-5555-5555-555555555555", rif="J-55667788-3",
         name="Transporte y Logística Los Andes C.A.", sector="Transporte y Logística",
         sanction_status="sanctioned", awards_count_12m=2, total_awarded_12m=450000.00, state="Mérida"),
    dict(id="66666666-6666-6666-6666-666666666666", rif="J-99887766-4",
         name="Consultores Asociados Metropolis C.A.",
         sector="Consultoría y Servicios Profesionales",
         sanction_status="active", awards_count_12m=15, total_awarded_12m=1750000.00, state="Caracas"),
    dict(id="77777777-7777-7777-7777-777777777777", rif="J-33445566-7",
         name="Electricidad y Telecomunicaciones del Sur C.A.",
         sector="Electricidad y Telecomunicaciones",
         sanction_status="active", awards_count_12m=5, total_awarded_12m=2200000.00, state="Zulia"),
    dict(id="88888888-8888-8888-8888-888888888888", rif="J-77889900-6",
         name="Alimentos y Distribución Nacional C.A.", sector="Alimentos y Distribución",
         sanction_status="active", awards_count_12m=9, total_awarded_12m=890000.00, state="Aragua"),
]

PROCESSES = [
    dict(id="aaaa1111-1111-1111-1111-aaaaaaaaaaaa", ocid="ocds-ve-2026-001",
         title="Construcción y Rehabilitación de 500 km de Vías Nacionales — Fase I",
         description="Rehabilitación de infraestructura vial en los estados Carabobo, Aragua y Miranda",
         status="awarded", procurement_method="open_tender",
         buyer_name="Ministerio de Infraestructura y Obras Públicas", buyer_entity_type="ministerio",
         tender_amount=12500000.00, tender_currency="USD",
         awarded_amount=11800000.00, awarded_currency="USD",
         awarded_supplier_id="11111111-1111-1111-1111-111111111111",
         awarded_supplier_name="Constructora Venezuela 2000 C.A.",
         published_at=datetime(2025, 10, 1, 9, 0, tzinfo=timezone.utc),
         tender_start_date=date(2025, 10, 1), tender_end_date=date(2025, 11, 15),
         award_date=date(2025, 12, 1), category="obras", bidders_count=3),
    dict(id="aaaa2222-2222-2222-2222-aaaaaaaaaaaa", ocid="ocds-ve-2026-002",
         title="Sistema Integral de Gestión Hospitalaria — Hospitales Públicos Nacionales",
         description="Plataforma tecnológica para gestión de pacientes, inventario y facturación en 45 hospitales",
         status="awarded", procurement_method="open_tender",
         buyer_name="Ministerio de Salud", buyer_entity_type="ministerio",
         tender_amount=4200000.00, tender_currency="USD",
         awarded_amount=4150000.00, awarded_currency="USD",
         awarded_supplier_id="22222222-2222-2222-2222-222222222222",
         awarded_supplier_name="TecnoSol Soluciones Tecnológicas C.A.",
         published_at=datetime(2025, 11, 15, 9, 0, tzinfo=timezone.utc),
         tender_start_date=date(2025, 11, 15), tender_end_date=date(2025, 12, 30),
         award_date=date(2026, 1, 15), category="servicios", bidders_count=2),
    dict(id="aaaa3333-3333-3333-3333-aaaaaaaaaaaa", ocid="ocds-ve-2026-003",
         title="Adquisición de Equipos Médicos para Unidades de Cuidados Intensivos",
         description="Ventiladores, monitores y equipos de diagnóstico para 12 UCIs del país",
         status="awarded", procurement_method="limited",
         buyer_name="Ministerio de Salud", buyer_entity_type="ministerio",
         tender_amount=8900000.00, tender_currency="USD",
         awarded_amount=8750000.00, awarded_currency="USD",
         awarded_supplier_id="44444444-4444-4444-4444-444444444444",
         awarded_supplier_name="Grupo Médico Hospitalario Nacional C.A.",
         published_at=datetime(2025, 9, 20, 9, 0, tzinfo=timezone.utc),
         tender_start_date=date(2025, 9, 20), tender_end_date=date(2025, 10, 20),
         award_date=date(2025, 11, 1), category="bienes", bidders_count=4),
    dict(id="aaaa4444-4444-4444-4444-aaaaaaaaaaaa", ocid="ocds-ve-2026-004",
         title="Servicio de Transporte Escolar Zona Metropolitana de Caracas",
         description="Servicio de transporte para 25,000 estudiantes de escuelas públicas",
         status="awarded", procurement_method="open_tender",
         buyer_name="Ministerio de Educación", buyer_entity_type="ministerio",
         tender_amount=2100000.00, tender_currency="USD",
         awarded_amount=1950000.00, awarded_currency="USD",
         awarded_supplier_id="55555555-5555-5555-5555-555555555555",
         awarded_supplier_name="Transporte y Logística Los Andes C.A.",
         published_at=datetime(2025, 8, 10, 9, 0, tzinfo=timezone.utc),
         tender_start_date=date(2025, 8, 10), tender_end_date=date(2025, 9, 10),
         award_date=date(2025, 9, 25), category="servicios", bidders_count=1),
    dict(id="aaaa5555-5555-5555-5555-aaaaaaaaaaaa", ocid="ocds-ve-2026-005",
         title="Modernización del Sistema Eléctrico — Maracaibo Norte",
         description="Sustitución de transformadores y tendido eléctrico en sectores norte de Maracaibo",
         status="tender", procurement_method="open_tender",
         buyer_name="Corporación Eléctrica Nacional", buyer_entity_type="ente",
         tender_amount=15000000.00, tender_currency="USD",
         awarded_amount=None, awarded_currency="USD",
         awarded_supplier_id=None, awarded_supplier_name=None,
         published_at=datetime(2026, 2, 1, 9, 0, tzinfo=timezone.utc),
         tender_start_date=date(2026, 2, 1), tender_end_date=date(2026, 3, 15),
         award_date=None, category="obras", bidders_count=0),
    dict(id="aaaa6666-6666-6666-6666-aaaaaaaaaaaa", ocid="ocds-ve-2026-006",
         title="Consultoría para Diseño del Sistema Nacional de Datos Abiertos",
         description="Diseño de arquitectura y política para portal nacional de datos abiertos gubernamentales",
         status="awarded", procurement_method="direct",
         buyer_name="Ministerio de Ciencia y Tecnología", buyer_entity_type="ministerio",
         tender_amount=380000.00, tender_currency="USD",
         awarded_amount=375000.00, awarded_currency="USD",
         awarded_supplier_id="66666666-6666-6666-6666-666666666666",
         awarded_supplier_name="Consultores Asociados Metropolis C.A.",
         published_at=datetime(2025, 12, 1, 9, 0, tzinfo=timezone.utc),
         tender_start_date=None, tender_end_date=None,
         award_date=date(2025, 12, 5), category="consultoria", bidders_count=1),
    dict(id="aaaa7777-7777-7777-7777-aaaaaaaaaaaa", ocid="ocds-ve-2026-007",
         title="Suministro de Materiales de Construcción — Obras de Emergencia Vargas",
         description="Materiales para reparación de viviendas afectadas por lluvias en La Guaira",
         status="awarded", procurement_method="emergency",
         buyer_name="Gobernación de La Guaira", buyer_entity_type="gobernacion",
         tender_amount=920000.00, tender_currency="USD",
         awarded_amount=1380000.00, awarded_currency="USD",
         awarded_supplier_id="33333333-3333-3333-3333-333333333333",
         awarded_supplier_name="Suministros Industriales del Orinoco C.A.",
         published_at=datetime(2025, 7, 15, 9, 0, tzinfo=timezone.utc),
         tender_start_date=None, tender_end_date=None,
         award_date=date(2025, 7, 16), category="bienes", bidders_count=1),
    dict(id="aaaa8888-8888-8888-8888-aaaaaaaaaaaa", ocid="ocds-ve-2026-008",
         title="Implementación de Red de Fibra Óptica — Zona Industrial Guacara",
         description="Tendido de 120 km de fibra óptica para zona industrial de Carabobo",
         status="awarded", procurement_method="open_tender",
         buyer_name="Ministerio de Ciencia y Tecnología", buyer_entity_type="ministerio",
         tender_amount=3400000.00, tender_currency="USD",
         awarded_amount=3350000.00, awarded_currency="USD",
         awarded_supplier_id="77777777-7777-7777-7777-777777777777",
         awarded_supplier_name="Electricidad y Telecomunicaciones del Sur C.A.",
         published_at=datetime(2025, 10, 15, 9, 0, tzinfo=timezone.utc),
         tender_start_date=date(2025, 10, 15), tender_end_date=date(2025, 11, 30),
         award_date=date(2025, 12, 15), category="obras", bidders_count=3),
]

CONTRACTS = [
    dict(id="cccc1111-1111-1111-1111-cccccccccccc",
         contract_number="CTR-MIOP-2026-001",
         process_id="aaaa1111-1111-1111-1111-aaaaaaaaaaaa",
         supplier_id="11111111-1111-1111-1111-111111111111",
         supplier_name="Constructora Venezuela 2000 C.A.",
         buyer_name="Ministerio de Infraestructura y Obras Públicas",
         title="Construcción y Rehabilitación Vial — Fase I",
         description="Rehabilitación de vías nacionales Carabobo, Aragua y Miranda",
         category="obras", status="active",
         amount=14200000.00, currency="USD", original_amount=11800000.00,
         signed_at=date(2025, 12, 15), start_date=date(2026, 1, 1), end_date=date(2027, 6, 30),
         has_amendments=True, amendments_count=2, amendment_amount_increase=2400000.00),
    dict(id="cccc2222-2222-2222-2222-cccccccccccc",
         contract_number="CTR-MSALUD-2026-001",
         process_id="aaaa2222-2222-2222-2222-aaaaaaaaaaaa",
         supplier_id="22222222-2222-2222-2222-222222222222",
         supplier_name="TecnoSol Soluciones Tecnológicas C.A.",
         buyer_name="Ministerio de Salud",
         title="Sistema Integral de Gestión Hospitalaria",
         description="Plataforma tecnológica 45 hospitales públicos",
         category="servicios", status="active",
         amount=4150000.00, currency="USD", original_amount=4150000.00,
         signed_at=date(2026, 1, 20), start_date=date(2026, 2, 1), end_date=date(2026, 12, 31),
         has_amendments=False, amendments_count=0, amendment_amount_increase=0.00),
    dict(id="cccc3333-3333-3333-3333-cccccccccccc",
         contract_number="CTR-MSALUD-2026-002",
         process_id="aaaa3333-3333-3333-3333-aaaaaaaaaaaa",
         supplier_id="44444444-4444-4444-4444-444444444444",
         supplier_name="Grupo Médico Hospitalario Nacional C.A.",
         buyer_name="Ministerio de Salud",
         title="Equipos Médicos para UCIs",
         description="Ventiladores, monitores y equipos de diagnóstico para 12 UCIs",
         category="bienes", status="active",
         amount=8750000.00, currency="USD", original_amount=8750000.00,
         signed_at=date(2025, 11, 10), start_date=date(2025, 11, 15), end_date=date(2026, 3, 31),
         has_amendments=False, amendments_count=0, amendment_amount_increase=0.00),
    dict(id="cccc4444-4444-4444-4444-cccccccccccc",
         contract_number="CTR-MEDU-2026-001",
         process_id="aaaa4444-4444-4444-4444-aaaaaaaaaaaa",
         supplier_id="55555555-5555-5555-5555-555555555555",
         supplier_name="Transporte y Logística Los Andes C.A.",
         buyer_name="Ministerio de Educación",
         title="Transporte Escolar Zona Metropolitana",
         description="Servicio de transporte 25,000 estudiantes",
         category="servicios", status="active",
         amount=1950000.00, currency="USD", original_amount=1950000.00,
         signed_at=date(2025, 10, 1), start_date=date(2025, 10, 15), end_date=date(2026, 6, 30),
         has_amendments=False, amendments_count=0, amendment_amount_increase=0.00),
    dict(id="cccc5555-5555-5555-5555-cccccccccccc",
         contract_number="CTR-MCT-2026-001",
         process_id="aaaa6666-6666-6666-6666-aaaaaaaaaaaa",
         supplier_id="66666666-6666-6666-6666-666666666666",
         supplier_name="Consultores Asociados Metropolis C.A.",
         buyer_name="Ministerio de Ciencia y Tecnología",
         title="Consultoría Datos Abiertos — Contratación Directa",
         description="Diseño de arquitectura y política de datos abiertos",
         category="consultoria", status="active",
         amount=375000.00, currency="USD", original_amount=375000.00,
         signed_at=date(2025, 12, 10), start_date=date(2025, 12, 15), end_date=date(2026, 6, 15),
         has_amendments=False, amendments_count=0, amendment_amount_increase=0.00),
    dict(id="cccc6666-6666-6666-6666-cccccccccccc",
         contract_number="CTR-GLAGUAIRA-2026-001",
         process_id="aaaa7777-7777-7777-7777-aaaaaaaaaaaa",
         supplier_id="33333333-3333-3333-3333-333333333333",
         supplier_name="Suministros Industriales del Orinoco C.A.",
         buyer_name="Gobernación de La Guaira",
         title="Materiales Construcción — Emergencia Vargas",
         description="Materiales para reparación viviendas afectadas por lluvias",
         category="bienes", status="active",
         amount=1380000.00, currency="USD", original_amount=920000.00,
         signed_at=date(2025, 7, 17), start_date=date(2025, 7, 17), end_date=date(2025, 12, 31),
         has_amendments=True, amendments_count=1, amendment_amount_increase=460000.00),
    dict(id="cccc7777-7777-7777-7777-cccccccccccc",
         contract_number="CTR-MCT-2026-002",
         process_id="aaaa8888-8888-8888-8888-aaaaaaaaaaaa",
         supplier_id="77777777-7777-7777-7777-777777777777",
         supplier_name="Electricidad y Telecomunicaciones del Sur C.A.",
         buyer_name="Ministerio de Ciencia y Tecnología",
         title="Red Fibra Óptica — Zona Industrial Guacara",
         description="Tendido 120 km fibra óptica Carabobo",
         category="obras", status="active",
         amount=3350000.00, currency="USD", original_amount=3350000.00,
         signed_at=date(2025, 12, 20), start_date=date(2026, 1, 1), end_date=date(2026, 9, 30),
         has_amendments=False, amendments_count=0, amendment_amount_increase=0.00),
    dict(id="cccc8888-8888-8888-8888-cccccccccccc",
         contract_number="CTR-MCT-2026-003",
         process_id=None,
         supplier_id="66666666-6666-6666-6666-666666666666",
         supplier_name="Consultores Asociados Metropolis C.A.",
         buyer_name="Ministerio de Planificación",
         title="Consultoría Reforma Tributaria Digital",
         description="Análisis y propuesta de digitalización del sistema tributario",
         category="consultoria", status="completed",
         amount=290000.00, currency="USD", original_amount=290000.00,
         signed_at=date(2025, 6, 1), start_date=date(2025, 6, 1), end_date=date(2025, 11, 30),
         has_amendments=False, amendments_count=0, amendment_amount_increase=0.00),
]

AMENDMENTS = [
    dict(contract_id="cccc1111-1111-1111-1111-cccccccccccc", amendment_number=1,
         description="Ampliación de alcance: inclusión de 80 km adicionales en estado Miranda por derrumbes",
         original_amount=11800000.00, new_amount=13200000.00, amount_change=1400000.00,
         original_end_date=date(2027, 6, 30), new_end_date=date(2027, 12, 31),
         signed_at=date(2026, 2, 15)),
    dict(contract_id="cccc1111-1111-1111-1111-cccccccccccc", amendment_number=2,
         description="Ajuste por variación de precios de materiales — índice inflacionario 2026-Q1",
         original_amount=13200000.00, new_amount=14200000.00, amount_change=1000000.00,
         original_end_date=date(2027, 12, 31), new_end_date=date(2028, 3, 31),
         signed_at=date(2026, 3, 1)),
    dict(contract_id="cccc6666-6666-6666-6666-cccccccccccc", amendment_number=1,
         description="Incremento de scope: inclusión de municipios Vargas y Naiguatá no contemplados en diseño original",
         original_amount=920000.00, new_amount=1380000.00, amount_change=460000.00,
         original_end_date=date(2025, 12, 31), new_end_date=date(2025, 12, 31),
         signed_at=date(2025, 9, 1)),
]

PAYMENTS = [
    dict(contract_id="cccc1111-1111-1111-1111-cccccccccccc", payment_number=1,
         amount=3550000.00, currency="USD", status="paid",
         payment_date=date(2026, 1, 15), description="Anticipo 25% — inicio de obras"),
    dict(contract_id="cccc1111-1111-1111-1111-cccccccccccc", payment_number=2,
         amount=4260000.00, currency="USD", status="paid",
         payment_date=date(2026, 2, 28), description="Segundo pago 30% — avance de obra certificado"),
    dict(contract_id="cccc2222-2222-2222-2222-cccccccccccc", payment_number=1,
         amount=1245000.00, currency="USD", status="paid",
         payment_date=date(2026, 2, 1), description="Anticipo 30% — inicio del proyecto"),
    dict(contract_id="cccc3333-3333-3333-3333-cccccccccccc", payment_number=1,
         amount=4375000.00, currency="USD", status="paid",
         payment_date=date(2025, 11, 20), description="Pago total contra entrega de equipos"),
    dict(contract_id="cccc6666-6666-6666-6666-cccccccccccc", payment_number=1,
         amount=690000.00, currency="USD", status="paid",
         payment_date=date(2025, 7, 20), description="Anticipo de emergencia 50%"),
    dict(contract_id="cccc6666-6666-6666-6666-cccccccccccc", payment_number=2,
         amount=690000.00, currency="USD", status="paid",
         payment_date=date(2025, 10, 15), description="Segundo pago 50% — entrega parcial"),
]

RISK_ALERTS = [
    dict(id="aaaa0001-0000-0000-0000-000000000000",
         type="systematic_amendments", severity="high", status="open", score=0.875,
         contract_id="cccc1111-1111-1111-1111-cccccccccccc",
         process_id="aaaa1111-1111-1111-1111-aaaaaaaaaaaa",
         supplier_id="11111111-1111-1111-1111-111111111111",
         explanation=[
             "Monto del contrato incrementado 20.3% en 75 días tras la firma",
             "2 adendas de incremento en menos de 90 días",
             "Ampliación de plazo de 9 meses adicionales sobre el contrato original",
             "Patrón: adendas múltiples de aumento en contratos de obras viales del mismo comprador",
         ],
         supporting_data={"original_amount": 11800000, "current_amount": 14200000,
                          "increase_pct": 20.3, "amendments_count": 2, "days_since_signing": 75},
         generated_at=datetime(2026, 3, 10, 10, 5, tzinfo=timezone.utc)),
    dict(id="aaaa0002-0000-0000-0000-000000000000",
         type="repeat_entity", severity="critical", status="open", score=0.950,
         contract_id="cccc4444-4444-4444-4444-cccccccccccc",
         process_id="aaaa4444-4444-4444-4444-aaaaaaaaaaaa",
         supplier_id="55555555-5555-5555-5555-555555555555",
         explanation=[
             "Proveedor con estatus SANCIONADO adjudicado en proceso activo",
             "Solo 1 oferente presentó propuesta (baja competencia)",
             "Proceso adjudicado al único oferente sin evaluación comparativa documentada",
             "Proveedor tiene registro de sanciones previas verificado en registro oficial",
         ],
         supporting_data={"sanction_status": "sanctioned", "bidders_count": 1,
                          "procurement_method": "open_tender"},
         generated_at=datetime(2026, 3, 8, 14, 30, tzinfo=timezone.utc)),
    dict(id="aaaa0003-0000-0000-0000-000000000000",
         type="low_competition", severity="medium", status="open", score=0.720,
         contract_id="cccc5555-5555-5555-5555-cccccccccccc",
         process_id="aaaa6666-6666-6666-6666-aaaaaaaaaaaa",
         supplier_id="66666666-6666-6666-6666-666666666666",
         explanation=[
             "Modalidad de contratación directa para monto de USD 375,000",
             "No se registra proceso competitivo previo",
             "El mismo proveedor tiene 15 contratos en los últimos 12 meses con distintos entes",
             "Concentración: 1 proveedor, múltiples ministerios, patrón de contrataciones directas",
         ],
         supporting_data={"procurement_method": "direct", "amount": 375000,
                          "supplier_contracts_12m": 15, "unique_buyers": 4},
         generated_at=datetime(2026, 3, 5, 9, 15, tzinfo=timezone.utc)),
    dict(id="aaaa0004-0000-0000-0000-000000000000",
         type="overprice", severity="high", status="reviewed", score=0.810,
         contract_id="cccc6666-6666-6666-6666-cccccccccccc",
         process_id="aaaa7777-7777-7777-7777-aaaaaaaaaaaa",
         supplier_id="33333333-3333-3333-3333-333333333333",
         explanation=[
             "Monto final 50% superior al monto licitado (USD 920K → USD 1.38M)",
             "Modalidad de emergencia usada para ampliar scope original significativamente",
             "Adenda aplicada 45 días después de inicio por scope no contemplado en diseño de emergencia",
             "Patrón: contrataciones de emergencia con ampliaciones sistemáticas",
         ],
         supporting_data={"original_tender": 920000, "final_amount": 1380000,
                          "overprice_pct": 50.0, "days_to_amendment": 45},
         generated_at=datetime(2026, 2, 20, 11, 0, tzinfo=timezone.utc)),
    dict(id="aaaa0005-0000-0000-0000-000000000000",
         type="winner_rotation", severity="low", status="dismissed", score=0.450,
         contract_id=None, process_id=None,
         supplier_id="22222222-2222-2222-2222-222222222222",
         explanation=[
             "Proveedor TecnoSol adjudicado en 12 contratos en 12 meses",
             "Alta concentración en sector tecnología gubernamental",
             "Nota: los contratos muestran procesos competitivos con múltiples oferentes — alerta revisada y desestimada",
         ],
         supporting_data={"contracts_12m": 12, "total_awarded_12m": 2800000, "unique_buyers": 3},
         generated_at=datetime(2026, 1, 15, 8, 0, tzinfo=timezone.utc)),
]


# ---------------------------------------------------------------------------
# Inserción
# ---------------------------------------------------------------------------

async def seed(db: AsyncSession) -> None:
    print("Limpiando datos existentes...")
    # Orden inverso a las FK
    for table in ("risk_alerts", "contract_payments", "contract_amendments",
                  "contracts", "processes", "suppliers"):
        await db.execute(text(f"DELETE FROM {table}"))

    print("Insertando suppliers...")
    for row in SUPPLIERS:
        db.add(Supplier(**row))
    await db.flush()

    print("Insertando processes...")
    for row in PROCESSES:
        db.add(Process(**row))
    await db.flush()

    print("Insertando contracts...")
    from app.models.contract import Contract as ContractModel
    for row in CONTRACTS:
        db.add(ContractModel(**row))
    await db.flush()

    print("Insertando contract_amendments...")
    from app.models.contract import ContractAmendment
    for row in AMENDMENTS:
        db.add(ContractAmendment(**row))

    print("Insertando contract_payments...")
    from app.models.contract import ContractPayment
    for row in PAYMENTS:
        db.add(ContractPayment(**row))

    print("Insertando risk_alerts...")
    for row in RISK_ALERTS:
        db.add(RiskAlert(**row))

    await db.commit()
    print("✓ Seed completado exitosamente.")


async def main() -> None:
    async with AsyncSessionLocal() as db:
        await seed(db)
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
