"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useCallback, useRef, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { apiBaseUrl } from "@/lib/api";
import { startAnalysisSession } from "@/lib/ingestFlow";

export default function UploadPage() {
  const router = useRouter();
  const [drag, setDrag] = useState(false);
  const [files, setFiles] = useState<File[]>([]);
  const [notes, setNotes] = useState("");
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const addFiles = useCallback((list: FileList | File[]) => {
    setFiles((prev) => {
      const next = [...prev];
      for (const f of Array.from(list)) next.push(f);
      return next;
    });
  }, []);

  const onDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDrag(false);
    if (e.dataTransfer.files?.length) addFiles(e.dataTransfer.files);
  };

  const submit = async () => {
    setErr(null);
    if (!notes.trim() && files.length === 0) {
      setErr("Add at least one file or worker notes.");
      return;
    }
    setBusy(true);
    try {
      const threadId = await startAnalysisSession({
        notes: notes || undefined,
        files: files.length > 0 ? files : undefined,
      });
      router.push(`/progress?thread_id=${encodeURIComponent(threadId)}`);
    } catch (e) {
      setErr(e instanceof Error ? e.message : "Upload failed");
    } finally {
      setBusy(false);
    }
  };

  return (
    <AppShell>
      <h1 className="text-3xl font-black tracking-tight text-ink">Upload workspace</h1>
      <p className="mt-2 text-ink/70">
        Creates a session, POSTs multipart to{" "}
        <span className="font-mono text-xs text-primary">{apiBaseUrl}/api/v1/ingest</span>, then
        opens progress.
      </p>

      {err && (
        <Card className="mt-6 border-red-200 bg-red-50/80 p-4">
          <p className="text-sm text-red-800">{err}</p>
        </Card>
      )}

      <Card className="mt-8 p-6">
        <label className="text-sm font-semibold text-ink">Worker notes (optional if files present)</label>
        <textarea
          className="mt-2 min-h-[100px] w-full rounded-xl border border-border bg-white p-3 text-sm text-ink"
          placeholder="e.g. Unusual vibration on spindle 2 after night shift…"
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
        />
      </Card>

      <Card
        className={`mt-6 border-dashed p-10 text-center transition ${drag ? "border-primary bg-primary/5" : ""}`}
        onDragEnter={() => setDrag(true)}
        onDragLeave={() => setDrag(false)}
        onDrop={onDrop}
        onDragOver={(e) => e.preventDefault()}
      >
        <p className="text-sm font-semibold text-ink">Drop inspection photos, PDFs, or CSV here</p>
        <p className="mt-2 text-xs text-ink/60">Or choose files — multiple selection allowed.</p>
        <input
          ref={inputRef}
          type="file"
          multiple
          className="hidden"
          onChange={(e) => {
            if (e.target.files?.length) addFiles(e.target.files);
            e.target.value = "";
          }}
        />
        <div className="mt-6 flex flex-wrap justify-center gap-2">
          <Badge tone="image">image</Badge>
          <Badge tone="pdf">pdf</Badge>
          <Badge tone="text">text</Badge>
          <Badge tone="sensor">sensor</Badge>
        </div>
        <div className="mt-6 flex flex-wrap justify-center gap-3">
          <Button type="button" variant="ghost" onClick={() => inputRef.current?.click()}>
            Choose files
          </Button>
        </div>
        {files.length > 0 && (
          <ul className="mt-6 max-h-40 overflow-auto text-left text-xs text-ink/80">
            {files.map((f) => (
              <li key={`${f.name}-${f.size}`} className="border-b border-border/50 py-1 font-mono">
                {f.name} ({Math.round(f.size / 1024)} KB)
              </li>
            ))}
          </ul>
        )}
      </Card>

      <div className="mt-8 flex flex-wrap gap-3">
        <Button type="button" disabled={busy} onClick={() => void submit()}>
          {busy ? "Running pipeline…" : "Run analysis"}
        </Button>
        <Link
          href="/progress"
          className={`inline-flex items-center justify-center rounded-pill border border-border bg-white px-5 py-2.5 text-sm font-semibold text-ink transition hover:bg-surface focus:outline-none focus:ring-2 focus:ring-primary/40 ${busy ? "pointer-events-none opacity-50" : ""}`}
        >
          Open progress (saved thread)
        </Link>
      </div>
    </AppShell>
  );
}
