import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";
import type { AlertSeverity, AlertType, ContractStatus, SanctionStatus } from "./types";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatCurrency(amount: number, currency = "USD"): string {
  return new Intl.NumberFormat("es-VE", {
    style: "currency",
    currency,
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(amount);
}

export function formatDate(dateStr?: string | null): string {
  if (!dateStr) return "—";
  return new Intl.DateTimeFormat("es-VE", {
    year: "numeric",
    month: "short",
    day: "numeric",
  }).format(new Date(dateStr));
}

export function getSeverityColor(severity: AlertSeverity): string {
  const colors: Record<AlertSeverity, string> = {
    critical: "text-red-400 bg-red-400/10 border-red-400/30",
    high: "text-orange-400 bg-orange-400/10 border-orange-400/30",
    medium: "text-yellow-400 bg-yellow-400/10 border-yellow-400/30",
    low: "text-green-400 bg-green-400/10 border-green-400/30",
  };
  return colors[severity];
}

export function getStatusColor(status: ContractStatus): string {
  const colors: Record<ContractStatus, string> = {
    active: "text-green-400 bg-green-400/10",
    completed: "text-blue-400 bg-blue-400/10",
    draft: "text-gray-400 bg-gray-400/10",
    terminated: "text-orange-400 bg-orange-400/10",
    cancelled: "text-red-400 bg-red-400/10",
  };
  return colors[status] || "text-gray-400 bg-gray-400/10";
}

export function getSanctionColor(status: SanctionStatus): string {
  const colors: Record<SanctionStatus, string> = {
    active: "text-green-400 bg-green-400/10",
    sanctioned: "text-red-400 bg-red-400/10",
    suspended: "text-orange-400 bg-orange-400/10",
  };
  return colors[status];
}

export function getAlertTypeLabel(type: AlertType): string {
  const labels: Record<AlertType, string> = {
    overprice: "Sobrecosto",
    repeat_entity: "Entidad Sancionada",
    low_competition: "Baja Competencia",
    systematic_amendments: "Adendas Sistemáticas",
    winner_rotation: "Concentración",
    emergency_procurement: "Emergencia",
    short_bidding_period: "Plazo Corto",
  };
  return labels[type] || type;
}

export function getProcurementMethodLabel(method?: string): string {
  const labels: Record<string, string> = {
    open_tender: "Concurso Abierto",
    limited: "Concurso Limitado",
    direct: "Contratación Directa",
    framework: "Marco de Acuerdo",
    emergency: "Emergencia",
  };
  return method ? (labels[method] || method) : "—";
}
