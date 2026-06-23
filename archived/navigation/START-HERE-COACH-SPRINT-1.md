# 🎯 DMF Coach — NEXT IMMEDIATE STEPS

**Created:** 2026-06-18  
**Status:** 🟢 Phase 1 Complete  
**Next:** Sprint 1 Kickoff (Jun 25)  

---

## ⏱️ What To Do RIGHT NOW (Today – Jun 18)

### Step 1: Read Documentation (15 minutes)
**Pick ONE of these based on your role:**

**If you're an executive:**
```
READ: docs/COACH-COMO-TUTOR-BOAS-PRATICAS.md
TIME: 10 minutes
ACTION: Understand strategy + approve Sprint 1 budget
```

**If you're a PM / Tech Lead:**
```
READ: docs/COACH-DECISIONS-APPROVED.md
TIME: 15 minutes
ACTION: Understand decisions + assign owners for Sprint 1
```

**If you're a developer (you will code Sprint 1):**
```
READ: .coach/SPRINT-1-KICKOFF-GUIDE.md
TIME: 30 minutes
ACTION: Know what you'll code starting Jun 25
```

**If you're an architect / reviewer:**
```
READ: docs/COACH-INTEGRATION-BLUEPRINT.md
TIME: 45 minutes
ACTION: Understand full design, validate decisions
```

---

## Step 2: Verify You Have Everything (5 minutes)

### Check Files Exist
```bash
cd ~/projects/imfai-ava-fabric-data-agents

# Should see all 6 docs/COACH-*.md files:
ls docs/COACH-*

# Should see Python modules:
ls src/shared/coaches/*.py

# Should see .coach infrastructure:
ls -la .coach/
```

### Check Imports Work
```bash
python -c "from src.shared.coaches import telemetry_hook, gate_scorer; print('✅ Ready')"
```

If both succeed → **You have everything!** ✅

---

## Step 3: Assign Owners for Sprint 1 (Before Jun 25)

### **Week 1 Owner (Jun 25–28) — Telemetry Hook**
```
Task: Find migration-coordinator.py and add telemetry hook
Assigned to: ___________________
Start date: Jun 25
End date: Jun 28
Deliverable: .coach/telemetry/wave_*.jsonl files created
```

### **Week 2 Owner (Jul 1–5) — GateScore + Dashboard**
```
Task: Find quality-gate.py, add adjustment, build dashboard
Assigned to: ___________________
Start date: Jul 1
End date: Jul 5
Deliverable: GateScore adjusting + HTML dashboard working
```

**ACTION:** Assign these two people NOW (before Jun 25 kickoff)

---

## Step 4: Schedule Sprint 1 Kickoff (Before Jun 25)

```
📅 DATE:     Monday, Jun 25, 2026
🕐 TIME:     [Decide now]
📍 WHERE:    [Conference room or Teams meeting]
⏱️  DURATION: 15 minutes

ATTENDEES:
  • Coach Owner
  • Week 1 Owner (migration-coordinator)
  • Week 2 Owner (GateScore + dashboard)
  • [Optional] Architect (reviewer)

AGENDA:
  1. Review Phase 1 deliverables (2 min)
  2. Review 3 decisions (3 min)
  3. Review Week 1 + Week 2 tasks (5 min)
  4. Identify real files to modify (3 min)
  5. Confirm daily standups (Mon–Fri, 5 min) (2 min)
```

**ACTION:** Send calendar invite NOW

---

## Step 5: Copy One Code Example (5 minutes)

### For Week 1 Owner:
```bash
# Copy this example to understand the pattern:
open src/shared/coaches/INTEGRATION-EXAMPLES.py

# Jump to: EXAMPLE_1_MIGRATION_COORDINATOR
# (This is what you'll implement in Week 1)
```

### For Week 2 Owner:
```bash
# Copy this example to understand the pattern:
open src/shared/coaches/INTEGRATION-EXAMPLES.py

# Jump to: EXAMPLE_2_QUALITY_GATE
# (This is what you'll implement in Week 2)
```

---

## Step 6: Create Sprint 1 Calendar (Before Jun 25)

```
📅 Sprint 1 Timeline:

MON–FRI (Jun 25–28)    WEEK 1: Telemetry Hook
  ├─ Mon Jun 25 (10:00) — Kickoff meeting
  ├─ Mon Jun 25 (11:00) — Week 1 owner starts: find migration-coordinator.py
  ├─ Tue Jun 26 — Add telemetry hook
  ├─ Wed Jun 27 — Test with real agent
  ├─ Thu Jun 28 (10:00) — Standup: Week 1 status
  └─ Fri Jun 28 (16:00) — Week 1 deliverable due

MON–FRI (Jul 1–5)      WEEK 2: GateScore + Dashboard
  ├─ Mon Jul 1 (10:00) — Week 2 owner starts: find quality-gate.py
  ├─ Tue Jul 2 — Add GateScore hook
  ├─ Wed Jul 3 — Build dashboard
  ├─ Thu Jul 4 (10:00) — Standup: Week 2 status
  └─ Fri Jul 5 (16:00) — Sprint 1 COMPLETE ✅
```

**ACTION:** Add to team calendar NOW

---

## 🚀 QUICK START CHECKLIST

Before Jun 25 Kickoff:

**LEADERSHIP:**
- [ ] Read docs/COACH-COMO-TUTOR-BOAS-PRATICAS.md (10 min)
- [ ] Approve Sprint 1 go-ahead

**PM / TECH LEAD:**
- [ ] Read docs/COACH-DECISIONS-APPROVED.md (15 min)
- [ ] Assign Week 1 owner
- [ ] Assign Week 2 owner
- [ ] Schedule kickoff meeting (Jun 25, 15 min)
- [ ] Confirm daily standups (Mon–Fri)

**WEEK 1 OWNER:**
- [ ] Read .coach/SPRINT-1-KICKOFF-GUIDE.md (30 min)
- [ ] Copy EXAMPLE_1_MIGRATION_COORDINATOR (15 min)
- [ ] Prepare to find migration-coordinator.py (30 min research)

**WEEK 2 OWNER:**
- [ ] Read .coach/SPRINT-1-KICKOFF-GUIDE.md (30 min)
- [ ] Copy EXAMPLE_2_QUALITY_GATE (15 min)
- [ ] Prepare to find quality-gate.py (30 min research)

**EVERYONE:**
- [ ] Verify Python imports work (5 min)
- [ ] Know where to find documentation (link below)

---

## 📚 Documentation Cheat Sheet

**Lost? Use this to find things:**

```
👤 "I'm an executive"
   → docs/COACH-COMO-TUTOR-BOAS-PRATICAS.md (10 min)

💼 "I'm a PM"
   → docs/COACH-DECISIONS-APPROVED.md (15 min)

👨‍💻 "I'm coding Week 1"
   → .coach/SPRINT-1-KICKOFF-GUIDE.md Tarefa 1–4

👨‍💻 "I'm coding Week 2"
   → .coach/SPRINT-1-KICKOFF-GUIDE.md Tarefa 5–8

🏗️ "I want to understand the design"
   → docs/COACH-INTEGRATION-BLUEPRINT.md (45 min)

❓ "I need help navigating"
   → docs/COACH-DOCUMENTATION-INDEX.md (10 min)

⚡ "I want a quick reference"
   → .coach/README.md (10 min)

🎯 "I need code examples"
   → src/shared/coaches/INTEGRATION-EXAMPLES.py (copy-paste)

📊 "What's the summary?"
   → COACH-PHASE-1-FINAL-DELIVERY.txt (this directory)
```

---

## ✅ Success Criteria (For Sprint 1)

### **By Friday, Jul 5 @ 16:00:**

**Telemetry Hook (Week 1):**
- [ ] migration-coordinator.py modified with telemetry_hook call
- [ ] No syntax errors
- [ ] Tested with real agent execution
- [ ] `.coach/telemetry/clientebanco_wave_2_*.jsonl` file created
- [ ] Events contain: timestamp, agent_id, tokens, cost

**GateScore Adjustment (Week 2):**
- [ ] quality-gate.py modified with gate_scorer.adjust_score() call
- [ ] No syntax errors
- [ ] Tested with mock artifacts
- [ ] Adjusted score used for approval decision
- [ ] Anti-patterns correctly deducted

**Dashboard (Week 2):**
- [ ] `.coach/templates/wave-analysis.html` created (or similar)
- [ ] Can read JSONL telemetry files
- [ ] Generates HTML report with charts
- [ ] Shows metrics (tokens, cost, patterns detected)

**Documentation:**
- [ ] All code has comments (what, why, error handling)
- [ ] Sprint 1 tasks marked DONE in .coach/SPRINT-1-KICKOFF-GUIDE.md
- [ ] Any blockers documented

**Sprint 1 COMPLETE = All above done ✅**

---

## 📞 If You Get Stuck

### **"Where is the real migration-coordinator.py file?"**
→ Run: `grep -r "def spawn_agent" src/` in the terminal

### **"Where is the real quality-gate file?"**
→ Run: `grep -r "class.*GateScore" src/`

### **"I don't understand the hook code"**
→ Copy the code from INTEGRATION-EXAMPLES.py + read docstrings

### **"My tests are failing"**
→ Check: src/shared/coaches/INTEGRATION-EXAMPLES.py TEST_* sections

### **"I need the design details"**
→ Read: docs/COACH-INTEGRATION-BLUEPRINT.md (search for your specific question)

---

## 🎯 THE BIG PICTURE

What you're doing in Sprint 1:

```
┌─────────────────────────────────────────────────────────┐
│ COACH SYSTEM                                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ 1. Telemetry Hook (Week 1)                             │
│    └─→ Captures what agents are doing                  │
│        └─→ Stores events: .coach/telemetry/*.jsonl     │
│                                                         │
│ 2. Anti-Pattern Detection (Week 2)                     │
│    └─→ Analyzes events for 6 known anti-patterns      │
│        └─→ Adjusts GateScore automatically            │
│                                                         │
│ 3. Dashboard (Week 2)                                  │
│    └─→ Visualizes metrics + patterns                  │
│        └─→ Shows team progress + improvements         │
│                                                         │
│ RESULT: Waves improve iteratively with feedback ✅    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 📋 FINAL CHECKLIST: Ready for Sprint 1?

### By Jun 25 Kickoff:

**Leadership:**
- [ ] Read strategy doc
- [ ] Approved Sprint 1

**PM/Lead:**
- [ ] Week 1 owner assigned
- [ ] Week 2 owner assigned
- [ ] Kickoff meeting scheduled
- [ ] Daily standups confirmed

**Team:**
- [ ] Python imports verified
- [ ] Understood 3 decisions
- [ ] Know Week 1 + Week 2 tasks
- [ ] Calendar blocked (Jun 25 – Jul 5)
- [ ] Code examples copied

**Infrastructure:**
- [ ] .coach/ directory exists
- [ ] telemetry-schema.json in place
- [ ] Python path correct

**Documentation:**
- [ ] Can find all 6 COACH-*.md files
- [ ] Can find INTEGRATION-EXAMPLES.py
- [ ] Can find .coach/SPRINT-1-KICKOFF-GUIDE.md

**If all checked: You're ready! 🚀**

---

## 🎬 GO TIME!

```
╔════════════════════════════════════════════════════════╗
║                                                        ║
║  EVERYTHING IS READY FOR SPRINT 1                     ║
║                                                        ║
║  Phase 1: ✅ COMPLETE                                 ║
║  - Strategic analysis done                            ║
║  - 3 decisions locked in                              ║
║  - 15 files delivered                                 ║
║  - Code written + tested                              ║
║  - Documentation complete                             ║
║                                                        ║
║  Sprint 1: 🚀 STARTS JUN 25                           ║
║  - Week 1: Telemetry hook                             ║
║  - Week 2: GateScore + Dashboard                      ║
║  - Jul 5: Delivery                                    ║
║                                                        ║
║  Your mission (if you accept it):                     ║
║  1. Read docs (today)                                 ║
║  2. Assign owners (today)                             ║
║  3. Schedule kickoff (today)                          ║
║  4. Start Sprint 1 (Jun 25)                           ║
║  5. Deliver by Jul 5 ✅                               ║
║                                                        ║
║  Questions? See COACH-DOCUMENTATION-INDEX.md          ║
║                                                        ║
║  LET'S GO! 🚀                                         ║
║                                                        ║
╚════════════════════════════════════════════════════════╝
```

---

**Questions?** See [docs/COACH-DOCUMENTATION-INDEX.md](./docs/COACH-DOCUMENTATION-INDEX.md)  
**Need code?** See [src/shared/coaches/INTEGRATION-EXAMPLES.py](./src/shared/coaches/INTEGRATION-EXAMPLES.py)  
**Need tasks?** See [.coach/SPRINT-1-KICKOFF-GUIDE.md](./.coach/SPRINT-1-KICKOFF-GUIDE.md)  

**Status:** ✅ Phase 1 Complete | 🚀 Ready to Go  
**Created:** 2026-06-18  
**Owner:** DMF Coach Team
