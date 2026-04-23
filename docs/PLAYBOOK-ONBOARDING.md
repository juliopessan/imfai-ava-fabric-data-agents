# Onboarding Playbook — New Project

> **Type:** Tutorial — from zero to first executable wave  
> **Audience:** New team members (analysts, engineers, coordinators)  
> **Estimated time:** Full onboarding in ~2 hours of reading + setup

---

## What You Will Learn

By the end of this guide you will know:

1. How the operating model works (phases, gates, agents)
2. How to set up the local environment
3. How to activate and use agents in VS Code
4. How to run your first simulated wave
5. Where to find help when you get stuck

---

## Section 1 — Understand the Method Before Configuring Anything

### 1.1 — The core idea

This project is an **agentic migration factory**: instead of standalone scripts and manual processes, the entire data migration lifecycle is orchestrated by specialized AI agents, validated by mandatory gates with measurable criteria.

```

UPSTREAM          MIDSTREAM         DOWNSTREAM
(Discovery)       (Design)          (Execution)
    │                 │                  │
  Gate 1           Gate 2             Gate 3
    │                 │                  │
 Catalog           Architect          Execute
 Map               Model              Reconcile
 Strategize        Validate           Document

```

**Rule you need to internalize:** nothing advances to the next phase without a calculated gate score and a recorded decision. A gate is not an honor checklist — it is a technical blocker.

### 1.2 — The three roles you will likely perform

| Role | What it does | Most used agents |
| --- | --- | --- |

| **Migration Coordinator** | Orchestrates waves, validates gates, decides approval | `master-agent`, `migration-coordinator` |
| **Data Engineer / Architect** | Designs, models, generates code, validates quality | `data-architect`, `data-modeler`, `code-generator`, `quality-gate` |
| **Downstream Executor** | Executes waves, reconciles, documents | `downstream-executor`, `reconciliation`, `documentation` |

In smaller projects one person may perform all roles. In enterprise projects each role has a dedicated owner.

### 1.3 — The project agents

We have 19 agents organized by phase. The rule is to always start with `master-agent` if you don't know where to go:

| Phase | Core Agents |
| --- | --- |

| Pre-wave | `master-agent`, `migration-coordinator` |
| UPSTREAM (Gate 1) | `discovery-scout`, `data-strategist`, `business-analyst`, `logic-extractor` |
| MIDSTREAM (Gate 2) | `data-architect`, `data-modeler`, `data-steward`, `quality-gate`, `security-compliance` |
| DOWNSTREAM (Gate 3) | `downstream-executor`, `reconciliation`, `self-healing`, `documentation` |
| Post-wave | `iteration-improvement` |

Optional agents: `bi-semantic`, `code-generator`, `inventory-scout`, `agent-designer`

### 1.4 — Recommended reading before getting hands-on

Complete this reading in order:

1. [README.md](../README.md) — project overview (5 min)
2. This playbook to the end (you are here)
3. [COPILOT-AGENTS-GUIDE.md](COPILOT-AGENTS-GUIDE.md) — command reference (read the sections for the phases you will work in)
4. [PLAYBOOK-MIGRATION-OPERATIONS.md](PLAYBOOK-MIGRATION-OPERATIONS.md) — when you are ready to run your first real wave

Advanced documents (read when needed):

- [PRD-Agentic-Data-Migration-Factory.md](PRD-Agentic-Data-Migration-Factory.md) — requirements and acceptance criteria

- [OPERATING-MODEL-CANVAS-v2.md](OPERATING-MODEL-CANVAS-v2.md) — operating model and agent permissions

- [SKILLS-BLUEPRINT-BY-GATE.md](SKILLS-BLUEPRINT-BY-GATE.md) — available skills per gate

---

## Section 2 — Set Up the Local Environment

### Prerequisites

Before starting, verify that you have the following installed:

| Tool | Minimum version | How to verify |
| --- | --- | --- |

| Python | 3.13+ | `python --version` |
| Git | any | `git --version` |
| VS Code | any | open the app |
| GitHub Copilot | active extension | icon in VS Code |

### Step 2.1 — Clone and open the workspace

```powershell
# Clone the repository (replace with the actual URL)
git clone <REPOSITORY-URL>

# Navigate to the project folder
cd "Data-Migration v3"

# Open in VS Code
code .

```

> If the project is already cloned, simply open the folder in VS Code: `File → Open Folder`.

### Step 2.2 — Create and activate the virtual environment

```powershell
# Create the venv
python -m venv .venv

# Activate on Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

# Activate on Linux/Mac
source .venv/bin/activate

```

You will see `(.venv)` at the beginning of the prompt — this confirms the venv is active.

> **Important:** always activate the venv before running any Python script. If the terminal was closed and reopened, run Activate again.

### Step 2.3 — Install dependencies

```powershell
pip install pytest pyyaml

```

There is no `requirements.txt` at this time — these two are the only dependencies of the governance framework.

### Step 2.4 — Validate the installation

```powershell
python -m pytest tests/ -q

```

Expected result:

```

189 passed in X.XXs

```

If you see `189 passed`, the environment is working correctly. Any failure indicates a configuration problem — see Section 6 (Troubleshooting).

---

## Section 3 — Activate the Agents in VS Code

### Step 3.1 — Confirm that GitHub Copilot is active

1. Open VS Code
2. Press `Ctrl+Alt+I` to open GitHub Copilot Chat
3. The chat panel should appear on the left or right side

If it does not appear, install the **GitHub Copilot Chat** extension from the VS Code Marketplace.

### Step 3.2 — Select an agent

1. In the Copilot Chat panel, click the mode selector in the upper left corner:
   ```

   [ Ask ▼ ]  ← click here
   ```

2. You will see the list of available agents (the `.chatmode.md` files in the `.github/agents/` folder)
3. Select the desired agent

### Step 3.3 — Test with master-agent

```

[Select: master-agent]
> hello

```

The agent should introduce itself with its command menu. If the introduction does not appear, try:

```

> *help

```

### Step 3.4 — Explore available commands

Each agent has commands prefixed with `*`. To see all of them:

```

> *help

```

To navigate the project without knowing which agent to use:

```

[Select: master-agent]
> *route
Context: [describe what you want to do]

```

The `master-agent` will recommend the correct agent.

---

## Section 4 — Understand the Project Structure

```

Data-Migration v3/
├── .github/
│   ├── agents/          ← 19 agents (.chatmode.md files)
│   └── skills/          ← 26 installed skills
├── scripts/             ← 23 Python governance modules
├── tests/               ← 189 automated tests
├── docs/                ← Project documentation
│   ├── PRD-...          ← Product requirements
│   ├── OPERATING-MODEL  ← Operating model
│   ├── COPILOT-AGENTS-GUIDE ← Command reference
│   ├── SKILLS-BLUEPRINT ← Skills per gate
│   ├── PLAYBOOK-MIGRATION-OPERATIONS.md ← Wave operations
│   └── PLAYBOOK-ONBOARDING.md ← This file
├── <name>-agent/        ← Each agent's folder with its outputs
│   ├── <agent>-outputs/ ← Artifacts generated by the agent
│   └── README.md
└── README.md            ← Project entry point

```

### Governance scripts (`scripts/` folder)

The Python scripts implement the validations that agents use internally. As a new member, you will likely interact with:

| Script | What it does |
| --- | --- |
| `validate_wave_config.py` | Validates the wave configuration YAML |
| `gate_score_report.py` | Calculates the GateScore for a gate |
| `validate_gate1_artifacts.py` | Checks required Gate 1 artifacts |
| `validate_gate2_artifacts.py` | Checks required Gate 2 artifacts |
| `validate_gate3_artifacts.py` | Checks required Gate 3 artifacts |
| `kpi_dashboard_report.py` | Calculates and reports project KPIs |
| `wave_status_tracker.py` | Consolidated wave status across all 3 gates |
| `governance_policy.py` | Tool-use policy engine per agent |
| `data_contract_validator.py` | Declarative data contract validation |

See [scripts/README.md](../scripts/README.md) for the full list of all 23 modules.

---

## Section 5 — Run Your First Simulated Wave

This section guides you through a wave simulation to learn the flow without risk. Use fictitious data.

### Step 5.1 — Create a sample wave-config

```powershell
# Create a folder for the test wave
mkdir wave-test-onboarding

```

Create the file `wave-test-onboarding/wave-config.yaml`:

```yaml
wave_id: WAVE-ONBOARDING
wave_name: "Onboarding Test Wave"
scope:
  entities:
    - Customers
    - Orders

source:
  type: sql_server
  database: NORTHWIND_DEV
target:
  platform: "target to be defined"
discovery_owner: discovery-scout
status: in_progress

```

### Step 5.2 — Validate the config

```powershell
python scripts/validate_wave_config.py

```

### Step 5.3 — Simulate Gate 1 with discovery-scout

```text
[Select: discovery-scout]
> *scan-repo
Source: SQL Server 2019, database: NORTHWIND_DEV
Scope: Customers and Orders tables (onboarding simulation)

> *classify
Classify by complexity

```

Observe the output format — `inventory-report.md` with Low/Medium/High complexity.

### Step 5.4 — Simulate the business problem

```text
[Select: data-strategist]
> *define-problem
Project: WAVE-ONBOARDING — test migration
Objective: learn the factory workflow

```

### Step 5.5 — Calculate a simulated GateScore

```text
[Select: migration-coordinator]
> *gate1-validate
Wave: WAVE-ONBOARDING

```

If any required artifact is missing, the agent will point out what is needed. This is the expected behavior — learn what each gate requires by observing the blockers.

### Step 5.6 — Read the Operations Playbook

With the simulated flow in mind, read [PLAYBOOK-MIGRATION-OPERATIONS.md](PLAYBOOK-MIGRATION-OPERATIONS.md) end to end. Now you will understand each step with practical context.

---

## Section 6 — Troubleshooting

### Problem: `189 passed` does not appear

**Most common cause:** pyyaml not installed.

```powershell
pip install pyyaml
python -m pytest tests/ -q

```

### Problem: agents do not appear in VS Code

**Check:**

1. The GitHub Copilot Chat extension is installed and active
2. The open workspace is the project root folder (where `.github/` resides)
3. The `.chatmode.md` files exist in `.github/agents/`

```powershell
# Check if the files exist
Get-ChildItem .github\agents\ -Filter "*.chatmode.md" | Measure-Object
# Expected: 21 files (19 active + 1 deprecated + 1 optional)

```

### Problem: venv does not activate (PowerShell)

```powershell
# If there is a script execution error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try activating again:
.\.venv\Scripts\Activate.ps1

```

### Problem: I don't know which agent to use

```text
[Select: master-agent]
> *route
[describe what you want to do]

```

The `master-agent` always recommends the correct agent for the context.

### Problem: the agent does not understand my context

- Always provide: wave name, in-scope entities, source and target platforms

- Use `*` commands instead of free-form language when available

- If the agent gets lost, open a new chat and select the agent again

---

## Section 7 — Quick Reference for Setup Commands

```powershell
# Full setup of a new environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install pytest pyyaml
python -m pytest tests/ -q    # should return 189 passed

# Day-to-day commands
python -m pytest tests/ -q                                             # all tests
python -m pytest tests/test_gate_score_report.py -v                   # specific test
python -m scripts.validate_wave_config WAVE-001.yaml                  # validate wave-config
python -m scripts.validate_agent_contracts --root .                   # agent contracts
python -m scripts.validate_gate3_artifacts downstream-executor-agent/downstream-outputs

```

---

## Section 8 — Next Steps

After completing sections 1 through 5, you are ready to:

| Goal | What to do |
| --- | --- |

| Run a real wave | Follow [PLAYBOOK-MIGRATION-OPERATIONS.md](PLAYBOOK-MIGRATION-OPERATIONS.md) |
| Deep dive into a specific agent | Read the corresponding section in [COPILOT-AGENTS-GUIDE.md](COPILOT-AGENTS-GUIDE.md) |
| Understand permissions and governance | Read [OPERATING-MODEL-CANVAS-v2.md](OPERATING-MODEL-CANVAS-v2.md) |
| See the quality model (GateScore) | Read [PRD-Agentic-Data-Migration-Factory.md](PRD-Agentic-Data-Migration-Factory.md) section 4 |
| Explore available skills | Read [SKILLS-BLUEPRINT-BY-GATE.md](SKILLS-BLUEPRINT-BY-GATE.md) |

---

## Onboarding Completion Checklist

- [ ] Read sections 1 through 5 of this playbook

- [ ] Python environment configured with active venv

- [ ] `pip install pytest pyyaml` executed

- [ ] `189 passed` confirmed in `pytest`

- [ ] GitHub Copilot Chat open in VS Code

- [ ] `master-agent` activated and `*help` responded

- [ ] Simulated wave created and Gate 1 attempted

- [ ] [PLAYBOOK-MIGRATION-OPERATIONS.md](PLAYBOOK-MIGRATION-OPERATIONS.md) read

- [ ] Knew which agent to use for each phase
