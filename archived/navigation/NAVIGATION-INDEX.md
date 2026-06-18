# 🗺️ Repository Navigation Index

**Date:** 2026-06-16  
**Purpose:** Find exactly what you need based on your role & task  
**Master Index:** [INDEX.md](INDEX.md) | [REPOSITORY-ORGANIZATION.md](REPOSITORY-ORGANIZATION.md)

---

## 🎯 By Role

### 👤 New Team Member
Start here to understand the project:
1. **[README.md](README.md)** — Overview & quick start
2. **[QUICK-START.md](QUICK-START.md)** — Get running in 5 minutes
3. **[AGENTIC-ENGINEERING-V1-SUMMARY.md](AGENTIC-ENGINEERING-V1-SUMMARY.md)** — Understand "agentic engineering"
4. **[docs/HARNESS-MANIFEST.md](docs/HARNESS-MANIFEST.md)** — What is harness?
5. **[REPOSITORY-ORGANIZATION.md](REPOSITORY-ORGANIZATION.md)** — How repo is structured

### 🏗️ Architect / Solution Designer
Understand the architecture:
- **[docs/HARNESS-MANIFEST.md](docs/HARNESS-MANIFEST.md)** — Harness components & policies
- **[docs/HUMAN-AGENT-CHECKPOINTS.md](docs/HUMAN-AGENT-CHECKPOINTS.md)** — Escalation rules (3-tier)
- **[projects/bradesco/WORKFLOW_AND_ARCHITECTURE.md](projects/bradesco/WORKFLOW_AND_ARCHITECTURE.md)** — Migration pipeline
- **[AGENTIC-ENGINEERING-V1-SUMMARY.md](AGENTIC-ENGINEERING-V1-SUMMARY.md)** — New framework overview
- **[src/shared/schemas/wave-config-extended.yaml](src/shared/schemas/wave-config-extended.yaml)** — Configuration schema

### 👨‍💻 Agent / Skill Developer
Implement new agents or skills:
- **[src/shared/schemas/wave-config-extended.yaml](src/shared/schemas/wave-config-extended.yaml)** — Skills versioning
- **[.github/copilot-instructions.md](.github/copilot-instructions.md)** — Agent development guidelines
- **[.github/skills/README.md](.github/skills/README.md)** — How to create skills
- **[AGENTIC-ENGINEERING-V1-SUMMARY.md](AGENTIC-ENGINEERING-V1-SUMMARY.md)** — Skills versioning strategy

### 🔧 DevOps / SRE
Implement observability & infrastructure:
- **[docs/OBSERVABILITY-AND-TRACES.md](docs/OBSERVABILITY-AND-TRACES.md)** — Traces, spans, cost attribution
- **[src/shared/scripts/README.md](src/shared/scripts/README.md)** — Governance modules overview
- **[config/README.md](config/README.md)** — Configuration & setup
- **[AGENTIC-ENGINEERING-V1-SUMMARY.md](AGENTIC-ENGINEERING-V1-SUMMARY.md)** — Observability roadmap (Week 3)

### 📊 Project Manager / Product Owner
Track progress & make decisions:
- **[QUICK-START.md](QUICK-START.md)** — How to run migrations
- **[projects/multi-platform-migration/EXEC-SUMMARY.md](projects/multi-platform-migration/EXEC-SUMMARY.md)** — Wave executive brief
- **[PHASE2-PHASE3-DELIVERY-SUMMARY.md](PHASE2-PHASE3-DELIVERY-SUMMARY.md)** — What was built
- **[/memories/repo/MEMORY-INDEX.md](/memories/repo/MEMORY-INDEX.md)** — Historical context

### 🧪 QA / Test Lead
Validate & monitor quality:
- **[docs/HUMAN-AGENT-CHECKPOINTS.md](docs/HUMAN-AGENT-CHECKPOINTS.md)** — Escalation & SLAs
- **[src/shared/schemas/spec-as-executable.md](src/shared/schemas/spec-as-executable.md)** — Spec validators (DataContractValidator)
- **[src/shared/tests/](src/shared/tests/)** — 189 test cases
- **[AGENTIC-ENGINEERING-V1-SUMMARY.md](AGENTIC-ENGINEERING-V1-SUMMARY.md)** — Week 4: Specs validation

### 📝 Data Analyst / Domain Expert
Work with data models & specs:
- **[.github/specs/HOW-TO-USE-SPECS.md](.github/specs/HOW-TO-USE-SPECS.md)** — Specs system (3000+ words)
- **[src/shared/schemas/spec-as-executable.md](src/shared/schemas/spec-as-executable.md)** — Write data contracts
- **[projects/bradesco/](projects/bradesco/)** — See examples

---

## 📚 By Task / Problem

### "I need to..."

#### ...understand what agentic engineering is
→ **[AGENTIC-ENGINEERING-V1-SUMMARY.md](AGENTIC-ENGINEERING-V1-SUMMARY.md)** (5 min read)

#### ...implement harness formalization
→ **[docs/HARNESS-MANIFEST.md](docs/HARNESS-MANIFEST.md)** (detail)  
→ **[docs/HARNESS-CHANGELOG.md](docs/HARNESS-CHANGELOG.md)** (tracking)

#### ...set up observability (traces, cost, drift)
→ **[docs/OBSERVABILITY-AND-TRACES.md](docs/OBSERVABILITY-AND-TRACES.md)** (8-week roadmap)

#### ...implement escalation rules (3-tier system)
→ **[docs/HUMAN-AGENT-CHECKPOINTS.md](docs/HUMAN-AGENT-CHECKPOINTS.md)** (gate-specific rules)

#### ...version my skills independently
→ **[src/shared/schemas/wave-config-extended.yaml](src/shared/schemas/wave-config-extended.yaml)** (config)  
→ **[AGENTIC-ENGINEERING-V1-SUMMARY.md](AGENTIC-ENGINEERING-V1-SUMMARY.md)** (Week 2 roadmap)

#### ...create executable specs (not static docs)
→ **[src/shared/schemas/spec-as-executable.md](src/shared/schemas/spec-as-executable.md)** (DataContractValidator)  
→ **[.github/specs/HOW-TO-USE-SPECS.md](.github/specs/HOW-TO-USE-SPECS.md)** (general specs info)

#### ...run a Bradesco migration
→ **[QUICK-START.md](QUICK-START.md)** (5 min)  
→ **[projects/bradesco/README.md](projects/bradesco/README.md)** (detailed)

#### ...understand the wave configuration
→ **[src/shared/schemas/wave-config-extended.yaml](src/shared/schemas/wave-config-extended.yaml)** (full schema)  
→ **[/memories/repo/bradesco-migration-setup.md](/memories/repo/bradesco-migration-setup.md)** (context)

#### ...find a script or module
→ **[REPOSITORY-QUICK-REFERENCE.md](REPOSITORY-QUICK-REFERENCE.md)** (file locations)  
→ **[src/shared/scripts/README.md](src/shared/scripts/README.md)** (script descriptions)

#### ...understand the 3-tier governance model
→ **[docs/HARNESS-MANIFEST.md](docs/HARNESS-MANIFEST.md)** (governance policies)  
→ **[PHASE2-PHASE3-IMPLEMENTATION-COMPLETE.md](PHASE2-PHASE3-IMPLEMENTATION-COMPLETE.md)** (full spec)

#### ...track my project progress
→ **[/memories/repo/MEMORY-INDEX.md](/memories/repo/MEMORY-INDEX.md)** (persistent knowledge)  
→ **[projects/[your-project]/](projects/)** (project-specific files)

#### ...implement the 4-week agentic engineering roadmap
→ **[AGENTIC-ENGINEERING-V1-SUMMARY.md](AGENTIC-ENGINEERING-V1-SUMMARY.md)** (overview)  
→ **[docs/IMPLEMENTATION-GUIDE-AGENTIC-ENGINEERING.md](docs/IMPLEMENTATION-GUIDE-AGENTIC-ENGINEERING.md)** (detailed roadmap)

---

## 📂 By Document Type

### Comprehensive Guides
- **[AGENTIC-ENGINEERING-V1-SUMMARY.md](AGENTIC-ENGINEERING-V1-SUMMARY.md)** — New framework overview (v1.0)
- **[PHASE2-PHASE3-IMPLEMENTATION-COMPLETE.md](PHASE2-PHASE3-IMPLEMENTATION-COMPLETE.md)** — Specs system architecture
- **[REPOSITORY-ORGANIZATION.md](REPOSITORY-ORGANIZATION.md)** — Full repo structure explained
- **[.github/specs/HOW-TO-USE-SPECS.md](.github/specs/HOW-TO-USE-SPECS.md)** — Specs system (3000+ words)

### Architecture Docs
- **[docs/HARNESS-MANIFEST.md](docs/HARNESS-MANIFEST.md)** — Harness components & policies
- **[docs/HUMAN-AGENT-CHECKPOINTS.md](docs/HUMAN-AGENT-CHECKPOINTS.md)** — Escalation architecture
- **[docs/OBSERVABILITY-AND-TRACES.md](docs/OBSERVABILITY-AND-TRACES.md)** — Observability architecture
- **[projects/bradesco/WORKFLOW_AND_ARCHITECTURE.md](projects/bradesco/WORKFLOW_AND_ARCHITECTURE.md)** — Pipeline architecture

### Quick References
- **[QUICK-START.md](QUICK-START.md)** — Get running in 5 min
- **[REPOSITORY-QUICK-REFERENCE.md](REPOSITORY-QUICK-REFERENCE.md)** — File & script locations
- **[PHASE2-PHASE3-QUICK-START.md](PHASE2-PHASE3-QUICK-START.md)** — Phase 2 & 3 commands

### Roadmaps & Plans
- **[AGENTIC-ENGINEERING-V1-SUMMARY.md](AGENTIC-ENGINEERING-V1-SUMMARY.md)** — 4-week implementation roadmap
- **[docs/IMPLEMENTATION-GUIDE-AGENTIC-ENGINEERING.md](docs/IMPLEMENTATION-GUIDE-AGENTIC-ENGINEERING.md)** — Detailed implementation guide
- **[PHASE2-PHASE3-EXECUTION-ROADMAP.md](PHASE2-PHASE3-EXECUTION-ROADMAP.md)** — Phase 2 & 3 detailed roadmap

### Schemas & Configuration
- **[src/shared/schemas/wave-config-extended.yaml](src/shared/schemas/wave-config-extended.yaml)** — Wave configuration schema
- **[src/shared/schemas/spec-as-executable.md](src/shared/schemas/spec-as-executable.md)** — Specification schema & validator

### Memory & Knowledge
- **[/memories/repo/MEMORY-INDEX.md](/memories/repo/MEMORY-INDEX.md)** — Memory file index
- **[/memories/repo/fabricae-*.md](/memories/repo/)** — Platform decisions & lessons learned
- **[/memories/repo/phase2-phase3-*.md](/memories/repo/)** — Implementation history

### Executive Summaries
- **[PHASE2-PHASE3-DELIVERY-SUMMARY.md](PHASE2-PHASE3-DELIVERY-SUMMARY.md)** — What was built
- **[projects/multi-platform-migration/EXEC-SUMMARY.md](projects/multi-platform-migration/EXEC-SUMMARY.md)** — Wave overview

---

## 🆕 What's New (2026-06-16)

### Agentic Engineering Framework
**Status:** ✅ Complete & Ready for Implementation

| Document | Size | Purpose | Timeline |
|----------|------|---------|----------|
| AGENTIC-ENGINEERING-V1-SUMMARY | 18 KB | Executive summary | READ NOW |
| docs/HARNESS-MANIFEST | 26 KB | Harness formalization | Week 1 |
| docs/HARNESS-CHANGELOG | 14 KB | Version tracking | Week 1 |
| docs/OBSERVABILITY-AND-TRACES | 32 KB | Tracing + cost | Week 3 |
| docs/HUMAN-AGENT-CHECKPOINTS | 28 KB | Escalation rules | Week 4 |
| docs/IMPLEMENTATION-GUIDE-AGENTIC-ENGINEERING | 18 KB | Roadmap | READ NOW |
| src/shared/schemas/wave-config-extended | FULL | Skills versioning | Week 2 |
| src/shared/schemas/spec-as-executable | 32 KB | Spec validators | Week 4 |

**Next Step:** Read [AGENTIC-ENGINEERING-V1-SUMMARY.md](AGENTIC-ENGINEERING-V1-SUMMARY.md)

---

## 🔗 Cross-References

### If you're working on:

**A migration wave:**  
1. Check wave config template → `src/shared/schemas/wave-config-extended.yaml`
2. Learn specs format → `src/shared/schemas/spec-as-executable.md`
3. Understand orchestration → `projects/bradesco/WORKFLOW_AND_ARCHITECTURE.md`

**Harness improvements:**  
1. Understand current harness → `docs/HARNESS-MANIFEST.md`
2. Track changes → `docs/HARNESS-CHANGELOG.md`
3. Implement new rules → `docs/HUMAN-AGENT-CHECKPOINTS.md`

**Observability / monitoring:**  
1. Understand traces architecture → `docs/OBSERVABILITY-AND-TRACES.md`
2. Follow 8-week roadmap → Same file (Week 1-4 detailed)
3. Build PowerBI dashboard → Same file (metrics + KQL examples)

**Specs system:**  
1. Quick intro → `.github/specs/HOW-TO-USE-SPECS.md`
2. Technical deep-dive → `src/shared/schemas/spec-as-executable.md`
3. See examples → `PHASE2-PHASE3-*.md` files

---

## 📞 Still Lost?

Try these:
1. **Search this file** (Ctrl+F) for your keyword
2. **Read [INDEX.md](INDEX.md)** (master index)
3. **Check [REPOSITORY-QUICK-REFERENCE.md](REPOSITORY-QUICK-REFERENCE.md)** (file locations)
4. **Ask in** `/memories/repo/MEMORY-INDEX.md` (patterns & lessons)

---

**Last Updated:** 2026-06-16  
**Status:** 🟢 Navigation Complete
