import json
import time
import requests

BASE = "http://localhost:11434"
MODEL = "study-assistant"

def non_streaming(prompt):
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
    }
    start = time.perf_counter()
    r = requests.post(f"{BASE}/api/generate", json=payload, timeout=120)
    r.raise_for_status()
    data = r.json()
    total = time.perf_counter() - start

    eval_count = data.get("eval_count", 0)
    eval_duration = data.get("eval_duration", 0)
    tps = eval_count / (eval_duration / 1e9) if eval_duration else 0

    print("\n=== NON-STREAMING /api/generate ===")
    print("Prompt:", prompt)
    print("Answer:", data.get("response", "").strip())
    print(f"Total time: {total:.3f} s")
    print(f"Tokens: {eval_count}")
    print(f"Tokens/sec: {tps:.2f}")

def streaming(prompt):
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": True,
    }
    start = time.perf_counter()
    first_token = None
    pieces = []
    final = {}

    with requests.post(f"{BASE}/api/generate", json=payload, stream=True, timeout=120) as r:
        r.raise_for_status()
        for line in r.iter_lines():
            if not line:
                continue
            data = json.loads(line)
            if first_token is None and data.get("response"):
                first_token = time.perf_counter()
            pieces.append(data.get("response", ""))
            if data.get("done"):
                final = data

    end = time.perf_counter()
    ttft = (first_token - start) if first_token else None
    total = end - start

    eval_count = final.get("eval_count", 0)
    eval_duration = final.get("eval_duration", 0)
    tps = eval_count / (eval_duration / 1e9) if eval_duration else 0

    print("\n=== STREAMING /api/generate ===")
    print("Prompt:", prompt)
    print("Answer:", "".join(pieces).strip())
    print(f"TTFT: {ttft:.3f} s" if ttft is not None else "TTFT: unavailable")
    print(f"Total time: {total:.3f} s")
    print(f"Tokens: {eval_count}")
    print(f"Tokens/sec: {tps:.2f}")

def openai_override(prompt):
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You are a strict exam-answer assistant. Answer in formal English and use exactly 3 bullet points."
            },
            {"role": "user", "content": prompt},
        ],
        "stream": False,
        "temperature": 0.2,
    }
    r = requests.post(f"{BASE}/v1/chat/completions", json=payload, timeout=120)
    r.raise_for_status()
    data = r.json()

    print("\n=== OPENAI-COMPATIBLE ENDPOINT ===")
    print("Program system prompt: strict exam-answer assistant")
    print("Answer:")
    print(data["choices"][0]["message"]["content"].strip())

if __name__ == "__main__":
    print("Custom model:", MODEL)
    non_streaming("What is a Java class? Explain for a beginner.")
    streaming("Explain what an API is in simple words.")
    openai_override("What is inheritance in Java?")
    print("\nRun one prompt twice to compare first-load and warm-run behaviour.")
