# Datasets

Module benchmarks are **not** a single end-to-end dataset. Use **separate** corpora per submodule, plus a **small curated integration set** under `data/integration_cases/`.

## Vision anomaly

- **MVTec AD** — [https://www.mvtec.com/research-teaching/datasets/mvtec-ad](https://www.mvtec.com/research-teaching/datasets/mvtec-ad)
- **VisA** — [https://registry.opendata.aws/visa/](https://registry.opendata.aws/visa/)

Preparation (run from repository root):

```bash
python backend/scripts/prepare_mvtec.py --source "D:/datasets/mvtec_ad"
python backend/scripts/prepare_visa.py --source "D:/datasets/visa"
```

Scripts write manifests under `data/processed/benchmarks/*/manifest.json` (paths stay on your machine; MVTec/VisA are not redistributed here).

## Tabular triage

- **AI4I 2020 Predictive Maintenance** — [https://archive.ics.uci.edu/dataset/601/ai4i+2020+predictive+maintenance+dataset](https://archive.ics.uci.edu/dataset/601/ai4i+2020+predictive+maintenance+dataset)

Download + manifest:

```bash
python backend/scripts/prepare_ai4i.py
# reuse cache:
python backend/scripts/prepare_ai4i.py --skip-download
```

Outputs: `data/processed/ai4i/*.csv` and `manifest.json`.

## Document / form parsing

- **FUNSD** — [https://guillaumejaume.github.io/FUNSD/](https://guillaumejaume.github.io/FUNSD/)
- Custom manufacturing checklists: place PDFs/images under `data/raw/custom_checklists/` and annotate per [`data/integration_cases/schema.json`](../data/integration_cases/schema.json).

After downloading the corpus from the official page, point at a local extract or zip:

```bash
python backend/scripts/prepare_funsd.py --source path/to/funsd_extracted
python backend/scripts/prepare_funsd.py --zip path/to/funsd.zip
```

The script searches for ``training_data/images`` and ``training_data/annotations``.

## Integration scenarios

Define 20–30 (or fewer for MVP) scenarios with images, optional forms, notes, tabular features, and expected fields/severity/sections/citations. Schema: `data/integration_cases/schema.json`.
