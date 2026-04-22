"""OCR / form extraction evaluation (implement metrics in Phase 6)."""

from __future__ import annotations

import argparse


def main() -> None:
    p = argparse.ArgumentParser(description="Evaluate OCR / field extraction.")
    p.add_argument("--gold-dir", default="data/benchmarks/funsd", help="Ground-truth root")
    p.add_argument("--pred-dir", default="data/processed/ocr_preds", help="Predictions root")
    args = p.parse_args()
    print("[stub] eval_ocr — not implemented.")
    print(f"  gold={args.gold_dir} pred={args.pred_dir}")


if __name__ == "__main__":
    main()
