/**
 * Demo / display name for personalized copy on the home screen.
 * Replace with auth context or env when real users exist.
 */
export const DEFAULT_DEMO_USER_DISPLAY_NAME = "Eric" as const;

/** Reads NEXT_PUBLIC_USER_DISPLAY_NAME when set, else default demo name. */
export function getUserDisplayName(): string {
  if (typeof process !== "undefined" && process.env.NEXT_PUBLIC_USER_DISPLAY_NAME?.trim()) {
    return process.env.NEXT_PUBLIC_USER_DISPLAY_NAME.trim();
  }
  return DEFAULT_DEMO_USER_DISPLAY_NAME;
}
