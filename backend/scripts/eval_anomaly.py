"""Anomaly detection evaluation (implement metrics in Phase 6)."""

from __future__ import annotations

import argparse


def main() -> None:
    p = argparse.ArgumentParser(description="Evaluate anomaly detection.")
    p.add_argument("--dataset", default="mvtec", choices=["mvtec", "visa"])
    p.add_argument("--scores", default="data/processed/anomaly_scores.jsonl")
    args = p.parse_args()
    print("[stub] eval_anomaly — not implemented.")
    print(f"  dataset={args.dataset} scores={args.scores}")


if __name__ == "__main__":
    main()
