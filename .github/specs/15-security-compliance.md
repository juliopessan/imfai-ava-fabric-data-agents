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

## Success Criteria

- ✅ 100% of columns scanned against pii_patterns (no skipped tables)
- ✅ Every PII match assigned a risk level and a required control (masking, encryption, RBAC, or audit logging)
- ✅ Compliance checklist covers every policy in compliance_policies

---

## Output Contract

```
Produces:
  ├─ pii-catalog.json: {column, pii_type, risk_level, remediation}
  ├─ compliance-checklist.md: LGPD/GDPR/SOC2 alignment
  └─ security-controls.md: Required masking/encryption/RBAC

Passes To: code-generator (for masking DDL) & downstream-executor
```

---

## Constraints

🔴 NO GUESSING PII classification — match against pii_patterns and compliance_policies only
🔴 Every flagged column must show its required control (masking/encryption/RBAC/audit)
🟡 If a pattern is ambiguous, flag for human review instead of deciding silently

---

**Status:** ✅ ACTIVE | **Updated:** 2026-06-16