---
name: Estado actual del frontend
description: Inventario de páginas, componentes existentes, deuda técnica conocida y hallazgos del primer análisis completo del frontend (marzo 2026) — actualizado tras batch de fixes
type: project
---

Estado al 2026-03-15 — actualizado tras batch de fixes 2.x/3.x.

**Why:** Sirve como baseline para priorizar trabajo futuro y no repetir trabajo ya hecho.

**How to apply:** Usar como referencia antes de sugerir refactorizaciones o nuevas features. Actualizar cuando se resuelvan los problemas listados.

## Páginas implementadas
- `/` — Dashboard (Server Component, Promise.allSettled con 8 fetch paralelos)
- `/contracts` — Listado con filtros rápidos y tabla (Server Component)
- `/contracts/[id]` — Detalle con notFound() y manejo de ApiError
- `/suppliers` — Grid con filtros (Server Component)
- `/suppliers/[id]` — Detalle con notFound() y manejo de ApiError
- `/risk` — Panel de alertas con filtros (Server Component)
- `/api/health` — Route handler simple

## Componentes existentes
- `components/layout/Navbar` (Server Component, usa NavLink)
- `components/layout/NavLink` (Client Component, activo via usePathname)
- `components/layout/Footer`
- `components/contracts/ContractCard`, `ContractTable`, `StatusBadge`
- `components/dashboard/StatCard`, `RiskChart` (stub vacío), `RecentContracts`
- `components/risk/AlertCard`, `SeverityBadge`
- `components/suppliers/SupplierCard`

## Archivos de infraestructura de routing
- `app/loading.tsx` — skeleton del dashboard
- `app/error.tsx` — error boundary global (Client Component)
- `app/contracts/loading.tsx`
- `app/contracts/[id]/not-found.tsx`
- `app/suppliers/loading.tsx`
- `app/suppliers/[id]/not-found.tsx`
- `app/risk/loading.tsx`

## Decisiones de arquitectura (batch fixes 2026-03-15)
- **fetch nativo** reemplaza axios. `apiFetch` en `lib/api.ts` usa `next: { revalidate: 60 }`.
- **`ApiError`** clase exportada desde `lib/api.ts` — usar con `instanceof` en Server Components para `notFound()`.
- **`API_URL`** (sin prefijo NEXT_PUBLIC_) para Server Components. `NEXT_PUBLIC_API_URL` solo para links de cliente en Navbar.
- **`buildPageHref`** helper local en cada list page para preservar filtros en paginación.
- **next/font** — `IBM_Plex_Mono` + `IBM_Plex_Sans` con variables CSS `--font-mono` / `--font-sans`. Tailwind apunta a `var(--font-mono)` / `var(--font-sans)`.
- Skip-to-content `#main-content` en `layout.tsx` para WCAG.
- `frontend/Dockerfile` — multi-stage build, usuario non-root nextjs, healthcheck.

## Paquetes removidos
- `axios` — reemplazado por fetch nativo
- `@radix-ui/react-badge` — no existe en npm, era typo

## Problemas resueltos en el batch de fixes
1. ~~lib/api.ts usa axios~~ — reescrito con fetch nativo
2. ~~Páginas de detalle sin try/catch ni notFound()~~ — corregido
3. ~~NEXT_PUBLIC_API_URL en Server Components~~ — ahora usa API_URL (sin prefijo)
4. ~~as any en risk/page.tsx~~ — eliminado, usa `AlertType`
5. ~~Paginación no preserva filtros~~ — buildPageHref en contracts, suppliers, risk
6. ~~Sin loading.tsx ni error.tsx~~ — creados en todos los segmentos
7. ~~Navbar sin estado activo~~ — NavLink con usePathname
8. ~~Fuente via link tag~~ — migrado a next/font
9. ~~@radix-ui/react-badge typo~~ — removido del package.json

## Problemas aún pendientes (al 2026-03-15)
- Búsqueda full-text con input UI (solo queryParam sin input real)
- Toggle de moneda VES/USD
- Visualizaciones Recharts (stub vacío en RiskChart)
- Detalle de contrato: timeline, adendas detalladas, pagos, alertas asociadas, enlace a proveedor
- Detalle de proveedor: historial de contratos, alertas del proveedor
- `generateMetadata` dinámico en páginas de detalle
- `getSanctionColor` discrepancia: no incluye `border` en sus clases pero SupplierCard espera border

## Funcionalidades faltantes según spec completa
- Explorador de Entes (`/entes`)
- Red de Proveedores (`/red`) con grafo interactivo
- Tablero de Alertas avanzado con acciones de auditor
- API Pública Docs (`/api-docs`)
