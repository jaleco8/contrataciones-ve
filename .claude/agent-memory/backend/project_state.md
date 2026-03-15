---
name: Estado actual del backend — contrataciones-ve
description: Issues conocidos, deuda técnica y decisiones de arquitectura identificadas en la auditoría del 2026-03-15
type: project
---

Auditoría completa del backend realizada el 2026-03-15.

**Por:** análisis de código estático completo de todos los archivos en backend/.

**RESUELTOS en Fix Batch 1 (2026-03-15):**
- [x] Column injection via `sort` — whitelists ALLOWED_SORT_* en los 4 routers
- [x] Sin autenticación en PATCH /risk/alerts — ahora require_api_key (X-API-Key)
- [x] alembic/env.py target_metadata=None — reescrito con Base.metadata real
- [x] Dockerfile corre como root, sin multi-stage — ahora multi-stage + non-root user + HEALTHCHECK
- [x] download.py sin streaming real — CSV usa generador async chunked (CHUNK_SIZE=500)
- [x] SECRET_KEY con default inseguro — ahora campo sin default (falla si no está en .env)
- [x] RiskEngine.save_alerts() duplicados — ahora verifica existencia antes de insertar
- [x] get_db() doble cierre de sesión — eliminado el finally redundante
- [x] RiskAlertUpdate.status acepta cualquier string — ahora Literal["open","reviewed","dismissed"]
- [x] Path params como str en vez de uuid.UUID — corregido en los 4 routers
- [x] pytest en requirements.txt de producción — movido a requirements-dev.txt
- [x] Motor de riesgo sin endpoint — añadido POST /risk/run con auth
- [x] app/core/security.py no existía — creado

**Pendientes (no abordados aún):**
- PaginatedResponse usa List[Any] — pierde validación de tipos en runtime
- Modelos SQLAlchemy sin relaciones ORM (no usan relationship())
- No hay versiones de migración en alembic/versions/ — requiere alembic revision
- pandas en requirements no usado en código
- CORS con allow_credentials=True potencialmente peligroso si .env mal configurado

**How to apply:** Al sugerir cambios, priorizar estos issues en orden: seguridad > corrección > performance > calidad.
