# Validate Gate 2 Task

**Task ID:** validate-gate-2  
**Agent:** Orchestrator  
**Version:** 1.0  
**Gate:** MIDSTREAM → DOWNSTREAM

---

## Purpose

Validate that all MIDSTREAM artifacts are complete and meet quality criteria before allowing transition to DOWNSTREAM phase (implementation).

---

## Gate 2 Criteria

### Required Artifacts

| # | Artifact | Description | Required |
|---|----------|-------------|----------|
| 1 | Architecture Document | Technical architecture decisions | ✅ Yes |
| 2 | Data Model | Logical/Physical data model | ✅ Yes |
| 3 | Tech Decisions | ADRs (Architecture Decision Records) | ✅ Yes |
| 4 | DQ Rules | Detailed data quality rules | ✅ Yes |
| 5 | Monitoring Spec | Monitoring and alerting specification | ⚠️ Recommended |

### Quality Criteria

Each artifact must meet these minimum standards:

**Architecture Document:**
- [ ] Layers clearly defined (Landing, Bronze, Silver, Gold)
- [ ] Technology stack documented
- [ ] Data flow diagrams included
- [ ] Security considerations addressed
- [ ] Scalability approach defined

**Data Model:**
- [ ] Entities and relationships documented
- [ ] Primary/Foreign keys defined
- [ ] Data types specified
- [ ] Naming conventions followed
- [ ] Normalization level justified

**Tech Decisions (ADRs):**
- [ ] At least 3 ADRs documented
- [ ] Context/Problem stated
- [ ] Decision clearly stated
- [ ] Consequences listed
- [ ] Alternatives considered

**DQ Rules:**
- [ ] Rules linked to source fields
- [ ] SQL/Expression provided for each rule
- [ ] Severity levels defined (Error/Warning/Info)
- [ ] Actions on failure specified
- [ ] Coverage of critical fields

**Monitoring Spec:**
- [ ] Key metrics identified
- [ ] Alert thresholds defined
- [ ] Notification channels specified
- [ ] Escalation procedures documented

---

## Execution Steps

### Step 1: Locate Artifacts

Search workspace for Gate 2 artifacts:

```
Search patterns:
- **/architecture*.md
- **/data-model*.md
- **/data_model*.md
- **/logical-model*.md
- **/decisions*.md
- **/adr*.md
- **/dq-rules*.md
- **/data-quality-rules*.md
- **/monitoring*.md
```

### Step 2: Validate Each Artifact

For each artifact found, check:
1. File exists and is not empty
2. Required sections are present
3. Content meets quality criteria
4. Consistency with UPSTREAM artifacts

### Step 3: Cross-Reference Validation

Verify consistency between artifacts:
- Data Model aligns with STTM
- DQ Rules cover KPI fields
- Architecture supports Analytical Questions

### Step 4: Generate Gate Report

Use template `gate-report-tmpl.yaml` to generate:

**Output file:** `{output_folder}/gate-reports/gate-2-report_{date}.md`

---

## Output Format

```markdown
# 🚦 Gate 2 Validation Report

**Gate:** MIDSTREAM → DOWNSTREAM  
**Date:** {date}  
**Validated by:** Orchestrator

---

## Overall Result

**Status:** {PASS | FAIL | PARTIAL}

---

## Artifact Checklist

| # | Artifact | Found | Location | Quality |
|---|----------|-------|----------|---------|
| 1 | Architecture | {✅/❌} | {path} | {✅/⚠️/❌} |
| 2 | Data Model | {✅/❌} | {path} | {✅/⚠️/❌} |
| 3 | Tech Decisions | {✅/❌} | {path} | {✅/⚠️/❌} |
| 4 | DQ Rules | {✅/❌} | {path} | {✅/⚠️/❌} |
| 5 | Monitoring Spec | {✅/❌} | {path} | {✅/⚠️/❌} |

---

## Cross-Reference Check

| Validation | Status | Notes |
|------------|--------|-------|
| Data Model ↔ STTM | {✅/⚠️/❌} | {notes} |
| DQ Rules ↔ KPIs | {✅/⚠️/❌} | {notes} |
| Architecture ↔ Questions | {✅/⚠️/❌} | {notes} |

---

## Detailed Findings

### Architecture Document
{detailed quality assessment}

### Data Model
{detailed quality assessment}

### Tech Decisions (ADRs)
{detailed quality assessment}

### DQ Rules
{detailed quality assessment}

### Monitoring Spec
{detailed quality assessment}

---

## Gaps Identified

{list of missing or incomplete items}

---

## Recommendations

{if PASS}
✅ Gate 2 PASSED. Project may proceed to DOWNSTREAM phase.
Recommended next agent: **DataFlow**

{if FAIL}
❌ Gate 2 FAILED. The following must be completed:
{list of required actions}
Recommended agent to resolve: **{agent}**

---

*Gate validation performed by Orchestrator Agent*
```

---

## Decision Rules

```
IF all 4 required artifacts found AND all quality checks pass:
  → RESULT: PASS
  → ACTION: Record gate passage, update project state

IF 3+ required artifacts AND critical quality checks pass:
  → RESULT: PARTIAL (with conditions)
  → ACTION: List conditions for full passage

IF <3 required artifacts OR critical quality checks fail:
  → RESULT: FAIL
  → ACTION: List gaps and assign to DataArchitect or DataSteward
```

---

## Post-Validation Actions

**On PASS:**
1. Create gate-2-report.md in gate-reports folder
2. Update project status to "DOWNSTREAM"
3. Log passage in audit trail
4. Suggest routing to DataFlow

**On FAIL:**
1. Create gate-2-report.md with gaps
2. Keep project status as "MIDSTREAM"
3. Log attempt in audit trail
4. Suggest routing to:
   - DataArchitect for architecture/model issues
   - DataSteward for DQ/governance issues
