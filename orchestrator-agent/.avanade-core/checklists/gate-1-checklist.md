# Gate 1 Checklist

**Gate:** UPSTREAM → MIDSTREAM  
**Agent:** Orchestrator  
**Version:** 1.0

---

## Pre-Validation Requirements

### Environment Check
- [ ] Workspace accessible
- [ ] Search tools functional
- [ ] Template files available
- [ ] Output folder exists

---

## Artifact Verification

### 1. Problem Statement
- [ ] File exists: `**/problem-statement*.md`
- [ ] Not empty (> 100 characters)
- [ ] Contains: Business Context section
- [ ] Contains: Problem Description section
- [ ] Contains: Impact/Scope section
- [ ] Contains: Stakeholders section

### 2. KPIs (Key Performance Indicators)
- [ ] File exists: `**/kpi*.md`
- [ ] Not empty (> 100 characters)
- [ ] At least 3 KPIs defined
- [ ] Each KPI has: Name
- [ ] Each KPI has: Baseline value
- [ ] Each KPI has: Target value
- [ ] Each KPI has: Calculation method

### 3. Analytical Questions
- [ ] File exists: `**/analytical-questions*.md`
- [ ] Not empty (> 100 characters)
- [ ] At least 5 questions defined
- [ ] Questions are specific/measurable
- [ ] Priority assigned to each
- [ ] Data source identified per question

### 4. STTM (Source-to-Target Mapping)
- [ ] File exists: `**/sttm*.md`
- [ ] Not empty (> 200 characters)
- [ ] Source systems documented
- [ ] Target tables defined
- [ ] Field mapping present
- [ ] Transformation rules included

### 5. DQ Initial (Data Quality Requirements)
- [ ] File exists: `**/dq-initial*.md`
- [ ] Not empty (> 100 characters)
- [ ] Quality dimensions defined
- [ ] Critical fields identified
- [ ] Acceptable thresholds set
- [ ] Validation approach documented

---

## Quality Validation

### Completeness Check
- [ ] All 5 artifacts found
- [ ] All artifacts have required sections
- [ ] No placeholder text remaining
- [ ] Cross-references consistent

### Consistency Check
- [ ] KPIs align with Problem Statement
- [ ] Questions support KPI measurement
- [ ] STTM covers Question data needs
- [ ] DQ covers critical KPI fields

---

## Decision Criteria

### PASS Conditions (ALL required)
- [ ] All 5 artifacts present
- [ ] All artifacts meet minimum quality
- [ ] No critical gaps identified
- [ ] Consistency checks pass

### PARTIAL Conditions (ANY applies)
- [ ] 4 of 5 artifacts present
- [ ] Minor quality issues only
- [ ] Non-critical gaps documented
- [ ] Path to completion clear

### FAIL Conditions (ANY applies)
- [ ] Fewer than 4 artifacts present
- [ ] Critical quality failures
- [ ] Major inconsistencies
- [ ] Blocker issues identified

---

## Post-Validation Actions

### On PASS
- [ ] Generate gate-1-report.md
- [ ] Update project status to MIDSTREAM
- [ ] Log in audit trail
- [ ] Recommend DataArchitect

### On PARTIAL
- [ ] Generate gate-1-report.md with conditions
- [ ] Document conditions for passage
- [ ] Recommend agent to resolve conditions
- [ ] Schedule re-validation

### On FAIL
- [ ] Generate gate-1-report.md with gaps
- [ ] Keep status as UPSTREAM
- [ ] Log failure in audit trail
- [ ] Recommend agent to fix gaps
