# SDD: inventory-scout (Fallback Discovery)

**Role:** Backup discovery if discovery-scout unavailable. Same output, direct scanning.

---

## Input Contract

```
Required:
  ├─ legacy_folder: Path — direct file system path
  └─ platform_type: String — Cloudera|SAP|PowerCenter|Other

Optional:
  └─ discovery_inventory.json: File — partial/previous inventory
```

---

## Task Definition

1. **Scan** legacy folder for all files
2. **Categorize** by type (SQL, DAG, config, etc.)
3. **Extract** objects (same as discovery-scout)
4. **Merge** with existing inventory if provided
5. **Output** same format as discovery-scout

---

## Success Criteria

- ✅ 100% of legacy folder scanned (no skipped files)
- ✅ Output format matches discovery-scout exactly (drop-in replacement)
- ✅ Merge with existing partial inventory loses no previously-discovered objects

---

## Output Contract

```
Produces:
  ├─ DISCOVERY_INVENTORY.json: Same as discovery-scout
  └─ discovery_summary.md: Same as discovery-scout

Passes To: business-analyst (same as discovery-scout)
```

---

## Constraints

🔴 NO GUESSING object definitions — same hard rule as discovery-scout
🔴 Must produce output in the exact same schema as discovery-scout (consumers can't tell which agent ran)
🟡 Use only if discovery-scout is unavailable

---

**Status:** ✅ ACTIVE | **Updated:** 2026-06-16