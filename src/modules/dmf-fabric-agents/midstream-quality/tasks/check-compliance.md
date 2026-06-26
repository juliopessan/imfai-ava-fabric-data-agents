# 🔒 Task: Check Compliance

## AI-Agent Migration Factory™ — Security & Compliance Agent

---

## Task ID
`check-compliance`

## Command
`*check-compliance`

## Purpose
Validate the migration pipeline against selected compliance frameworks (LGPD, GDPR, SOX, HIPAA). Checks data retention policies, consent management, audit trail enablement, encryption at rest and in transit, and access control configurations.

---

## Trigger
- Manual: `*check-compliance --frameworks=LGPD,GDPR --pipeline=<id>`
- Automatic: After `*apply-masking` completes successfully

---

## Inputs

| Input                         | Source                | Format | Required |
| ----------------------------- | --------------------- | ------ | -------- |
| `pii-findings.json`          | scan-pii task         | JSON   | Yes      |
| `masking-report.json`        | apply-masking task    | JSON   | Optional |
| `table-schemas.json`          | Discovery Scout 🔍    | JSON   | Yes      |
| `compliance-requirements.yaml`| Migration Coordinator 🎯 | YAML | Optional |
| `access-grants.json`          | Unity Catalog export  | JSON   | Optional |

---

## Parameters

| Parameter       | Default     | Description                                    |
| --------------- | ----------- | ---------------------------------------------- |
| `--frameworks`  | LGPD,GDPR   | Comma-separated frameworks to validate against |
| `--pipeline`    | —           | Pipeline ID for scoped validation              |
| `--scope`       | all         | `all`, `pii-only`, `access-only`, `encryption-only` |
| `--full-report` | false       | Generate detailed report with all checks       |

---

## Procedure

### Step 1: Initialize Compliance Check
```
1.1 Load selected frameworks and their rules
1.2 Load pipeline artifacts (PII findings, masking reports, schemas)
1.3 Initialize checklist with all applicable checks
1.4 Log: "Starting compliance validation for {pipeline_id} against {frameworks}"
```

### Step 2: LGPD Compliance Checks
```
LGPD-01: Legal Basis Documentation
  - Verify legal basis is documented for each data processing activity
  - Check: compliance-requirements.yaml contains legal_basis field
  - Reference: Art. 7

LGPD-02: Sensitive Data Protection
  - Verify sensitive data (CPF, health, biometric) has enhanced protection
  - Check: All BR_CPF fields are masked or tokenized
  - Reference: Art. 11

LGPD-03: Data Subject Rights
  - Verify capability to export/delete individual data subject records
  - Check: DELETE and EXPORT procedures exist for PII tables
  - Reference: Art. 9

LGPD-04: Data Retention Policy
  - Verify retention periods are defined and enforced
  - Check: Table properties include retention_days metadata
  - Reference: Art. 16

LGPD-05: Consent Management
  - Verify consent records exist for personal data processing
  - Check: Consent tracking table/column exists in schema
  - Reference: Art. 8
```

### Step 3: GDPR Compliance Checks
```
GDPR-01: Data Minimization
  - Verify only necessary data is collected and migrated
  - Check: No unused PII columns in target schema
  - Reference: Art. 5(1)(c)

GDPR-02: Purpose Limitation
  - Verify data processing purpose is documented
  - Check: Processing purpose metadata exists
  - Reference: Art. 5(1)(b)

GDPR-03: Storage Limitation
  - Verify data retention periods are defined
  - Check: TTL or retention policies on Delta tables
  - Reference: Art. 5(1)(e)

GDPR-04: Integrity & Confidentiality
  - Verify encryption at rest and in transit
  - Check: Workspace encryption enabled, TLS enforced
  - Reference: Art. 5(1)(f)

GDPR-05: Right to Erasure
  - Verify capability for data deletion (Delta DELETE support)
  - Check: DELETE operations tested on PII tables
  - Reference: Art. 17

GDPR-06: Data Protection by Design
  - Verify masking applied before data lands in target
  - Check: Masking functions applied at ingestion, not post-hoc
  - Reference: Art. 25
```

### Step 4: SOX Compliance Checks
```
SOX-01: Internal Controls
  - Verify access controls on financial data tables
  - Check: Row-level and column-level security on financial tables
  - Reference: Section 404

SOX-02: Audit Trail
  - Verify complete audit trail for all data modifications
  - Check: Change Data Capture (CDC) enabled, audit log present
  - Reference: Section 302

SOX-03: Data Integrity
  - Verify checksums and row counts match between source and target
  - Check: Reconciliation report available
  - Reference: Section 404

SOX-04: Segregation of Duties
  - Verify no single user has full read/write/admin access
  - Check: Role assignments show proper separation
  - Reference: Section 302

SOX-05: Retention Compliance
  - Verify financial records retained for 7+ years
  - Check: Retention policy >= 2555 days on financial tables
  - Reference: Section 802
```

### Step 5: HIPAA Compliance Checks (if enabled)
```
HIPAA-01: PHI Identification
  - Verify Protected Health Information is identified and classified
  - Check: PII scan includes health-related identifiers

HIPAA-02: Minimum Necessary Standard
  - Verify only minimum necessary PHI is accessed
  - Check: Column-level access controls on PHI fields

HIPAA-03: Encryption Requirements
  - Verify PHI encrypted at rest (AES-256) and in transit (TLS 1.2+)
  - Check: Workspace and storage encryption configuration

HIPAA-04: Access Logging
  - Verify all PHI access is logged
  - Check: Unity Catalog audit logs enabled for PHI tables
```

### Step 6: Cross-Framework Checks
```
CROSS-01: Encryption at Rest
  - Verify: Azure Storage Service Encryption enabled
  - Verify: Databricks workspace encryption enabled
  - Verify: Key management (Azure Key Vault) configured

CROSS-02: Encryption in Transit
  - Verify: TLS 1.2+ enforced on all connections
  - Verify: JDBC/ODBC connections use encrypted channels

CROSS-03: Access Control Validation
  - Verify: Unity Catalog enabled and configured
  - Verify: No public access to data tables
  - Verify: Service principals use least privilege

CROSS-04: Audit Trail Completeness
  - Verify: All compliance activities have audit entries
  - Verify: Audit log is immutable (append-only)
  - Verify: Retention meets strictest framework requirement
```

### Step 7: Generate Compliance Report
```
7.1 Aggregate all check results:
    - PASS: Check fully satisfied with evidence
    - FAIL: Check not satisfied, requires remediation
    - PARTIAL: Check partially satisfied, review needed
    - N/A: Check not applicable to current scope
7.2 Calculate compliance score: (PASS / total_applicable) * 100
7.3 Determine verdict:
    - Score >= 95% and no CRITICAL fails → COMPLIANT
    - Score >= 80% with only MEDIUM fails → REVIEW_REQUIRED
    - Score < 80% or any CRITICAL fail → NON-COMPLIANT
7.4 Write to compliance-reports/{pipeline_id}.json
7.5 Log audit entry: COMPLIANCE_CHECK_COMPLETED
```

---

## Output

### Primary: `compliance-reports/{pipeline_id}.json`

```json
{
  "compliance_id": "COMP-2025-001",
  "timestamp": "2025-01-15T12:00:00Z",
  "pipeline_id": "MM_MDG_001",
  "frameworks_evaluated": ["LGPD", "GDPR", "SOX"],
  "score": 97.5,
  "verdict": "COMPLIANT",
  "summary": {
    "total_checks": 20,
    "pass": 19,
    "fail": 0,
    "partial": 1,
    "not_applicable": 0
  },
  "checks": [
    {
      "id": "LGPD-01",
      "framework": "LGPD",
      "name": "Legal Basis Documentation",
      "reference": "Art. 7",
      "result": "PASS",
      "evidence": "Legal basis documented in compliance-requirements.yaml",
      "severity": "CRITICAL"
    }
  ],
  "remediation_required": [],
  "next_action": "Forward to Balance ⚖️ for reconciliation"
}
```

---

## Compliance Score Thresholds

| Score       | Verdict          | Action                                          |
| ----------- | ---------------- | ----------------------------------------------- |
| ≥ 95%       | COMPLIANT        | Forward to Balance ⚖️ for reconciliation        |
| 80% – 94%   | REVIEW_REQUIRED  | Flag for human review, list remediation items    |
| < 80%       | NON-COMPLIANT    | Block pipeline, notify Phoenix 🔧 for remediation |

---

## Acceptance Criteria

- [ ] All selected framework checks are executed
- [ ] Each check includes result, evidence, and regulatory reference
- [ ] Compliance score is calculated correctly
- [ ] Verdict follows the score threshold matrix
- [ ] Failed checks include specific remediation guidance
- [ ] Audit log entry generated for compliance check completion
- [ ] NON-COMPLIANT verdict blocks pipeline progression
