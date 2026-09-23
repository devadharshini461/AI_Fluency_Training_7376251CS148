"""
Day 2 Task:
Run the Hospital Appointment Assistant using ReAct.
"""

from agent import agent
from config import banner


QUESTIONS = [

    (
        "A patient has a cardiology consultation costing "
        "Rs. 800 and a blood test costing Rs. 300. "
        "The hospital gives a 10% discount on the total. "
        "How much does the patient pay?"
    ),

    (
        "Three patients have appointments at 9:00 AM, "
        "9:30 AM and 10:00 AM. Ravi's appointment is "
        "before Kumar's, and Kumar's appointment is "
        "before Priya's. Who has the latest appointment?"
    ),

    (
        "What is the consultation fee for the CARDIO service?"
    )
]


if __name__ == "__main__":

    banner("HOSPITAL APPOINTMENT ASSISTANT")
    banner("ReAct AGENT")

    for number, question in enumerate(
        QUESTIONS,
        start=1
    ):

        print("\n" + "=" * 70)

        print(f"QUESTION {number}:")
        print(question)

        print("\n--- REACT TRACE ---")

        answer = agent(
            question,
            max_steps=8
        )

        print("\nFINAL OUTPUT:")
        print(answer)