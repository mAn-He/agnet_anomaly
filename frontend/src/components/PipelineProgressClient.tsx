"use client";

import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import { getGraphState } from "@/lib/api";
import { MILESTONES, stepRank } from "@/lib/pipeline";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";

type Props = { threadId: string | null };

export function PipelineProgressClient({ threadId }: Props) {
  const [step, setStep] = useState<string | null>(null);
  const [maxRank, setMaxRank] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [modalities, setModalities] = useState<string[]>([]);
  const [done, setDone] = useState(false);

  const poll = useCallback(async () => {
    if (!threadId) return;
    try {
      const s = await getGraphState(threadId);
      const ps = typeof s.pipeline_step === "string" ? s.pipeline_step : null;
      setStep(ps);
      const r = stepRank(ps ?? undefined);
      if (r >= 0) setMaxRank((m) => Math.max(m, r));
      setModalities(Array.isArray(s.modalities_present) ? (s.modalities_present as string[]) : []);
      setDone(Boolean(s.final_export_markdown));
      setError(null);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load state");
    }
  }, [threadId]);

  useEffect(() => {
    if (!threadId) return;
    void poll();
    const t = setInterval(poll, 2000);
    return () => clearInterval(t);
  }, [threadId, poll]);

  const finalRank = stepRank("final_export");
  const pct = finalRank > 0 ? Math.min(100, Math.round((maxRank / finalRank) * 100)) : 0;

  if (!threadId) {
    return (
      <Card className="p-6">
        <p className="text-sm text-ink/70">No active thread. Start from Upload.</p>
        <Link
          href="/upload"
          className="mt-4 inline-flex items-center justify-center rounded-pill bg-primary px-5 py-2.5 text-sm font-semibold text-white shadow-card hover:brightness-110"
        >
          Go to upload
        </Link>
      </Card>
    );
  }

  return (
    <div className="space-y-8">
      {error && (
        <Card className="border-red-200 bg-red-50/80 p-4">
          <p className="text-sm font-semibold text-red-800">API error</p>
          <p className="mt-1 text-xs text-red-700">{error}</p>
        </Card>
      )}

      <Card className="p-6">
        <div className="flex flex-wrap items-end justify-between gap-4">
          <div>
            <p className="text-xs font-bold uppercase tracking-wider text-primary">Thread</p>
            <p className="mt-1 font-mono text-sm text-ink">{threadId}</p>
          </div>
          {modalities.length > 0 && (
            <div>
              <p className="text-xs font-bold text-ink/50">Modalities</p>
              <p className="mt-1 text-sm text-ink">{modalities.join(", ")}</p>
            </div>
          )}
        </div>
        <div className="mt-6">
          <div className="flex justify-between text-xs font-semibold text-ink/60">
            <span>Progress</span>
            <span>{pct}%</span>
          </div>
          <div className="mt-2 h-3 overflow-hidden rounded-pill bg-border/60">
            <div
              className="h-full rounded-pill bg-gradient-to-r from-primary to-cyan transition-all duration-500"
              style={{ width: `${pct}%` }}
            />
          </div>
        </div>
        <p className="mt-4 font-mono text-xs text-ink/80">
          Last step: <span className="text-primary">{step ?? "—"}</span>
        </p>
      </Card>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
        {MILESTONES.map((m, i) => {
          const endR = stepRank(m.endStep);
          const prevEndR = i === 0 ? -1 : stepRank(MILESTONES[i - 1].endStep);
          const completed = maxRank >= endR;
          const active = !completed && maxRank > prevEndR && maxRank <= endR;
          return (
            <Card
              key={m.id}
              className={`p-4 transition ${
                completed
                  ? "border-primary/40 bg-primary/5"
                  : active
                    ? "border-cyan/50 bg-cyan/5 ring-2 ring-cyan/20"
                    : ""
              }`}
            >
              <p className="text-xs font-bold text-primary">{String(i + 1).padStart(2, "0")}</p>
              <p className="mt-2 text-sm font-semibold text-ink">{m.label}</p>
              <p className="mt-1 text-xs text-ink/55">
                {completed ? "Done" : active ? "Running…" : "Pending"}
              </p>
            </Card>
          );
        })}
      </div>

      <div className="flex flex-wrap gap-3">
        <Button type="button" onClick={() => void poll()}>
          Refresh now
        </Button>
        {done && (
          <Link
            href="/report"
            className="inline-flex items-center justify-center rounded-pill bg-primary px-5 py-2.5 text-sm font-semibold text-white shadow-card transition hover:brightness-110 focus:outline-none focus:ring-2 focus:ring-primary/40"
          >
            Open report editor
          </Link>
        )}
      </div>
    </div>
  );
}
