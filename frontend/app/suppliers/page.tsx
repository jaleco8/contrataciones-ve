export const dynamic = "force-dynamic";

import { getSuppliers } from "@/lib/api";
import { formatCurrency, getSanctionColor } from "@/lib/utils";
import { cn } from "@/lib/utils";
import type { SanctionStatus } from "@/lib/types";
import { Users, AlertCircle } from "lucide-react";
import Link from "next/link";

function buildPageHref(
  base: string,
  current: Record<string, string | undefined>,
  newPage: number
): string {
  const params = new URLSearchParams(
    Object.fromEntries(
      Object.entries(current).filter(([, v]) => v !== undefined)
    ) as Record<string, string>
  );
  params.set("page", String(newPage));
  return `${base}?${params.toString()}`;
}

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
              <Link
                href={buildPageHref("/suppliers", searchParams, page - 1)}
                className="px-3 py-1.5 text-xs font-display bg-ve-dark border border-ve-border rounded-lg text-ve-muted hover:text-ve-text"
              >
                Anterior
              </Link>
            )}
            {page < meta.total_pages && (
              <Link
                href={buildPageHref("/suppliers", searchParams, page + 1)}
                className="px-3 py-1.5 text-xs font-display bg-ve-dark border border-ve-border rounded-lg text-ve-muted hover:text-ve-text"
              >
                Siguiente
              </Link>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
