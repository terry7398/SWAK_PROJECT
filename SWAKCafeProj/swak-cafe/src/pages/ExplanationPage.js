import { motion } from "framer-motion";
import { useNavigate, useParams } from "react-router-dom";
import Question from "../components/Question";
import "./QuestionPage.css";

const ExplanationPage = () => {
  const { questionID } = useParams();
  const navigate = useNavigate();

  const handleBackToHome = () => {
    navigate("/");
  };

  return (
    <motion.div
      initial={{ y: 10, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 1 }}
    >
      <Question isExplanation={true} questionID={questionID} />
      <motion.button
        className="answer-button"
        onClick={handleBackToHome}
        whileTap={{ scale: 1.2 }}
      >
        처음으로
      </motion.button>
    </motion.div>
  );
};

export default ExplanationPage;
