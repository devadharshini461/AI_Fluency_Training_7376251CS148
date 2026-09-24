from config import client, MODEL

response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {
            "role": "user",
            "content": "Reply with exactly these two words: SETUP OK"
        }
    ]
)

print(response.choices[0].message.content.strip())