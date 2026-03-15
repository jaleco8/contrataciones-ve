"use client";

import { useEffect } from "react";
import { AlertTriangle } from "lucide-react";

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error(error);
  }, [error]);

  return (
    <div className="max-w-7xl mx-auto px-4 py-16 text-center">
      <AlertTriangle className="w-12 h-12 mx-auto mb-4 text-orange-400 opacity-70" />
      <h2 className="font-display text-xl font-semibold text-ve-text mb-2">
        Error al cargar los datos
      </h2>
      <p className="text-ve-muted text-sm mb-6">
        No se pudo conectar con el servidor. Verifica tu conexión e intenta de nuevo.
      </p>
      <button
        onClick={reset}
        className="inline-flex items-center gap-2 px-4 py-2 bg-ve-blue/20 hover:bg-ve-blue/30 border border-ve-blue/40 rounded-lg text-sm text-ve-blue hover:text-white transition-all"
      >
        Reintentar
      </button>
    </div>
  );
}
