from sqlalchemy import Column, Integer, String, JSON, create_engine,Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Quiz(Base):
    __tablename__ = "quizzes"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String,index=True)
    title = Column(String)
    summary = Column(String)
    key_entities = Column(JSON)
    sections = Column(JSON)
    quiz = Column(JSON)
    related_topics = Column(JSON)
    raw_html = Column(Text)

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # for simplicity; change to PostgreSQL/MySQL if needed
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)
