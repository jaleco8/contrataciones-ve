import { cn, getSeverityColor } from "@/lib/utils";
import type { AlertSeverity } from "@/lib/types";

interface Props {
  severity: AlertSeverity;
  className?: string;
}

const LABELS: Record<AlertSeverity, string> = {
  critical: "CRÍTICA",
  high: "ALTA",
  medium: "MEDIA",
  low: "BAJA",
};

export function SeverityBadge({ severity, className }: Props) {
  return (
    <span
      className={cn(
        "inline-flex items-center px-2 py-0.5 rounded text-xs font-display font-medium border",
        getSeverityColor(severity),
        className
      )}
    >
      {LABELS[severity]}
    </span>
  );
}
