// Base API URL
const BASE_URL = "http://127.0.0.1:8000/api";

// ✅ Generate quiz from URL
export async function generateQuiz(url) {
  const res = await fetch(`${BASE_URL}/generate_quiz`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url }),
  });

  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Failed to generate quiz");
  }

  return res.json();
}

// ✅ Get all quizzes
export async function getAllQuizzes() {
  const res = await fetch(`${BASE_URL}/quizzes`);
  if (!res.ok) {
    throw new Error("Failed to fetch quizzes");
  }
  return res.json();
}

// ✅ Get quiz by ID
export async function getQuizById(id) {
  const res = await fetch(`${BASE_URL}/quiz/${id}`);
  if (!res.ok) {
    throw new Error("Failed to fetch quiz");
  }
  return res.json();
}
