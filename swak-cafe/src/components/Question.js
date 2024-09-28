import questions from "../assets/question.json";
import "./Question.css";

const Question = ({ questionID }) => {
  const question = questions.find((q) => q.id === parseInt(questionID));

  if (!question) {
    return <div className="question-box">Question not found.</div>;
  }

  return (
    <div className="question-box">
      <h2 className="question-title"> {question.name}</h2>
      <strong className="question-description">{question.description}</strong>
    </div>
  );
};

export default Question;
