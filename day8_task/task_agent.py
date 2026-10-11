"""Day 8 task: agentic RAG helpdesk + placement doc, exam-eligibility tool, relevance guard."""
import ast
import operator
import os
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from lc_config import get_model, get_vectorstore

COURSE_FEES = {"CS101": 12000, "AI202": 18000, "DS303": 15000}   # same data as Day 1
store = get_vectorstore()

# PART C: cosine-distance limit. Chunks with a score ABOVE this are dropped.
# 0.6 works for the offline hash embedding. For nomic-embed-text / bge-small,
# run measure_scores.py and set MAX_DISTANCE in .env (or change the default below).
MAX_DISTANCE = float(os.getenv("MAX_DISTANCE", "0.6"))


@tool
def search_handbook(query: str) -> str:
    """Search the college handbook (fees, hostel, exams, library, AI training, placements) and return matching passages."""
    results = store.similarity_search_with_score(query, k=3)          # (doc, cosine distance)
    good = [(d, s) for d, s in results if s <= MAX_DISTANCE]          # drop weak matches
    if not good:
        return "NO_MATCH: this is not covered in the college handbook."
    return "\n\n".join(f"[{d.metadata['source']}] {d.page_content}" for d, _ in good)


@tool
def get_course_fee(course_code: str) -> str:
    """Return the fee in rupees for a course code such as CS101, AI202 or DS303."""
    fee = COURSE_FEES.get(course_code.strip().upper())
    return f"{course_code.upper()} fee is Rs. {fee}" if fee else f"Unknown course code {course_code}"


OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv}


@tool
def calculator(expression: str) -> str:
    """Evaluate simple arithmetic such as '18000 + 15000' or '100 * 12'."""
    def ev(n):
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):
            return n.value
        if isinstance(n, ast.BinOp) and type(n.op) in OPS:
            return OPS[type(n.op)](ev(n.left), ev(n.right))
        raise ValueError("only + - * / on numbers")
    try:
        return str(ev(ast.parse(expression, mode="eval").body))
    except Exception as e:                       # tell the model, don't crash the graph
        return f"Error: {e}"


# PART B: new tool (rules from exam_regulations.md)
@tool
def check_exam_eligibility(attendance_percent: float) -> str:
    """Check if a student with this attendance percentage (0-100) may write the end-semester exam."""
    if attendance_percent < 0 or attendance_percent > 100:                    # TODO 1
        return f"Error: attendance must be between 0 and 100, got {attendance_percent}."
    if attendance_percent >= 75:                                              # TODO 2
        return f"ELIGIBLE: {attendance_percent}% attendance meets the 75% minimum. The student may write the exam."
    if attendance_percent >= 65:                                              # TODO 3
        return (f"CONDONATION: {attendance_percent}% is below 75% but at least 65%. "
                "The student may write the exam after paying a condonation fee of Rs. 500 per course.")
    return (f"NOT ELIGIBLE: {attendance_percent}% is below 65%. "                # TODO 4
            "The student is not permitted to write the exam.")


tools = [search_handbook, get_course_fee, calculator, check_exam_eligibility]
model = get_model().bind_tools(tools)
SYSTEM = ("You are the Greenfield College helpdesk. Use search_handbook for any rule or policy "
          "(fees, hostel, exams, library, placements), get_course_fee for course fees and calculator for arithmetic. "
          "Use check_exam_eligibility whenever the student gives an attendance percentage and asks "
          "if they can write the exam. "
          "If search_handbook returns NO_MATCH, say you don't know - do not guess or use your own knowledge. "
          "Answer briefly and name the source file. If the tools do not give the answer, say you don't know.")


def agent(state: MessagesState):
    """The LLM node: read the conversation, either answer or ask for a tool."""
    reply = model.invoke([("system", SYSTEM)] + state["messages"])
    return {"messages": [reply]}


builder = StateGraph(MessagesState)
builder.add_node("agent", agent)
builder.add_node("tools", ToolNode(tools))          # runs every tool call in the last message
builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition)   # tool calls? -> "tools", else -> END
builder.add_edge("tools", "agent")                  # the LOOP back to the LLM
graph = builder.compile(checkpointer=InMemorySaver())  # checkpointer = memory per thread


def ask(question, thread_id):
    """Run one question; print the trace; return (tools called in order, final answer)."""
    config = {"configurable": {"thread_id": thread_id}, "recursion_limit": 10}
    print(f"\n[{thread_id}] USER: {question}")
    called, answer = [], ""
    for step in graph.stream({"messages": [("user", question)]}, config, stream_mode="updates"):
        for node, update in step.items():
            for msg in update["messages"]:
                if getattr(msg, "tool_calls", None):
                    for c in msg.tool_calls:
                        called.append(c["name"])
                        print(f"   {node:6} -> call {c['name']}({c['args']})")
                elif node == "tools":
                    print(f"   {node:6} -> {msg.name} returned {msg.content[:55]!r}...")
                else:
                    answer = msg.content
                    print(f"   {node:6} -> ANSWER: {msg.content}")
    return called, answer


# PART D: five questions, ONE thread
QUESTIONS = [
    "What CGPA do I need to be eligible for placements?",
    "My attendance is 70%. Can I write the exam?",
    "What is the total of the CS101 fee, the AI202 fee and the maximum late fee?",
    "And if I pay only 5 days late instead?",
    "What is the capital of France?",
]

if __name__ == "__main__":
    rows = []
    for i, q in enumerate(QUESTIONS, 1):
        called, answer = ask(q, "task-run")
        rows.append((i, " -> ".join(called) or "(none)", " ".join(answer.split())[:150]))

    # Copy these two columns into results.md, then fill Correct? / If N, why?
    print("\n\n=== COPY INTO results.md ===")
    print("| # | Tools called (in order) | Agent's answer (short) |")
    print("|---|-------------------------|------------------------|")
    for i, t, a in rows:
        print(f"| {i} | {t} | {a} |")
    print(f"\nModel used: {os.getenv('MODEL', 'qwen2.5:1.5b')}   "
          f"Embedding model: {os.getenv('EMBED_MODEL', os.getenv('EMBED_PROVIDER', 'default'))}   "
          f"MAX_DISTANCE: {MAX_DISTANCE}")
    n = len(graph.get_state({"configurable": {"thread_id": "task-run"}}).values["messages"])
    print(f"Thread task-run has {n} messages saved in memory")
