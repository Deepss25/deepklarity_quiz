from sqlalchemy.orm import Session
from app.models import Quiz, SessionLocal

def create_quiz(quiz_data: dict):
    db = SessionLocal()
    try:
        db_quiz = Quiz(**quiz_data)
        db.add(db_quiz)
        db.commit()
        db.refresh(db_quiz)
        return db_quiz.__dict__
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def get_all_quizzes():
    db = SessionLocal()
    try:
        quizzes = db.query(Quiz).all()
        return [q.__dict__ for q in quizzes]
    finally:
        db.close()


def get_quiz_by_id(quiz_id: int):
    db = SessionLocal()
    try:
        quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
        return quiz.__dict__ if quiz else None
    finally:
        db.close()


def get_quiz_by_url(url: str):
    db = SessionLocal()
    try:
        quiz = db.query(Quiz).filter(Quiz.url == url).first()
        return quiz.__dict__ if quiz else None
    finally:
        db.close()
