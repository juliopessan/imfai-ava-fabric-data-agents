# ⚙️ Code Generator Agent

> **AI-Agent Migration Factory™ — Multi-Platform Code Generation & Optimization**

---

## Overview

The **Code Generator Agent** converts platform-agnostic pseudocode from **Logan 🧠** into native target platform code (Databricks PySpark, SQL, Scala). Generates unit tests and job definitions. Uses a hybrid approach: **templates for common patterns + LLM for complex logic**.

This agent bridges the gap between abstract migration logic and production-ready, optimized code for the target data platform.

---

## Agent Details

| Property       | Value                                                    |
|----------------|----------------------------------------------------------|
| **Persona**    | Coda                                                     |
| **Icon**       | ⚙️                                                       |
| **Phase**      | MIDSTREAM                                                |
| **Gate**       | 2                                                        |
| **Autonomy**   | Level 2 — Supervised                                     |
| **Engine**     | LLM (GPT-4 + CodeLlama fine-tuned) + Template Engine     |
| **Activation** | `@code-generator`                                        |

---

## Commands

| Command              | Description                                              |
|----------------------|----------------------------------------------------------|
| `*help`              | Show available commands and usage guide                  |
| `*generate-code`     | Generate target platform code from pseudocode            |
| `*generate-tests`    | Generate unit tests (pytest) for generated code          |
| `*generate-job`      | Create Databricks job JSON definition                    |
| `*optimize`          | Apply performance optimizations to generated code        |
| `*batch-generate`    | Generate code for multiple pipelines in batch            |
| `*yolo`              | Autonomous generation for low-complexity pipelines       |

---

## Deliverables

| Output                                    | Description                                    |
|-------------------------------------------|------------------------------------------------|
| `generated-code/{pipeline_id}.py`         | Native target platform code (PySpark/SQL/Scala)|
| `generated-tests/{pipeline_id}_test.py`   | Unit tests for the generated code              |
| `job-definition/{pipeline_id}.json`       | Databricks job definition JSON                 |

---

## Integration Map

### Upstream (Inputs)

| Agent              | Artifact                    | Description                              |
|--------------------|-----------------------------|------------------------------------------|
| **Logan 🧠**       | `pseudocode/*.json`         | Platform-agnostic pseudocode definitions |
| **Coordinator 🎯** | `target-config.yaml`        | Target platform configuration            |

### Downstream (Outputs)

| Agent          | Artifact                          | Description                                   |
|----------------|-----------------------------------|-----------------------------------------------|
| **Vera ✅**     | `generated-code/`, `generated-tests/` | Code and tests for quality validation     |

---

## How It Works

```
┌──────────────────────────────────────────────────────┐
│                  CODE GENERATOR FLOW                 │
├──────────────────────────────────────────────────────┤
│                                                      │
│  1. Load pseudocode from Logan 🧠                    │
│  2. Classify transformation pattern                  │
│  3. Select approach:                                 │
│     ├─ Known pattern → Template Engine               │
│     └─ Complex logic → LLM (GPT-4 / CodeLlama)      │
│  4. Apply platform-specific optimizations            │
│  5. Format as Databricks notebook                    │
│  6. Generate unit tests                              │
│  7. Create job definition                            │
│  8. Deliver to Vera ✅ for validation                │
│                                                      │
└──────────────────────────────────────────────────────┘
```

---

## Supported Platforms

| Platform            | Languages / Frameworks                    |
|---------------------|-------------------------------------------|
| **Databricks**      | PySpark, Spark SQL, Delta Lake, Scala     |
| **Microsoft Fabric**| Spark, T-SQL                              |
| **Snowflake**       | Snowpark, SQL                             |

---

## Code Templates

| Template           | Use Case                                           |
|--------------------|-----------------------------------------------------|
| Simple ETL         | Source → Transform → Target (single source)         |
| Complex Join       | Multi-source joins with business logic              |
| Aggregation        | Group-by with window functions                      |
| SCD Type 2         | Slowly Changing Dimension with history tracking     |
| Incremental Load   | Change-based / watermark incremental loads          |
| Full Load          | Truncate-and-reload patterns                        |
| Delta Merge        | MERGE INTO with upsert logic                        |

---

## Quick Start

```
@code-generator *help
@code-generator *generate-code --pipeline=PL_CUSTOMER_MASTER --platform=databricks
@code-generator *generate-tests --pipeline=PL_CUSTOMER_MASTER
@code-generator *generate-job --pipeline=PL_CUSTOMER_MASTER --schedule="0 6 * * *"
@code-generator *optimize --pipeline=PL_CUSTOMER_MASTER
@code-generator *batch-generate --batch=batch_001.json
```

---

## File Structure

```
code-generator-agent/
├── README.md
├── .avanade-core/
│   ├── core-config.yaml
│   ├── agents/
│   │   └── code-generator.md
│   ├── tasks/
│   │   ├── generate-code.md
│   │   ├── generate-tests.md
│   │   ├── generate-job-definition.md
│   │   ├── optimize-code.md
│   │   └── batch-generate.md
│   ├── checklists/
│   │   └── code-generator-checklist.md
│   ├── data/
│   │   └── code-generation-best-practices.md
│   └── templates/
│       ├── pyspark-notebook-tmpl.md
│       ├── pytest-tmpl.md
│       ├── job-definition-tmpl.yaml
│       └── delta-merge-tmpl.md
└── codegen-outputs/
    ├── generated-code/
    ├── generated-tests/
    ├── job-definitions/
    └── optimization-reports/
```

---

> **Coda** — *"45 linhas de PySpark geradas com Delta Lake merge. Testes inclusos."*
