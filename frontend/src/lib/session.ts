/** Browser session for current LangGraph thread (MVP: sessionStorage). */

export const THREAD_ID_KEY = "fieldops_thread_id";

export function getThreadId(): string | null {
  if (typeof window === "undefined") return null;
  return sessionStorage.getItem(THREAD_ID_KEY);
}

export function setThreadId(id: string): void {
  sessionStorage.setItem(THREAD_ID_KEY, id);
}

export function clearThreadId(): void {
  sessionStorage.removeItem(THREAD_ID_KEY);
}
