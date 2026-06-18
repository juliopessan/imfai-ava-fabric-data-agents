# SDD: security-compliance (Scan for PII & Compliance)

**Role:** Identify sensitive data. Ensure compliance (LGPD, GDPR, SOC2).

---

## Input Contract

```
Required:
  ├─ data-model.md: File — column definitions
  ├─ discovery_inventory.json: File — legacy objects
  ├─ compliance_policies: Dict — LGPD|GDPR|SOC2 rules
  └─ pii_patterns: Dict — regex for PII detection
```

---

## Task Definition

1. **Scan** all columns for PII (email, phone, SSN, card, medical data)
2. **Match** against compliance policies
3. **Flag** columns requiring:
   - Masking
   - Encryption
   - Access controls
   - Audit logging
4. **Generate** remediation plan

---

## Output

```
Produces:
  ├─ pii-catalog.json: {column, pii_type, risk_level, remediation}
  ├─ compliance-checklist.md: LGPD/GDPR/SOC2 alignment
  └─ security-controls.md: Required masking/encryption/RBAC

Passes To: code-generator (for masking DDL) & downstream-executor
```

---

**Status:** ✅ ACTIVE | **Updated:** 2026-06-16