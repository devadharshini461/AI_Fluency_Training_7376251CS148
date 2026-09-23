import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

MODEL = os.getenv("MODEL")
API_KEY = os.getenv("GROQ_API_KEY")
BASE_URL = os.getenv("BASE_URL")

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)


def banner(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)