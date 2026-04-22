"use client";

import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { getGraphState } from "@/lib/api";
import { getThreadId } from "@/lib/session";

const LOCAL_EDIT_KEY = "fieldops_report_markdown_override";

export default function ReportPage() {
  const [threadId, setThreadId] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [markdown, setMarkdown] = useState("");
  const [copied, setCopied] = useState(false);

  const load = useCallback(async (opts?: { preferApi?: boolean }) => {
    const tid = getThreadId();
    setThreadId(tid);
    if (!tid) {
      setLoading(false);
      setMarkdown("");
      return;
    }
    try {
      const s = await getGraphState(tid);
      const fromApi =
        typeof s.final_export_markdown === "string" ? s.final_export_markdown : "";
      const local =
        typeof window !== "undefined" ? localStorage.getItem(LOCAL_EDIT_KEY) : null;
      if (!opts?.preferApi && local?.trim()) setMarkdown(local);
      else {
        setMarkdown(fromApi);
        if (opts?.preferApi) localStorage.setItem(LOCAL_EDIT_KEY, fromApi);
      }
      setError(null);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load report");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void load();
  }, [load]);

  useEffect(() => {
    if (!markdown) return;
    const t = setTimeout(() => localStorage.setItem(LOCAL_EDIT_KEY, markdown), 400);
    return () => clearTimeout(t);
  }, [markdown]);

  const copy = async () => {
    await navigator.clipboard.writeText(markdown);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const resetFromServer = () => {
    localStorage.removeItem(LOCAL_EDIT_KEY);
    setLoading(true);
    void load({ preferApi: true });
  };

  return (
    <AppShell>
      <h1 className="text-3xl font-black tracking-tight text-ink">Draft report editor</h1>
      <p className="mt-2 text-ink/70">
        Loads <code className="rounded bg-ink/5 px-1">final_export_markdown</code> from the API.
        Edits autosave to localStorage (MVP — no PATCH endpoint yet).
      </p>

      {!threadId && !loading && (
        <Card className="mt-6 p-4">
          <p className="text-sm text-ink/70">No thread in session. Upload first.</p>
          <Link
            href="/upload"
            className="mt-3 inline-flex items-center justify-center rounded-pill bg-primary px-5 py-2.5 text-sm font-semibold text-white shadow-card hover:brightness-110"
          >
            Go to upload
          </Link>
        </Card>
      )}

      {error && (
        <Card className="mt-6 border-red-200 bg-red-50/80 p-4">
          <p className="text-sm text-red-800">{error}</p>
        </Card>
      )}

      {threadId && (
        <Card className="mt-8 p-6">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <p className="font-mono text-xs text-ink/60">{threadId}</p>
            <div className="flex flex-wrap gap-2">
              <Button type="button" variant="ghost" onClick={() => void load({ preferApi: true })}>
                Reload from API
              </Button>
              <Button type="button" variant="ghost" onClick={resetFromServer}>
                Discard local edits
              </Button>
              <Button type="button" onClick={() => void copy()}>
                {copied ? "Copied" : "Copy Markdown"}
              </Button>
              <Link
                href="/export"
                className="inline-flex items-center justify-center rounded-pill border border-border bg-white px-5 py-2.5 text-sm font-semibold text-ink hover:bg-surface"
              >
                Export page
              </Link>
            </div>
          </div>
          <textarea
            className="mt-4 min-h-[420px] w-full rounded-xl border border-border bg-white p-4 font-mono text-sm leading-relaxed text-ink"
            placeholder={loading ? "Loading…" : "Markdown report…"}
            value={markdown}
            onChange={(e) => setMarkdown(e.target.value)}
            disabled={loading}
          />
        </Card>
      )}
    </AppShell>
  );
}
