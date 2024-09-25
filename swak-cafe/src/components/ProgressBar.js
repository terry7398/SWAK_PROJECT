import React, { useEffect, useState } from "react";
import { motion } from "framer-motion";

const ProgressBar = ({ duration, onComplete }) => {
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setProgress((prev) => prev + 100 / duration);
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
      transition={{ ease: "linear" }}
    />
  );
};

export default ProgressBar;
