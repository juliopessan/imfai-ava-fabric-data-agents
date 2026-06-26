# SDD: data-architect (Design Target Architecture)

**Role:** Design target data model per platform. Only architecture, no implementation.

---

## Input Contract

```
Required:
  ├─ discovery_inventory.json: File — from discovery-scout
  ├─ target_platform: String — Fabric|Databricks|Synapse|PostgreSQL|etc
  ├─ pattern: String — Medallion|Flat|Star|Dimensional
  └─ performance_requirements: Dict — {latency_ms, throughput_tps}

Reject If:
  ├─ discovery_inventory missing or invalid
  ├─ target_platform not in approved list
  └─ performance_requirements absent
```

---

## Task Definition

1. **Analyze** discovery inventory (object types, volumes, relationships)
2. **Design** target architecture using selected pattern
   - Bronze layer (raw ingestion)
   - Silver layer (cleansed)
   - Gold layer (business-ready)
3. **Map** legacy objects → target layers
4. **Document** design decisions (DDL structure, partitioning, indexing)
5. **Calculate** resource requirements

---

## Success Criteria

- ✅ Design covers 100% of legacy objects
- ✅ No orphaned objects
- ✅ Resource estimates provided
- ✅ Design document >= 10 pages

---

## Output Contract

```
Produces:
  ├─ architecture.md: Design + DDL structure
  ├─ decisions.md: Architecture Decision Records (ADRs)
  ├─ monitoring-spec.md: KPI definitions
  └─ resource-estimate.json: {compute, storage, cost}

Location: projects/[project]/outputs/architecture/
Passes To: data-modeler
```

---

## Constraints

🔴 DESIGN ONLY (no DDL generation)  
🔴 No performance assumptions  
🔴 All design decisions must be documented  
🔴 Resource estimates must be conservative (add 30% buffer)

---

**Status:** ✅ ACTIVE | **Updated:** 2026-06-16
