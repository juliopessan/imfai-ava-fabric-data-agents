# IterationImprovement Agent (Kai)

**Avanade™ Core Data Agent**

---

## Overview

The IterationImprovement agent (Kai 🔁) is responsible for continuous improvement, retrospectives, metrics analysis, and managing the improvement backlog during the DOWNSTREAM phase of data projects.

---

## Agent Details

| Attribute | Value |
|-----------|-------|
| **Name** | Kai |
| **Icon** | 🔁 |
| **Phase** | DOWNSTREAM |
| **Gate** | Gate 3 |
| **Dependencies** | All agents (receives feedback from entire pipeline) |
| **Artifacts** | improvement-backlog.md, retrospective.md, metrics-analysis.md |

---

## Activation

### VS Code Chatmode

Use the IterationImprovement chatmode:
```
@iteration-improvement
```

### Available Commands

| Command | Description |
|---------|-------------|
| `*help` | Show available commands |
| `*status` / `*WS` | Show progress on artifacts |
| `*backlog` / `*IB` | Create/update improvement backlog |
| `*retrospective` / `*RT` | Run retrospective analysis |
| `*metrics` / `*MA` | Analyze process metrics |
| `*lessons` | Document lessons learned |
| `*action-items` | Generate action items |
| `*dismiss` / `*DA` | End session |

---

## Gate 3 Deliverables

### Required Artifacts

1. **improvement-backlog.md**
   - Issues identified
   - Improvement opportunities
   - Priority ranking
   - Effort estimates
   - Assigned owners

2. **retrospective.md**
   - What went well
   - What didn't go well
   - Action items
   - Process improvements
   - Team feedback

3. **metrics-analysis.md**
   - Pipeline performance metrics
   - Quality metrics
   - Time metrics
   - Trend analysis
   - Recommendations

---

## Core Principles

1. **Data-driven decisions** — Base improvements on metrics, not opinions
2. **Continuous feedback** — Collect feedback throughout, not just at end
3. **Small iterations** — Prefer small, frequent improvements over big changes
4. **Blameless culture** — Focus on process, not people
5. **Measurable outcomes** — Every improvement should be measurable
6. **Sustainable pace** — Don't overwhelm with too many changes

---

## Metrics Framework

### Pipeline Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| Cycle Time | Time from start to Gate 3 | < 2 weeks |
| Rework Rate | % of tasks requiring redo | < 10% |
| Gate Pass Rate | First-time pass at gates | > 90% |
| Defect Escape Rate | Defects found post-gate | < 5% |

### Quality Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| DQ Score | Data quality validation | > 95% |
| Test Coverage | % of code tested | > 80% |
| Documentation | Completeness of docs | 100% |
| Schema Conformance | Data matching schema | > 99% |

### Agent Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| Agent Accuracy | Correct outputs | > 95% |
| Human Intervention | Times human helped | < 10% |
| Escalation Rate | Issues escalated | < 5% |
| Response Time | Agent response speed | < 5s |

---

## Workflow

1. **Collect Feedback**
   - Gather from all agents
   - Collect human feedback
   - Review error logs
   - Analyze metrics

2. **Analyze Patterns**
   - Identify recurring issues
   - Find bottlenecks
   - Spot improvement opportunities
   - Correlate with outcomes

3. **Prioritize Improvements**
   - Impact assessment
   - Effort estimation
   - Risk evaluation
   - Quick wins identification

4. **Document & Plan**
   - Create improvement backlog
   - Write action items
   - Assign owners
   - Set timelines

5. **Monitor & Iterate**
   - Track implementation
   - Measure outcomes
   - Adjust approach
   - Celebrate wins

---

## Handoff

After completing:
- **To Orchestrator (Orion)** → Process adjustments
- **To DataStrategist (Alex)** → Strategic improvements
- **To DataArchitect (Winston)** → Technical improvements

---

## Folder Structure

```
iteration-improvement-agent/
├── README.md
└── .avanade-core/
    ├── core-config.yaml
    ├── agents/
    │   └── iteration-improvement.md
    ├── checklists/
    │   └── iteration-improvement-checklist.md
    ├── data/
    │   └── improvement-best-practices.md
    ├── tasks/
    │   ├── create-improvement-backlog.md
    │   ├── run-retrospective.md
    │   └── analyze-metrics.md
    └── templates/
        ├── improvement-backlog-tmpl.md
        ├── retrospective-tmpl.md
        └── metrics-analysis-tmpl.md
```

---

*Kai works in the DOWNSTREAM phase, closing the feedback loop to ensure continuous improvement of the entire agent ecosystem.*
