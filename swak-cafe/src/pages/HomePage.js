import React, { useState } from "react";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import "./HomePage.css";

const HomePage = () => {
  const navigate = useNavigate();
  const [isClick, setisClick] = useState(false);

  const getRandomNumber = () => {
    let max = 8;
    let res = Math.floor(Math.random() * max - 0.1) + 1;
    return res;
  };

  const handleGetStarted = () => {
    setTimeout(() => {
      navigate("/question/" + getRandomNumber());
    }, 100);
  };

  return (
    <motion.div
      className="homepage"
      initial={{ y: 10, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 1 }}
    >
      <h1 className="title">솩 3기 수학 카페</h1>
      <motion.button
        whileTap={{ scale: 1.2 }}
        onClick={() => {
          setisClick(!isClick);
          handleGetStarted();
        }}
      >
        시작하기
      </motion.button>
    </motion.div>
  );
};

export default HomePage;
