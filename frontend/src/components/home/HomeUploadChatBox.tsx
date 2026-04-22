"use client";

import { useRouter } from "next/navigation";
import { useCallback, useRef, useState, type KeyboardEvent } from "react";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { startAnalysisSession } from "@/lib/ingestFlow";

const PLACEHOLDER =
  "점검 사진, 체크리스트, 센서 로그를 올리고 보고서 생성을 요청해보세요";

/** Accept: images, PDF, CSV, TXT (matches backend multimodal use cases) */
const FILE_ACCEPT =
  "image/*,.pdf,.csv,.txt,application/pdf,text/csv,text/plain" as const;

function toneForFile(name: string): "image" | "pdf" | "text" | "sensor" | "default" {
  const n = name.toLowerCase();
  if (/\.(png|jpg|jpeg|webp|gif|bmp|tif|tiff)$/.test(n)) return "image";
  if (n.endsWith(".pdf")) return "pdf";
  if (n.endsWith(".csv")) return "sensor";
  if (n.endsWith(".txt")) return "text";
  return "default";
}

/**
 * Home chat-style composer: text + file chips + send.
 * Wires to existing ingest API via startAnalysisSession → /progress
 */
export function HomeUploadChatBox() {
  const router = useRouter();
  const [text, setText] = useState("");
  const [files, setFiles] = useState<File[]>([]);
  const [drag, setDrag] = useState(false);
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const canSubmit = (text.trim().length > 0 || files.length > 0) && !busy;

  const addFiles = useCallback((list: FileList | File[]) => {
    setFiles((prev) => {
      const next = [...prev];
      for (const f of Array.from(list)) next.push(f);
      return next;
    });
  }, []);

  const removeFile = (idx: number) => {
    setFiles((prev) => prev.filter((_, i) => i !== idx));
  };

  const submit = useCallback(async () => {
    setErr(null);
    if (!text.trim() && files.length === 0) {
      setErr("메시지를 입력하거나 파일을 첨부해주세요.");
      return;
    }
    setBusy(true);
    try {
      const threadId = await startAnalysisSession({
        notes: text.trim() || undefined,
        files: files.length > 0 ? files : undefined,
      });
      router.push(`/progress?thread_id=${encodeURIComponent(threadId)}`);
    } catch (e) {
      setErr(e instanceof Error ? e.message : "요청에 실패했습니다.");
    } finally {
      setBusy(false);
    }
  }, [text, files, router]);

  const onTextKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      if (canSubmit) void submit();
    }
  };

  return (
    <div
      className="home-input-shell relative overflow-hidden rounded-3xl border border-border/90 bg-surface/95 p-1 shadow-card ring-1 ring-primary/5 transition focus-within:ring-2 focus-within:ring-primary/20"
    >
      <div
        className={`rounded-[1.4rem] transition ${drag ? "bg-primary/5" : "bg-gradient-to-b from-white to-primary/[0.02]"}`}
        onDragEnter={() => setDrag(true)}
        onDragLeave={() => setDrag(false)}
        onDragOver={(e) => e.preventDefault()}
        onDrop={(e) => {
          e.preventDefault();
          setDrag(false);
          if (e.dataTransfer.files?.length) addFiles(e.dataTransfer.files);
        }}
      >
        {files.length > 0 && (
          <ul className="flex flex-wrap gap-2 border-b border-border/60 px-4 pb-3 pt-4 sm:px-5">
            {files.map((f, i) => (
              <li
                key={`${f.name}-${f.size}-${i}`}
                className="group inline-flex items-center gap-1.5 rounded-pill border border-border bg-white/90 py-1 pl-2.5 pr-1 text-xs shadow-sm"
              >
                <Badge tone={toneForFile(f.name)}>{f.name.split(".").pop()}</Badge>
                <span className="max-w-[10rem] truncate font-mono text-ink/80" title={f.name}>
                  {f.name}
                </span>
                <button
                  type="button"
                  onClick={() => removeFile(i)}
                  className="ml-0.5 rounded-pill p-1 text-ink/40 hover:bg-red-50 hover:text-red-600"
                  aria-label={`첨부 제거: ${f.name}`}
                >
                  <span className="sr-only">Remove</span>×
                </button>
              </li>
            ))}
          </ul>
        )}

        <label htmlFor="home-chat-text" className="sr-only">
          보고서 요청 메시지
        </label>
        <textarea
          id="home-chat-text"
          rows={4}
          className="w-full resize-y rounded-2xl border-0 bg-transparent px-4 py-3 text-sm leading-relaxed text-ink placeholder:text-ink/40 focus:outline-none focus:ring-0 sm:px-5 sm:py-4 sm:text-[15px]"
          placeholder={PLACEHOLDER}
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={onTextKeyDown}
        />

        <div className="flex flex-wrap items-center justify-between gap-3 border-t border-border/60 px-3 py-3 sm:px-4">
          <div className="flex flex-wrap items-center gap-2">
            <input
              ref={fileInputRef}
              type="file"
              className="sr-only"
              accept={FILE_ACCEPT}
              multiple
              onChange={(e) => {
                if (e.target.files?.length) addFiles(e.target.files);
                e.target.value = "";
              }}
            />
            <button
              type="button"
              onClick={() => fileInputRef.current?.click()}
              className="inline-flex items-center gap-1.5 rounded-pill border border-border bg-white px-3 py-2 text-xs font-semibold text-ink/80 shadow-sm transition hover:border-primary/40 hover:bg-primary/5 hover:text-primary focus:outline-none focus:ring-2 focus:ring-primary/30"
              aria-label="파일 첨부"
            >
              <span className="text-base leading-none" aria-hidden>
                +
              </span>
              파일
            </button>
            <p className="text-[10px] text-ink/45 sm:text-xs">Shift+Enter 줄바꿈 · Enter 전송</p>
          </div>
          <Button
            type="button"
            disabled={!canSubmit}
            onClick={() => void submit()}
            className="min-w-[7rem] shadow-md"
            aria-label="보고서 분석 시작"
          >
            {busy ? "처리 중…" : "보고서 시작"}
          </Button>
        </div>
      </div>

      {err && (
        <p className="px-4 pb-3 text-xs font-medium text-red-600" role="alert">
          {err}
        </p>
      )}

      {/* Future: stream chat / follow-up; today startAnalysisSession + progress */}
    </div>
  );
}
