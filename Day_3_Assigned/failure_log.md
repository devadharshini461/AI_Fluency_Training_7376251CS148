# Day 3 Failure Log

## Failure 1 - Repeating Tool Call

### What I did

I intentionally made the product data unavailable.

### What happened

The agent attempted to repeat the same tool operation.

### Cause

There was no repeat detection in the unguarded agent.

### Fix

The fixed agent counts identical tool calls and stops
after the third identical call.

---

## Failure 2 - Hallucinated Tool

### What I did

I temporarily mentioned a non-existent tool called
send_notification in the system prompt.

### What happened

The model attempted to call the tool even though it was
not present in the registry.

### Cause

The model generated a tool call that was not available.

### Fix

The registry uses:

TOOL_FUNCTIONS.get(name)

instead of direct dictionary indexing.

This produces an Unknown tool message instead of crashing.

---

## Failure 3 - Context Overflow

### What I did

I intentionally generated a very large product result.

### What happened

The tool produced excessive output that could increase
the model's context usage.

### Cause

There was no output-size protection.

### Fix

The fixed agent truncates large tool observations and
also uses a character budget.