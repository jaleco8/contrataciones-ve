-- ============================================================
-- PLATAFORMA ABIERTA ANTICORRUPCIÓN VENEZUELA
-- Schema inicial v1.0 — Compatible con OCDS
-- ============================================================

-- Extensiones
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE SCHEMA IF NOT EXISTS extensions;
CREATE EXTENSION IF NOT EXISTS "pg_trgm" WITH SCHEMA extensions;  -- Para búsqueda de texto

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
CREATE INDEX idx_suppliers_name_trgm ON suppliers USING GIN (name extensions.gin_trgm_ops);
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
CREATE INDEX idx_processes_title_trgm ON processes USING GIN (title extensions.gin_trgm_ops);

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
CREATE INDEX idx_contracts_title_trgm ON contracts USING GIN (title extensions.gin_trgm_ops);

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
RETURNS TRIGGER
LANGUAGE plpgsql
SET search_path = pg_catalog
AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$;

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
-- SEGURIDAD: habilitar RLS en tablas públicas y políticas mínimas
-- ============================================================

ALTER TABLE suppliers ENABLE ROW LEVEL SECURITY;
ALTER TABLE processes ENABLE ROW LEVEL SECURITY;
ALTER TABLE contracts ENABLE ROW LEVEL SECURITY;
ALTER TABLE contract_amendments ENABLE ROW LEVEL SECURITY;
ALTER TABLE contract_payments ENABLE ROW LEVEL SECURITY;
ALTER TABLE risk_alerts ENABLE ROW LEVEL SECURITY;

-- Lectura pública (anon/authenticated) para datos de transparencia.
-- Escrituras se mantienen restringidas por ausencia de políticas DML.
DROP POLICY IF EXISTS suppliers_public_read ON suppliers;
CREATE POLICY suppliers_public_read
    ON suppliers
    FOR SELECT
    TO anon, authenticated
    USING (TRUE);

DROP POLICY IF EXISTS processes_public_read ON processes;
CREATE POLICY processes_public_read
    ON processes
    FOR SELECT
    TO anon, authenticated
    USING (TRUE);

DROP POLICY IF EXISTS contracts_public_read ON contracts;
CREATE POLICY contracts_public_read
    ON contracts
    FOR SELECT
    TO anon, authenticated
    USING (TRUE);

DROP POLICY IF EXISTS contract_amendments_public_read ON contract_amendments;
CREATE POLICY contract_amendments_public_read
    ON contract_amendments
    FOR SELECT
    TO anon, authenticated
    USING (TRUE);

DROP POLICY IF EXISTS contract_payments_public_read ON contract_payments;
CREATE POLICY contract_payments_public_read
    ON contract_payments
    FOR SELECT
    TO anon, authenticated
    USING (TRUE);

DROP POLICY IF EXISTS risk_alerts_public_read ON risk_alerts;
CREATE POLICY risk_alerts_public_read
    ON risk_alerts
    FOR SELECT
    TO anon, authenticated
    USING (TRUE);

-- ============================================================
-- VISTAS útiles para el dashboard
-- ============================================================

-- Vista: resumen de contratos por comprador
CREATE OR REPLACE VIEW v_buyer_summary
WITH (security_invoker = true) AS
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
CREATE OR REPLACE VIEW v_supplier_concentration
WITH (security_invoker = true) AS
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
CREATE OR REPLACE VIEW v_dashboard_stats
WITH (security_invoker = true) AS
SELECT
    (SELECT COUNT(*) FROM contracts WHERE status = 'active') as active_contracts,
    (SELECT COUNT(*) FROM contracts) as total_contracts,
    (SELECT COALESCE(SUM(amount), 0) FROM contracts WHERE status != 'cancelled') as total_value_usd,
    (SELECT COUNT(*) FROM suppliers WHERE sanction_status = 'active') as active_suppliers,
    (SELECT COUNT(*) FROM risk_alerts WHERE status = 'open') as open_alerts,
    (SELECT COUNT(*) FROM risk_alerts WHERE severity IN ('high', 'critical') AND status = 'open') as critical_alerts,
    (SELECT COUNT(*) FROM processes WHERE status = 'tender') as active_tenders,
    (SELECT COUNT(*) FROM contracts WHERE has_amendments = TRUE) as amended_contracts;
