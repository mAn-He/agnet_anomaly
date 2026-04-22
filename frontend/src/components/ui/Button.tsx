import type { ButtonHTMLAttributes, ReactNode } from "react";

type Props = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: "primary" | "ghost";
  children: ReactNode;
};

export function Button({
  variant = "primary",
  className = "",
  children,
  ...rest
}: Props) {
  const base =
    "inline-flex items-center justify-center px-5 py-2.5 text-sm font-semibold rounded-pill transition focus:outline-none focus:ring-2 focus:ring-primary/40 disabled:opacity-50";
  const styles =
    variant === "primary"
      ? "bg-primary text-white shadow-card hover:brightness-110"
      : "bg-white text-ink border border-border hover:bg-surface";
  return (
    <button type="button" className={`${base} ${styles} ${className}`} {...rest}>
      {children}
    </button>
  );
}
