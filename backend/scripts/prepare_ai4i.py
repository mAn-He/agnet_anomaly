"""Download and stage AI4I 2020 (UCI) for tabular triage / LightGBM baselines.

Official: https://archive.ics.uci.edu/dataset/601/ai4i+2020+predictive+maintenance+dataset
"""

from __future__ import annotations

import argparse
import csv
import shutil
from pathlib import Path

from _data_prep_utils import (
    download_url,
    extract_zip,
    repo_root_from_script,
    resolve_under_repo,
    write_json,
)


UCI_AI4I_ZIP = (
    "https://archive.ics.uci.edu/static/public/601/"
    "ai4i+2020+predictive+maintenance+dataset.zip"
)


def _find_csv(root: Path) -> Path:
    cands = sorted(root.rglob("*.csv"))
    if not cands:
        raise FileNotFoundError(f"No CSV found under extracted tree: {root}")
    # Prefer filename matching ai4i if multiple
    for p in cands:
        if "ai4i" in p.name.lower():
            return p
    return cands[0]


def main() -> None:
    parser = argparse.ArgumentParser(description="Download AI4I 2020 and write manifest.")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="Repository root (default: infer from script location).",
    )
    parser.add_argument(
        "--output-dir",
        default="data/processed/ai4i",
        help="Relative to repo root; CSV + manifest written here.",
    )
    parser.add_argument(
        "--raw-dir",
        default="data/raw/ai4i",
        help="Relative to repo root; download + extract cache.",
    )
    parser.add_argument(
        "--skip-download",
        action="store_true",
        help="Reuse existing zip/extract under raw-dir.",
    )
    args = parser.parse_args()

    root = args.repo_root or repo_root_from_script(__file__)
    out_dir = resolve_under_repo(root, args.output_dir)
    raw_dir = resolve_under_repo(root, args.raw_dir)
    zip_path = raw_dir / "ai4i2020.zip"
    extract_dir = raw_dir / "extracted"

    if not args.skip_download:
        raw_dir.mkdir(parents=True, exist_ok=True)
        print(f"Downloading:\n  {UCI_AI4I_ZIP}\n→ {zip_path}")
        download_url(UCI_AI4I_ZIP, zip_path)
        if extract_dir.exists():
            shutil.rmtree(extract_dir)
        extract_zip(zip_path, extract_dir)
    else:
        if not extract_dir.exists():
            raise SystemExit(
                f"--skip-download set but {extract_dir} missing. Run without --skip-download first."
            )

    src_csv = _find_csv(extract_dir)
    dest_csv = out_dir / src_csv.name
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src_csv, dest_csv)

    with dest_csv.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        n_rows = sum(1 for _ in reader)

    # Column grouping for triage MVP (binary / multi-label targets vary by task).
    label_candidates = {
        "Machine failure",
        "TWF",
        "HDF",
        "PWF",
        "OSF",
        "RNF",
    }
    label_columns = [c for c in header if c in label_candidates]
    feature_columns = [c for c in header if c not in label_columns]

    manifest = {
        "dataset": "ai4i_2020",
        "source_url": UCI_AI4I_ZIP,
        "uci_page": "https://archive.ics.uci.edu/dataset/601/ai4i+2020+predictive+maintenance+dataset",
        "csv_path": str(dest_csv.relative_to(root)).replace("\\", "/"),
        "n_rows": n_rows,
        "columns": header,
        "label_columns": label_columns,
        "feature_columns": feature_columns,
        "notes": "Use Machine failure as primary severity label; other columns are failure modes.",
    }
    write_json(out_dir / "manifest.json", manifest)
    print(f"Wrote {dest_csv} ({n_rows} rows)")
    print(f"Manifest: {out_dir / 'manifest.json'}")


if __name__ == "__main__":
    main()
