import { useState, useEffect } from "react";
import { getAllQuizzes } from "../services/api";
import QuizCard from "./QuizCard";

export default function History({ setTab }) {
  const [quizzes, setQuizzes] = useState([]);
  const [selectedQuiz, setSelectedQuiz] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      const data = await getAllQuizzes();
      if (Array.isArray(data)) setQuizzes(data);
      else setQuizzes([]);
    };
    fetchData();
  }, []);

  if (selectedQuiz) {
    return (
      <div style={{ textAlign: "center" }}>
        <button
          onClick={() => setSelectedQuiz(null)}
          style={{
            marginBottom: "20px",
            padding: "10px 20px",
            backgroundColor: "#0ff",
            color: "#000",
            border: "none",
            borderRadius: "8px",
            cursor: "pointer",
            boxShadow: "0 0 10px #0ff",
          }}
        >
          ⬅ Back
        </button>
        <QuizCard quiz={selectedQuiz} />
      </div>
    );
  }

  if (!quizzes.length) {
    return (
      <div style={{ textAlign: "center", color: "#0ff" }}>
        <p>No previous quizzes found.</p>
        <button
          onClick={() => setTab("generate")}
          style={{
            marginTop: "20px",
            padding: "10px 20px",
            backgroundColor: "#ff007f",
            color: "white",
            border: "none",
            borderRadius: "8px",
            cursor: "pointer",
            boxShadow: "0 0 10px #ff007f",
          }}
        >
          ⬅ Back to Generate Quiz
        </button>
      </div>
    );
  }

  return (
    <div style={{ textAlign: "center", color: "#0ff" }}>
      <h2 style={{ marginBottom: "20px" }}>Past Quizzes</h2>

      {quizzes.map((quiz, i) => (
        <div
          key={quiz.id || i}
          style={{
            border: "1px solid #0ff",
            borderRadius: "12px",
            padding: "15px",
            marginBottom: "15px",
            backgroundColor: "rgba(0, 255, 255, 0.05)",
            boxShadow: "0 0 10px rgba(0, 255, 255, 0.3)",
          }}
        >
          <h3 style={{ color: "#ff007f" }}>{quiz.title}</h3>
          <a href={quiz.url} target="_blank" rel="noreferrer" style={{ color: "#0ff" }}>
            {quiz.url}
          </a>
          <br />
          <button
            onClick={() => setSelectedQuiz(quiz)}
            style={{
              marginTop: "10px",
              padding: "8px 16px",
              backgroundColor: "#0ff",
              border: "none",
              borderRadius: "8px",
              cursor: "pointer",
              boxShadow: "0 0 10px #0ff",
            }}
          >
            View Quiz
          </button>
        </div>
      ))}

      <button
        onClick={() => setTab("generate")}
        style={{
          marginTop: "30px",
          padding: "10px 20px",
          backgroundColor: "#ff007f",
          color: "white",
          border: "none",
          borderRadius: "8px",
          cursor: "pointer",
          boxShadow: "0 0 10px #ff007f",
        }}
      >
        ⬅ Back to Generate Quiz
      </button>
    </div>
  );
}
