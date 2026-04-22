"use client";

import { useCallback, useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { getGraphState } from "@/lib/api";
import { getThreadId } from "@/lib/session";

const LOCAL_EDIT_KEY = "fieldops_report_markdown_override";

function downloadBlob(filename: string, text: string) {
  const blob = new Blob([text], { type: "text/markdown;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}

export default function ExportPage() {
  const [text, setText] = useState("");
  const [busy, setBusy] = useState(false);

  const load = useCallback(async () => {
    const tid = getThreadId();
    const local = localStorage.getItem(LOCAL_EDIT_KEY);
    if (local?.trim()) {
      setText(local);
      return;
    }
    if (!tid) {
      setText("");
      return;
    }
    setBusy(true);
    try {
      const s = await getGraphState(tid);
      setText(typeof s.final_export_markdown === "string" ? s.final_export_markdown : "");
    } finally {
      setBusy(false);
    }
  }, []);

  useEffect(() => {
    void load();
  }, [load]);

  return (
    <AppShell>
      <h1 className="text-3xl font-black tracking-tight text-ink">Approval & export</h1>
      <Card className="mt-8 p-6">
        <p className="text-sm text-ink/70">
          Uses editor local draft if present, otherwise{" "}
          <code className="rounded bg-ink/5 px-1">final_export_markdown</code> from the API.
        </p>
        <div className="mt-6 flex flex-wrap gap-3">
          <Button type="button" disabled={!text || busy} onClick={() => downloadBlob("fieldops-report.md", text)}>
            Download Markdown
          </Button>
          <Button type="button" variant="ghost" disabled={busy} onClick={() => void load()}>
            Refresh
          </Button>
        </div>
      </Card>
    </AppShell>
  );
}
