import { AppShell } from "@/components/AppShell";
import { Card } from "@/components/ui/Card";

export default function EvalPage() {
  return (
    <AppShell>
      <h1 className="text-3xl font-black tracking-tight text-ink">Evaluation dashboard</h1>
      <p className="mt-2 text-ink/70">
        Module benchmarks vs integration cases — metrics wired in Phase 6 (`backend/scripts/eval_*.py`).
      </p>
      <div className="mt-8 grid gap-4 sm:grid-cols-2">
        {["OCR", "Anomaly", "Triage", "Retrieval", "Report", "E2E"].map((m) => (
          <Card key={m} className="p-5">
            <p className="text-sm font-bold text-primary">{m}</p>
            <p className="mt-2 text-xs text-ink/60">Awaiting dataset + metric hooks.</p>
          </Card>
        ))}
      </div>
    </AppShell>
  );
}
