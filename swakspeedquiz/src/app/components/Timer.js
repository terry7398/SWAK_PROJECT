import React, { useEffect, useState } from "react";
import "../../style/Timer.css";

const Timer = ({ duration, onComplete }) => {
  const [timeLeft, setTimeLeft] = useState(duration);

  useEffect(() => {
    const interval = setInterval(() => {
      if (timeLeft > 0) {
        setTimeLeft((prev) => prev - 1);
      }
    }, 1000);

    const timeout = setTimeout(() => {
      clearInterval(interval);
    }, duration * 1000);

    return () => {
      clearInterval(interval);
      clearTimeout(timeout);
    };
  }, [duration, onComplete]);

  return (
    <div className="timer">
      <h2>{timeLeft}</h2>
    </div>
  );
};

export default Timer;
