# 🛡️ Data Governance Framework

> **Projeto:** NYC Green Taxi Analytics  
> **Versão:** 1.0  
> **Data:** 2026-02-05  
> **Autor:** 🛡️ Gaia (DataSteward)  
> **Referências:** [dq-rules.md](dq-rules.md) | [classification.md](classification.md) | [architecture.md](../architecture/architecture.md)

---

## 1. Sumário Executivo

Este documento estabelece o **Framework de Governança de Dados** para o projeto NYC Green Taxi Analytics, definindo papéis, responsabilidades, políticas, padrões e procedimentos para garantir que os dados sejam gerenciados como um ativo estratégico da organização.

### 1.1 Objetivos da Governança

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                            DATA GOVERNANCE OBJECTIVES                                    │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  1. QUALIDADE         Garantir ≥99% de qualidade de dados em todos os layers          │
│                                                                                         │
│  2. SEGURANÇA         Proteger dados confidenciais com controles apropriados           │
│                                                                                         │
│  3. COMPLIANCE        Atender requisitos regulatórios (GDPR, LGPD aplicáveis)          │
│                                                                                         │
│  4. ACESSO            Democratizar acesso a dados de forma controlada                   │
│                                                                                         │
│  5. RASTREABILIDADE   Manter lineage completa de todos os dados                        │
│                                                                                         │
│  6. EFICIÊNCIA        Reduzir duplicação e retrabalho com padrões                       │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Princípios de Governança

| Princípio | Descrição | Aplicação |
|-----------|-----------|-----------|
| **Data as an Asset** | Dados são um ativo estratégico | Tratados com mesmo rigor que ativos financeiros |
| **Single Source of Truth** | Uma única fonte confiável | Gold layer é a verdade para Analytics |
| **Metadata First** | Metadados são obrigatórios | Toda tabela tem description, owner, lineage |
| **Privacy by Design** | Privacidade desde o início | Classificação e masking planejados desde Bronze |
| **Fail Fast, Fix Fast** | Detectar e corrigir rapidamente | DQ em todas as camadas, alertas automáticos |
| **Transparency** | Visibilidade total | Lineage, audit logs, metrics públicos para stakeholders |

---

## 2. Governança Organizacional

### 2.1 Estrutura de Governança

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                          GOVERNANCE ORGANIZATION STRUCTURE                               │
└─────────────────────────────────────────────────────────────────────────────────────────┘

                              ┌──────────────────────────┐
                              │   EXECUTIVE SPONSOR      │
                              │   (Business Owner)       │
                              └────────────┬─────────────┘
                                           │
                                           ▼
                              ┌──────────────────────────┐
                              │  DATA GOVERNANCE BOARD   │
                              │  (Steering Committee)    │
                              └────────────┬─────────────┘
                                           │
                    ┌──────────────────────┼──────────────────────┐
                    │                      │                      │
                    ▼                      ▼                      ▼
          ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
          │  DATA STEWARD   │   │ TECHNICAL LEAD  │   │  BUSINESS OWNER │
          │  (Gaia)         │   │ (Diego)         │   │  (Mary)         │
          ├─────────────────┤   ├─────────────────┤   ├─────────────────┤
          │ • DQ Rules      │   │ • Architecture  │   │ • Requirements  │
          │ • Metadata      │   │ • Security      │   │ • Priorities    │
          │ • Standards     │   │ • Performance   │   │ • Acceptance    │
          └─────────────────┘   └─────────────────┘   └─────────────────┘
                    │                      │                      │
                    └──────────────────────┼──────────────────────┘
                                           │
                              ┌────────────┴─────────────┐
                              │                          │
                              ▼                          ▼
                    ┌─────────────────┐       ┌─────────────────┐
                    │  DATA ENGINEERS │       │  DATA ANALYSTS  │
                    │  (Execution)    │       │  (Consumption)  │
                    └─────────────────┘       └─────────────────┘
```

### 2.2 Roles & Responsibilities (RACI)

#### 2.2.1 Data Governance Board

**Composition:** Executive Sponsor, Business Owner (Mary), Data Steward (Gaia), Technical Lead (Diego)  
**Meeting Frequency:** Monthly  
**Responsibilities:**
- Approve governance policies and standards
- Review DQ metrics and trends
- Prioritize data initiatives
- Resolve escalated data issues
- Approve major architectural changes

#### 2.2.2 Data Steward (Gaia)

**Primary Responsibilities:**
- Define and maintain DQ rules
- Manage metadata catalog (Unity Catalog)
- Enforce data standards and naming conventions
- Classify data by sensitivity
- Monitor DQ metrics and quarantine resolution
- Coordinate data issue resolution

**Metrics Owned:**
- Overall DQ Score (target: ≥99%)
- Quarantine rate (target: ≤1%)
- Time to resolution (target: <24h)
- Metadata completeness (target: 100%)

#### 2.2.3 Technical Lead (Diego - DataEngineerExec)

**Primary Responsibilities:**
- Implement DQ rules in DLT pipelines
- Maintain architecture and infrastructure
- Ensure security controls are in place
- Optimize performance
- Implement monitoring and alerting

**Metrics Owned:**
- Pipeline SLA adherence (target: 100%)
- Security incidents (target: 0)
- Performance (query time <10s for BI)

#### 2.2.4 Business Owner (Mary - BusinessAnalyst)

**Primary Responsibilities:**
- Define business requirements for data
- Validate analytical outputs
- Accept deliverables at each gate
- Prioritize features and fixes

**Metrics Owned:**
- KPI accuracy (target: ±1%)
- User satisfaction (target: ≥4/5)

### 2.3 RACI Matrix - Key Activities

| Activity | Business Owner | Data Steward | Technical Lead | Data Engineer | Data Analyst |
|----------|----------------|--------------|----------------|---------------|--------------|
| **Define DQ Rules** | C | **R** | C | I | I |
| **Implement DQ Rules** | I | C | **R** | **A** | I |
| **Review Quarantine** | I | **R** | C | **A** | I |
| **Define Metadata Standards** | C | **R** | C | I | I |
| **Document Metadata** | I | **A** | C | **R** | I |
| **Classify Data** | C | **R** | C | I | C |
| **Approve Schema Changes** | C | **A** | **R** | C | I |
| **Grant Data Access** | I | **R** | C | I | **A** |
| **Monitor DQ Metrics** | I | **R** | C | **A** | I |
| **Resolve Data Issues** | C | **A** | C | **R** | I |
| **Create Reports** | C | C | I | I | **R** |
| **Validate KPIs** | **R** | **A** | I | I | C |

**Legend:**  
- **R** = Responsible (does the work)  
- **A** = Accountable (final approval)  
- **C** = Consulted (provides input)  
- **I** = Informed (kept updated)

---

## 3. Data Policies

### 3.1 Data Access Policy

#### 3.1.1 Access Principles

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              DATA ACCESS PRINCIPLES                                      │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  1. LEAST PRIVILEGE       Users receive minimum necessary access                        │
│                                                                                         │
│  2. NEED-TO-KNOW          Access granted based on business justification               │
│                                                                                         │
│  3. ROLE-BASED            Access via AAD groups, not individual grants                  │
│                                                                                         │
│  4. TEMPORARY ELEVATED    Admin access time-limited (max 8 hours)                       │
│                                                                                         │
│  5. AUDIT ALL ACCESS      All data access logged and reviewable                         │
│                                                                                         │
│  6. AUTOMATED REVOCATION  Access removed when role changes                              │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

#### 3.1.2 Access Matrix (Unity Catalog Permissions)

| Role | Catalog | Bronze Schema | Silver Schema | Gold Schema | Audit Schema | SQL Warehouse |
|------|---------|---------------|---------------|-------------|--------------|---------------|
| **Platform Admin** | ALL PRIVILEGES | ALL PRIVILEGES | ALL PRIVILEGES | ALL PRIVILEGES | ALL PRIVILEGES | Admin |
| **Data Engineer** | USE CATALOG | ALL PRIVILEGES | ALL PRIVILEGES | ALL PRIVILEGES | SELECT, INSERT | Can Use |
| **Data Analyst** | USE CATALOG | - | SELECT | SELECT | SELECT | Can Use |
| **BI Developer** | USE CATALOG | - | - | SELECT (views only) | - | Can Use |
| **Data Scientist** | USE CATALOG | - | SELECT | SELECT | SELECT | Can Use |
| **Business User** | - | - | - | - | - | - |

**Note:** Business Users access via Power BI only (no direct warehouse access)

#### 3.1.3 Access Request Process

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                            ACCESS REQUEST WORKFLOW                                       │
└─────────────────────────────────────────────────────────────────────────────────────────┘

  Step 1: REQUEST              Step 2: APPROVAL           Step 3: PROVISIONING
  ───────────────              ────────────────           ────────────────────

  ┌──────────────┐            ┌──────────────┐            ┌──────────────┐
  │ User submits │            │ Data Steward │            │ Tech Lead    │
  │ ticket with: │────────▶   │ reviews:     │────────▶   │ executes:    │
  │              │            │              │            │              │
  │ • Justification          │ • Business   │            │ • Grant Unity│
  │ • Data needed │            │   need       │            │   Catalog    │
  │ • Duration    │            │ • Classification        │   permissions│
  │ • Role        │            │   level      │            │ • Add to AAD │
  └──────────────┘            │ • Approve/   │            │   group      │
                              │   Reject     │            │ • Notify user│
                              └──────────────┘            └──────────────┘
                                     │                           │
                                     │ REJECT                    │
                                     ▼                           ▼
                              ┌──────────────┐            ┌──────────────┐
                              │ Notify user  │            │ Log in audit │
                              │ with reason  │            │ table        │
                              └──────────────┘            └──────────────┘

  SLA: 24 hours for standard requests, 4 hours for urgent
```

#### 3.1.4 Access Review Schedule

| Review Type | Frequency | Owner | Action |
|-------------|-----------|-------|--------|
| **User Access Certification** | Quarterly | Data Steward | Review all users, revoke inactive |
| **Admin Access Review** | Monthly | Technical Lead | Validate admin necessity |
| **Service Principal Audit** | Monthly | Technical Lead | Rotate secrets, validate usage |
| **AAD Group Membership** | Quarterly | Data Steward | Remove leavers, validate roles |
| **Privilege Escalation Review** | Weekly | Security Team | Review temporary admin grants |

### 3.2 Data Quality Policy

#### 3.2.1 Quality Standards

| Layer | Minimum Pass Rate | Critical Failures Allowed | Review Frequency |
|-------|-------------------|---------------------------|------------------|
| **Bronze** | ≥98% | 0 | Daily |
| **Silver** | ≥99% | 0 | Daily |
| **Gold** | ≥99.5% | 0 | Daily |
| **Cross-Layer** | Reconciliation ±0.1% | N/A | Daily |

#### 3.2.2 Quarantine Management

**Quarantine Review SLA:**
- **CRITICAL** severity: Dropped immediately, logged only (no review)
- **HIGH** severity: Review within 24 hours
- **MEDIUM** severity: Weekly batch review
- **LOW** severity: Monthly review (optional)

**Quarantine Resolution:**
```sql
-- Daily quarantine review query
SELECT 
    rule_id,
    severity,
    COUNT(*) AS record_count,
    MIN(quarantine_timestamp) AS oldest_record,
    MAX(quarantine_timestamp) AS newest_record,
    COLLECT_SET(field_name) AS affected_fields
FROM audit.quarantine_records
WHERE 
    reprocess_status = 'PENDING'
    AND severity IN ('HIGH', 'MEDIUM')
GROUP BY rule_id, severity
ORDER BY severity DESC, record_count DESC;
```

**Reprocessing Approval:**
- Data Engineer proposes fixes
- Data Steward approves reprocessing plan
- Technical Lead executes reprocessing
- Business Owner validates results

#### 3.2.3 DQ Incident Response

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                          DATA QUALITY INCIDENT RESPONSE                                  │
└─────────────────────────────────────────────────────────────────────────────────────────┘

  SEVERITY     RESPONSE TIME    NOTIFICATION              ESCALATION
  ────────     ─────────────    ────────────              ──────────

  🔴 CRITICAL   Immediate       #data-alerts, PagerDuty   → Tech Lead (immediate)
  (Pass <95%)                   Phone call to on-call     → Governance Board (if >4h)

  🟡 HIGH       <4 hours        #data-alerts, Email       → Data Steward (<4h)
  (Pass <99%)                                             → Tech Lead (<8h)

  🟢 MEDIUM     <24 hours       Email digest              → Data Steward (daily)
  (Pass <99.5%)

  ℹ️ LOW        <7 days         Weekly report             → None
  (Information)
```

### 3.3 Data Retention Policy

#### 3.3.1 Retention Periods by Layer

| Layer | Retention Period | Rationale | Backup Strategy |
|-------|------------------|-----------|-----------------|
| **Landing (Raw Files)** | 90 days | Legal requirement, reprocessing | ADLS lifecycle policy (move to Cool) |
| **Bronze** | 1 year | Audit trail, reprocessing | Delta Lake time travel (30 days) |
| **Silver** | 3 years | Regulatory, analytics | Delta Lake time travel (30 days) |
| **Gold** | 7 years | Financial reporting | Delta Lake time travel (90 days) |
| **Audit Logs** | 7 years | Compliance | GRS replication |
| **Quarantine** | 180 days | DQ investigation | Standard storage |

#### 3.3.2 Deletion Procedures

**Automated Deletion:**
```sql
-- Monthly VACUUM job (remove old Delta versions)
VACUUM bronze.lnd_green_tripdata RETAIN 720 HOURS;  -- 30 days
VACUUM silver.slv_trips RETAIN 720 HOURS;
VACUUM gold.fact_trips RETAIN 2160 HOURS;  -- 90 days

-- Quarterly quarantine cleanup
DELETE FROM audit.quarantine_records
WHERE quarantine_timestamp < current_date() - INTERVAL 180 DAYS;
```

**Manual Deletion Requests:**
- Requires Data Steward approval
- Must document business justification
- Log in audit.deletion_log table
- Verify no downstream dependencies

### 3.4 Data Privacy Policy

#### 3.4.1 Privacy Principles

**Note:** Este projeto usa dados públicos de táxis NYC que não contêm PII identificável. As políticas abaixo são **preventivas** para futuras expansões.

| Principle | Application | Example |
|-----------|-------------|---------|
| **Minimize Collection** | Collect only necessary data | No driver/passenger names |
| **Purpose Limitation** | Use data only for stated purpose | Analytics only, no marketing |
| **Transparency** | Users know what data is collected | Dashboard shows data sources |
| **Data Masking** | Mask sensitive fields in non-prod | Location IDs masked in dev/test |
| **Right to Deletion** | Support deletion requests | GDPR/LGPD compliance process |

#### 3.4.2 PII Handling (Future State)

**IF** projeto expandir para incluir PII:

```sql
-- Example: Column-level masking for non-privileged users
CREATE FUNCTION mask_location(location_id INT)
RETURNS INT
RETURN CASE 
    WHEN IS_ACCOUNT_GROUP_MEMBER('grp-nyctaxi-admins') THEN location_id
    ELSE -1  -- Masked for non-admins
END;

ALTER TABLE gold.fact_trips 
ALTER COLUMN pu_location_id 
SET MASK mask_location;
```

### 3.5 Security Policy

#### 3.5.1 Encryption Standards

| Component | At Rest | In Transit | Key Management |
|-----------|---------|------------|----------------|
| **ADLS Gen2** | AES-256 (Microsoft-managed) | TLS 1.2+ | Azure Key Vault |
| **Databricks Workspace** | AES-256 | TLS 1.2+ | Databricks-managed |
| **SQL Warehouse** | AES-256 | TLS 1.2+ | Databricks-managed |
| **Power BI** | AES-256 | TLS 1.2+ | Power BI encryption |
| **Secrets** | N/A | N/A | Azure Key Vault (FIPS 140-2) |

#### 3.5.2 Network Security

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              NETWORK SECURITY CONTROLS                                   │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  1. NO PUBLIC ENDPOINTS     All resources in VNet with Private Endpoints                │
│                                                                                         │
│  2. NSG RULES               Deny-all inbound, allow only required outbound              │
│                                                                                         │
│  3. WORKSPACE ISOLATION     Databricks in dedicated subnet with delegation              │
│                                                                                         │
│  4. FIREWALL                Azure Firewall for outbound internet (if needed)            │
│                                                                                         │
│  5. BASTION HOST            Secure admin access via Azure Bastion only                  │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

#### 3.5.3 Secret Management

**Mandatory:**
- All secrets in Azure Key Vault
- Databricks secret scopes backed by Key Vault
- Service principals with AAD authentication (no keys)
- Secret rotation every 90 days (automated)

**Prohibited:**
- Hard-coded credentials in code
- Secrets in Git repositories
- Sharing of personal credentials
- Storage account keys (use AAD tokens)

---

## 4. Data Standards

### 4.1 Naming Conventions

#### 4.1.1 Object Naming Standards

| Object Type | Pattern | Example | Case Sensitivity |
|-------------|---------|---------|------------------|
| **Catalog** | `{env}_nyctaxi` | `prod_nyctaxi` | lowercase |
| **Schema** | `{layer}` | `bronze`, `silver`, `gold` | lowercase |
| **Table** | `{prefix}_{entity}` | `lnd_green_tripdata`, `fact_trips` | lowercase + underscore |
| **Column** | `{name}_{suffix}` | `pickup_datetime`, `trip_distance` | lowercase + underscore |
| **Surrogate Key** | `{entity}_sk` | `payment_type_sk` | lowercase + _sk |
| **Natural Key** | `{entity}_id` | `payment_type_id` | lowercase + _id |
| **Foreign Key** | `{related_entity}_sk` | `date_sk` | lowercase + _sk |
| **Flag** | `is_{name}` | `is_weekend` | lowercase + is_ |
| **Amount** | `{name}_amount` | `fare_amount` | lowercase + _amount |
| **Count** | `{name}_count` | `passenger_count` | lowercase + _count |
| **Timestamp** | `{name}_timestamp` | `created_timestamp` | lowercase + _timestamp |
| **Date** | `{name}_date` | `pickup_date` | lowercase + _date |

#### 4.1.2 Naming Prohibited Patterns

**Avoid:**
- Reserved SQL keywords as names (`user`, `order`, `select`)
- Camel case or Pascal case (`pickupDateTime` ❌)
- Special characters (`pickup-datetime` ❌)
- Ambiguous abbreviations (`pckp_dt` ❌)
- Hungarian notation (`strFirstName` ❌)

**Preferred:**
- Descriptive names (`pickup_datetime` ✅)
- Consistent casing (`snake_case`)
- Clear abbreviations (`avg_speed_mph` ✅)

### 4.2 Data Type Standards

#### 4.2.1 Standard Data Types (Delta Lake)

| Logical Type | Delta Lake Type | Nullability | Default | Use Case |
|--------------|-----------------|-------------|---------|----------|
| **Identifier (Large)** | LONG | NOT NULL | - | Surrogate keys, row counts |
| **Identifier (Small)** | INT | NOT NULL | - | Codes, natural keys |
| **Text (Short)** | STRING | NULLABLE | NULL | Descriptions ≤255 chars |
| **Text (Long)** | STRING | NULLABLE | NULL | Comments, JSON |
| **Monetary** | DECIMAL(10,2) | NOT NULL | 0.00 | Amounts in USD |
| **Measurement** | DECIMAL(10,2) | NOT NULL | 0.00 | Distance, weight |
| **Percentage** | DECIMAL(5,2) | NOT NULL | 0.00 | Rates (0.00-100.00) |
| **Timestamp** | TIMESTAMP | NOT NULL | current_timestamp() | Event time |
| **Date** | DATE | NOT NULL | current_date() | Calendar date |
| **Boolean** | BOOLEAN | NOT NULL | FALSE | Flags |
| **JSON** | STRING | NULLABLE | NULL | Semi-structured data |

#### 4.2.2 Type Casting Rules

```python
# Standard type casting in DLT pipelines
from pyspark.sql.functions import *
from pyspark.sql.types import *

# Rule: Always specify precision for DECIMAL
.withColumn("fare_amount", col("fare_amount").cast(DecimalType(10, 2)))

# Rule: Use to_timestamp for string → timestamp conversion
.withColumn("pickup_datetime", to_timestamp("lpep_pickup_datetime", "yyyy-MM-dd HH:mm:ss"))

# Rule: Use COALESCE for nullable → NOT NULL with default
.withColumn("passenger_count", coalesce(col("passenger_count"), lit(1)))

# Rule: Validate before casting (expect_or_drop in DLT)
@dlt.expect_or_drop("valid_amount", "CAST(total_amount AS DECIMAL(10,2)) IS NOT NULL")
```

### 4.3 Metadata Standards

#### 4.3.1 Mandatory Metadata (Unity Catalog)

**Every table MUST have:**

```sql
CREATE TABLE gold.fact_trips (
    -- columns...
)
COMMENT 'Gold layer fact table containing trip-level transaction data'
TBLPROPERTIES (
    'owner' = 'diego@nyctaxi.com',
    'created_date' = '2026-02-05',
    'layer' = 'gold',
    'grain' = 'One row per trip',
    'source_systems' = 'NYC TLC Green Taxi',
    'refresh_frequency' = 'Daily',
    'quality_level' = 'high',
    'pii_data' = 'false',
    'sensitivity' = 'internal',
    'retention_days' = '2555'  -- 7 years
);
```

**Every column SHOULD have:**

```sql
ALTER TABLE gold.fact_trips 
ALTER COLUMN total_amount 
COMMENT 'Total trip cost including fare, tolls, tips, taxes - DECIMAL(10,2) - Source: total_amount';
```

#### 4.3.2 Metadata Documentation Process

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                          METADATA DOCUMENTATION WORKFLOW                                 │
└─────────────────────────────────────────────────────────────────────────────────────────┘

  CREATE TABLE             ADD METADATA              VALIDATE                CATALOG UPDATE
  ────────────             ────────────              ────────                ──────────────

  ┌──────────┐            ┌──────────┐            ┌──────────┐            ┌──────────┐
  │ Engineer │            │ Engineer │            │ Steward  │            │ Unity    │
  │ creates  │───────────▶│ adds     │───────────▶│ reviews  │───────────▶│ Catalog  │
  │ DDL      │            │ COMMENT, │            │ metadata │            │ indexed  │
  │          │            │ TBLPROPERTIES       │ completeness        │ lineage  │
  └──────────┘            └──────────┘            └──────────┘            └──────────┘

  Required fields:
  • Table COMMENT
  • owner
  • layer
  • grain
  • sensitivity
```

#### 4.3.3 Metadata Completeness Target

| Metadata Field | Target Completeness | Validated By | Frequency |
|----------------|---------------------|--------------|-----------|
| Table COMMENT | 100% | Data Steward | At PR review |
| owner | 100% | Data Steward | At PR review |
| layer | 100% | Data Steward | At PR review |
| grain | 100% (fact/dims) | Data Steward | At PR review |
| Column COMMENT | 100% (key columns) | Data Steward | At PR review |
| sensitivity | 100% | Data Steward | At creation |

---

## 5. Procedures

### 5.1 Change Management

#### 5.1.1 Schema Change Process

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              SCHEMA CHANGE WORKFLOW                                      │
└─────────────────────────────────────────────────────────────────────────────────────────┘

  MINOR CHANGE (Backward Compatible)          MAJOR CHANGE (Breaking)
  ──────────────────────────────────          ───────────────────────

  Examples:                                    Examples:
  • Add new column                              • Drop column
  • Add new table                               • Rename column
  • Modify column comment                       • Change data type
                                                • Change NOT NULL constraint

  ┌──────────────┐                            ┌──────────────┐
  │ 1. Engineer  │                            │ 1. Engineer  │
  │    submits PR│                            │    submits PR│
  └──────┬───────┘                            └──────┬───────┘
         │                                           │
         ▼                                           ▼
  ┌──────────────┐                            ┌──────────────┐
  │ 2. Steward   │                            │ 2. Steward   │
  │    reviews   │                            │    impact    │
  │    metadata  │                            │    analysis  │
  └──────┬───────┘                            └──────┬───────┘
         │                                           │
         ├─ Approve ──▶ Deploy                       ▼
         │                                    ┌──────────────┐
         └─ Reject ───▶ Revise               │ 3. Notify    │
                                              │    consumers │
                                              └──────┬───────┘
                                                     │
                                                     ▼
                                              ┌──────────────┐
                                              │ 4. Governance│
                                              │    Board     │
                                              │    approval  │
                                              └──────┬───────┘
                                                     │
                                                     ├─ Approve ──▶ Deploy
                                                     │
                                                     └─ Reject ───▶ Redesign
```

#### 5.1.2 Change Categories

| Category | Approval Required | Notification | Deployment Window |
|----------|-------------------|--------------|-------------------|
| **Emergency Fix** | Technical Lead | Governance Board (after) | Immediate |
| **Minor Change** | Data Steward | None | Any time |
| **Major Change** | Governance Board | All consumers (7 days prior) | Scheduled maintenance |
| **New Feature** | Business Owner | Stakeholders | Sprint boundary |

#### 5.1.3 Rollback Plan

**Every major change requires:**
```markdown
## Rollback Plan

### Detection
- Metric to monitor: {metric_name}
- Threshold: {value}
- Detection time: <10 minutes

### Rollback Steps
1. Stop {pipeline_name} workflow
2. Restore {table_name} to VERSION AS OF {n-1}
3. Revert {code_repo} to commit {hash}
4. Restart {pipeline_name} workflow
5. Validate {validation_query}

### Rollback Time
- Estimated: {X} minutes
- Tested: Yes/No

### Communication
- Notify: {stakeholder_list}
- Channel: {Slack/email}
```

### 5.2 Data Issue Resolution

#### 5.2.1 Issue Severity Classification

| Severity | Definition | Response SLA | Examples |
|----------|------------|--------------|----------|
| **P0 - Critical** | Pipeline stopped, no data | <1 hour | DLT pipeline failed, storage unreachable |
| **P1 - High** | Wrong data in production | <4 hours | Incorrect KPI, missing trips |
| **P2 - Medium** | Data quality degraded | <24 hours | High quarantine rate, schema drift |
| **P3 - Low** | Enhancement request | <7 days | New column request, performance optimization |

#### 5.2.2 Issue Escalation Path

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              ISSUE ESCALATION PATH                                       │
└─────────────────────────────────────────────────────────────────────────────────────────┘

  P3 (Low)                P2 (Medium)             P1 (High)               P0 (Critical)
  ────────                ───────────             ─────────               ─────────────

  ┌──────────┐            ┌──────────┐            ┌──────────┐            ┌──────────┐
  │ Engineer │            │ Engineer │            │ On-call  │            │ On-call  │
  │ assigned │            │ assigned │            │ Engineer │            │ Engineer │
  └────┬─────┘            └────┬─────┘            └────┬─────┘            └────┬─────┘
       │                       │                       │                       │
       │ (if >7d)              │ (if >24h)             │ (if >2h)              │ (if >30min)
       ▼                       ▼                       ▼                       ▼
  ┌──────────┐            ┌──────────┐            ┌──────────┐            ┌──────────┐
  │ Data     │            │ Tech     │            │ Tech     │            │ CTO /    │
  │ Steward  │            │ Lead     │            │ Lead     │            │ Sponsor  │
  └──────────┘            └────┬─────┘            └────┬─────┘            └──────────┘
                               │                       │
                               │ (if >48h)             │ (if >4h)
                               ▼                       ▼
                          ┌──────────┐            ┌──────────┐
                          │ Governance            │ Governance
                          │ Board    │            │ Board    │
                          └──────────┘            └──────────┘
```

#### 5.2.3 Post-Incident Review

**For P0 and P1 incidents, conduct Post-Incident Review (PIR):**

```markdown
## Post-Incident Review Template

### Incident Summary
- **Incident ID:** PIR-2026-001
- **Date/Time:** 2026-02-05 14:30 UTC
- **Duration:** 2 hours
- **Severity:** P1 - High
- **Affected Systems:** Silver layer, fact_trips

### Timeline
- 14:30 - Issue detected (alert triggered)
- 14:35 - On-call engineer notified
- 14:50 - Root cause identified
- 15:30 - Fix deployed
- 16:30 - Validation complete

### Root Cause
{Detailed explanation of what went wrong}

### Resolution
{What was done to fix the issue}

### Impact
- Records affected: {number}
- Downtime: {duration}
- Data loss: {yes/no}

### Prevention Measures
1. {Action item 1} - Owner: {name} - Due: {date}
2. {Action item 2} - Owner: {name} - Due: {date}

### Lessons Learned
{What we learned and how to improve}
```

### 5.3 Access Request Process

**(See Section 3.1.3 for detailed workflow)**

**Standard SLA:**
- Request submission: Self-service ticket
- Approval: 24 hours (4 hours for urgent)
- Provisioning: 1 hour after approval

### 5.4 Onboarding/Offboarding

#### 5.4.1 User Onboarding Checklist

```markdown
## New User Onboarding - {User Name}

### Day 1: Access Setup
- [ ] AAD account created
- [ ] Added to appropriate AAD group based on role
- [ ] Unity Catalog permissions granted
- [ ] Databricks workspace access configured
- [ ] Power BI license assigned (if needed)

### Week 1: Training
- [ ] Governance policies review
- [ ] Data catalog introduction (Unity Catalog)
- [ ] DQ rules training
- [ ] BI tools training (Power BI)
- [ ] Security awareness training

### Week 2: Validation
- [ ] Can query Gold layer tables
- [ ] Can view DQ dashboard
- [ ] Can create reports (BI Developer)
- [ ] Understands escalation procedures
```

#### 5.4.2 User Offboarding Checklist

```markdown
## User Offboarding - {User Name}

### Immediate (Last Working Day)
- [ ] Disable AAD account
- [ ] Remove from all AAD groups
- [ ] Revoke Unity Catalog permissions
- [ ] Revoke Databricks workspace access
- [ ] Revoke Power BI license
- [ ] Invalidate service principal secrets (if applicable)

### Within 7 Days
- [ ] Transfer ownership of created objects
- [ ] Document knowledge handover
- [ ] Archive user's notebooks/queries
- [ ] Update RACI matrix

### Within 30 Days
- [ ] Delete personal folders (after backup)
- [ ] Remove from distribution lists
- [ ] Update documentation (remove as owner)
```

---

## 6. Governance Metrics

### 6.1 Key Governance Metrics

```sql
-- Governance Scorecard (to be displayed in executive dashboard)
CREATE OR REPLACE VIEW audit.vw_governance_scorecard AS
SELECT
    current_date() AS report_date,
    
    -- Data Quality Metrics
    (SELECT ROUND(AVG(pass_rate_pct), 2) 
     FROM audit.vw_dq_daily_metrics 
     WHERE metric_date = current_date()) AS overall_dq_score,
    
    (SELECT ROUND(AVG(quarantine_rate_pct), 2) 
     FROM audit.vw_dq_daily_metrics 
     WHERE metric_date = current_date()) AS quarantine_rate,
    
    (SELECT COUNT(*) 
     FROM audit.quarantine_records 
     WHERE reprocess_status = 'PENDING' AND severity = 'HIGH') AS pending_quarantine_count,
    
    -- Metadata Completeness
    (SELECT ROUND(100.0 * COUNT(CASE WHEN comment IS NOT NULL THEN 1 END) / COUNT(*), 2)
     FROM information_schema.tables
     WHERE table_schema IN ('bronze', 'silver', 'gold')) AS metadata_table_completeness_pct,
    
    (SELECT ROUND(100.0 * COUNT(CASE WHEN comment IS NOT NULL THEN 1 END) / COUNT(*), 2)
     FROM information_schema.columns
     WHERE table_schema IN ('bronze', 'silver', 'gold')) AS metadata_column_completeness_pct,
    
    -- Access Governance
    (SELECT COUNT(DISTINCT grantee) 
     FROM information_schema.table_privileges 
     WHERE table_schema = 'gold') AS unique_users_with_access,
    
    (SELECT COUNT(*) 
     FROM audit.access_requests 
     WHERE status = 'PENDING') AS pending_access_requests,
    
    -- Security
    (SELECT COUNT(*) 
     FROM audit.security_incidents 
     WHERE incident_date >= current_date() - INTERVAL 30 DAYS) AS security_incidents_30d,
    
    -- Pipeline Health
    (SELECT ROUND(100.0 * COUNT(CASE WHEN status = 'SUCCESS' THEN 1 END) / COUNT(*), 2)
     FROM audit.pipeline_runs
     WHERE DATE(start_timestamp) = current_date()) AS pipeline_success_rate_pct;
```

### 6.2 Metric Targets & Thresholds

| Metric | Target | Threshold | Alert If | Owner |
|--------|--------|-----------|----------|-------|
| **Overall DQ Score** | ≥99% | ≥95% | <95% | Data Steward |
| **Quarantine Rate** | ≤1% | ≤5% | >5% | Data Steward |
| **Pending Quarantine (HIGH)** | 0 | <10 | >10 | Data Engineer |
| **Metadata Table Completeness** | 100% | 100% | <100% | Data Steward |
| **Metadata Column Completeness** | 100% (key cols) | ≥80% | <80% | Data Steward |
| **Pending Access Requests** | 0 (SLA met) | <5 | >5 for >24h | Data Steward |
| **Security Incidents (30d)** | 0 | 0 | >0 | Technical Lead |
| **Pipeline Success Rate** | 100% | ≥99% | <99% | Technical Lead |

### 6.3 Reporting Schedule

| Report | Audience | Frequency | Delivery Method | Owner |
|--------|----------|-----------|-----------------|-------|
| **DQ Daily Digest** | Data Team | Daily | Slack #data-alerts | Data Steward |
| **Governance Scorecard** | Governance Board | Weekly | Power BI Dashboard | Data Steward |
| **Quarantine Review** | Data Engineers | Daily (if pending >0) | Email | Data Steward |
| **Access Audit Report** | Governance Board | Quarterly | PDF Report | Data Steward |
| **Security Incident Report** | CISO, Governance Board | Monthly | Email | Technical Lead |
| **Metadata Completeness** | Data Steward | Weekly | Power BI Dashboard | Data Steward |
| **Pipeline Health Report** | Technical Lead | Daily | Databricks Workflow UI | Technical Lead |

---

## 7. Compliance & Audit

### 7.1 Regulatory Considerations

**Note:** NYC Taxi data é público e não contém PII. As políticas abaixo aplicam-se caso projeto expanda.

| Regulation | Applicability | Requirements | Implementation |
|------------|---------------|--------------|----------------|
| **GDPR** | If EU citizens' data | Right to deletion, consent | Deletion procedures, audit logs |
| **LGPD** | If Brazilian citizens' data | Data minimization, consent | PII classification, retention |
| **SOC 2** | If SaaS offering | Security controls, audit logs | Encryption, access logs |
| **SOX** | If financial reporting | Data accuracy, retention | 7-year retention, DQ controls |

### 7.2 Audit Log Requirements

```sql
-- Comprehensive audit logging
CREATE TABLE audit.access_log (
    log_id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    timestamp           TIMESTAMP NOT NULL DEFAULT current_timestamp(),
    user_identity       STRING NOT NULL,
    action              STRING NOT NULL,  -- SELECT, INSERT, UPDATE, DELETE, GRANT
    object_type         STRING NOT NULL,  -- TABLE, VIEW, SCHEMA
    object_name         STRING NOT NULL,
    rows_affected       BIGINT,
    query_text          STRING,
    source_ip           STRING,
    application         STRING,
    success             BOOLEAN NOT NULL
)
PARTITIONED BY (DATE(timestamp))
TBLPROPERTIES ('delta.logRetentionDuration' = '2555 days');  -- 7 years

-- Log retention: 7 years (SOX compliance)
-- Daily summary reports for security team
```

### 7.3 Audit Trail Queries

```sql
-- Who accessed what, when?
SELECT 
    DATE(timestamp) AS access_date,
    user_identity,
    COUNT(*) AS query_count,
    COUNT(DISTINCT object_name) AS unique_objects_accessed,
    COLLECT_SET(object_name) AS objects_accessed
FROM audit.access_log
WHERE timestamp >= current_date() - INTERVAL 30 DAYS
GROUP BY DATE(timestamp), user_identity
ORDER BY access_date DESC, query_count DESC;

-- Unusual access patterns
SELECT 
    user_identity,
    HOUR(timestamp) AS access_hour,
    COUNT(*) AS access_count
FROM audit.access_log
WHERE DATE(timestamp) = current_date()
GROUP BY user_identity, HOUR(timestamp)
HAVING access_hour NOT BETWEEN 6 AND 22  -- Outside business hours
ORDER BY access_count DESC;
```

---

## 8. Training & Awareness

### 8.1 Training Program

| Role | Training Module | Duration | Frequency | Format |
|------|----------------|----------|-----------|--------|
| **All Users** | Data Governance Overview | 1 hour | Onboarding | Video + Quiz |
| **All Users** | Security Awareness | 30 min | Annual | Video + Quiz |
| **Data Engineers** | DQ Implementation (DLT) | 4 hours | Onboarding | Hands-on Lab |
| **Data Engineers** | Unity Catalog Deep Dive | 2 hours | Onboarding | Presentation |
| **Data Analysts** | Data Catalog Usage | 1 hour | Onboarding | Hands-on Demo |
| **BI Developers** | Metadata Standards | 1 hour | Onboarding | Presentation |
| **Governance Board** | Metrics & KPIs | 2 hours | Quarterly | Dashboard Review |

### 8.2 Documentation Repository

```
Docs/
├── governance/
│   ├── governance.md                  (this document)
│   ├── dq-rules.md                    (DQ rules detailed)
│   ├── classification.md              (data classification)
│   ├── runbooks/
│   │   ├── quarantine-review.md
│   │   ├── access-request.md
│   │   ├── schema-change.md
│   │   └── incident-response.md
│   └── training/
│       ├── onboarding-checklist.md
│       └── dq-training.pptx
```

---

## 9. Continuous Improvement

### 9.1 Governance Maturity Model

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                          DATA GOVERNANCE MATURITY MODEL                                  │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  LEVEL 1: INITIAL          LEVEL 2: MANAGED         LEVEL 3: DEFINED                    │
│  (Ad-hoc)                  (Repeatable)             (Standardized) ◀── WE ARE HERE      │
│  ─────────                 ──────────               ──────────────                       │
│                                                                                         │
│  • No standards            • Basic policies         • Comprehensive policies            │
│  • Manual processes        • Some automation        • Automated DQ checks               │
│  • No DQ rules             • Basic DQ rules         • 73 DQ rules implemented           │
│  • No metadata             • Partial metadata       • 100% metadata coverage            │
│                                                                                         │
│  LEVEL 4: QUANTITATIVELY   LEVEL 5: OPTIMIZING                                          │
│  MANAGED (Measured)        (Continuous Improvement)                                     │
│  ───────────────           ───────────────────                                          │
│                                                                                         │
│  • Predictive metrics      • ML-driven DQ                                               │
│  • SLA-driven              • Auto-remediation                                           │
│  • Continuous monitoring   • Proactive governance                                       │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

**Current Maturity:** Level 3 (Defined)  
**Target (1 year):** Level 4 (Quantitatively Managed)

### 9.2 Improvement Roadmap

| Quarter | Initiative | Goal | Owner |
|---------|-----------|------|-------|
| **Q1 2026** | Implement governance framework | Baseline established | Data Steward |
| **Q2 2026** | Automate quarantine review | 80% auto-fix rate | Data Engineer |
| **Q3 2026** | Predictive DQ alerts | Detect issues before they escalate | Data Scientist |
| **Q4 2026** | Self-service data catalog | Users can discover data without asking | Data Steward |
| **Q1 2027** | ML-driven anomaly detection | Reduce false positives by 50% | Data Scientist |

### 9.3 Feedback Mechanisms

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                          GOVERNANCE FEEDBACK LOOP                                        │
└─────────────────────────────────────────────────────────────────────────────────────────┘

  COLLECT FEEDBACK          ANALYZE               PRIORITIZE              IMPLEMENT
  ────────────────          ───────               ──────────              ─────────

  ┌──────────────┐         ┌──────────────┐      ┌──────────────┐      ┌──────────────┐
  │ • Surveys    │         │ Governance   │      │ Board votes  │      │ Update       │
  │ • Incidents  │────────▶│ Board        │─────▶│ on top 3     │─────▶│ policies     │
  │ • Metrics    │         │ reviews      │      │ improvements │      │ & standards  │
  │ • Suggestions│         │ feedback     │      │              │      │              │
  └──────────────┘         └──────────────┘      └──────────────┘      └──────────────┘
        ▲                                                                      │
        │                                                                      │
        └──────────────────────────────────────────────────────────────────────┘
                                    MEASURE IMPACT
```

**Feedback Channels:**
- Quarterly user survey (satisfaction, pain points)
- Monthly metrics review (Governance Board)
- Issue tracker analysis (common problems)
- Post-incident reviews (lessons learned)

---

## 10. Próximos Artefatos

Este documento alimenta:

| Artefato | Agente | Propósito |
|----------|--------|-----------|
| `classification.md` | 🛡️ Gaia | Classificação de sensibilidade de dados |
| `data-lineage.md` | 🛡️ Gaia | Documentação de linhagem de dados |
| `compliance-mapping.md` | 🛡️ Gaia | Mapeamento de requisitos regulatórios |
| `notebooks/governance_*.py` | 🛠️ Diego | Implementação de políticas em código |

---

## Histórico de Versões

| Versão | Data | Autor | Alterações |
|--------|------|-------|------------|
| 1.0 | 2026-02-05 | Gaia (DataSteward) | Versão inicial - Framework completo de governança |

---

*Documento gerado pelo 🛡️ DataSteward Agent - Avanade™ Core*
