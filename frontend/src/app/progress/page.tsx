"use client";

import { useSearchParams } from "next/navigation";
import { Suspense, useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { PipelineProgressClient } from "@/components/PipelineProgressClient";
import { getThreadId, setThreadId as saveThreadId } from "@/lib/session";

function ProgressInner() {
  const sp = useSearchParams();
  const qThread = sp.get("thread_id");
  const [threadId, setThreadId] = useState<string | null>(null);

  useEffect(() => {
    if (qThread) {
      saveThreadId(qThread);
      setThreadId(qThread);
      return;
    }
    setThreadId(getThreadId());
  }, [qThread]);

  return (
    <>
      <h1 className="text-3xl font-black tracking-tight text-ink">Pipeline progress</h1>
      <p className="mt-2 max-w-2xl text-ink/70">
        Polls the LangGraph checkpoint every 2s. Run the API on port 8000 with{" "}
        <code className="rounded bg-ink/5 px-1">NEXT_PUBLIC_API_URL</code> if needed.
      </p>
      <div className="mt-8">
        <PipelineProgressClient threadId={threadId} />
      </div>
    </>
  );
}

export default function ProgressPage() {
  return (
    <AppShell>
      <Suspense
        fallback={<p className="text-sm text-ink/60">Loading…</p>}
      >
        <ProgressInner />
      </Suspense>
    </AppShell>
  );
}
