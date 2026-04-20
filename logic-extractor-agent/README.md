# 🧠 Logic Extractor Agent

> **AI-Agent Migration Factory™ — Business Logic Extraction & Semantic Analysis**

---

## Overview

O **Logic Extractor Agent (Logan)** extrai lógica de negócio de código legado e converte em pseudocódigo agnóstico de plataforma. É o **diferencial competitivo** da solução — onde outras abordagens migram código linha a linha, Logan **compreende a intenção** por trás do código e gera representações semânticas que preservam as regras de negócio.

Utiliza **LLM (GPT-4 + Claude 3.5)** combinado com **AST Parsers** para análise multi-linguagem, com scoring de confiança por pipeline.

---

## Agent Details

| Property       | Value                                              |
|----------------|----------------------------------------------------|
| **Persona**    | Logan                                              |
| **Icon**       | 🧠                                                 |
| **Phase**      | UPSTREAM                                           |
| **Gate**       | Gate 1                                             |
| **Autonomy**   | Level 2 (Supervised)                               |
| **Engine**     | LLM (GPT-4 + Claude 3.5) + AST Parsers            |
| **Language**   | pt-BR                                              |
| **Version**    | 4.0                                                |
| **Framework**  | AI-Agent Migration Factory - Avanade-Enhanced Edition |

---

## Activation

```
@logic-extractor
```

---

## Commands

| Command                | Description                                              |
|------------------------|----------------------------------------------------------|
| `*help`                | Show available commands and usage                        |
| `*extract-logic`       | Parse source code and extract business logic             |
| `*generate-pseudocode` | Convert extracted logic to platform-agnostic pseudocode  |
| `*create-digital-twin` | Create semantic blueprint (physical→semantic→target)     |
| `*parse-udf`           | Decompile and document User Defined Functions            |
| `*confidence-report`   | Generate confidence scores per pipeline                  |

---

## Deliverables

| Artifact                       | Format | Description                                          |
|--------------------------------|--------|------------------------------------------------------|
| `pseudocode/{pipeline_id}.json`| JSON   | Platform-agnostic pseudocode for each pipeline       |
| `digital-twin.json`            | JSON   | Semantic blueprint mapping physical→semantic→target  |
| `logic-extraction-report.md`   | MD     | Confidence scores and extraction quality per pipeline|

---

## Integration

| Direction      | Agent                             | Artifacts Exchanged                                   |
|----------------|-----------------------------------|------------------------------------------------------|
| **Upstream**   | Scout 🔍 (Discovery Scout)        | `inventory.json`, `dependency-graph.json`            |
| **Downstream** | Coda ⚙️ (Code Generator)          | `pseudocode/*.json`, `digital-twin.json`             |
| **Downstream** | Orion 🧭 (Migration Coordinator)  | `logic-extraction-report.md`                         |

---

## File Structure

```
logic-extractor-agent/
├── README.md
├── .avanade-core/
│   ├── core-config.yaml
│   ├── agents/
│   │   └── logic-extractor.md
│   ├── tasks/
│   │   ├── extract-logic.md
│   │   ├── generate-pseudocode.md
│   │   ├── create-digital-twin.md
│   │   ├── parse-udf.md
│   │   └── generate-confidence-report.md
│   ├── checklists/
│   │   └── logic-extractor-checklist.md
│   ├── data/
│   │   └── logic-extraction-best-practices.md
│   └── templates/
│       ├── pseudocode-tmpl.md
│       ├── digital-twin-tmpl.md
│       └── logic-report-tmpl.md
└── logic-outputs/
    ├── pseudocode/
    ├── digital-twin/
    ├── reports/
    └── udf-analysis/
```

---

## Related Agents

| Agent                      | Icon | Phase      | Interaction                                  |
|----------------------------|------|------------|----------------------------------------------|
| Discovery Scout            | 🔍   | UPSTREAM   | Provides inventory and dependency graph      |
| Migration Coordinator      | 🧭   | CORE       | Receives extraction reports, validates Gate 1|
| Code Generator             | ⚙️   | MIDSTREAM  | Consumes pseudocode to generate target code  |
| Data Modeler               | 📐   | UPSTREAM   | Uses digital twin for target modeling        |
| Quality Gate               | ✅   | MIDSTREAM  | Validates generated code against pseudocode  |

---

## Quick Start

1. Activate the agent: `@logic-extractor`
2. Extract business logic: `*extract-logic`
3. Generate pseudocode: `*generate-pseudocode`
4. Create digital twin: `*create-digital-twin`
5. Parse UDFs if applicable: `*parse-udf`
6. Generate confidence report: `*confidence-report`

---

> **AI-Agent Migration Factory™** · Avanade-Enhanced Edition v4.0
