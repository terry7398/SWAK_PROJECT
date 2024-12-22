"use client";
import { useState, useEffect, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { motion } from "framer-motion";
import "../../style/game.css";
import "../../style/popup.css";
import Timer from "../components/Timer.js";
import ProgressBar from "../components/ProgressBar.js";
import Modal from "react-modal";

export default function Game() {
  return (
    <Suspense fallback={<div>로딩 중...</div>}>
      <GamePage />
    </Suspense>
  );
}

export function GamePage() {
  const [countdown, setCountdown] = useState(3);
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState({});
  const [openModal, setOpenModal] = useState(false);
  const router = useRouter();
  const [time, setTime] = useState(0);
  const searchParams = useSearchParams();

  useEffect(() => {
    const interval = setInterval(() => {
      setTime((prev) => prev + 1);
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    fetch(`/question${searchParams.get("ProblemNumber")}.json`)
      .then((res) => res.json())
      .then((data) => setQuestions(Object.entries(data)));

    setTimeout(() => {
      let { emptyFields, incorrectCount, stringFileds } = testAnswers();
      let incorrectAnswer = emptyFields + incorrectCount + stringFileds;
      router.push(
        `/result?correctAnswer=${30 - incorrectAnswer}&issuccess=${false}`
      );
    }, 5000);

    const timer = setInterval(() => {
      setCountdown((prev) => (prev > 1 ? prev - 1 : 0));
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  const closeModal = () => {
    setOpenModal(false);
  };

  const testAnswers = () => {
    let emptyFields = 0;
    let incorrectCount = 0;
    let stringFileds = 0;

    questions.forEach(([id, question]) => {
      const correctAnswer = question[1];
      const userAnswer = answers[id]?.trim();

      if (!userAnswer) {
        emptyFields += 1;
      } else if (!/^\d+$/.test(userAnswer)) {
        stringFileds += 1;
      } else if (userAnswer !== correctAnswer) {
        incorrectCount += 1;
      }
    });

    return { emptyFields, incorrectCount, stringFileds };
  };

  const handleSubmit = () => {
    let { emptyFields, incorrectCount, stringFileds } = testAnswers();

    if (stringFileds > 0) {
      alert(`문자로 된 답이 ${stringFileds}개 있습니다. 숫자로 입력해주세요.`);
      return;
    }
    if (emptyFields > 0) {
      alert(`입력하지 않은 답이 ${emptyFields}개 있습니다. 모두 입력해주세요.`);
      return;
    }

    if (incorrectCount > 0) {
      alert(`틀린 답이 ${incorrectCount}개 있습니다. 다시 확인해주세요.`);
      return;
    }

    router.push(`/result?time=${time}&issuccess=${true}`);
  };

  const togglePopup = () => {
    setOpenModal((prev) => !prev);
  };

  return (
    <div className="container">
      {countdown > 0 ? (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 1 }}
          className="title"
        >
          {countdown}
        </motion.div>
      ) : (
        <>
          <Timer duration={900} />
          <ProgressBar duration={900} />
          <div className="problem-grid">
            {questions.map(([id, question]) => (
              <motion.div
                key={id}
                className="problem-box"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.5 }}
              >
                <p className="problem-description">{question[0]}</p>
              </motion.div>
            ))}
          </div>
          <motion.h3
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 1 }}
            style={{ marginTop: "10px" }}
          >
            문제의 답은 모두 숫자로 이루어져 있습니다. 숫자로만 입력해 주세요
          </motion.h3>
          <motion.button
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 1 }}
            onClick={togglePopup}
          >
            정답 입력하기
          </motion.button>
          <Modal
            ariaHideApp={false}
            isOpen={openModal}
            onRequestClose={closeModal}
            className="popup-container"
            overlayClassName="overlay"
          >
            <div className="popup-grid">
              {questions.map(([id]) => (
                <input
                  key={id}
                  placeholder={`${id}번 정답`}
                  className="input-box"
                  onChange={(e) =>
                    setAnswers({
                      ...answers,
                      [id]: e.target.value,
                    })
                  }
                />
              ))}
            </div>
            <button onClick={handleSubmit}>정답 확인하기</button>
          </Modal>
        </>
      )}
    </div>
  );
}
