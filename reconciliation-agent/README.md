# ⚖️ Reconciliation Agent

> **AI-Agent Migration Factory™ — Data Reconciliation & Parity Validation**

---

## Overview

The **Reconciliation Agent** validates data parity between source and target systems after migration. It compares row counts, checksums (SHA-256), schemas, and runs data profiling using Great Expectations. The agent ensures **99.9% data fidelity** and reports all discrepancies with severity classification (Critical / Warning / Info).

> *"450/450 tabelas reconciliadas. 99.97% paridade. 1 tabela com delta de 3 rows."*

---

## Agent Details

| Property       | Value                                              |
| -------------- | -------------------------------------------------- |
| **Persona**    | Balance                                            |
| **Icon**       | ⚖️                                                |
| **Phase**      | DOWNSTREAM                                         |
| **Gate**       | 3                                                  |
| **Autonomy**   | Level 3 — Monitored                                |
| **Engine**     | PySpark + Data Profiling (Great Expectations)       |
| **Activation** | `@reconciliation`                                  |

---

## Commands

| Command             | Description                                                         |
| ------------------- | ------------------------------------------------------------------- |
| `*help`             | Show available commands and usage                                   |
| `*row-count`        | Compare row counts between source and target for all tables         |
| `*checksum`         | Compute and compare SHA-256 checksums on source and target data     |
| `*schema-diff`      | Compare source and target schemas (columns, types, constraints)     |
| `*profile-data`     | Run Great Expectations data profiling and compare statistical profiles |
| `*reconcile-wave`   | Full reconciliation for a wave — all checks, aggregated report      |
| `*yolo`             | Auto-execute row count and schema comparison (yolo-eligible scope)  |

---

## Deliverables

| Artifact                    | Format | Description                                        |
| --------------------------- | ------ | -------------------------------------------------- |
| `reconciliation-report.json`| JSON   | Aggregate reconciliation results per wave           |
| `discrepancy-details.json`  | JSON   | Detailed discrepancy records with severity & action |

---

## Agent Dependencies

### Upstream (inputs received from)

| Agent                  | Artifact                                                        |
| ---------------------- | --------------------------------------------------------------- |
| Vera ✅ (Quality Gate) | Approved code / validated migration artifacts                   |
| Shield 🔒 (Security)  | Compliant code / security-cleared pipelines                     |
| Orion 🧭 (Coordinator)| `source-connection-config.yaml`, `target-connection-config.yaml`|

### Downstream (outputs sent to)

| Agent               | Artifact                      |
| -------------------- | ----------------------------- |
| Scribe 📚 (Docs)    | `reconciliation-report.json`  |

---

## Quick Start

```text
@reconciliation *help
@reconciliation *row-count --wave 1
@reconciliation *checksum --table MARA --partition-column MANDT
@reconciliation *schema-diff --wave 1
@reconciliation *profile-data --table MARA
@reconciliation *reconcile-wave --wave 1
@reconciliation *yolo --wave 1
```

---

## Directory Structure

```
reconciliation-agent/
├── README.md
├── .avanade-core/
│   ├── core-config.yaml
│   ├── agents/
│   │   └── reconciliation.md
│   ├── tasks/
│   │   ├── compare-row-counts.md
│   │   ├── validate-checksums.md
│   │   ├── diff-schemas.md
│   │   ├── profile-data.md
│   │   └── reconcile-wave.md
│   ├── checklists/
│   │   └── reconciliation-checklist.md
│   ├── data/
│   │   └── reconciliation-best-practices.md
│   └── templates/
│       ├── reconciliation-report-tmpl.md
│       └── discrepancy-report-tmpl.md
└── reconciliation-outputs/
    ├── reconciliation-reports/
    ├── discrepancy-details/
    ├── data-profiles/
    └── schema-diffs/
```

---

## License

Proprietary — Avanade AI-Agent Migration Factory™
