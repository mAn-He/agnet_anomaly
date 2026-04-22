"use client";

import { useEffect, useState } from "react";
import { apiBaseUrl, healthCheck } from "@/lib/api";

export function ApiStatusBanner() {
  const [ok, setOk] = useState<boolean | null>(null);

  useEffect(() => {
    let cancelled = false;
    void (async () => {
      try {
        const h = await healthCheck();
        if (!cancelled) setOk(h.status === "ok");
      } catch {
        if (!cancelled) setOk(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  if (ok === null) return null;

  return (
    <div
      className={`rounded-pill border px-3 py-1 text-xs font-semibold ${
        ok
          ? "border-primary/30 bg-primary/10 text-primary"
          : "border-red-200 bg-red-50 text-red-800"
      }`}
    >
      API {apiBaseUrl}: {ok ? "connected" : "unreachable — start backend :8000"}
    </div>
  );
}
