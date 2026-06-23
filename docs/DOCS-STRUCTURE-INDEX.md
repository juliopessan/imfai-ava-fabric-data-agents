# 📚 DMF Documentation Structure

**Last Updated:** 2026-06-18  
**Status:** ✅ Organized by Theme

---

## 📁 Directory Organization

```
docs/
├── coach/                           🤖 DMF Coach (AI Tutor System)
│   ├── COACH-COMO-TUTOR-BOAS-PRATICAS.md
│   ├── COACH-DECISIONS-APPROVED.md
│   ├── COACH-INTEGRATION-BLUEPRINT.md
│   ├── COACH-IMPLEMENTATION-SUMMARY.md
│   ├── COACH-PHASE-1-COMPLETE.md
│   ├── COACH-DOCUMENTATION-INDEX.md
│   └── README.md
│
├── implementation/                  🏗️ Implementation & Engineering
│   ├── IMPLEMENTATION-GUIDE-AGENTIC-ENGINEERING.md
│   ├── HUMAN-AGENT-CHECKPOINTS.md
│   └── README.md
│
├── observability/                   📊 Observability & Monitoring
│   ├── OBSERVABILITY-AND-TRACES.md
│   └── README.md
│
├── harness/                         🔄 CI/CD & Deployment
│   ├── HARNESS-CHANGELOG.md
│   ├── HARNESS-MANIFEST.md
│   └── README.md
│
├── governance/                      ✅ Governance & Audits
│   ├── AUDIT-REPORT-2026-06-16.md
│   ├── REPOSITORY-REORGANIZATION-COMPLETE-2026-06-16.md
│   └── README.md
│
├── sessions/                        📝 Session Notes & Learnings
│   ├── SESSION-SUMMARY-2026-06-18.md
│   └── README.md
│
├── _templates/                      📋 Templates & Examples
│   ├── DESIGN-TOKENS.css
│   ├── ORANGE-DNA-DESIGN-SYSTEM.md
│   ├── BRAND-GUIDELINES.md
│   ├── dashboards/
│   ├── scripts/
│   └── README.md
│
├── project-plans/                   📅 Project Planning
│   ├── CLIENTEBANCO-TIER1-EXECUTION-PLAN.md
│   ├── CLIENTEBANCO-TIER1-VALIDATION-REPORT.md
│   ├── GAP-ANALYSIS-REPORT.md
│   ├── PROJECT-COMPLETION-SUMMARY.md
│   └── README.md
│
├── reports/                         📊 Reports & Analysis
│   ├── CLEANUP-REPORT.md
│   ├── FINAL-INTEGRATION-REPORT.md
│   ├── TIER1-COMPLETION-REPORT.md
│   └── README.md
│
├── README.md                        🏠 Main Documentation Index
└── DOCS-STRUCTURE-INDEX.md          📍 This File
```

---

## 🎯 Quick Navigation

| Folder | Theme | Purpose | Owner |
|--------|-------|---------|-------|
| **coach/** | 🤖 AI Tutor | Coach system design & integration | Coach Team |
| **implementation/** | 🏗️ Engineering | Implementation guides & checkpoints | Architecture |
| **observability/** | 📊 Monitoring | Traces, telemetry, monitoring | DevOps |
| **harness/** | 🔄 CI/CD | Build pipelines, deployment | DevOps |
| **governance/** | ✅ Quality | Audits, compliance, reorganization | QA |
| **sessions/** | 📝 Knowledge | Session notes, learnings, decisions | Team |
| **_templates/** | 📋 Assets | Design tokens, brand, templates | Design |
| **project-plans/** | 📅 Planning | Wave plans, execution, validation | PM |
| **reports/** | 📊 Analysis | Reports, metrics, completion | Analytics |

---

## 📖 What's in Each Folder

### **coach/** 🤖 DMF Coach System
- Strategic guides (PT-BR + EN)
- Design & integration architecture (42 sections)
- Implementation summary & checklist
- Documentation index for navigation
- **Best for:** Understanding Coach as AI tutor, Sprint 1 planning

### **implementation/** 🏗️ Implementation & Engineering
- Agentic engineering implementation guide
- Human-agent checkpoint system
- Development best practices
- **Best for:** Developers building agentic features

### **observability/** 📊 Observability & Monitoring
- Traces and tracing setup
- Telemetry collection guides
- Monitoring standards
- **Best for:** DevOps, performance monitoring, debugging

### **harness/** 🔄 CI/CD & Deployment
- Harness pipeline changelog
- Harness deployment manifest
- CI/CD integration patterns
- **Best for:** DevOps, release management

### **governance/** ✅ Governance & Audits
- Audit reports (compliance, quality)
- Repository reorganization records
- Governance policies
- **Best for:** Compliance, quality assurance, risk management

### **sessions/** 📝 Session Notes & Learnings
- Session summaries & decisions
- Lessons learned (append-only log)
- Team insights & patterns
- **Best for:** Team knowledge base, decision history

### **_templates/** 📋 Templates & Examples
- Design system (Orange DNA)
- Brand guidelines
- Dashboards templates
- Code examples & scripts
- **Best for:** Designers, documentation, standardization

### **project-plans/** 📅 Project Planning
- Wave execution plans (ClienteBanco, ClienteSaude, etc.)
- Validation reports
- Gap analysis
- Completion summaries
- **Best for:** PMs, project tracking, wave execution

### **reports/** 📊 Reports & Analysis
- Cleanup reports
- Integration reports
- Completion metrics
- Analysis dashboards
- **Best for:** Leadership, metrics review, status updates

---

## 🚀 How to Use This Structure

### **For Executives**
```
→ reports/              (Current status & metrics)
→ project-plans/        (Timeline & milestones)
→ coach/README.md       (Strategic initiatives)
```

### **For PMs / Team Leads**
```
→ project-plans/        (Wave plans & execution)
→ sessions/             (Decisions & learnings)
→ governance/           (Audit results & compliance)
```

### **For Developers**
```
→ implementation/       (Engineering guides)
→ coach/               (Coach system details)
→ observability/       (Tracing & monitoring)
→ _templates/          (Code examples)
```

### **For DevOps**
```
→ harness/             (CI/CD configuration)
→ observability/       (Monitoring setup)
→ governance/          (Compliance checks)
```

### **For Architects**
```
→ coach/               (Design blueprints)
→ implementation/      (Architecture patterns)
→ project-plans/       (System design integration)
```

---

## 📝 README Files in Each Folder

Each folder contains a **README.md** with:
- Folder purpose & contents
- What files belong here
- Who owns this section
- How to add new files
- Links to related folders

**Example:** `coach/README.md` explains:
- What Coach is
- Which files to read first
- Who manages Coach docs
- Sprint 1 getting started

---

## 🔄 File Organization Rules

### **When Adding a New File**
1. **Determine the theme** (coach, implementation, observability, etc.)
2. **Place it in the appropriate folder**
3. **Update the folder's README.md**
4. **Update this index if needed**

### **Theme Matching**
- Contains "COACH" → `coach/`
- Contains "IMPLEMENTATION" or "GUIDE" → `implementation/`
- Contains "TRACE" or "OBSERVABILITY" → `observability/`
- Contains "HARNESS" → `harness/`
- Contains "AUDIT" or "GOVERNANCE" → `governance/`
- Contains "SESSION" or "SUMMARY" → `sessions/`
- Contains "REPORT" → `reports/`
- Contains "PLAN" → `project-plans/`

---

## 📊 Statistics

| Folder | Files | Focus |
|--------|-------|-------|
| coach/ | 6 | AI Tutor System |
| implementation/ | 2 | Engineering |
| observability/ | 1 | Monitoring |
| harness/ | 2 | CI/CD |
| governance/ | 2 | Quality |
| sessions/ | 1 | Knowledge |
| _templates/ | 20+ | Design Assets |
| project-plans/ | 5+ | Planning |
| reports/ | 10+ | Analysis |
| **Total** | **~50+** | **All Topics** |

---

## 🎯 Navigation Commands

### **Quick Find**
```bash
# Find Coach docs
ls docs/coach/

# Find all implementation guides
ls docs/implementation/

# Find reports
ls docs/reports/

# Find by filename pattern
grep -r "COACH" docs/coach/
grep -r "IMPLEMENTATION" docs/implementation/
```

### **Search Content**
```bash
# Search across all docs
grep -r "GateScore" docs/

# Search in specific folder
grep -r "telemetry" docs/observability/

# Search with context
grep -r "anti-pattern" docs/coach/ -A 3 -B 1
```

---

## 🔗 Cross-Folder References

Some documents reference others across folders:

```
coach/COACH-INTEGRATION-BLUEPRINT.md
  ↓ references
observability/OBSERVABILITY-AND-TRACES.md

implementation/IMPLEMENTATION-GUIDE-AGENTIC-ENGINEERING.md
  ↓ references
coach/COACH-DECISIONS-APPROVED.md

harness/HARNESS-MANIFEST.md
  ↓ references
governance/AUDIT-REPORT-2026-06-16.md
```

Use the **README.md in each folder** to find related documents.

---

## 📚 Related Root-Level Files

These files are in the root of `/docs` and referenced from all folders:

- **README.md** — Main documentation portal
- **DOCS-STRUCTURE-INDEX.md** — This file (navigation map)

---

## ✅ Folder Readiness

| Folder | Status | README | Examples |
|--------|--------|--------|----------|
| coach/ | ✅ Ready | ✅ Yes | ✅ Yes |
| implementation/ | ✅ Ready | ✅ Yes | ✅ Yes |
| observability/ | ✅ Ready | ✅ Yes | 🔵 Soon |
| harness/ | ✅ Ready | ✅ Yes | 🔵 Soon |
| governance/ | ✅ Ready | ✅ Yes | ✅ Yes |
| sessions/ | ✅ Ready | ✅ Yes | ✅ Yes |
| _templates/ | ✅ Ready | ✅ Yes | ✅ Yes |
| project-plans/ | ✅ Ready | ✅ Yes | ✅ Yes |
| reports/ | ✅ Ready | ✅ Yes | ✅ Yes |

---

## 🚀 Next Steps

1. **Read** the README.md in your folder of interest
2. **Search** for related documents using grep commands above
3. **Add** new documents following the organization rules
4. **Update** this index when adding new themes

---

**Status:** ✅ Organized | 📍 Ready for Use  
**Created:** 2026-06-18 | **Last Updated:** 2026-06-18  
**Owner:** Documentation Team

Questions? See the **README.md** in each folder.
