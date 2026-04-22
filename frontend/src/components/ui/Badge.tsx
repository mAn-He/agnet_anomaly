import type { ReactNode } from "react";

const tones: Record<string, string> = {
  image: "bg-cyan/15 text-primary border-cyan/30",
  pdf: "bg-primary/10 text-primary border-primary/25",
  text: "bg-violet/10 text-violet border-violet/25",
  sensor: "bg-ink/5 text-ink border-border",
  tabular: "bg-ink/5 text-ink border-border",
  default: "bg-ink/5 text-ink border-border",
};

export function Badge({
  tone = "default",
  children,
}: {
  tone?: keyof typeof tones;
  children: ReactNode;
}) {
  return (
    <span
      className={`inline-flex items-center rounded-pill border px-2.5 py-0.5 text-xs font-semibold ${tones[tone] ?? tones.default}`}
    >
      {children}
    </span>
  );
}
