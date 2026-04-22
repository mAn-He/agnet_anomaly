import { AppShell } from "@/components/AppShell";
import { Card } from "@/components/ui/Card";

export default function EvidencePage() {
  return (
    <AppShell>
      <h1 className="text-3xl font-black tracking-tight text-ink">Intermediate evidence</h1>
      <div className="mt-8 grid gap-6 lg:grid-cols-2">
        <Card className="p-6">
          <p className="text-sm font-bold text-primary">Anomaly heatmap</p>
          <p className="mt-2 text-sm text-ink/70">
            Viewer for anomalib PatchCore maps (Phase 2+). Placeholder panel.
          </p>
          <div className="mt-4 h-40 rounded-xl border border-dashed border-border bg-primary/5" />
        </Card>
        <Card className="p-6">
          <p className="text-sm font-bold text-primary">Checklist fields</p>
          <p className="mt-2 text-sm text-ink/70">OCR / FUNSD-style field table from graph state.</p>
        </Card>
      </div>
    </AppShell>
  );
}
