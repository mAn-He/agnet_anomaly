/**
 * Shared “start analysis” flow: session + ingest, persist thread.
 * Home / Upload UIs call this, then navigate to /progress?thread_id=…
 */
import { createSession, ingestFiles } from "@/lib/api";
import { setThreadId } from "@/lib/session";

export type StartAnalysisOptions = {
  notes?: string;
  files?: File[];
  projectId?: string;
};

export async function startAnalysisSession(opts: StartAnalysisOptions): Promise<string> {
  const session = await createSession();
  setThreadId(session.thread_id);
  await ingestFiles(session.thread_id, {
    notes: opts.notes,
    files: opts.files,
    projectId: opts.projectId,
  });
  return session.thread_id;
}
