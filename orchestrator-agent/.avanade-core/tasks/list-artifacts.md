# List Artifacts Task

**Task ID:** list-artifacts  
**Agent:** Orchestrator  
**Version:** 1.0

---

## Purpose

Scan the workspace and generate a comprehensive inventory of all project artifacts organized by phase, with status and location information.

---

## Artifact Categories

### UPSTREAM Artifacts

| Category | Artifacts | Pattern |
|----------|-----------|---------|
| Problem Definition | problem-statement.md | **/problem*.md |
| KPIs | kpis.md, metrics.md | **/kpi*.md, **/metric*.md |
| Analytical Questions | analytical-questions.md | **/analytical*.md, **/questions*.md |
| Source-to-Target | sttm.md, source-mapping.md | **/sttm*.md, **/source*.md |
| Initial DQ | dq-initial.md | **/dq-initial*.md |

### MIDSTREAM Artifacts

| Category | Artifacts | Pattern |
|----------|-----------|---------|
| Architecture | architecture.md, aod.md | **/architect*.md, **/aod*.md |
| Data Model | data-model.md, logical-model.md | **/model*.md, **/logical*.md |
| Decisions | decisions.md, adr-*.md | **/decision*.md, **/adr*.md |
| DQ Rules | dq-rules.md | **/dq-rules*.md, **/quality-rules*.md |
| Monitoring | monitoring.md, alerting.md | **/monitor*.md, **/alert*.md |

### DOWNSTREAM Artifacts

| Category | Artifacts | Pattern |
|----------|-----------|---------|
| DDL Scripts | *.sql in ddl/ | **/ddl/*.sql |
| ETL Code | *.sql or *.py in etl/ | **/etl/*.sql, **/etl/*.py |
| Tests | *.sql or *.py in tests/ | **/tests/*.sql, **/tests/*.py |
| Documentation | *.md in docs/ | **/docs/*.md, **/documentation/*.md |
| Quality Reports | *.md in quality/ | **/quality/*.md, **/profiles/*.md |

### ORCHESTRATION Artifacts

| Category | Artifacts | Pattern |
|----------|-----------|---------|
| Gate Reports | gate-*-report.md | **/gate*.md |
| Audit Trail | audit-trail.md | **/audit*.md |
| Status Reports | status-*.md | **/status*.md |

---

## Execution Steps

### Step 1: Scan Workspace

Use file search to locate all artifacts:

```
For each pattern in artifact_patterns:
  results = file_search(pattern)
  categorize(results)
```

### Step 2: Analyze Each Artifact

For each artifact found:
1. Get file metadata (size, modified date)
2. Check if file is empty
3. Estimate completeness (sections count)
4. Determine status

### Step 3: Categorize by Phase

Group artifacts into:
- UPSTREAM
- MIDSTREAM
- DOWNSTREAM
- ORCHESTRATION

### Step 4: Generate Inventory

Create comprehensive artifact list with statuses.

---

## Output Format

```markdown
# 📦 Project Artifacts Inventory

**Workspace:** {workspace_path}  
**Scan Date:** {date}  
**Total Artifacts:** {count}

---

## Summary by Phase

| Phase | Expected | Found | Completion |
|-------|----------|-------|------------|
| UPSTREAM | 5 | {n} | {%}% |
| MIDSTREAM | 5 | {n} | {%}% |
| DOWNSTREAM | 5+ | {n} | {%}% |
| ORCHESTRATION | 3 | {n} | {%}% |

---

## Overall Completion

```
UPSTREAM    [████████░░] 80%
MIDSTREAM   [██████░░░░] 60%
DOWNSTREAM  [████░░░░░░] 40%
OVERALL     [██████░░░░] 60%
```

---

## UPSTREAM Artifacts

### ✅ Found

| # | Artifact | Location | Size | Modified | Status |
|---|----------|----------|------|----------|--------|
| 1 | {name} | [{path}]({path}) | {size} | {date} | {status} |
| ... | ... | ... | ... | ... | ... |

### ❌ Missing

| # | Artifact | Expected Location | Responsible Agent |
|---|----------|-------------------|-------------------|
| 1 | {name} | {expected_path} | {agent} |
| ... | ... | ... | ... |

---

## MIDSTREAM Artifacts

### ✅ Found

| # | Artifact | Location | Size | Modified | Status |
|---|----------|----------|------|----------|--------|
| 1 | {name} | [{path}]({path}) | {size} | {date} | {status} |
| ... | ... | ... | ... | ... | ... |

### ❌ Missing

| # | Artifact | Expected Location | Responsible Agent |
|---|----------|-------------------|-------------------|
| 1 | {name} | {expected_path} | {agent} |
| ... | ... | ... | ... |

---

## DOWNSTREAM Artifacts

### DDL Scripts

| # | File | Location | Lines | Status |
|---|------|----------|-------|--------|
| 1 | {name} | [{path}]({path}) | {lines} | {status} |

### ETL Code

| # | File | Location | Lines | Status |
|---|------|----------|-------|--------|
| 1 | {name} | [{path}]({path}) | {lines} | {status} |

### Tests

| # | File | Location | Lines | Status |
|---|------|----------|-------|--------|
| 1 | {name} | [{path}]({path}) | {lines} | {status} |

### Documentation

| # | File | Location | Size | Status |
|---|------|----------|------|--------|
| 1 | {name} | [{path}]({path}) | {size} | {status} |

---

## ORCHESTRATION Artifacts

| # | Artifact | Location | Status |
|---|----------|----------|--------|
| 1 | Gate Reports | [{path}]({path}) | {status} |
| 2 | Audit Trail | [{path}]({path}) | {status} |
| 3 | Status Reports | [{path}]({path}) | {status} |

---

## Recommendations

### To Complete UPSTREAM
{list of actions and responsible agents}

### To Complete MIDSTREAM
{list of actions and responsible agents}

### To Complete DOWNSTREAM
{list of actions and responsible agents}

---

## Next Steps

Based on current inventory:
1. {recommendation_1}
2. {recommendation_2}
3. {recommendation_3}

**Suggested Agent:** {agent}  
**Suggested Command:** `*{command}`

---

*Inventory generated by Orchestrator Agent*
```

---

## Status Definitions

| Status | Icon | Description |
|--------|------|-------------|
| Complete | ✅ | Artifact exists and meets quality criteria |
| In Progress | 🔄 | Artifact exists but incomplete |
| Draft | 📝 | Artifact exists but needs review |
| Missing | ❌ | Artifact not found |
| Empty | ⚠️ | File exists but is empty |

---

## Commands

| Command | Description |
|---------|-------------|
| `*artifacts` | List all artifacts |
| `*artifacts upstream` | List UPSTREAM artifacts only |
| `*artifacts midstream` | List MIDSTREAM artifacts only |
| `*artifacts downstream` | List DOWNSTREAM artifacts only |
| `*artifacts missing` | List missing artifacts only |
| `*artifacts export` | Export inventory to file |
