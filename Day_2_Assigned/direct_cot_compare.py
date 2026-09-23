"""
Day 2 Task:
Compare Direct Prompting and Chain-of-Thought
using the Hospital Appointment Assistant scenario.
"""

from config import client, MODEL, banner


QUESTIONS = [

    # Question 1: Multi-step calculation
    (
        "A patient has a cardiology consultation costing Rs. 800 "
        "and a blood test costing Rs. 300. "
        "The hospital gives a 10% discount on the total. "
        "How much does the patient pay?"
    ),

    # Question 2: Logical reasoning
    (
        "Three patients have appointments at 9:00 AM, 9:30 AM "
        "and 10:00 AM. Ravi's appointment is before Kumar's, "
        "and Kumar's appointment is before Priya's. "
        "Who has the latest appointment?"
    ),

    # Question 3: External information
    (
        "What is the consultation fee for the CARDIO service "
        "at the hospital?"
    )
]


DIRECT_PROMPT = """
You are a helpful hospital assistant.

Answer the user's question directly.

Give only the final answer.
Do not show your reasoning.
Do not use tools.
"""


COT_PROMPT = """
You are a helpful hospital assistant.

Solve the problem step by step.

Number each reasoning step.
Show calculations when required.

After the reasoning, write:

Final Answer: <answer>

Do not use external tools.
"""


def ask(system_prompt, question, temperature=0):

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=temperature
    )

    return response.choices[0].message.content.strip()


if __name__ == "__main__":

    banner("HOSPITAL APPOINTMENT ASSISTANT")
    banner("DIRECT PROMPTING vs CHAIN-OF-THOUGHT")

    for number, question in enumerate(
        QUESTIONS,
        start=1
    ):

        print("=" * 70)

        print(f"QUESTION {number}")
        print(question)

        print("\n--- WITHOUT CoT ---")

        direct_answer = ask(
            DIRECT_PROMPT,
            question
        )

        print(direct_answer)

        print("\n--- WITH CoT ---")

        cot_answer = ask(
            COT_PROMPT,
            question
        )

        print(cot_answer)

        print()