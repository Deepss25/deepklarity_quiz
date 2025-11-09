import { useState } from "react";
import GenerateQuiz from "./components/GenerateQuiz";
import History from "./components/History";
import "./App.css";
import { FaBrain } from "react-icons/fa";

function App() {
  const [tab, setTab] = useState("generate");

  return (
    <div className="app-wrapper">
      <div className="app-container">
        <h1 className="app-title">
          <FaBrain className="icon" /> DeepKlarity Quiz Generator
        </h1>

        <div className="tab-buttons">
          <button
            className={tab === "generate" ? "active" : ""}
            onClick={() => setTab("generate")}
          >
            Generate Quiz
          </button>
          <button
            className={tab === "history" ? "active" : ""}
            onClick={() => setTab("history")}
          >
            Past Quizzes
          </button>
        </div>

        <div className="content">
          {tab === "generate" && <GenerateQuiz />}
          {tab === "history" && <History setTab={setTab} />}
        </div>
      </div>
    </div>
  );
}

export default App;
