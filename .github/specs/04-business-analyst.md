# SDD: business-analyst (Extract Business Logic)

**Role:** Map legacy business logic to target model. Create STTM (Source-to-Target Mapping).

---

## Input Contract

```
Required:
  ├─ discovery_inventory.json: File — from discovery-scout
  ├─ legacy_source_code: Path — SQL/DAG/config files
  ├─ transformation_rules: Dict — custom business rules
  └─ business_glossary: File — term definitions

Optional:
  └─ assumptions_log: File — known unknowns
```

---

## Task Definition

1. **Extract** business logic from legacy code (SQL joins, calculations, aggregations)
2. **Catalog** every transformation rule
3. **Build** STTM matrix (Legacy object → Target object, Transformation logic, DQ rules)
4. **Identify** data quality requirements
5. **Flag** ambiguous logic with ⚠️ NEEDS_CLARIFICATION

---

## Success Criteria

- ✅ STTM 100% complete
- ✅ All transformations documented
- ✅ No ambiguous mappings
- ✅ Stakeholder review approval

---

## Output Contract

```
Produces:
  ├─ STTM.xlsx: Source-to-Target mapping
  ├─ business-rules.md: Transformation logic
  ├─ data-quality-rules.json: Validation rules
  └─ assumptions.md: Known unknowns

Location: projects/[project]/outputs/sttm/
Passes To: data-modeler
```

---

## Constraints

🔴 NO REWRITING business logic  
🔴 Only EXTRACT and MAP  
🔴 Flag ambiguities (don't guess)  
🔴 STTM must be 100% traceable (legacy → target)

---

**Status:** ✅ ACTIVE | **Updated:** 2026-06-16
