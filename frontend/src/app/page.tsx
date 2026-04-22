import Link from "next/link";
import { AppShell } from "@/components/AppShell";
import { ApiStatusBanner } from "@/components/ApiStatusBanner";
import { HomePageHero } from "@/components/home/HomePageHero";
import { HomeUploadChatBox } from "@/components/home/HomeUploadChatBox";
import { Card } from "@/components/ui/Card";

const btnGhost =
  "inline-flex items-center justify-center rounded-pill border border-border bg-white px-5 py-2.5 text-sm font-semibold text-ink transition hover:border-primary/30 hover:bg-primary/5 hover:text-primary focus:outline-none focus:ring-2 focus:ring-primary/40";

export default function LandingPage() {
  return (
    <AppShell>
      <div className="space-y-12 pb-10">
        <div className="grid gap-12 lg:grid-cols-[minmax(0,1.15fr)_minmax(0,0.9fr)] lg:items-start">
          <div className="space-y-8">
            <HomePageHero />
            <section aria-label="빠른 보고서 시작">
              <HomeUploadChatBox />
            </section>
            <div className="flex flex-wrap items-center gap-3">
              <ApiStatusBanner />
            </div>
            <div className="flex flex-wrap gap-3 border-t border-border/60 pt-6">
              <Link href="/upload" className={btnGhost}>
                상세 업로드
              </Link>
              <Link href="/progress" className={btnGhost}>
                진행 상황
              </Link>
              <Link href="/report" className={btnGhost}>
                보고서 편집
              </Link>
            </div>
          </div>
          <aside className="relative lg:sticky lg:top-24">
            <div className="absolute -inset-1 -z-10 rounded-[1.7rem] bg-gradient-to-br from-primary/15 via-cyan/10 to-transparent opacity-80 blur-2xl" />
            <div className="glass-orb relative rounded-[1.5rem] p-6 sm:p-8">
              <div className="absolute -right-3 -top-3 h-24 w-24 rounded-full bg-cyan-400/20 blur-2xl" />
              <Card className="relative border-white/80 bg-white/90 p-5 shadow-lg backdrop-blur-sm sm:p-6">
                <p className="text-sm font-bold text-primary">오늘의 파이프라인</p>
                <p className="mt-2 text-xs leading-relaxed text-ink/60">
                  Intake → 모달리티 → Fusion → RAG → 초안 → Rule / Reviewer → 내보내기
                </p>
                <ul className="mt-4 space-y-2.5 text-sm text-ink/80">
                  <li className="flex items-start gap-2">
                    <span className="mt-0.5 text-primary" aria-hidden>
                      ·
                    </span>
                    이미지·PDF·노트·센서 데이터 동시에 처리
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="mt-0.5 text-cyan" aria-hidden>
                      ·
                    </span>
                    SOP 기반 RAG + 규칙·리뷰어 이중 검증
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="mt-0.5 text-violet" aria-hidden>
                      ·
                    </span>
                    Markdown로 승인·다운로드
                  </li>
                </ul>
              </Card>
            </div>
          </aside>
        </div>
      </div>
    </AppShell>
  );
}
