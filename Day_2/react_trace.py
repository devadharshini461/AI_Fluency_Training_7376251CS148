"""Day 2, Part D: print the agent's real ReAct trace to compare with your paper trace."""
import sys
import os
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'Day-1')
        )
)

from agent import run_agent_for_question

QUESTION = ("Which is cheaper: CS101 and AI202 with a 10% scholarship, "
            "or all three courses with a 25% scholarship? By how much?")

print("QUESTION:", QUESTION, "\n")
print("--- the agent's actions and observations ---")
answer = run_agent_for_question(QUESTION)
print("\nFINAL ANSWER:", answer)