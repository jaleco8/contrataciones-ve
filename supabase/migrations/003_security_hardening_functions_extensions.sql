-- ============================================================
-- MIGRACIÓN 003: HARDENING DE FUNCIÓN Y EXTENSIÓN
-- Fecha: 2026-03-24
-- Objetivo:
--   1) Eliminar search_path mutable en función trigger
--   2) Mover pg_trgm fuera de public (schema extensions)
-- ============================================================

-- 1) Función trigger con search_path fijo (evita shadowing de objetos)
CREATE OR REPLACE FUNCTION public.update_updated_at_column()
RETURNS TRIGGER
LANGUAGE plpgsql
SET search_path = pg_catalog
AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$;

-- 2) Extensión pg_trgm en schema dedicado
CREATE SCHEMA IF NOT EXISTS extensions;

DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'pg_trgm') THEN
        ALTER EXTENSION "pg_trgm" SET SCHEMA extensions;
    ELSE
        CREATE EXTENSION "pg_trgm" WITH SCHEMA extensions;
    END IF;
END
$$;
