"""Validate local MVTec AD tree and write a benchmark manifest (no redistribution).

Download the dataset from the official MVTec site, extract locally, then point --source
at the root folder that contains category subdirectories (e.g. bottle, cable, ...).

Official: https://www.mvtec.com/research-teaching/datasets/mvtec-ad
"""

from __future__ import annotations

import argparse
from pathlib import Path

from _data_prep_utils import repo_root_from_script, resolve_under_repo, write_json


def _is_mvtec_category(cat_dir: Path) -> bool:
    train_good = cat_dir / "train" / "good"
    test_dir = cat_dir / "test"
    return train_good.is_dir() and test_dir.is_dir()


def main() -> None:
    parser = argparse.ArgumentParser(description="Index local MVTec AD for training/eval.")
    parser.add_argument(
        "--source",
        type=Path,
        required=True,
        help="Path to MVTec AD root (folder containing category subdirs).",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="Repository root (default: infer from script location).",
    )
    parser.add_argument(
        "--output-dir",
        default="data/processed/benchmarks/mvtec_ad",
        help="Relative to repo root; manifest.json written here.",
    )
    args = parser.parse_args()

    root = args.repo_root or repo_root_from_script(__file__)
    out_dir = resolve_under_repo(root, args.output_dir)
    src = args.source.resolve()
    if not src.is_dir():
        raise SystemExit(f"--source is not a directory: {src}")

    categories: list[dict] = []
    for child in sorted(src.iterdir()):
        if not child.is_dir() or child.name.startswith("."):
            continue
        if not _is_mvtec_category(child):
            continue
        train_good = child / "train" / "good"
        test_root = child / "test"
        test_subdirs = [p.name for p in test_root.iterdir() if p.is_dir()]
        n_train_good = len(list(train_good.glob("*.png"))) + len(list(train_good.glob("*.bmp")))
        categories.append(
            {
                "name": child.name,
                "path": str(child),
                "n_train_good_images": n_train_good,
                "test_splits": sorted(test_subdirs),
            }
        )

    if not categories:
        raise SystemExit(
            f"No MVTec-like categories found under {src}. "
            "Expected layout: <category>/train/good and <category>/test/*."
        )

    manifest = {
        "dataset": "mvtec_ad",
        "source_root": str(src),
        "official": "https://www.mvtec.com/research-teaching/datasets/mvtec-ad",
        "n_categories": len(categories),
        "categories": categories,
        "notes": "Paths are absolute on this machine; use for local anomalib/PatchCore baselines.",
    }
    write_json(out_dir / "manifest.json", manifest)
    print(f"Indexed {len(categories)} categories → {out_dir / 'manifest.json'}")


if __name__ == "__main__":
    main()
