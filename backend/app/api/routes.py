from fastapi import APIRouter, HTTPException
from app.schemas import QuizCreate, QuizOut
from app.services.wiki_service import generate_quiz_from_url
from app import crud
from app.models import SessionLocal

router = APIRouter()


@router.post("/generate_quiz", response_model=QuizOut)
def generate_quiz(quiz_in: QuizCreate):
    url = quiz_in.url
    if not url:
        raise HTTPException(status_code=400, detail="URL is required")

    try:
        # Generate quiz data
        quiz_data = generate_quiz_from_url(url)

        # Check if quiz already exists
        existing = crud.get_quiz_by_url(url)
        if existing:
            return existing  # return existing quiz

        # Create new quiz
        new_quiz = crud.create_quiz(quiz_data)
        return new_quiz

    except Exception as e:
        db = SessionLocal()
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))



# ✅ Add this route to fetch all quizzes for "Past Quizzes"
@router.get("/quizzes")
def get_all_quizzes():
    try:
        quizzes = crud.get_all_quizzes()
        return quizzes if quizzes else []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
