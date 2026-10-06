# Day 6 Analysis - Reliable Tool Calling

## 1. Scenario
I used an original **Study Helper** scenario rather than the lab manual's course-fee example. The two tools are `calculate_percentage(score,total)` and `get_study_tip(topic,difficulty)`. The difficulty field is an enum: `beginner`, `intermediate`, `advanced`.

## 2. Chat Completions
A Chat Completions request contains a model and messages and can include tool definitions. A response contains a choice, assistant message and `finish_reason`. When the assistant requests a tool, `message.tool_calls` contains generated calls and `message.content` can be empty because the model is requesting an action rather than giving its final answer. `stop` means normal completion; `length` means generation was truncated; some providers report `tool_calls` when tools are requested.

## 3. OpenAI-compatible API
An OpenAI-compatible server exposes a similar request/response shape so the same client style can point to another provider. This project points to Ollama through `/v1`. Compatibility does not guarantee identical feature support, so tool calling and structured-output support must be tested on the actual provider/model.

## 4. Streaming and Responses API
Streaming improves perceived responsiveness by delivering partial output. It is normally kept off while debugging an agent loop because the loop needs the complete tool-call structure. The task uses Chat Completions and does not require the Responses API.

## 5. One tool call
The model receives the question and tool definitions; it generates a tool name and arguments; the program parses the JSON; looks up and validates the tool; executes Python; then sends the result back as a `tool` message with the matching `tool_call_id`. The Python program performs the action, not the model, so generated arguments must be treated as untrusted input.

## 6. Schemas
This project uses `description`, `properties`, `required`, `enum`, and `additionalProperties:false`. `required` catches missing arguments, `additionalProperties:false` rejects invented arguments, type rules catch wrong types, and the enum restricts difficulty values. The same `SCHEMAS` dictionary is used for model tool definitions and local validation. `tool_choice` may be `auto`, `none`, `required`, or a named tool; this project uses `auto`.

## 7. JSON mode vs schema mode
JSON mode constrains the response to JSON but not necessarily to the application's exact fields. Schema mode defines the expected object shape. Neither proves that the returned facts are true: schemas constrain form, not truth.

## 8. Parallel calls
The question `I scored 72/100 in Python. Give my percentage and a beginner study tip.` is designed to allow two independent tool calls. The loop must process every call and append one tool message for every `tool_call_id`. Leaving one unanswered can make the next request invalid. Independent calls can be concurrent; dependent calls cannot.

## 9. Failure handling
| Failure | Guard |
|---|---|
| Invalid JSON | Catch JSON parsing error and return a string |
| Unknown tool | Safe registry lookup and available-tool message |
| Missing argument | Validator |
| Wrong type | Validator |
| Enum violation | Validator |
| Invented argument | `additionalProperties:false` + validator |
| Truncated reply | Retry with larger `max_tokens` when `finish_reason=length` |
| Repeated identical call | Stop after repeated identical calls |
All failures are returned as strings rather than crashing the loop.

## 10. Fault injection
The fault script runs without a model or internet. It injects invalid JSON, unknown tool, missing argument, wrong type, enum violation, invented argument, negative total, and unknown topic. The final two are custom semantic faults. A schema can restrict shape and types, but it cannot automatically encode every business rule.

## 11. Tool calling vs structured outputs
| Basis | Tool calling | Structured outputs |
|---|---|---|
| Model asked to do | Request an action/function | Return data in a defined shape |
| Who performs action | Python tool code | Model returns data |
| Shape control | Tool parameter schema | Response JSON/schema |
| Remaining risks | Bad calls, semantic errors, loops | Wrong values, unsupported feature, parsing errors |
| Guards | Parse, lookup, validate, execute, step/repeat guards | Parse and validate expected structure |
| Fetch/calculate | **Tool calling** | Not the first choice |
| Extract fields | Usually not needed | **Structured output** |

## 12. Observations
Run the scripts and fill these with the **actual** terminal results.

### Fault table
| Fault | Message returned | Continued? |
|---|---|---|
| Invalid JSON | actual output | Y |
| Unknown tool | actual output | Y |
| Missing required | actual output | Y |
| Wrong type | actual output | Y |
| Enum violation | actual output | Y |
| Invented argument | actual output | Y |
| Negative total | actual output | Y |
| Unknown topic | actual output | Y |

### Agent behaviour
| Question | Steps | Calls | Final answer | Parallel? | length? |
|---|---:|---|---|---|---|
| 72/100 percentage | actual | actual | actual | actual | actual |
| 72/100 Python + tip | actual | actual | actual | actual | actual |
| Expert-level tip | actual | actual | actual | actual | actual |
| List vs tuple | actual | actual | actual | actual | actual |

### Before/after guards
| Behaviour | Unguarded | Guarded |
|---|---|---|
| Steps | actual | actual |
| Final answer | actual | actual |
| Looped? | actual | actual |

### Structured outputs
| Case | Actual provider result |
|---|---|
| No constraint | actual |
| JSON mode | actual |
| Schema mode | actual |

## 13. Conclusion
The main lesson is that a model tool call is generated input and cannot be trusted on arrival. Every loop must parse, look up, validate and execute calls, answer every `tool_call_id`, handle truncation, detect repeated calls and stop at a maximum number of steps. Schemas prevent many interface errors but cannot prove semantic correctness or factual truth. Fault injection gives deterministic tests for failure paths without waiting for a model to fail randomly. For this Study Helper, tool calling is appropriate for calculations/lookups, while structured outputs are preferable when the model only needs to return extracted fields in a predictable shape.
