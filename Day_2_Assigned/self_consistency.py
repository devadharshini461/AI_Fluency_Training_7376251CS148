"""
Day 2 Task:
Self-consistency experiment for the Hospital Appointment Assistant.
"""

from collections import Counter

from config import client, MODEL, banner


QUESTION = (
    "A patient has a cardiology consultation costing "
    "Rs. 800 and a blood test costing Rs. 300. "
    "The hospital gives a 10% discount on the total. "
    "How much does the patient pay?"
)


COT_PROMPT = """
You are a helpful hospital assistant.

Solve the problem step by step.

Number each step and show the calculation.

At the end write exactly:

Final Answer: <answer>
"""


RUNS = 5
TEMPERATURE = 0.8


def final_answer(text):

    for line in reversed(text.splitlines()):

        if "final answer" in line.lower():

            return line.split(
                ":",
                1
            )[-1].strip()

    lines = text.splitlines()

    return lines[-1].strip() if lines else "(empty)"


def run_many(
    question,
    runs=RUNS,
    temperature=TEMPERATURE
):

    answers = []

    for attempt in range(1, runs + 1):

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": COT_PROMPT
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            temperature=temperature
        )

        output = response.choices[0].message.content.strip()

        answer = final_answer(output)

        print(f"Run {attempt}: {answer}")

        answers.append(answer)

    return answers


if __name__ == "__main__":

    banner("SELF-CONSISTENCY EXPERIMENT")

    print("QUESTION:")
    print(QUESTION)

    print("\n--- TEMPERATURE = 0.8 ---")

    answers = run_many(
        QUESTION,
        runs=5,
        temperature=0.8
    )

    counts = Counter(answers)

    winner, count = counts.most_common(1)[0]

    print(
        f"\nMajority answer "
        f"({count} of {len(answers)} runs): "
        f"{winner}"
    )

    print("\n--- TEMPERATURE = 0 ---")

    zero_answers = run_many(
        QUESTION,
        runs=5,
        temperature=0
    )

    zero_counts = Counter(zero_answers)

    zero_winner, zero_count = (
        zero_counts.most_common(1)[0]
    )

    print(
        f"\nTemperature 0 majority "
        f"({zero_count} of {len(zero_answers)} runs): "
        f"{zero_winner}"
    )