import { React, useEffect, useState } from "react";
import { Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import QuestionPage from "./pages/QuestionPage";
import "./App.css";

const App = () => {
  const [dimensions, setDimensions] = useState({
    width: window.innerWidth,
    height: window.innerHeight,
  });
  const [isTablet, setIsTablet] = useState(false);

  useEffect(() => {
    // 갤럭시 태블릿 감지
    const userAgent = window.navigator.userAgent.toLowerCase();
    if (userAgent.includes("SM")) {
      setIsTablet(true);
    }

    function handleResize() {
      setDimensions({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    }

    window.addEventListener("resize", handleResize);

    handleResize();

    return () => window.removeEventListener("resize", handleResize);
  }, []);

  return (
    <div
      style={{
        width: isTablet ? dimensions.width * 0.7 : dimensions.width * 0.9,
        height: isTablet ? dimensions.height * 0.7 : dimensions.height * 0.9,
        margin: "0 auto",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/question/:questionID" element={<QuestionPage />} />
      </Routes>
    </div>
  );
};

export default App;
