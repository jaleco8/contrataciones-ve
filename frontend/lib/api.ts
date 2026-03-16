import type {
  PaginatedResponse,
  Contract,
  Process,
  Supplier,
  RiskAlert,
} from "./types";

// Server-side: API_URL (no NEXT_PUBLIC_ prefix)
// Client-side: NEXT_PUBLIC_API_URL kept only for Navbar docs link
const API_URL = process.env.API_URL ?? process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = "ApiError";
  }
}

async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_URL}/api/v1${path}`, {
    cache: "no-store",
    ...init,
  });
  if (!res.ok) {
    const message = await res.text().catch(() => res.statusText);
    throw new ApiError(res.status, message);
  }
  return res.json() as Promise<T>;
}

function toQueryString(params?: Record<string, unknown>): string {
  if (!params) return "";
  const p = new URLSearchParams();
  for (const [k, v] of Object.entries(params)) {
    if (v !== undefined && v !== null) p.set(k, String(v));
  }
  const str = p.toString();
  return str ? `?${str}` : "";
}

// Contratos
export async function getContracts(
  params?: Record<string, unknown>
): Promise<PaginatedResponse<Contract>> {
  return apiFetch(`/contracts${toQueryString(params)}`);
}

export async function getContract(id: string): Promise<Contract> {
  return apiFetch(`/contracts/${id}`);
}

// Procesos
export async function getProcesses(
  params?: Record<string, unknown>
): Promise<PaginatedResponse<Process>> {
  return apiFetch(`/processes${toQueryString(params)}`);
}

export async function getProcess(id: string): Promise<Process> {
  return apiFetch(`/processes/${id}`);
}

// Proveedores
export async function getSuppliers(
  params?: Record<string, unknown>
): Promise<PaginatedResponse<Supplier>> {
  return apiFetch(`/suppliers${toQueryString(params)}`);
}

export async function getSupplier(id: string): Promise<Supplier> {
  return apiFetch(`/suppliers/${id}`);
}

// Alertas
export async function getRiskAlerts(
  params?: Record<string, unknown>
): Promise<PaginatedResponse<RiskAlert>> {
  return apiFetch(`/risk/alerts${toQueryString(params)}`);
}

export async function updateAlert(
  id: string,
  update: { status?: string; reviewed_by?: string; review_notes?: string }
): Promise<RiskAlert> {
  return apiFetch(`/risk/alerts/${id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(update),
  });
}
