"""RAG retrieval evaluation (implement metrics in Phase 6)."""

from __future__ import annotations

import argparse


def main() -> None:
    p = argparse.ArgumentParser(description="Evaluate retrieval quality.")
    p.add_argument("--queries", default="data/benchmarks/rag_queries.jsonl")
    args = p.parse_args()
    print("[stub] eval_retrieval — not implemented.")
    print(f"  queries={args.queries}")


if __name__ == "__main__":
    main()
