import React, { useEffect, useState } from "react";
import { motion, easeIn } from "framer-motion";
import "./ProgressBar.css";

const ProgressBar = ({ duration, onComplete }) => {
  const [progress, setProgress] = useState(0);
  const [timeLeft, setTimeLeft] = useState(duration);

  useEffect(() => {
    const interval = setInterval(() => {
      if (timeLeft > 0) {
        setProgress((prev) => prev + 100 / duration);
        setTimeLeft((prev) => prev - 1);
      }
    }, 1000);

    const timeout = setTimeout(() => {
      clearInterval(interval);
      onComplete();
    }, duration * 1000);

    return () => {
      clearInterval(interval);
      clearTimeout(timeout);
    };
  }, [duration, onComplete]);

  return (
    <motion.div
      className="progress-bar"
      style={{ width: `${progress}%` }}
      animate={{ width: `${progress}%` }}
      transition={{ ease: easeIn }}
    />
  );
};

export default ProgressBar;
