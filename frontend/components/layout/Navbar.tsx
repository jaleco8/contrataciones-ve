"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Shield, FileText, Users, AlertTriangle, Download } from "lucide-react";

export function Navbar() {
  const pathname = usePathname();

  function navClass(href: string) {
    const isActive = pathname === href || (href !== "/" && pathname.startsWith(href));
    return `flex items-center gap-2 px-3 py-2 rounded-lg text-sm transition-all ${
      isActive
        ? "text-ve-text bg-ve-border/50"
        : "text-ve-muted hover:text-ve-text hover:bg-ve-border/50"
    }`;
  }

  return (
    <nav className="border-b border-ve-border bg-ve-slate/50 backdrop-blur-sm sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-3 group">
            <Shield className="w-7 h-7 text-ve-red group-hover:text-ve-yellow transition-colors" />
            <div className="hidden sm:block">
              <div className="font-display text-sm font-semibold text-ve-text">CONTRATACIONES</div>
              <div className="font-display text-xs text-ve-yellow tracking-widest">VENEZUELA</div>
            </div>
          </Link>

          {/* Nav Links */}
          <div className="flex items-center gap-1">
            <Link href="/contracts" className={navClass("/contracts")}>
              <FileText className="w-4 h-4" />
              <span className="hidden md:inline">Contratos</span>
            </Link>
            <Link href="/suppliers" className={navClass("/suppliers")}>
              <Users className="w-4 h-4" />
              <span className="hidden md:inline">Proveedores</span>
            </Link>
            <Link href="/risk" className={navClass("/risk")}>
              <AlertTriangle className="w-4 h-4" />
              <span className="hidden md:inline">Alertas</span>
            </Link>

            <a
              href={`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/docs`}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-2 px-3 py-2 rounded-lg text-sm text-blue-400 hover:text-ve-yellow hover:bg-ve-border/50 transition-all ml-2"
            >
              <Download className="w-4 h-4" />
              <span className="hidden md:inline font-display text-xs">API</span>
            </a>
          </div>
        </div>
      </div>
    </nav>
  );
}
