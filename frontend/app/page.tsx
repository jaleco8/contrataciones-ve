import Link from "next/link";
import {
  FileText, Users, AlertTriangle, TrendingUp,
  Shield, ArrowRight, Activity, Database
} from "lucide-react";
import { getContracts, getRiskAlerts, getSuppliers, getProcesses } from "@/lib/api";
import { formatCurrency } from "@/lib/utils";
import { SeverityBadge } from "@/components/risk/SeverityBadge";
import { StatusBadge } from "@/components/contracts/StatusBadge";
import type { AlertSeverity, ContractStatus } from "@/lib/types";

async function getDashboardData() {
  const [
    activeContracts,
    allContracts,
    openAlerts,
    criticalAlerts,
    suppliers,
    tenders,
    recentContracts,
    recentAlerts,
  ] = await Promise.allSettled([
    getContracts({ page_size: 1, status: "active" }),
    getContracts({ page_size: 1 }),
    getRiskAlerts({ page_size: 1, status: "open" }),
    getRiskAlerts({ page_size: 1, status: "open", severity: "critical" }),
    getSuppliers({ page_size: 1 }),
    getProcesses({ page_size: 1, status: "tender" }),
    getContracts({ page_size: 5, sort: "signed_at", order: "desc" }),
    getRiskAlerts({ page_size: 4, status: "open", sort: "score", order: "desc" }),
  ]);

  return {
    stats: {
      activeContracts: activeContracts.status === "fulfilled" ? activeContracts.value.meta.total_results : 0,
      totalContracts: allContracts.status === "fulfilled" ? allContracts.value.meta.total_results : 0,
      openAlerts: openAlerts.status === "fulfilled" ? openAlerts.value.meta.total_results : 0,
      criticalAlerts: criticalAlerts.status === "fulfilled" ? criticalAlerts.value.meta.total_results : 0,
      totalSuppliers: suppliers.status === "fulfilled" ? suppliers.value.meta.total_results : 0,
      activeTenders: tenders.status === "fulfilled" ? tenders.value.meta.total_results : 0,
    },
    recentContracts: recentContracts.status === "fulfilled" ? recentContracts.value.data : [],
    recentAlerts: recentAlerts.status === "fulfilled" ? recentAlerts.value.data : [],
  };
}

export default async function DashboardPage() {
  const { stats, recentContracts, recentAlerts } = await getDashboardData();

  const statCards = [
    {
      label: "Contratos Activos",
      value: stats.activeContracts,
      total: `de ${stats.totalContracts} totales`,
      icon: FileText,
      color: "text-blue-400",
      bg: "bg-blue-400/10",
      href: "/contracts",
    },
    {
      label: "Alertas Abiertas",
      value: stats.openAlerts,
      total: `${stats.criticalAlerts} críticas`,
      icon: AlertTriangle,
      color: stats.criticalAlerts > 0 ? "text-red-400" : "text-orange-400",
      bg: stats.criticalAlerts > 0 ? "bg-red-400/10" : "bg-orange-400/10",
      href: "/risk",
    },
    {
      label: "Proveedores",
      value: stats.totalSuppliers,
      total: "registrados",
      icon: Users,
      color: "text-green-400",
      bg: "bg-green-400/10",
      href: "/suppliers",
    },
    {
      label: "Licitaciones Activas",
      value: stats.activeTenders,
      total: "en proceso",
      icon: Activity,
      color: "text-yellow-400",
      bg: "bg-yellow-400/10",
      href: "/contracts",
    },
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">

      {/* Hero */}
      <div className="mb-10">
        <div className="flex items-center gap-3 mb-4">
          <Shield className="w-8 h-8 text-ve-red" />
          <div>
            <h1 className="font-display text-2xl font-semibold text-ve-text">
              Plataforma Abierta Anticorrupción
            </h1>
            <p className="text-ve-muted text-sm">
              Transparencia de contratación y gasto público — Venezuela
            </p>
          </div>
        </div>

        {/* Banner disclaimer */}
        <div className="bg-ve-yellow/10 border border-ve-yellow/30 rounded-lg p-3 flex items-start gap-3">
          <TrendingUp className="w-4 h-4 text-ve-yellow mt-0.5 flex-shrink-0" />
          <p className="text-xs text-ve-yellow/80 font-display">
            PROTOTIPO DE DEMOSTRACIÓN — Datos ficticios para propósitos de desarrollo.
            Las alertas de riesgo son señales para revisión humana, no conclusiones.
            <span className="font-semibold"> Human-in-the-loop obligatorio.</span>
          </p>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-10">
        {statCards.map(({ label, value, total, icon: Icon, color, bg, href }) => (
          <Link
            key={label}
            href={href}
            className="bg-ve-slate border border-ve-border rounded-xl p-5 hover:border-ve-muted transition-colors group"
          >
            <div className={`inline-flex p-2 rounded-lg ${bg} mb-3`}>
              <Icon className={`w-5 h-5 ${color}`} />
            </div>
            <div className="font-display text-3xl font-semibold text-ve-text group-hover:text-white transition-colors">
              {value}
            </div>
            <div className="text-xs text-ve-muted mt-1">{label}</div>
            <div className="text-xs text-ve-muted/60">{total}</div>
          </Link>
        ))}
      </div>

      {/* Main Content Grid */}
      <div className="grid lg:grid-cols-2 gap-6">

        {/* Alertas recientes */}
        <div className="bg-ve-slate border border-ve-border rounded-xl p-6">
          <div className="flex items-center justify-between mb-5">
            <h2 className="font-display text-sm font-semibold text-ve-text flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 text-orange-400" />
              Alertas de Riesgo Prioritarias
            </h2>
            <Link href="/risk" className="text-xs text-ve-blue hover:text-ve-yellow flex items-center gap-1 transition-colors">
              Ver todas <ArrowRight className="w-3 h-3" />
            </Link>
          </div>

          <div className="space-y-3">
            {recentAlerts.length === 0 ? (
              <p className="text-ve-muted text-sm text-center py-4">No hay alertas abiertas</p>
            ) : (
              recentAlerts.map((alert) => (
                <div key={alert.id} className="border border-ve-border/50 rounded-lg p-3 hover:border-ve-muted transition-colors">
                  <div className="flex items-start justify-between gap-2 mb-2">
                    <SeverityBadge severity={alert.severity as AlertSeverity} />
                    <span className="font-display text-xs text-ve-muted">
                      Score: {(alert.score * 100).toFixed(0)}%
                    </span>
                  </div>
                  <p className="text-xs text-ve-text mb-1 line-clamp-2">
                    {alert.explanation[0]}
                  </p>
                  {alert.explanation[1] && (
                    <p className="text-xs text-ve-muted line-clamp-1">
                      {alert.explanation[1]}
                    </p>
                  )}
                </div>
              ))
            )}
          </div>
        </div>

        {/* Contratos recientes */}
        <div className="bg-ve-slate border border-ve-border rounded-xl p-6">
          <div className="flex items-center justify-between mb-5">
            <h2 className="font-display text-sm font-semibold text-ve-text flex items-center gap-2">
              <FileText className="w-4 h-4 text-blue-400" />
              Contratos Recientes
            </h2>
            <Link href="/contracts" className="text-xs text-ve-blue hover:text-ve-yellow flex items-center gap-1 transition-colors">
              Ver todos <ArrowRight className="w-3 h-3" />
            </Link>
          </div>

          <div className="space-y-3">
            {recentContracts.map((contract) => (
              <Link
                key={contract.id}
                href={`/contracts/${contract.id}`}
                className="block border border-ve-border/50 rounded-lg p-3 hover:border-ve-muted transition-colors"
              >
                <div className="flex items-start justify-between gap-2 mb-1">
                  <StatusBadge status={contract.status as ContractStatus} />
                  <span className="font-display text-xs text-ve-yellow font-semibold">
                    {formatCurrency(contract.amount, contract.currency)}
                  </span>
                </div>
                <p className="text-xs text-ve-text line-clamp-1 mb-1">{contract.title}</p>
                <p className="text-xs text-ve-muted">{contract.buyer_name}</p>
                {contract.has_amendments && (
                  <span className="inline-block mt-1 text-xs text-orange-400 font-display">
                    {contract.amendments_count} adenda(s)
                  </span>
                )}
              </Link>
            ))}
          </div>
        </div>
      </div>

      {/* API CTA */}
      <div className="mt-6 bg-ve-blue/10 border border-ve-blue/30 rounded-xl p-5 flex items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <Database className="w-5 h-5 text-ve-blue flex-shrink-0" />
          <div>
            <p className="font-display text-sm font-semibold text-ve-text">API Pública Disponible</p>
            <p className="text-xs text-ve-muted">OCDS compatible | Paginación estándar | CSV y JSON</p>
          </div>
        </div>
        <a
          href={`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/docs`}
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center gap-2 px-4 py-2 bg-ve-blue/20 hover:bg-ve-blue/30 border border-ve-blue/40 rounded-lg text-xs font-display text-ve-blue hover:text-white transition-all whitespace-nowrap"
        >
          Explorar API <ArrowRight className="w-3 h-3" />
        </a>
      </div>
    </div>
  );
}
