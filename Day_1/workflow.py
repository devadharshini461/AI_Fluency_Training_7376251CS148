import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from config import COURSES, QUESTIONS

def workflow(question):
    q_lower = question.lower()

    # Rule 1: CS101 and AI202 combined scholarship query
    if "cs101" in q_lower and "ai202" in q_lower:
        cs_fee = COURSES.get("CS101", 0)
        ai_fee = COURSES.get("AI202", 0)
        total = cs_fee + ai_fee
        final = total * 0.90
        return f"After 10% scholarship, the total is ₹{final:,.0f}."

    # Rule 2: DS303 vs CS101 price comparison
    elif "ds303" in q_lower and "cs101" in q_lower:
        ds_fee = COURSES.get("DS303", 0)
        cs_fee = COURSES.get("CS101", 0)
        difference = ds_fee - cs_fee
        if difference > 0:
            return f"Yes. DS303 is ₹{difference:,} more expensive than CS101."
        else:
            return "No. DS303 is not more expensive than CS101."

    # Rule 3: Single course fee inquiry for AI202
    elif "ai202" in q_lower and "fee" in q_lower:
        fee = COURSES.get("AI202", 0)
        return f"AI202 fee is ₹{fee:,}."

    # Unhandled question fallback
    else:
        return "Sorry, I don't have a rule for that question."

def run_workflow():
    print("=== Rule-Based Workflow (Fixed Rules & Private Data) ===\n")
    for i, question in enumerate(QUESTIONS, start=1):
        print(f"\n--- Question {i}: {question} ---")
        answer = workflow(question)
        print(f"Workflow: {answer}")

if __name__ == "__main__":
    run_workflow()