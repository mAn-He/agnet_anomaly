const base = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export async function apiPost<T>(path: string, body?: unknown): Promise<T> {
  const r = await fetch(`${base}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });
  if (!r.ok) {
    const t = await r.text();
    throw new Error(t || r.statusText);
  }
  return r.json() as Promise<T>;
}

export async function apiGet<T>(path: string): Promise<T> {
  const r = await fetch(`${base}${path}`, { cache: "no-store" });
  if (!r.ok) {
    const t = await r.text();
    throw new Error(t || r.statusText);
  }
  return r.json() as Promise<T>;
}

export type SessionResponse = { thread_id: string; project_id: string };

export async function createSession(): Promise<SessionResponse> {
  return apiPost<SessionResponse>("/api/v1/sessions");
}

export type IngestResponse = {
  thread_id: string;
  run_id: string;
  artifacts_saved: number;
  message?: string;
};

export async function ingestFiles(
  threadId: string,
  opts: { notes?: string; files?: File[]; projectId?: string },
): Promise<IngestResponse> {
  const fd = new FormData();
  fd.append("thread_id", threadId);
  fd.append("project_id", opts.projectId ?? "default");
  if (opts.notes?.trim()) fd.append("notes", opts.notes.trim());
  for (const f of opts.files ?? []) fd.append("files", f);

  const r = await fetch(`${base}/api/v1/ingest`, { method: "POST", body: fd });
  if (!r.ok) {
    const t = await r.text();
    throw new Error(t || r.statusText);
  }
  return r.json() as Promise<IngestResponse>;
}

export type GraphState = Record<string, unknown>;

export async function getGraphState(threadId: string): Promise<GraphState> {
  return apiGet<GraphState>(`/api/v1/graph/state/${encodeURIComponent(threadId)}`);
}

export async function healthCheck(): Promise<{ status: string }> {
  return apiGet<{ status: string }>("/health");
}

export { base as apiBaseUrl };
