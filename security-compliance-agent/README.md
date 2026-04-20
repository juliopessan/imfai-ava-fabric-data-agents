# 🔒 Security & Compliance Agent

## AI-Agent Migration Factory™ — Security, Privacy & Regulatory Compliance

---

## Overview

The **Security & Compliance Agent** ensures that all generated code and migrated data comply with security policies and regulatory requirements (LGPD, GDPR, SOX, HIPAA). It detects Personally Identifiable Information (PII), applies data masking strategies, validates access controls, and maintains comprehensive audit trails.

**Zero tolerance for exposed PII.**

Every pipeline artifact, table schema, and data sample passes through Shield's compliance gate before advancing in the migration workflow.

---

## Agent Details

| Property       | Value                                                  |
| -------------- | ------------------------------------------------------ |
| **Persona**    | Shield                                                 |
| **Icon**       | 🔒                                                     |
| **Phase**      | MIDSTREAM                                              |
| **Gate**       | 2                                                      |
| **Autonomy**   | Level 2 — Supervised                                   |
| **Engine**     | Policy Engine + PII Scanner (Presidio) + Audit Logger  |
| **Activation** | `@security-compliance`                                 |

---

## Commands

| Command              | Description                                                       |
| -------------------- | ----------------------------------------------------------------- |
| `*help`              | Display available commands and agent capabilities                 |
| `*scan-pii`          | Detect PII in table schemas and data samples using Presidio       |
| `*apply-masking`     | Apply masking strategy (SHA-256, partial mask, tokenization) to PII fields |
| `*check-compliance`  | Validate against selected compliance frameworks (LGPD/GDPR/SOX/HIPAA) |
| `*audit-log`         | Generate structured audit log entries for compliance activities   |
| `*validate-access`   | Validate Unity Catalog permissions and least privilege enforcement |

---

## Deliverables

| Artifact                                  | Format | Description                                  |
| ----------------------------------------- | ------ | -------------------------------------------- |
| `compliance-reports/{pipeline_id}.json`   | JSON   | Full compliance validation report per pipeline |
| `pii-findings.json`                       | JSON   | Detected PII fields with confidence scores    |
| `audit-trail.log`                         | LOG    | Structured audit log for all compliance events |
| `masking-reports/{pipeline_id}.json`      | JSON   | Masking actions applied to PII fields          |

---

## Integration Map

### Upstream (inputs)

| Agent           | Icon | Artifact                      | Purpose                        |
| --------------- | ---- | ----------------------------- | ------------------------------ |
| Coda            | ⚙️   | `generated-code/*.py`         | Code to scan for PII exposure  |
| Scout           | 🔍   | `table-schemas.json`          | Table schemas for PII detection |
| Coordinator     | 🎯   | `compliance-requirements.yaml`| Compliance framework selection  |

### Downstream (outputs)

| Agent           | Icon | Artifact                      | Condition                      |
| --------------- | ---- | ----------------------------- | ------------------------------ |
| Phoenix         | 🔧   | `pii-findings.json`          | If **non-compliant** — triggers remediation |
| Balance         | ⚖️   | `compliance-report.json`     | If **compliant** — advances to reconciliation |

---

## Workflow Position

```
┌─────────────┐     ┌─────────────────┐     ┌──────────────────┐
│  Coda ⚙️     │────▶│  Shield 🔒       │────▶│  Phoenix 🔧      │
│  (code)      │     │  (compliance)    │     │  (if non-compliant)
└─────────────┘     └────────┬────────┘     └──────────────────┘
                             │
┌─────────────┐              │              ┌──────────────────┐
│  Scout 🔍    │──────────────┘              │  Balance ⚖️      │
│  (schemas)   │              ──────────────▶│  (if compliant)  │
└─────────────┘                             └──────────────────┘
```

---

## Quick Start

```bash
# 1. Activate the agent
@security-compliance

# 2. Scan for PII in schemas
*scan-pii --source=table-schemas.json --frameworks=LGPD,GDPR

# 3. Apply masking to detected PII
*apply-masking --strategy=sha256 --input=pii-findings.json

# 4. Run full compliance check
*check-compliance --frameworks=LGPD,GDPR,SOX --pipeline=MM_MDG_001

# 5. Generate audit trail
*audit-log --pipeline=MM_MDG_001 --output=audit-trail.log

# 6. Validate access controls
*validate-access --catalog=unity_catalog --schema=migration_staging
```

---

## Compliance Frameworks Supported

| Framework | Scope                          | Key Articles/Sections         |
| --------- | ------------------------------ | ----------------------------- |
| **LGPD**  | Brazilian data protection      | Art. 7–11 (legal bases, sensitive data) |
| **GDPR**  | EU data protection             | Art. 5–9 (principles, lawfulness, special categories) |
| **SOX**   | Financial reporting integrity  | Sections 302, 404 (internal controls) |
| **HIPAA** | US healthcare data             | Privacy Rule, Security Rule   |

---

## PII Types Detected

| PII Type        | Example               | Detection Method       |
| --------------- | ---------------------- | ---------------------- |
| `EMAIL`         | `user@example.com`    | Regex + Presidio       |
| `PHONE_NUMBER`  | `+55 11 99999-0000`   | Regex + Presidio       |
| `BR_CPF`        | `123.456.789-00`      | Regex + Check Digit    |
| `BR_CNPJ`       | `12.345.678/0001-00`  | Regex + Check Digit    |
| `CREDIT_CARD`   | `4111-1111-1111-1111` | Luhn + Presidio        |
| `IBAN`          | `BR18 0036 0305 ...`  | Regex + Presidio       |
| `PASSPORT`      | `AB123456`            | Regex + Presidio       |
| `ADDRESS`       | `Rua Example, 123`    | NLP + Presidio         |

---

## License

Proprietary — Avanade Migration Factory™
