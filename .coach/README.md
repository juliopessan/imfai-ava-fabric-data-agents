# DMF Coach — Continuous Best-Practices Mentor

**Status:** 🟡 Phase 1 (MVP) — Telemetry + Anti-pattern Engine  
**Timeline:** 4 sprints (8 weeks)

---

## What is DMF Coach?

An integrated best-practices mentoring system that monitors Data Migration Factory agent executions and provides **continuous, actionable feedback** to improve wave quality, reduce costs, and identify reusable patterns.

Inspired by the [AI Engineer Coach](https://github.com/juliopessan/AI-Engineering-Coach) — which analyzes coding-assistant usage — DMF Coach applies the same principles to agentic migrations:

- **Observe** → Timeline of agent executions + costs
- **Measure** → Tokens, time, cost per agent per wave
- **Improve** → 6+ anti-pattern rules with scoring adjustments
- **Level Up** → Skill discovery + context health scoring
- **Context Health** → Audit .agent.md + skill loading

---

## Quick Start

### Installation

```bash
cd /path/to/imfai-ava-fabric-data-agents

# Copy coach schema and rules
mkdir -p .coach/{rules,telemetry,reports}

# Install dependencies (already in requirements.txt)
pip install pyyaml jsonschema
```

### Use in Your Agent

```python
from src.shared.coaches import telemetry_collector

# After agent execution
result = migration_coordinator.spawn_agent(...)

telemetry_collector.log_execution(
    agent_id="data-architect",
    wave="financeiro_wave_2",
    gate=1,
    model="claude-opus-4-1",
    tokens_in=12500,
    tokens_out=8300,
    artifact_filename="architecture.md",
    artifact_size=45600,
    execution_time_sec=130,
    artifact_sections=12,
    artifact_entities=87,
)
```

### Analyze a Wave

```bash
python -m src.shared.coaches.cli --wave bradesco_wave_2 --action analyze
# Output: .coach/reports/bradesco-wave-2-analysis.html
```

---

## Directory Structure

```
imfai-ava-fabric-data-agents/
├── .coach/                              Coach data store
│   ├── telemetry-schema.json            Event schema (JSON Schema)
│   ├── rules/                           Anti-pattern rule definitions
│   │   ├── wave-completion.yaml
│   │   ├── sttm-stability.yaml
│   │   ├── model-overreliance.yaml
│   │   ├── context-bloat.yaml
│   │   ├── silent-executor.yaml
│   │   └── gate-regression.yaml
│   ├── telemetry/                       Execution logs (JSONL)
│   │   ├── bradesco_wave_2_2026-06-18.jsonl
│   │   └── ...
│   └── reports/                         Generated analysis reports
│       ├── bradesco-wave-2-analysis.html
│       └── ...
│
├── src/shared/coaches/                  Coach implementation
│   ├── __init__.py
│   ├── telemetry_collector.py           Event capture & storage
│   ├── anti_pattern_detector.py         Pattern detection engine (6 rules)
│   ├── context_health_scorer.py         [TODO] .agent.md audit
│   ├── skill_finder.py                  [TODO] Pattern discovery
│   └── cli.py                           [TODO] CLI for analysis
│
├── src/shared/tests/
│   └── test_coaches/                    Coach unit tests
│       ├── test_telemetry.py
│       ├── test_anti_patterns.py
│       └── ...
│
└── docs/
    └── COACH-INTEGRATION-BLUEPRINT.md   Full design doc
```

---

## Anti-Patterns (6 Critical Rules)

| # | Name | Severity | Score Impact | Trigger |
|---|------|----------|--------------|---------|
| 1 | Wave Completion | HIGH | -15 | Entity coverage < 90% |
| 2 | STTM Stability | MEDIUM | -10 | STTM regenerated > 2× in 2h |
| 3 | Model Overreliance | LOW | -5 | GPT-4/Opus used for parametric tasks |
| 4 | Context Bloat | MEDIUM | -10 | Context > 70% OR artifact > 40 KB |
| 5 | Silent Executor Failure | CRITICAL | -30 | Output < 1000 tokens AND artifact < 10 KB |
| 6 | Gate Score Regression | HIGH | -20 | GateScore drops > 5% WoW |

### Example: Silent Executor Failure

```python
from src.shared.coaches import anti_pattern_detector

pattern = anti_pattern_detector.detect_silent_executor_failure(
    executor_output_tokens=847,    # < 1000 threshold
    executor_artifact_size=2100,   # < 10 KB threshold
    executor_output_text="Ready to apply..."
)

if pattern:
    print(f"⚠️ {pattern.name} detected!")
    print(f"Action: {pattern.action}")
    print(f"Score impact: {pattern.score_impact} points")
    # → Output: Auto-trigger self-healing agent
```

---

## How It Integrates with DMF

### Hook Points

#### 1. **migration-coordinator** (before spawn)
```python
# Log telemetry for every agent execution
telemetry_collector.log_execution(...)
```

#### 2. **quality-gate** (before Gate sign-off)
```python
# Detect anti-patterns and adjust GateScore
anti_patterns = anti_pattern_detector.detect_all(...)
adjusted_score = base_score + sum(ap.score_impact for ap in anti_patterns)
```

#### 3. **wave_status_tracker** (after Gate 3)
```python
# Discover skills, audit context health
context_health = context_health_scorer.audit(wave)
skills = skill_finder.discover(wave)
```

---

## Roadmap

### Sprint 1 (2 weeks) — Telemetry MVP
- [x] `telemetry_collector.py`
- [x] Telemetry schema (JSON)
- [ ] Hook in `migration-coordinator`
- [ ] Basic dashboard (timeline + costs)

### Sprint 2 (2 weeks) — Anti-Pattern Engine
- [x] `anti_pattern_detector.py` (6 rules)
- [ ] YAML rule definitions
- [ ] Integration in `quality-gate`
- [ ] Dashboard: Anti-Patterns heatmap

### Sprint 3 (2 weeks) — Context Health + Skills
- [ ] `context_health_scorer.py`
- [ ] `skill_finder.py`
- [ ] Recomendations UI
- [ ] Dashboard: Skills opportunity + Agent health

### Sprint 4 (1 week) — Gamification + Docs
- [ ] Achievements / badges
- [ ] Learning center stubs
- [ ] CLI (`coach analyze --wave ...`)
- [ ] Integration guide

---

## Development

### Run Tests

```bash
python -m pytest src/shared/tests/test_coaches/ -v
```

### Add a Custom Rule

1. Create `.coach/rules/my-rule.yaml`:
```yaml
---
name: "My Custom Rule"
category: "custom"
severity: "medium"
description: "Rule description"
trigger:
  condition: "{{ artifact.size }} > 100000"
  flag_if: true
score_impact: -10
action: "What to do about it"
```

2. Detector loads it automatically via `_load_custom_rules()`

### Debug Telemetry

```bash
# View raw JSONL events
cat .coach/telemetry/bradesco_wave_2_2026-06-18.jsonl | python -m json.tool

# Summarize wave
python -c "
from src.shared.coaches import telemetry_collector
summary = telemetry_collector.collector.summarize_wave('bradesco_wave_2')
import json
print(json.dumps(summary, indent=2))
"
```

---

## Next Steps

1. **Hook telemetry into migration-coordinator** (log every agent spawn)
2. **Create 6 anti-pattern YAML rules** (parametrize detection thresholds)
3. **Test on historical data** (bradesco Wave 2 re-analyzed)
4. **Build dashboard** (HTML template with Chart.js)
5. **Integrate into quality-gate** (adjust GateScore)
6. **Package skills** (promote discovered patterns to `.github/skills/`)

---

## FAQ

**Q: Where do events get stored?**  
A: `.coach/telemetry/{wave}_{date}.jsonl` — one JSON object per line, never leaves your machine.

**Q: Can I customize anti-pattern thresholds?**  
A: Yes, create `.coach/rules/my-rule.yaml` and edit thresholds.

**Q: How does this affect GateScore?**  
A: Anti-patterns deduct points: GateScore = base_score + Σ(ap.score_impact). Gate approval threshold remains 0.85.

**Q: Can Coach auto-pause a wave?**  
A: Not yet (Phase 4). Currently advisory only.

**Q: Who discovers and approves skills?**  
A: Skill Finder proposes. Approval process TBD (likely: code-review + SKILL.md PR).

---

## References

- [AI Engineer Coach](https://github.com/juliopessan/AI-Engineering-Coach) — Inspiration & design
- [COACH-INTEGRATION-BLUEPRINT.md](../docs/COACH-INTEGRATION-BLUEPRINT.md) — Full design
- [Lessons Learned](./lessons-learned.md) — Anti-pattern rationale

---

**Status:** 🟡 MVP Phase | **Version:** 0.1.0 | **Last Updated:** 2026-06-18
