# 🔗 Spec Integration Guide

> **Goal:** Update all 16 agent files to reference their corresponding specs. This enables deterministic execution.

---

## 📋 Checklist: Agent Updates Required

| Agent | Spec File | Agent File | Status |
|-------|-----------|-----------|--------|
| master-agent | 01-master-agent.md | master-agent.chatmode.md | ⏳ TODO |
| discovery-scout | 02-discovery-scout.md | discovery-scout.chatmode.md | ⏳ TODO |
| data-architect | 03-data-architect.md | data-architect.chatmode.md | ⏳ TODO |
| business-analyst | 04-business-analyst.md | business-analyst.chatmode.md | ⏳ TODO |
| data-modeler | 05-data-modeler.md | data-modeler.chatmode.md | ⏳ TODO |
| code-generator | 06-code-generator.md | code-generator.chatmode.md | ⏳ TODO |
| downstream-executor | 07-downstream-executor.md | downstream-executor.chatmode.md | ⏳ TODO |
| migration-coordinator | 08-migration-coordinator.md | migration-coordinator.chatmode.md | ⏳ TODO |
| quality-gate | 09-quality-gate.md | quality-gate.chatmode.md | ⏳ TODO |
| reconciliation | 10-reconciliation.md | reconciliation.chatmode.md | ⏳ TODO |
| data-steward | 11-data-steward.md | data-steward.chatmode.md | ⏳ TODO |
| self-healing | 12-self-healing.md | self-healing.chatmode.md | ⏳ TODO |
| logic-extractor | 13-logic-extractor.md | logic-extractor.chatmode.md | ⏳ TODO |
| iteration-improvement | 14-iteration-improvement.md | iteration-improvement.chatmode.md | ⏳ TODO |
| security-compliance | 15-security-compliance.md | security-compliance.chatmode.md | ⏳ TODO |
| inventory-scout | 16-inventory-scout.md | inventory-scout.chatmode.md | ⏳ TODO |

---

## 📝 Template: How to Update an Agent File

### Original Agent File (Example: master-agent.chatmode.md)

```markdown
---
name: master-agent
description: Routes user requests to appropriate agent
tools: [read, search]
user-invocable: true
---

# Master Agent — Request Router
[... existing instructions ...]
```

### Updated Agent File (With Spec Reference)

```markdown
---
name: master-agent
description: Routes user requests to appropriate agent
spec: .github/specs/01-master-agent.md
tools: [read, search]
user-invocable: true
---

# Master Agent — Request Router

## 🔗 Spec Reference

**See:** [Spec: master-agent](.github/specs/01-master-agent.md)

This agent follows spec `01-master-agent.md` which defines:
- ✅ **Input Contract:** What inputs are valid
- ✅ **Task Definition:** Exactly what to do
- ✅ **Success Criteria:** How to measure success
- ✅ **Output Contract:** What to produce
- ✅ **Constraints:** Non-negotiable rules

### Key Points from Spec

- **Role:** Route user requests to correct agent (no execution)
- **Must Reject:** Ambiguous requests (ask user for clarification)
- **Must Validate:** All inputs before forwarding
- **Must NOT:** Execute Phase 1-3 tasks directly

[... rest of agent instructions unchanged ...]
```

---

## 🔧 Step-by-Step Update Process

### For Each Agent (15 steps, 5 min per agent)

1. **Open agent file**
   ```
   File: .github/agents/[agent-name].chatmode.md
   ```

2. **Find the frontmatter** (top section with ---)
   ```yaml
   ---
   name: agent-name
   description: ...
   tools: [...]
   ---
   ```

3. **Add `spec:` line** (after `description:`)
   ```yaml
   ---
   name: agent-name
   description: ...
   spec: .github/specs/NN-agent-name.md
   tools: [...]
   ---
   ```

4. **Add spec reference section** (after title, before existing instructions)
   ```markdown
   ## 🔗 Spec Reference

   **Spec:** [.github/specs/NN-agent-name.md](.github/specs/NN-agent-name.md)

   This agent follows the spec which defines input, task, output, and constraints.

   **Key Requirements from Spec:**
   - [Requirement 1]
   - [Requirement 2]
   - [Requirement 3]
   ```

5. **Test validation**
   ```bash
   python .github/scripts/validate_agent_contracts.py --check-links
   ```

6. **Commit change**
   ```bash
   git add .github/agents/[agent-name].chatmode.md
   git commit -m "feat: link [agent-name] to spec NN"
   ```

---

## ✅ Validation Commands

### Check All Agent-Spec Links
```bash
python .github/scripts/validate_agent_contracts.py --check-links
```

**Expected Output:**
```
🔗 Checking agent-spec links...

✅ master-agent.chatmode.md → spec found
✅ discovery-scout.chatmode.md → spec found
✅ data-architect.chatmode.md → spec found
... (16 total)

✅ 16/16 agents linked to specs
```

### Validate All Specs
```bash
python .github/scripts/validate_agent_contracts.py --all-specs
```

**Expected Output:**
```
🔍 Validating all specs...

✅ 01-master-agent.md
✅ 02-discovery-scout.md
... (16 total)

📊 Results: 16/16 specs valid
```

### Validate Workflow
```bash
python .github/scripts/validate_agent_contracts.py --validate-wave Financeiro
```

---

## 📋 Example: Complete Update for One Agent

### Before

**File:** `.github/agents/discovery-scout.chatmode.md`

```markdown
---
name: discovery-scout
description: Extract legacy system inventory
tools: [read, search, azure]
user-invocable: true
---

# Discovery Scout — Legacy Analyzer

You are an expert legacy system analyzer. Extract every object from legacy systems:

1. Scan the legacy_folder
2. Parse DDL (CREATE TABLE, CREATE VIEW, etc.)
3. Catalog every object with its properties
4. Generate structured inventory

...
```

### After

**File:** `.github/agents/discovery-scout.chatmode.md`

```markdown
---
name: discovery-scout
description: Extract legacy system inventory
spec: .github/specs/02-discovery-scout.md
tools: [read, search, azure]
user-invocable: true
---

# Discovery Scout — Legacy Analyzer

## 🔗 Spec Reference

**Spec:** [.github/specs/02-discovery-scout.md](.github/specs/02-discovery-scout.md)

This agent strictly follows spec `02-discovery-scout.md` which defines:
- ✅ **Input Contract:** Requires `legacy_folder`, `platform_type`, `wave_config`, `discovery_owner`
- ✅ **Task Definition:** Scan → Categorize → Catalog → Flag unknowns → Output
- ✅ **Success Criteria:** 100% files scanned, all objects categorized, unknowns flagged
- ✅ **Output Contract:** `DISCOVERY_INVENTORY.json`, `discovery_summary.md`, metrics
- ✅ **Constraints:** NO GUESSING, NO INFERRING, Flag incomplete with ⚠️

### Key Rules from Spec

- **REJECT if:** legacy_folder doesn't exist, platform_type unrecognized, wave_config invalid YAML
- **DO NOT:** Guess missing data or assume object definitions
- **MUST:** Flag unknowns with ⚠️ INCOMPLETE (don't hide them)
- **OUTPUT:** Structured inventory (309 objects extracted → catalog every one)

---

You are an expert legacy system analyzer. Follow the spec above exactly.

Extract every object from legacy systems:

1. Scan the legacy_folder
2. Parse DDL (CREATE TABLE, CREATE VIEW, etc.)
3. Catalog every object with its properties
4. Generate structured inventory

...
```

---

## 🚀 Mass Update (All 16 Agents at Once)

If you prefer to update all agents together, create a script:

```bash
#!/bin/bash
# update-agents-with-specs.sh

AGENTS=(
  "master-agent"
  "discovery-scout"
  "data-architect"
  "business-analyst"
  "data-modeler"
  "code-generator"
  "downstream-executor"
  "migration-coordinator"
  "quality-gate"
  "reconciliation"
  "data-steward"
  "self-healing"
  "logic-extractor"
  "iteration-improvement"
  "security-compliance"
  "inventory-scout"
)

for agent in "${AGENTS[@]}"; do
  echo "Updating $agent..."
  # Add spec: line to YAML frontmatter
  # This is a simplified example (real script would be more sophisticated)
done

echo "✅ All agents updated!"
python .github/scripts/validate_agent_contracts.py --check-links
```

---

## 📊 Integration Status

### Timeline

| Phase | Timeline | Status |
|-------|----------|--------|
| **Phase 1: Create Specs** | 2026-06-16 | ✅ DONE |
| **Phase 2: Update Agents** | 2026-06-17 to 2026-06-19 | ⏳ IN PROGRESS |
| **Phase 3: Validate & Test** | 2026-06-20 | ⏳ PENDING |
| **Phase 4: Deploy** | 2026-06-21 | ⏳ PENDING |

### Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Agents with spec reference | 16/16 | 0/16 |
| Specs validated | 16/16 | 16/16 ✅ |
| Agent-spec links working | 16/16 | 0/16 |
| Workflow test passed | 1/1 | 0/1 |

---

## 🎯 Success Criteria

When integration is complete:

✅ All 16 agent files have `spec:` field in frontmatter  
✅ All agent files have spec reference section  
✅ `validate_agent_contracts.py --check-links` returns 16/16  
✅ No validation errors  
✅ Workflow test passes  
✅ Sample wave execution succeeds  

---

## 🆘 Troubleshooting

### Error: "Spec not found for agent X"

**Cause:** Agent file doesn't have `spec:` line in frontmatter

**Fix:**
```yaml
---
name: agent-name
spec: .github/specs/NN-agent-name.md
---
```

### Error: "Agent-spec links broken"

**Cause:** Spec file missing or named incorrectly

**Fix:**
1. Check spec exists: `ls .github/specs/NN-*.md`
2. Check spec name matches agent name
3. Verify path in agent file

### Error: "Validation failed for spec"

**Cause:** Spec missing required sections

**Fix:**
```bash
python .github/scripts/validate_agent_contracts.py --spec NN-agent.md
# Shows which sections missing
```

---

## 📚 References

| Document | Purpose |
|----------|---------|
| **HOW-TO-USE-SPECS.md** | Complete guide to specs system |
| **SPEC-TEMPLATE.md** | Master template for creating specs |
| **01-master-agent.md** | Example spec (best to start with) |
| **validate_agent_contracts.py** | Validation tool |

---

## ✨ Next Steps

1. **Today:** Review this guide
2. **Tomorrow:** Update 2-3 agents (test the process)
3. **This week:** Update remaining agents
4. **End of week:** Run full validation
5. **Next week:** Deploy integrated system

---

**Integration Status:** ⏳ IN PROGRESS  
**Last Updated:** 2026-06-16  
**Target Completion:** 2026-06-21
