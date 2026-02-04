# Gate 2 Checklist

**Gate:** MIDSTREAM → DOWNSTREAM  
**Agent:** Orchestrator  
**Version:** 1.0

---

## Pre-Validation Requirements

### Gate 1 Status
- [ ] Gate 1 PASSED
- [ ] UPSTREAM artifacts available
- [ ] Project status is MIDSTREAM

### Environment Check
- [ ] Workspace accessible
- [ ] Search tools functional
- [ ] Template files available
- [ ] Output folder exists

---

## Artifact Verification

### 1. Architecture Document
- [ ] File exists: `**/architecture*.md`
- [ ] Not empty (> 300 characters)
- [ ] Contains: Layer definitions (Landing, Bronze, Silver, Gold)
- [ ] Contains: Technology stack
- [ ] Contains: Data flow diagram (or description)
- [ ] Contains: Security considerations
- [ ] Contains: Scalability approach
- [ ] Contains: Integration points

### 2. Data Model
- [ ] File exists: `**/data-model*.md` or `**/logical-model*.md`
- [ ] Not empty (> 200 characters)
- [ ] Entities documented
- [ ] Relationships defined
- [ ] Primary keys specified
- [ ] Foreign keys specified
- [ ] Data types documented
- [ ] Naming conventions followed

### 3. Tech Decisions (ADRs)
- [ ] File exists: `**/decisions*.md` or `**/adr*.md`
- [ ] Not empty (> 200 characters)
- [ ] At least 3 decisions documented
- [ ] Each has: Context/Problem
- [ ] Each has: Decision statement
- [ ] Each has: Consequences
- [ ] Each has: Alternatives considered

### 4. DQ Rules
- [ ] File exists: `**/dq-rules*.md`
- [ ] Not empty (> 200 characters)
- [ ] Rules linked to source fields
- [ ] SQL/Expression for each rule
- [ ] Severity levels defined
- [ ] Actions on failure specified
- [ ] Critical field coverage

### 5. Monitoring Spec (Recommended)
- [ ] File exists: `**/monitoring*.md`
- [ ] Key metrics identified
- [ ] Alert thresholds defined
- [ ] Notification channels specified
- [ ] Escalation procedures documented

---

## Cross-Reference Validation

### Architecture ↔ STTM
- [ ] All source systems in STTM are in architecture
- [ ] All target layers defined
- [ ] Data flow is consistent

### Data Model ↔ STTM
- [ ] All STTM targets exist in data model
- [ ] Field mappings align with model
- [ ] Relationships support queries

### DQ Rules ↔ KPIs
- [ ] KPI calculation fields have DQ rules
- [ ] Critical metrics have validation
- [ ] Thresholds are appropriate

### Architecture ↔ Analytical Questions
- [ ] Architecture supports question answering
- [ ] Data granularity is sufficient
- [ ] Aggregation levels available

---

## Decision Criteria

### PASS Conditions (ALL required)
- [ ] All 4 required artifacts present
- [ ] All artifacts meet minimum quality
- [ ] Cross-reference validations pass
- [ ] No critical gaps identified

### PARTIAL Conditions (ANY applies)
- [ ] 3 of 4 required artifacts present
- [ ] Minor cross-reference issues
- [ ] Non-critical gaps documented
- [ ] Clear remediation path

### FAIL Conditions (ANY applies)
- [ ] Fewer than 3 required artifacts
- [ ] Critical quality failures
- [ ] Major cross-reference failures
- [ ] Architecture fundamentally flawed

---

## Post-Validation Actions

### On PASS
- [ ] Generate gate-2-report.md
- [ ] Update project status to DOWNSTREAM
- [ ] Log in audit trail
- [ ] Recommend DataFlow for implementation

### On PARTIAL
- [ ] Generate gate-2-report.md with conditions
- [ ] Document conditions for passage
- [ ] Recommend agent to resolve:
  - DataArchitect for architecture/model issues
  - DataSteward for DQ/governance issues
- [ ] Schedule re-validation

### On FAIL
- [ ] Generate gate-2-report.md with gaps
- [ ] Keep status as MIDSTREAM
- [ ] Log failure in audit trail
- [ ] Recommend appropriate agent
