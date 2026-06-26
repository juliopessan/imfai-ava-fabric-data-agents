# SDD: data-modeler (Define Logical Data Model)

**Role:** Produce logical data model + data contracts. Foundation for DDL.

---

## Input Contract

```
Required:
  ├─ architecture.md: File — from data-architect
  ├─ STTM.xlsx: File — from business-analyst
  ├─ discovery_inventory.json: File — from discovery-scout
  └─ naming_conventions: Dict — table/column/index patterns

Optional:
  └─ performance_hints: Dict — partitioning, clustering keys
```

---

## Task Definition

1. **Create** logical data model (tables, columns, types, constraints)
2. **Define** data contracts (SLA, freshness, accuracy, completeness)
3. **Generate** metrics catalog (KPIs to track)
4. **Document** column lineage (legacy → target)
5. **Validate** model against STTM

---

## Success Criteria

- ✅ Logical model 100% defined
- ✅ All columns traced to legacy source
- ✅ Data contracts measurable
- ✅ No orphaned columns

---

## Output Contract

```
Produces:
  ├─ data-model.md: Logical model documentation
  ├─ data-contracts.json: {table, SLA, freshness, quality}
  ├─ metrics-catalog.json: {metric_name, definition, SLA}
  └─ column-lineage.json: {target_col → source_col path}

Location: projects/[project]/outputs/model/
Passes To: code-generator
```

---

## Constraints

🔴 LOGICAL model only (no DDL)  
🔴 All metrics must be measurable  
🔴 Lineage must be 100% traceable  
🔴 No implied columns (only documented)

---

**Status:** ✅ ACTIVE | **Updated:** 2026-06-16