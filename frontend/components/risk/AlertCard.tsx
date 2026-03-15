import { SeverityBadge } from "./SeverityBadge";
import { formatDate, getAlertTypeLabel } from "@/lib/utils";
import type { RiskAlert, AlertSeverity, AlertType } from "@/lib/types";

export function AlertCard({ alert }: { alert: RiskAlert }) {
  return (
    <div className="bg-ve-slate border border-ve-border rounded-xl p-5 hover:border-ve-muted transition-colors">
      <div className="flex items-start justify-between gap-4 mb-3">
        <div className="flex items-center gap-2">
          <SeverityBadge severity={alert.severity as AlertSeverity} />
          <span className="font-display text-xs text-ve-muted">
            {getAlertTypeLabel(alert.type as AlertType)}
          </span>
        </div>
        <span className="font-display text-sm font-semibold text-ve-text">
          {(alert.score * 100).toFixed(0)}%
        </span>
      </div>
      <ul className="space-y-1">
        {alert.explanation.map((exp, i) => (
          <li key={i} className="text-xs text-ve-text flex items-start gap-2">
            <span className="text-ve-red mt-0.5">&#9656;</span>
            {exp}
          </li>
        ))}
      </ul>
      <p className="text-xs text-ve-muted mt-3 font-display">
        {formatDate(alert.generated_at)}
      </p>
    </div>
  );
}
