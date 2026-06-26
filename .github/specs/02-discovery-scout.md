# SDD: discovery-scout (Legacy Analysis)

**Role:** Extract inventory from legacy systems. No assumptions.

---

## Input Contract

```
Required:
  ├─ legacy_folder: Path — projects/[project]/legacy/
  ├─ platform_type: String — Cloudera|Airflow|SAP|PowerCenter|Snowflake|Other
  ├─ wave_config: File — projects/[project]/wave-config.yaml
  └─ discovery_owner: String — from wave_config

Reject If:
  ├─ legacy_folder doesn't exist
  ├─ platform_type not recognized
  └─ wave_config invalid YAML
```

---

## Task Definition

1. **Scan** legacy_folder for all source files
2. **Extract** DDL/configuration using patterns (regex/parsing)
3. **Catalog** every object:
   - Type (TABLE, VIEW, PROCEDURE, FUNCTION, INDEX, etc.)
   - Name
   - Schema/database
   - Dependencies (if detectable)
4. **Flag unknowns** with ⚠️ INCOMPLETE
5. **Output** structured inventory

---

## Success Criteria

- ✅ 100% of legacy files scanned
- ✅ Object count >= expected (from config)
- ✅ All objects categorized
- ✅ Unknowns flagged (not guessed)

---

## Output Contract

```
Produces:
  ├─ DISCOVERY_INVENTORY.json: {objects: [{type, name, schema, ...}], count}
  ├─ discovery_summary.md: Human-readable report
  └─ discovery_metrics.json: {total_objects, by_type, quality_score}

Location: projects/[project]/outputs/
Passes To: business-analyst
```

---

## Constraints

🔴 NO GUESSING object definitions  
🔴 NO INFERRING missing data  
🔴 Flag partial extractions with ⚠️  
🔴 Quality score must be >= 0.80 or flag as INCOMPLETE

---

**Status:** ✅ ACTIVE | **Updated:** 2026-06-16