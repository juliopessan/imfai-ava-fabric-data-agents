# Route Next Task

**Task ID:** route-next  
**Agent:** Orchestrator  
**Version:** 1.0

---

## Purpose

Analyze current project state and route to the most appropriate agent based on:
- Current phase (UPSTREAM, MIDSTREAM, DOWNSTREAM)
- Pending artifacts
- User request context
- Agent availability and expertise

---

## Agent Registry

### UPSTREAM Agents (Discovery Phase)

| Agent | Expertise | Primary Artifacts |
|-------|-----------|-------------------|
| **DataStrategist** | Strategy, KPIs, Problem Definition | problem-statement.md, kpis.md, success-criteria.md |
| **BusinessAnalyst** | Requirements, Mapping, Questions | sttm.md, analytical-questions.md, dq-initial.md |

### MIDSTREAM Agents (Design Phase)

| Agent | Expertise | Primary Artifacts |
|-------|-----------|-------------------|
| **DataArchitect** | Architecture, Data Model, Decisions | architecture.md, data-model.md, decisions.md |
| **DataSteward** | Governance, DQ Rules, Compliance | dq-rules.md, governance.md, monitoring-spec.md |

### DOWNSTREAM Agents (Implementation Phase)

| Agent | Expertise | Primary Artifacts |
|-------|-----------|-------------------|
| **DataFlow** | DDL, ETL, Testing, Profiling | ddl/, etl/, tests/, quality/ |
| **InsightForge** | BI, Dashboards, DAX, Semantic Model | dashboards/, dax/, reports/ |

### CORE Agents (Cross-Phase)

| Agent | Expertise | Primary Artifacts |
|-------|-----------|-------------------|
| **Orchestrator** | Gates, Routing, State Management | gate-reports/, audit-trail.md |
| **DeliveryPro** | Delivery, Risks, Dependencies | delivery/, risks/, dependencies/ |

---

## Routing Logic

### Step 1: Determine Current Phase

```
IF gate-1-report shows PASS:
  IF gate-2-report shows PASS:
    → Current Phase: DOWNSTREAM
  ELSE:
    → Current Phase: MIDSTREAM
ELSE:
  → Current Phase: UPSTREAM
```

### Step 2: Identify Missing Artifacts

Based on current phase, list missing required artifacts.

### Step 3: Match Request to Agent

| User Intent | Recommended Agent |
|-------------|-------------------|
| "Define the problem" | DataStrategist |
| "What KPIs should we track" | DataStrategist |
| "Map sources to targets" | BusinessAnalyst |
| "What questions should data answer" | BusinessAnalyst |
| "Design the architecture" | DataArchitect |
| "Create data model" | DataArchitect |
| "Define quality rules" | DataSteward |
| "Governance requirements" | DataSteward |
| "Create tables" | DataFlow |
| "Write ETL" | DataFlow |
| "Profile the data" | DataFlow |
| "Create dashboard" | InsightForge |
| "Write DAX measures" | InsightForge |
| "Project status" | Orchestrator |
| "Validate gate" | Orchestrator |
| "Delivery planning" | DeliveryPro |
| "Risk assessment" | DeliveryPro |

### Step 4: Generate Routing Recommendation

---

## Execution Steps

### Step 1: Analyze Request

Parse user input to identify:
- Explicit agent mention (if any)
- Task type keywords
- Artifact mentions
- Phase indicators

### Step 2: Check Project State

Read current project state:
- Which artifacts exist
- Which gates passed
- Current phase

### Step 3: Apply Routing Rules

```
IF explicit agent requested AND agent exists:
  → Route to requested agent

ELSE IF task matches agent expertise:
  → Route to matching agent

ELSE IF phase is UPSTREAM AND missing upstream artifacts:
  → Route to DataStrategist or BusinessAnalyst

ELSE IF phase is MIDSTREAM AND missing midstream artifacts:
  → Route to DataArchitect or DataSteward

ELSE IF phase is DOWNSTREAM:
  → Route to DataFlow or InsightForge based on task

ELSE:
  → Return to Orchestrator with clarification request
```

### Step 4: Output Routing Decision

---

## Output Format

```markdown
# 🧭 Routing Decision

**Request:** {user_request_summary}  
**Current Phase:** {phase}  
**Date:** {date}

---

## Analysis

**Detected Intent:** {intent}  
**Keywords Found:** {keywords}  
**Phase Match:** {phase_match}

---

## Recommended Agent

**Agent:** {agent_name}  
**Icon:** {agent_icon}  
**Rationale:** {why_this_agent}

---

## Context for Agent

To use this agent, activate the appropriate chat mode:

**Chatmode:** `@{agent_id}`

**Suggested Command:** `*{command}`

**Context to Provide:**
{relevant_context_for_agent}

---

## Alternative Agents

If the recommended agent doesn't fit your needs:

| Agent | Use When |
|-------|----------|
| {alt_agent_1} | {when_to_use} |
| {alt_agent_2} | {when_to_use} |

---

*Routing performed by Orchestrator Agent*
```

---

## Routing Examples

### Example 1: New Project
```
Request: "I want to start a new data project"
Phase: UPSTREAM
→ Route to: DataStrategist
→ Reason: Start with problem definition and KPIs
→ Command: *define-problem
```

### Example 2: Post-Gate-1
```
Request: "Gate 1 passed, what's next?"
Phase: MIDSTREAM
→ Route to: DataArchitect
→ Reason: Design phase begins with architecture
→ Command: *create-architecture
```

### Example 3: Implementation Ready
```
Request: "Architecture approved, create tables"
Phase: DOWNSTREAM
→ Route to: DataFlow
→ Reason: Implementation with DDL generation
→ Command: *generate-ddl
```

### Example 4: Reporting Need
```
Request: "Create KPI dashboard"
Phase: DOWNSTREAM
→ Route to: InsightForge
→ Reason: BI and visualization expertise
→ Command: *create-dashboard
```

---

## Error Handling

```
IF no matching agent found:
  → Return: "Unable to determine best agent. Please clarify your request."
  → Suggest: List available agents with descriptions

IF multiple agents equally relevant:
  → Return: "Multiple agents can help. Please choose:"
  → List: Relevant agents with descriptions

IF agent not available:
  → Return: "Requested agent not configured in workspace."
  → Suggest: Similar available agent
```
