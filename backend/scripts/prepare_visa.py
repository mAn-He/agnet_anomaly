"""Validate local VisA anomaly layout and write a manifest (no redistribution).

VisA is commonly distributed as image folders per category. After you obtain the data
(AWS Open Data / project instructions), point --source at the root that contains category
folders with train/test splits (or adjust --layout).

Registry: https://registry.opendata.aws/visa/
"""

from __future__ import annotations

import argparse
from pathlib import Path

from _data_prep_utils import repo_root_from_script, resolve_under_repo, write_json


def _count_images(d: Path) -> int:
    if not d.is_dir():
        return 0
    exts = {".png", ".jpg", ".jpeg", ".bmp"}
    return sum(1 for p in d.rglob("*") if p.suffix.lower() in exts)


def _visa_category_score(cat_dir: Path) -> tuple[bool, str]:
    """Heuristic: category has train/ and test/ with images."""
    tr = cat_dir / "train"
    te = cat_dir / "test"
    if tr.is_dir() and te.is_dir():
        return True, "train_test"
    # Some releases use Data/ClassName/Train|Test
    return False, "unknown"


def main() -> None:
    parser = argparse.ArgumentParser(description="Index local VisA dataset tree.")
    parser.add_argument(
        "--source",
        type=Path,
        required=True,
        help="Path to VisA root (folder of categories or release root).",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
    )
    parser.add_argument(
        "--output-dir",
        default="data/processed/benchmarks/visa",
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
        ok, layout = _visa_category_score(child)
        if not ok:
            continue
        categories.append(
            {
                "name": child.name,
                "path": str(child),
                "layout": layout,
                "n_train_images": _count_images(child / "train"),
                "n_test_images": _count_images(child / "test"),
            }
        )

    if not categories:
        # Fallback: single-level release with nested `split_csv` etc. — report shallow scan
        categories.append(
            {
                "name": "_root",
                "path": str(src),
                "layout": "fallback_root",
                "n_images_total": _count_images(src),
                "hint": "No train/test per category found; inspect layout manually.",
            }
        )

    manifest = {
        "dataset": "visa",
        "source_root": str(src),
        "registry": "https://registry.opendata.aws/visa/",
        "n_categories": len(categories),
        "categories": categories,
        "notes": "MVP heuristic indexing; adjust tooling if your tarball layout differs.",
    }
    write_json(out_dir / "manifest.json", manifest)
    print(f"Wrote {out_dir / 'manifest.json'}")


if __name__ == "__main__":
    main()
