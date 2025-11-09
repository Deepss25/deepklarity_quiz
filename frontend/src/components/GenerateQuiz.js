import { useState } from "react";
import { generateQuiz } from "../services/api";
import QuizCard from "./QuizCard";

export default function GenerateQuiz() {
  const [url, setUrl] = useState("");
  const [quizData, setQuizData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const data = await generateQuiz(url);
      setQuizData(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>Generate Quiz</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Wikipedia URL"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          style={{ width: "300px", marginRight: "10px" }}
        />
        <button type="submit" className="my-button">Generate</button>
      </form>

      {loading && <p>Loading...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}
      {quizData && <QuizCard quiz={quizData} />}
    </div>
  );
}
