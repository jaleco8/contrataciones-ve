-- ============================================================
-- MIGRACIÓN 002: HARDENING DE SEGURIDAD (RLS + SECURITY INVOKER)
-- Fecha: 2026-03-24
-- Objetivo:
--   1) Corregir tablas públicas sin RLS
--   2) Corregir vistas con comportamiento SECURITY DEFINER
-- ============================================================

-- 1) Habilitar RLS en tablas expuestas por PostgREST
ALTER TABLE public.suppliers ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.processes ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.contracts ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.contract_amendments ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.contract_payments ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.risk_alerts ENABLE ROW LEVEL SECURITY;

-- 2) Políticas de lectura pública para la capa de transparencia
--    (escrituras siguen bloqueadas para anon/authenticated)
DROP POLICY IF EXISTS suppliers_public_read ON public.suppliers;
CREATE POLICY suppliers_public_read
    ON public.suppliers
    FOR SELECT
    TO anon, authenticated
    USING (TRUE);

DROP POLICY IF EXISTS processes_public_read ON public.processes;
CREATE POLICY processes_public_read
    ON public.processes
    FOR SELECT
    TO anon, authenticated
    USING (TRUE);

DROP POLICY IF EXISTS contracts_public_read ON public.contracts;
CREATE POLICY contracts_public_read
    ON public.contracts
    FOR SELECT
    TO anon, authenticated
    USING (TRUE);

DROP POLICY IF EXISTS contract_amendments_public_read ON public.contract_amendments;
CREATE POLICY contract_amendments_public_read
    ON public.contract_amendments
    FOR SELECT
    TO anon, authenticated
    USING (TRUE);

DROP POLICY IF EXISTS contract_payments_public_read ON public.contract_payments;
CREATE POLICY contract_payments_public_read
    ON public.contract_payments
    FOR SELECT
    TO anon, authenticated
    USING (TRUE);

DROP POLICY IF EXISTS risk_alerts_public_read ON public.risk_alerts;
CREATE POLICY risk_alerts_public_read
    ON public.risk_alerts
    FOR SELECT
    TO anon, authenticated
    USING (TRUE);

-- 3) Vistas en modo SECURITY INVOKER para respetar permisos del usuario
ALTER VIEW public.v_buyer_summary SET (security_invoker = true);
ALTER VIEW public.v_supplier_concentration SET (security_invoker = true);
ALTER VIEW public.v_dashboard_stats SET (security_invoker = true);
