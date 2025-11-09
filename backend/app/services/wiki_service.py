import os
import requests
from bs4 import BeautifulSoup
import json
from typing import List
from dotenv import load_dotenv
import textwrap
import time
import re

# LangChain imports
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI  # Gemini
# from langchain_openai import ChatOpenAI  # OpenAI alternative

load_dotenv()

# ---------------- Configuration ----------------
LLM_MODEL = os.getenv("LLM_MODEL", "gemini-1.5-turbo")  # Updated model
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ---------------- Text Chunking ----------------
def chunk_text(text: str, max_chars: int = 2000) -> List[str]:
    text = text.strip()
    if not text:
        return []
    paras = [p.strip() for p in text.split("\n") if p.strip()]
    chunks, current, cur_len = [], [], 0
    for p in paras:
        if cur_len + len(p) + 1 > max_chars and current:
            chunks.append("\n\n".join(current))
            current = [p]
            cur_len = len(p)
        else:
            current.append(p)
            cur_len += len(p) + 1
    if current:
        chunks.append("\n\n".join(current))
    return chunks

# ---------------- Prompt Template ----------------
PROMPT_TEMPLATE = textwrap.dedent("""
You are a helpful assistant that generates a multiple-choice quiz based ONLY on the provided article text.

ARTICLE_TITLE: {title}
ARTICLE_TEXT: {text_for_llm}

Important:
- ONLY return JSON.
- Generate at least 5 quiz questions.
- Do not include any extra text outside JSON.

Return JSON like:
{{
  "title": "...",
  "summary": "...",
  "key_entities": {{"people": [], "organizations": [], "locations": []}},
  "sections": ["..."],
  "quiz": [
    {{
      "question": "...",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "answer": "...",
      "difficulty": "easy/medium/hard",
      "explanation": "..."
    }}
  ],
  "related_topics": ["..."]
}}
""")

# ---------------- Call LLM ----------------
def call_llm_generate(text_for_llm: str, title: str):
    llm = ChatGoogleGenerativeAI(model=LLM_MODEL, temperature=0.2, google_api_key=GOOGLE_API_KEY)
    # llm = ChatOpenAI(model=LLM_MODEL, temperature=0.2, openai_api_key=OPENAI_API_KEY)

    prompt = PromptTemplate(input_variables=["title", "text_for_llm"], template=PROMPT_TEMPLATE)
    chain = prompt | llm | StrOutputParser()

    tries = 0
    while tries < 3:
        try:
            result = chain.invoke({"title": title, "text_for_llm": text_for_llm})
            return result
        except Exception as e:
            tries += 1
            time.sleep(1 + tries * 1.5)
            last_err = e
    raise last_err

# ---------------- Parse JSON ----------------
def parse_json_from_model(output_str: str):
    try:
        # Extract first {...} block
        match = re.search(r"\{.*\}", output_str, re.DOTALL)
        if not match:
            raise ValueError("No JSON found in output")
        json_text = match.group(0)
        return json.loads(json_text)
    except json.JSONDecodeError:
        # Attempt to fix single quotes
        try:
            fixed_text = json_text.replace("'", '"')
            return json.loads(fixed_text)
        except Exception as e2:
            raise ValueError("Failed to parse JSON from LLM output") from e2

# ---------------- Main Function ----------------
def generate_quiz_from_url(url: str) -> dict:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    resp = requests.get(url, headers=headers, timeout=15)
    if resp.status_code != 200:
        raise Exception("Unable to fetch URL")

    soup = BeautifulSoup(resp.text, "html.parser")
    title_tag = soup.find("h1")
    title = title_tag.get_text(strip=True) if title_tag else (soup.title.string if soup.title else "Untitled")
    paragraphs = [p.get_text(" ", strip=True) for p in soup.find_all("p")]
    headings = [h.get_text(" ", strip=True) for h in soup.find_all(["h1", "h2", "h3"])]
    full_text = "\n\n".join(headings + paragraphs)

    chunks = chunk_text(full_text, max_chars=2500)
    text_for_llm = "\n\n---\n\n".join(chunks[:3]) if chunks else full_text[:4000]

    llm_output = call_llm_generate(text_for_llm, title)
    model_data = parse_json_from_model(llm_output)

    # Post-validate quiz
    validated_questions = []
    for q in model_data.get("quiz", []):
        try:
            options = q.get("options") or []
            if len(options) != 4:
                options = (options + ["Option A", "Option B", "Option C", "Option D"])[:4]
            answer = q.get("answer", options[0] if options else "")
            if answer not in options:
                options[0] = answer
            validated_questions.append({
                "question": q.get("question", "")[:1000],
                "options": options,
                "answer": answer,
                "difficulty": q.get("difficulty", "medium"),
                "explanation": q.get("explanation", "")[:500]
            })
        except Exception:
            continue
    model_data["quiz"] = validated_questions

    # Return structured quiz
    return {
        "url": url,
        "title": model_data.get("title", title),
        "summary": model_data.get("summary", ""),
        "key_entities": model_data.get("key_entities", {"people": [], "organizations": [], "locations": []}),
        "sections": model_data.get("sections", headings),
        "quiz": model_data.get("quiz", []),
        "related_topics": model_data.get("related_topics", []),
        "raw_html": resp.text
    }
