# SDD (Spec Design Document) — Agent Blueprint

> **Purpose:** Eliminate hallucination. Define exact tasks, inputs, outputs, constraints.  
> **Audience:** The agent (machine-readable) + reviewers (human-readable)  
> **Size:** 1-2 pages max (keep context small)

---

## 1️⃣ Agent Identity

| Field | Value |
|-------|-------|
| **Name** | [Agent Name] |
| **File** | `.github/agents/[name].chatmode.md` |
| **Role** | [One-sentence mission] |
| **Triggered By** | [Other agents / users / conditions] |
| **Hands Off To** | [Next agent in workflow] |

---

## 2️⃣ Input Contract (What Comes In)

```
Required:
  ├─ [input_1]: [type] — [constraint]
  ├─ [input_2]: [type] — [constraint]
  └─ [input_N]: [type] — [constraint]

Optional:
  └─ [input_opt]: [type] — [default if missing]

Reject If:
  ├─ Missing required field
  ├─ Type mismatch
  └─ [other validation rule]
```

**Example:**
```
Required:
  ├─ wave_config.yaml: File — must exist in wave root
  ├─ platform_list: CSV — comma-separated platform names
  └─ discovery_owner: String — matches GitHub user

Reject If:
  ├─ wave_config.yaml doesn't parse as valid YAML
  ├─ No platforms specified
  └─ Discovery owner not in CODEOWNERS
```

---

## 3️⃣ Task Definition (What To Do)

### Primary Task
**Exactly** what to accomplish (no interpretation):
```
1. [Do this first]
2. [Then this]
3. [Then verify this]
4. [Output this]
```

### Success Criteria
- ✅ [Criterion 1] — how to measure
- ✅ [Criterion 2] — how to measure
- ✅ [Criterion 3] — how to measure

### Failure Modes
- ❌ If [X happens], then [Y action]
- ❌ If [X happens], then [Y action]
- ❌ If [X happens], then [escalate to Z]

---

## 4️⃣ Output Contract (What Goes Out)

```
Produces:
  ├─ [output_1]: [type] — [location/format]
  ├─ [output_2]: [type] — [location/format]
  └─ [output_N]: [type] — [location/format]

Passes To:
  └─ [Next Agent] with [what specifically]

Do NOT Produce:
  ├─ Assumptions (state them explicitly in warnings)
  ├─ Hallucinated data
  └─ Partial results
```

**Example:**
```
Produces:
  ├─ DISCOVERY_INVENTORY.json: File — projects/[project]/outputs/
  ├─ discovery_summary.md: File — projects/[project]/outputs/
  └─ discovery_metrics.json: File — projects/[project]/state/

Passes To:
  └─ business-analyst with complete DISCOVERY_INVENTORY.json

Do NOT Produce:
  ├─ Guesses about missing data
  ├─ Assumed data volumes
  └─ Incomplete object lists (flag as ⚠️ INCOMPLETE if needed)
```

---

## 5️⃣ Constraints (Non-Negotiable)

### Hard Rules (MUST)
- 🔴 [Rule 1] — why mandatory
- 🔴 [Rule 2] — why mandatory
- 🔴 [Rule 3] — why mandatory

### Microsoft Stack Only
- ✅ Allowed: [list]
- ❌ Forbidden: [list]

### Quality Gates
- ✅ Output must pass: [validation_script.py]
- ✅ Score must be: >= [threshold]
- ✅ No hallucination: [check method]

---

## 6️⃣ Context & References

| Ref | Purpose |
|-----|---------|
| [link] | What it is |
| [link] | What it is |

---

## 7️⃣ Example Execution

### Input Provided
```yaml
platform: "Cloudera"
wave_config: projects/clientebanco/wave-config.yaml
discovery_owner: "discovery-scout"
```

### Agent Does
```
1. Load wave-config.yaml
2. List all Cloudera objects from legacy/
3. Extract 309 objects (tables, views, procedures, etc.)
4. Validate against SCHEMA
5. Generate outputs
6. Hand off to business-analyst
```

### Output Generated
```
✅ DISCOVERY_INVENTORY.json (309 objects, validated)
✅ discovery_summary.md (human-readable report)
✅ discovery_metrics.json (KPIs)
✅ No hallucinated data
```

---

## 8️⃣ Token/Context Budget

| Item | Budget | Current |
|------|--------|---------|
| **Max spec size** | 1-2 KB | — |
| **Context window** | 4 KB | — |
| **Tokens per run** | ~500-2000 | — |
| **Tokens for full workflow** | ~10,000 | — |

---

## 9️⃣ Who Is Responsible?

| Role | Responsibility |
|------|-----------------|
| **Agent** | Execute spec exactly as written. Reject if unclear. |
| **Spec Author** | Keep spec tight, unambiguous, complete. |
| **QA (quality-gate)** | Validate output against success criteria. |
| **Coordinator** | Route between agents, validate gates. |

---

## 🔟 Changelog

| Date | Change | Reason |
|------|--------|--------|
| [YYYY-MM-DD] | [Change] | [Why] |

---

**Spec Status:** ✅ ACTIVE  
**Last Updated:** [DATE]  
**Next Review:** [DATE]
