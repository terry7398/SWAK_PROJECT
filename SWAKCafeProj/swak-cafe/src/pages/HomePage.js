import React, { useState } from "react";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import "./HomePage.css";
import questions from "../assets/question.json";

const HomePage = () => {
  const navigate = useNavigate();
  const [isClick, setisClick] = useState(false);

  const getRandomNumber = () => {
    const difficulty0 = questions.filter((q) => q.difficulty === 0);
    const difficulty1 = questions.filter((q) => q.difficulty === 1);
    const difficulty2 = questions.filter((q) => q.difficulty === 2);
    const difficulty3 = questions.filter((q) => q.difficulty === 3);
    const difficulty4 = questions.filter((q) => q.difficulty === 4);

    const getRandomDifficulty = () => {
      const random = Math.random();
      // if (random < 0.25) return 1;
      // else if (random < 0.5) return 2;
      // else if (random < 0.75) return 3;
      // else if (random < 0.9) return 4;
      // else return 5;
      if (random < 0.4) return 1;
      else if (random < 0.7) return 2;
      else return 3;
    };

    const randomDifficulty = getRandomDifficulty();

    let chosenList;
    let time;
    if (randomDifficulty === 1) {
      chosenList = difficulty0;
      // time = 60;
      time = 150;
    } else if (randomDifficulty === 2) {
      chosenList = difficulty1;
      // time = 100;
      time = 150;
    } else if (randomDifficulty === 3) {
      chosenList = difficulty2;
      // time = 150;
      time = 200;
    } else if (randomDifficulty === 4) {
      chosenList = difficulty3;
      time = 200;
    } else if (randomDifficulty === 5) {
      chosenList = difficulty4;
      time = 300;
    }
    const randomIndex = Math.floor(Math.random() * chosenList.length);
    return chosenList[randomIndex].id.toString() + "/" + time.toString();
  };

  const handleGetStarted = () => {
    setTimeout(() => {
      let param = getRandomNumber();
      if (param !== null) {
        navigate("/question/" + param);
      }
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
      <div>
        <h1 className="_title">솩 3기 수학 카페</h1>
      </div>

      <motion.button
        whileTap={{ scale: 1.2 }}
        onClick={() => {
          setisClick(!isClick);
          handleGetStarted();
        }}
      >
        시작하기
      </motion.button>
      <p>※기록의 목적으로 활동 모습이 촬영될 수 있습니다※</p>
      <p>
        ※활동사진에는 얼굴과 같은 부분은 모자이크 처리될 예정이며, 촬영을 원치
        않으시면 말씀해 주시기 바랍니다※
      </p>
    </motion.div>
  );
};

export default HomePage;
