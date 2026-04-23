# 📚 Task: Generate Migration Report

## Command
`*generate-report`

## Objective
Aggregate all artifacts produced by all agents in the AI-Agent Migration Factory and generate a comprehensive migration report. The report includes an executive summary (for sponsors and stakeholders) and a detailed technical report (for engineers and architects).

---

## Prerequisites

- All upstream agents have completed their execution
- Artifacts available:
  - `migration-coordinator → execution-log.json, wave-status-report.md`
  - `discovery-scout → inventory.json, dependency-graph.json`
  - `logic-extractor → digital-twin.json, pseudocode/*.json`
  - `code-generator → generated-code/*.py`
  - `quality-gate → validation-report/*.json`
  - `security-compliance → compliance-report/*.json, audit-trail.log`
  - `self-healing → healing-log/*.json`
  - `reconciliation → reconciliation-report.json`

---

## Steps

### 1. Artifact Collection
- Scan all agent output directories for artifacts
- Validate artifact integrity (JSON schema validation, file existence)
- Log missing or corrupted artifacts
- Create artifact manifest with checksums

### 2. Executive Summary Generation
- Extract key metrics: total tables migrated, success rate, duration, data volume
- Summarize per-wave results with status indicators (✅ ❌ ⚠️)
- Highlight critical findings and risks
- Generate recommendation section
- Target audience: C-level sponsors, project managers

### 3. Technical Report Generation
- Detailed per-pipeline analysis with transformation logic
- Data quality metrics per table (row counts, null rates, type mismatches)
- Performance metrics (throughput, latency, resource utilization)
- Error analysis with root cause categorization
- Code generation statistics
- Security and compliance summary

### 4. Visualization Embedding
- Generate summary charts (progress bars, pie charts via Mermaid)
- Embed data quality heatmaps
- Include architecture overview diagram
- Add wave timeline Gantt chart

### 5. Assembly and Formatting
- Merge sections using `migration-report-tmpl.md` template
- Generate table of contents
- Add metadata header (generation date, agent version, artifact sources)
- Format in Markdown with proper heading hierarchy
- Generate PT-BR version first, then EN-US

---

## Output

| File                                         | Description                      |
|----------------------------------------------|----------------------------------|
| `documentation-outputs/migration-reports/migration-report.md`       | Full migration report (50+ pages) |
| `documentation-outputs/migration-reports/migration-report-executive.md` | Executive summary extract     |
| `documentation-outputs/migration-reports/migration-report-technical.md` | Technical details extract     |

---

## Quality Criteria

- [ ] All upstream artifacts consumed and referenced
- [ ] Executive summary ≤ 5 pages
- [ ] Technical report includes per-table metrics
- [ ] All charts and diagrams render correctly
- [ ] Table of contents is accurate
- [ ] Both PT-BR and EN-US versions generated
- [ ] Metadata header present with generation timestamp
- [ ] No placeholder text remaining
