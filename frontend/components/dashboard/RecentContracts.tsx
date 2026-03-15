import Link from "next/link";
import { formatCurrency } from "@/lib/utils";
import { StatusBadge } from "@/components/contracts/StatusBadge";
import type { Contract, ContractStatus } from "@/lib/types";

export function RecentContracts({ contracts }: { contracts: Contract[] }) {
  return (
    <div className="space-y-3">
      {contracts.map((contract) => (
        <Link
          key={contract.id}
          href={`/contracts/${contract.id}`}
          className="block border border-ve-border/50 rounded-lg p-3 hover:border-ve-muted transition-colors"
        >
          <div className="flex items-start justify-between gap-2 mb-1">
            <StatusBadge status={contract.status as ContractStatus} />
            <span className="font-display text-xs text-ve-yellow font-semibold">
              {formatCurrency(contract.amount)}
            </span>
          </div>
          <p className="text-xs text-ve-text line-clamp-1">{contract.title}</p>
          <p className="text-xs text-ve-muted">{contract.buyer_name}</p>
        </Link>
      ))}
    </div>
  );
}
