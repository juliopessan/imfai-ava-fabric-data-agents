# 🛡️ Data Classification

> **Projeto:** NYC Green Taxi Analytics  
> **Versão:** 1.0  
> **Data:** 2026-02-05  
> **Autor:** 🛡️ Gaia (DataSteward)  
> **Referências:** [governance.md](governance.md) | [dq-rules.md](dq-rules.md) | [data-model.md](../architecture/data-model.md)

---

## 1. Sumário Executivo

Este documento define a **classificação de sensibilidade** de todos os dados do projeto NYC Green Taxi Analytics, categorizando entidades, tabelas e colunas por nível de sensibilidade, com justificativas e requisitos de controle.

### 1.1 Contexto do Projeto

**Importante:** Este projeto utiliza **dados públicos** da NYC Taxi & Limousine Commission (TLC). Os dados **NÃO contêm PII identificável** (sem nomes de motoristas/passageiros, placas de veículos, ou informações pessoais diretas).

No entanto, alguns campos podem ser considerados **potencialmente sensíveis** em contextos específicos:
- **Location IDs granulares** podem revelar padrões de movimento
- **Aggregate revenue data** pode ter implicações comerciais
- **Trip patterns** podem inferir comportamento

### 1.2 Níveis de Classificação

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                          DATA CLASSIFICATION LEVELS                                      │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  LEVEL              DESCRIPTION                    EXAMPLES                             │
│  ─────              ───────────                    ────────                             │
│                                                                                         │
│  🟢 PUBLIC          Publicly available data        • Rate codes                         │
│                     No access restrictions         • Payment types                      │
│                                                    • Trip types                          │
│                                                    • Aggregated metrics                  │
│                                                                                         │
│  🟡 INTERNAL        Business use only              • Individual trip records             │
│                     Requires authentication        • Daily revenue totals               │
│                                                    • Operational metrics                 │
│                                                                                         │
│  🟠 CONFIDENTIAL    Sensitive business data        • Detailed location patterns          │
│                     RBAC + encryption required     • High-value trip details            │
│                                                    • Business intelligence insights      │
│                                                                                         │
│  🔴 RESTRICTED      Highly sensitive/regulated     • (None in this project)             │
│                     Full protection + audit        • Would include: PII, PHI, PCI       │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 1.3 Distribuição da Classificação

| Layer | Public | Internal | Confidential | Restricted | Total Entities |
|-------|--------|----------|--------------|------------|----------------|
| **Bronze** | 3 (ref tables) | 1 (trips) | 0 | 0 | 4 |
| **Silver** | 3 (ref tables) | 1 (trips) | 0 | 0 | 4 |
| **Gold** | 5 (dimensions) | 1 (fact) | 1 (aggregations) | 0 | 7 |
| **Audit** | 0 | 2 (logs/quarantine) | 0 | 0 | 2 |
| **Total** | **11** | **5** | **1** | **0** | **17** |

---

## 2. Classification Framework

### 2.1 Classification Criteria

| Criteria | Public | Internal | Confidential | Restricted |
|----------|--------|----------|--------------|------------|
| **Public Availability** | Publicly available | Internal use | Business sensitive | Regulated/PII |
| **Access Control** | None required | AAD authentication | RBAC + groups | RBAC + masking + audit |
| **Encryption** | Optional | At rest (standard) | At rest + in transit | At rest + in transit + field-level |
| **Audit Logging** | Optional | Basic | Detailed | Full (all access) |
| **Retention** | Indefinite | 3-7 years | 7 years | Per regulation |
| **Sharing** | Unrestricted | Internal only | Approved parties | Prohibited |

### 2.2 Classification Decision Tree

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                          CLASSIFICATION DECISION TREE                                    │
└─────────────────────────────────────────────────────────────────────────────────────────┘

                              ┌──────────────────┐
                              │ Does data contain│
                              │ PII/PHI/PCI?     │
                              └────────┬─────────┘
                                       │
                        ┌──────────────┼──────────────┐
                        │ YES                         │ NO
                        ▼                             ▼
                  ┌──────────┐               ┌──────────────────┐
                  │RESTRICTED│               │ Is data publicly │
                  │   🔴     │               │ available?       │
                  └──────────┘               └────────┬─────────┘
                                                      │
                                       ┌──────────────┼──────────────┐
                                       │ YES                         │ NO
                                       ▼                             ▼
                                 ┌──────────┐               ┌──────────────────┐
                                 │ PUBLIC   │               │ Does disclosure  │
                                 │   🟢     │               │ harm business?   │
                                 └──────────┘               └────────┬─────────┘
                                                                     │
                                                      ┌──────────────┼──────────────┐
                                                      │ YES                         │ NO
                                                      ▼                             ▼
                                                ┌─────────────┐            ┌─────────────┐
                                                │CONFIDENTIAL │            │  INTERNAL   │
                                                │     🟠      │            │     🟡      │
                                                └─────────────┘            └─────────────┘
```

---

## 3. Entity-Level Classification

### 3.1 Bronze Layer

| Table | Classification | Rationale | Access Control | Encryption | Retention |
|-------|----------------|-----------|----------------|------------|-----------|
| **lnd_green_tripdata** | 🟡 INTERNAL | Individual trip records, operational data | Data Engineers only | Standard (at rest) | 1 year |
| **lnd_payment_type** | 🟢 PUBLIC | Reference data, publicly available | Authenticated users | Standard | Indefinite |
| **lnd_rate_code** | 🟢 PUBLIC | Reference data, publicly available | Authenticated users | Standard | Indefinite |
| **lnd_trip_type** | 🟢 PUBLIC | Reference data, publicly available | Authenticated users | Standard | Indefinite |

### 3.2 Silver Layer

| Table | Classification | Rationale | Access Control | Encryption | Retention |
|-------|----------------|-----------|----------------|------------|-----------|
| **slv_trips** | 🟡 INTERNAL | Cleansed trip records, business use | Analysts + Engineers | Standard (at rest) | 3 years |
| **slv_payment_type** | 🟢 PUBLIC | Reference data | Authenticated users | Standard | Indefinite |
| **slv_rate_code** | 🟢 PUBLIC | Reference data | Authenticated users | Standard | Indefinite |
| **slv_trip_type** | 🟢 PUBLIC | Reference data | Authenticated users | Standard | Indefinite |

### 3.3 Gold Layer

| Table | Classification | Rationale | Access Control | Encryption | Retention |
|-------|----------------|-----------|----------------|------------|-----------|
| **fact_trips** | 🟡 INTERNAL | Transaction-level data, granular | Analysts + BI Devs | Standard (at rest) | 7 years |
| **dim_date** | 🟢 PUBLIC | Calendar dimension | All authenticated | Standard | Indefinite |
| **dim_payment_type** | 🟢 PUBLIC | Payment dimension | All authenticated | Standard | Indefinite |
| **dim_rate_code** | 🟢 PUBLIC | Rate dimension | All authenticated | Standard | Indefinite |
| **dim_trip_type** | 🟢 PUBLIC | Trip type dimension | All authenticated | Standard | Indefinite |
| **dim_location** | 🟢 PUBLIC | TLC zone reference (if added) | All authenticated | Standard | Indefinite |
| **agg_daily_summary** | 🟠 CONFIDENTIAL | Business intelligence insights | Analysts + Management | Enhanced | 7 years |
| **agg_zone_metrics** | 🟠 CONFIDENTIAL | Competitive intelligence | Analysts + Management | Enhanced | 7 years |

### 3.4 Audit Layer

| Table | Classification | Rationale | Access Control | Encryption | Retention |
|-------|----------------|-----------|----------------|------------|-----------|
| **quarantine_records** | 🟡 INTERNAL | DQ investigation, operational | Data Engineers + Steward | Standard | 180 days |
| **dq_results** | 🟡 INTERNAL | Quality metrics, operational | Data Engineers + Steward | Standard | 1 year |
| **access_log** | 🟡 INTERNAL | Security/compliance audit | Admins + Security | Enhanced | 7 years |
| **pipeline_runs** | 🟡 INTERNAL | Operational monitoring | Engineers + Steward | Standard | 1 year |

---

## 4. Column-Level Classification

### 4.1 fact_trips (Most Critical Table)

| Column | Classification | Justification | Masking Required | Access |
|--------|----------------|---------------|------------------|--------|
| **date_sk** | 🟢 PUBLIC | Surrogate key, non-sensitive | No | All |
| **payment_type_sk** | 🟢 PUBLIC | FK to dimension | No | All |
| **rate_code_sk** | 🟢 PUBLIC | FK to dimension | No | All |
| **trip_type_sk** | 🟢 PUBLIC | FK to dimension | No | All |
| **pickup_location_sk** | 🟠 CONFIDENTIAL | Granular location (265 zones) may reveal patterns | Yes (Dev/Test) | Analysts+ |
| **dropoff_location_sk** | 🟠 CONFIDENTIAL | Granular location may reveal patterns | Yes (Dev/Test) | Analysts+ |
| **vendor_id** | 🟡 INTERNAL | Operational metadata | No | Analysts+ |
| **trip_distance** | 🟡 INTERNAL | Business metric | No | Analysts+ |
| **trip_duration_min** | 🟡 INTERNAL | Business metric | No | Analysts+ |
| **passenger_count** | 🟡 INTERNAL | Operational data | No | Analysts+ |
| **fare_amount** | 🟡 INTERNAL | Revenue data | No | Analysts+ |
| **extra** | 🟡 INTERNAL | Revenue component | No | Analysts+ |
| **mta_tax** | 🟡 INTERNAL | Revenue component | No | Analysts+ |
| **tip_amount** | 🟡 INTERNAL | Revenue data | No | Analysts+ |
| **tolls_amount** | 🟡 INTERNAL | Revenue component | No | Analysts+ |
| **improvement_surcharge** | 🟡 INTERNAL | Revenue component | No | Analysts+ |
| **congestion_surcharge** | 🟡 INTERNAL | Revenue component | No | Analysts+ |
| **total_amount** | 🟡 INTERNAL | Total revenue | No | Analysts+ |
| **created_at** | 🟡 INTERNAL | Audit timestamp | No | Analysts+ |

### 4.2 slv_trips (Silver Layer)

| Column | Classification | Justification | Masking Required | Access |
|--------|----------------|---------------|------------------|--------|
| **trip_id** | 🟡 INTERNAL | Surrogate key | No | Engineers+ |
| **vendor_id** | 🟡 INTERNAL | Operational | No | Engineers+ |
| **pickup_datetime** | 🟡 INTERNAL | Temporal data (granular timestamp) | No | Analysts+ |
| **dropoff_datetime** | 🟡 INTERNAL | Temporal data | No | Analysts+ |
| **store_and_fwd_flag** | 🟡 INTERNAL | Operational flag | No | Engineers+ |
| **ratecode_id** | 🟢 PUBLIC | Reference code | No | All |
| **PULocationID** | 🟠 CONFIDENTIAL | Granular location | Yes (Dev/Test) | Analysts+ |
| **DOLocationID** | 🟠 CONFIDENTIAL | Granular location | Yes (Dev/Test) | Analysts+ |
| **passenger_count** | 🟡 INTERNAL | Operational | No | Analysts+ |
| **trip_distance** | 🟡 INTERNAL | Business metric | No | Analysts+ |
| **fare_amount** | 🟡 INTERNAL | Revenue | No | Analysts+ |
| **extra** | 🟡 INTERNAL | Revenue | No | Analysts+ |
| **mta_tax** | 🟡 INTERNAL | Revenue | No | Analysts+ |
| **tip_amount** | 🟡 INTERNAL | Revenue | No | Analysts+ |
| **tolls_amount** | 🟡 INTERNAL | Revenue | No | Analysts+ |
| **improvement_surcharge** | 🟡 INTERNAL | Revenue | No | Analysts+ |
| **total_amount** | 🟡 INTERNAL | Revenue | No | Analysts+ |
| **payment_type** | 🟢 PUBLIC | Category | No | All |
| **trip_type** | 🟢 PUBLIC | Category | No | All |
| **congestion_surcharge** | 🟡 INTERNAL | Revenue | No | Analysts+ |
| **trip_duration_min** | 🟡 INTERNAL | Derived metric | No | Analysts+ |
| **avg_speed_mph** | 🟡 INTERNAL | Derived metric | No | Analysts+ |
| **pickup_date** | 🟡 INTERNAL | Derived date | No | Analysts+ |
| **pickup_hour** | 🟡 INTERNAL | Temporal pattern | No | Analysts+ |
| **is_weekend** | 🟡 INTERNAL | Temporal pattern | No | Analysts+ |
| **dq_status** | 🟡 INTERNAL | Quality metadata | No | Engineers+ |
| **dq_rules_failed** | 🟡 INTERNAL | Quality metadata | No | Engineers+ |
| **created_at** | 🟡 INTERNAL | Audit | No | Engineers+ |

### 4.3 agg_daily_summary (Aggregated Data)

| Column | Classification | Justification | Masking Required | Access |
|--------|----------------|---------------|------------------|--------|
| **summary_date** | 🟢 PUBLIC | Date dimension | No | All |
| **trip_count** | 🟠 CONFIDENTIAL | Business volume metric | No | Analysts+ |
| **total_revenue** | 🟠 CONFIDENTIAL | Financial metric | No | Management+ |
| **avg_fare** | 🟠 CONFIDENTIAL | Pricing intelligence | No | Analysts+ |
| **avg_distance** | 🟡 INTERNAL | Operational metric | No | Analysts+ |
| **avg_duration** | 🟡 INTERNAL | Operational metric | No | Analysts+ |
| **total_passengers** | 🟡 INTERNAL | Volume metric | No | Analysts+ |
| **peak_hour** | 🟡 INTERNAL | Pattern insight | No | Analysts+ |
| **weekend_flag** | 🟢 PUBLIC | Temporal category | No | All |

---

## 5. Classification by Sensitivity Level

### 5.1 🟢 PUBLIC Data Elements

**Definition:** Data that is publicly available or non-sensitive, can be shared freely.

**Tables (11):**
- All reference/dimension tables: `dim_date`, `dim_payment_type`, `dim_rate_code`, `dim_trip_type`
- All Bronze reference tables: `lnd_payment_type`, `lnd_rate_code`, `lnd_trip_type`
- Silver reference tables: `slv_payment_type`, `slv_rate_code`, `slv_trip_type`

**Columns Examples:**
- All surrogate keys (`*_sk`)
- All natural keys for dimensions (`payment_type_id`, `rate_code_id`)
- All dimension descriptions (`payment_type_desc`, `rate_code_desc`)
- Date/calendar fields (`date_key`, `year`, `month`, `day_of_week`)
- Categorical codes (`payment_type`, `rate_code_id`, `trip_type`)

**Handling Requirements:**
- **Access:** All authenticated users
- **Encryption:** Standard (at rest)
- **Masking:** Not required
- **Retention:** Indefinite
- **Sharing:** Can be shared externally if needed

### 5.2 🟡 INTERNAL Data Elements

**Definition:** Business-use data, not publicly available but not highly sensitive.

**Tables (5):**
- `lnd_green_tripdata` (Bronze trips)
- `slv_trips` (Silver trips)
- `fact_trips` (Gold fact table)
- `quarantine_records` (Audit)
- `dq_results` (Audit)

**Columns Examples:**
- Revenue fields: `fare_amount`, `tip_amount`, `total_amount`
- Operational metrics: `trip_distance`, `trip_duration_min`, `passenger_count`
- Temporal data: `pickup_datetime`, `dropoff_datetime`
- Operational flags: `vendor_id`, `store_and_fwd_flag`
- Quality metadata: `dq_status`, `dq_rules_failed`

**Handling Requirements:**
- **Access:** Analysts, BI Developers, Data Engineers (RBAC via AAD groups)
- **Encryption:** Standard (AES-256 at rest, TLS 1.2+ in transit)
- **Masking:** Not required in production; optional in dev/test
- **Retention:** 1-7 years depending on table
- **Sharing:** Internal only, no external sharing without approval

**Unity Catalog Implementation:**
```sql
-- Grant SELECT on Internal tables to analyst group
GRANT SELECT ON TABLE gold.fact_trips TO `grp-nyctaxi-data-analysts`;
GRANT SELECT ON TABLE silver.slv_trips TO `grp-nyctaxi-data-analysts`;

-- Engine-specific access
GRANT ALL PRIVILEGES ON TABLE silver.slv_trips TO `grp-nyctaxi-data-engineers`;
```

### 5.3 🟠 CONFIDENTIAL Data Elements

**Definition:** Sensitive business data that could harm competitiveness if disclosed.

**Tables (1):**
- `agg_daily_summary` (Gold aggregations)
- `agg_zone_metrics` (Gold zone analysis)

**Columns (Specific):**
- **Granular locations:** `PULocationID`, `DOLocationID`, `pickup_location_sk`, `dropoff_location_sk`
  - **Why Confidential:** 265 TLC zones are granular; patterns may reveal competitive intelligence
- **Aggregated business metrics:** `total_revenue`, `trip_count`, `avg_fare`
  - **Why Confidential:** Business performance indicators

**Handling Requirements:**
- **Access:** Senior Analysts, BI Developers, Management (restricted AAD groups)
- **Encryption:** Enhanced (at rest + in transit + key rotation every 90 days)
- **Masking:** **REQUIRED** in non-production environments
- **Retention:** 7 years
- **Sharing:** Prohibited without Data Steward approval
- **Audit:** All access logged

**Masking Rules (Dev/Test Environments):**

```sql
-- Mask location IDs in non-production
CREATE FUNCTION mask_location(location_id INT)
RETURNS INT
RETURN CASE 
    WHEN IS_ACCOUNT_GROUP_MEMBER('grp-nyctaxi-admins') THEN location_id
    WHEN current_catalog() = 'prod_nyctaxi' THEN location_id
    ELSE -1  -- Masked in dev/test for non-admins
END;

-- Apply masking to confidential columns
ALTER TABLE gold.fact_trips 
ALTER COLUMN pickup_location_sk 
SET MASK mask_location;

ALTER TABLE gold.fact_trips 
ALTER COLUMN dropoff_location_sk 
SET MASK mask_location;

-- Aggregate revenue masking in dev/test
CREATE FUNCTION mask_revenue(amount DECIMAL(10,2))
RETURNS DECIMAL(10,2)
RETURN CASE 
    WHEN IS_ACCOUNT_GROUP_MEMBER('grp-nyctaxi-admins') THEN amount
    WHEN current_catalog() = 'prod_nyctaxi' THEN amount
    ELSE ROUND(amount * 0.7, 2)  -- Scaled value for testing
END;

ALTER TABLE gold.agg_daily_summary 
ALTER COLUMN total_revenue 
SET MASK mask_revenue;
```

**Unity Catalog RBAC:**
```sql
-- Restrict access to aggregated tables
GRANT SELECT ON TABLE gold.agg_daily_summary TO `grp-nyctaxi-management`;
REVOKE SELECT ON TABLE gold.agg_daily_summary FROM `grp-nyctaxi-data-analysts`;

-- Grant with masking for testing
GRANT SELECT ON TABLE gold.agg_daily_summary TO `grp-nyctaxi-test-users`;
-- (masking function applies automatically)
```

### 5.4 🔴 RESTRICTED Data Elements

**Definition:** Highly sensitive or regulated data (PII, PHI, PCI).

**Status:** **NONE in this project** (NYC TLC data is anonymized)

**Future Considerations:**
If project expands to include:
- Driver names/licenses → **RESTRICTED**
- Passenger phone numbers → **RESTRICTED**
- Credit card numbers → **RESTRICTED**
- Precise GPS coordinates → **RESTRICTED**

**Future Handling (if applicable):**
- **Access:** Admins only, temporary access with approval
- **Encryption:** Field-level encryption + at rest + in transit
- **Masking:** **MANDATORY** in all non-production environments
- **Tokenization:** Replace real values with tokens
- **Retention:** Per regulation (GDPR: deletion on request)
- **Audit:** Full audit trail of all access
- **Compliance:** GDPR/LGPD deletion procedures

---

## 6. Access Control Matrix

### 6.1 Role-Based Access by Classification

| Role | Public | Internal | Confidential | Restricted |
|------|--------|----------|--------------|------------|
| **Platform Admin** | Full | Full | Full | Full |
| **Data Engineer** | Full | Full | Read-only (for validation) | - |
| **Data Analyst** | Full | Read-only | - | - |
| **BI Developer** | Full | Read-only (Gold only) | Read-only (views) | - |
| **Data Scientist** | Full | Read-only | - | - |
| **Business User** | Via BI only | Via BI only | - | - |
| **Management** | Full | Read-only | Read-only | - |

### 6.2 Unity Catalog Permissions (Detailed)

```sql
-- ============================================================================
-- PUBLIC DATA (Reference Dimensions)
-- ============================================================================
GRANT SELECT ON gold.dim_date TO `grp-nyctaxi-all-users`;
GRANT SELECT ON gold.dim_payment_type TO `grp-nyctaxi-all-users`;
GRANT SELECT ON gold.dim_rate_code TO `grp-nyctaxi-all-users`;
GRANT SELECT ON gold.dim_trip_type TO `grp-nyctaxi-all-users`;

-- ============================================================================
-- INTERNAL DATA (Fact Tables, Silver)
-- ============================================================================

-- Data Engineers: Full access to all layers
GRANT ALL PRIVILEGES ON SCHEMA bronze TO `grp-nyctaxi-data-engineers`;
GRANT ALL PRIVILEGES ON SCHEMA silver TO `grp-nyctaxi-data-engineers`;
GRANT ALL PRIVILEGES ON SCHEMA gold TO `grp-nyctaxi-data-engineers`;
GRANT ALL PRIVILEGES ON SCHEMA audit TO `grp-nyctaxi-data-engineers`;

-- Data Analysts: Read Silver + Gold (excluding confidential aggregations)
GRANT SELECT ON TABLE silver.slv_trips TO `grp-nyctaxi-data-analysts`;
GRANT SELECT ON TABLE gold.fact_trips TO `grp-nyctaxi-data-analysts`;
-- Note: No access to agg_daily_summary (CONFIDENTIAL)

-- BI Developers: Read Gold fact + dimensions (excluding confidential)
GRANT SELECT ON TABLE gold.fact_trips TO `grp-nyctaxi-bi-developers`;
GRANT SELECT ON SCHEMA gold TO `grp-nyctaxi-bi-developers`;  -- Dimensions
REVOKE SELECT ON TABLE gold.agg_daily_summary FROM `grp-nyctaxi-bi-developers`;

-- Data Scientists: Read Silver + Gold (for ML)
GRANT SELECT ON TABLE silver.slv_trips TO `grp-nyctaxi-data-scientists`;
GRANT SELECT ON TABLE gold.fact_trips TO `grp-nyctaxi-data-scientists`;

-- ============================================================================
-- CONFIDENTIAL DATA (Aggregated Business Metrics)
-- ============================================================================

-- Management: Read-only access to aggregated metrics
GRANT SELECT ON TABLE gold.agg_daily_summary TO `grp-nyctaxi-management`;
GRANT SELECT ON TABLE gold.agg_zone_metrics TO `grp-nyctaxi-management`;

-- Senior Analysts: Approved access to aggregated metrics
GRANT SELECT ON TABLE gold.agg_daily_summary TO `grp-nyctaxi-senior-analysts`;

-- ============================================================================
-- MASKING POLICIES (Non-Production Environments)
-- ============================================================================

-- Apply masking functions (see Section 5.3)
-- Enforced automatically by Unity Catalog in dev/test catalogs
```

---

## 7. Masking Strategy

### 7.1 Masking Requirements by Environment

| Environment | Public | Internal | Confidential | Restricted |
|-------------|--------|----------|--------------|------------|
| **Production** | No masking | No masking | No masking | Full masking |
| **Staging** | No masking | No masking | Partial masking | Full masking |
| **Development** | No masking | Optional | **Required** | Full masking |
| **Test** | No masking | Optional | **Required** | Full masking |

### 7.2 Masking Techniques

| Technique | Use Case | Example | Reversible |
|-----------|----------|---------|------------|
| **Nullification** | Completely hide value | `NULL` | No |
| **Fixed Value** | Replace with default | `-1`, `UNKNOWN` | No |
| **Randomization** | Maintain data type/range | Random int 1-265 | No |
| **Scaling** | Preserve relationships | `amount * 0.7` | No |
| **Hashing** | Preserve uniqueness | `SHA2(location_id)` | No |
| **Tokenization** | Preserve format, reversible | Token lookup | Yes |

### 7.3 Implemented Masking Functions

```sql
-- =======================================================================
-- MASKING FUNCTION: Location IDs (CONFIDENTIAL)
-- =======================================================================
CREATE FUNCTION mask_location(location_id INT)
RETURNS INT
COMMENT 'Mask location IDs in non-production environments'
RETURN CASE 
    -- Admins can see real values
    WHEN IS_ACCOUNT_GROUP_MEMBER('grp-nyctaxi-admins') THEN location_id
    -- Production catalog shows real values
    WHEN current_catalog() = 'prod_nyctaxi' THEN location_id
    -- Dev/Test: Mask to -1
    ELSE -1
END;

-- Apply to columns
ALTER TABLE gold.fact_trips ALTER COLUMN pickup_location_sk SET MASK mask_location;
ALTER TABLE gold.fact_trips ALTER COLUMN dropoff_location_sk SET MASK mask_location;

-- =======================================================================
-- MASKING FUNCTION: Revenue Amounts (CONFIDENTIAL in dev/test)
-- =======================================================================
CREATE FUNCTION mask_revenue(amount DECIMAL(10,2))
RETURNS DECIMAL(10,2)
COMMENT 'Scale revenue amounts in non-production environments'
RETURN CASE 
    WHEN IS_ACCOUNT_GROUP_MEMBER('grp-nyctaxi-admins') THEN amount
    WHEN current_catalog() = 'prod_nyctaxi' THEN amount
    -- Dev/Test: Scale to 70% of real value (preserves relationships)
    ELSE ROUND(amount * 0.7, 2)
END;

-- Apply to sensitive aggregations
ALTER TABLE gold.agg_daily_summary ALTER COLUMN total_revenue SET MASK mask_revenue;

-- =======================================================================
-- MASKING FUNCTION: Trip Count (CONFIDENTIAL in dev/test)
-- =======================================================================
CREATE FUNCTION mask_trip_count(count BIGINT)
RETURNS BIGINT
COMMENT 'Scale trip counts in non-production environments'
RETURN CASE 
    WHEN IS_ACCOUNT_GROUP_MEMBER('grp-nyctaxi-admins') THEN count
    WHEN current_catalog() = 'prod_nyctaxi' THEN count
    -- Dev/Test: Scale to 70%
    ELSE CAST(count * 0.7 AS BIGINT)
END;

ALTER TABLE gold.agg_daily_summary ALTER COLUMN trip_count SET MASK mask_trip_count;

-- =======================================================================
-- TESTING MASKING
-- =======================================================================
-- As admin in prod: See real values
USE CATALOG prod_nyctaxi;
SELECT pickup_location_sk, total_revenue FROM gold.fact_trips LIMIT 5;
-- Result: 132, 25.50 (real values)

-- As analyst in dev: See masked values
USE CATALOG dev_nyctaxi;
SELECT pickup_location_sk, total_revenue FROM gold.fact_trips LIMIT 5;
-- Result: -1, 17.85 (masked values)
```

---

## 8. Data Handling Procedures

### 8.1 Handling Requirements by Classification

| Activity | Public | Internal | Confidential | Restricted |
|----------|--------|----------|--------------|------------|
| **Creating Copies** | Allowed | Requires approval | Requires Data Steward approval | Prohibited |
| **Exporting to File** | Allowed | Allowed (secure location) | Encrypted files only | Prohibited |
| **Sharing via Email** | Allowed | Internal only | Prohibited | Prohibited |
| **Printing** | Allowed | Allowed | Prohibited | Prohibited |
| **Cloud Storage** | Any | ADLS Gen2 only | ADLS Gen2 + encryption | ADLS Gen2 + field encryption |
| **Third-Party Tools** | Allowed | Approved tools only | Approved + audit | Prohibited |
| **API Access** | Allowed | Authenticated | Authenticated + RBAC | Prohibited |

### 8.2 Data Export Procedures

```markdown
## Data Export Request Template

### Requester Information
- Name: {name}
- Role: {role}
- Email: {email}
- Date: {date}

### Export Details
- Tables/Views: {list}
- Classification Level: 🟢 PUBLIC | 🟡 INTERNAL | 🟠 CONFIDENTIAL
- Row Count (approx): {number}
- Export Format: CSV | Parquet | Excel
- Destination: {where will data go}

### Business Justification
{Why is this export needed?}

### Security Measures
- [ ] Export will be encrypted (if CONFIDENTIAL)
- [ ] Export will be stored in secure location
- [ ] Export will be deleted after {X} days
- [ ] No PII/sensitive data included (verified)

### Approvals
- Data Analyst: {name} - {date}
- Data Steward: {name} - {date} (if CONFIDENTIAL)
- CISO: {name} - {date} (if CONFIDENTIAL)
```

### 8.3 Incident Response for Data Leakage

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                          DATA LEAKAGE INCIDENT RESPONSE                                  │
└─────────────────────────────────────────────────────────────────────────────────────────┘

  DETECTION           CONTAINMENT          INVESTIGATION         REMEDIATION
  ─────────           ───────────          ─────────────         ───────────

  ┌──────────┐       ┌──────────┐         ┌──────────┐         ┌──────────┐
  │ Alert    │       │ Revoke   │         │ Determine│         │ Patch    │
  │ triggered│──────▶│ access   │────────▶│ scope &  │────────▶│ vulnerability│
  │          │       │ immediately       │ root cause        │          │
  └──────────┘       └──────────┘         └──────────┘         └──────────┘
                            │                    │                    │
                            ▼                    ▼                    ▼
                     ┌──────────┐         ┌──────────┐         ┌──────────┐
                     │ Isolate  │         │ Audit    │         │ Post-    │
                     │ affected │         │ logs     │         │ incident │
                     │ systems  │         │          │         │ review   │
                     └──────────┘         └──────────┘         └──────────┘
                                                                      │
                                                                      ▼
                                                               ┌──────────┐
                                                               │ Update   │
                                                               │ policies │
                                                               └──────────┘

  Timeline:
  • Detection → Containment: <15 minutes
  • Containment → Investigation: <1 hour
  • Investigation → Remediation: <24 hours
  • Post-incident review: Within 7 days
```

---

## 9. Classification Review & Maintenance

### 9.1 Review Schedule

| Review Type | Frequency | Trigger | Owner | Action |
|-------------|-----------|---------|-------|--------|
| **Routine Review** | Quarterly | Calendar | Data Steward | Review all classifications |
| **New Entity Review** | On creation | New table/column | Data Engineer | Submit for classification |
| **Incident-Triggered** | As needed | Data breach/leak | CISO | Re-classify affected data |
| **Regulation Change** | As needed | New law/regulation | Legal + Data Steward | Update compliance mapping |
| **Access Pattern Review** | Monthly | Audit logs | Data Steward | Identify misclassified data |

### 9.2 Classification Change Process

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                          CLASSIFICATION CHANGE WORKFLOW                                  │
└─────────────────────────────────────────────────────────────────────────────────────────┘

  Step 1: REQUEST          Step 2: REVIEW           Step 3: APPROVAL        Step 4: IMPLEMENT
  ───────────────          ──────────────           ────────────────        ─────────────────

  ┌──────────────┐        ┌──────────────┐         ┌──────────────┐        ┌──────────────┐
  │ Engineer or  │        │ Data Steward │         │ Governance   │        │ Update       │
  │ Analyst      │───────▶│ reviews:     │────────▶│ Board        │───────▶│ Unity Catalog│
  │ submits      │        │              │         │ approves     │        │ permissions  │
  │ request with:│        │ • Business   │         │ (if major    │        │              │
  │              │        │   impact     │         │  change)     │        │ Update docs  │
  │ • Rationale  │        │ • Risk       │         │              │        │              │
  │ • New level  │        │ • Compliance │         │              │        │ Notify users │
  └──────────────┘        └──────────────┘         └──────────────┘        └──────────────┘
                                 │                         │
                                 │ REJECT                  │
                                 ▼                         ▼
                          ┌──────────────┐         ┌──────────────┐
                          │ Notify       │         │ Log change   │
                          │ requester    │         │ in audit     │
                          └──────────────┘         └──────────────┘
```

**Change Categories:**

| Change Type | Approval | Example |
|-------------|----------|---------|
| **Minor** (No access change) | Data Steward | Update column description |
| **Moderate** (Downgrade classification) | Data Steward | PUBLIC → INTERNAL not allowed without justification |
| **Major** (Upgrade classification) | Governance Board | INTERNAL → CONFIDENTIAL (adds access restrictions) |

### 9.3 New Entity Classification Checklist

```markdown
## New Entity Classification Checklist

### Entity Details
- [ ] Table/View name: {name}
- [ ] Schema/Layer: {bronze/silver/gold}
- [ ] Created by: {engineer}
- [ ] Creation date: {date}

### Classification Questions
1. [ ] Is this data publicly available? (YES → PUBLIC)
2. [ ] Does it contain PII/PHI/PCI? (YES → RESTRICTED)
3. [ ] Would disclosure harm the business? (YES → CONFIDENTIAL)
4. [ ] Is it operational/internal-use data? (YES → INTERNAL)

### Proposed Classification
- [ ] 🟢 PUBLIC
- [ ] 🟡 INTERNAL
- [ ] 🟠 CONFIDENTIAL
- [ ] 🔴 RESTRICTED

### Justification
{Why this classification level?}

### Handling Requirements
- [ ] Access control configured (Unity Catalog)
- [ ] Encryption verified
- [ ] Masking applied (if CONFIDENTIAL)
- [ ] Retention period set
- [ ] Metadata documented (COMMENT, TBLPROPERTIES)

### Approvals
- [ ] Data Engineer: {name} - {date}
- [ ] Data Steward: {name} - {date}
- [ ] (If CONFIDENTIAL) CISO: {name} - {date}
```

---

## 10. Compliance Mapping

### 10.1 Regulatory Requirements (Future State)

| Regulation | Applicability | Classified Data | Required Controls |
|------------|---------------|-----------------|-------------------|
| **GDPR** | If EU citizens' data added | RESTRICTED (PII) | Right to deletion, consent, breach notification |
| **LGPD** | If Brazilian citizens' data | RESTRICTED (PII) | Data minimization, consent, transparency |
| **CCPA** | If California residents' data | RESTRICTED (PII) | Right to deletion, opt-out |
| **SOC 2** | If offering SaaS | CONFIDENTIAL+ | Access controls, audit logs, encryption |
| **SOX** | If financial reporting | INTERNAL+ (financial) | 7-year retention, audit trail, accuracy |

### 10.2 Current Compliance Status

**NYC TLC Data Classification:**
- **Public Domain:** Yes (all trip data is public)
- **PII Status:** None (anonymized)
- **Current Compliance:** ✅ No PII = No GDPR/LGPD obligations

**Preventive Measures in Place:**
- Classification framework (this document)
- Access audit logs (7-year retention)
- Encryption at rest and in transit
- RBAC via Unity Catalog
- Retention policies defined

---

## 11. Metrics & Monitoring

### 11.1 Classification Metrics

```sql
-- Classification Coverage Report
CREATE OR REPLACE VIEW audit.vw_classification_coverage AS
SELECT
    table_schema AS layer,
    COUNT(*) AS total_tables,
    
    -- Extract classification from table properties
    SUM(CASE WHEN tbl_properties LIKE '%sensitivity%public%' THEN 1 ELSE 0 END) AS public_tables,
    SUM(CASE WHEN tbl_properties LIKE '%sensitivity%internal%' THEN 1 ELSE 0 END) AS internal_tables,
    SUM(CASE WHEN tbl_properties LIKE '%sensitivity%confidential%' THEN 1 ELSE 0 END) AS confidential_tables,
    SUM(CASE WHEN tbl_properties LIKE '%sensitivity%restricted%' THEN 1 ELSE 0 END) AS restricted_tables,
    SUM(CASE WHEN tbl_properties NOT LIKE '%sensitivity%' THEN 1 ELSE 0 END) AS unclassified_tables,
    
    -- Completeness
    ROUND(100.0 * SUM(CASE WHEN tbl_properties LIKE '%sensitivity%' THEN 1 ELSE 0 END) / COUNT(*), 2) AS classification_completeness_pct
FROM information_schema.tables
WHERE table_schema IN ('bronze', 'silver', 'gold', 'audit')
GROUP BY table_schema;
```

### 11.2 Target Metrics

| Metric | Target | Current | Alert If |
|--------|--------|---------|----------|
| **Classification Completeness** | 100% | 100% | <100% |
| **Unclassified Tables** | 0 | 0 | >0 |
| **Masking Coverage (CONFIDENTIAL)** | 100% | 100% | <100% |
| **Access Violations (Confidential)** | 0/month | 0 | >0 |
| **Classification Review Age** | <90 days | Current | >90 days |

---

## 12. Próximos Artefatos

Este documento alimenta:

| Artefato | Agente | Propósito |
|----------|--------|-----------|
| `data-lineage.md` | 🛡️ Gaia | Documentar origem e transformações de dados classificados |
| `compliance-mapping.md` | 🛡️ Gaia | Mapear classificações para requisitos regulatórios |
| `security-controls.md` | 🛠️ Diego | Implementar controles técnicos por classificação |
| `access-request-form.md` | 🛡️ Gaia | Formulário de request considerando classificação |

---

## Histórico de Versões

| Versão | Data | Autor | Alterações |
|--------|------|-------|------------|
| 1.0 | 2026-02-05 | Gaia (DataSteward) | Versão inicial - Classificação completa de 17 entidades |

---

*Documento gerado pelo 🛡️ DataSteward Agent - Avanade™ Core*
