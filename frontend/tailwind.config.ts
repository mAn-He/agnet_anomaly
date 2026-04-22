import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        bg: "var(--bg)",
        surface: "var(--surface)",
        ink: "var(--text)",
        border: "var(--border)",
        primary: "var(--primary)",
        cyan: "var(--cyan)",
        violet: "var(--violet)",
      },
      borderRadius: {
        pill: "9999px",
      },
      boxShadow: {
        card: "0 12px 40px -24px rgba(15, 23, 42, 0.25)",
      },
    },
  },
  plugins: [],
};

export default config;
