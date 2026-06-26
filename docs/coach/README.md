# 🤖 Coach — DMF AI Tutor System

**Owner:** Coach Team  
**Theme:** AI-powered best-practices tutor for data migrations  
**Status:** ✅ Phase 1 Complete | 🚀 Sprint 1 Ready

---

## 📋 Contents

This folder contains **complete design, decisions, and implementation guides** for integrating Coach as a best-practices tutor into the DMF (Data Migration Factory).

### **Files in This Folder**

| File | Purpose | Audience | Time |
|------|---------|----------|------|
| **COACH-COMO-TUTOR-BOAS-PRATICAS.md** | Strategic guide (PT-BR) | Executives, Sponsors | 10 min |
| **COACH-DECISIONS-APPROVED.md** | 3 locked decisions + timeline | Team Leads | 15 min |
| **COACH-INTEGRATION-BLUEPRINT.md** | 42-section complete design | Architects | 45 min |
| **COACH-IMPLEMENTATION-SUMMARY.md** | Implementation overview | Developers | 20 min |
| **COACH-PHASE-1-COMPLETE.md** | Phase 1 recap + Sprint 1 plan | Everyone | 15 min |
| **COACH-DOCUMENTATION-INDEX.md** | Navigation guide for all docs | Everyone | 10 min |

---

## 🎯 Quick Start

### **For Executives (5 min)**
```
1. Read:  COACH-COMO-TUTOR-BOAS-PRATICAS.md
2. Action: Understand strategy + ROI
3. Decision: Approve Sprint 1 budget
```

### **For PMs (15 min)**
```
1. Read:  COACH-DECISIONS-APPROVED.md
2. Action: Understand decisions + assign owners
3. Task: Schedule Sprint 1 kickoff (Jun 25)
```

### **For Developers (Week 1–2)**
```
1. Read: .coach/SPRINT-1-KICKOFF-GUIDE.md (in parent directory)
2. Copy: Code examples from src/shared/coaches/INTEGRATION-EXAMPLES.py
3. Implement: Week 1 (telemetry) + Week 2 (GateScore + dashboard)
```

### **For Architects (45 min)**
```
1. Read: COACH-INTEGRATION-BLUEPRINT.md
2. Review: 42 sections, decisions, alternatives
3. Validate: Architecture against DMF patterns
```

---

## 🔑 The 3 Decisions

### ✅ Decision 1: Telemetry Hook Location
- **Where:** `migration-coordinator.spawn_agent()`
- **When:** AFTER agent execution, BEFORE return
- **What:** Capture agent execution events (tokens, cost, time, artifact)
- **Status:** APPROVED

### ✅ Decision 2: GateScore Adjustment
- **When:** During `quality-gate.calculate_gatescore()`
- **How:** Auto-deduct anti-pattern impacts (-15, -10, -5, -30 points)
- **Result:** Adjusted score used for approval decision
- **Status:** APPROVED

### ✅ Decision 3: Skills Governance
- **Status:** TBD (deferred)
- **Timeline:** Sprint 3 (week of Jul 22)
- **Note:** Placeholder implemented, approval workflow pending
- **Status:** APPROVED as deferred

---

## 📊 The 6 Anti-Patterns

| # | Pattern | Severity | Impact | Trigger |
|---|---------|----------|--------|---------|
| 1 | Wave Completion | HIGH | -15 | Entity coverage < 90% |
| 2 | STTM Stability | MEDIUM | -10 | Regen > 2× in 2h |
| 3 | Model Overreliance | LOW | -5 | GPT-4 on parametric tasks |
| 4 | Context Bloat | MEDIUM | -10 | Context > 70% |
| 5 | Silent Executor ⚠️ | CRITICAL | -30 | Output < 1000 tokens |
| 6 | GateScore Regression | HIGH | -20 | Drop > 5% WoW |

---

## 🚀 Sprint 1 Timeline

```
WEEK 1 (Jun 25–28)  ✓ Telemetry Hook
WEEK 2 (Jul 1–5)    ✓ GateScore + Dashboard
```

**Deliverable:** Telemetry flowing + GateScore adjusting + metrics dashboard  
**Success Criteria:** All 3 components working on Financeiro Wave 2 history

---

## 🔗 Related Documents

### **In This Folder**
- All 6 files listed above

### **In Root /docs**
- **README.md** — Main documentation portal
- **DOCS-STRUCTURE-INDEX.md** — Navigation map

### **In Parent Directories**
- **.coach/SPRINT-1-KICKOFF-GUIDE.md** — Week-by-week Sprint 1 tasks (PT-BR)
- **src/shared/coaches/INTEGRATION-EXAMPLES.py** — Code examples
- **src/shared/coaches/integration.py** — Implementation (hooks)

### **In Other Folders**
- `../governance/AUDIT-REPORT-2026-06-16.md` — Quality audits
- `../implementation/IMPLEMENTATION-GUIDE-AGENTIC-ENGINEERING.md` — Engineering patterns
- `../sessions/SESSION-SUMMARY-2026-06-18.md` — Session decisions

---

## 📚 How to Use These Files

### **Scenario 1: "I need to understand Coach quickly"**
```
Read in this order:
1. COACH-PHASE-1-COMPLETE.md         (Phase 1 recap, 10 min)
2. COACH-COMO-TUTOR-BOAS-PRATICAS.md (Strategy, 10 min)
→ You now understand Coach ✅
```

### **Scenario 2: "I need to implement Sprint 1"**
```
Read in this order:
1. COACH-DECISIONS-APPROVED.md                 (Decisions, 15 min)
2. .coach/SPRINT-1-KICKOFF-GUIDE.md           (Tasks, 30 min)
3. src/shared/coaches/INTEGRATION-EXAMPLES.py (Code, 15 min)
→ You can now start coding ✅
```

### **Scenario 3: "I need to review the architecture"**
```
Read in this order:
1. COACH-INTEGRATION-BLUEPRINT.md (42 sections, 45 min)
2. COACH-DECISIONS-APPROVED.md    (Rationale, 15 min)
→ You understand all design decisions ✅
```

### **Scenario 4: "I'm lost, where do I start?"**
```
Read: COACH-DOCUMENTATION-INDEX.md
→ Get navigation + links to specific topics ✅
```

---

## 🎓 Key Concepts

### **What is Coach?**
An AI system that observes DMF agent executions and provides continuous feedback for improvement through:
- **Observe** → Telemetry (what agents are doing)
- **Measure** → Metrics (cost, time, tokens, quality)
- **Improve** → Anti-patterns (detect problems early)
- **Level Up** → Skills (reuse patterns, optimize)

### **Why Coach Matters**
- 🎯 **Predictability:** -50% variance in GateScore
- ⚡ **Speed:** -75% waste (retrabalho/wave)
- 💰 **Efficiency:** -33% cost per entity
- 🔍 **Visibility:** 100% silent failure detection

### **How It Integrates**
1. **Telemetry Hook** — Captures agent execution data
2. **Anti-Pattern Detection** — Analyzes 6 known issues
3. **GateScore Adjustment** — Auto-penalizes anti-patterns
4. **Dashboard** — Visualizes metrics for team

---

## 📖 File Descriptions

### **COACH-COMO-TUTOR-BOAS-PRATICAS.md**
```
🇧🇷 PT-BR Strategic Guide

Covers:
  • The problem Coach solves
  • 4 feedback loops (Observe, Measure, Improve, Level Up)
  • 3 real-world examples
  • Metrics of success
  • Why Coach is essential

Audience: Executives, sponsors, leadership
Time: 10–15 minutes
Language: Portuguese (PT-BR)
```

### **COACH-DECISIONS-APPROVED.md**
```
📋 Decision Record + Sprint 1 Plan

Covers:
  • 3 critical architectural decisions
  • Rationale for each decision
  • Implementation timeline
  • What's done, what's next
  • How to use Coach

Audience: Team leads, developers, reviewers
Time: 15–20 minutes
Language: Mixed (PT-BR + EN)
```

### **COACH-INTEGRATION-BLUEPRINT.md**
```
🏗️ Complete Technical Design

Covers:
  • 42 sections (full design document)
  • Coach 5 pillars × DMF workflows
  • 6 anti-patterns detailed
  • Integration architecture
  • Data models, APIs, error handling
  • Wireframes, alternatives, FAQs

Audience: Architects, tech leads, reviewers
Time: 45–60 minutes
Language: English (EN-US)
```

### **COACH-IMPLEMENTATION-SUMMARY.md**
```
📝 Implementation Overview

Covers:
  • What was delivered (phase 1)
  • Python modules created
  • Code examples
  • Next steps (Sprint 1)

Audience: Developers, PMs
Time: 15–20 minutes
Language: English (EN-US)
```

### **COACH-PHASE-1-COMPLETE.md**
```
✅ Phase 1 Recap + Sprint 1 Ready

Covers:
  • Phase 1 deliverables
  • The 6 anti-patterns
  • File map (what you have)
  • Sprint 1 timeline
  • How to start

Audience: Everyone
Time: 15 minutes
Language: English (EN-US)
```

### **COACH-DOCUMENTATION-INDEX.md**
```
🧭 Navigation Guide

Covers:
  • All Coach documents
  • How to find things
  • Role-based quick starts
  • Cross-document references

Audience: Anyone lost
Time: 10 minutes
Language: English (EN-US)
```

---

## 🔄 Workflow: Adding New Coach Docs

### **When Adding a File**
1. **Decide**: Is it Coach-related? (If no, move to another folder)
2. **Place it here** in `docs/coach/`
3. **Update this README.md** (add to "Contents" table)
4. **Update COACH-DOCUMENTATION-INDEX.md** (if it's a new document type)

### **Naming Convention**
- Use: `COACH-<DESCRIPTION>.md`
- Examples:
  - ✅ `COACH-DECISIONS-APPROVED.md`
  - ✅ `COACH-TELEMETRY-SETUP.md`
  - ❌ `telemetry-setup.md` (missing prefix)

### **Version Control**
- Never delete docs (mark as `[DEPRECATED]` if needed)
- Always update "Last Updated" date
- Add date to filename if tracking versions: `COACH-XYZ-2026-06-18.md`

---

## ✅ Checklist: Ready for Coach?

- [ ] Read COACH-PHASE-1-COMPLETE.md (10 min)
- [ ] Understand 3 decisions from COACH-DECISIONS-APPROVED.md
- [ ] Know Sprint 1 timeline (Jun 25 – Jul 5)
- [ ] Assigned owner for Week 1 (telemetry)
- [ ] Assigned owner for Week 2 (GateScore + dashboard)
- [ ] Daily standups scheduled (Mon–Fri)
- [ ] Python environment ready (imports verified)

**All checked? You're ready for Sprint 1! 🚀**

---

## 📞 Support

### **"Where do I start?"**
→ COACH-PHASE-1-COMPLETE.md

### **"I'm coding Sprint 1"**
→ .coach/SPRINT-1-KICKOFF-GUIDE.md (in parent directory)

### **"I need design details"**
→ COACH-INTEGRATION-BLUEPRINT.md

### **"I need code examples"**
→ src/shared/coaches/INTEGRATION-EXAMPLES.py (in src/ directory)

### **"I'm lost"**
→ COACH-DOCUMENTATION-INDEX.md

---

**Status:** ✅ Phase 1 Complete | 🚀 Sprint 1 Ready  
**Created:** 2026-06-18 | **Owner:** Coach Team

Ready to go! 🎉
