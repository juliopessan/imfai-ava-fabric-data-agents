# Validate Gate 1 Task

**Task ID:** validate-gate-1  
**Agent:** Orchestrator  
**Version:** 1.0  
**Gate:** UPSTREAM → MIDSTREAM

---

## Purpose

Validate that all UPSTREAM artifacts are complete and meet quality criteria before allowing transition to MIDSTREAM phase.

---

## Gate 1 Criteria

### Required Artifacts

| # | Artifact | Description | Required |
|---|----------|-------------|----------|
| 1 | Problem Statement | Clear definition of business problem | ✅ Yes |
| 2 | KPIs | Key Performance Indicators with baseline/target | ✅ Yes |
| 3 | Analytical Questions | Business questions to be answered | ✅ Yes |
| 4 | STTM | Source-to-Target Mapping document | ✅ Yes |
| 5 | DQ Initial | Initial Data Quality requirements | ✅ Yes |

### Quality Criteria

Each artifact must meet these minimum standards:

**Problem Statement:**
- [ ] Business context clearly explained
- [ ] Problem impact quantified
- [ ] Scope boundaries defined
- [ ] Stakeholders identified

**KPIs:**
- [ ] At least 3 KPIs defined
- [ ] Each KPI has baseline value
- [ ] Each KPI has target value
- [ ] Calculation method documented

**Analytical Questions:**
- [ ] At least 5 analytical questions
- [ ] Questions are specific and measurable
- [ ] Priority assigned to each question
- [ ] Data sources identified per question

**STTM:**
- [ ] Source systems documented
- [ ] Target tables defined
- [ ] Field mapping complete
- [ ] Transformation rules specified

**DQ Initial:**
- [ ] Data quality dimensions defined
- [ ] Critical fields identified
- [ ] Acceptable thresholds set
- [ ] Validation rules documented

---

## Execution Steps

### Step 1: Locate Artifacts

Search workspace for Gate 1 artifacts:

```
Search patterns:
- **/problem-statement*.md
- **/problem_statement*.md
- **/kpi*.md
- **/analytical-questions*.md
- **/analytical_questions*.md
- **/sttm*.md
- **/source-to-target*.md
- **/dq-initial*.md
- **/data-quality*.md
```

### Step 2: Validate Each Artifact

For each artifact found, check:
1. File exists and is not empty
2. Required sections are present
3. Content meets quality criteria

### Step 3: Generate Gate Report

Use template `gate-report-tmpl.yaml` to generate:

**Output file:** `{output_folder}/gate-reports/gate-1-report_{date}.md`

---

## Output Format

```markdown
# 🚦 Gate 1 Validation Report

**Gate:** UPSTREAM → MIDSTREAM  
**Date:** {date}  
**Validated by:** Orchestrator

---

## Overall Result

**Status:** {PASS | FAIL | PARTIAL}

---

## Artifact Checklist

| # | Artifact | Found | Location | Quality |
|---|----------|-------|----------|---------|
| 1 | Problem Statement | {✅/❌} | {path} | {✅/⚠️/❌} |
| 2 | KPIs | {✅/❌} | {path} | {✅/⚠️/❌} |
| 3 | Analytical Questions | {✅/❌} | {path} | {✅/⚠️/❌} |
| 4 | STTM | {✅/❌} | {path} | {✅/⚠️/❌} |
| 5 | DQ Initial | {✅/❌} | {path} | {✅/⚠️/❌} |

---

## Detailed Findings

### Problem Statement
{detailed quality assessment}

### KPIs
{detailed quality assessment}

### Analytical Questions
{detailed quality assessment}

### STTM
{detailed quality assessment}

### DQ Initial
{detailed quality assessment}

---

## Gaps Identified

{list of missing or incomplete items}

---

## Recommendations

{if PASS}
✅ Gate 1 PASSED. Project may proceed to MIDSTREAM phase.
Recommended next agent: **DataArchitect**

{if FAIL}
❌ Gate 1 FAILED. The following must be completed:
{list of required actions}
Recommended agent to resolve: **{agent}**

---

*Gate validation performed by Orchestrator Agent*
```

---

## Decision Rules

```
IF all 5 artifacts found AND all quality checks pass:
  → RESULT: PASS
  → ACTION: Record gate passage, update project state

IF 4+ artifacts found AND critical quality checks pass:
  → RESULT: PARTIAL (with conditions)
  → ACTION: List conditions that must be met

IF <4 artifacts found OR critical quality checks fail:
  → RESULT: FAIL
  → ACTION: List gaps and assign to appropriate agent
```

---

## Post-Validation Actions

**On PASS:**
1. Create gate-1-report.md in gate-reports folder
2. Update project status to "MIDSTREAM"
3. Log passage in audit trail
4. Suggest routing to DataArchitect

**On FAIL:**
1. Create gate-1-report.md with gaps
2. Keep project status as "UPSTREAM"
3. Log attempt in audit trail
4. Suggest routing to appropriate agent to fix gaps
