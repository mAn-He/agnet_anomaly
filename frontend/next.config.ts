import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  /**
   * Dev: 브라우저가 localhost가 아닌 LAN IP(예: 다른 기기, 같은 PC의 14.x로 접속)로 열릴 때
   * /_next/* 요청이 “다른 origin”으로 잡혀 경고가 납니다. IP가 바뀌면 여기에 맞게 수정하세요.
   * @see https://nextjs.org/docs/app/api-reference/config/next-config-js/allowedDevOrigins
   */
  allowedDevOrigins: [
    "14.34.56.219",
    "127.0.0.1",
    "localhost",
  ],
};

export default nextConfig;
