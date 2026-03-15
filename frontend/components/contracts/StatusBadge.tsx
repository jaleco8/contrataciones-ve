import { cn, getStatusColor } from "@/lib/utils";
import type { ContractStatus } from "@/lib/types";

const LABELS: Record<ContractStatus, string> = {
  active: "Activo",
  completed: "Completado",
  draft: "Borrador",
  terminated: "Terminado",
  cancelled: "Cancelado",
};

export function StatusBadge({ status }: { status: ContractStatus }) {
  return (
    <span className={cn("inline-flex px-2 py-0.5 rounded text-xs font-medium", getStatusColor(status))}>
      {LABELS[status]}
    </span>
  );
}
