import QuizCard from "./QuizCard";

export default function QuizModal({ quiz, onClose }) {
  return (
    <div style={{
      position: "fixed", top: 0, left: 0, width: "100%", height: "100%",
      backgroundColor: "rgba(0,0,0,0.5)", display: "flex", justifyContent: "center", alignItems: "center"
    }}>
      <div style={{ backgroundColor: "white", padding: "20px", maxWidth: "800px", width: "90%", maxHeight: "90%", overflowY: "scroll" }}>
        <button onClick={onClose} style={{ float: "right" }}>Close</button>
        <QuizCard quiz={quiz} />
      </div>
    </div>
  );
}
