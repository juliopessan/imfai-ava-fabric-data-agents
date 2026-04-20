# Generate Healing Report Task

**Task ID:** generate-healing-report  
**Agent:** Phoenix (Self-Healing)  
**Version:** 1.0  
**Command:** `*healing-report`  
**Phase:** DOWNSTREAM

---

## Purpose

Generate a comprehensive healing report with all diagnosis attempts, fix strategies used, success/failure outcomes, patterns learned, time spent, and escalations needed. Provides actionable summary for stakeholders and audit trail.

---

## Prerequisites

- At least one healing cycle completed for the pipeline(s)
- Healing logs available in `healing-logs/`

---

## Inputs

| Input | Type | Required | Description |
|-------|------|----------|-------------|
| pipeline_id | string | No | Specific pipeline (omit for full report) |
| scope | string | No | "pipeline", "wave", or "project" (default: "pipeline") |
| wave_id | string | No | Wave identifier (for wave-level reports) |
| include_diffs | bool | No | Include code diffs in report (default: false) |

---

## Execution Steps

### Step 1: Collect Healing Data

```
IF pipeline_id provided:
  LOAD healing-logs/{pipeline_id}.json
  LOAD healing-logs/{pipeline_id}_attempts.json
  LOAD healing-logs/{pipeline_id}_diagnosis.json
  SET scope = "pipeline"
ELSE IF wave_id provided:
  LOAD ALL healing-logs/*.json for pipelines in wave
  SET scope = "wave"
ELSE:
  LOAD ALL healing-logs/*.json
  SET scope = "project"

LOG "📊 Coletando dados de healing ({scope}): {count} pipelines"
```

### Step 2: Calculate Metrics

```
CALCULATE aggregate metrics:
  total_pipelines_healed: count(status == "HEALED")
  total_pipelines_escalated: count(status == "ESCALATED")
  total_pipelines_partial: count(status == "PARTIAL")
  total_pipelines_in_progress: count(status == "IN_PROGRESS")
  
  healing_rate: healed / (healed + escalated + partial) * 100
  
  avg_attempts_to_fix: mean(successful_attempt_number)
  avg_time_to_fix: mean(fix_duration_minutes)
  
  strategy_breakdown:
    rule_based_success: count(strategy == "rule_based" AND success)
    llm_alt_prompt_success: count(strategy == "llm_alternative_prompt" AND success)
    llm_diff_model_success: count(strategy == "llm_different_model" AND success)
  
  error_distribution:
    FOR EACH pattern_id:
      count, success_rate, avg_attempts
  
  patterns_learned: count(new patterns added to MLflow)
  patterns_promoted: count(patterns promoted to rule-based)
  regressions_detected: count(regression events)
  
  total_time_spent: sum(all fix durations)
  cost_savings: estimated_human_hours_saved * hourly_rate

LOG "📈 Healing rate: {healing_rate}% ({healed}/{total})"
```

### Step 3: Generate Report

```
LOAD template FROM .avanade-core/templates/healing-report-tmpl.md

POPULATE template with:
  - Header (pipeline/wave/project info, date, agent)
  - Executive Summary (healing rate, key metrics)
  - Error Distribution (pie chart data)
  - Attempt Details (per-pipeline breakdown)
  - Strategy Effectiveness (which strategies work best)
  - Patterns Learned (new patterns from this cycle)
  - Escalations (details of what couldn't be fixed)
  - Recommendations (improvements, new patterns to create)
  - Appendix (diffs if include_diffs == true)

SAVE report to:
  IF scope == "pipeline":
    healing-outputs/error-analysis/{pipeline_id}_healing-report.md
  ELSE IF scope == "wave":
    healing-outputs/error-analysis/{wave_id}_healing-report.md
  ELSE:
    healing-outputs/error-analysis/project-healing-report.md
```

### Step 4: Generate Summary Table

```
DISPLAY summary:

┌────────────────────────────────────────────────────────┐
│              🔧 HEALING REPORT SUMMARY                 │
├────────────────────────────────────────────────────────┤
│  Scope: {scope}           Date: {today}                │
│  Pipelines Processed: {total}                          │
│                                                        │
│  ✅ Healed:      {healed}  ({healing_rate}%)           │
│  ⚠️ Partial:     {partial}                             │
│  ❌ Escalated:   {escalated}                           │
│  🔄 In Progress: {in_progress}                         │
│                                                        │
│  Avg Attempts:   {avg_attempts}                        │
│  Avg Fix Time:   {avg_time} min                        │
│  Patterns Learned: {learned}                           │
│  Cost Savings:   ~{savings} hours saved                │
└────────────────────────────────────────────────────────┘
```

---

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| `healing-outputs/error-analysis/{id}_healing-report.md` | Markdown | Full healing report |
| Console summary | Text | Quick summary table |

---

## Report Sections

1. **Executive Summary** — High-level healing rate and key takeaways
2. **Error Distribution** — Breakdown by error type/pattern
3. **Fix Attempt Details** — Per-pipeline, per-attempt breakdown
4. **Strategy Effectiveness** — Success rates by strategy (rule/LLM/model)
5. **Patterns Learned** — New patterns added to knowledge base
6. **Regressions** — Any regressions detected and how handled
7. **Escalations** — What was escalated and why
8. **Time Analysis** — Time spent per pipeline, per attempt
9. **Recommendations** — Suggested improvements for next cycle
10. **Appendix** — Code diffs (optional)
