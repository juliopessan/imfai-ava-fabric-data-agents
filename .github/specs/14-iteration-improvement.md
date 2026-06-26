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

## Success Criteria

- ✅ Every optimization opportunity is scored (effort vs. impact)
- ✅ Opportunities ranked, not just listed
- ✅ Next-iteration plan ties back to specific, named opportunities

---

## Output Contract

```
Produces:
  ├─ optimization-opportunities.md: Ranked list with ROI
  └─ next-iteration-plan.md: Specific actions

Passes To: migration-coordinator (for Phase 6+ planning)
```

---

## Constraints

🔴 NO GUESSING cost/performance numbers — derive from monitoring-metrics.json and cost-analysis.json only
🔴 Every opportunity must show effort vs. impact scoring, not just a recommendation
🟡 If baseline data is missing or incomplete, flag it instead of estimating

---

**Status:** ✅ ACTIVE | **Updated:** 2026-06-16