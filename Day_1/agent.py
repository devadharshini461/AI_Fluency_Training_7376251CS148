import json
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from config import client, MODEL, QUESTIONS
from tools import get_course_fee, calculator

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_course_fee",
            "description": "Get the tuition fee for a specific course code (e.g. CS101, AI202, DS303).",
            "parameters": {
                "type": "object",
                "properties": {
                    "course_code": {
                        "type": "string",
                        "description": "The exact course code like CS101, AI202, or DS303"
                    }
                },
                "required": ["course_code"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Perform math calculations such as addition, subtraction, multiplication, division.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Math expression string, e.g. '(12000 + 18000) * 0.9' or '15000 - 12000'"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]

def run_agent_for_question(question: str):
    print(f"\n==========================================")
    print(f"USER QUESTION: {question}")
    print(f"==========================================")

    messages = [
        {
            "role": "system",
            "content": (
                "You are an accurate college fee assistant agent. "
                "The available college courses are CS101, AI202, and DS303. "
                "Always look up course fees using get_course_fee and perform math calculations using the calculator tool. "
                "Never guess course fees or do mental math. "
                "Use exact function names 'get_course_fee' or 'calculator' without any extra text or tags in tool names. "
                "If multiple courses are mentioned in the question, call get_course_fee for each course to retrieve all required fees before producing the final response."
            )
        },
        {
            "role": "user",
            "content": question
        }
    ]

    for step in range(9):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=tools
            )
        except Exception as e:
            print(f"\n[Agent Error]: API call encountered an error: {e}")
            messages.append({
                "role": "user",
                "content": "Please output the final answer using the information gathered so far without making further tool calls."
            })
            continue

        message = response.choices[0].message

        if message.tool_calls:
            clean_tool_calls = []
            for tc in message.tool_calls:
                raw_name = tc.function.name or ""
                clean_name = raw_name.split("<")[0].strip()
                tc.function.name = clean_name
                clean_tool_calls.append({
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": clean_name,
                        "arguments": tc.function.arguments
                    }
                })
            
            messages.append({
                "role": "assistant",
                "content": message.content or None,
                "tool_calls": clean_tool_calls
            })
        else:
            messages.append({
                "role": "assistant",
                "content": message.content
            })

        if not message.tool_calls:
            if message.content and message.content.strip():
                print(f"\n[Final Agent Answer]:\n{message.content.strip()}")
                return message.content.strip()
            else:
                messages.append({
                    "role": "user",
                    "content": "Please state the complete final answer based on the tool results."
                })
                continue

        for tool_call in message.tool_calls:
            raw_name = tool_call.function.name or ""
            name = raw_name.split("<")[0].strip()
            
            if isinstance(tool_call.function.arguments, str):
                arguments = json.loads(tool_call.function.arguments)
            else:
                arguments = tool_call.function.arguments

            print(f"\n--- [Step {step + 1}] Tool Call Trace ---")
            print(f"Tool Name : {name}")
            print(f"Arguments : {arguments}")

            if name == "get_course_fee":
                code = arguments.get("course_code", "")
                result = get_course_fee(code)
            elif name in ("calculator", "calculate") or name.startswith("calc"):
                expr = arguments.get("expression", "")
                result = calculator(expr)
            else:
                result = f"Unknown tool: {name}"

            print(f"Tool Result: {result}")

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result)
            })

    print("\n[Agent Warning]: Maximum step count (6) reached.")
    return None

def main():
    print("=== AI Agent with Tool Integration ===")
    for q in QUESTIONS:
        run_agent_for_question(q)

if __name__ == "__main__":
    main()