# 🤝 Coordination — Notas Técnicas Compartilhadas

**Última atualização:** 2026-06-26 | **Status:** Active Collaboration

---

## 📌 Key Points

### Remotes
```
ssh-github → GitHub (juliopessan/imfai-ava-fabric-data-agents)
ssh-azure  → Azure DevOps (IMFAI organization)
origin     → Current HTTPS remote (temporary)
```

### Branch Structure
```
main (production) ← Stable releases
  ↓
Dev (staging) ← Integration test
  ↓
trabalho-backlog (collaborative) ← You are here ← All work happens
```

---

## 🔗 Integration Points

### Headroom System (Phase 1 Starting 2026-06-22)
- **Feature:** Token compression for agent handoffs
- **Branch:** `feature/headroom-p1`
- **Owner:** TBD
- **Docs:** `.github/BACKLOG-COLLABORATION.md` (top-level)
- **Integration:** `src/shared/scripts/` → `src/modules/core-coordination/migration-coordinator.py`

### Token Metrics System (Existing)
- **Location:** `src/shared/scripts/token_metrics_collector.py`
- **Already integrated:** Dashboard generation in `src/shared/scripts/generate_telemetry_dashboard.py`
- **Coordinate with:** Anyone working on instrumentation

### Migration Coordinator (Core)
- **Location:** `src/modules/core-coordination/migration-coordinator.py`
- **Update frequency:** Daily (if touching)
- **Breaking changes:** Announce in #backlog-channel

---

## 🛠️ Shared Tools & Utilities

### Available in `.backlog/shared/`

**None yet — add your reusable code here:**

```python
# Example: .backlog/shared/my_utility.py
def shared_function(...):
    """Reusable function for team to use."""
    ...

# Document in SHARED-UTILITIES.md
# Team can import: 
#   sys.path.insert(0, '.backlog/shared')
#   from my_utility import shared_function
```

---

## 📊 Environments & Access

### Local Development
```
C:\Users\julio.cesar.d.pessan\Downloads\imfai-ava-fabric-data-agents
Python: .venv (activated)
Tests: pytest (run in terminal)
```

### Shared Infrastructure
- GitHub: https://github.com/juliopessan/imfai-ava-fabric-data-agents (pull requests)
- Azure DevOps: IMFAI org (backlog, pipelines - when available)

---

## 🔐 Credentials & Access

### Current Setup
- **GitHub:** HTTPS (configured)
- **Azure DevOps:** HTTPS with PAT (configured)
- **SSH:** Not yet configured (ready when needed)

### Add SSH (When Available)

See `.github/BACKLOG-COLLABORATION.md` — "SSH Setup" section

---

## 📈 Performance Baselines

### For Optimization Work

**Current (as of 2026-06-25):**
```
Headroom Orchestrator (Parallel):
- Execution time: 0.16 seconds
- Tokens: 2,644
- Compression: 91.8%
- GateScore: 0.9543
```

**Target (Phase 1):**
```
- Maintain performance
- Reduce tokens by 75-90% (via Headroom)
- Cache hit rate > 90%
```

---

## 🎯 Milestones & Dependencies

### Phase 1 Dependencies (Starting 2026-06-22)

| Work | Depends On | Status |
|------|-----------|--------|
| Headroom P1 | Migration-Coordinator ✅ | Ready |
| Metrics Dashboard | Token Metrics ✅ | Ready |
| Testing | PoC validation ✅ | Done |

### No Blocking Issues
All dependencies resolved. Team can start immediately.

---

## 💬 Communication

### Channels
- **Daily:** #trabalho-backlog (09:00 standup)
- **Technical:** #headroom-implementation (feature-specific)
- **Escalations:** @architecture-team or Lead

### Async Communication
- GitHub PRs (for code review)
- Commit messages (must be descriptive)
- STATUS.md files (updates per feature)

---

## 🚨 Known Constraints

### Microsoft-Only Stack
- ✅ Azure services only
- ✅ OpenAI via Azure, not public API
- ✅ No LangChain, Datadog, or non-Microsoft tools
- See `.github/copilot-instructions.md` for full list

### Performance Constraints
- Execution time < 2 seconds (target)
- Memory < 512 MB per agent
- Token budget: $0.01-0.05 per workflow

---

## 📚 Documentation Sources

| Doc | Purpose | Location |
|-----|---------|----------|
| This file | Technical coordination | `.backlog/COORDINATION.md` |
| Sync Protocol | How to sync | `.backlog/SYNC-PROTOCOL.md` |
| Assignments | Who works on what | `.backlog/ASSIGNMENTS.md` |
| Merge Checklist | Pre-merge validation | `.backlog/MERGE-CHECKLIST.md` |
| Feature Status | Per-feature progress | `.backlog/features/*/STATUS.md` |
| Backlog Guide (Top-Level) | Full overview | `.github/BACKLOG-COLLABORATION.md` |

---

## 🔄 Weekly Review

**Every Friday 17:00:**
- Review all feature STATUS.md files
- Promote complete features to Dev
- Plan next week's work
- Update ASSIGNMENTS.md

---

## ⚡ Quick Commands

```bash
# Status check
git status
git log --oneline -5

# Sync with team
git fetch ssh-github trabalho-backlog

# Start new feature
git checkout -b feature/your-name trabalho-backlog

# Daily push
git push ssh-github feature/your-name

# Ready for merge
# → Verify MERGE-CHECKLIST.md
# → Create PR on GitHub
```

---

## 🆘 Troubleshooting

### "SSH not available" → Use HTTPS (current setup)
```bash
git push origin feature/your-name  # Will work until SSH ready
```

### "Conflicts on merge" → Rebase first
```bash
git fetch ssh-github trabalho-backlog
git rebase ssh-github/trabalho-backlog
```

### "Lost commits?" → Check reflog
```bash
git reflog
git checkout <commit-id>
```

---

## 📞 Points of Contact

| Topic | Contact | Channel |
|-------|---------|---------|
| Headroom Technical | TBD | #headroom-impl |
| Metrics Integration | Data Analyst | #metrics |
| Git/Workflow | Tech Lead | #backlog-channel |
| Architecture Questions | @architecture-team | #architecture |

---

**Last Sync:** 2026-06-26 09:00  
**Next Review:** 2026-06-28 (Friday)  
**Status:** 🟢 All systems ready for collaboration

---

Questions? Check other `.backlog/` files or ask in team channels.
