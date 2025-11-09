from sqlalchemy import create_engine, text

# Change the path if your DB file is different
engine = create_engine("sqlite:///test.db")

with engine.connect() as conn:
    conn.execute(text("ALTER TABLE quizzes ADD COLUMN raw_html TEXT;"))
    conn.commit()

print("raw_html column added!")
