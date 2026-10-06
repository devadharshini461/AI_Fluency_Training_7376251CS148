# Day 6 Assigned - Reliable Tool Calling

This package follows the Day 6 Task and Lab Manual, but uses an original **Study Helper** scenario instead of the manual's course-fee example.

## Folder structure

This folder is designed to sit directly inside your existing `AI AGENTS` folder. Your common `.env`, `.gitignore`, `requirements.txt`, and `.venv` stay in the parent folder and are **not duplicated here**.

```text
AI AGENTS/
├── .venv/
├── .env
├── .gitignore
├── requirements.txt
├── Day_1/
├── ...
├── Day_5_Assigned/
└── Day_6_Assigned/
    ├── tools_v2.py
    ├── agent.py
    ├── fault_injection.py
    ├── structured_outputs.py
    ├── analysis.md
    ├── README.md
    └── screenshots/
```

## Setup

Open the **AI AGENTS** folder in VS Code and use the existing environment:

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

The scripts read the existing parent `.env`. No new `.env` is required inside this folder.

The expected existing Ollama model is `study-assistant` from Day 5. Check with:

```powershell
ollama list
ollama ps
```

## Run Day 6

Move into this folder:

```powershell
cd Day_6_Assigned
```

Then run:

```powershell
python tools_v2.py
python fault_injection.py
python agent.py
python structured_outputs.py
```

For one agent question only:

```powershell
python agent.py --question "I scored 90/100 in Java. What is my percentage?"
```

## Screenshots

After running the scripts successfully, save screenshots of:

- validator output
- fault-injection output
- each required agent run, including the parallel-call question
- structured-output demo

Do not invent model observations. Record the actual provider behavior in `analysis.md` after running the code.
