export interface PaginationMeta {
  page: number;
  page_size: number;
  total_results: number;
  total_pages: number;
  sort: string;
  order: string;
  timezone: string;
}

export interface PaginatedResponse<T> {
  meta: PaginationMeta;
  data: T[];
}

export interface Contract {
  id: string;
  contract_number: string;
  process_id?: string;
  supplier_id?: string;
  supplier_name: string;
  buyer_name: string;
  title: string;
  description?: string;
  category?: string;
  status: ContractStatus;
  amount: number;
  currency: string;
  original_amount?: number;
  signed_at?: string;
  start_date?: string;
  end_date?: string;
  has_amendments: boolean;
  amendments_count: number;
  amendment_amount_increase: number;
  created_at: string;
  updated_at: string;
}

export type ContractStatus = "draft" | "active" | "completed" | "terminated" | "cancelled";

export interface Process {
  id: string;
  ocid?: string;
  title: string;
  description?: string;
  status: ProcessStatus;
  procurement_method?: string;
  buyer_name: string;
  buyer_entity_type?: string;
  tender_amount?: number;
  tender_currency: string;
  awarded_amount?: number;
  awarded_supplier_name?: string;
  published_at?: string;
  award_date?: string;
  category?: string;
  bidders_count: number;
  created_at: string;
  updated_at: string;
}

export type ProcessStatus = "planned" | "tender" | "awarded" | "cancelled" | "complete";

export interface Supplier {
  id: string;
  rif: string;
  name: string;
  legal_name?: string;
  sector?: string;
  type: string;
  sanction_status: SanctionStatus;
  awards_count_12m: number;
  total_awarded_12m: number;
  state?: string;
  created_at: string;
  updated_at: string;
}

export type SanctionStatus = "active" | "sanctioned" | "suspended";

export interface RiskAlert {
  id: string;
  type: AlertType;
  severity: AlertSeverity;
  status: AlertStatus;
  score: number;
  contract_id?: string;
  process_id?: string;
  supplier_id?: string;
  explanation: string[];
  supporting_data: Record<string, unknown>;
  reviewed_by?: string;
  reviewed_at?: string;
  review_notes?: string;
  generated_at: string;
  updated_at: string;
}

export type AlertType =
  | "overprice"
  | "repeat_entity"
  | "low_competition"
  | "systematic_amendments"
  | "winner_rotation"
  | "emergency_procurement"
  | "short_bidding_period";

export type AlertSeverity = "low" | "medium" | "high" | "critical";
export type AlertStatus = "open" | "reviewed" | "dismissed";

export interface DashboardStats {
  active_contracts: number;
  total_contracts: number;
  total_value_usd: number;
  active_suppliers: number;
  open_alerts: number;
  critical_alerts: number;
  active_tenders: number;
  amended_contracts: number;
}
