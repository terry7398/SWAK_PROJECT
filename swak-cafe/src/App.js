import { React, useEffect } from "react";
import { Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import QuestionPage from "./pages/QuestionPage";
import "./App.css";

const App = () => {
  useEffect(() => {
    const vh = window.innerHeight * 0.01;
    const vw = window.innerWidth * 0.01;
    document.documentElement.style.setProperty("--vh", `${vh}px`);
    document.documentElement.style.setProperty("--vw", `${vw}px`);
  }, []);
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/question/:questionID" element={<QuestionPage />} />
    </Routes>
  );
};

export default App;
