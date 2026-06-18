# Multi-Platform Migration Wave — Execution Guide

**Project Location:** `projects/multi-platform-migration/`  
**Wave Config:** `wave-config.yaml` (validated by `src/shared/scripts/validate_wave_config.py`)  
**Status:** 📁 REORGANIZED | 📂 Folders: scripts/, outputs/, state/, legacy/  
**Documentation:** See [`REPOSITORY-QUICK-REFERENCE.md`](../../REPOSITORY-QUICK-REFERENCE.md) for organization

---

## 📋 Overview

This migration wave **inventories 6 heterogeneous legacy platforms** and phases them toward **Microsoft Fabric** (primary target) with parallel track support for **Azure Data Factory, Synapse, Power BI**.

### Platforms Covered

| Platform | Priority | Status | Criticality | Target | Issues |
|----------|----------|--------|-------------|--------|--------|
| **Cloudera** | 1 | Pending | HIGH | Fabric | Partition loss, ACL granularity |
| **Airflow** | 4 | **BLOCKED** | HIGH | Data Factory | ⚠️ **Version unknown (1.x vs 2.x)** |
| **SSS** | 6 | **BLOCKED** | UNKNOWN | Unknown | ⚠️ **System not recognized** |
| **SAP BO** | 3 | Pending | VERY_HIGH | Power BI | Business Layer complexity |
| **PowerCenter** | 2 | Pending | HIGH | Data Factory | ⚠️ **.par files frequently lost** |
| **Snowflake** | 5 | Pending | HIGH | Fabric | Stream TTL (14d), Dynamic Tables undocumented |

---

## 🚨 CRITICAL BLOCKERS (Must Resolve Week 1)

### 1️⃣ Airflow: Version Unknown
- **Blocker:** `wave-config.yaml` lines 387–404
- **Action:** Run `airflow version` on production scheduler → confirm 1.x or 2.x
- **Impact:** 1.x → 2.x = 2-week DAG refactoring sprint (TaskFlow API rewrite)
- **Owner:** `discovery-scout` → escalate to `business-analyst`
- **Timeline:** **IMMEDIATE** (before Phase 1 starts)

### 2️⃣ SSS: System Identity Unknown
- **Blocker:** `wave-config.yaml` lines 516–540
- **Action:** Confirm what "SSS" is (proprietary legacy, vendor product, typo?)
- **Impact:** Cannot proceed with any migration planning until confirmed
- **Owner:** `discovery-scout` → stakeholder confirmation required
- **Timeline:** **IMMEDIATE**

### 3️⃣ PowerCenter: .par Files May Be Missing
- **Blocker:** `wave-config.yaml` lines 619–626
- **Action:** Audit repository for ALL .par (parameter) files
- **Impact:** Missing .par files = silent production failures
- **Owner:** `inventory-scout`
- **Timeline:** **Week 1 Phase 1** (discovery task #2)

---

## 🎯 Phase 1: Discovery & Inventory (4 weeks)

### Agents Assigned
- **Primary:** `discovery-scout`, `inventory-scout`
- **Support:** `data-architect`, `business-analyst`

### Outputs
```
projects/multi-platform-migration/outputs/phase-1-discovery/
├── DISCOVERY-REPORT.md                    (per platform)
├── ARTIFACT-INVENTORY.yaml                (comprehensive)
├── RISK-REGISTER.md                       (with mitigation)
├── BLOCKER-ASSESSMENT.md                  ⚠️ CRITICAL
├── DATA-CONTRACT-DRAFT.md
└── DEPENDENCY-MAP.md
```

### Platform-by-Platform Inventory Tasks

#### Cloudera (Est. 2 weeks)
```bash
# Step 1: Export all Hive schemas
hive -e "SHOW DATABASES" | tee databases.log

# Step 2: Export DDL per table
for db in $(cat databases.log); do
  hive -e "USE $db; SHOW TABLES" | while read table; do
    hive -e "SHOW CREATE TABLE $db.$table" > ddl/$db-$table.hql
  done
done

# Step 3: Ranger policy export (via Admin API)
curl -X GET \
  "http://ranger-admin:6080/service/public/v2/policies/download" \
  -H "Authorization: Basic <base64>" \
  > ranger-policies.json

# Step 4: Sample data + validate
hive -e "SELECT COUNT(*) as row_count FROM $table" >> data-volume.csv
```

#### Airflow (Est. 2-3 weeks + blockers)
```bash
# ⚠️ BLOCKER: Confirm version first
airflow version

# Once version confirmed:
airflow dags list --output json > dags-inventory.json
airflow connections export --file-format json > connections.json
airflow variables export --file-format json > variables.json

# Capture requirements + plugins
pip freeze > requirements-airflow.txt
find plugins/ -name "*.py" > custom-operators.log
```

#### SAP BusinessObjects (Est. 2 weeks)
```bash
# Step 1: LCM bundle export (non-negotiable)
# Via BOBJ Admin Console > LCM > Export
# Output: bobj-lcm-bundle.lcmbiar

# Step 2: Universe exports
# Via Information Design Tool > Export > .unv/.unx files

# Step 3: Security export
# Via BOBJ Admin > Roles/Groups > XML Export
```

#### PowerCenter (Est. 2 weeks)
```bash
# Step 1: Repository export
pmrep export -o xml -r PROD_REPO -f repository-export.xml

# Step 2: ⚠️ CRITICAL: Locate all .par files
find /opt/informatica -name "*.par" -type f > par-files-audit.log
# Cross-check against Workflows

# Step 3: Connection export
pmrep export -c relational -f connections.xml
```

#### Snowflake (Est. 2 weeks)
```sql
-- Step 1: Export complete DDL
SELECT GET_DDL('DATABASE', 'MY_DB');

-- Step 2: Streams inventory (critical for CDC)
SHOW STREAMS;
SELECT * FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()));

-- Step 3: Dynamic Tables (if present)
SHOW DYNAMIC TABLES;

-- Step 4: Roles + Grants
SHOW ROLES;
SHOW GRANTS ON DATABASE MY_DB;
```

### Gate 1 Acceptance Criteria

| Criterion | Weight | Target | Status |
|-----------|--------|--------|--------|
| Artifact Completude | 35% | ≥90% | 🔴 Pending |
| Blocker Resolution | 25% | 100% | 🔴 **Airflow/SSS/PowerCenter** |
| Risk Assessment | 20% | ≥90% | 🔴 Pending |
| Documentation | 20% | ≥85% | 🔴 Pending |

**Gate 1 Score Formula:** `0.35×completude + 0.25×blockers + 0.20×risk + 0.20×docs`  
**Pass Threshold:** ≥ 0.85

---

## 🏗️ Phase 2: Architecture & Design (6 weeks)

### Agents Assigned
- **Primary:** `data-architect`, `data-modeler`
- **Support:** `business-analyst`, `code-generator`

### Outputs
```
projects/multi-platform-migration/outputs/phase-2-architecture/
├── ARCHITECTURE-DESIGN.md
├── STTM-MAPPING.yaml              (Source-Target mapping)
├── DATA-MODEL-DESIGN.md
├── DDL-TEMPLATE.sql               (per platform)
├── ETL-LOGIC.md
├── DQ-RULES.yaml
└── DATA-CONTRACTS.yaml
```

### Key Deliverables

- **STTM (Source-Target Mapping):** Entity-by-entity mapping (source table → target table + transformations)
- **Data Contracts:** Schema, data types, nullable constraints, partition strategy
- **Data Quality Rules:** Null rates, domain validation, referential integrity checks
- **DDL Templates:** SQL for creating target schemas in Fabric

---

## 🚀 Phase 3: Execution & Validation (8 weeks)

### Agents Assigned
- **Primary:** `downstream-executor`, `reconciliation`
- **Support:** `quality-gate`, `code-generator`

### Outputs
```
projects/multi-platform-migration/outputs/phase-3-execution/
├── MIGRATION-LOG.md               (per-platform execution timeline)
├── RECONCILIATION-REPORT.md       (row counts, schema validation)
├── DATA-QUALITY-REPORT.md
├── PERFORMANCE-BASELINE.md
├── POST-MIGRATION-VALIDATION.md
└── LESSONS-LEARNED.md
```

### Execution Strategy

**Parallel Execution (with dependencies):**
1. **Wave A (Tier-1, critical path):** Cloudera DDLs → PowerCenter mappings → Airflow ETL
2. **Wave B (Supporting):** SAP BO → Power BI (parallel, no upstream dependencies)
3. **Wave C (Federated):** Snowflake → Fabric (with optional hybrid federation)

**Reconciliation Checklist:**
- [ ] Row count parity: Target ≥ 99.9% of Source
- [ ] Schema match: All columns, types, constraints present
- [ ] Data quality: Null rates, domain values validated
- [ ] Performance: Query latency within 1.5x baseline

---

## 🔧 How to Execute Using Existing Agents

### 1. Validate Wave Config
```bash
python src/shared/scripts/validate_wave_config.py \
  --config projects/multi-platform-migration/wave-config.yaml
```

Expected output:
```json
{
  "valid": false,
  "errors": [
    "blocker_resolution: Airflow version not confirmed",
    "blocker_resolution: SSS system identity unknown"
  ],
  "score": 0.75
}
```

### 2. Trigger Phase 1 Discovery (once blockers resolved)
```bash
# Use migration-coordinator to orchestrate
# (This is pseudo-code; adapt to your agent framework)

migration-coordinator --action start-phase \
  --wave-config projects/multi-platform-migration/wave-config.yaml \
  --phase 1 \
  --agent discovery-scout \
  --output-path projects/multi-platform-migration/outputs/phase-1-discovery
```

### 3. Generate Per-Platform Inventory Reports
```bash
# discovery-scout generates per-platform reports
discovery-scout --action inventory \
  --platform cloudera \
  --config projects/multi-platform-migration/wave-config.yaml \
  --output DISCOVERY-REPORT-CLOUDERA.md

# Repeat for: airflow, businessobjects, powercenter, snowflake
# SSS: skip until system identified
```

### 4. Risk & Assumption Validation
```bash
# quality-gate validates Gate 1 completeness
quality-gate --action validate \
  --gate gate-1 \
  --artifacts projects/multi-platform-migration/outputs/phase-1-discovery/ \
  --output GATE-1-VALIDATION-REPORT.md
```

---

## 📊 Progress Tracking

### Phase 1 Milestones
- [ ] **Week 1 (June 9–15):** Blocker resolution (Airflow version, SSS ID, .par files)
- [ ] **Week 2–3 (June 16–29):** Platform-by-platform inventory exports
- [ ] **Week 4 (June 30–July 7):** Gate 1 review + score calculation
- [ ] **Gate 1 Pass Decision:** July 8 (Target: ≥0.85 score)

### Phase 2 Milestones
- [ ] **Weeks 5–8:** Architecture design per platform
- [ ] **Weeks 9–10:** STTM mapping + data contracts finalized
- [ ] **Gate 2 Review:** August 18 (Target: ≥0.85 score)

### Phase 3 Milestones
- [ ] **Weeks 11–16:** Parallel execution (Wave A, B, C)
- [ ] **Weeks 17–18:** Reconciliation + validation + tuning
- [ ] **Gate 3 Review:** October 13 (Target: ≥0.90 score)

---

## 🔗 Related Files

- **Wave Config:** [wave-config.yaml](wave-config.yaml)
- **Agent Guide:** [/docs/COPILOT-AGENTS-GUIDE.md](../../docs/COPILOT-AGENTS-GUIDE.md)
- **Operating Model:** [/docs/OPERATING-MODEL-CANVAS-v2.md](../../docs/OPERATING-MODEL-CANVAS-v2.md)
- **Validation Scripts:** [/src/shared/scripts/validate_wave_config.py](../../src/shared/scripts/validate_wave_config.py)
- **Playbook:** [/docs/PLAYBOOK-MIGRATION-OPERATIONS.md](../../docs/PLAYBOOK-MIGRATION-OPERATIONS.md)

---

## 📞 Escalation Paths

| Blocker | Owner | Action |
|---------|-------|--------|
| Airflow version unknown | Stakeholder | Confirm version immediately |
| SSS system identity | Stakeholder | Identify system + provide docs |
| PowerCenter .par files | IT Ops | Audit + locate all .par files |
| Cloudera partition loss risk | data-architect | Design preservation strategy |
| SAP BO Business Layer | business-analyst | Plan Universe migration + remodeling |
| Snowflake Stream TTL | data-architect | Map CDC consumers + plan reconfiguration |

---

## ✅ Next Actions

1. **Resolve 3 critical blockers** (Week 1):
   - Airflow: `airflow version` confirmation
   - SSS: System identity + documentation
   - PowerCenter: .par file audit report

2. **Trigger Phase 1** (once blockers resolved):
   - Assign `discovery-scout` per platform
   - Run platform-specific inventory scripts
   - Generate ARTIFACT-INVENTORY.yaml

3. **Gate 1 Review** (July 8):
   - Validate completude + blocker resolution
   - Calculate GateScore (target ≥0.85)
   - Approve Phase 2 or request remediation

---

**Wave Created:** 2026-06-09  
**Last Updated:** 2026-06-09  
**Status:** 🟡 **Awaiting Blocker Resolution**
