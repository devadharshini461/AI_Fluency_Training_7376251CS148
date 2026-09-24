"""Day 3: Online Shopping Agent with safety guards."""

import json
import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent / "Day_1")
)
from config import client, MODEL, banner
from my_agent import SYSTEM_PROMPT
from my_tools import TOOLS, TOOL_FUNCTIONS


# Safety guards
MAX_TOOL_CHARS = 1500
CHAR_BUDGET = 30000


def agent(question, max_steps=8, verbose=True):

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

    # Guard 1: repeat detection
    seen_calls = {}

    # Guard 3: character budget
    chars_sent = 0

    for step in range(1, max_steps + 1):

        chars_sent += sum(
            len(str(message.get("content", "")))
            for message in messages
        )

        if chars_sent > CHAR_BUDGET:

            return (
                "Stopped: character budget exceeded "
                f"({chars_sent} characters sent)."
            )

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            temperature=0
        )

        message = response.choices[0].message

        # Final answer
        if not message.tool_calls:
            return message.content.strip()

        # Record assistant tool calls
        messages.append({
            "role": "assistant",
            "content": message.content or "",
            "tool_calls": [
                {
                    "id": call.id,
                    "type": "function",
                    "function": {
                        "name": call.function.name,
                        "arguments": call.function.arguments
                    }
                }
                for call in message.tool_calls
            ]
        })

        for call in message.tool_calls:

            name = call.function.name
            arguments = {}

            try:

                arguments = json.loads(
                    call.function.arguments or "{}"
                )

                # SAFE REGISTRY LOOKUP
                function = TOOL_FUNCTIONS.get(name)

                if function is None:

                    result = (
                        f"Unknown tool: {name}. "
                        f"Available: {list(TOOL_FUNCTIONS)}"
                    )

                else:

                    result = function(**arguments)

            except json.JSONDecodeError as error:

                result = (
                    f"Argument error: {error}. "
                    "Send valid JSON."
                )

            except TypeError as error:

                result = f"Argument error: {error}"

            except Exception as error:

                result = (
                    f"Tool error: "
                    f"{type(error).__name__}: {error}"
                )

            result = str(result)

            # =================================================
            # GUARD 1: REPEAT DETECTION
            # =================================================

            signature = (
                name,
                json.dumps(
                    arguments,
                    sort_keys=True
                )
            )

            seen_calls[signature] = (
                seen_calls.get(signature, 0) + 1
            )

            if seen_calls[signature] >= 3:

                return (
                    f"Stopped: tool {name} was called "
                    "3 times with the same arguments "
                    "and no progress was made.\n"
                    f"Last result: {result[:200]}"
                )

            # =================================================
            # GUARD 2: OUTPUT TRUNCATION
            # =================================================

            if len(result) > MAX_TOOL_CHARS:

                result = (
                    result[:MAX_TOOL_CHARS]
                    + " ... [observation truncated]"
                )

            if verbose:

                print(
                    f"\nstep {step}: "
                    f"{name}({arguments}) "
                    f"-> {result[:200]}"
                )

            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": result
            })

    return (
        "Stopped: maximum steps reached "
        "without a final answer."
    )


if __name__ == "__main__":

    banner(
        "ONLINE SHOPPING ASSISTANT - GUARDS ON"
    )

    questions = [

        (
            "Read products.html. "
            "Find a laptop under Rs. 60000, "
            "check whether it is in stock, "
            "and calculate the price after "
            "a 10 percent discount."
        ),

        (
            "Read missing_products.html "
            "and find a laptop under Rs. 60000."
        ),

        (
            "Read products.html and "
            "find all laptops and give me "
            "their information."
        )
    ]

    for question in questions:

        print("\n" + "=" * 60)

        print("\nQ:", question)

        print("\nA:", agent(question))