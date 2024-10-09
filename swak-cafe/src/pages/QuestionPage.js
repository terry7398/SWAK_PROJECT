import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { motion, useMotionValue, useTransform, animate } from "framer-motion";
import "./QuestionPage.css";
import ProgressBar from "../components/ProgressBar";
import Timer from "../components/Timer";
import Question from "../components/Question";

const QuestionPage = () => {
  const { questionID } = useParams();
  const navigate = useNavigate();
  const [showAnswer, setShowAnswer] = useState(false);
  const [firstAnim, setFirstAnim] = useState(false);
  const [ready, setReady] = useState(false);
  const [lateReady, setLateReady] = useState(false);
  const count = useMotionValue(0);
  const rounded = useTransform(count, Math.round);
  const [answerInput, setAnswerInput] = useState("");

  const handleCheckAnswer = () => {
    setShowAnswer(true);
  };

  const handleTimeUp = () => {
    if (!showAnswer) {
      setShowAnswer(true);
    }
  };

  const handleBackToHome = () => {
    navigate("/");
  };
  const handleExplanation = () => {
    navigate("/explanation/" + questionID);
  };
  const handleInputChange = (e) => {
    setAnswerInput(e.target.value);
  };

  useEffect(() => {
    const animation = animate(count, 180, { duration: 3 });
    animation.then(() => {
      setTimeout(() => {
        setFirstAnim(true);
      }, 500);
      setTimeout(() => {
        setReady(true);
      }, 2000);
      setTimeout(() => {
        setLateReady(true);
      }, 2010);
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
        {lateReady && !showAnswer && (
          <motion.div
            initial={{ y: 10, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            exit={{ y: -10, opacity: 0 }}
            transition={{ duration: 2 }}
          >
            <ProgressBar duration={180} onComplete={handleTimeUp} />
            <Timer duration={180} onComplete={handleTimeUp} />
          </motion.div>
        )}
        {showAnswer && (
          <motion.div
            initial={{ y: 10, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 2 }}
          >
            <div className="button-container">
              <Question
                questionID={questionID}
                isRight={true}
                answer={answerInput}
              />
            </div>
            <Question questionID={questionID} />
          </motion.div>
        )}
        {ready && !showAnswer && (
          <motion.div
            initial={{ y: 10, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 2 }}
          >
            <Question questionID={questionID} />
          </motion.div>
        )}

        {lateReady && !showAnswer && (
          <motion.div
            initial={{ y: 10, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 2 }}
          >
            <div className="button-container">
              <input
                type="number"
                oninput="this.value = this.value.replace(/[^0-9.]/g, '').replace(/(\..*)\./g, '$1');"
                onChange={handleInputChange}
                value={answerInput}
              />
              <button className="answer-button" onClick={handleCheckAnswer}>
                정답
              </button>
            </div>
          </motion.div>
        )}

        {showAnswer && (
          <motion.div
            initial={{ y: 10, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 1 }}
          >
            <div className="button-container">
              <Question questionID={questionID} isAnswer={true} />
            </div>
            <div className="button-container">
              <motion.button
                className="answer-button"
                onClick={handleBackToHome}
                whileTap={{ scale: 1.2 }}
              >
                처음으로
              </motion.button>
              <motion.button
                className="answer-button"
                onClick={() => {
                  handleExplanation();
                }}
                whileTap={{ scale: 1.2 }}
              >
                풀이 보기
              </motion.button>
            </div>
          </motion.div>
        )}
      </motion.div>
    </>
  );
};

export default QuestionPage;
