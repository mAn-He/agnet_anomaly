/**
 * Time-of-day greeting (Korean) using local time.
 * Rules: 05–11:59 아침, 12–17:59 오후, 18–21:59 퇴근, 22–04:59 늦은 밤
 */
export function getGreetingKoreanByLocalDate(d: Date = new Date()): string {
  const h = d.getHours();
  if (h >= 22 || h < 5) {
    return "늦은 시간까지 고생 많으십니다";
  }
  if (h < 12) {
    return "좋은 아침입니다";
  }
  if (h < 18) {
    return "좋은 오후입니다";
  }
  return "퇴근까지 화이팅입니다";
}
