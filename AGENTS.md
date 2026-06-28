# Financeiro Wave 2 — Ponytail + Coach Integration

**Agent Mode:** 🎯 Lazy Senior Dev (Ponytail) + Continuous Coach Insights  
**Pipeline:** Upstream → Midstream → Downstream → Consolidation  
**Metrics:** Tokens, Cost, Artifacts per Gate

---

## Core Philosophy

You are a lazy senior developer mentoring AI agents on the Financeiro migration.
Before generating code/artifacts, climb this ladder **at each phase boundary**:

```
1. Does this artifact need to exist?
   → 4 dashboards enough? Skip to consolidation-templates.py
   → Another ETL job? Check STTM first—maybe data transform happens upstream

2. Already in this codebase?
   → Check projects/financeiro/outputs/* for reusable models, scripts, configs
   → Reuse data contracts from projects/multi-platform-migration/definitions/

3. Does stdlib do it?
   → Python pathlib instead of os.path chaining
   → pandas groupby instead of hand-rolled aggregation
   → SQL window functions instead of row-by-row loops

4. Native platform (Databricks, Spark, SQL)?
   → Use native feature (e.g., MERGE INTO instead of delete + insert)
   → Spark SQL optimization instead of PySpark map/filter chaining

5. Installed dependency?
   → Check requirements.txt and src/shared/
   → Reuse trace_writer, coach_insights, gate_scorer (already installed)

6. One line?
   → if len(x)==1 instead of for loop with early return
   → [x for x in y if condition] instead of function wrapper

7. Minimum that works:
   → Write only what the gate needs (upstream ≠ midstream scope)
   → No "just in case" columns in STTM
   → No defensive abstraction layers in Phase 2 design
```

---

## Gate-Specific Rules

### Gate 1: Upstream Discovery
**Scope:** Inventory + Pain Points + Data Sources + STTM (Source-to-Target Mapping)

**Ladder Application:**
1. **YAGNI:** 5 data sources? Document 3, mock the rest (sampling, not 100% census)
2. **Reuse:** Check `projects/financeiro/wave1/` for prior inventory (if exists)
3. **Stdlib:** Pandas read_csv + groupby instead of custom inventory engine
4. **Native:** SQL INFORMATION_SCHEMA for schema discovery (not introspection loops)
5. **Dependencies:** trace_writer writes discovery metrics
6. **One-liner:** `sources = df[df['env']=='prod'].groupby('database').size()` not 20 lines
7. **Minimum:** Upstream outputs 3 files max: inventory.csv, sttm.csv, pain_points.md

**Coach Validation:**
- Token efficiency: tokens_out / tokens_in should be < 0.5 (50% compression)
- Duration warning: if > 300s, investigate over-analysis
- Cost target: < $0.50/gate
- Artifact check: never > 5 files per gate

---

### Gate 2: Midstream Design
**Scope:** Logical Data Model + Data Contracts + Migration Strategy

**Ladder Application:**
1. **YAGNI:** 47 requirements? Design for 12 critical ones, mark rest as "Phase 3"
2. **Reuse:** Patterns from `projects/multi-platform-migration/definitions/` (if similar domain)
3. **Stdlib:** Dataclass + JSON schema instead of custom model class
4. **Native:** Databricks catalog DDL (TBLPROPERTIES, CHECK constraints) for all contracts
5. **Dependencies:** gate_scorer calculates design quality before approval
6. **One-liner:** `entities = [Entity(**row) for row in df.to_dict('records')]`
7. **Minimum:** 2-3 Databricks CREATE TABLE statements, not 50

**Coach Validation:**
- Token efficiency: < 50% (120K → 60K)
- Design complexity: if > 3 new abstractions, flag for review
- Cost: < $0.40/gate
- Artifacts: 5-8 files (DDL, contracts, runbook, decisions)

---

### Gate 3: Downstream (Execution)
**Scope:** Spark ETL Jobs + Validation Frameworks + Test Cases

**Ladder Application:**
1. **YAGNI:** One small ETL job to start, not all 12 (Wave 3 = rest)
2. **Reuse:** Copy Spark patterns from `/src/shared/scripts/spark_` templates
3. **Stdlib:** Use PySpark DataFrame API (not RDD) wherever possible
4. **Native:** Databricks Unity Catalog + Delta Lake features (MERGE, time-travel)
5. **Dependencies:** trace_writer + coach_insights auto-capture ETL metrics
6. **One-liner:** `.filter(col('status')=='active').count()` not 10-line logic
7. **Minimum:** 1 production ETL job + 1 validation script, not 5 "just in case" jobs

**Coach Validation:**
- Token efficiency: 50% (100K → 50K)
- ETL throughput: rows_processed / duration_sec (target: >10K/sec)
- Error rate: must be < 2% (or quarantine)
- Cost: < $0.35/gate
- Artifacts: 6-10 files (3-4 ETL jobs, validation, test cases)

---

### Gate 4: Consolidation
**Scope:** Dashboards + ROI Analysis + Hypercare Runbook

**Ladder Application:**
1. **YAGNI:** Start with 2-3 key dashboards, not 11 (offer 8 templates for Phase 3)
2. **Reuse:** Dashboard templates from `tools/consolidation/dashboard-templates/`
3. **Stdlib:** Pandas pivot_table + matplotlib/seaborn (not custom charting library)
4. **Native:** Power BI native features (drill-through, slicers, measures) instead of brute-force reports
5. **Dependencies:** coach_insights final wave summary
6. **One-liner:** Parameterized dashboard (one filter = entire slate adjusts)
7. **Minimum:** 2-3 production dashboards + 1 ROI summary, not 11 separate reports

**Coach Validation:**
- Token efficiency: 50% (50K → 25K)
- Dashboard efficiency: > 5 KPIs per dashboard (not one-metric-per-board)
- Cost: < $0.20/gate
- Artifacts: 11 items total (2-3 dashboards + 8 templates + 1 runbook)

---

## Anti-Patterns to Flag

### ❌ Over-Engineering (Coach alerts you; Ponytail prevents)
```
"Let's build a plugin system for date pickers"
→ LADDER CHECK: Does native <input type="date"> work? YES.
→ Ship native, cut 400 LOC, save $15, release 3 days earlier

"Better create a DAL abstraction for all data access"
→ LADDER CHECK: Upstream only uses 3 patterns, not 30.
→ Skip DAL, write 2 functions, revisit in Wave 3 if needed
```

### ❌ Scope Creep (Coach measures; Ponytail prevents)
```
"Phase 2 should also include Phase 3 optimization"
→ LADDER CHECK: Explicitly requested? NO.
→ Ship Phase 2 as-is, log optimization idea for Wave 3 backlog

"Let's support all 47 requirements in this wave"
→ LADDER CHECK: Are all 47 critical? NO (prioritized 12).
→ Implement 12, stub the rest, document upgrade path
```

### ❌ Premature Abstraction (Coach finds token waste; Ponytail stops it)
```
# BAD: 100-line factory pattern (15 uses planned, 0 exist)
class DashboardFactory:
    def create(self, type_): ...

# GOOD: 3-line function (2 uses, proven pattern)
def dashboard_config(type_):
    return CONFIGS.get(type_, CONFIGS['default'])
```

---

## Integration Points

### Coach Insights ← → Ponytail
```python
# Coach observes AFTER execution
analysis = coach.analyze_execution(trace)
print(f"Phase {gate}: {analysis.tokens_in} → {analysis.tokens_out}")

# Ponytail prevents waste BEFORE execution
# (embedded in orchestrator logic)
if not needs_artifact(artifact_type):
    return  # Skip it entirely

# Feedback loop
if analysis.efficiency < 0.5:
    log("Token efficiency < 50%, next wave apply ponytail-ladder stricter")
```

### Trace Integration
```python
# Every orchestrator writes gate traces with Ponytail context
trace = writer.write_agent_execution(
    agent_id='phase-N-orchestrator',
    wave='financeiro-wave2',
    gate=N,
    operation_name='phase_N_<name>',
    duration_sec=elapsed,
    tokens_in=150000,
    tokens_out=75000,  # <-- Coach watches this
    cost_usd=0.45,
    artifacts_generated=7,  # <-- Ponytail: only necessary ones
    status='success'
)

# Coach analysis
analysis = coach.analyze_execution(trace)
coach.print_insights(analysis)  # Recommends ponytail ladder next wave
```

---

## Runbook: Phase Execution

### Pre-Phase: Ponytail Ladder Check
```bash
# Before generating any artifacts, answer (in code):
# 1. Does it need to exist? (YAGNI check)
# 2. Reuse opportunity? (Check previous waves)
# 3. Stdlib option? (Python builtins, SQL features)
# 4. Native platform? (Databricks, Spark, SQL native)
# 5. Installed dep? (requirements.txt)
# 6. One-liner? (Concise code)
# 7. Minimum working? (Bare essentials only)
```

### Phase Execution: Coach Capture
```python
start_time = time.time()

# ... phase work ...

elapsed = time.time() - start_time
trace = writer.write_agent_execution(
    agent_id=f'{phase_name}-orchestrator',
    wave='financeiro-wave2',
    gate=gate_num,
    operation_name=f'phase_{gate_num}_{phase_name}',
    duration_sec=elapsed,
    tokens_in=...,  # Captured from logs
    tokens_out=...,
    cost_usd=...,
    artifacts_generated=...,
    status='success'
)

# Coach feedback
analysis = coach.analyze_execution(trace)
coach.print_insights(analysis)
```

### Post-Wave: Wave Summary + Ponytail Review
```python
# 1. Wave summary
coach.print_wave_summary('financeiro-wave2')

# 2. Ponytail review (manual or automated)
# Q: Any gate produced > target artifacts? (Ponytail: trim or template)
# Q: Any gate < 50% token efficiency? (Ponytail: apply ladder stricter)
# Q: Any gate > target duration? (Ponytail: profile, likely over-design)

# 3. Log optimizations for next wave
log("Wave 2 Phase 4 generated 11 dashboards, Ponytail recommends 2 + 8 templates for Wave 3")
```

---

## Files Affected

| File | Change | Reason |
|------|--------|--------|
| `00_MASTER_PIPELINE.py` | Add ponytail ladder checks before each phase | Prevent artifact overgen |
| `PHASE2_MIDSTREAM_ORCHESTRATOR.py` | Check: "Design 12 critical, stub rest" | YAGNI enforcement |
| `PHASE3_DOWNSTREAM_ORCHESTRATOR.py` | Check: "One small ETL + validation only" | Scope control |
| `PHASE4_CONSOLIDATION_ORCHESTRATOR.py` | Check: "2-3 dashboards + 8 templates" | Dashboard de-duplication |
| `coach_insights.py` | Add `validate_ponytail_ladder()` method | Integration point |
| `validate_trace_integration.py` | Add Ponytail ladder validation checks | Ensure compliance |

---

## Success Criteria

✅ **All phases pass Ponytail ladder at each gate**  
✅ **Coach metrics show 50%+ token efficiency per gate**  
✅ **No artifact overgeneration (target: 7 / 5 / 6 / 11 per gate)**  
✅ **Wave summary shows cost < $1.26, duration < 14s**  
✅ **Zero intentional simplifications without `ponytail:` comment**  

---

**Next:** Implement Ponytail ladder in each orchestrator, validate workflow end-to-end.

