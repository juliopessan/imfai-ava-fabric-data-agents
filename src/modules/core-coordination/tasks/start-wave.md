# Start Wave Task

**Task ID:** start-wave  
**Agent:** Orion (Migration Coordinator)  
**Version:** 1.0  
**Command:** `*start-wave`  
**Phase:** CORE

---

## Purpose

Initialize and execute a migration wave, selecting pipelines, resolving dependencies, configuring parallelism, and triggering the agent pipeline.

---

## Prerequisites

- Migration plan (migration-plan.md) approved by PM
- Source and target connections validated
- All agents operational and configured

---

## Inputs

| Input | Type | Required | Description |
|-------|------|----------|-------------|
| wave_id | string | Yes | Wave identifier (e.g., wave_1_pilot) |
| pipeline_ids | list | Yes | Pipeline IDs to include in this wave |
| strategy | string | Yes | Execution strategy: sequential, parallel, hybrid |
| parallelism | int | No | Max parallel workers (default: 5) |

---

## Execution Steps

### Step 1: Validate Wave Configuration

```
CHECK wave_id is unique (not previously executed)
CHECK all pipeline_ids exist in inventory.json
CHECK no pipeline_id is in another active wave
LOAD complexity classification for each pipeline
CALCULATE estimated execution time
```

### Step 2: Resolve Dependencies

```
LOAD dependency-graph.json from Scout
FOR EACH pipeline in wave:
  RESOLVE upstream dependencies
  VERIFY all dependencies are either:
    - Already migrated (in previous wave)
    - Included in this wave (will be processed first)
  IF unresolved dependencies:
    WARN and ask for confirmation
BUILD execution DAG (topological sort)
```

### Step 3: Configure Execution

```
SET parallelism based on strategy
CONFIGURE Celery workers
INITIALIZE Redis state for wave tracking
CREATE wave entry in Migration Control DB
SET wave status = "initialized"
```

### Step 4: Execute Pipeline Loop

```
FOR EACH pipeline in execution_order:
  1. Trigger Scout 🔍 → scan pipeline metadata
  2. Trigger Logan 🧠 → extract business logic
  3. Trigger Coda ⚙️ → generate target code
  4. Trigger Vera ✅ → validate code quality
  5. IF Vera rejects:
     Trigger Phoenix 🔧 → attempt fix (max 3x)
     Re-trigger Vera ✅
  6. Trigger Shield 🔒 → check compliance
  7. IF Shield rejects:
     Trigger Phoenix 🔧 → apply masking/fix
  8. Deploy to target platform
  9. UPDATE pipeline status in Control DB
```

### Step 5: Post-Wave Actions

```
Trigger Balance ⚖️ → reconcile wave data
Trigger Scribe 📚 → generate wave documentation
GENERATE wave-status-report using template
UPDATE wave status = "completed" or "completed_with_issues"
NOTIFY stakeholders
```

---

## Output

Generate wave execution report using `wave-status-report-tmpl.md` template.
