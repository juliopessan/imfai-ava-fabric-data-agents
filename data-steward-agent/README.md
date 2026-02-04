# DataSteward Agent

**Avanade™ Core Data Agent**

---

## Overview

The DataSteward agent is responsible for establishing data governance frameworks, defining comprehensive data quality rules, ensuring compliance with regulations, and managing data classification.

---

## Agent Details

| Attribute | Value |
|-----------|-------|
| **Icon** | 🛡️ |
| **Phase** | MIDSTREAM |
| **Gate** | Gate 2 |
| **Dependencies** | BusinessAnalyst (DQ initial), DataArchitect (data model) |
| **Artifacts** | dq-rules.md, governance.md, classification.md |

---

## Activation

### VS Code Chatmode

Use the DataSteward chatmode:
```
@data-steward
```

### Available Commands

| Command | Description |
|---------|-------------|
| `*help` | Show available commands |
| `*status` | Current progress on Gate 2 artifacts |
| `*create-dq-rules` | Define comprehensive DQ rules |
| `*create-governance` | Create governance framework |
| `*classify-data` | Classify data by sensitivity |
| `*map-compliance` | Map regulatory requirements |
| `*document-lineage` | Document data lineage |

---

## Gate 2 Deliverables

### Required Artifacts

1. **dq-rules.md**
   - DQ rules by layer (Bronze, Silver, Gold)
   - Severity levels and actions
   - Quarantine strategy
   - Threshold alerts

2. **governance.md**
   - Roles and responsibilities (RACI)
   - Data policies
   - Standards and procedures
   - Governance metrics

3. **classification.md**
   - Sensitivity levels
   - Entity classification
   - Column-level classification
   - Handling requirements

---

## Data Quality Rule Types

| Type | Description | Example |
|------|-------------|---------|
| Completeness | Check for nulls | NOT NULL on required columns |
| Validity | Format/range checks | Amount between 0 and 999999 |
| Uniqueness | Duplicate detection | Unique business key |
| Referential | FK validation | vendor_id exists in dim_vendor |
| Consistency | Cross-field validation | pickup_time < dropoff_time |
| Timeliness | Freshness checks | Data < 24 hours old |

---

## Severity Levels

| Severity | Action | Use When |
|----------|--------|----------|
| CRITICAL | Reject record | Breaks downstream processing |
| HIGH | Quarantine | Significant business impact |
| MEDIUM | Flag record | Moderate impact |
| LOW | Log only | Minor/informational |

---

## Classification Levels

| Level | Description | Controls |
|-------|-------------|----------|
| PUBLIC | Non-sensitive | None |
| INTERNAL | Business use only | Access control |
| CONFIDENTIAL | Sensitive business | Encryption + RBAC |
| RESTRICTED | PII/PHI/PCI | Full protection + audit |

---

## Workflow

### Typical Session

```
User: @data-steward let's define DQ rules

Agent: I'll help define data quality rules. Let me review 
       the data model and initial DQ requirements...
       
       Based on the model, I'll create rules for:
       - Bronze: Schema validation, null checks
       - Silver: Business rules, referential integrity  
       - Gold: Aggregation validation
       
       Should I proceed?
```

### Sequential Tasks

1. **Start**: `*create-dq-rules`
   - Review data model
   - Define rules per layer
   - Set severity levels
   - Define quarantine strategy

2. **Then**: `*create-governance`
   - Define roles (RACI)
   - Create policies
   - Document standards

3. **Finally**: `*classify-data`
   - Classify entities
   - Identify sensitive columns
   - Define masking rules

---

## Integration Points

### Upstream (Gate 1 + Gate 2)

Receives from:
- **BusinessAnalyst**: Initial DQ requirements
- **DataArchitect**: Data model, architecture

### Downstream (Gate 2 → Gate 3)

Provides to:
- **DataFlow**: DQ rules for ETL implementation
- **InsightForge**: Governance rules for BI
- **Orchestrator**: Gate 2 validation artifacts

---

## File Structure

```
data-steward-agent/
├── .avanade-core/
│   ├── agents/
│   │   └── data-steward.md
│   ├── core-config.yaml
│   ├── tasks/
│   │   ├── create-dq-rules.md
│   │   ├── create-governance.md
│   │   └── classify-data.md
│   ├── checklists/
│   │   └── data-steward-checklist.md
│   ├── templates/
│   │   ├── dq-rules-tmpl.yaml
│   │   ├── governance-tmpl.yaml
│   │   └── classification-tmpl.yaml
│   └── data/
│       └── governance-best-practices.md
└── README.md
```

---

## Best Practices

1. **Fail Fast**: Critical rules should block processing
2. **Never Drop**: Always quarantine, never silently discard
3. **Enable Investigation**: Capture context with failed records
4. **Balance Strictness**: Too strict = blocked pipelines
5. **Automate Enforcement**: Technical controls > paper policies
6. **Regular Review**: Classification and rules need updates

---

## Related Agents

| Agent | Relationship |
|-------|--------------|
| **Orchestrator** | Validates Gate 2 readiness |
| **BusinessAnalyst** | Provides initial DQ requirements |
| **DataArchitect** | Provides data model |
| **DataFlow** | Implements DQ rules in ETL |
| **InsightForge** | Applies governance in BI |

---

*Avanade™ Core - DataSteward Agent*
