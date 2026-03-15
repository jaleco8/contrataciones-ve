import { formatCurrency, getSanctionColor, cn } from "@/lib/utils";
import type { Supplier, SanctionStatus } from "@/lib/types";

export function SupplierCard({ supplier }: { supplier: Supplier }) {
  return (
    <div className="bg-ve-slate border border-ve-border rounded-xl p-5 hover:border-ve-muted transition-colors">
      <div className="flex items-start justify-between gap-3 mb-3">
        <div>
          <p className="font-semibold text-ve-text text-sm">{supplier.name}</p>
          <p className="font-display text-xs text-ve-muted">{supplier.rif}</p>
        </div>
        <span className={cn(
          "inline-flex px-2 py-0.5 rounded text-xs font-display font-medium border",
          getSanctionColor(supplier.sanction_status as SanctionStatus)
        )}>
          {supplier.sanction_status === "active" ? "Activo" : supplier.sanction_status.toUpperCase()}
        </span>
      </div>
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
    </div>
  );
}
