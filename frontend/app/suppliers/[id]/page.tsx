import { notFound } from "next/navigation";
import { getSupplier } from "@/lib/api";
import { ApiError } from "@/lib/api";
import { formatCurrency, formatDate, getSanctionColor } from "@/lib/utils";
import { cn } from "@/lib/utils";
import type { SanctionStatus } from "@/lib/types";
import { Users, AlertCircle, ArrowLeft } from "lucide-react";
import Link from "next/link";

export default async function SupplierDetailPage({
  params,
}: {
  params: { id: string };
}) {
  let supplier;
  try {
    supplier = await getSupplier(params.id);
  } catch (err) {
    if (err instanceof ApiError && err.status === 404) notFound();
    throw err;
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <Link
        href="/suppliers"
        className="flex items-center gap-2 text-ve-muted hover:text-ve-text text-sm mb-6 transition-colors"
      >
        <ArrowLeft className="w-4 h-4" />
        Volver a proveedores
      </Link>

      <div className="bg-ve-slate border border-ve-border rounded-xl p-6">
        <div className="flex items-start justify-between gap-4 mb-4">
          <div>
            <p className="font-display text-xs text-ve-muted mb-1">{supplier.rif}</p>
            <h1 className="text-xl font-semibold text-ve-text">{supplier.name}</h1>
            {supplier.legal_name && supplier.legal_name !== supplier.name && (
              <p className="text-sm text-ve-muted mt-1">{supplier.legal_name}</p>
            )}
          </div>
          <span
            className={cn(
              "inline-flex px-2 py-0.5 rounded text-xs font-display font-medium border flex-shrink-0",
              getSanctionColor(supplier.sanction_status as SanctionStatus)
            )}
          >
            {supplier.sanction_status === "active"
              ? "Activo"
              : supplier.sanction_status === "sanctioned"
              ? "SANCIONADO"
              : "Suspendido"}
          </span>
        </div>

        {supplier.sanction_status !== "active" && (
          <div className="flex items-center gap-3 bg-red-400/10 border border-red-400/30 rounded-lg p-4 mb-6">
            <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0" />
            <p className="text-sm text-red-400">
              Proveedor inhabilitado — verificar contratos activos en el sistema
            </p>
          </div>
        )}

        <div className="grid sm:grid-cols-2 gap-4 mb-6">
          <div className="bg-ve-dark/50 rounded-lg p-4 border border-ve-border/50 text-center">
            <p className="font-display text-2xl font-semibold text-ve-yellow">
              {formatCurrency(supplier.total_awarded_12m)}
            </p>
            <p className="text-xs text-ve-muted mt-1">Adjudicado últimos 12 meses</p>
          </div>
          <div className="bg-ve-dark/50 rounded-lg p-4 border border-ve-border/50 text-center">
            <p className="font-display text-2xl font-semibold text-ve-text">
              {supplier.awards_count_12m}
            </p>
            <p className="text-xs text-ve-muted mt-1">Contratos últimos 12 meses</p>
          </div>
        </div>

        <div className="grid sm:grid-cols-2 gap-6">
          <div>
            <h2 className="font-display text-xs font-semibold text-ve-muted uppercase tracking-wider mb-3">
              Información
            </h2>
            <div className="space-y-2">
              {supplier.sector && (
                <div>
                  <p className="text-xs text-ve-muted">Sector</p>
                  <p className="text-sm text-ve-text">{supplier.sector}</p>
                </div>
              )}
              {supplier.state && (
                <div>
                  <p className="text-xs text-ve-muted">Estado</p>
                  <p className="text-sm text-ve-text">{supplier.state}</p>
                </div>
              )}
              <div>
                <p className="text-xs text-ve-muted">Tipo</p>
                <p className="text-sm text-ve-text capitalize">{supplier.type}</p>
              </div>
            </div>
          </div>
          <div>
            <h2 className="font-display text-xs font-semibold text-ve-muted uppercase tracking-wider mb-3">
              Registro
            </h2>
            <div className="space-y-2">
              <div>
                <p className="text-xs text-ve-muted">Creado</p>
                <p className="text-sm text-ve-text">{formatDate(supplier.created_at)}</p>
              </div>
              <div>
                <p className="text-xs text-ve-muted">Actualizado</p>
                <p className="text-sm text-ve-text">{formatDate(supplier.updated_at)}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
