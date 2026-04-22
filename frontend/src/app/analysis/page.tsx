import { AppShell } from "@/components/AppShell";
import { Card } from "@/components/ui/Card";

export default function AnalysisPage() {
  return (
    <AppShell>
      <h1 className="text-3xl font-black tracking-tight text-ink">New analysis</h1>
      <p className="mt-2 max-w-2xl text-ink/70">
        Configure line metadata and analysis presets (Phase 1 placeholder). Wire to backend
        session API in Phase 5.
      </p>
      <Card className="mt-8 p-6">
        <p className="text-sm font-semibold text-primary">Session</p>
        <p className="mt-2 text-sm text-ink/75">POST /api/v1/sessions creates a thread_id.</p>
      </Card>
    </AppShell>
  );
}
