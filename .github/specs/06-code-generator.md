# SDD: code-generator (Generate DDL + ETL)

**Role:** Generate production-ready DDL and ETL code. From logical model → executable.

---

## Input Contract

```
Required:
  ├─ data-model.md: File — from data-modeler
  ├─ STTM.xlsx: File — from business-analyst
  ├─ target_platform: String — Fabric|Databricks|Synapse
  └─ code_style: Dict — naming_convention, formatting_rules

Optional:
  └─ performance_hints: Dict — partitioning, indexing strategy
```

---

## Task Definition

1. **Generate** DDL scripts (CREATE TABLE, partitions, constraints)
2. **Generate** ETL transformations (SQL, PySpark, or equivalent)
3. **Validate** generated code against data contracts
4. **Test** with sample data (if available)
5. **Package** for deployment

---

## Success Criteria

- ✅ DDL passes syntax validation
- ✅ ETL logic matches business rules (100% mapped from STTM)
- ✅ Code is idiomatic for target platform
- ✅ Test sample produces expected output

---

## Output

```
Produces:
  ├─ ddl-bronze.sql: Raw data layer
  ├─ ddl-silver.sql: Cleansed data layer
  ├─ ddl-gold.sql: Business-ready layer
  ├─ etl-bronze.py: Ingestion pipeline
  ├─ etl-silver.py: Transformation pipeline
  ├─ etl-gold.py: Aggregation pipeline
  └─ test-results.json: Sample data validation

Location: projects/[project]/outputs/code/
Passes To: downstream-executor
```

---

## Constraints

🔴 NO HALLUCINATED transformations  
🔴 ALL code must be from STTM mapping  
🔴 Code must be idiomatic for target platform  
🔴 Must pass syntax validation before output

---

**Status:** ✅ ACTIVE | **Updated:** 2026-06-16