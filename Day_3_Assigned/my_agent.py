"""Day 3: Online Shopping ReAct Agent."""

import json
import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent / "Day_1")
)

from config import client, MODEL, banner

from my_tools import TOOLS, TOOL_FUNCTIONS


# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are an Online Shopping Assistant.

You have access to three tools:

1. search_product
   - Finds products within a user's maximum budget.

2. check_stock
   - Checks whether a product is in stock.

3. calculator
   - Performs arithmetic calculations safely.

Rules:

- Use search_product when the user asks to find a product.
- Use check_stock when stock availability is required.
- Use calculator for price calculations.
- Never guess a product price.
- Never guess stock availability.
- Base your final answer on tool results.
- If a tool returns an error, explain the problem instead of inventing information.
"""


# ============================================================
# REACT AGENT
# ============================================================

def agent(question, max_steps=6, verbose=True):

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

        # ====================================================
        # 1. REASON
        # ====================================================

        response = client.chat.completions.create(

            model=MODEL,

            messages=messages,

            tools=TOOLS,

            temperature=0

        )

        message = response.choices[0].message


        # ====================================================
        # 2. STOP
        # ====================================================

        if not message.tool_calls:

            return message.content.strip()


        # ====================================================
        # 3. RECORD
        # ====================================================

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


        # ====================================================
        # 4. ACT + 5. OBSERVE
        # ====================================================

        for call in message.tool_calls:

            name = call.function.name

            arguments = {}


            try:

                arguments = json.loads(
                    call.function.arguments or "{}"
                )


                function = TOOL_FUNCTIONS.get(name)


                if function is None:

                    result = (
                        f"Unknown tool: {name}. "
                        f"Available tools: "
                        f"{list(TOOL_FUNCTIONS)}"
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


            if verbose:

                print(
                    f"\nstep {step}: "
                    f"{name}({arguments}) "
                    f"-> {str(result)[:200]}"
                )


            messages.append({

                "role": "tool",

                "tool_call_id": call.id,

                "content": str(result)

            })


    # ========================================================
    # 6. SAFETY EXIT
    # ========================================================

    return (
        "Stopped: maximum steps reached "
        "without a final answer."
    )


# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    banner("ONLINE SHOPPING ASSISTANT - NO GUARDS")


    question = (
        "Read products.html and Find a laptop under Rs. 60000, "
        "check whether it is in stock, "
        "and calculate the price after a 10 percent discount."
    )
    # question = (
    #     "Find a sunscreen under Rs. 60000 , "
    #     "check whether it is in stock, "
    #     "and calculate the price after a 10 percent discount."
    # )


    print("\nQ:", question)

    print("\nA:", agent(question))