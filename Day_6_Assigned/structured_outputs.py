"""Day 6: Same extraction question, three response formats."""
import os
import json
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Robustly load the shared .env file located one directory level above
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("GROQ_API_KEY") or os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("BASE_URL") or os.getenv("OPENAI_BASE_URL")
MODEL = os.getenv("MODEL", "openai/gpt-oss-120b")

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

Q = "Extract the student's name, course and score from: 'Anu scored 82 in Python programming.'"

S = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "course": {"type": "string"},
        "score": {"type": "number"}
    },
    "required": ["name", "course", "score"],
    "additionalProperties": False
}

def ask(fmt, label):
    print("\n---", label, "---")
    sys_msg = "Extract the requested fields as JSON." if fmt else "Extract the requested fields."
    messages = [
        {"role": "system", "content": sys_msg},
        {"role": "user", "content": Q}
    ]
    kwargs = {"model": MODEL, "messages": messages, "temperature": 0}
    if fmt is not None:
        kwargs["response_format"] = fmt

    response = client.chat.completions.create(**kwargs)
    raw = (response.choices[0].message.content or "").strip()
    print("raw:", raw)

    try:
        parsed = json.loads(raw)
        print("parsed:", parsed)
    except Exception as e:
        print("parsed/error:", e)

if __name__ == "__main__":
    ask(None, "1. no constraint")
    ask({"type": "json_object"}, "2. JSON mode")
    ask(
        {
            "type": "json_schema",
            "json_schema": {
                "name": "student_result",
                "schema": S,
                "strict": True
            }
        },
        "3. schema mode"
    )
