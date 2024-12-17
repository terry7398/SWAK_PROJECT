"use client";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import "../../style/game.css";
import "../../style/popup.css";
import Timer from "../components/Timer.js";
import ProgressBar from "../components/ProgressBar.js";
import Modal from "react-modal";

export default function GamePage() {
  const [countdown, setCountdown] = useState(3);
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState({});
  const [openModal, setOpenModal] = useState(false);
  const router = useRouter();
  const [time, setTime] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setTime((prev) => prev + 1);
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    fetch("/question1.json")
      .then((res) => res.json())
      .then((data) => setQuestions(Object.entries(data)));

    const timer = setInterval(() => {
      setCountdown((prev) => (prev > 1 ? prev - 1 : 0));
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  const closeModal = () => {
    setOpenModal(false);
  };

  const handleSubmit = () => {
    let emptyFields = 0;
    let incorrectCount = 0;

    questions.forEach(([id, question]) => {
      const correctAnswer = question[1];
      const userAnswer = answers[id]?.trim();

      if (!userAnswer) {
        emptyFields += 1;
      } else if (userAnswer !== correctAnswer) {
        incorrectCount += 1;
      }
    });

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
