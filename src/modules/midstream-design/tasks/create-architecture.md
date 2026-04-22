# Create Architecture Task

```yaml
task_id: create-architecture
agent: data-architect
version: "1.0"
command: "*create-architecture"
phase: MIDSTREAM
gate: 2
output: "tobe-target-architecture.html"
output_folder: "projects/{project_name}/outputs/midstream/"
```

---

## Purpose

Design and document a comprehensive data architecture that supports the business requirements defined in UPSTREAM phase.

---

## Prerequisites

- Gate 1 passed
- STTM available
- Analytical questions defined
- Understanding of technology constraints

---

## Execution Steps

### Step 1: Review Upstream Artifacts

Load and review:
- STTM (source systems, target tables, transformations)
- Analytical questions (data requirements)
- Problem statement (business context)
- KPIs (success metrics)

### Step 2: Define Architecture Pattern

Select appropriate pattern:
- **Lakehouse**: Unified analytics with Delta Lake
- **Data Warehouse**: Traditional DW/DM approach
- **Hybrid**: Combination based on needs

### Step 3: Design Data Layers

Define each layer:
1. **Landing/Raw**: Ingestion strategy
2. **Bronze**: Cleansing approach
3. **Silver**: Business logic layer
4. **Gold**: Aggregation/serving layer

### Step 4: Select Technology Stack

For each component, document:
1. Technology choice
2. Justification
3. Alternatives considered

### Step 5: Design Data Flow

Document:
1. Ingestion patterns (batch, streaming, hybrid)
2. Transformation pipeline
3. Serving patterns
4. Refresh schedules

### Step 6: Address Cross-Cutting Concerns

Document:
1. Security (access, encryption)
2. Scalability (growth strategy)
3. Monitoring (observability)
4. Disaster recovery

### Step 7: Generate Architecture Document

Produce a single self-contained HTML file (`tobe-target-architecture.html`)
using all decisions made in Steps 2–6. Do NOT produce Markdown.
Save to `projects/{project_name}/outputs/midstream/`.

The file must match this visual specification:

**Style:** Light theme (#F7F8FA bg). Fonts: Playfair Display (headings —
elegant serif), JetBrains Mono (labels/tags/metadata), Plus Jakarta Sans
(body) via Google Fonts. Primary accent: Microsoft Fabric blue #0078D4.
Layer colors: Bronze #C0782A, Silver #5B7FA6, Gold #A8860C, each with
*-light bg variant and *-mid border variant. All as CSS variables.
Header: white card, border-radius 16px, 3px gradient top border spanning
all layer colors.

**Required sections (in order):**

1. Header — white card with gradient top border, fabric blue badge
   'TO-BE Architecture', Playfair Display title, subtitle, right-aligned
   metadata (Trace ID, agents, target platform, pattern, gate status, date).
2. Architecture Principles — 4-column grid. Each card: large muted number
   (01-04), bold title, 2-line description.
3. Medallion Architecture — main visual. Horizontal flow:
   Sources → Bronze → Silver → Gold → Serving.
   Each layer: tall card with colored top border + tinted background,
   uppercase layer label, large serif name, description, JetBrains Mono
   detail lines (Format, Naming, Retention, Access), colored mini-badges.
   SVG chevron arrows (opacity 0.3) between layers.
   Below flow: 2-column cross-cutting cards (Governance + Observability).
4. Technology Stack — 3-column grid. Each card: colored dot + layer tag,
   bold tech name, description mentioning what it replaces from AS-IS.
5. SLA Table — columns: Layer, Metric, Target (TO-BE in green mono),
   Current AS-IS, Improvement (green with + prefix). Hover on rows.
6. Architecture Decisions (ADRs) — 3-column grid, 6 cards. Each card:
   ADR-00X in muted mono, bold title, decision in fabric blue, rationale.
7. Footer — left: brand. Right: 'TO-BE Architecture · Gate 2 · date'.

Section titles: JetBrains Mono, uppercase, letter-spacing 0.14em,
::after line to the right. No external JS. Single <style> block.
All content from decisions made in this task execution.

---

## Step 10 — Generate Markdown Output (architecture.md)

After saving the HTML file in Step 9, produce a second output:
a Markdown file (`architecture.md`) with the same architectural
content in structured text format.

Save to `projects/{project_name}/outputs/midstream/architecture.md`.

The Markdown file must contain:

```
# Data Architecture — {project_name}

**Pattern:** {architecture_pattern}
**Primary Technology:** {primary_technology}
**Target Environment:** {target_environment}
**Date:** {date}
**Version:** {version}

---

## Executive Summary

{executive_summary — 2-3 paragraphs}

---

## Architecture Principles

1. **{principle_1_title}**: {principle_1_desc}
2. **{principle_2_title}**: {principle_2_desc}
3. **{principle_3_title}**: {principle_3_desc}
4. **{principle_4_title}**: {principle_4_desc}

---

## Data Layers

### Sources
- Systems: {source_systems}
- Ingestion: {ingestion_method}

### Bronze Layer
- Format: {bronze_format}
- Retention: {bronze_retention}
- Naming: `brz_{domain}_{entity}`
- Transformations: {bronze_transformations}

### Silver Layer
- Format: {silver_format}
- Retention: {silver_retention}
- Naming: `slv_{domain}_{entity}`
- Transformations: {silver_transformations}

### Gold Layer
- Format: {gold_format}
- Retention: {gold_retention}
- Naming: `gld_{domain}_{subject}`
- Optimizations: {gold_optimizations}

### Serving
- BI Tool: {bi_tool}
- Access Pattern: {access_pattern}
- Consumers: {consumers}

---

## Technology Stack

| Layer | Technology | Replaces | Justification |
|-------|-----------|----------|---------------|
| Ingestion | {tech} | {replaces} | {justification} |
| Processing | {tech} | {replaces} | {justification} |
| Orchestration | {tech} | {replaces} | {justification} |
| Storage | {tech} | {replaces} | {justification} |
| Governance | {tech} | {replaces} | {justification} |
| Consumption | {tech} | {replaces} | {justification} |

---

## SLA Targets

| Layer | Metric | Target | Current (AS-IS) | Improvement |
|-------|--------|--------|-----------------|-------------|
| {layer} | {metric} | {target} | {current} | {delta} |

---

## Security Architecture

| Layer | Access Level | Method |
|-------|-------------|--------|
| Landing | ETL Service only | Service Principal |
| Bronze | ETL + Advanced Users | AAD Groups |
| Silver | Analytics Team | AAD Groups + RLS |
| Gold | All Authorized | AAD + RLS |

- Encryption at Rest: {encryption_rest}
- Encryption in Transit: {encryption_transit}
- Key Management: {key_management}

---

## Cross-Cutting Concerns

### Governance
{governance_description}

### Observability & SLO
{observability_description}

---

## Architecture Decisions (ADRs)

### ADR-001 — {title}
**Decision:** {decision_statement}
**Rationale:** {rationale}

### ADR-002 — {title}
**Decision:** {decision_statement}
**Rationale:** {rationale}

### ADR-003 — {title}
**Decision:** {decision_statement}
**Rationale:** {rationale}

### ADR-004 — {title}
**Decision:** {decision_statement}
**Rationale:** {rationale}

### ADR-005 — {title}
**Decision:** {decision_statement}
**Rationale:** {rationale}

### ADR-006 — {title}
**Decision:** {decision_statement}
**Rationale:** {rationale}

---

*Generated by DataArchitect Agent · Gate 2 · {date}*
```

> Both files must be saved before the task is considered complete.
> The HTML is the executive presentation; the Markdown is the
> machine-readable artifact consumed by downstream agents and CI.

---

## Validation Checklist

Before completing, verify:

- [ ] All data layers defined
- [ ] Technology stack documented with justifications
- [ ] Data flow clearly diagrammed
- [ ] Security approach documented
- [ ] Scalability strategy defined
- [ ] Monitoring approach specified
- [ ] Aligns with STTM requirements
- [ ] Supports all analytical questions
- [ ] `architecture.md` generated and saved to outputs/midstream/
- [ ] `architecture.md` contains all sections: layers, stack, SLAs, ADRs, security
