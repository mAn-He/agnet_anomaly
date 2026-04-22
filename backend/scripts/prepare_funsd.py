"""Stage FUNSD for OCR / layout baselines (local zip or folder — official hosts vary).

Official: https://guillaumejaume.github.io/FUNSD/

The upstream GitHub `FUNSD` default branch is a Jekyll site, not the image corpus. For MVP,
download the dataset archive from the official page (or your mirror), then pass ``--zip`` or
an extracted tree via ``--source``.
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from _data_prep_utils import (
    extract_zip,
    repo_root_from_script,
    resolve_under_repo,
    write_json,
)


def find_training_data_root(search_under: Path) -> Path:
    """Locate ``training_data`` with ``images/`` and ``annotations/``."""
    if (search_under / "training_data").is_dir():
        td = search_under / "training_data"
        if (td / "images").is_dir() and (td / "annotations").is_dir():
            return td
    for td in search_under.rglob("training_data"):
        if td.is_dir() and (td / "images").is_dir() and (td / "annotations").is_dir():
            return td
    raise FileNotFoundError(
        f"Could not find training_data/{{images,annotations}} under {search_under}. "
        "Unpack the official FUNSD download and retry."
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Index FUNSD training_data for eval.")
    parser.add_argument("--repo-root", type=Path, default=None)
    parser.add_argument(
        "--source",
        type=Path,
        default=None,
        help="Extracted FUNSD root (folder that contains training_data or is training_data's parent).",
    )
    parser.add_argument(
        "--zip",
        type=Path,
        default=None,
        help="Local .zip from the official FUNSD download page; extracted under --raw-dir.",
    )
    parser.add_argument(
        "--raw-dir",
        default="data/raw/funsd",
        help="Relative to repo root; used when --zip is set.",
    )
    parser.add_argument(
        "--output-dir",
        default="data/processed/benchmarks/funsd",
    )
    args = parser.parse_args()

    if not args.source and not args.zip:
        parser.error("Provide --source (extracted tree) or --zip (local archive).")

    root = args.repo_root or repo_root_from_script(__file__)
    out_dir = resolve_under_repo(root, args.output_dir)

    if args.zip:
        raw_dir = resolve_under_repo(root, args.raw_dir)
        zip_path = args.zip.resolve()
        if not zip_path.is_file():
            raise SystemExit(f"--zip not found: {zip_path}")
        extract_dir = raw_dir / "extracted_from_zip"
        if extract_dir.exists():
            shutil.rmtree(extract_dir)
        extract_dir.mkdir(parents=True, exist_ok=True)
        extract_zip(zip_path, extract_dir)
        td_root = find_training_data_root(extract_dir)
    else:
        src = args.source.resolve()
        if not src.is_dir():
            raise SystemExit(f"--source is not a directory: {src}")
        td_root = find_training_data_root(src)

    images_dir = td_root / "images"
    ann_dir = td_root / "annotations"

    image_paths = sorted(
        p for p in images_dir.rglob("*") if p.suffix.lower() in {".png", ".jpg", ".jpeg"}
    )
    ann_paths = sorted(p for p in ann_dir.rglob("*.json"))

    manifest = {
        "dataset": "funsd",
        "homepage": "https://guillaumejaume.github.io/FUNSD/",
        "training_data_root": str(td_root).replace("\\", "/"),
        "n_images": len(image_paths),
        "n_annotations": len(ann_paths),
        "sample_images": [str(p).replace("\\", "/") for p in image_paths[:5]],
        "sample_annotations": [str(p).replace("\\", "/") for p in ann_paths[:5]],
        "notes": "Paths are absolute/local. Use for OCR / form field extraction benchmarks.",
    }
    write_json(out_dir / "manifest.json", manifest)
    print(f"training_data={td_root}")
    print(f"Wrote {out_dir / 'manifest.json'} ({len(image_paths)} images)")


if __name__ == "__main__":
    main()
