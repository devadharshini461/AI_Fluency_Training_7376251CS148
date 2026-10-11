"""Part B helper: test check_exam_eligibility directly (no LLM needed)."""
from task_agent import check_exam_eligibility

for v in (82, 70, 50, 120):
    print(v, "->", check_exam_eligibility.invoke({"attendance_percent": v}))

