import Link from "next/link";
import { formatCurrency, formatDate } from "@/lib/utils";
import { StatusBadge } from "./StatusBadge";
import type { Contract, ContractStatus } from "@/lib/types";

export function ContractTable({ contracts }: { contracts: Contract[] }) {
  return (
    <div className="overflow-x-auto">
      <table className="w-full">
        <thead>
          <tr className="border-b border-ve-border bg-ve-dark/50">
            <th className="text-left py-3 px-4 text-xs font-display font-medium text-ve-muted">Contrato</th>
            <th className="text-left py-3 px-4 text-xs font-display font-medium text-ve-muted hidden md:table-cell">Comprador</th>
            <th className="text-right py-3 px-4 text-xs font-display font-medium text-ve-muted">Monto</th>
            <th className="text-center py-3 px-4 text-xs font-display font-medium text-ve-muted hidden sm:table-cell">Estado</th>
          </tr>
        </thead>
        <tbody>
          {contracts.map((contract) => (
            <tr key={contract.id} className="border-b border-ve-border/50 hover:bg-ve-dark/30 transition-colors">
              <td className="py-3 px-4">
                <Link href={`/contracts/${contract.id}`} className="group">
                  <div className="font-display text-xs text-ve-muted">{contract.contract_number}</div>
                  <div className="text-sm text-ve-text group-hover:text-white line-clamp-1">{contract.title}</div>
                </Link>
              </td>
              <td className="py-3 px-4 hidden md:table-cell">
                <p className="text-xs text-ve-muted line-clamp-1">{contract.buyer_name}</p>
              </td>
              <td className="py-3 px-4 text-right">
                <span className="font-display text-xs font-semibold text-ve-yellow">
                  {formatCurrency(contract.amount)}
                </span>
              </td>
              <td className="py-3 px-4 text-center hidden sm:table-cell">
                <StatusBadge status={contract.status as ContractStatus} />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
