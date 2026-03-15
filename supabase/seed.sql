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
