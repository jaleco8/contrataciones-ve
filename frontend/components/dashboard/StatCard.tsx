import type { LucideIcon } from "lucide-react";

interface Props {
  label: string;
  value: number | string;
  subtitle?: string;
  icon: LucideIcon;
  color: string;
  bg: string;
}

export function StatCard({ label, value, subtitle, icon: Icon, color, bg }: Props) {
  return (
    <div className="bg-ve-slate border border-ve-border rounded-xl p-5 hover:border-ve-muted transition-colors">
      <div className={`inline-flex p-2 rounded-lg ${bg} mb-3`}>
        <Icon className={`w-5 h-5 ${color}`} />
      </div>
      <div className="font-display text-3xl font-semibold text-ve-text">{value}</div>
      <div className="text-xs text-ve-muted mt-1">{label}</div>
      {subtitle && <div className="text-xs text-ve-muted/60">{subtitle}</div>}
    </div>
  );
}
