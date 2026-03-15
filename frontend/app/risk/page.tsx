import { getRiskAlerts } from "@/lib/api";
import { formatDate, getAlertTypeLabel } from "@/lib/utils";
import { SeverityBadge } from "@/components/risk/SeverityBadge";
import type { AlertSeverity, AlertType } from "@/lib/types";
import { AlertTriangle, Info } from "lucide-react";
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

export default async function RiskPage({
  searchParams,
}: {
  searchParams: { severity?: string; status?: string; page?: string };
}) {
  const page = parseInt(searchParams.page || "1");
  const { data: alerts, meta } = await getRiskAlerts({
    page,
    page_size: 20,
    severity: searchParams.severity,
    status: searchParams.status || "open",
    sort: "score",
    order: "desc",
  });

  const statusFilter = searchParams.status || "open";

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-6">
        <h1 className="font-display text-xl font-semibold text-ve-text flex items-center gap-2">
          <AlertTriangle className="w-5 h-5 text-orange-400" />
          Panel de Alertas de Riesgo
        </h1>
        <p className="text-ve-muted text-sm mt-1">
          {meta.total_results} alerta(s) — Motor de banderas rojas OCDS
        </p>
      </div>

      {/* Aviso human-in-the-loop */}
      <div className="bg-ve-slate border border-ve-border rounded-xl p-4 mb-6 flex items-start gap-3">
        <Info className="w-4 h-4 text-blue-400 flex-shrink-0 mt-0.5" />
        <p className="text-xs text-ve-muted">
          <span className="text-ve-text font-semibold">Human-in-the-loop:</span> Las alertas son señales
          para priorización y revisión por auditores, no prueba concluyente de irregularidad.
          Cada alerta debe ser revisada y validada por un analista antes de generar consecuencias.
        </p>
      </div>

      {/* Filtros */}
      <div className="flex flex-wrap gap-2 mb-6">
        {[
          { label: "Abiertas", status: "open" },
          { label: "Revisadas", status: "reviewed" },
          { label: "Desestimadas", status: "dismissed" },
        ].map(({ label, status }) => (
          <Link
            key={label}
            href={`/risk?status=${status}`}
            className={`px-3 py-1.5 rounded-full text-xs font-display border transition-all ${
              statusFilter === status
                ? "bg-ve-blue/20 border-ve-blue text-ve-blue"
                : "bg-ve-slate border-ve-border text-ve-muted hover:border-ve-muted"
            }`}
          >
            {label}
          </Link>
        ))}
        <span className="text-ve-border">|</span>
        {(["critical", "high", "medium", "low"] as AlertSeverity[]).map((sev) => (
          <Link
            key={sev}
            href={`/risk?severity=${sev}&status=${statusFilter}`}
            className={`px-3 py-1.5 rounded-full text-xs font-display border transition-all ${
              searchParams.severity === sev
                ? "bg-ve-blue/20 border-ve-blue text-ve-blue"
                : "bg-ve-slate border-ve-border text-ve-muted hover:border-ve-muted"
            }`}
          >
            <SeverityBadge severity={sev} className="text-xs" />
          </Link>
        ))}
      </div>

      {/* Alertas */}
      <div className="space-y-4">
        {alerts.length === 0 ? (
          <div className="text-center py-16 text-ve-muted">
            <AlertTriangle className="w-12 h-12 mx-auto mb-4 opacity-30" />
            <p className="font-display text-sm">No hay alertas con los filtros seleccionados</p>
          </div>
        ) : (
          alerts.map((alert) => (
            <div
              key={alert.id}
              className="bg-ve-slate border border-ve-border rounded-xl p-5 hover:border-ve-muted transition-colors"
            >
              <div className="flex items-start justify-between gap-4 mb-3">
                <div className="flex items-center gap-2 flex-wrap">
                  <SeverityBadge severity={alert.severity as AlertSeverity} />
                  <span className="font-display text-xs text-ve-muted px-2 py-0.5 bg-ve-dark rounded border border-ve-border">
                    {getAlertTypeLabel(alert.type as AlertType)}
                  </span>
                  {alert.status !== "open" && (
                    <span className={`font-display text-xs px-2 py-0.5 rounded border ${
                      alert.status === "reviewed"
                        ? "text-blue-400 border-blue-400/30 bg-blue-400/10"
                        : "text-ve-muted border-ve-border bg-ve-dark"
                    }`}>
                      {alert.status === "reviewed" ? "Revisada" : "Desestimada"}
                    </span>
                  )}
                </div>
                <div className="text-right flex-shrink-0">
                  <div className="font-display text-lg font-semibold text-ve-text">
                    {(alert.score * 100).toFixed(0)}%
                  </div>
                  <div className="text-xs text-ve-muted">score</div>
                </div>
              </div>

              {/* Explicaciones */}
              <ul className="space-y-1 mb-3">
                {alert.explanation.map((exp, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm text-ve-text">
                    <span className="text-ve-red mt-1 flex-shrink-0">&#9656;</span>
                    {exp}
                  </li>
                ))}
              </ul>

              {/* Datos de soporte */}
              {Object.keys(alert.supporting_data).length > 0 && (
                <div className="bg-ve-dark/50 rounded-lg p-3 font-display text-xs text-ve-muted border border-ve-border/50">
                  {Object.entries(alert.supporting_data).map(([k, v]) => (
                    <span key={k} className="mr-4">
                      <span className="text-ve-muted/60">{k}:</span>{" "}
                      <span className="text-ve-text">{String(v)}</span>
                    </span>
                  ))}
                </div>
              )}

              <div className="flex items-center justify-between mt-3 pt-3 border-t border-ve-border/50">
                <span className="font-display text-xs text-ve-muted">
                  Generada: {formatDate(alert.generated_at)}
                </span>
                <span className="font-display text-xs text-ve-muted/60">
                  ID: {alert.id.slice(0, 8)}...
                </span>
              </div>
            </div>
          ))
        )}
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
                href={buildPageHref("/risk", searchParams, page - 1)}
                className="px-3 py-1.5 text-xs font-display bg-ve-dark border border-ve-border rounded-lg text-ve-muted hover:text-ve-text"
              >
                Anterior
              </Link>
            )}
            {page < meta.total_pages && (
              <Link
                href={buildPageHref("/risk", searchParams, page + 1)}
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
