import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { motion, useMotionValue, useTransform, animate } from "framer-motion";
import ProgressBar from "../components/ProgressBar";
import Timer from "../components/Timer";
import answerData from "../assets/answer.json"; // Import answer data

const QuestionPage = () => {
  const { questionID } = useParams();
  const navigate = useNavigate();
  const [showAnswer, setShowAnswer] = useState(false);
  const [timerExpired, setTimerExpired] = useState(false);
  const [firstAnim, setFirstAnim] = useState(false);
  const [ready, setReady] = useState(false);
  const [lateReady, setLateReady] = useState(false);
  const count = useMotionValue(0);
  const rounded = useTransform(count, Math.round);

  const handleCheckAnswer = () => {
    setShowAnswer(true);
  };

  const handleTimeUp = () => {
    setTimerExpired(true);
    if (!showAnswer) {
      setTimerExpired(true);
      setShowAnswer(true);
    }
  };

  const handleBackToHome = () => {
    navigate("/");
  };

  const questionImage = require(`../assets/${questionID}.jpg`); // Dynamically load the image

  useEffect(() => {
    const animation = animate(count, 180, { duration: 3 });
    animation.then(() => {
      setTimeout(() => {
        setFirstAnim(true);
      }, 1000);
      setTimeout(() => {
        setReady(true);
      }, 3000);
      setTimeout(() => {
        setLateReady(true);
      }, 3010);
    });
    return animation.stop;
  }, []);

  return (
    <>
      <motion.div
        initial={{ y: 10, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        exit={{ opacity: 0 }}
        transition={{ duration: 1 }}
      >
        {!firstAnim && (
          <motion.h1
            className="start-anim-number"
            animate={{ y: 0, opacity: 1 }}
            exit={{ y: -10, opacity: 0 }}
            transition={{ duration: 1 }}
          >
            {rounded}
          </motion.h1>
        )}
        {firstAnim && (
          <>
            <motion.h1
              className="start-anim-number"
              animate={{ y: 60, opacity: 0 }}
              transition={{ duration: 2 }}
            >
              {rounded}
            </motion.h1>
          </>
        )}
        {lateReady && (
          <motion.div
            initial={{ y: 10, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 2 }}
          >
            <ProgressBar duration={180} onComplete={handleTimeUp} />
            <Timer duration={180} onComplete={handleTimeUp} />
          </motion.div>
        )}
        {ready && (
          <motion.div
            initial={{ y: 10, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 2 }}
          >
            <img src={questionImage} alt={`Question ${questionID}`} />
          </motion.div>
        )}

        {lateReady && !showAnswer && (
          <motion.div
            initial={{ y: 10, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 2 }}
          >
            <button className="answer-button" onClick={handleCheckAnswer}>
              정답
            </button>
          </motion.div>
        )}

        {showAnswer && (
          <motion.div
            initial={{ y: 10, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 1 }}
          >
            <p>Correct Answer: {answerData[questionID]}</p>
            <button className="answer-button" onClick={handleBackToHome}>
              처음으로
            </button>
          </motion.div>
        )}
      </motion.div>
    </>
  );
};

export default QuestionPage;
