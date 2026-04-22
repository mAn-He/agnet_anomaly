"""End-to-end pipeline evaluation (implement metrics in Phase 6)."""

from __future__ import annotations

import argparse


def main() -> None:
    p = argparse.ArgumentParser(description="Evaluate full workflow.")
    p.add_argument("--cases", default="data/integration_cases")
    args = p.parse_args()
    print("[stub] eval_end_to_end — not implemented.")
    print(f"  cases={args.cases}")


if __name__ == "__main__":
    main()
