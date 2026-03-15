import Link from "next/link";
import { formatCurrency, formatDate } from "@/lib/utils";
import { StatusBadge } from "./StatusBadge";
import type { Contract, ContractStatus } from "@/lib/types";

export function ContractCard({ contract }: { contract: Contract }) {
  return (
    <Link
      href={`/contracts/${contract.id}`}
      className="block bg-ve-slate border border-ve-border rounded-xl p-5 hover:border-ve-muted transition-colors"
    >
      <div className="flex items-start justify-between gap-2 mb-2">
        <StatusBadge status={contract.status as ContractStatus} />
        <span className="font-display text-xs text-ve-yellow font-semibold">
          {formatCurrency(contract.amount, contract.currency)}
        </span>
      </div>
      <p className="text-sm text-ve-text line-clamp-2 mb-1">{contract.title}</p>
      <p className="text-xs text-ve-muted">{contract.buyer_name}</p>
      <p className="text-xs text-ve-muted/60 mt-1 font-display">
        {contract.contract_number} | {formatDate(contract.signed_at)}
      </p>
    </Link>
  );
}
