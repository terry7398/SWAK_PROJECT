"use client";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import "../style/Global.css";

export default function HomePage() {
  const router = useRouter();
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
        onClick={() =>
          router.push(
            `/game?ProblemNumber=${process.env.NEXT_PUBLIC_PROBLEM_NUMBER}`
          )
        }
      >
        시작하기
      </motion.button>
    </div>
  );
}
