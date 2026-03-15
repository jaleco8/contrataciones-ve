import Link from "next/link";
import { Users } from "lucide-react";

export default function SupplierNotFound() {
  return (
    <div className="max-w-4xl mx-auto px-4 py-16 text-center">
      <Users className="w-12 h-12 mx-auto mb-4 text-ve-muted opacity-50" />
      <h2 className="font-display text-xl font-semibold text-ve-text mb-2">
        Proveedor no encontrado
      </h2>
      <p className="text-ve-muted text-sm mb-6">
        El proveedor que buscas no existe o fue eliminado.
      </p>
      <Link
        href="/suppliers"
        className="inline-flex items-center gap-2 px-4 py-2 bg-ve-slate border border-ve-border rounded-lg text-sm text-ve-muted hover:text-ve-text transition-colors"
      >
        Ver todos los proveedores
      </Link>
    </div>
  );
}
