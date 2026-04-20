# 🔧 Self-Healing Agent

> **AI-Agent Migration Factory™ — Automatic Error Recovery & Self-Healing**

---

## Overview

The **Self-Healing Agent** attempts automatic correction of errors detected by **Vera ✅** (quality gate rejections) or **Shield 🔒** (compliance violations). Uses a **hybrid approach**: LLM-based reasoning for novel errors and a rule-based engine for known patterns. Learns from successful fixes via **MLflow**, continuously expanding its knowledge base.

**Key behavior:** Max **3 retry attempts** before escalating to human via **Orion 🧭**. Each attempt uses a progressively different strategy — from deterministic rules to LLM creativity — ensuring maximum fix coverage with minimal risk.

**Competitive differentiator** — no other migration tool on the market offers automatic self-healing with learning capabilities. Phoenix transforms rejected pipelines into approved ones without human intervention in **75%+ of cases**.

---

## Agent Details

| Property       | Value                                                           |
|----------------|-----------------------------------------------------------------|
| **Persona**    | Phoenix                                                         |
| **Icon**       | 🔧                                                              |
| **Phase**      | DOWNSTREAM                                                      |
| **Gate**       | 2 (support)                                                     |
| **Autonomy**   | Level 3 — Monitored                                             |
| **Engine**     | LLM + Rule-based Fixes + Learning System (MLflow)               |
| **Activation** | `@self-healing`                                                 |

---

## Commands

| Command              | Description                                                  |
|----------------------|--------------------------------------------------------------|
| `*help`              | Show available commands and usage guide                      |
| `*diagnose`          | Classify error type, parse stack trace, perform root cause analysis |
| `*fix`               | Apply fix strategy (rule-based → LLM alt prompt → LLM diff model) |
| `*verify`            | Re-submit fixed code to Vera for re-validation loop         |
| `*learn-pattern`     | Extract successful fix pattern and store in MLflow           |
| `*healing-report`    | Generate comprehensive healing report with all attempts      |
| `*yolo`              | Auto-execute full diagnose→fix→verify cycle for known patterns |

---

## Deliverables

| Output                                        | Description                                         |
|-----------------------------------------------|-----------------------------------------------------|
| `fixed-code/{pipeline_id}.py`                 | Corrected pipeline code after successful healing     |
| `healing-log/{pipeline_id}.json`              | Detailed log of all diagnosis, attempts, and results |
| `error-analysis.md`                           | Deep analysis of errors with root cause trees        |

---

## Integration Map

### Upstream (Inputs)

| Agent             | Artifact                              | Description                                          |
|-------------------|---------------------------------------|------------------------------------------------------|
| **Vera ✅**        | `validation-report/{pipeline_id}.json`| Validation errors and rejection details              |
| **Shield 🔒**     | `compliance-report/{pipeline_id}.json`| Compliance issues (PII, LGPD, SOX)                  |
| **Coda ⚙️**       | `generated-code/{pipeline_id}.py`     | Original generated code for patching                 |

### Downstream (Outputs)

| Agent               | Artifact                        | Condition        | Description                                    |
|---------------------|---------------------------------|------------------|------------------------------------------------|
| **Vera ✅**          | `fixed-code/{pipeline_id}.py`   | Re-validation    | Fixed code sent back for quality re-check      |
| **Orion 🧭**        | `healing-log/{pipeline_id}.json`| Escalation       | Escalation after 3 failed attempts             |

---

## How It Works

```
┌──────────────────────────────────────────────────────────┐
│                  SELF-HEALING FLOW                        │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  1. Receive rejected code + validation report            │
│  2. DIAGNOSE: Classify error, parse stack trace          │
│     ├─ Match against known patterns (MLflow registry)    │
│     └─ LLM root cause analysis if novel error            │
│  3. FIX: Apply strategy based on attempt number          │
│     ├─ Attempt 1: Rule-based fix (deterministic)         │
│     ├─ Attempt 2: LLM with alternative prompt            │
│     └─ Attempt 3: LLM with different model               │
│  4. VERIFY: Re-submit to Vera ✅ for validation          │
│     ├─ Compare scores before/after                       │
│     └─ Confirm no regression introduced                  │
│  5. LEARN: If fixed successfully                         │
│     ├─ Extract error signature + fix pattern             │
│     └─ Store in MLflow for future use                    │
│  6. ESCALATE: If 3 attempts fail → Orion 🧭             │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## Fix Strategy Matrix

| Attempt | Strategy              | Risk   | Description                                            |
|---------|-----------------------|--------|--------------------------------------------------------|
| 1       | Rule-based            | Low    | Deterministic fix from known pattern registry          |
| 2       | LLM Alternative Prompt| Medium | LLM with focused repair prompt and error context       |
| 3       | LLM Different Model   | Higher | Stronger/different LLM model for creative fix          |
| —       | Escalate              | —      | Human intervention via Orion after all attempts fail   |

---

## Known Error Patterns

| Pattern ID         | Description                    | Auto-Fix Success Rate |
|--------------------|--------------------------------|-----------------------|
| `type_mismatch`    | Data type incompatibility      | ~95%                  |
| `null_handling`    | Missing null/None handling     | ~90%                  |
| `sql_syntax`       | SQL dialect translation errors | ~85%                  |
| `import_missing`   | Missing Python/PySpark imports | ~98%                  |
| `column_not_found` | Column name mismatch           | ~88%                  |
| `partition_error`  | Partitioning strategy issues   | ~80%                  |
| `schema_evolution` | Schema drift handling          | ~75%                  |
| `encoding_error`   | Character encoding issues      | ~92%                  |
| `date_format`      | Date/timestamp format mismatch | ~93%                  |
| `join_condition`   | Join key mismatch or type diff | ~85%                  |

---

## Quick Start

```bash
# Diagnose an error from validation report
@self-healing *diagnose --pipeline=PL_CUSTOMER_MASTER

# Apply fix (auto-selects strategy based on attempt #)
@self-healing *fix --pipeline=PL_CUSTOMER_MASTER

# Verify fix by re-submitting to Vera
@self-healing *verify --pipeline=PL_CUSTOMER_MASTER

# Learn from a successful fix
@self-healing *learn-pattern --pipeline=PL_CUSTOMER_MASTER

# Full healing report
@self-healing *healing-report --pipeline=PL_CUSTOMER_MASTER

# YOLO mode: auto-execute full cycle for known patterns
@self-healing *yolo --pipeline=PL_CUSTOMER_MASTER
```

---

## Configuration

See `.avanade-core/core-config.yaml` for error patterns, fix strategies, and dependencies.

---

## Related Agents

| Agent              | Relationship        | Description                                 |
|--------------------|---------------------|---------------------------------------------|
| **Vera ✅**         | Upstream (input)    | Provides validation errors for rejected code |
| **Shield 🔒**      | Upstream (input)    | Provides compliance violation details        |
| **Coda ⚙️**        | Upstream (input)    | Provides original generated code             |
| **Vera ✅**         | Downstream (verify) | Re-validates fixed code in feedback loop     |
| **Orion 🧭**       | Downstream (escal.) | Receives escalations after 3 failed attempts |
