import Link from "next/link";
import { getContracts } from "@/lib/api";
import { formatCurrency, formatDate } from "@/lib/utils";
import { StatusBadge } from "@/components/contracts/StatusBadge";
import type { ContractStatus } from "@/lib/types";
import { FileText, Download, AlertCircle } from "lucide-react";

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
                <th scope="col" className="text-left py-3 px-4 text-xs font-display font-medium text-ve-muted">Contrato</th>
                <th scope="col" className="text-left py-3 px-4 text-xs font-display font-medium text-ve-muted hidden md:table-cell">Comprador</th>
                <th scope="col" className="text-left py-3 px-4 text-xs font-display font-medium text-ve-muted hidden lg:table-cell">Proveedor</th>
                <th scope="col" className="text-right py-3 px-4 text-xs font-display font-medium text-ve-muted">Monto</th>
                <th scope="col" className="text-center py-3 px-4 text-xs font-display font-medium text-ve-muted hidden sm:table-cell">Estado</th>
                <th scope="col" className="text-right py-3 px-4 text-xs font-display font-medium text-ve-muted hidden lg:table-cell">Firma</th>
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
                  href={buildPageHref("/contracts", searchParams, page - 1)}
                  className="px-3 py-1.5 text-xs font-display bg-ve-dark border border-ve-border rounded-lg text-ve-muted hover:text-ve-text transition-colors"
                >
                  Anterior
                </Link>
              )}
              {page < meta.total_pages && (
                <Link
                  href={buildPageHref("/contracts", searchParams, page + 1)}
                  className="px-3 py-1.5 text-xs font-display bg-ve-dark border border-ve-border rounded-lg text-ve-muted hover:text-ve-text transition-colors"
                >
                  Siguiente
                </Link>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
