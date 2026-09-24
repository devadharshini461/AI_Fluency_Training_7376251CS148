# Day 3 Observations

## Scenario

Online Shopping Assistant

The user asks:

"Find a laptop under Rs. 60,000, check whether it
is in stock, and calculate the price after a 10%
discount."

---

## Successful Run

### Steps

1. search_product()
2. check_stock()
3. calculator()

### Result

The agent found a laptop within the budget, checked
its stock status, and calculated the discounted price.

---

## Failure 1 - Repeating Loop

The agent repeatedly attempted the same tool operation
when the required information could not be obtained.

### Guard

Repeat detection.

---

## Failure 2 - Unknown Tool

The model attempted to call a tool that was not present
in the tool registry.

### Guard

Safe registry lookup using TOOL_FUNCTIONS.get(name).

---

## Failure 3 - Context Overflow

A very large tool result produced an excessive amount
of information for the model.

### Guard

Observation truncation and character budget.

---

## Chosen Limits

| Setting | Value |
|---|---:|
| max_steps | 6 |
| MAX_TOOL_CHARS | 1500 |
| CHAR_BUDGET | 30000 |
| Repeat threshold | 3 |

---

## Conclusion

The experiment demonstrated that a ReAct agent can reason,
select tools, observe their results, and continue working
until it reaches a final answer.

The failure experiments showed that an agent also needs
stopping conditions and safety guards. Repeat detection
prevents endless repeated calls, output truncation prevents
large tool responses from flooding the model context, and
the character budget limits excessive model input.