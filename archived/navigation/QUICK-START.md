# 🚀 Quick Start — Data Migration Factory

**Get up & running in 5 minutes.**

---

## 1️⃣ Setup Environment (2 min)

```powershell
# Navigate to repo root
cd c:\Users\julio.cesar.d.pessan\Downloads\imfai-ava-fabric-data-agents

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install dependencies (if not already done)
pip install -r config/requirements-dev.txt
```

---

## 2️⃣ Run a Case Study (choose one)

### Option A: Financeiro Migration
```powershell
# Execute the complete migration pipeline
python projects/Financeiro/scripts/00_MASTER_PIPELINE.py
```

### Option B: Reference-Saúde KPI Portal
```powershell
# Generate the KPI portal with real legacy metrics
python projects/Reference-Sa�de/scripts/generate_kpi_portal.py
```

**When done, you'll see:**
- ✓ Artifacts generated
- ✓ Portal/dashboards created
- ✓ Outputs consolidated in outputs/
- ✓ Summary reports generated

---

## 3️⃣ View Dashboards (choose project)

### Financeiro Dashboard
```powershell
python -m http.server 8000 --directory projects/Financeiro/outputs
# Open: http://localhost:8000/00_CONSOLIDATED_MIGRATION_REPORT_tabbed.html
```

### Reference-Sa�de KPI Portal
```powershell
python -m http.server 8000 --directory projects/Reference-Sa�de/outputs
# Open: http://localhost:8000/KPI_PORTAL_MASTER.html
```

**What you'll see:**
- 📊 Interactive dashboards
- 📈 Real-time KPI metrics
- 🎨 Avanade Orange DNA branding
- 🌍 Bilingual interface (EN/PT)
- ✅ Production-ready analytics

---

## 4️⃣ Run Tests (1 min)

```powershell
# Run all 189 tests
python -m pytest src/shared/tests/ -q

# Expected output:
# 189 passed ✓
```

---

## 5️⃣ Explore Docs (Optional)

- **Master Index:** [`INDEX.md`](INDEX.md)
- **Financeiro Case:** [`projects/Financeiro/README.md`](projects/Financeiro/README.md)
- **Multi-Platform Wave:** [`projects/multi-platform-migration/README.md`](projects/multi-platform-migration/README.md)
- **Memory System:** [`/memories/repo/MEMORY-INDEX.md`](/memories/repo/MEMORY-INDEX.md)

---

## 🎯 What's Next?

| Goal | Location |
|------|----------|
| **Understand Financeiro workflow** | [`projects/Financeiro/WORKFLOW_AND_ARCHITECTURE.md`](projects/Financeiro/WORKFLOW_AND_ARCHITECTURE.md) |
| **Learn Reference-Sa�de portal** | [`projects/Reference-Sa�de/README.md`](projects/Reference-Sa�de/README.md) |
| **View file locations** | [`REPOSITORY-QUICK-REFERENCE.md`](REPOSITORY-QUICK-REFERENCE.md) |
| **Learn about 6-platform wave** | [`projects/multi-platform-migration/README.md`](projects/multi-platform-migration/README.md) |
| **Add a new migration case** | Copy any project folder → `projects/[new-name]/` with same structure |
| **Review repository organization** | [`REPOSITORY-ORGANIZATION.md`](REPOSITORY-ORGANIZATION.md) |
| **Validate structure** | Run: `python validate_repo_structure.py` |

---

## 🆘 Issues?

| Issue | Fix |
|-------|-----|
| Command not found | Run `.\.venv\Scripts\Activate.ps1` first |
| Permission denied | Run: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned` |
| Missing dependencies | Run: `pip install -r config/requirements-dev.txt` |

---

**💡 Tip:** Bookmark [`INDEX.md`](INDEX.md) — it's your navigation hub for everything in this repository.

**Ready?** Start with Step 1️⃣ above!
