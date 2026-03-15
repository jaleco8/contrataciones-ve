import type { Metadata } from "next";
import { IBM_Plex_Mono, IBM_Plex_Sans } from "next/font/google";
import "./globals.css";
import { Navbar } from "@/components/layout/Navbar";
import { Footer } from "@/components/layout/Footer";

const ibmPlexMono = IBM_Plex_Mono({
  subsets: ["latin"],
  weight: ["400", "500", "600"],
  variable: "--font-mono",
  display: "swap",
});

const ibmPlexSans = IBM_Plex_Sans({
  subsets: ["latin"],
  weight: ["300", "400", "500", "600"],
  variable: "--font-sans",
  display: "swap",
});

export const metadata: Metadata = {
  title: "Contrataciones VE — Transparencia Pública",
  description:
    "Plataforma abierta anticorrupción de contratación y gasto público para Venezuela. Datos abiertos, alertas de riesgo y auditoría social.",
  keywords: ["Venezuela", "contratos", "transparencia", "anticorrupción", "datos abiertos"],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="es" className={`dark ${ibmPlexMono.variable} ${ibmPlexSans.variable}`}>
      <body className="bg-ve-dark text-ve-text font-body antialiased min-h-screen flex flex-col">
        <a
          href="#main-content"
          className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 z-50 px-4 py-2 bg-ve-blue text-white rounded-lg text-sm"
        >
          Saltar al contenido
        </a>
        <Navbar />
        <main id="main-content" className="flex-1">{children}</main>
        <Footer />
      </body>
    </html>
  );
}
