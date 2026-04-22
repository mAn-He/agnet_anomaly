# Evaluation

Phase 6 adds metric implementations. CLI entry points (stubs in Phase 1):

| Script | Metrics (target) |
|--------|-------------------|
| `backend/scripts/eval_ocr.py` | Field extraction accuracy, completeness |
| `backend/scripts/eval_anomaly.py` | Image-level AUROC, localization where applicable |
| `backend/scripts/eval_triage.py` | Accuracy, F1, precision/recall, imbalance handling |
| `backend/scripts/eval_retrieval.py` | Recall@k, MRR, citation support |
| `backend/scripts/eval_report.py` | Section completeness, citation rate, unsupported claims |
| `backend/scripts/eval_end_to_end.py` | Completion rate, latency, approval rate |

Run from repo root (after `pip install -e ".[dev]"`):

```bash
python backend/scripts/eval_ocr.py --help
```

Stubs print “not implemented” until datasets and model paths are configured.

Rationale on RAG vs fine-tuning: [IBM — RAG vs fine-tuning](https://www.ibm.com/think/topics/rag-vs-fine-tuning).
