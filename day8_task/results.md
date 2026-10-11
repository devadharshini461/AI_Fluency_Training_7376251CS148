# Day 8 Task - Results

## Part A - Evidence              
Loaded 6 documents
Split into 27 chunks (chunk_size=300, overlap=50)
Example chunk -> '## Contact\nQueries about the training can be sent to the Training & Placement Cell office, Room 104, Main Block.' {'source': 'ai_fluency_training.md'}
Stored 27 vectors in ./chroma_db using EMBED_PROVIDER=fastembed
Vector length: 384
```            

Q: How much is the late fee for paying fees after the due date?
  0.197  [fee_policy.md]  '## Late fee\nA late fee of Rs. 100 per day is charged after the due dat'
  0.299  [fee_policy.md]  '## Tuition fee\nThe annual tuition fee must be paid before 15 July for '
  0.333  [exam_regulations.md]  '## Revaluation\nRevaluation can be applied for within 5 working days of'

Q: What time should hostel students return?
  0.130  [hostel_rules.md]  '## In-time\nAll hostel residents must return to the hostel by 9.00 PM. '
  0.295  [hostel_rules.md]  '## Leave\nTo go home, a student must submit a leave form to the warden '
  0.300  [hostel_rules.md]  '# Hostel Rules (Greenfield College of Engineering - sample document)'

Q: Can I write the exam with 70% attendance?
  0.247  [exam_regulations.md]  '## Attendance requirement\nA student needs a minimum of 75% attendance '
  0.332  [exam_regulations.md]  'Students below 65% attendance are not permitted to write the examinati'
  0.336  [placement_policy.md]  '## Pre-placement training\nA minimum of 90% attendance in pre-placement'

Q: What CGPA do I need to be eligible for placements?
  0.177  [placement_policy.md]  '# Placement Policy (Greenfield College of Engineering - sample documen'
  0.236  [fee_policy.md]  '## Scholarships\nStudents with a CGPA of 9.0 or above in the previous y'
  0.318  [placement_policy.md]  '## Pre-placement training\nA minimum of 90% attendance in pre-placement'

Filtered to library.md:
   library.md -> ## Fines A fine of Rs. 2 per day per book is charged for late return. Lost books
   library.md -> # Library Rules (Greenfield College of Engineering - sample document)  ## Borrow
```

## Part B - Tool test 
82 -> ELIGIBLE: 82.0% attendance meets the 75% minimum. The student may write the exam.
70 -> CONDONATION: 70.0% is below 75% but at least 65%. The student may write the exam after paying a condonation fee of Rs. 500 per course.
50 -> NOT ELIGIBLE: 50.0% is below 65%. The student is not permitted to write the exam.
120 -> Error: attendance must be between 0 and 100, got 120.0.
```

## Part C - Relevance guard
GOOD (placements): [0.177, 0.236, 0.318]   best = 0.177
BAD  (France)    : [0.573, 0.573, 0.577]   best = 0.573

Pick MAX_DISTANCE between the GOOD best score and the BAD best score.

## Part D - Test report
[task-run] USER: What CGPA do I need to be eligible for placements?
   agent  -> call search_handbook({'query': 'CGPA eligibility placements'})
   tools  -> search_handbook returned '[placement_policy.md] # Placement Policy (Greenfield Co'...
   agent  -> ANSWER: Students need a CGPA of 6.5 or higher to be eligible for campus placements. (Source: **placement_policy.md**)

[task-run] USER: My attendance is 70%. Can I write the exam?
   agent  -> call check_exam_eligibility({'attendance_percent': 70})
   tools  -> check_exam_eligibility returned 'CONDONATION: 70.0% is below 75% but at least 65%. The s'...
   agent  -> ANSWER: Yes. With 70 % attendance you’re below the 75 % threshold, but youcan still write the exam by applying for condonation and paying the Rs 500 per‑course fee. (Source: **exam_regulations.md**)

[task-run] USER: What is the total of the CS101 fee, the AI202 fee and the maximum latefee?
   agent  -> call search_handbook({'query': 'late fee maximum'})
   tools  -> search_handbook returned '[fee_policy.md] ## Late fee\nA late fee of Rs. 100 per d'...
   agent  -> call get_course_fee({'course_code': 'CS101'})
   tools  -> get_course_fee returned 'CS101 fee is Rs. 12000'...
   agent  -> call get_course_fee({'course_code': 'AI202'})
   tools  -> get_course_fee returned 'AI202 fee is Rs. 18000'...
   agent  -> call calculator({'expression': '12000 + 18000 + 2000'})
   tools  -> calculator returned '32000'...
   agent  -> ANSWER: The total is **Rs 32,000** (CS101 = 12,000 + AI202 = 18,000 + maximum late fee = 2,000). (Source: **fee_policy.md**, **CS101 fee**, **AI202 fee**)

[task-run] USER: And if I pay only 5 days late instead?
   agent  -> call calculator({'expression': '12000 + 18000 + 500'})
   tools  -> calculator returned '30500'...
   agent  -> ANSWER: If you’re only 5 days late, the late fee is 5 × Rs 100 = Rs 500.
Total payable = CS101 Rs 12,000 + AI202 Rs 18,000 + late fee Rs 500 = **Rs 30,500**. (Source: **fee_policy.md**, **CS101 fee**, **AI202 fee**)

[task-run] USER: What is the capital of France?
   agent  -> ANSWER: I’m sorry, but I don’t have that information.


=== COPY INTO results.md ===
| # | Tools called (in order) | Agent's answer (short) |
|---|-------------------------|------------------------|
| 1 | search_handbook | Students need a CGPA of 6.5 or higher to be eligible for campusplacements. (Source: **placement_policy.md**) |
| 2 | check_exam_eligibility | Yes. With 70 % attendance you’re below the 75 % threshold, but you can still write the exam by applying for condonation and paying the Rs 500 per‑cour |
| 3 | search_handbook -> get_course_fee -> get_course_fee -> calculator | The total is **Rs 32,000** (CS101 = 12,000 + AI202 = 18,000 + maximum late fee = 2,000). (Source: **fee_policy.md**, **CS101 fee**, **AI202 fee**) |
| 4 | calculator | If you’re only 5 days late, the late fee is 5 × Rs 100 = Rs 500. Total payable = CS101 Rs 12,000 + AI202 Rs 18,000 + late fee Rs 500 = **Rs 30,500**.  |
| 5 | (none) | I’m sorry, but I don’t have that information. |

Model used: openai/gpt-oss-120b   Embedding model: BAAI/bge-small-en-v1.5   MAX_DISTANCE: 0.8
Thread task-run has 24 messages saved in memory