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

  const [answers, setAnswers] = useState({});
  const [openModal, setOpenModal] = useState(false);
  const router = useRouter();
  const [time, setTime] = useState(0);
  const searchParams = useSearchParams();
  const [question, setQuestion] = useState([]);
  const tip =
    "문제의 답은 모두 숫자로 이루어져 있습니다. \n숫자로만 입력해 주세요";

  useEffect(() => {
    setTimeout(() => {
      handleFail();
    }, 900000);
  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      setTime((prev) => prev + 1);
    }, 1000);

    return () => {
      clearInterval(interval);
    };
  }, []);

  const testAnswers = () => {
    let emptyFields = 0;
    let incorrectCount = 0;
    let stringFields = 0;

    question.forEach(([id, question]) => {
      const correctAnswer = question[1];
      const userAnswer = answers[id]?.trim();

      if (!userAnswer) {
        emptyFields += 1;
      } else if (!/^\d+$/.test(userAnswer)) {
        stringFields += 1;
      } else if (userAnswer !== correctAnswer) {
        incorrectCount += 1;
      }
    });

    return { emptyFields, incorrectCount, stringFields };
  };

  const handleFail = () => {
    const { emptyFields, incorrectCount, stringFields } = testAnswers();
    const incorrectAnswer = emptyFields + incorrectCount + stringFields;
    router.push(
      `/result?correctAnswer=${30 - incorrectAnswer}&issuccess=${false}`
    );
  };

  useEffect(() => {
    const problemNumber = searchParams.get("ProblemNumber");

    if (problemNumber) {
      fetch(`/question${problemNumber}.json`)
        .then((res) => {
          if (!res.ok) {
            throw new Error("Failed to fetch questions");
          }
          return res.json();
        })
        .then((data) => {
          setQuestion(Object.entries(data));
        })
        .catch((error) => {
          console.error("Error fetching questions:", error);
        });
    }

    const timer = setInterval(() => {
      setCountdown((prev) => (prev > 1 ? prev - 1 : 0));
    }, 1000);

    return () => clearInterval(timer);
  }, [searchParams]);

  const closeModal = () => {
    setOpenModal(false);
  };

  const handleSubmit = () => {
    const { emptyFields, incorrectCount, stringFields } = testAnswers();

    if (stringFields > 0) {
      alert(`문자로 된 답이 ${stringFields}개 있습니다. 숫자로 입력해주세요.`);
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
          {question.length > 0 && (
            <div className="problem-grid">
              {question.map(([id, question]) => (
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
          )}
          <motion.h3
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 1 }}
            style={{
              marginTop: "10px",
              whiteSpace: "pre-line",
              textAlign: "center",
            }}
          >
            {tip}
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
              {question.map(([id]) => (
                <input
                  key={id}
                  placeholder={`${id}번 정답`}
                  className="input-box"
                  value={answers[id] || ""}
                  onChange={(e) => {
                    setAnswers({
                      ...answers,
                      [id]: e.target.value,
                    });
                  }}
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
