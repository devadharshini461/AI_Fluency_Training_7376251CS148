import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from config import client, MODEL, QUESTIONS

def run_chatbot():
    print("=== Simple LLM Chatbot (No Private Data / No Tools) ===\n")
    
    for i, question in enumerate(QUESTIONS, start=1):
        print(f"\n--- Question {i}: {question} ---")
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": question
                }
            ]
        )
        answer = response.choices[0].message.content
        print(f"AI: {answer}")

if __name__ == "__main__":
    run_chatbot()