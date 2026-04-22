"""Report quality evaluation (implement metrics in Phase 6)."""

from __future__ import annotations

import argparse


def main() -> None:
    p = argparse.ArgumentParser(description="Evaluate generated reports.")
    p.add_argument("--cases", default="data/integration_cases")
    args = p.parse_args()
    print("[stub] eval_report — not implemented.")
    print(f"  cases={args.cases}")


if __name__ == "__main__":
    main()
