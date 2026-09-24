import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from workflow import workflow
from agent import run_agent_for_question

CHALLENGE_QUESTION = "I can pay Rs. 30,000. Which two courses can I take together within this budget?"

def run_challenge():
    print("==================================================")
    print("DAY 1 PRACTICE TASK: CHALLENGE COMPARISON")
    print("==================================================")
    print(f"Question: \"{CHALLENGE_QUESTION}\"\n")

    print("--------------------------------------------------")
    print("1. RUNNING RULE-BASED WORKFLOW")
    print("--------------------------------------------------")
    workflow_result = workflow(CHALLENGE_QUESTION)
    print(f"Workflow Output: {workflow_result}\n")
    print("Explanation: The workflow fails because it relies on hardcoded keyword rules.")

    print("\n--------------------------------------------------")
    print("2. RUNNING AI AGENT WITH TOOLS")
    print("--------------------------------------------------")
    agent_result = run_agent_for_question(CHALLENGE_QUESTION)
    print("\nExplanation: The AI agent dynamically queries available tools (get_course_fee and calculator) to determine all valid course combinations under ₹30,000.")

if __name__ == "__main__":
    run_challenge()