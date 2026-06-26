# SDD: logic-extractor (Extract Business Logic)

**Role:** Deep-analyze legacy code. Extract and catalog transformation logic.

---

## Input Contract

```
Required:
  ├─ legacy_folder: Path — SQL/DAG/config files
  ├─ discovery_inventory.json: File — object types
  └─ max_complexity: Int — code lines to analyze (default: unlimited)
```

---

## Task Definition

1. **Parse** legacy code (SQL, Python, XML, DAG definitions)
2. **Extract** transformation logic:
   - JOINs and filters
   - Aggregations and calculations
   - Error handling
3. **Identify** dependencies (table → table)
4. **Catalog** every rule with source code reference
5. **Flag** complex/ambiguous logic with ⚠️

---

## Success Criteria

- ✅ 100% of legacy code files parsed (no skipped files)
- ✅ Every extracted rule cites its source file + line number
- ✅ Ambiguous/complex logic flagged with ⚠️ (not guessed)

---

## Output Contract

```
Produces:
  ├─ logic-catalog.json: {source, logic, complexity, references}
  └─ dependency-graph.json: {object_a → object_b via rule}

Passes To: business-analyst (for STTM mapping)
```

---

## Constraints

🔴 100% extraction (no partial analysis)  
🔴 Must cite source code line numbers  
🔴 Flag anything ambiguous  

---

**Status:** ✅ ACTIVE | **Updated:** 2026-06-16