# FieldOps Copilot

Manufacturing-focused multimodal workflow for inspection report automation: LangGraph orchestration, RAG, and a Next.js GUI (MVP Phase 1 scaffold).

## Prerequisites

- Python 3.11+
- Node.js 20+ (for the frontend)

## Backend

From the repository root:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
```

Run the API (working directory must be `backend` so imports resolve as `app`):

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

- API docs: [http://localhost:8000/docs](http://localhost:8000/docs)
- Optional: set `FIELDOPS_DATA_DIR` to an absolute path for uploaded files (default: repository `data/`).

## Frontend

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000). Set `NEXT_PUBLIC_API_URL=http://localhost:8000` if the API runs elsewhere.

## Tests

```bash
pip install -e ".[dev]"
pytest backend/tests
```

## Dataset preparation (MVP)

From the repository root (requires network for AI4I / FUNSD):

```bash
python backend/scripts/prepare_ai4i.py
python backend/scripts/prepare_funsd.py --zip path/to/funsd.zip
python backend/scripts/prepare_mvtec.py --source /path/to/mvtec_ad
```

See [docs/datasets.md](docs/datasets.md).

## Evaluation stubs (Phase 6)

```bash
python backend/scripts/eval_ocr.py --help
```

## Push to GitHub

1. Create an **empty** repository on GitHub (no README, no .gitignore) and copy the HTTPS or SSH URL.
2. In this folder:

```bash
git remote add origin https://github.com/YOUR_USER/YOUR_REPO.git
git push -u origin main
```

If the default branch is `master` on the remote, use: `git push -u origin main:main` or rename as needed.

Large paths are ignored (see `.gitignore`: `data/mvtec/`, `data/**/*.zip`, `node_modules/`, etc.).

## Documentation

See [docs/architecture.md](docs/architecture.md) for system design and memory layers.
