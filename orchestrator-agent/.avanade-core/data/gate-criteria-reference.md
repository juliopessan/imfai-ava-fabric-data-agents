# Gate Criteria Reference

**Document:** Gate Criteria and Validation Rules  
**Agent:** Orchestrator  
**Version:** 1.0

---

## Gate Overview

The Avanade Core methodology uses a three-gate system to ensure quality and completeness at each phase transition.

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  UPSTREAM   │────▶│  MIDSTREAM  │────▶│ DOWNSTREAM  │────▶│ PRODUCTION  │
│  Discovery  │     │   Design    │     │Implementation│     │   Deploy    │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
        │                  │                  │
        ▼                  ▼                  ▼
    ┌───────┐          ┌───────┐          ┌───────┐
    │Gate 1 │          │Gate 2 │          │Gate 3 │
    └───────┘          └───────┘          └───────┘
```

---

## Gate 1: UPSTREAM → MIDSTREAM

### Purpose
Validate that the business problem is well understood and requirements are complete before starting technical design.

### Required Artifacts

| # | Artifact | Description | Owner Agent |
|---|----------|-------------|-------------|
| 1 | Problem Statement | Clear definition of business problem | DataStrategist |
| 2 | KPIs | Key Performance Indicators | DataStrategist |
| 3 | Analytical Questions | Business questions to answer | BusinessAnalyst |
| 4 | STTM | Source-to-Target Mapping | BusinessAnalyst |
| 5 | DQ Initial | Initial Data Quality requirements | BusinessAnalyst |

### Quality Criteria

#### Problem Statement
| Criterion | Weight | Validation |
|-----------|--------|------------|
| Business context present | Required | Section exists with content |
| Problem impact quantified | Required | Numbers/metrics included |
| Scope boundaries defined | Required | In-scope/out-of-scope listed |
| Stakeholders identified | Required | Names or roles listed |

#### KPIs
| Criterion | Weight | Validation |
|-----------|--------|------------|
| At least 3 KPIs | Required | Count >= 3 |
| Baseline values | Required | Each KPI has current value |
| Target values | Required | Each KPI has goal value |
| Calculation method | Required | Formula or logic documented |

#### Analytical Questions
| Criterion | Weight | Validation |
|-----------|--------|------------|
| At least 5 questions | Required | Count >= 5 |
| Specific and measurable | Required | No vague questions |
| Priority assigned | Recommended | High/Medium/Low per question |
| Data source identified | Recommended | Source linked to each question |

#### STTM
| Criterion | Weight | Validation |
|-----------|--------|------------|
| Source systems listed | Required | At least 1 source |
| Target tables defined | Required | Table names specified |
| Field mapping present | Required | Source → Target columns |
| Transformations documented | Required | Rules/logic specified |

#### DQ Initial
| Criterion | Weight | Validation |
|-----------|--------|------------|
| Quality dimensions | Required | At least 3 dimensions |
| Critical fields identified | Required | Fields marked as critical |
| Acceptable thresholds | Required | Percentage or count thresholds |

### Pass Criteria
- **PASS:** All 5 artifacts present with all Required criteria met
- **PARTIAL:** 4+ artifacts with most Required criteria met
- **FAIL:** <4 artifacts or critical criteria missing

---

## Gate 2: MIDSTREAM → DOWNSTREAM

### Purpose
Validate that technical design is complete and feasible before starting implementation.

### Required Artifacts

| # | Artifact | Description | Owner Agent |
|---|----------|-------------|-------------|
| 1 | Architecture Document | Technical architecture | DataArchitect |
| 2 | Data Model | Logical/Physical model | DataArchitect |
| 3 | Tech Decisions (ADRs) | Architecture decisions | DataArchitect |
| 4 | DQ Rules | Detailed quality rules | DataSteward |
| 5 | Monitoring Spec | Monitoring/alerting (Recommended) | DataSteward |

### Quality Criteria

#### Architecture Document
| Criterion | Weight | Validation |
|-----------|--------|------------|
| Layers defined | Required | Landing, Bronze, Silver, Gold |
| Technology stack | Required | Tools/platforms listed |
| Data flow diagram | Required | Visual or text description |
| Security considerations | Required | Section exists |
| Scalability approach | Recommended | Growth strategy documented |

#### Data Model
| Criterion | Weight | Validation |
|-----------|--------|------------|
| Entities documented | Required | All tables/entities listed |
| Relationships defined | Required | FK relationships shown |
| Data types specified | Required | Per column |
| Naming conventions | Required | Consistent naming |

#### Tech Decisions (ADRs)
| Criterion | Weight | Validation |
|-----------|--------|------------|
| At least 3 ADRs | Required | Count >= 3 |
| Context stated | Required | Problem/context section |
| Decision clear | Required | Decision statement |
| Consequences listed | Required | Pros/cons documented |
| Alternatives considered | Recommended | Other options mentioned |

#### DQ Rules
| Criterion | Weight | Validation |
|-----------|--------|------------|
| Rules linked to fields | Required | Source field reference |
| SQL/Expression provided | Required | Executable rule logic |
| Severity levels | Required | Error/Warning/Info |
| Actions on failure | Required | What happens on fail |

#### Monitoring Spec
| Criterion | Weight | Validation |
|-----------|--------|------------|
| Key metrics | Required | Metrics to track |
| Alert thresholds | Required | When to alert |
| Notification channels | Recommended | How to notify |

### Cross-Reference Validations

| Check | Description | Severity |
|-------|-------------|----------|
| Model ↔ STTM | All STTM targets in model | Critical |
| DQ ↔ KPIs | KPI fields have DQ rules | Major |
| Architecture ↔ Questions | Design supports all questions | Major |

### Pass Criteria
- **PASS:** All 4 required artifacts present, quality criteria met, cross-references valid
- **PARTIAL:** 3+ required artifacts, minor issues only
- **FAIL:** <3 required artifacts or critical issues

---

## Gate 3: DOWNSTREAM → PRODUCTION

### Purpose
Validate that implementation is complete, tested, and ready for production deployment.

### Required Artifacts

| # | Artifact | Description | Owner Agent |
|---|----------|-------------|-------------|
| 1 | DDL Scripts | Database definitions | DataFlow |
| 2 | ETL Code | Data transformation code | DataFlow |
| 3 | Unit Tests | Automated tests | DataFlow |
| 4 | Integration Tests | End-to-end tests | DataFlow |
| 5 | Documentation | Pipeline documentation | DataFlow |
| 6 | DQ Validation | Quality validation results | DataFlow |
| 7 | Performance Tests | Load tests (Recommended) | DataFlow |

### Quality Criteria

#### DDL Scripts
| Criterion | Weight | Validation |
|-----------|--------|------------|
| All layers covered | Required | Landing through Gold |
| No syntax errors | Required | Valid SQL |
| Constraints defined | Required | PK, FK, NOT NULL |
| Idempotent scripts | Recommended | Can re-run safely |

#### ETL Code
| Criterion | Weight | Validation |
|-----------|--------|------------|
| All mappings implemented | Required | STTM coverage 100% |
| Error handling | Required | TRY/CATCH or equivalent |
| Logging present | Required | Audit/log statements |
| Incremental logic | If applicable | Delta load support |

#### Tests
| Criterion | Weight | Validation |
|-----------|--------|------------|
| Unit test coverage | Required | >= 80% |
| All tests passing | Required | 0 failures |
| Edge cases covered | Recommended | Boundary tests |
| Integration tests exist | Required | E2E validation |

#### Documentation
| Criterion | Weight | Validation |
|-----------|--------|------------|
| Pipeline overview | Required | Architecture documented |
| Data lineage | Required | Source to target flow |
| Troubleshooting guide | Required | Common issues |
| Runbook | Required | Operations guide |

#### DQ Validation
| Criterion | Weight | Validation |
|-----------|--------|------------|
| All rules executed | Required | Rule execution report |
| Pass rate >= 95% | Required | Quality threshold met |
| No critical failures | Required | Critical rules pass |

### Pass Criteria
- **PASS:** All 6 required categories present, tests passing >= 95%, DQ >= 95%
- **PARTIAL:** 5+ categories, tests >= 80%, DQ >= 90%
- **FAIL:** <5 categories, tests < 80%, DQ < 90%, or critical failures

---

## Decision Matrix

### Gate Result Determination

```
                    Artifacts     Quality      Cross-Ref
PASS                All present   All met      All valid
PARTIAL             Most present  Most met     Minor issues
FAIL                Missing       Not met      Major issues
```

### Remediation Agent Mapping

| Gap Type | Recommended Agent |
|----------|-------------------|
| Problem/KPI missing | DataStrategist |
| STTM/Questions missing | BusinessAnalyst |
| Architecture issues | DataArchitect |
| DQ rules issues | DataSteward |
| DDL/ETL issues | DataFlow |
| Reporting issues | InsightForge |

---

## Validation Workflow

```
1. Orchestrator receives *gate-{n} command
2. Load gate checklist
3. Scan workspace for artifacts
4. Validate each artifact against criteria
5. Perform cross-reference checks (Gate 2+)
6. Calculate pass/partial/fail
7. Generate gate report
8. Update audit trail
9. Recommend next steps
```

---

*Gate criteria reference maintained by Orchestrator Agent*
