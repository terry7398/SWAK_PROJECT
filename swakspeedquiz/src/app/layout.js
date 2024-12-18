import "./globals.css";
import "../style/Global.css";
import { Analytics } from "@vercel/analytics/react";

export const metadata = {
  title: "스피드 퀴즈 레이스",
  description: "A simple quiz race website",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
      <Analytics />
    </html>
  );
}
