"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import type { LucideIcon } from "lucide-react";

interface NavLinkProps {
  href: string;
  label: string;
  icon: LucideIcon;
}

export function NavLink({ href, label, icon: Icon }: NavLinkProps) {
  const pathname = usePathname();
  const isActive =
    pathname === href || (href !== "/" && pathname.startsWith(href));

  return (
    <Link
      href={href}
      aria-label={label}
      className={`flex items-center gap-2 px-3 py-2 rounded-lg text-sm transition-all ${
        isActive
          ? "text-ve-text bg-ve-border/50"
          : "text-ve-muted hover:text-ve-text hover:bg-ve-border/50"
      }`}
    >
      <Icon className="w-4 h-4" aria-hidden="true" />
      <span className="hidden md:inline">{label}</span>
    </Link>
  );
}
