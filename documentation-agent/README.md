# 📚 Documentation Agent

## AI-Agent Migration Factory™ — Automatic Documentation Generation

---

## Overview

Terminal agent in the pipeline. Automatically generates all migration documentation from artifacts produced by other agents. Creates executive reports, technical docs, data lineage diagrams (Mermaid), operational runbooks, and changelogs. Zero human intervention needed — **Level 4 Autonomous**. Generates in **PT-BR** and **EN**.

---

## Agent Details

| Property       | Value                                              |
|----------------|-----------------------------------------------------|
| **Persona**    | Scribe                                              |
| **Icon**       | 📚                                                  |
| **Phase**      | DOWNSTREAM                                          |
| **Gate**       | 3                                                   |
| **Autonomy**   | Level 4 (Autonomous)                                |
| **Engine**     | LLM (GPT-4) + Template Engine (Jinja2) + Mermaid.js |
| **Activation** | `@documentation`                                    |

---

## Commands

| Command              | Description                                                |
|----------------------|------------------------------------------------------------|
| `*help`              | Display available commands and usage instructions          |
| `*generate-report`   | Generate the full migration report (executive + technical) |
| `*generate-lineage`  | Generate Mermaid data lineage diagrams for all tables      |
| `*generate-runbook`  | Generate operational runbooks for the migrated environment |
| `*generate-changelog`| Generate changelog from Git log and agent execution history|
| `*generate-all`      | Execute all generation tasks in sequence                   |
| `*yolo`              | Full autonomous run — generate all documentation, no stops |

---

## Deliverables

| Artifact                   | Format   | Description                                      |
|----------------------------|----------|--------------------------------------------------|
| `migration-report.md`      | Markdown | Comprehensive migration report (50+ pages)       |
| `technical-docs/`          | Markdown | Detailed technical documentation per component   |
| `runbooks/`                | Markdown | Operational runbooks for the migrated environment |
| `data-lineage-diagrams/`   | Mermaid  | Data lineage diagrams for all migrated tables     |
| `changelog.md`             | Markdown | Chronological changelog with semantic versioning  |

---

## Dependencies

### Upstream (Input Sources)

This agent aggregates artifacts from **all** other agents in the factory:

| Agent                    | Artifacts Consumed                                        |
|--------------------------|-----------------------------------------------------------|
| Migration Coordinator    | `execution-log.json`, `wave-status-report.md`             |
| Discovery Scout          | `inventory.json`, `dependency-graph.json`                 |
| Logic Extractor          | `digital-twin.json`, `pseudocode/*.json`                  |
| Code Generator           | `generated-code/*.py`                                     |
| Quality Gate             | `validation-report/*.json`                                |
| Security & Compliance    | `compliance-report/*.json`, `audit-trail.log`             |
| Self-Healing             | `healing-log/*.json`                                      |
| Reconciliation           | `reconciliation-report.json`                              |

### Downstream

**None** — This is the **terminal agent** in the pipeline. Publishes final documentation to:

- Confluence (API)
- SharePoint (API)
- Git (commit)
- PDF (export)

---

## Folder Structure

```
documentation-agent/
├── README.md
├── .avanade-core/
│   ├── core-config.yaml
│   ├── agents/
│   │   └── documentation.md
│   ├── tasks/
│   │   ├── generate-migration-report.md
│   │   ├── generate-lineage-diagrams.md
│   │   ├── generate-runbook.md
│   │   ├── generate-changelog.md
│   │   └── generate-all.md
│   ├── checklists/
│   │   └── documentation-checklist.md
│   ├── data/
│   │   └── documentation-best-practices.md
│   └── templates/
│       ├── migration-report-tmpl.md
│       ├── lineage-diagram-tmpl.md
│       ├── runbook-tmpl.md
│       └── changelog-tmpl.md
└── documentation-outputs/
    ├── migration-reports/
    ├── technical-docs/
    ├── runbooks/
    ├── lineage-diagrams/
    └── changelogs/
```

---

## Quick Start

```bash
# Activate the Documentation Agent
@documentation

# Generate all documentation at once
*generate-all

# Or run in full YOLO mode
*yolo
```

---

## Output Languages

| Language | Priority  | Usage                              |
|----------|-----------|------------------------------------|
| PT-BR    | Primary   | All documentation generated first  |
| EN-US    | Secondary | Translations generated after PT-BR |

---

## Publishing Targets

| Target      | Method  | Description                              |
|-------------|---------|------------------------------------------|
| Confluence  | API     | Publish pages to Confluence space        |
| SharePoint  | API     | Upload documents to SharePoint library   |
| Git         | Commit  | Commit documentation to repository       |
| PDF         | Export  | Export final documents as PDF            |

---

> *"Documentação gerada: 50 páginas, 12 diagramas, 8 runbooks. Zero intervenção humana."*
> — **Scribe**, Documentation Agent 📚
