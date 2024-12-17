import questions from "../assets/question.json";
import "@/style/Question.css";

const Question = ({ questionID, isAnswer, isExplanation, isRight, answer }) => {
  const question = questions.find((q) => q.id === parseInt(questionID));

  const convertBR = (text) => {
    return text.split("\n").map((line, index) => (
      <span key={index}>
        {line}
        <br />
      </span>
    ));
  };

  if (!question) {
    return <div className="question-box">Question not found.</div>;
  }
  if (isAnswer) {
    return <p className="answer">정답 : {question.answer}</p>;
  }
  if (isExplanation) {
    return (
      <div className="question-box">
        <b className="question-description">
          {convertBR(question.explanation)}
        </b>
      </div>
    );
  }
  if (isRight) {
    if (answer === question.answer) {
      return <p className="answer">정답!</p>;
    } else {
      return <p className="answer">오답</p>;
    }
  }

  return (
    <div className="question-box">
      <h2 className="question-title"> {question.name}</h2>
      <b className="question-description">{convertBR(question.description)}</b>
      <b className="question-source">{"출처 : " + question.source}</b>
    </div>
  );
};

export default Question;
