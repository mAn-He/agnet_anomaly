"""Tabular triage evaluation (implement metrics in Phase 6)."""

from __future__ import annotations

import argparse


def main() -> None:
    p = argparse.ArgumentParser(description="Evaluate triage classifier.")
    p.add_argument("--test-csv", default="data/processed/ai4i/test.csv")
    args = p.parse_args()
    print("[stub] eval_triage — not implemented.")
    print(f"  test_csv={args.test_csv}")


if __name__ == "__main__":
    main()
