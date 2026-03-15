import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // Paleta Venezuela: rojo, amarillo, azul + dark slate para gobierno
        ve: {
          red: "#CF142B",
          yellow: "#F4C430",
          blue: "#003DA5",
          dark: "#0D1117",
          slate: "#1B2432",
          border: "#2D3748",
          muted: "#4A5568",
          text: "#E2E8F0",
        },
        risk: {
          critical: "#FF3B30",
          high: "#FF9500",
          medium: "#FFCC00",
          low: "#34C759",
        }
      },
      fontFamily: {
        display: ["var(--font-mono)", "monospace"],
        body: ["var(--font-sans)", "sans-serif"],
      },
    },
  },
  plugins: [],
};

export default config;
