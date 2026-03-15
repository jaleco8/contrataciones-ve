export function Footer() {
  return (
    <footer className="border-t border-ve-border bg-ve-slate/30 mt-16">
      <div className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="text-center md:text-left">
            <p className="font-display text-xs text-ve-muted">
              Plataforma Abierta Anticorrupción Venezuela — Prototipo v1.0
            </p>
            <p className="font-display text-xs text-ve-muted/60 mt-1">
              Autor: Jesús Alexander León Cordero | Tech Lead | MSc. Ciencias de la Computación
            </p>
          </div>
          <div className="flex items-center gap-4">
            <span className="text-xs text-ve-muted font-display">OCDS v1.1</span>
            <span className="text-xs text-ve-muted font-display">MIT License</span>
            <span className="text-xs text-ve-muted font-display">CC BY 4.0</span>
          </div>
        </div>
      </div>
    </footer>
  );
}
