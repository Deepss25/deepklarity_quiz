from pydantic import BaseModel
from typing import List, Optional, Dict


# Input schema for generating a quiz
class QuizCreate(BaseModel):
    url: str  # Use str, not Text


# Output schema for a quiz question
class QuizQuestion(BaseModel):
    question: str
    options: List[str]
    answer: str
    difficulty: Optional[str] = "medium"
    explanation: Optional[str] = ""


# Output schema for the full quiz
class QuizOut(BaseModel):
    id: Optional[int] = None
    url: str
    title: str
    summary: Optional[str] = ""
    key_entities: Optional[Dict[str, List[str]]] = {"people": [], "organizations": [], "locations": []}
    sections: Optional[List[str]] = []
    quiz: Optional[List[QuizQuestion]] = []
    related_topics: Optional[List[str]] = []
    raw_html: Optional[str] = None
