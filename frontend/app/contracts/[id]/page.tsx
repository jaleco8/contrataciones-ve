import { notFound } from "next/navigation";
import { getContract } from "@/lib/api";
import { ApiError } from "@/lib/api";
import { formatCurrency, formatDate, getStatusColor } from "@/lib/utils";
import { StatusBadge } from "@/components/contracts/StatusBadge";
import type { ContractStatus } from "@/lib/types";
import { FileText, AlertCircle, ArrowLeft } from "lucide-react";
import Link from "next/link";

export default async function ContractDetailPage({
  params,
}: {
  params: { id: string };
}) {
  let contract;
  try {
    contract = await getContract(params.id);
  } catch (err) {
    if (err instanceof ApiError && err.status === 404) notFound();
    throw err;
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <Link
        href="/contracts"
        className="flex items-center gap-2 text-ve-muted hover:text-ve-text text-sm mb-6 transition-colors"
      >
        <ArrowLeft className="w-4 h-4" />
        Volver a contratos
      </Link>

      <div className="bg-ve-slate border border-ve-border rounded-xl p-6">
        <div className="flex items-start justify-between gap-4 mb-4">
          <div>
            <p className="font-display text-xs text-ve-muted mb-1">
              {contract.contract_number}
            </p>
            <h1 className="text-xl font-semibold text-ve-text">{contract.title}</h1>
          </div>
          <StatusBadge status={contract.status as ContractStatus} />
        </div>

        {contract.description && (
          <p className="text-sm text-ve-muted mb-6">{contract.description}</p>
        )}

        <div className="grid sm:grid-cols-2 gap-4 mb-6">
          <div className="bg-ve-dark/50 rounded-lg p-4 border border-ve-border/50">
            <p className="text-xs text-ve-muted mb-1">Monto del contrato</p>
            <p className="font-display text-2xl font-semibold text-ve-yellow">
              {formatCurrency(contract.amount, contract.currency)}
            </p>
            {contract.original_amount && contract.original_amount !== contract.amount && (
              <p className="text-xs text-ve-muted mt-1">
                Original: {formatCurrency(contract.original_amount, contract.currency)}
              </p>
            )}
          </div>
          <div className="bg-ve-dark/50 rounded-lg p-4 border border-ve-border/50">
            <p className="text-xs text-ve-muted mb-1">Categoría</p>
            <p className="text-sm text-ve-text capitalize">{contract.category || "—"}</p>
          </div>
        </div>

        <div className="grid sm:grid-cols-2 gap-6">
          <div>
            <h2 className="font-display text-xs font-semibold text-ve-muted uppercase tracking-wider mb-3">
              Partes
            </h2>
            <div className="space-y-2">
              <div>
                <p className="text-xs text-ve-muted">Comprador</p>
                <p className="text-sm text-ve-text">{contract.buyer_name}</p>
              </div>
              <div>
                <p className="text-xs text-ve-muted">Proveedor</p>
                <p className="text-sm text-ve-text">{contract.supplier_name}</p>
              </div>
            </div>
          </div>

          <div>
            <h2 className="font-display text-xs font-semibold text-ve-muted uppercase tracking-wider mb-3">
              Fechas
            </h2>
            <div className="space-y-2">
              <div>
                <p className="text-xs text-ve-muted">Firmado</p>
                <p className="text-sm text-ve-text">{formatDate(contract.signed_at)}</p>
              </div>
              <div>
                <p className="text-xs text-ve-muted">Vigencia</p>
                <p className="text-sm text-ve-text">
                  {formatDate(contract.start_date)} → {formatDate(contract.end_date)}
                </p>
              </div>
            </div>
          </div>
        </div>

        {contract.has_amendments && (
          <div className="mt-6 flex items-center gap-3 bg-orange-400/10 border border-orange-400/30 rounded-lg p-4">
            <AlertCircle className="w-5 h-5 text-orange-400 flex-shrink-0" />
            <div>
              <p className="text-sm font-semibold text-orange-400">
                {contract.amendments_count} adenda(s) registradas
              </p>
              <p className="text-xs text-ve-muted">
                Incremento total:{" "}
                {formatCurrency(contract.amendment_amount_increase, contract.currency)}
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
