import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

PROVIDER = os.getenv("PROVIDER")
MODEL = os.getenv("MODEL")

if PROVIDER == "groq":
    client = OpenAI(
        api_key=os.getenv("GROQ_API_KEY"),
        base_url="https://api.groq.com/openai/v1"
    )
else:
    raise ValueError("Unsupported provider")

COURSES = {
    "CS101": 12000,
    "AI202": 18000,
    "DS303": 15000
}

QUESTIONS = [
    "What is the fee for AI202?",
    "What is the total fee for CS101 and AI202 after a 10% scholarship?",
    "Is DS303 more expensive than CS101? If yes, by how much?",
    "Give me a two-line welcome message."
]

def banner(title):
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)