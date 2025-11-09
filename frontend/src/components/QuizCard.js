import { useState } from "react";

export default function QuizCard({ quiz }) {
  const [answers, setAnswers] = useState({});
  const [score, setScore] = useState(null);

  const handleSelect = (qIndex, option) => {
    setAnswers({ ...answers, [qIndex]: option });
  };

  const handleSubmit = () => {
    let correct = 0;
    quiz.quiz.forEach((q, i) => {
      if (answers[i] === q.answer) correct++;
    });
    setScore(correct);
  };

  return (
    <div style={{ border: "1px solid #ccc", padding: "15px", marginTop: "20px" }}>
      <h3>{quiz.title}</h3>
      <p>{quiz.summary}</p>

      <h4>Questions:</h4>
      {quiz.quiz.map((q, index) => (
        <div key={index} style={{ marginBottom: "15px" }}>
          <strong>{index + 1}. {q.question}</strong>
          <ul style={{ listStyleType: "none", padding: 0 }}>
            {q.options.map((opt, i) => (
              <li key={i}>
                <label>
                  <input
                    type="radio"
                    name={`q-${index}`}
                    value={opt}
                    onChange={() => handleSelect(index, opt)}
                    checked={answers[index] === opt}
                  />
                  {" "}{opt}
                </label>
              </li>
            ))}
          </ul>
          <p><em>Difficulty: {q.difficulty}</em></p>
        </div>
      ))}

      <button onClick={handleSubmit} style={{ marginTop: "10px" }}>
        Submit Quiz
      </button>

      {score !== null && (
        <h3 style={{ marginTop: "15px" }}>
          ✅ Your Score: {score} / {quiz.quiz.length}
        </h3>
      )}

      <h4>Related Topics:</h4>
      <ul>
        {quiz.related_topics.map((t, i) => (
          <li key={i}>{t}</li>
        ))}
      </ul>
    </div>
  );
}
