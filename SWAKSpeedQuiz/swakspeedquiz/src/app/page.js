"use client";
import { useRouter, useSearchParams } from "next/navigation";
import { motion } from "framer-motion";
import { Suspense } from "react";
import "../style/Global.css";

export default function Home() {
  return (
    <Suspense fallback={<div>로딩 중...</div>}>
      <HomePage />
    </Suspense>
  );
}

export function HomePage() {
  const router = useRouter();
  const searchParams = useSearchParams();

  const problemNumber = searchParams.get("ProblemNumber");

  return (
    <div className="container">
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1 }}
        className="title"
      >
        스피드 퀴즈 레이스
      </motion.div>
      <motion.button
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1.5 }}
        onClick={() => router.push(`/game?ProblemNumber=${problemNumber}`)}
      >
        시작하기
      </motion.button>
    </div>
  );
}
