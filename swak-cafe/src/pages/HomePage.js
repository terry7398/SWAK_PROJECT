import React from "react";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import "./HomePage.css";

const HomePage = () => {
  const navigate = useNavigate();

  const getRandomNumber = () => {
    let max = 8;
    let res = Math.floor(Math.random() * max) + 1;
    return res;
  };

  const handleGetStarted = () => {
    navigate("/question/" + getRandomNumber());
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
        initial={false}
        animate={{ scale: 1.5 }}
        whileTap="press"
        onClick={handleGetStarted}
      ></motion.button>
    </motion.div>
  );
};

export default HomePage;
