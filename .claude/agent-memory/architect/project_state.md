---
name: Estado del proyecto — MVP inicial
description: Estado arquitectónico actual del monorepo contrataciones-ve tras análisis completo del código (2026-03-15)
type: project
---

El proyecto está en estado de prototipo funcional inicial. Todo el código fue generado siguiendo el plan del CLAUDE.md y existe como un primer commit (todo en staging, sin commits previos).

**Stack implementado:**
- Backend: FastAPI + SQLAlchemy 2.0 async + asyncpg + Supabase (PostgreSQL)
- Frontend: Next.js 14 App Router + TypeScript + Tailwind CSS (dark mode, paleta Venezuela)
- DB: schema SQL manual en supabase/migrations/001_initial_schema.sql + seed.sql

**Lo que existe y funciona estructuralmente:**
- 4 modelos SQLAlchemy: Supplier, Process, Contract, RiskAlert
- 5 routers FastAPI: processes, contracts, suppliers, risk, download
- Motor de riesgo (risk_engine.py) con 4 checks: systematic_amendments, sanctioned_suppliers, low_competition, emergency_overprice
- Frontend con dashboard, listados de contratos/proveedores/alertas, detalles de contrato y proveedor
- Exportación CSV y OCDS JSON básica
- Schema SQL con índices, triggers updated_at, y 3 vistas (v_buyer_summary, v_supplier_concentration, v_dashboard_stats)

**Problemas críticos identificados en análisis 2026-03-15:**
1. Alembic desconectado de los modelos (target_metadata = None) — las migraciones no detectan cambios
2. contract_amendments y contract_payments existen en SQL y seed pero NO tienen modelos SQLAlchemy ni endpoints API
3. dashboard usa 7 llamadas HTTP en cascada para stats (antipatrón de rendimiento grave)
4. sort/time_field params en API son injection vectors — getattr sin whitelist
5. RiskEngine nunca se invoca desde ningún endpoint — está desconectado del sistema
6. download.py carga TODOS los registros en memoria sin paginación ni límite
7. Alembic env.py usa engine síncrono con asyncpg — incompatible
8. Frontend usa axios (cliente) en Server Components de Next.js App Router — correcto para SSR pero sin error boundary ni loading states
9. awards_count_12m y total_awarded_12m son campos desnormalizados calculados manualmente — propensos a inconsistencia
10. No existe ningún test

**Why:** El proyecto fue construido como prototipo de demostración rápido para validar el concepto. La deuda técnica estructural es esperada pero debe abordarse antes de exponer datos reales.

**How to apply:** Priorizar deuda técnica crítica (seguridad > trazabilidad > rendimiento) antes de agregar features. No asumir que el código actual es production-ready.
