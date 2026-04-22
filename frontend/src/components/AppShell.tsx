import Link from "next/link";
import type { ReactNode } from "react";

const nav = [
  { href: "/", label: "Home" },
  { href: "/analysis", label: "Analysis" },
  { href: "/upload", label: "Upload" },
  { href: "/progress", label: "Progress" },
  { href: "/evidence", label: "Evidence" },
  { href: "/report", label: "Report" },
  { href: "/review", label: "Review" },
  { href: "/export", label: "Export" },
  { href: "/eval", label: "Eval" },
];

export function AppShell({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen hero-glow">
      <header className="sticky top-0 z-20 border-b border-border/80 bg-white/70 backdrop-blur-md">
        <div className="mx-auto flex max-w-6xl items-center justify-between gap-4 px-6 py-4">
          <Link href="/" className="text-lg font-bold tracking-tight text-ink">
            FieldOps <span className="text-primary">Copilot</span>
          </Link>
          <nav className="hidden flex-wrap items-center gap-2 md:flex">
            {nav.map((n) => (
              <Link
                key={n.href}
                href={n.href}
                className="rounded-pill px-3 py-1 text-xs font-semibold text-ink/70 hover:bg-primary/10 hover:text-primary"
              >
                {n.label}
              </Link>
            ))}
          </nav>
        </div>
      </header>
      <main className="mx-auto max-w-6xl px-6 py-10">{children}</main>
    </div>
  );
}
