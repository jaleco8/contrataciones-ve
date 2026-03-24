# AGENTS.md — Plan Maestro: Plataforma Abierta Anticorrupción Venezuela

> **Propósito de este documento**: Instrucciones completas y ordenadas para que Codex
> construya el monorepo `contrataciones-ve` desde cero. Ejecuta cada sección en orden.
> Autor del proyecto: Jesús Alexander León Cordero

---

## 0. Contexto del proyecto

Construir un **prototipo open-source** de una plataforma de transparencia de contratación pública
para Venezuela. La plataforma publica licitaciones, contratos, proveedores y alertas de riesgo
detectadas por IA, siguiendo el estándar **OCDS** (Open Contracting Data Standard).

**Stack exacto:**
- Backend: **Python 3.12 + FastAPI + SQLAlchemy 2.0 + Supabase (PostgreSQL)**
- Frontend: **Next.js 14 (App Router) + TypeScript + Tailwind CSS + shadcn/ui**
- Base de datos: **Supabase** (PostgreSQL managed)
- Monorepo: carpetas `backend/` y `frontend/` en la raíz
- Containerización: `docker-compose.yml` en la raíz

---

## 1. Estructura del monorepo

Crea exactamente esta estructura de archivos y carpetas:

```
contrataciones-ve/
├── AGENTS.md                        ← este archivo
├── README.md
├── docker-compose.yml
├── .gitignore
│
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── .env.example
│   ├── alembic.ini
│   ├── alembic/
│   │   ├── env.py
│   │   └── versions/
│   └── app/
│       ├── main.py
│       ├── core/
│       │   ├── __init__.py
│       │   ├── config.py
│       │   └── database.py
│       ├── models/
│       │   ├── __init__.py
│       │   ├── process.py
│       │   ├── contract.py
│       │   ├── supplier.py
│       │   └── risk_alert.py
│       ├── schemas/
│       │   ├── __init__.py
│       │   ├── process.py
│       │   ├── contract.py
│       │   ├── supplier.py
│       │   ├── risk_alert.py
│       │   └── common.py
│       ├── api/
│       │   ├── __init__.py
│       │   └── v1/
│       │       ├── __init__.py
│       │       ├── router.py
│       │       ├── processes.py
│       │       ├── contracts.py
│       │       ├── suppliers.py
│       │       ├── risk.py
│       │       └── download.py
│       ├── services/
│       │   ├── __init__.py
│       │   └── risk_engine.py
│       └── seed/
│           ├── __init__.py
│           └── seed_data.py
│
├── frontend/
│   ├── package.json
│   ├── next.config.js
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   ├── postcss.config.js
│   ├── .env.local.example
│   ├── public/
│   │   └── favicon.ico
│   ├── lib/
│   │   ├── api.ts
│   │   ├── types.ts
│   │   └── utils.ts
│   ├── components/
│   │   ├── ui/                      ← shadcn/ui components aquí
│   │   ├── layout/
│   │   │   ├── Navbar.tsx
│   │   │   └── Footer.tsx
│   │   ├── dashboard/
│   │   │   ├── StatCard.tsx
│   │   │   ├── RiskChart.tsx
│   │   │   └── RecentContracts.tsx
│   │   ├── contracts/
│   │   │   ├── ContractCard.tsx
│   │   │   ├── ContractTable.tsx
│   │   │   └── StatusBadge.tsx
│   │   ├── suppliers/
│   │   │   └── SupplierCard.tsx
│   │   └── risk/
│   │       ├── AlertCard.tsx
│   │       └── SeverityBadge.tsx
│   └── app/
│       ├── layout.tsx
│       ├── page.tsx                 ← Dashboard principal
│       ├── contracts/
│       │   ├── page.tsx             ← Listado de contratos
│       │   └── [id]/
│       │       └── page.tsx         ← Detalle de contrato
│       ├── suppliers/
│       │   ├── page.tsx
│       │   └── [id]/
│       │       └── page.tsx
│       ├── risk/
│       │   └── page.tsx             ← Panel de alertas
│       └── api/                     ← API routes de Next.js (proxies)
│           └── health/
│               └── route.ts
│
└── supabase/
    ├── migrations/
    │   └── 001_initial_schema.sql
    └── seed.sql
```

---

## 2. Archivos raíz

### `README.md`

```markdown
# Contrataciones VE — Plataforma Abierta Anticorrupción

Prototipo open-source de transparencia de contratación pública para Venezuela.
Basado en estándares OCDS (Open Contracting Data Standard).

**Autor:** Jesús Alexander León Cordero — Tech Lead | MSc. Ciencias de la Computación
**Licencia:** MIT
**Fecha:** 2026

## Stack
- Backend: Python 3.12 + FastAPI
- Frontend: Next.js 14 (App Router) + TypeScript
- Base de datos: Supabase (PostgreSQL)

## Inicio rápido

### Requisitos
- Python 3.12+
- Node.js 20+
- Cuenta en Supabase (supabase.com)
- Docker (opcional)

### 1. Clonar y configurar variables de entorno

```bash
git clone https://github.com/tu-usuario/contrataciones-ve
cd contrataciones-ve

# Backend
cp backend/.env.example backend/.env
# Editar backend/.env con tus credenciales de Supabase

# Frontend
cp frontend/.env.local.example frontend/.env.local
# Editar frontend/.env.local con la URL del backend
```

### 2. Inicializar la base de datos

Ejecutar el SQL de `supabase/migrations/001_initial_schema.sql` en el SQL Editor de Supabase.
Luego ejecutar `supabase/seed.sql` para datos de demostración.

### 3. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

API disponible en: http://localhost:8000
Docs interactivos: http://localhost:8000/docs

### 4. Frontend

```bash
cd frontend
npm install
npm run dev
```

App disponible en: http://localhost:3000

### 5. Con Docker

```bash
docker-compose up --build
```

## Endpoints principales

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | /api/v1/processes | Listado de procesos de contratación |
| GET | /api/v1/contracts | Listado de contratos |
| GET | /api/v1/suppliers | Listado de proveedores |
| GET | /api/v1/risk/alerts | Alertas de riesgo |
| GET | /api/v1/download/contracts.csv | Descarga masiva CSV |
| GET | /api/v1/download/ocds/releases.json | Exportación OCDS |

## Documentación
Ver `/docs` en el backend para la especificación OpenAPI completa.
```

### `.gitignore`

```gitignore
# Python
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/
.venv/
venv/
*.egg
.pytest_cache/
.mypy_cache/

# Environment
.env
.env.local
.env.*.local
!.env.example
!.env.local.example

# Node
node_modules/
.next/
out/
.npm

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Docker
*.pid
```

### `docker-compose.yml`

```yaml
version: "3.9"

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: contrataciones-ve-backend
    ports:
      - "8000:8000"
    env_file:
      - ./backend/.env
    volumes:
      - ./backend:/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    restart: unless-stopped

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: contrataciones-ve-frontend
    ports:
      - "3000:3000"
    env_file:
      - ./frontend/.env.local
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000
    depends_on:
      - backend
    restart: unless-stopped
```

---

## 3. Base de datos — Supabase

### `supabase/migrations/001_initial_schema.sql`

Ejecutar este SQL completo en el SQL Editor de Supabase:

```sql
-- ============================================================
-- PLATAFORMA ABIERTA ANTICORRUPCIÓN VENEZUELA
-- Schema inicial v1.0 — Compatible con OCDS
-- ============================================================

-- Extensiones
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- Para búsqueda de texto

-- ============================================================
-- TABLA: suppliers (proveedores)
-- ============================================================
CREATE TABLE IF NOT EXISTS suppliers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Identificación
    rif VARCHAR(20) UNIQUE NOT NULL,          -- J-12345678-9
    name VARCHAR(500) NOT NULL,
    legal_name VARCHAR(500),
    
    -- Clasificación
    sector VARCHAR(200),
    type VARCHAR(50) DEFAULT 'company',       -- company | individual | cooperative
    
    -- Estado
    sanction_status VARCHAR(50) DEFAULT 'active', -- active | sanctioned | suspended
    
    -- Métricas (actualizadas por trigger/servicio)
    awards_count_12m INTEGER DEFAULT 0,
    total_awarded_12m DECIMAL(20, 2) DEFAULT 0.00,
    
    -- Contacto
    address TEXT,
    state VARCHAR(100),                       -- Estado de Venezuela
    
    -- Auditoría
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Índices suppliers
CREATE INDEX idx_suppliers_rif ON suppliers(rif);
CREATE INDEX idx_suppliers_name_trgm ON suppliers USING GIN (name gin_trgm_ops);
CREATE INDEX idx_suppliers_sanction ON suppliers(sanction_status);
CREATE INDEX idx_suppliers_sector ON suppliers(sector);

-- ============================================================
-- TABLA: processes (procesos de contratación / licitaciones)
-- ============================================================
CREATE TABLE IF NOT EXISTS processes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Identificador OCDS
    ocid VARCHAR(100) UNIQUE,                 -- ocds-abc123-VE-2026-001
    
    -- Información básica
    title VARCHAR(1000) NOT NULL,
    description TEXT,
    
    -- Estado del proceso
    status VARCHAR(50) NOT NULL DEFAULT 'planned',
    -- planned | tender | awarded | cancelled | complete
    
    -- Modalidad de contratación
    procurement_method VARCHAR(100),
    -- open_tender | limited | direct | framework | emergency
    
    -- Comprador / Ente contratante
    buyer_name VARCHAR(500) NOT NULL,
    buyer_id VARCHAR(100),
    buyer_entity_type VARCHAR(100),           -- ministerio | gobernacion | municipio | ente
    
    -- Montos
    tender_amount DECIMAL(20, 2),
    tender_currency VARCHAR(10) DEFAULT 'USD',
    awarded_amount DECIMAL(20, 2),
    awarded_currency VARCHAR(10) DEFAULT 'USD',
    
    -- Proveedor adjudicado (FK opcional)
    awarded_supplier_id UUID REFERENCES suppliers(id),
    awarded_supplier_name VARCHAR(500),
    
    -- Fechas clave
    published_at TIMESTAMPTZ,
    tender_start_date DATE,
    tender_end_date DATE,
    award_date DATE,
    
    -- Categoría / objeto
    category VARCHAR(200),                    -- obras | bienes | servicios | consultoria
    cpv_code VARCHAR(50),                     -- Código de producto/servicio
    
    -- Número de oferentes
    bidders_count INTEGER DEFAULT 0,
    
    -- Auditoría
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Índices processes
CREATE INDEX idx_processes_ocid ON processes(ocid);
CREATE INDEX idx_processes_status ON processes(status);
CREATE INDEX idx_processes_buyer ON processes(buyer_name);
CREATE INDEX idx_processes_awarded_supplier ON processes(awarded_supplier_id);
CREATE INDEX idx_processes_category ON processes(category);
CREATE INDEX idx_processes_published ON processes(published_at DESC);
CREATE INDEX idx_processes_title_trgm ON processes USING GIN (title gin_trgm_ops);

-- ============================================================
-- TABLA: contracts (contratos)
-- ============================================================
CREATE TABLE IF NOT EXISTS contracts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Referencia interna
    contract_number VARCHAR(200) UNIQUE NOT NULL,
    
    -- Relación con proceso de contratación
    process_id UUID REFERENCES processes(id),
    
    -- Relación con proveedor
    supplier_id UUID REFERENCES suppliers(id),
    supplier_name VARCHAR(500) NOT NULL,
    
    -- Comprador
    buyer_name VARCHAR(500) NOT NULL,
    buyer_id VARCHAR(100),
    
    -- Objeto del contrato
    title VARCHAR(1000) NOT NULL,
    description TEXT,
    category VARCHAR(200),
    
    -- Estado
    status VARCHAR(50) NOT NULL DEFAULT 'draft',
    -- draft | active | completed | terminated | cancelled
    
    -- Montos
    amount DECIMAL(20, 2) NOT NULL,
    currency VARCHAR(10) DEFAULT 'USD',
    original_amount DECIMAL(20, 2),           -- Monto original antes de adendas
    
    -- Fechas
    signed_at DATE,
    start_date DATE,
    end_date DATE,
    
    -- Indicadores de riesgo (calculados por el motor)
    has_amendments BOOLEAN DEFAULT FALSE,
    amendments_count INTEGER DEFAULT 0,
    amendment_amount_increase DECIMAL(20, 2) DEFAULT 0.00,
    
    -- Auditoría
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    status_changed_at TIMESTAMPTZ
);

-- Índices contracts
CREATE INDEX idx_contracts_number ON contracts(contract_number);
CREATE INDEX idx_contracts_process ON contracts(process_id);
CREATE INDEX idx_contracts_supplier ON contracts(supplier_id);
CREATE INDEX idx_contracts_buyer ON contracts(buyer_name);
CREATE INDEX idx_contracts_status ON contracts(status);
CREATE INDEX idx_contracts_signed ON contracts(signed_at DESC);
CREATE INDEX idx_contracts_amount ON contracts(amount DESC);
CREATE INDEX idx_contracts_title_trgm ON contracts USING GIN (title gin_trgm_ops);

-- ============================================================
-- TABLA: contract_amendments (adendas)
-- ============================================================
CREATE TABLE IF NOT EXISTS contract_amendments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    contract_id UUID NOT NULL REFERENCES contracts(id) ON DELETE CASCADE,
    
    amendment_number INTEGER NOT NULL,
    description TEXT,
    
    -- Cambio de monto
    original_amount DECIMAL(20, 2),
    new_amount DECIMAL(20, 2),
    amount_change DECIMAL(20, 2),            -- new - original
    
    -- Cambio de plazo
    original_end_date DATE,
    new_end_date DATE,
    
    signed_at DATE,
    
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_amendments_contract ON contract_amendments(contract_id);

-- ============================================================
-- TABLA: contract_payments (pagos)
-- ============================================================
CREATE TABLE IF NOT EXISTS contract_payments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    contract_id UUID NOT NULL REFERENCES contracts(id) ON DELETE CASCADE,
    
    payment_number INTEGER NOT NULL,
    amount DECIMAL(20, 2) NOT NULL,
    currency VARCHAR(10) DEFAULT 'USD',
    
    status VARCHAR(50) DEFAULT 'paid',       -- pending | paid | cancelled
    payment_date DATE,
    description TEXT,
    
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_payments_contract ON contract_payments(contract_id);

-- ============================================================
-- TABLA: risk_alerts (alertas de riesgo)
-- ============================================================
CREATE TABLE IF NOT EXISTS risk_alerts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Tipo de alerta
    type VARCHAR(100) NOT NULL,
    -- overprice | repeat_entity | low_competition | systematic_amendments
    -- winner_rotation | emergency_procurement | short_bidding_period
    
    -- Severidad
    severity VARCHAR(20) NOT NULL DEFAULT 'medium',
    -- low | medium | high | critical
    
    -- Estado de revisión (human-in-the-loop)
    status VARCHAR(50) NOT NULL DEFAULT 'open',
    -- open | reviewed | dismissed
    
    -- Score de riesgo [0.0 - 1.0]
    score DECIMAL(4, 3) NOT NULL DEFAULT 0.500,
    
    -- Referencia a entidades involucradas
    contract_id UUID REFERENCES contracts(id),
    process_id UUID REFERENCES processes(id),
    supplier_id UUID REFERENCES suppliers(id),
    
    -- Explicación (human-readable, OCDS red flags)
    explanation JSONB NOT NULL DEFAULT '[]',
    -- Array de strings explicando por qué se generó la alerta
    
    -- Datos de soporte para auditoría
    supporting_data JSONB DEFAULT '{}',
    
    -- Revisión humana
    reviewed_by VARCHAR(200),
    reviewed_at TIMESTAMPTZ,
    review_notes TEXT,
    
    -- Timestamps
    generated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Índices risk_alerts
CREATE INDEX idx_alerts_type ON risk_alerts(type);
CREATE INDEX idx_alerts_severity ON risk_alerts(severity);
CREATE INDEX idx_alerts_status ON risk_alerts(status);
CREATE INDEX idx_alerts_contract ON risk_alerts(contract_id);
CREATE INDEX idx_alerts_supplier ON risk_alerts(supplier_id);
CREATE INDEX idx_alerts_generated ON risk_alerts(generated_at DESC);
CREATE INDEX idx_alerts_score ON risk_alerts(score DESC);

-- ============================================================
-- FUNCIÓN: actualizar updated_at automáticamente
-- ============================================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers para updated_at
CREATE TRIGGER update_suppliers_updated_at
    BEFORE UPDATE ON suppliers
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_processes_updated_at
    BEFORE UPDATE ON processes
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_contracts_updated_at
    BEFORE UPDATE ON contracts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_risk_alerts_updated_at
    BEFORE UPDATE ON risk_alerts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================
-- VISTAS útiles para el dashboard
-- ============================================================

-- Vista: resumen de contratos por comprador
CREATE OR REPLACE VIEW v_buyer_summary AS
SELECT
    buyer_name,
    COUNT(*) as contracts_count,
    SUM(amount) as total_amount,
    AVG(amount) as avg_amount,
    COUNT(CASE WHEN has_amendments THEN 1 END) as amended_count
FROM contracts
WHERE status != 'cancelled'
GROUP BY buyer_name
ORDER BY total_amount DESC;

-- Vista: proveedores con más contratos
CREATE OR REPLACE VIEW v_supplier_concentration AS
SELECT
    s.id,
    s.rif,
    s.name,
    s.sanction_status,
    COUNT(c.id) as contracts_count,
    SUM(c.amount) as total_amount,
    COUNT(DISTINCT c.buyer_name) as unique_buyers,
    COUNT(ra.id) as alerts_count
FROM suppliers s
LEFT JOIN contracts c ON c.supplier_id = s.id AND c.status != 'cancelled'
LEFT JOIN risk_alerts ra ON ra.supplier_id = s.id AND ra.status = 'open'
GROUP BY s.id, s.rif, s.name, s.sanction_status
ORDER BY total_amount DESC;

-- Vista: estadísticas generales del dashboard
CREATE OR REPLACE VIEW v_dashboard_stats AS
SELECT
    (SELECT COUNT(*) FROM contracts WHERE status = 'active') as active_contracts,
    (SELECT COUNT(*) FROM contracts) as total_contracts,
    (SELECT COALESCE(SUM(amount), 0) FROM contracts WHERE status != 'cancelled') as total_value_usd,
    (SELECT COUNT(*) FROM suppliers WHERE sanction_status = 'active') as active_suppliers,
    (SELECT COUNT(*) FROM risk_alerts WHERE status = 'open') as open_alerts,
    (SELECT COUNT(*) FROM risk_alerts WHERE severity IN ('high', 'critical') AND status = 'open') as critical_alerts,
    (SELECT COUNT(*) FROM processes WHERE status = 'tender') as active_tenders,
    (SELECT COUNT(*) FROM contracts WHERE has_amendments = TRUE) as amended_contracts;
```

### `supabase/seed.sql`

```sql
-- ============================================================
-- DATOS DE DEMOSTRACIÓN — Plataforma Anticorrupción Venezuela
-- Datos ficticios para propósitos de prototipo
-- ============================================================

-- PROVEEDORES
INSERT INTO suppliers (id, rif, name, sector, sanction_status, awards_count_12m, total_awarded_12m, state) VALUES
('11111111-1111-1111-1111-111111111111', 'J-12345678-9', 'Constructora Venezuela 2000 C.A.', 'Construcción e Infraestructura', 'active', 8, 4200000.00, 'Caracas'),
('22222222-2222-2222-2222-222222222222', 'J-98765432-1', 'TecnoSol Soluciones Tecnológicas C.A.', 'Tecnología e Informática', 'active', 12, 2800000.00, 'Caracas'),
('33333333-3333-3333-3333-333333333333', 'J-45678901-2', 'Suministros Industriales del Orinoco C.A.', 'Suministros y Equipos', 'active', 6, 1900000.00, 'Bolívar'),
('44444444-4444-4444-4444-444444444444', 'J-11223344-5', 'Grupo Médico Hospitalario Nacional C.A.', 'Salud y Equipos Médicos', 'active', 4, 3100000.00, 'Miranda'),
('55555555-5555-5555-5555-555555555555', 'J-55667788-3', 'Transporte y Logística Los Andes C.A.', 'Transporte y Logística', 'sanctioned', 2, 450000.00, 'Mérida'),
('66666666-6666-6666-6666-666666666666', 'J-99887766-4', 'Consultores Asociados Metropolis C.A.', 'Consultoría y Servicios Profesionales', 'active', 15, 1750000.00, 'Caracas'),
('77777777-7777-7777-7777-777777777777', 'J-33445566-7', 'Electricidad y Telecomunicaciones del Sur C.A.', 'Electricidad y Telecomunicaciones', 'active', 5, 2200000.00, 'Zulia'),
('88888888-8888-8888-8888-888888888888', 'J-77889900-6', 'Alimentos y Distribución Nacional C.A.', 'Alimentos y Distribución', 'active', 9, 890000.00, 'Aragua');

-- PROCESOS DE CONTRATACIÓN
INSERT INTO processes (id, ocid, title, description, status, procurement_method, buyer_name, buyer_entity_type, tender_amount, tender_currency, awarded_amount, awarded_currency, awarded_supplier_id, awarded_supplier_name, published_at, tender_start_date, tender_end_date, award_date, category, bidders_count) VALUES
('aaaa1111-1111-1111-1111-aaaaaaaaaaaa', 'ocds-ve-2026-001', 'Construcción y Rehabilitación de 500 km de Vías Nacionales — Fase I', 'Rehabilitación de infraestructura vial en los estados Carabobo, Aragua y Miranda', 'awarded', 'open_tender', 'Ministerio de Infraestructura y Obras Públicas', 'ministerio', 12500000.00, 'USD', 11800000.00, 'USD', '11111111-1111-1111-1111-111111111111', 'Constructora Venezuela 2000 C.A.', '2025-10-01 09:00:00+00', '2025-10-01', '2025-11-15', '2025-12-01', 'obras', 3),
('aaaa2222-2222-2222-2222-aaaaaaaaaaaa', 'ocds-ve-2026-002', 'Sistema Integral de Gestión Hospitalaria — Hospitales Públicos Nacionales', 'Plataforma tecnológica para gestión de pacientes, inventario y facturación en 45 hospitales', 'awarded', 'open_tender', 'Ministerio de Salud', 'ministerio', 4200000.00, 'USD', 4150000.00, 'USD', '22222222-2222-2222-2222-222222222222', 'TecnoSol Soluciones Tecnológicas C.A.', '2025-11-15 09:00:00+00', '2025-11-15', '2025-12-30', '2026-01-15', 'servicios', 2),
('aaaa3333-3333-3333-3333-aaaaaaaaaaaa', 'ocds-ve-2026-003', 'Adquisición de Equipos Médicos para Unidades de Cuidados Intensivos', 'Ventiladores, monitores y equipos de diagnóstico para 12 UCIs del país', 'awarded', 'limited', 'Ministerio de Salud', 'ministerio', 8900000.00, 'USD', 8750000.00, 'USD', '44444444-4444-4444-4444-444444444444', 'Grupo Médico Hospitalario Nacional C.A.', '2025-09-20 09:00:00+00', '2025-09-20', '2025-10-20', '2025-11-01', 'bienes', 4),
('aaaa4444-4444-4444-4444-aaaaaaaaaaaa', 'ocds-ve-2026-004', 'Servicio de Transporte Escolar Zona Metropolitana de Caracas', 'Servicio de transporte para 25,000 estudiantes de escuelas públicas', 'awarded', 'open_tender', 'Ministerio de Educación', 'ministerio', 2100000.00, 'USD', 1950000.00, 'USD', '55555555-5555-5555-5555-555555555555', 'Transporte y Logística Los Andes C.A.', '2025-08-10 09:00:00+00', '2025-08-10', '2025-09-10', '2025-09-25', 'servicios', 1),
('aaaa5555-5555-5555-5555-aaaaaaaaaaaa', 'ocds-ve-2026-005', 'Modernización del Sistema Eléctrico — Maracaibo Norte', 'Sustitución de transformadores y tendido eléctrico en sectores norte de Maracaibo', 'tender', 'open_tender', 'Corporación Eléctrica Nacional', 'ente', 15000000.00, 'USD', NULL, 'USD', NULL, NULL, '2026-02-01 09:00:00+00', '2026-02-01', '2026-03-15', NULL, 'obras', 0),
('aaaa6666-6666-6666-6666-aaaaaaaaaaaa', 'ocds-ve-2026-006', 'Consultoría para Diseño del Sistema Nacional de Datos Abiertos', 'Diseño de arquitectura y política para portal nacional de datos abiertos gubernamentales', 'awarded', 'direct', 'Ministerio de Ciencia y Tecnología', 'ministerio', 380000.00, 'USD', 375000.00, 'USD', '66666666-6666-6666-6666-666666666666', 'Consultores Asociados Metropolis C.A.', '2025-12-01 09:00:00+00', NULL, NULL, '2025-12-05', 'consultoria', 1),
('aaaa7777-7777-7777-7777-aaaaaaaaaaaa', 'ocds-ve-2026-007', 'Suministro de Materiales de Construcción — Obras de Emergencia Vargas', 'Materiales para reparación de viviendas afectadas por lluvias en La Guaira', 'awarded', 'emergency', 'Gobernación de La Guaira', 'gobernacion', 920000.00, 'USD', 1380000.00, 'USD', '33333333-3333-3333-3333-333333333333', 'Suministros Industriales del Orinoco C.A.', '2025-07-15 09:00:00+00', NULL, NULL, '2025-07-16', 'bienes', 1),
('aaaa8888-8888-8888-8888-aaaaaaaaaaaa', 'ocds-ve-2026-008', 'Implementación de Red de Fibra Óptica — Zona Industrial Guacara', 'Tendido de 120 km de fibra óptica para zona industrial de Carabobo', 'awarded', 'open_tender', 'Ministerio de Ciencia y Tecnología', 'ministerio', 3400000.00, 'USD', 3350000.00, 'USD', '77777777-7777-7777-7777-777777777777', 'Electricidad y Telecomunicaciones del Sur C.A.', '2025-10-15 09:00:00+00', '2025-10-15', '2025-11-30', '2025-12-15', 'obras', 3);

-- CONTRATOS
INSERT INTO contracts (id, contract_number, process_id, supplier_id, supplier_name, buyer_name, title, description, category, status, amount, currency, original_amount, signed_at, start_date, end_date, has_amendments, amendments_count, amendment_amount_increase) VALUES
('cccc1111-1111-1111-1111-cccccccccccc', 'CTR-MIOP-2026-001', 'aaaa1111-1111-1111-1111-aaaaaaaaaaaa', '11111111-1111-1111-1111-111111111111', 'Constructora Venezuela 2000 C.A.', 'Ministerio de Infraestructura y Obras Públicas', 'Construcción y Rehabilitación Vial — Fase I', 'Rehabilitación de vías nacionales Carabobo, Aragua y Miranda', 'obras', 'active', 14200000.00, 'USD', 11800000.00, '2025-12-15', '2026-01-01', '2027-06-30', TRUE, 2, 2400000.00),
('cccc2222-2222-2222-2222-cccccccccccc', 'CTR-MSALUD-2026-001', 'aaaa2222-2222-2222-2222-aaaaaaaaaaaa', '22222222-2222-2222-2222-222222222222', 'TecnoSol Soluciones Tecnológicas C.A.', 'Ministerio de Salud', 'Sistema Integral de Gestión Hospitalaria', 'Plataforma tecnológica 45 hospitales públicos', 'servicios', 'active', 4150000.00, 'USD', 4150000.00, '2026-01-20', '2026-02-01', '2026-12-31', FALSE, 0, 0.00),
('cccc3333-3333-3333-3333-cccccccccccc', 'CTR-MSALUD-2026-002', 'aaaa3333-3333-3333-3333-aaaaaaaaaaaa', '44444444-4444-4444-4444-444444444444', 'Grupo Médico Hospitalario Nacional C.A.', 'Ministerio de Salud', 'Equipos Médicos para UCIs', 'Ventiladores, monitores y equipos de diagnóstico para 12 UCIs', 'bienes', 'active', 8750000.00, 'USD', 8750000.00, '2025-11-10', '2025-11-15', '2026-03-31', FALSE, 0, 0.00),
('cccc4444-4444-4444-4444-cccccccccccc', 'CTR-MEDU-2026-001', 'aaaa4444-4444-4444-4444-aaaaaaaaaaaa', '55555555-5555-5555-5555-555555555555', 'Transporte y Logística Los Andes C.A.', 'Ministerio de Educación', 'Transporte Escolar Zona Metropolitana', 'Servicio de transporte 25,000 estudiantes', 'servicios', 'active', 1950000.00, 'USD', 1950000.00, '2025-10-01', '2025-10-15', '2026-06-30', FALSE, 0, 0.00),
('cccc5555-5555-5555-5555-cccccccccccc', 'CTR-MCT-2026-001', 'aaaa6666-6666-6666-6666-aaaaaaaaaaaa', '66666666-6666-6666-6666-666666666666', 'Consultores Asociados Metropolis C.A.', 'Ministerio de Ciencia y Tecnología', 'Consultoría Datos Abiertos — Contratación Directa', 'Diseño de arquitectura y política de datos abiertos', 'consultoria', 'active', 375000.00, 'USD', 375000.00, '2025-12-10', '2025-12-15', '2026-06-15', FALSE, 0, 0.00),
('cccc6666-6666-6666-6666-cccccccccccc', 'CTR-GLAGUAIRA-2026-001', 'aaaa7777-7777-7777-7777-aaaaaaaaaaaa', '33333333-3333-3333-3333-333333333333', 'Suministros Industriales del Orinoco C.A.', 'Gobernación de La Guaira', 'Materiales Construcción — Emergencia Vargas', 'Materiales para reparación viviendas afectadas por lluvias', 'bienes', 'active', 1380000.00, 'USD', 920000.00, '2025-07-17', '2025-07-17', '2025-12-31', TRUE, 1, 460000.00),
('cccc7777-7777-7777-7777-cccccccccccc', 'CTR-MCT-2026-002', 'aaaa8888-8888-8888-8888-aaaaaaaaaaaa', '77777777-7777-7777-7777-777777777777', 'Electricidad y Telecomunicaciones del Sur C.A.', 'Ministerio de Ciencia y Tecnología', 'Red Fibra Óptica — Zona Industrial Guacara', 'Tendido 120 km fibra óptica Carabobo', 'obras', 'active', 3350000.00, 'USD', 3350000.00, '2025-12-20', '2026-01-01', '2026-09-30', FALSE, 0, 0.00),
('cccc8888-8888-8888-8888-cccccccccccc', 'CTR-MCT-2026-003', NULL, '66666666-6666-6666-6666-666666666666', 'Consultores Asociados Metropolis C.A.', 'Ministerio de Planificación', 'Consultoría Reforma Tributaria Digital', 'Análisis y propuesta de digitalización del sistema tributario', 'consultoria', 'completed', 290000.00, 'USD', 290000.00, '2025-06-01', '2025-06-01', '2025-11-30', FALSE, 0, 0.00);

-- ADENDAS
INSERT INTO contract_amendments (contract_id, amendment_number, description, original_amount, new_amount, amount_change, original_end_date, new_end_date, signed_at) VALUES
('cccc1111-1111-1111-1111-cccccccccccc', 1, 'Ampliación de alcance: inclusión de 80 km adicionales en estado Miranda por derrumbes', 11800000.00, 13200000.00, 1400000.00, '2027-06-30', '2027-12-31', '2026-02-15'),
('cccc1111-1111-1111-1111-cccccccccccc', 2, 'Ajuste por variación de precios de materiales — índice inflacionario 2026-Q1', 13200000.00, 14200000.00, 1000000.00, '2027-12-31', '2028-03-31', '2026-03-01'),
('cccc6666-6666-6666-6666-cccccccccccc', 1, 'Incremento de scope: inclusión de municipios Vargas y Naiguatá no contemplados en diseño original', 920000.00, 1380000.00, 460000.00, '2025-12-31', '2025-12-31', '2025-09-01');

-- PAGOS
INSERT INTO contract_payments (contract_id, payment_number, amount, currency, status, payment_date, description) VALUES
('cccc1111-1111-1111-1111-cccccccccccc', 1, 3550000.00, 'USD', 'paid', '2026-01-15', 'Anticipo 25% — inicio de obras'),
('cccc1111-1111-1111-1111-cccccccccccc', 2, 4260000.00, 'USD', 'paid', '2026-02-28', 'Segundo pago 30% — avance de obra certificado'),
('cccc2222-2222-2222-2222-cccccccccccc', 1, 1245000.00, 'USD', 'paid', '2026-02-01', 'Anticipo 30% — inicio del proyecto'),
('cccc3333-3333-3333-3333-cccccccccccc', 1, 4375000.00, 'USD', 'paid', '2025-11-20', 'Pago total contra entrega de equipos'),
('cccc6666-6666-6666-6666-cccccccccccc', 1, 690000.00, 'USD', 'paid', '2025-07-20', 'Anticipo de emergencia 50%'),
('cccc6666-6666-6666-6666-cccccccccccc', 2, 690000.00, 'USD', 'paid', '2025-10-15', 'Segundo pago 50% — entrega parcial');

-- ALERTAS DE RIESGO
INSERT INTO risk_alerts (id, type, severity, status, score, contract_id, process_id, supplier_id, explanation, supporting_data, generated_at) VALUES

-- Alerta: sobrecostos en contrato de vialidad (adendas repetidas)
('aaaa0001-0000-0000-0000-000000000000', 'systematic_amendments', 'high', 'open', 0.875,
 'cccc1111-1111-1111-1111-cccccccccccc', 'aaaa1111-1111-1111-1111-aaaaaaaaaaaa', '11111111-1111-1111-1111-111111111111',
 '["Monto del contrato incrementado 20.3% en 75 días tras la firma", "2 adendas de incremento en menos de 90 días", "Ampliación de plazo de 9 meses adicionales sobre el contrato original", "Patrón: adendas múltiples de aumento en contratos de obras viales del mismo comprador"]',
 '{"original_amount": 11800000, "current_amount": 14200000, "increase_pct": 20.3, "amendments_count": 2, "days_since_signing": 75}',
 '2026-03-10 10:05:00+00'),

-- Alerta: proveedor sancionado adjudicado
('aaaa0002-0000-0000-0000-000000000000', 'repeat_entity', 'critical', 'open', 0.950,
 'cccc4444-4444-4444-4444-cccccccccccc', 'aaaa4444-4444-4444-4444-aaaaaaaaaaaa', '55555555-5555-5555-5555-555555555555',
 '["Proveedor con estatus SANCIONADO adjudicado en proceso activo", "Solo 1 oferente presentó propuesta (baja competencia)", "Proceso adjudicado al único oferente sin evaluación comparativa documentada", "Proveedor tiene registro de sanciones previas verificado en registro oficial"]',
 '{"sanction_status": "sanctioned", "bidders_count": 1, "procurement_method": "open_tender"}',
 '2026-03-08 14:30:00+00'),

-- Alerta: contratación directa sin justificación clara
('aaaa0003-0000-0000-0000-000000000000', 'low_competition', 'medium', 'open', 0.720,
 'cccc5555-5555-5555-5555-cccccccccccc', 'aaaa6666-6666-6666-6666-aaaaaaaaaaaa', '66666666-6666-6666-6666-666666666666',
 '["Modalidad de contratación directa para monto de USD 375,000", "No se registra proceso competitivo previo", "El mismo proveedor tiene 15 contratos en los últimos 12 meses con distintos entes", "Concentración: 1 proveedor, múltiples ministerios, patrón de contrataciones directas"]',
 '{"procurement_method": "direct", "amount": 375000, "supplier_contracts_12m": 15, "unique_buyers": 4}',
 '2026-03-05 09:15:00+00'),

-- Alerta: sobrecosto en emergencia
('aaaa0004-0000-0000-0000-000000000000', 'overprice', 'high', 'reviewed', 0.810,
 'cccc6666-6666-6666-6666-cccccccccccc', 'aaaa7777-7777-7777-7777-aaaaaaaaaaaa', '33333333-3333-3333-3333-333333333333',
 '["Monto final 50% superior al monto licitado (USD 920K → USD 1.38M)", "Modalidad de emergencia usada para ampliar scope original significativamente", "Adenda aplicada 45 días después de inicio por scope no contemplado en diseño de emergencia", "Patrón: contrataciones de emergencia con ampliaciones sistemáticas"]',
 '{"original_tender": 920000, "final_amount": 1380000, "overprice_pct": 50.0, "days_to_amendment": 45}',
 '2026-02-20 11:00:00+00'),

-- Alerta: concentración de proveedor
('aaaa0005-0000-0000-0000-000000000000', 'winner_rotation', 'low', 'dismissed', 0.450,
 NULL, NULL, '22222222-2222-2222-2222-222222222222',
 '["Proveedor TecnoSol adjudicado en 12 contratos en 12 meses", "Alta concentración en sector tecnología gubernamental", "Nota: los contratos muestran procesos competitivos con múltiples oferentes — alerta revisada y desestimada"]',
 '{"contracts_12m": 12, "total_awarded_12m": 2800000, "unique_buyers": 3}',
 '2026-01-15 08:00:00+00');

-- Actualizar métricas de proveedores
UPDATE suppliers SET awards_count_12m = 8, total_awarded_12m = 4200000.00 WHERE id = '11111111-1111-1111-1111-111111111111';
UPDATE suppliers SET awards_count_12m = 12, total_awarded_12m = 2800000.00 WHERE id = '22222222-2222-2222-2222-222222222222';
UPDATE suppliers SET awards_count_12m = 6, total_awarded_12m = 1900000.00 WHERE id = '33333333-3333-3333-3333-333333333333';
UPDATE suppliers SET awards_count_12m = 4, total_awarded_12m = 3100000.00 WHERE id = '44444444-4444-4444-4444-444444444444';
UPDATE suppliers SET awards_count_12m = 2, total_awarded_12m = 450000.00 WHERE id = '55555555-5555-5555-5555-555555555555';
UPDATE suppliers SET awards_count_12m = 15, total_awarded_12m = 1750000.00 WHERE id = '66666666-6666-6666-6666-666666666666';
UPDATE suppliers SET awards_count_12m = 5, total_awarded_12m = 2200000.00 WHERE id = '77777777-7777-7777-7777-777777777777';
```

---

## 4. Backend — Python / FastAPI

### `backend/.env.example`

```env
# Supabase
SUPABASE_URL=https://xxxxxxxxxxxx.supabase.co
SUPABASE_KEY=your-anon-key-here
DATABASE_URL=postgresql://postgres:your-password@db.xxxxxxxxxxxx.supabase.co:5432/postgres

# App
APP_NAME="Contrataciones VE - API"
APP_VERSION="1.0.0"
DEBUG=true
SECRET_KEY=your-secret-key-for-jwt-change-in-production

# CORS — agregar URL del frontend
CORS_ORIGINS=["http://localhost:3000","https://tu-frontend.vercel.app"]

# Paginación
DEFAULT_PAGE_SIZE=20
MAX_PAGE_SIZE=100
```

### `backend/requirements.txt`

```
fastapi==0.115.5
uvicorn[standard]==0.32.1
sqlalchemy==2.0.36
asyncpg==0.30.0
alembic==1.14.0
pydantic==2.10.3
pydantic-settings==2.7.0
python-dotenv==1.0.1
httpx==0.28.1
supabase==2.10.0
psycopg2-binary==2.9.10
pandas==2.2.3
python-dateutil==2.9.0.post0
pytest==8.3.4
pytest-asyncio==0.24.0
```

### `backend/app/core/config.py`

```python
from pydantic_settings import BaseSettings
from typing import List
import json


class Settings(BaseSettings):
    # App
    APP_NAME: str = "Contrataciones VE - API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""

    # Security
    SECRET_KEY: str = "changeme-in-production"

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
```

### `backend/app/core/database.py`

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

# Convertir URL de postgres a asyncpg
DATABASE_URL = settings.DATABASE_URL.replace(
    "postgresql://", "postgresql+asyncpg://"
).replace(
    "postgres://", "postgresql+asyncpg://"
)

engine = create_async_engine(
    DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
```

### `backend/app/models/supplier.py`

```python
from sqlalchemy import Column, String, Integer, Numeric, DateTime, text
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
import uuid


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    rif = Column(String(20), unique=True, nullable=False)
    name = Column(String(500), nullable=False)
    legal_name = Column(String(500))
    sector = Column(String(200))
    type = Column(String(50), default="company")
    sanction_status = Column(String(50), default="active")
    awards_count_12m = Column(Integer, default=0)
    total_awarded_12m = Column(Numeric(20, 2), default=0.00)
    address = Column(String)
    state = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=text("NOW()"))
    updated_at = Column(DateTime(timezone=True), server_default=text("NOW()"))
```

### `backend/app/models/process.py`

```python
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
```

### `backend/app/models/contract.py`

```python
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
```

### `backend/app/models/risk_alert.py`

```python
from sqlalchemy import Column, String, Numeric, DateTime, text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.core.database import Base
import uuid


class RiskAlert(Base):
    __tablename__ = "risk_alerts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = Column(String(100), nullable=False)
    severity = Column(String(20), nullable=False, default="medium")
    status = Column(String(50), nullable=False, default="open")
    score = Column(Numeric(4, 3), nullable=False, default=0.500)
    contract_id = Column(UUID(as_uuid=True), ForeignKey("contracts.id"))
    process_id = Column(UUID(as_uuid=True), ForeignKey("processes.id"))
    supplier_id = Column(UUID(as_uuid=True), ForeignKey("suppliers.id"))
    explanation = Column(JSONB, nullable=False, default=list)
    supporting_data = Column(JSONB, default=dict)
    reviewed_by = Column(String(200))
    reviewed_at = Column(DateTime(timezone=True))
    review_notes = Column(String)
    generated_at = Column(DateTime(timezone=True), server_default=text("NOW()"))
    updated_at = Column(DateTime(timezone=True), server_default=text("NOW()"))
```

### `backend/app/models/__init__.py`

```python
from app.models.supplier import Supplier
from app.models.process import Process
from app.models.contract import Contract
from app.models.risk_alert import RiskAlert

__all__ = ["Supplier", "Process", "Contract", "RiskAlert"]
```

### `backend/app/schemas/common.py`

```python
from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime


class PaginationMeta(BaseModel):
    page: int
    page_size: int
    total_results: int
    total_pages: int
    sort: str
    order: str
    timezone: str = "UTC"
    interval_semantics: str = "[from,to)"
    request_id: Optional[str] = None


class PaginatedResponse(BaseModel):
    meta: PaginationMeta
    data: List[Any]
```

### `backend/app/schemas/supplier.py`

```python
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid


class SupplierBase(BaseModel):
    rif: str
    name: str
    legal_name: Optional[str] = None
    sector: Optional[str] = None
    type: str = "company"
    sanction_status: str = "active"
    state: Optional[str] = None


class SupplierResponse(SupplierBase):
    id: uuid.UUID
    awards_count_12m: int = 0
    total_awarded_12m: float = 0.0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

### `backend/app/schemas/contract.py`

```python
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
import uuid


class ContractResponse(BaseModel):
    id: uuid.UUID
    contract_number: str
    process_id: Optional[uuid.UUID] = None
    supplier_id: Optional[uuid.UUID] = None
    supplier_name: str
    buyer_name: str
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    status: str
    amount: float
    currency: str = "USD"
    original_amount: Optional[float] = None
    signed_at: Optional[date] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    has_amendments: bool = False
    amendments_count: int = 0
    amendment_amount_increase: float = 0.0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

### `backend/app/schemas/process.py`

```python
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
import uuid


class ProcessResponse(BaseModel):
    id: uuid.UUID
    ocid: Optional[str] = None
    title: str
    description: Optional[str] = None
    status: str
    procurement_method: Optional[str] = None
    buyer_name: str
    buyer_entity_type: Optional[str] = None
    tender_amount: Optional[float] = None
    tender_currency: str = "USD"
    awarded_amount: Optional[float] = None
    awarded_supplier_name: Optional[str] = None
    published_at: Optional[datetime] = None
    award_date: Optional[date] = None
    category: Optional[str] = None
    bidders_count: int = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

### `backend/app/schemas/risk_alert.py`

```python
from pydantic import BaseModel
from typing import Optional, List, Any, Dict
from datetime import datetime
import uuid


class RiskAlertResponse(BaseModel):
    id: uuid.UUID
    type: str
    severity: str
    status: str
    score: float
    contract_id: Optional[uuid.UUID] = None
    process_id: Optional[uuid.UUID] = None
    supplier_id: Optional[uuid.UUID] = None
    explanation: List[str] = []
    supporting_data: Dict[str, Any] = {}
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    review_notes: Optional[str] = None
    generated_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class RiskAlertUpdate(BaseModel):
    status: Optional[str] = None          # open | reviewed | dismissed
    reviewed_by: Optional[str] = None
    review_notes: Optional[str] = None
```

### `backend/app/api/v1/processes.py`

```python
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from typing import Optional
from datetime import date
import math

from app.core.database import get_db
from app.models.process import Process
from app.schemas.process import ProcessResponse
from app.schemas.common import PaginatedResponse, PaginationMeta

router = APIRouter()


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
    sort_col = getattr(Process, sort, Process.published_at)
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
async def get_process(process_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Process).where(Process.id == process_id))
    process = result.scalar_one_or_none()
    if not process:
        raise HTTPException(status_code=404, detail="Proceso no encontrado")
    return ProcessResponse.model_validate(process)
```

### `backend/app/api/v1/contracts.py`

```python
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from typing import Optional
from datetime import date
import math

from app.core.database import get_db
from app.models.contract import Contract
from app.schemas.contract import ContractResponse
from app.schemas.common import PaginatedResponse, PaginationMeta

router = APIRouter()


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

    sort_col = getattr(Contract, sort, Contract.signed_at)
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
async def get_contract(contract_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Contract).where(Contract.id == contract_id))
    contract = result.scalar_one_or_none()
    if not contract:
        raise HTTPException(status_code=404, detail="Contrato no encontrado")
    return ContractResponse.model_validate(contract)
```

### `backend/app/api/v1/suppliers.py`

```python
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from typing import Optional
import math

from app.core.database import get_db
from app.models.supplier import Supplier
from app.schemas.supplier import SupplierResponse
from app.schemas.common import PaginatedResponse, PaginationMeta

router = APIRouter()


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

    sort_col = getattr(Supplier, sort, Supplier.total_awarded_12m)
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
async def get_supplier(supplier_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Supplier).where(Supplier.id == supplier_id))
    supplier = result.scalar_one_or_none()
    if not supplier:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return SupplierResponse.model_validate(supplier)
```

### `backend/app/api/v1/risk.py`

```python
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional
from datetime import date, datetime, timezone
import math

from app.core.database import get_db
from app.models.risk_alert import RiskAlert
from app.schemas.risk_alert import RiskAlertResponse, RiskAlertUpdate
from app.schemas.common import PaginatedResponse, PaginationMeta

router = APIRouter()


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

    sort_col = getattr(RiskAlert, sort, RiskAlert.generated_at)
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
async def get_alert(alert_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(RiskAlert).where(RiskAlert.id == alert_id))
    alert = result.scalar_one_or_none()
    if not alert:
        raise HTTPException(status_code=404, detail="Alerta no encontrada")
    return RiskAlertResponse.model_validate(alert)


@router.patch("/alerts/{alert_id}", response_model=RiskAlertResponse,
              summary="Revisar o desestimar alerta (human-in-the-loop)")
async def update_alert(
    alert_id: str,
    update_data: RiskAlertUpdate,
    db: AsyncSession = Depends(get_db)
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
```

### `backend/app/api/v1/download.py`

```python
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import csv
import io
import json
from datetime import datetime, timezone

from app.core.database import get_db
from app.models.contract import Contract
from app.models.process import Process

router = APIRouter()


@router.get("/contracts.csv", summary="Descarga masiva de contratos en CSV")
async def download_contracts_csv(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Contract).order_by(Contract.signed_at.desc()))
    contracts = result.scalars().all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "id", "contract_number", "title", "buyer_name", "supplier_name",
        "amount", "currency", "status", "category", "signed_at",
        "start_date", "end_date", "has_amendments", "amendments_count"
    ])
    for c in contracts:
        writer.writerow([
            str(c.id), c.contract_number, c.title, c.buyer_name, c.supplier_name,
            float(c.amount), c.currency, c.status, c.category,
            c.signed_at, c.start_date, c.end_date, c.has_amendments, c.amendments_count
        ])

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
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
```

### `backend/app/api/v1/router.py`

```python
from fastapi import APIRouter
from app.api.v1 import processes, contracts, suppliers, risk, download

api_router = APIRouter()

api_router.include_router(processes.router, prefix="/processes", tags=["Procesos de Contratación"])
api_router.include_router(contracts.router, prefix="/contracts", tags=["Contratos"])
api_router.include_router(suppliers.router, prefix="/suppliers", tags=["Proveedores"])
api_router.include_router(risk.router, prefix="/risk", tags=["Alertas de Riesgo"])
api_router.include_router(download.router, prefix="/download", tags=["Descargas"])
```

### `backend/app/services/risk_engine.py`

Motor de riesgo simplificado (red flags OCDS):

```python
"""
Motor de riesgo — Plataforma Anticorrupción Venezuela
Implementa banderas rojas basadas en OCDS Red Flags for Integrity
Todas las alertas generadas son señales para revisión humana, NO conclusiones.
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
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
        """Persiste las alertas generadas en la base de datos."""
        count = 0
        for alert_data in alerts:
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
```

### `backend/app/main.py`

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import json

from app.core.config import settings
from app.api.v1.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION} iniciando...")
    yield
    print("Cerrando conexiones...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
## Plataforma Abierta Anticorrupción Venezuela

API pública para transparencia de contratación y gasto público.

### Características
- **OCDS Compatible**: Datos estructurados según Open Contracting Data Standard
- **Alertas de riesgo**: Motor de detección con revisión humana obligatoria
- **Descarga masiva**: CSV y JSON OCDS disponibles sin autenticación
- **Paginación estándar**: Metadatos completos en todas las respuestas

### Licencia
MIT — Uso libre con atribución al autor.

**Autor:** Jesús Alexander León Cordero
    """,
    openapi_tags=[
        {"name": "Procesos de Contratación", "description": "Licitaciones y procesos de compra pública"},
        {"name": "Contratos", "description": "Contratos firmados con trazabilidad de adendas y pagos"},
        {"name": "Proveedores", "description": "Registro de empresas y proveedores del Estado"},
        {"name": "Alertas de Riesgo", "description": "Banderas rojas con revisión human-in-the-loop"},
        {"name": "Descargas", "description": "Exportaciones masivas CSV y OCDS JSON"},
    ],
    lifespan=lifespan
)

# CORS
origins = settings.CORS_ORIGINS if isinstance(settings.CORS_ORIGINS, list) else json.loads(settings.CORS_ORIGINS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas
app.include_router(api_router, prefix="/api/v1")


@app.get("/", tags=["Health"], summary="Raíz de la API")
async def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "operational",
        "docs": "/docs",
        "api": "/api/v1",
        "license": "MIT",
        "author": "Jesús Alexander León Cordero",
        "standard": "OCDS v1.1",
    }


@app.get("/health", tags=["Health"], summary="Health check")
async def health():
    return {"status": "ok"}
```

### `backend/Dockerfile`

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 5. Frontend — Next.js 14

### `frontend/package.json`

```json
{
  "name": "contrataciones-ve-frontend",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "14.2.16",
    "react": "^18",
    "react-dom": "^18",
    "@tanstack/react-query": "^5.59.20",
    "axios": "^1.7.7",
    "clsx": "^2.1.1",
    "tailwind-merge": "^2.5.4",
    "lucide-react": "^0.460.0",
    "recharts": "^2.13.3",
    "date-fns": "^4.1.0",
    "@radix-ui/react-dialog": "^1.1.2",
    "@radix-ui/react-badge": "^1.0.0",
    "@radix-ui/react-select": "^2.1.2",
    "@radix-ui/react-tooltip": "^1.1.3"
  },
  "devDependencies": {
    "typescript": "^5",
    "@types/node": "^20",
    "@types/react": "^18",
    "@types/react-dom": "^18",
    "tailwindcss": "^3.4.14",
    "postcss": "^8",
    "autoprefixer": "^10",
    "eslint": "^8",
    "eslint-config-next": "14.2.16"
  }
}
```

### `frontend/.env.local.example`

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME="Contrataciones VE"
NEXT_PUBLIC_APP_VERSION="1.0.0"
```

### `frontend/next.config.js`

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/backend/:path*',
        destination: `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/:path*`,
      },
    ];
  },
};

module.exports = nextConfig;
```

### `frontend/tailwind.config.ts`

```typescript
import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // Paleta Venezuela: rojo, amarillo, azul + dark slate para gobierno
        ve: {
          red: "#CF142B",
          yellow: "#F4C430",
          blue: "#003DA5",
          dark: "#0D1117",
          slate: "#1B2432",
          border: "#2D3748",
          muted: "#4A5568",
          text: "#E2E8F0",
        },
        risk: {
          critical: "#FF3B30",
          high: "#FF9500",
          medium: "#FFCC00",
          low: "#34C759",
        }
      },
      fontFamily: {
        display: ["'IBM Plex Mono'", "monospace"],
        body: ["'IBM Plex Sans'", "sans-serif"],
      },
    },
  },
  plugins: [],
};

export default config;
```

### `frontend/lib/types.ts`

```typescript
export interface PaginationMeta {
  page: number;
  page_size: number;
  total_results: number;
  total_pages: number;
  sort: string;
  order: string;
  timezone: string;
}

export interface PaginatedResponse<T> {
  meta: PaginationMeta;
  data: T[];
}

export interface Contract {
  id: string;
  contract_number: string;
  process_id?: string;
  supplier_id?: string;
  supplier_name: string;
  buyer_name: string;
  title: string;
  description?: string;
  category?: string;
  status: ContractStatus;
  amount: number;
  currency: string;
  original_amount?: number;
  signed_at?: string;
  start_date?: string;
  end_date?: string;
  has_amendments: boolean;
  amendments_count: number;
  amendment_amount_increase: number;
  created_at: string;
  updated_at: string;
}

export type ContractStatus = "draft" | "active" | "completed" | "terminated" | "cancelled";

export interface Process {
  id: string;
  ocid?: string;
  title: string;
  description?: string;
  status: ProcessStatus;
  procurement_method?: string;
  buyer_name: string;
  buyer_entity_type?: string;
  tender_amount?: number;
  tender_currency: string;
  awarded_amount?: number;
  awarded_supplier_name?: string;
  published_at?: string;
  award_date?: string;
  category?: string;
  bidders_count: number;
  created_at: string;
  updated_at: string;
}

export type ProcessStatus = "planned" | "tender" | "awarded" | "cancelled" | "complete";

export interface Supplier {
  id: string;
  rif: string;
  name: string;
  legal_name?: string;
  sector?: string;
  type: string;
  sanction_status: SanctionStatus;
  awards_count_12m: number;
  total_awarded_12m: number;
  state?: string;
  created_at: string;
  updated_at: string;
}

export type SanctionStatus = "active" | "sanctioned" | "suspended";

export interface RiskAlert {
  id: string;
  type: AlertType;
  severity: AlertSeverity;
  status: AlertStatus;
  score: number;
  contract_id?: string;
  process_id?: string;
  supplier_id?: string;
  explanation: string[];
  supporting_data: Record<string, unknown>;
  reviewed_by?: string;
  reviewed_at?: string;
  review_notes?: string;
  generated_at: string;
  updated_at: string;
}

export type AlertType =
  | "overprice"
  | "repeat_entity"
  | "low_competition"
  | "systematic_amendments"
  | "winner_rotation"
  | "emergency_procurement"
  | "short_bidding_period";

export type AlertSeverity = "low" | "medium" | "high" | "critical";
export type AlertStatus = "open" | "reviewed" | "dismissed";

export interface DashboardStats {
  active_contracts: number;
  total_contracts: number;
  total_value_usd: number;
  active_suppliers: number;
  open_alerts: number;
  critical_alerts: number;
  active_tenders: number;
  amended_contracts: number;
}
```

### `frontend/lib/api.ts`

```typescript
import axios from "axios";
import type {
  PaginatedResponse,
  Contract,
  Process,
  Supplier,
  RiskAlert,
  DashboardStats,
} from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const api = axios.create({
  baseURL: `${API_BASE}/api/v1`,
  timeout: 15000,
  headers: {
    "Content-Type": "application/json",
  },
});

// Contratos
export async function getContracts(params?: Record<string, unknown>): Promise<PaginatedResponse<Contract>> {
  const { data } = await api.get("/contracts", { params });
  return data;
}

export async function getContract(id: string): Promise<Contract> {
  const { data } = await api.get(`/contracts/${id}`);
  return data;
}

// Procesos
export async function getProcesses(params?: Record<string, unknown>): Promise<PaginatedResponse<Process>> {
  const { data } = await api.get("/processes", { params });
  return data;
}

export async function getProcess(id: string): Promise<Process> {
  const { data } = await api.get(`/processes/${id}`);
  return data;
}

// Proveedores
export async function getSuppliers(params?: Record<string, unknown>): Promise<PaginatedResponse<Supplier>> {
  const { data } = await api.get("/suppliers", { params });
  return data;
}

export async function getSupplier(id: string): Promise<Supplier> {
  const { data } = await api.get(`/suppliers/${id}`);
  return data;
}

// Alertas
export async function getRiskAlerts(params?: Record<string, unknown>): Promise<PaginatedResponse<RiskAlert>> {
  const { data } = await api.get("/risk/alerts", { params });
  return data;
}

export async function updateAlert(
  id: string,
  update: { status?: string; reviewed_by?: string; review_notes?: string }
): Promise<RiskAlert> {
  const { data } = await api.patch(`/risk/alerts/${id}`, update);
  return data;
}

// Dashboard stats — consulta directa a la vista de Supabase
export async function getDashboardStats(): Promise<DashboardStats> {
  // Para el MVP, calculamos desde los endpoints disponibles
  const [contracts, alerts, suppliers, tenders] = await Promise.all([
    getContracts({ page_size: 1, status: "active" }),
    getRiskAlerts({ page_size: 1, status: "open" }),
    getSuppliers({ page_size: 1, sanction_status: "active" }),
    getProcesses({ page_size: 1, status: "tender" }),
  ]);

  const allContracts = await getContracts({ page_size: 1 });
  const criticalAlerts = await getRiskAlerts({ page_size: 1, status: "open", severity: "critical" });
  const amendedContracts = await getContracts({ page_size: 1, has_amendments: true });

  return {
    active_contracts: contracts.meta.total_results,
    total_contracts: allContracts.meta.total_results,
    total_value_usd: 0, // Se calcula en el servidor idealmente
    active_suppliers: suppliers.meta.total_results,
    open_alerts: alerts.meta.total_results,
    critical_alerts: criticalAlerts.meta.total_results,
    active_tenders: tenders.meta.total_results,
    amended_contracts: amendedContracts.meta.total_results,
  };
}
```

### `frontend/lib/utils.ts`

```typescript
import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";
import type { AlertSeverity, AlertType, ContractStatus, SanctionStatus } from "./types";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatCurrency(amount: number, currency = "USD"): string {
  return new Intl.NumberFormat("es-VE", {
    style: "currency",
    currency,
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(amount);
}

export function formatDate(dateStr?: string | null): string {
  if (!dateStr) return "—";
  return new Intl.DateTimeFormat("es-VE", {
    year: "numeric",
    month: "short",
    day: "numeric",
  }).format(new Date(dateStr));
}

export function getSeverityColor(severity: AlertSeverity): string {
  const colors: Record<AlertSeverity, string> = {
    critical: "text-red-400 bg-red-400/10 border-red-400/30",
    high: "text-orange-400 bg-orange-400/10 border-orange-400/30",
    medium: "text-yellow-400 bg-yellow-400/10 border-yellow-400/30",
    low: "text-green-400 bg-green-400/10 border-green-400/30",
  };
  return colors[severity];
}

export function getStatusColor(status: ContractStatus): string {
  const colors: Record<ContractStatus, string> = {
    active: "text-green-400 bg-green-400/10",
    completed: "text-blue-400 bg-blue-400/10",
    draft: "text-gray-400 bg-gray-400/10",
    terminated: "text-orange-400 bg-orange-400/10",
    cancelled: "text-red-400 bg-red-400/10",
  };
  return colors[status] || "text-gray-400 bg-gray-400/10";
}

export function getSanctionColor(status: SanctionStatus): string {
  const colors: Record<SanctionStatus, string> = {
    active: "text-green-400 bg-green-400/10",
    sanctioned: "text-red-400 bg-red-400/10",
    suspended: "text-orange-400 bg-orange-400/10",
  };
  return colors[status];
}

export function getAlertTypeLabel(type: AlertType): string {
  const labels: Record<AlertType, string> = {
    overprice: "Sobrecosto",
    repeat_entity: "Entidad Sancionada",
    low_competition: "Baja Competencia",
    systematic_amendments: "Adendas Sistemáticas",
    winner_rotation: "Concentración",
    emergency_procurement: "Emergencia",
    short_bidding_period: "Plazo Corto",
  };
  return labels[type] || type;
}

export function getProcurementMethodLabel(method?: string): string {
  const labels: Record<string, string> = {
    open_tender: "Concurso Abierto",
    limited: "Concurso Limitado",
    direct: "Contratación Directa",
    framework: "Marco de Acuerdo",
    emergency: "Emergencia",
  };
  return method ? (labels[method] || method) : "—";
}
```

### `frontend/app/layout.tsx`

```tsx
import type { Metadata } from "next";
import "./globals.css";
import { Navbar } from "@/components/layout/Navbar";
import { Footer } from "@/components/layout/Footer";

export const metadata: Metadata = {
  title: "Contrataciones VE — Transparencia Pública",
  description:
    "Plataforma abierta anticorrupción de contratación y gasto público para Venezuela. Datos abiertos, alertas de riesgo y auditoría social.",
  keywords: ["Venezuela", "contratos", "transparencia", "anticorrupción", "datos abiertos"],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="es" className="dark">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="bg-ve-dark text-ve-text font-body antialiased min-h-screen flex flex-col">
        <Navbar />
        <main className="flex-1">{children}</main>
        <Footer />
      </body>
    </html>
  );
}
```

### `frontend/app/globals.css`

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --ve-red: #CF142B;
  --ve-yellow: #F4C430;
  --ve-blue: #003DA5;
}

body {
  background-color: #0D1117;
}

/* Scrollbar dark */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}
::-webkit-scrollbar-track {
  background: #1B2432;
}
::-webkit-scrollbar-thumb {
  background: #4A5568;
  border-radius: 3px;
}

/* Selección */
::selection {
  background: rgba(207, 20, 43, 0.3);
  color: #F4C430;
}
```

### `frontend/components/layout/Navbar.tsx`

```tsx
import Link from "next/link";
import { Shield, FileText, Users, AlertTriangle, Download } from "lucide-react";

const navLinks = [
  { href: "/contracts", label: "Contratos", icon: FileText },
  { href: "/suppliers", label: "Proveedores", icon: Users },
  { href: "/risk", label: "Alertas", icon: AlertTriangle },
];

export function Navbar() {
  return (
    <nav className="border-b border-ve-border bg-ve-slate/50 backdrop-blur-sm sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-3 group">
            <div className="relative">
              <Shield className="w-7 h-7 text-ve-red group-hover:text-ve-yellow transition-colors" />
            </div>
            <div className="hidden sm:block">
              <div className="font-display text-sm font-semibold text-ve-text">
                CONTRATACIONES
              </div>
              <div className="font-display text-xs text-ve-yellow tracking-widest">
                VENEZUELA
              </div>
            </div>
          </Link>

          {/* Nav Links */}
          <div className="flex items-center gap-1">
            {navLinks.map(({ href, label, icon: Icon }) => (
              <Link
                key={href}
                href={href}
                className="flex items-center gap-2 px-3 py-2 rounded-lg text-sm text-ve-muted hover:text-ve-text hover:bg-ve-border/50 transition-all"
              >
                <Icon className="w-4 h-4" />
                <span className="hidden md:inline">{label}</span>
              </Link>
            ))}
            
            {/* API Link */}
            <a
              href={`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/docs`}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-2 px-3 py-2 rounded-lg text-sm text-ve-blue hover:text-ve-yellow hover:bg-ve-border/50 transition-all ml-2"
            >
              <Download className="w-4 h-4" />
              <span className="hidden md:inline font-display text-xs">API</span>
            </a>
          </div>
        </div>
      </div>
    </nav>
  );
}
```

### `frontend/components/layout/Footer.tsx`

```tsx
export function Footer() {
  return (
    <footer className="border-t border-ve-border bg-ve-slate/30 mt-16">
      <div className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="text-center md:text-left">
            <p className="font-display text-xs text-ve-muted">
              Plataforma Abierta Anticorrupción Venezuela — Prototipo v1.0
            </p>
            <p className="font-display text-xs text-ve-muted/60 mt-1">
              Autor: Jesús Alexander León Cordero | Tech Lead | MSc. Ciencias de la Computación
            </p>
          </div>
          <div className="flex items-center gap-4">
            <span className="text-xs text-ve-muted font-display">OCDS v1.1</span>
            <span className="text-xs text-ve-muted font-display">MIT License</span>
            <span className="text-xs text-ve-muted font-display">CC BY 4.0</span>
          </div>
        </div>
      </div>
    </footer>
  );
}
```

### `frontend/components/risk/SeverityBadge.tsx`

```tsx
import { cn, getSeverityColor } from "@/lib/utils";
import type { AlertSeverity } from "@/lib/types";

interface Props {
  severity: AlertSeverity;
  className?: string;
}

const LABELS: Record<AlertSeverity, string> = {
  critical: "CRÍTICA",
  high: "ALTA",
  medium: "MEDIA",
  low: "BAJA",
};

export function SeverityBadge({ severity, className }: Props) {
  return (
    <span
      className={cn(
        "inline-flex items-center px-2 py-0.5 rounded text-xs font-display font-medium border",
        getSeverityColor(severity),
        className
      )}
    >
      {LABELS[severity]}
    </span>
  );
}
```

### `frontend/components/contracts/StatusBadge.tsx`

```tsx
import { cn, getStatusColor } from "@/lib/utils";
import type { ContractStatus } from "@/lib/types";

const LABELS: Record<ContractStatus, string> = {
  active: "Activo",
  completed: "Completado",
  draft: "Borrador",
  terminated: "Terminado",
  cancelled: "Cancelado",
};

export function StatusBadge({ status }: { status: ContractStatus }) {
  return (
    <span className={cn("inline-flex px-2 py-0.5 rounded text-xs font-medium", getStatusColor(status))}>
      {LABELS[status]}
    </span>
  );
}
```

### `frontend/app/page.tsx` — Dashboard Principal

```tsx
import Link from "next/link";
import {
  FileText, Users, AlertTriangle, TrendingUp,
  Shield, ArrowRight, Activity, Database
} from "lucide-react";
import { getContracts, getRiskAlerts, getSuppliers, getProcesses } from "@/lib/api";
import { formatCurrency } from "@/lib/utils";
import { SeverityBadge } from "@/components/risk/SeverityBadge";
import { StatusBadge } from "@/components/contracts/StatusBadge";
import type { AlertSeverity, ContractStatus } from "@/lib/types";

async function getDashboardData() {
  const [
    activeContracts,
    allContracts,
    openAlerts,
    criticalAlerts,
    suppliers,
    tenders,
    recentContracts,
    recentAlerts,
  ] = await Promise.allSettled([
    getContracts({ page_size: 1, status: "active" }),
    getContracts({ page_size: 1 }),
    getRiskAlerts({ page_size: 1, status: "open" }),
    getRiskAlerts({ page_size: 1, status: "open", severity: "critical" }),
    getSuppliers({ page_size: 1 }),
    getProcesses({ page_size: 1, status: "tender" }),
    getContracts({ page_size: 5, sort: "signed_at", order: "desc" }),
    getRiskAlerts({ page_size: 4, status: "open", sort: "score", order: "desc" }),
  ]);

  return {
    stats: {
      activeContracts: activeContracts.status === "fulfilled" ? activeContracts.value.meta.total_results : 0,
      totalContracts: allContracts.status === "fulfilled" ? allContracts.value.meta.total_results : 0,
      openAlerts: openAlerts.status === "fulfilled" ? openAlerts.value.meta.total_results : 0,
      criticalAlerts: criticalAlerts.status === "fulfilled" ? criticalAlerts.value.meta.total_results : 0,
      totalSuppliers: suppliers.status === "fulfilled" ? suppliers.value.meta.total_results : 0,
      activeTenders: tenders.status === "fulfilled" ? tenders.value.meta.total_results : 0,
    },
    recentContracts: recentContracts.status === "fulfilled" ? recentContracts.value.data : [],
    recentAlerts: recentAlerts.status === "fulfilled" ? recentAlerts.value.data : [],
  };
}

export default async function DashboardPage() {
  const { stats, recentContracts, recentAlerts } = await getDashboardData();

  const statCards = [
    {
      label: "Contratos Activos",
      value: stats.activeContracts,
      total: `de ${stats.totalContracts} totales`,
      icon: FileText,
      color: "text-blue-400",
      bg: "bg-blue-400/10",
      href: "/contracts",
    },
    {
      label: "Alertas Abiertas",
      value: stats.openAlerts,
      total: `${stats.criticalAlerts} críticas`,
      icon: AlertTriangle,
      color: stats.criticalAlerts > 0 ? "text-red-400" : "text-orange-400",
      bg: stats.criticalAlerts > 0 ? "bg-red-400/10" : "bg-orange-400/10",
      href: "/risk",
    },
    {
      label: "Proveedores",
      value: stats.totalSuppliers,
      total: "registrados",
      icon: Users,
      color: "text-green-400",
      bg: "bg-green-400/10",
      href: "/suppliers",
    },
    {
      label: "Licitaciones Activas",
      value: stats.activeTenders,
      total: "en proceso",
      icon: Activity,
      color: "text-yellow-400",
      bg: "bg-yellow-400/10",
      href: "/contracts",
    },
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      
      {/* Hero */}
      <div className="mb-10">
        <div className="flex items-center gap-3 mb-4">
          <Shield className="w-8 h-8 text-ve-red" />
          <div>
            <h1 className="font-display text-2xl font-semibold text-ve-text">
              Plataforma Abierta Anticorrupción
            </h1>
            <p className="text-ve-muted text-sm">
              Transparencia de contratación y gasto público — Venezuela
            </p>
          </div>
        </div>
        
        {/* Banner disclaimer */}
        <div className="bg-ve-yellow/10 border border-ve-yellow/30 rounded-lg p-3 flex items-start gap-3">
          <TrendingUp className="w-4 h-4 text-ve-yellow mt-0.5 flex-shrink-0" />
          <p className="text-xs text-ve-yellow/80 font-display">
            PROTOTIPO DE DEMOSTRACIÓN — Datos ficticios para propósitos de desarrollo.
            Las alertas de riesgo son señales para revisión humana, no conclusiones.
            <span className="font-semibold"> Human-in-the-loop obligatorio.</span>
          </p>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-10">
        {statCards.map(({ label, value, total, icon: Icon, color, bg, href }) => (
          <Link
            key={label}
            href={href}
            className="bg-ve-slate border border-ve-border rounded-xl p-5 hover:border-ve-muted transition-colors group"
          >
            <div className={`inline-flex p-2 rounded-lg ${bg} mb-3`}>
              <Icon className={`w-5 h-5 ${color}`} />
            </div>
            <div className="font-display text-3xl font-semibold text-ve-text group-hover:text-white transition-colors">
              {value}
            </div>
            <div className="text-xs text-ve-muted mt-1">{label}</div>
            <div className="text-xs text-ve-muted/60">{total}</div>
          </Link>
        ))}
      </div>

      {/* Main Content Grid */}
      <div className="grid lg:grid-cols-2 gap-6">
        
        {/* Alertas recientes */}
        <div className="bg-ve-slate border border-ve-border rounded-xl p-6">
          <div className="flex items-center justify-between mb-5">
            <h2 className="font-display text-sm font-semibold text-ve-text flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 text-orange-400" />
              Alertas de Riesgo Prioritarias
            </h2>
            <Link href="/risk" className="text-xs text-ve-blue hover:text-ve-yellow flex items-center gap-1 transition-colors">
              Ver todas <ArrowRight className="w-3 h-3" />
            </Link>
          </div>

          <div className="space-y-3">
            {recentAlerts.length === 0 ? (
              <p className="text-ve-muted text-sm text-center py-4">No hay alertas abiertas</p>
            ) : (
              recentAlerts.map((alert) => (
                <div key={alert.id} className="border border-ve-border/50 rounded-lg p-3 hover:border-ve-muted transition-colors">
                  <div className="flex items-start justify-between gap-2 mb-2">
                    <SeverityBadge severity={alert.severity as AlertSeverity} />
                    <span className="font-display text-xs text-ve-muted">
                      Score: {(alert.score * 100).toFixed(0)}%
                    </span>
                  </div>
                  <p className="text-xs text-ve-text mb-1 line-clamp-2">
                    {alert.explanation[0]}
                  </p>
                  {alert.explanation[1] && (
                    <p className="text-xs text-ve-muted line-clamp-1">
                      {alert.explanation[1]}
                    </p>
                  )}
                </div>
              ))
            )}
          </div>
        </div>

        {/* Contratos recientes */}
        <div className="bg-ve-slate border border-ve-border rounded-xl p-6">
          <div className="flex items-center justify-between mb-5">
            <h2 className="font-display text-sm font-semibold text-ve-text flex items-center gap-2">
              <FileText className="w-4 h-4 text-blue-400" />
              Contratos Recientes
            </h2>
            <Link href="/contracts" className="text-xs text-ve-blue hover:text-ve-yellow flex items-center gap-1 transition-colors">
              Ver todos <ArrowRight className="w-3 h-3" />
            </Link>
          </div>

          <div className="space-y-3">
            {recentContracts.map((contract) => (
              <Link
                key={contract.id}
                href={`/contracts/${contract.id}`}
                className="block border border-ve-border/50 rounded-lg p-3 hover:border-ve-muted transition-colors"
              >
                <div className="flex items-start justify-between gap-2 mb-1">
                  <StatusBadge status={contract.status as ContractStatus} />
                  <span className="font-display text-xs text-ve-yellow font-semibold">
                    {formatCurrency(contract.amount, contract.currency)}
                  </span>
                </div>
                <p className="text-xs text-ve-text line-clamp-1 mb-1">{contract.title}</p>
                <p className="text-xs text-ve-muted">{contract.buyer_name}</p>
                {contract.has_amendments && (
                  <span className="inline-block mt-1 text-xs text-orange-400 font-display">
                    ⚠ {contract.amendments_count} adenda(s)
                  </span>
                )}
              </Link>
            ))}
          </div>
        </div>
      </div>

      {/* API CTA */}
      <div className="mt-6 bg-ve-blue/10 border border-ve-blue/30 rounded-xl p-5 flex items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <Database className="w-5 h-5 text-ve-blue flex-shrink-0" />
          <div>
            <p className="font-display text-sm font-semibold text-ve-text">API Pública Disponible</p>
            <p className="text-xs text-ve-muted">OCDS compatible • Paginación estándar • CSV y JSON</p>
          </div>
        </div>
        <a
          href={`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/docs`}
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center gap-2 px-4 py-2 bg-ve-blue/20 hover:bg-ve-blue/30 border border-ve-blue/40 rounded-lg text-xs font-display text-ve-blue hover:text-white transition-all whitespace-nowrap"
        >
          Explorar API <ArrowRight className="w-3 h-3" />
        </a>
      </div>
    </div>
  );
}
```

### `frontend/app/contracts/page.tsx`

```tsx
import Link from "next/link";
import { getContracts } from "@/lib/api";
import { formatCurrency, formatDate, getProcurementMethodLabel } from "@/lib/utils";
import { StatusBadge } from "@/components/contracts/StatusBadge";
import type { ContractStatus } from "@/lib/types";
import { FileText, Download, AlertCircle } from "lucide-react";

export default async function ContractsPage({
  searchParams,
}: {
  searchParams: { page?: string; status?: string; query?: string; has_amendments?: string };
}) {
  const page = parseInt(searchParams.page || "1");
  const { data: contracts, meta } = await getContracts({
    page,
    page_size: 20,
    status: searchParams.status,
    query: searchParams.query,
    has_amendments: searchParams.has_amendments === "true" ? true : undefined,
    sort: "signed_at",
    order: "desc",
  });

  const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="font-display text-xl font-semibold text-ve-text flex items-center gap-2">
            <FileText className="w-5 h-5 text-blue-400" />
            Contratos Públicos
          </h1>
          <p className="text-ve-muted text-sm mt-1">
            {meta.total_results.toLocaleString()} contratos registrados
          </p>
        </div>
        <a
          href={`${API_URL}/api/v1/download/contracts.csv`}
          className="flex items-center gap-2 px-3 py-2 bg-ve-slate border border-ve-border rounded-lg text-xs text-ve-muted hover:text-ve-text hover:border-ve-muted transition-all font-display"
        >
          <Download className="w-4 h-4" />
          Descargar CSV
        </a>
      </div>

      {/* Filtros rápidos */}
      <div className="flex flex-wrap gap-2 mb-6">
        {[
          { label: "Todos", status: undefined },
          { label: "Activos", status: "active" },
          { label: "Completados", status: "completed" },
          { label: "Con adendas", status: undefined, amendments: "true" },
        ].map(({ label, status, amendments }) => {
          const params = new URLSearchParams();
          if (status) params.set("status", status);
          if (amendments) params.set("has_amendments", amendments);
          const isActive = (status === searchParams.status) || 
                           (amendments && searchParams.has_amendments === amendments);
          return (
            <Link
              key={label}
              href={`/contracts?${params.toString()}`}
              className={`px-3 py-1.5 rounded-full text-xs font-display border transition-all ${
                isActive
                  ? "bg-ve-blue/20 border-ve-blue text-ve-blue"
                  : "bg-ve-slate border-ve-border text-ve-muted hover:border-ve-muted"
              }`}
            >
              {label}
            </Link>
          );
        })}
      </div>

      {/* Tabla */}
      <div className="bg-ve-slate border border-ve-border rounded-xl overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-ve-border bg-ve-dark/50">
                <th className="text-left py-3 px-4 text-xs font-display font-medium text-ve-muted">Contrato</th>
                <th className="text-left py-3 px-4 text-xs font-display font-medium text-ve-muted hidden md:table-cell">Comprador</th>
                <th className="text-left py-3 px-4 text-xs font-display font-medium text-ve-muted hidden lg:table-cell">Proveedor</th>
                <th className="text-right py-3 px-4 text-xs font-display font-medium text-ve-muted">Monto</th>
                <th className="text-center py-3 px-4 text-xs font-display font-medium text-ve-muted hidden sm:table-cell">Estado</th>
                <th className="text-right py-3 px-4 text-xs font-display font-medium text-ve-muted hidden lg:table-cell">Firma</th>
              </tr>
            </thead>
            <tbody>
              {contracts.map((contract, idx) => (
                <tr
                  key={contract.id}
                  className={`border-b border-ve-border/50 hover:bg-ve-dark/30 transition-colors ${
                    idx % 2 === 0 ? "" : "bg-ve-dark/10"
                  }`}
                >
                  <td className="py-3 px-4">
                    <Link href={`/contracts/${contract.id}`} className="group">
                      <div className="font-display text-xs text-ve-muted group-hover:text-ve-blue transition-colors">
                        {contract.contract_number}
                      </div>
                      <div className="text-sm text-ve-text group-hover:text-white transition-colors line-clamp-1 mt-0.5">
                        {contract.title}
                      </div>
                      {contract.has_amendments && (
                        <span className="inline-flex items-center gap-1 text-xs text-orange-400 mt-0.5">
                          <AlertCircle className="w-3 h-3" />
                          {contract.amendments_count} adenda(s)
                        </span>
                      )}
                    </Link>
                  </td>
                  <td className="py-3 px-4 hidden md:table-cell">
                    <p className="text-xs text-ve-muted line-clamp-1">{contract.buyer_name}</p>
                  </td>
                  <td className="py-3 px-4 hidden lg:table-cell">
                    <p className="text-xs text-ve-muted line-clamp-1">{contract.supplier_name}</p>
                  </td>
                  <td className="py-3 px-4 text-right">
                    <span className="font-display text-xs font-semibold text-ve-yellow">
                      {formatCurrency(contract.amount, contract.currency)}
                    </span>
                  </td>
                  <td className="py-3 px-4 text-center hidden sm:table-cell">
                    <StatusBadge status={contract.status as ContractStatus} />
                  </td>
                  <td className="py-3 px-4 text-right hidden lg:table-cell">
                    <span className="text-xs text-ve-muted font-display">
                      {formatDate(contract.signed_at)}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Paginación */}
        {meta.total_pages > 1 && (
          <div className="border-t border-ve-border px-4 py-3 flex items-center justify-between">
            <p className="text-xs text-ve-muted font-display">
              Página {meta.page} de {meta.total_pages} ({meta.total_results} resultados)
            </p>
            <div className="flex gap-2">
              {page > 1 && (
                <Link
                  href={`/contracts?page=${page - 1}`}
                  className="px-3 py-1.5 text-xs font-display bg-ve-dark border border-ve-border rounded-lg text-ve-muted hover:text-ve-text transition-colors"
                >
                  ← Anterior
                </Link>
              )}
              {page < meta.total_pages && (
                <Link
                  href={`/contracts?page=${page + 1}`}
                  className="px-3 py-1.5 text-xs font-display bg-ve-dark border border-ve-border rounded-lg text-ve-muted hover:text-ve-text transition-colors"
                >
                  Siguiente →
                </Link>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
```

### `frontend/app/risk/page.tsx`

```tsx
import { getRiskAlerts } from "@/lib/api";
import { formatDate, getAlertTypeLabel } from "@/lib/utils";
import { SeverityBadge } from "@/components/risk/SeverityBadge";
import type { AlertSeverity, AlertStatus } from "@/lib/types";
import { AlertTriangle, Info } from "lucide-react";
import Link from "next/link";

export default async function RiskPage({
  searchParams,
}: {
  searchParams: { severity?: string; status?: string; page?: string };
}) {
  const page = parseInt(searchParams.page || "1");
  const { data: alerts, meta } = await getRiskAlerts({
    page,
    page_size: 20,
    severity: searchParams.severity,
    status: searchParams.status || "open",
    sort: "score",
    order: "desc",
  });

  const statusFilter = searchParams.status || "open";

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-6">
        <h1 className="font-display text-xl font-semibold text-ve-text flex items-center gap-2">
          <AlertTriangle className="w-5 h-5 text-orange-400" />
          Panel de Alertas de Riesgo
        </h1>
        <p className="text-ve-muted text-sm mt-1">
          {meta.total_results} alerta(s) — Motor de banderas rojas OCDS
        </p>
      </div>

      {/* Aviso human-in-the-loop */}
      <div className="bg-ve-slate border border-ve-border rounded-xl p-4 mb-6 flex items-start gap-3">
        <Info className="w-4 h-4 text-blue-400 flex-shrink-0 mt-0.5" />
        <p className="text-xs text-ve-muted">
          <span className="text-ve-text font-semibold">Human-in-the-loop:</span> Las alertas son señales
          para priorización y revisión por auditores, no prueba concluyente de irregularidad.
          Cada alerta debe ser revisada y validada por un analista antes de generar consecuencias.
        </p>
      </div>

      {/* Filtros */}
      <div className="flex flex-wrap gap-2 mb-6">
        {[
          { label: "Abiertas", status: "open" },
          { label: "Revisadas", status: "reviewed" },
          { label: "Desestimadas", status: "dismissed" },
        ].map(({ label, status }) => (
          <Link
            key={label}
            href={`/risk?status=${status}`}
            className={`px-3 py-1.5 rounded-full text-xs font-display border transition-all ${
              statusFilter === status
                ? "bg-ve-blue/20 border-ve-blue text-ve-blue"
                : "bg-ve-slate border-ve-border text-ve-muted hover:border-ve-muted"
            }`}
          >
            {label}
          </Link>
        ))}
        <span className="text-ve-border">|</span>
        {(["critical", "high", "medium", "low"] as AlertSeverity[]).map((sev) => (
          <Link
            key={sev}
            href={`/risk?severity=${sev}&status=${statusFilter}`}
            className={`px-3 py-1.5 rounded-full text-xs font-display border transition-all ${
              searchParams.severity === sev
                ? "bg-ve-blue/20 border-ve-blue text-ve-blue"
                : "bg-ve-slate border-ve-border text-ve-muted hover:border-ve-muted"
            }`}
          >
            <SeverityBadge severity={sev} className="text-xs" />
          </Link>
        ))}
      </div>

      {/* Alertas */}
      <div className="space-y-4">
        {alerts.length === 0 ? (
          <div className="text-center py-16 text-ve-muted">
            <AlertTriangle className="w-12 h-12 mx-auto mb-4 opacity-30" />
            <p className="font-display text-sm">No hay alertas con los filtros seleccionados</p>
          </div>
        ) : (
          alerts.map((alert) => (
            <div
              key={alert.id}
              className="bg-ve-slate border border-ve-border rounded-xl p-5 hover:border-ve-muted transition-colors"
            >
              <div className="flex items-start justify-between gap-4 mb-3">
                <div className="flex items-center gap-2 flex-wrap">
                  <SeverityBadge severity={alert.severity as AlertSeverity} />
                  <span className="font-display text-xs text-ve-muted px-2 py-0.5 bg-ve-dark rounded border border-ve-border">
                    {getAlertTypeLabel(alert.type as any)}
                  </span>
                  {alert.status !== "open" && (
                    <span className={`font-display text-xs px-2 py-0.5 rounded border ${
                      alert.status === "reviewed"
                        ? "text-blue-400 border-blue-400/30 bg-blue-400/10"
                        : "text-ve-muted border-ve-border bg-ve-dark"
                    }`}>
                      {alert.status === "reviewed" ? "Revisada" : "Desestimada"}
                    </span>
                  )}
                </div>
                <div className="text-right flex-shrink-0">
                  <div className="font-display text-lg font-semibold text-ve-text">
                    {(alert.score * 100).toFixed(0)}%
                  </div>
                  <div className="text-xs text-ve-muted">score</div>
                </div>
              </div>

              {/* Explicaciones */}
              <ul className="space-y-1 mb-3">
                {alert.explanation.map((exp, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm text-ve-text">
                    <span className="text-ve-red mt-1 flex-shrink-0">▸</span>
                    {exp}
                  </li>
                ))}
              </ul>

              {/* Datos de soporte */}
              {Object.keys(alert.supporting_data).length > 0 && (
                <div className="bg-ve-dark/50 rounded-lg p-3 font-display text-xs text-ve-muted border border-ve-border/50">
                  {Object.entries(alert.supporting_data).map(([k, v]) => (
                    <span key={k} className="mr-4">
                      <span className="text-ve-muted/60">{k}:</span>{" "}
                      <span className="text-ve-text">{String(v)}</span>
                    </span>
                  ))}
                </div>
              )}

              <div className="flex items-center justify-between mt-3 pt-3 border-t border-ve-border/50">
                <span className="font-display text-xs text-ve-muted">
                  Generada: {formatDate(alert.generated_at)}
                </span>
                <span className="font-display text-xs text-ve-muted/60">
                  ID: {alert.id.slice(0, 8)}...
                </span>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Paginación */}
      {meta.total_pages > 1 && (
        <div className="mt-6 flex items-center justify-between">
          <p className="text-xs text-ve-muted font-display">
            Página {meta.page} de {meta.total_pages}
          </p>
          <div className="flex gap-2">
            {page > 1 && (
              <Link href={`/risk?page=${page - 1}&status=${statusFilter}`}
                className="px-3 py-1.5 text-xs font-display bg-ve-dark border border-ve-border rounded-lg text-ve-muted hover:text-ve-text">
                ← Anterior
              </Link>
            )}
            {page < meta.total_pages && (
              <Link href={`/risk?page=${page + 1}&status=${statusFilter}`}
                className="px-3 py-1.5 text-xs font-display bg-ve-dark border border-ve-border rounded-lg text-ve-muted hover:text-ve-text">
                Siguiente →
              </Link>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
```

### `frontend/app/suppliers/page.tsx`

```tsx
import { getSuppliers } from "@/lib/api";
import { formatCurrency, getSanctionColor } from "@/lib/utils";
import { cn } from "@/lib/utils";
import type { SanctionStatus } from "@/lib/types";
import { Users, AlertCircle } from "lucide-react";
import Link from "next/link";

export default async function SuppliersPage({
  searchParams,
}: {
  searchParams: { page?: string; sanction_status?: string; query?: string };
}) {
  const page = parseInt(searchParams.page || "1");
  const { data: suppliers, meta } = await getSuppliers({
    page,
    page_size: 20,
    sanction_status: searchParams.sanction_status,
    query: searchParams.query,
    sort: "total_awarded_12m",
    order: "desc",
  });

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-6">
        <h1 className="font-display text-xl font-semibold text-ve-text flex items-center gap-2">
          <Users className="w-5 h-5 text-green-400" />
          Registro de Proveedores
        </h1>
        <p className="text-ve-muted text-sm mt-1">
          {meta.total_results} proveedores registrados — ordenados por monto adjudicado
        </p>
      </div>

      {/* Filtros */}
      <div className="flex flex-wrap gap-2 mb-6">
        {[
          { label: "Todos", status: undefined },
          { label: "Activos", status: "active" },
          { label: "Sancionados", status: "sanctioned" },
          { label: "Suspendidos", status: "suspended" },
        ].map(({ label, status }) => {
          const isActive = searchParams.sanction_status === status ||
                           (!searchParams.sanction_status && !status);
          const params = status ? `?sanction_status=${status}` : "";
          return (
            <Link
              key={label}
              href={`/suppliers${params}`}
              className={`px-3 py-1.5 rounded-full text-xs font-display border transition-all ${
                isActive
                  ? "bg-ve-blue/20 border-ve-blue text-ve-blue"
                  : "bg-ve-slate border-ve-border text-ve-muted hover:border-ve-muted"
              }`}
            >
              {label}
            </Link>
          );
        })}
      </div>

      {/* Grid de proveedores */}
      <div className="grid md:grid-cols-2 gap-4">
        {suppliers.map((supplier) => (
          <div
            key={supplier.id}
            className="bg-ve-slate border border-ve-border rounded-xl p-5 hover:border-ve-muted transition-colors"
          >
            <div className="flex items-start justify-between gap-3 mb-3">
              <div className="flex-1 min-w-0">
                <p className="font-semibold text-ve-text text-sm line-clamp-2 mb-1">
                  {supplier.name}
                </p>
                <p className="font-display text-xs text-ve-muted">{supplier.rif}</p>
              </div>
              <span className={cn(
                "inline-flex px-2 py-0.5 rounded text-xs font-display font-medium border flex-shrink-0",
                getSanctionColor(supplier.sanction_status as SanctionStatus)
              )}>
                {supplier.sanction_status === "active" ? "Activo" :
                 supplier.sanction_status === "sanctioned" ? "SANCIONADO" : "Suspendido"}
              </span>
            </div>

            {supplier.sanction_status !== "active" && (
              <div className="flex items-center gap-2 text-xs text-red-400 bg-red-400/10 rounded-lg px-3 py-2 mb-3 border border-red-400/20">
                <AlertCircle className="w-3 h-3 flex-shrink-0" />
                Proveedor inhabilitado — verificar contratos activos
              </div>
            )}

            <div className="grid grid-cols-2 gap-3 text-center">
              <div className="bg-ve-dark/50 rounded-lg p-2 border border-ve-border/50">
                <p className="font-display text-lg font-semibold text-ve-yellow">
                  {formatCurrency(supplier.total_awarded_12m)}
                </p>
                <p className="text-xs text-ve-muted">Adjudicado 12m</p>
              </div>
              <div className="bg-ve-dark/50 rounded-lg p-2 border border-ve-border/50">
                <p className="font-display text-lg font-semibold text-ve-text">
                  {supplier.awards_count_12m}
                </p>
                <p className="text-xs text-ve-muted">Contratos 12m</p>
              </div>
            </div>

            {supplier.sector && (
              <p className="text-xs text-ve-muted mt-3 truncate">
                Sector: {supplier.sector}
              </p>
            )}
            {supplier.state && (
              <p className="text-xs text-ve-muted/60">{supplier.state}</p>
            )}
          </div>
        ))}
      </div>

      {/* Paginación */}
      {meta.total_pages > 1 && (
        <div className="mt-6 flex items-center justify-between">
          <p className="text-xs text-ve-muted font-display">
            Página {meta.page} de {meta.total_pages}
          </p>
          <div className="flex gap-2">
            {page > 1 && (
              <Link href={`/suppliers?page=${page - 1}`}
                className="px-3 py-1.5 text-xs font-display bg-ve-dark border border-ve-border rounded-lg text-ve-muted hover:text-ve-text">
                ← Anterior
              </Link>
            )}
            {page < meta.total_pages && (
              <Link href={`/suppliers?page=${page + 1}`}
                className="px-3 py-1.5 text-xs font-display bg-ve-dark border border-ve-border rounded-lg text-ve-muted hover:text-ve-text">
                Siguiente →
              </Link>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
```

---

## 6. Orden de ejecución para Codex

Ejecuta exactamente en este orden:

```
PASO 1: Crear la estructura de carpetas del monorepo
PASO 2: Crear todos los archivos raíz (README.md, .gitignore, docker-compose.yml)
PASO 3: Crear backend/requirements.txt y backend/.env.example
PASO 4: Crear app/core/config.py y app/core/database.py
PASO 5: Crear todos los modelos SQLAlchemy (models/)
PASO 6: Crear todos los schemas Pydantic (schemas/)
PASO 7: Crear todos los endpoints FastAPI (api/v1/)
PASO 8: Crear el risk_engine.py (services/)
PASO 9: Crear app/main.py
PASO 10: Crear backend/Dockerfile
PASO 11: Crear frontend/package.json y configuración base (tailwind, next.config, tsconfig)
PASO 12: Crear frontend/lib/ (types.ts, api.ts, utils.ts)
PASO 13: Crear frontend/components/ (todos los componentes)
PASO 14: Crear frontend/app/ (layout, pages)
PASO 15: Crear supabase/migrations/001_initial_schema.sql
PASO 16: Crear supabase/seed.sql
```

---

## 7. Variables de entorno mínimas para arrancar

Para obtener las credenciales de Supabase:
1. Crear proyecto en https://supabase.com
2. Ir a **Settings → API**
3. Copiar **Project URL** → `SUPABASE_URL`
4. Copiar **anon public** → `SUPABASE_KEY`
5. Ir a **Settings → Database** → copiar **Connection string** → `DATABASE_URL`

```env
# backend/.env
DATABASE_URL=postgresql://postgres:[TU-PASSWORD]@db.[TU-REF].supabase.co:5432/postgres
SUPABASE_URL=https://[TU-REF].supabase.co
SUPABASE_KEY=[TU-ANON-KEY]
CORS_ORIGINS=["http://localhost:3000"]

# frontend/.env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 8. Verificación final

Después de implementar todo, verificar:

```bash
# Backend
cd backend && pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
# Verificar: http://localhost:8000/docs

# Frontend  
cd frontend && npm install && npm run dev
# Verificar: http://localhost:3000

# Endpoints críticos a probar:
curl http://localhost:8000/api/v1/contracts?page_size=3
curl http://localhost:8000/api/v1/risk/alerts?status=open
curl http://localhost:8000/api/v1/suppliers
curl http://localhost:8000/api/v1/download/contracts.csv
curl http://localhost:8000/api/v1/download/ocds/releases.json
```

---

*Plan generado para el proyecto: Plataforma Abierta Anticorrupción Venezuela*
*Autor: Jesús Alexander León Cordero — Tech Lead | MSc. Ciencias de la Computación*
*Fecha: 14 de marzo de 2026 | Licencia: MIT*
