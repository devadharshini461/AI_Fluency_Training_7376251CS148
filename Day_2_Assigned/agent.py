"""
ReAct agent for the Hospital Appointment Assistant.
"""

import json

from config import client, MODEL
from tools import get_service_fee, calculator


SYSTEM_PROMPT = """
You are a hospital appointment assistant.

You have access to two tools:

1. get_service_fee(service_code)
   Use this when you need the fee of a hospital service.

2. calculator(expression)
   Use this when you need arithmetic calculations.

Available service codes:
GENERAL
CARDIO
DERMA
LAB001

You MUST follow this exact text-based ReAct format.

For a tool call:

Thought: explain what information you need.
TOOL: tool_name
ARGS: {"argument": "value"}

After receiving an Observation, continue reasoning.

When you have enough information, finish with:

FINAL ANSWER: your answer

Important rules:
- Do not invent hospital service fees.
- Use get_service_fee when a service fee is required.
- Use calculator for arithmetic.
- Use only ONE tool at a time.
- Do not perform arithmetic mentally.
- Do not use Markdown code blocks.
- Do not call tools using any special API format.
- Only use the TOOL and ARGS text format described above.
"""


def call_tool(tool_name, arguments):
    """
    Execute the requested local tool.
    """

    if tool_name == "get_service_fee":
        return get_service_fee(
            arguments.get("service_code", "")
        )

    if tool_name == "calculator":
        return calculator(
            arguments.get("expression", "")
        )

    return f"Unknown tool: {tool_name}"


def parse_tool_call(content):
    """
    Extract TOOL and ARGS from the model's text response.
    """

    tool_name = None
    arguments = {}

    lines = content.splitlines()

    for line in lines:

        line = line.strip()

        if line.upper().startswith("TOOL:"):
            tool_name = line.split(":", 1)[1].strip()

        elif line.upper().startswith("ARGS:"):
            argument_text = line.split(":", 1)[1].strip()

            try:
                arguments = json.loads(argument_text)
            except json.JSONDecodeError:
                arguments = {}

    return tool_name, arguments


def agent(question, max_steps=8):
    """
    Run a simple text-based ReAct loop.
    """

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": question
        }
    ]

    for step in range(1, max_steps + 1):

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0
        )

        message = response.choices[0].message

        content = message.content or ""

        content = content.strip()

        print(f"\n--- Step {step} ---")
        print(content)

        # Check whether the model has finished.
        if "FINAL ANSWER:" in content.upper():

            messages.append(
                {
                    "role": "assistant",
                    "content": content
                }
            )

            return content

        # Parse text-based tool request.
        tool_name, arguments = parse_tool_call(content)

        if not tool_name:

            messages.append(
                {
                    "role": "assistant",
                    "content": content
                }
            )

            messages.append(
                {
                    "role": "user",
                    "content": (
                        "Continue the ReAct process.\n"
                        "If you need a tool, use exactly:\n"
                        "TOOL: tool_name\n"
                        "ARGS: JSON\n\n"
                        "If you have enough information, use:\n"
                        "FINAL ANSWER: your answer"
                    )
                }
            )

            continue

        # Execute the local tool.
        result = call_tool(tool_name, arguments)

        print(f"TOOL RESULT: {result}")

        # Add model response to conversation.
        messages.append(
            {
                "role": "assistant",
                "content": content
            }
        )

        # Give the tool result back to the model.
        messages.append(
            {
                "role": "user",
                "content": (
                    f"Observation from {tool_name}: {result}\n\n"
                    "Continue the ReAct process."
                )
            }
        )

    return "Agent stopped because maximum steps were reached."