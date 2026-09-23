# Day 2 Task
## Reasoning and Acting: Direct Prompting, Chain-of-Thought and ReAct

## 1. Scenario

The scenario chosen for this experiment is an AI Hospital Appointment
Assistant.

The assistant is designed to help users with simple hospital-related
calculations, appointment reasoning, and retrieval of hospital service
information.

The hospital data used in this experiment is fictional and is stored
locally in the Python tool functions.

The available services are:

| Service | Fee |
|---|---:|
| General Consultation | Rs. 500 |
| Cardiology Consultation | Rs. 800 |
| Dermatology Consultation | Rs. 700 |
| Blood Test | Rs. 300 |

---

## 2. Questions Used

### Question 1 - Calculation

A patient has a cardiology consultation costing Rs. 800 and a blood
test costing Rs. 300. The hospital gives a 10% discount on the total.
How much does the patient pay?

Expected answer: Rs. 990.

### Question 2 - Logical Reasoning

Three patients have appointments at 9:00 AM, 9:30 AM and 10:00 AM.
Ravi's appointment is before Kumar's, and Kumar's appointment is
before Priya's. Who has the latest appointment?

Expected answer: Priya.

### Question 3 - External Information

What is the consultation fee for the CARDIO service?

Expected answer: Rs. 800.

This question requires the ReAct agent to retrieve information from
the hospital service tool.

---

## 3. Direct Prompting

Direct prompting asks the language model to provide an answer directly
without requesting visible step-by-step reasoning or using external
tools.

In this experiment, the direct prompt was tested on all three questions.

For Questions 1 and 2, the model can potentially answer because the
information needed to solve the problems is included directly in the
question.

For Question 3, direct prompting has no access to the hospital service
database. Therefore, the model may not reliably retrieve the correct
CARDIO fee unless that information is already available to the model.

Actual results:

[WRITE YOUR ACTUAL RESULTS HERE]

---

## 4. Chain-of-Thought

Chain-of-Thought prompting asks the model to solve the problem in
multiple steps before producing the final answer.

For Question 1, step-by-step reasoning allows the model to calculate
the total cost, discount and final amount.

For Question 2, step-by-step reasoning helps the model establish the
ordering of the three appointment times.

However, Chain-of-Thought does not itself provide access to the
hospital's local service database.

Therefore, for Question 3, reasoning alone cannot reliably retrieve
the CARDIO service fee.

Actual results:

[WRITE YOUR ACTUAL RESULTS HERE]

---

## 5. ReAct Agent

The ReAct agent combines reasoning with actions.

The agent can determine that external information is required, call a
tool, observe the returned result, and then continue toward the final
answer.

For example:

Thought:
I need the fee of the CARDIO service.

Action:
get_service_fee("CARDIO")

Observation:
800

Final Answer:
The CARDIO consultation fee is Rs. 800.

The ReAct approach is therefore able to use the local hospital tool
when the required information is not contained directly in the
question.

Actual results:

[WRITE YOUR ACTUAL RESULTS HERE]

---

## 6. Comparison Table

| Basis | Direct Prompting | Chain-of-Thought | ReAct Agent |
|---|---|---|---|
| Reasoning depth | Direct answer | Step-by-step reasoning | Reasoning combined with actions |
| Tool usage | No | No | Yes |
| Multi-step questions | Can solve simple problems | Better suited for multi-step reasoning | Can reason and use tools |
| External information | Cannot retrieve it | Cannot retrieve it by reasoning alone | Can retrieve through tools |
| Transparency | Final answer only | Reasoning steps requested | Tool/action/observation trace |
| Speed / cost | Usually lowest | Usually more tokens | Additional tool/model calls |
| Consistency | Depends on model/settings | Depends on model/settings | Depends on model and tools |

---

## 7. Self-Consistency Observation

The calculation question was selected for the self-consistency
experiment.

Question:

A patient has a cardiology consultation costing Rs. 800 and a blood
test costing Rs. 300. The hospital gives a 10% discount on the total.
How much does the patient pay?

### Results with temperature = 0.8

Run 1:
[ACTUAL RESULT]

Run 2:
[ACTUAL RESULT]

Run 3:
[ACTUAL RESULT]

Run 4:
[ACTUAL RESULT]

Run 5:
[ACTUAL RESULT]

Majority answer:
[ACTUAL RESULT]

Was the majority answer correct?
[YES/NO]

### Results with temperature = 0

[WRITE ACTUAL OBSERVATION]

The experiment showed that changing the temperature affects the
variation between repeated responses.

---

## 8. Suitability Analysis

For simple questions where all required information is already
provided, direct prompting can be sufficient.

For multi-step calculations and logical problems, Chain-of-Thought
prompting can provide a structured reasoning process.

For questions requiring information from an external source, ReAct is
more suitable because the agent can call a tool and use its returned
observation.

In the hospital scenario, the CARDIO service fee demonstrates the
importance of tool access. The model cannot reliably obtain a locally
stored hospital fee simply by being instructed to reason step by step.

Based on the experiment, the three approaches serve different
purposes rather than replacing one another completely.

---

## 9. Conclusion

Direct prompting is appropriate for straightforward questions where
the necessary information is already available.

Chain-of-Thought prompting is useful when a problem requires multiple
reasoning steps, calculations, or logical deductions.

ReAct is appropriate when reasoning must be combined with external
information or actions. It allows an agent to reason about what it
needs, call a suitable tool, observe the result, and continue toward
the final answer.

The hospital appointment scenario demonstrates that reasoning ability
and access to external information are different capabilities. A model
may be able to reason correctly about information supplied in a
question while still being unable to obtain information that is
outside the question without using a tool.