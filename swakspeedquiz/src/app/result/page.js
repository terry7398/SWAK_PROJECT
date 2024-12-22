"use client";
import { motion } from "framer-motion";
import { Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import "../../style/Global.css";

export default function Result() {
  return (
    <Suspense fallback={<div>로딩 중...</div>}>
      <ResultPage />
    </Suspense>
  );
}

export function ResultPage() {
  const router = useRouter();
  const searchParams = useSearchParams();

  const time = searchParams.get("time");
  const issuccess = searchParams.get("issuccess") === "true" ? true : false;
  const correctAnswer = searchParams.get("correctAnswer");

  return (
    <div className="container">
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1 }}
        className="title"
      >
        {issuccess && (
          <>
            <h1>성공!</h1>
            <br />
            <h2>걸린 시간 : {time}초</h2>
          </>
        )}
        {!issuccess && (
          <div>
            <h1>실패...</h1>
            <br />
            <h2>맞힌 개수 : {correctAnswer}</h2>
          </div>
        )}
      </motion.div>
      <motion.button
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1 }}
        onClick={() => {
          router.push("/");
        }}
      >
        돌아가기
      </motion.button>
    </div>
  );
}
