# DeepKlarity Technologies - AI Wiki Quiz Generator

## 📋 Project Overview
This project automatically generates quizzes from Wikipedia articles using LLMs.
It includes a FastAPI backend, React frontend, and PostgreSQL database.

---

## ⚙️ Setup Instructions

### 🧠 Backend (FastAPI)
```bash
cd backend
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env       # then add your real API key here
uvicorn app.main:app --reload
