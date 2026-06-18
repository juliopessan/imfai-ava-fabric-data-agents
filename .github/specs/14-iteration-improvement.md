# SDD: iteration-improvement (Continuous Optimization)

**Role:** Analyze deployed wave. Identify performance & cost opportunities.

---

## Input Contract

```
Required:
  ├─ deployment-log.txt: File — execution history
  ├─ monitoring-metrics.json: File — runtime KPIs
  ├─ cost-analysis.json: File — spend by layer
  └─ performance_baseline.json: File — target vs actual
```

---

## Task Definition

1. **Analyze** deployment performance (latency, throughput, resource usage)
2. **Identify** optimization opportunities:
   - Unused indexes
   - Over-partitioning
   - Inefficient joins
   - Cost waste
3. **Score** each opportunity (effort vs. impact)
4. **Propose** prioritized list for next iteration

---

## Output

```
Produces:
  ├─ optimization-opportunities.md: Ranked list with ROI
  └─ next-iteration-plan.md: Specific actions

Passes To: migration-coordinator (for Phase 6+ planning)
```

---

**Status:** ✅ ACTIVE | **Updated:** 2026-06-16