"use client";

import { useEffect, useState } from "react";
import { getGreetingKoreanByLocalDate } from "@/lib/greetingKorean";
import { getUserDisplayName } from "@/lib/userDisplay";

/**
 * Line 1–3: 이름 / 시간대 인사(클라이언트 마운트 후) / CTA
 * 인사는 마운트 후에만 채움(시간 기준) → 서버/클라이언트 불일치 방지
 */
export function HomePageHero() {
  const name = getUserDisplayName();
  const [greeting, setGreeting] = useState("");

  useEffect(() => {
    setGreeting(getGreetingKoreanByLocalDate());
  }, []);

  return (
    <div className="max-w-2xl">
      <p className="text-xs font-bold uppercase tracking-widest text-primary/90">
        Field inspection · Report automation
      </p>
      <h1 className="mt-5 space-y-2 text-ink">
        <span className="block text-2xl font-bold tracking-tight sm:text-3xl">
          {name} 님
        </span>
        <span className="block min-h-[1.25em] text-2xl font-semibold text-ink/90 sm:text-3xl">
          {greeting || "\u00a0"}
        </span>
        <span className="block text-xl font-medium leading-snug text-ink/80 sm:text-2xl">
          어떤 보고서를 만들까요?
        </span>
      </h1>
      <p className="mt-5 max-w-xl text-sm leading-relaxed text-ink/65 sm:text-base">
        사진·PDF·로그·메모를 한 곳에 올리면 LangGraph로 분석·초안·검수까지 이어집니다.
        아래에 자료를 붙이고 지시를 입력하세요.
      </p>
    </div>
  );
}
