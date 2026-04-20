# 🔍 Discovery Scout Agent

> **AI-Agent Migration Factory™ — Legacy Environment Discovery & Inventory**

---

## Overview

The **Discovery Scout** is the **first agent executed** in the AI-Agent Migration Factory pipeline. It discovers, inventories, and classifies all legacy objects — pipelines, tables, jobs, scripts, and configurations — across the source environment. It maps dependencies between objects, detects dead code (orphan tables, unused scripts, deprecated jobs), and estimates data volumes for migration planning.

No migration begins without a complete, validated inventory from Scout.

---

## Agent Details

| Property       | Value                                              |
|----------------|----------------------------------------------------|
| **Persona**    | Scout                                              |
| **Icon**       | 🔍                                                 |
| **Phase**      | UPSTREAM                                           |
| **Gate**       | Gate 1                                             |
| **Autonomy**   | Level 3 — Monitored                                |
| **Engine**     | Python + SQL Parsers + AST Walkers                 |
| **Language**   | pt-BR                                              |
| **Version**    | 4.0                                                |
| **Framework**  | AI-Agent Migration Factory - Avanade-Enhanced Edition |

---

## Activation

```
@discovery-scout
```

---

## Commands

| Command               | Description                                      |
|-----------------------|--------------------------------------------------|
| `*help`               | Show available commands and usage                |
| `*scan-repo`          | Scan source platform for all objects             |
| `*classify`           | Classify pipelines by complexity                 |
| `*map-dependencies`   | Generate dependency graph                        |
| `*detect-dead-code`   | Find orphan and unused objects                   |
| `*estimate-volume`    | Estimate data volumes and transfer times         |
| `*generate-inventory` | Generate complete inventory report               |

---

## Deliverables

| Artifact                    | Format | Description                                       |
|-----------------------------|--------|---------------------------------------------------|
| `inventory.json`            | JSON   | Complete inventory of all legacy objects           |
| `dependency-graph.json`     | JSON   | DAG of dependencies between objects                |
| `dead-code-report.md`       | MD     | Orphan tables, unused scripts, deprecated jobs     |
| `data-volume-estimate.json` | JSON   | Table sizes, row counts, transfer time estimates   |
| `classification.json`       | JSON   | Pipeline complexity scoring and classification     |

---

## Integration

| Direction    | Agent                          | Artifacts Exchanged                              |
|--------------|--------------------------------|--------------------------------------------------|
| **Upstream** | Orion 🧭 (Migration Coordinator) | `migration-plan.md`, `source-connection-config.yaml` |
| **Downstream** | Logan 🧠 (Logic Extractor)    | `inventory.json`, `dependency-graph.json`         |
| **Downstream** | Orion 🧭 (Migration Coordinator) | `dead-code-report.md`, `data-volume-estimate.json` |

---

## File Structure

```
discovery-scout-agent/
├── README.md
├── .avanade-core/
│   ├── core-config.yaml
│   ├── agents/
│   │   └── discovery-scout.md
│   ├── tasks/
│   │   ├── scan-repo.md
│   │   ├── classify-pipelines.md
│   │   ├── map-dependencies.md
│   │   ├── detect-dead-code.md
│   │   ├── estimate-volume.md
│   │   └── generate-inventory.md
│   ├── checklists/
│   │   └── discovery-scout-checklist.md
│   ├── data/
│   │   └── discovery-best-practices.md
│   └── templates/
│       ├── inventory-tmpl.md
│       ├── dependency-graph-tmpl.md
│       └── dead-code-report-tmpl.md
└── discovery-outputs/
    ├── inventory/
    ├── dependency-graphs/
    ├── dead-code-reports/
    └── volume-estimates/
```

---

## Related Agents

| Agent                      | Icon | Phase      | Interaction                                 |
|----------------------------|------|------------|---------------------------------------------|
| Migration Coordinator      | 🧭   | ALL        | Receives plan, returns inventory & reports  |
| Logic Extractor            | 🧠   | UPSTREAM   | Receives inventory for logic extraction     |
| Data Modeler               | 📐   | UPSTREAM   | Uses inventory for target modeling          |
| Data Architect             | 🏗️   | UPSTREAM   | Uses dependency graph for architecture      |
| Data Steward               | 🛡️   | MIDSTREAM  | Uses inventory for governance mapping       |
| Inventory Scout            | 📦   | UPSTREAM   | Complementary scanning capabilities         |

---

## Quick Start

1. Activate the agent: `@discovery-scout`
2. Scan the source environment: `*scan-repo`
3. Classify pipeline complexity: `*classify`
4. Map dependencies: `*map-dependencies`
5. Detect dead code: `*detect-dead-code`
6. Estimate data volumes: `*estimate-volume`
7. Generate the complete inventory: `*generate-inventory`

---

> **AI-Agent Migration Factory™** · Avanade-Enhanced Edition v4.0
