import { AppShell } from "@/components/AppShell";
import { Card } from "@/components/ui/Card";

export default function ReviewPage() {
  return (
    <AppShell>
      <h1 className="text-3xl font-black tracking-tight text-ink">Reviewer findings</h1>
      <div className="mt-8 grid gap-6 lg:grid-cols-2">
        <Card className="p-6">
          <p className="text-sm font-bold text-primary">Rule checker</p>
          <ul className="mt-3 list-disc space-y-1 pl-5 text-sm text-ink/80">
            <li>Required sections / placeholders</li>
            <li>Equipment ID / date presence</li>
            <li>Citation presence</li>
          </ul>
        </Card>
        <Card className="p-6">
          <p className="text-sm font-bold text-primary">Reviewer agent</p>
          <ul className="mt-3 list-disc space-y-1 pl-5 text-sm text-ink/80">
            <li>Hallucination risk heuristic</li>
            <li>Unsupported claims vs retrieved SOP</li>
            <li>Tone / actionability</li>
          </ul>
        </Card>
      </div>
    </AppShell>
  );
}
