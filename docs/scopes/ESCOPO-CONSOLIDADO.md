# 📊 CONSOLIDAÇÃO: FINANCEIRO + SAÚDE — ROADMAP UNIFICADO

**Data:** 2026-06-26  
**Escopo:** Análise comparativa e planejamento integrado de migração  
**Status:** ✅ Finalizado

---

## 🎯 RESUMO EXECUTIVO (2 PROJETOS)

### Por Números

| Métrica | Financeiro | Saúde | Total | % Saúde |
|---------|-----------|-------|-------|---------|
| **Arquivos** | 795 | 166 | 961 | 17.3% |
| **Tamanho** | 43.67 MB | 153.38 MB | 197.05 MB | 77.8% |
| **Tokens (bruto)** | ~11.4M | ~40.2M | ~51.6M | 77.8% |
| **Tokens (overhead)** | ~15M | ~52.3M | ~67.3M | 77.8% |
| **Entidades BD** | 103 | 27 | 130 | 20.8% |
| **Scripts** | 98 | 11 | 109 | 10.1% |

### Complexidade vs. Token Burn

| Projeto | Arquivos | Token Burn | Complexity | Priority |
|---------|----------|-----------|-----------|----------|
| **Financeiro** | 795 | ~700k | 🔴 ALTA | 1️⃣ Critical |
| **Saúde** | 166 | ~410k | 🟠 MÉDIA-ALTA | 2️⃣ High |
| **TOTAL** | 961 | ~1.11M | 🔴 ALTA | Combined |

---

## 📋 DETALHAMENTO POR PROJETO

### FINANCEIRO (🔴 CRÍTICO)

**Escopo:**
- 795 arquivos | 43.67 MB
- 103 entidades (8 SQL + 92 Hive + 1 proc + 2 views)
- 98 scripts (22 reproc + 76 outros)

**Stack Legado:**
- Hive/HDFS (92 scripts) → Spark
- SSIS (75 packages) → Data Factory
- PowerCenter (workflows customizados)
- Teradata + TDCH
- Pickles (23.77 MB binary)

**Token Budget: ~700k**
- Discovery: 50-200k
- Design: 250-350k
- Execution: 150-250k

**Criticality:** 🔴 Core Financial (rentabilidade)

---

### SAÚDE (🟠 MÉDIO-ALTO)

**Escopo:**
- 166 arquivos | 153.38 MB
- 27 schemas SQL (367,513 linhas)
- 5 DAGs Airflow (11 tasks)

**Stack Moderno:**
- SQL Server DW → Fabric DW
- Airflow → Data Factory
- EMR (AWS) → Spark on Fabric (CROSS-CLOUD)
- Medallion architecture (Raw → Curated → Gold → Public)

**Token Budget: ~410k**
- Discovery: 30-50k
- SQL+Airflow: 100-130k
- Design: 150-200k
- Execution: 50-100k

**Criticality:** 🟠 Healthcare (regulated, LGPD/GDPR)

---

## 🔄 COMPARATIVO DETALHADO

### Estrutura e Complexidade

```
FINANCEIRO                          SAÚDE
════════════════════════════════════════════════════════════

Arquivos Pequenos:                  Arquivos Grandes:
  • 234 shell scripts                 • 113 ZIP archives (78%)
  • 104 Python files                  • 27 SQL schemas (367k lines)
  • 92 Hive SQL scripts               • 5 Airflow DAGs

Stack: Multi-legacy                 Stack: Cloud-native+Cross-cloud
  • Hive + SSIS + PowerCenter         • SQL Server + Airflow + EMR
  • Teradata + TDCH                   • Medallion layers
  • Legacy orchestration              • Docker infrastructure

Interdependencies:                  Straightforward Dependencies:
  • 22 reproc scripts (cascading)    • SQL schema relationships
  • Complex workflows                • Linear DAG flows
```

### Risk Profile

```
FINANCEIRO 🔴 CRÍTICO              SAÚDE 🟠 MÉDIO-ALTO
─────────────────────────────────────────────────────

Hive → Spark translation (92 files) EMR → Fabric (cross-cloud)
SSIS → Data Factory (75 packages)   Airflow → Data Factory
PowerCenter mapping                 SQL Server → Fabric DW
Reproc cascading logic              Schema interdependencies
Binary pickle conversion            Medical data sensitivity
```

---

## 🏗️ UNIFIED ROADMAP (1.11M tokens total)

### Phase 1: DISCOVERY & INVENTORY (80-250k tokens)

**Parallel Execution:**

| Activity | Fin | Saúde | Duration | Tokens |
|----------|-----|-------|----------|--------|
| Inventory scan | 50k | 30k | Week 1 | 80k |
| SQL/Hive analysis | 100k | 100k | Week 1-2 | 200k |
| Dependency mapping | 50k | 30k | Week 2 | 80k |
| **Subtotal** | **200k** | **160k** | | **360k** |

**Deliverables:**
- Complete file inventory (961 files cataloged)
- Entity-relationship diagrams (130 entities mapped)
- Risk register per project
- Cross-project dependency graph

---

### Phase 2: DESIGN & ARCHITECTURE (300-400k tokens)

**Sequential (Design → Validation):**

| Activity | Fin | Saúde | Tokens |
|----------|-----|-------|--------|
| Fin: Hive → Spark design | 150k | — | 150k |
| Fin: SSIS → Data Factory design | 100k | — | 100k |
| Saúde: EMR → Fabric cross-cloud | — | 150k | 150k |
| Saúde: Airflow → Data Factory | — | 80k | 80k |
| Data model + contracts | 50k | 50k | 100k |
| **Subtotal** | **300k** | **280k** | **580k** |

**Deliverables:**
- Architecture decision records (ADRs)
- Target data models (Fabric semantic layer)
- Data contracts + quality rules
- Migration wave plan (1-3 waves per project)

---

### Phase 3: EXECUTION (200-300k tokens)

**Parallel Implementation:**

| Component | Fin | Saúde | Tokens |
|-----------|-----|-------|--------|
| Infrastructure (Bicep/Terraform) | 50k | 50k | 100k |
| Code generation + deployment | 150k | 100k | 250k |
| Testing + validation | 100k | 50k | 150k |
| Documentation + runbooks | 50k | 30k | 80k |
| **Subtotal** | **350k** | **230k** | **580k** |

**Deliverables:**
- Deployed infrastructure
- Migrated data pipelines
- Test suite + reconciliation reports
- Operational runbooks

---

## 🎯 SEQUENCING STRATEGY

### Option A: Financeiro First (Critical Path)
```
Phase 1: Fin Discovery (50-200k) ─┐
                                   ├─→ Phase 2: Fin Design (300k)
Phase 1: Saúde Discovery (30-50k) ┤      ↓
                                   ├─→ Phase 3: Fin Execution (200-250k)
                                   │
                                   └─→ Phase 2: Saúde Design (280k)
                                          ↓
                                       Phase 3: Saúde Exec (100-150k)
```
**Total Duration:** 5-6 months  
**Total Tokens:** ~1.11M  
**Risk:** High initial critical path dependency

---

### Option B: Parallel Discovery (Recommended)
```
WEEK 1-2: DISCOVERY (Both parallel)
  Fin: 50k  +  Saúde: 30k  =  80k

WEEK 3-6: DESIGN (Staggered)
  Fin Design: 300k (starts week 3)
  ↓ (week 5)
  Saúde Design: 280k (starts week 5)

WEEK 7-12: EXECUTION (Parallel if possible)
  Fin Exec: 200-250k (starts week 7)
  Saúde Exec: 100-150k (starts week 9)
```
**Total Duration:** 12 weeks  
**Total Tokens:** ~1.11M  
**Risk:** Balanced, both projects progress in parallel

---

## 💰 TOKEN BUDGET ALLOCATION

### Total Pot: 1.11M tokens

```
Discovery (Upstream)           360k  (32%)
├─ Financeiro              200k
├─ Saúde                   160k
└─ Reserve                  20k

Design (Midstream)           580k  (52%)
├─ Financeiro              300k
├─ Saúde                   280k
└─ Reserve                  50k

Execution (Downstream)       170k  (16%)
├─ Financeiro               85k
├─ Saúde                    85k
└─ Reserve                  20k

TOTAL                     1,110k (100%)
```

**Burn Rate by Phase:**
- Phase 1: 360k tokens / 2-3 weeks = 120-180k/week
- Phase 2: 580k tokens / 4-6 weeks = 97-145k/week
- Phase 3: 170k tokens / 6-8 weeks = 21-28k/week

---

## ⚠️ CRITICAL SUCCESS FACTORS

### Financeiro
1. ✅ **Hive → Spark translation** (92 scripts)
2. ✅ **SSIS → Data Factory mapping** (75 packages)
3. ✅ **PowerCenter workflow reverse-engineering**
4. ✅ **Reproc cascade dependency resolution**

### Saúde
1. ✅ **Cross-cloud migration** (EMR/AWS → Azure/Fabric)
2. ✅ **Healthcare data compliance** (LGPD/GDPR)
3. ✅ **Airflow → Data Factory orchestration**
4. ✅ **Medallion architecture preservation**

### Both
1. ✅ **Quality gates** (Gate 1/2/3 validation)
2. ✅ **Reconciliation** (row counts, checksums, schema diffs)
3. ✅ **Knowledge transfer** (runbooks, documentation)
4. ✅ **Schedule adherence** (avoid token overruns)

---

## 📈 SUCCESS METRICS

### Financeiro
- [ ] All 103 entities migrated
- [ ] 92 Hive scripts converted to Spark
- [ ] 75 SSIS packages → Data Factory
- [ ] GateScore ≥ 0.85 (Gate 2)

### Saúde
- [ ] All 27 schemas migrated
- [ ] 5 DAGs running in Data Factory
- [ ] EMR data → Fabric Spark validated
- [ ] GateScore ≥ 0.85 (Gate 2)

### Combined
- [ ] <10% reconciliation variance
- [ ] 0 data quality rule violations
- [ ] All stakeholders trained
- [ ] Go-live ready

---

## 📊 FILES GENERATED

✅ **FINANCEIRO-ESCOPO-TOKENS.md** (comprehensive)  
✅ **SAUDE-ESCOPO-TOKENS.md** (comprehensive)  
✅ **ESCOPO-CONSOLIDADO.md** (this file)  

**Supporting Scripts:**
- `analyze_financeiro.py` / `analyze_saude.py`
- `analyze_financeiro_detailed.py` / `analyze_saude_detailed.py`
- `report_token_summary.py` / `report_saude_summary.py`

---

## 🚀 NEXT STEPS

1. **Approve Sequencing:** Option A (Fin first) or Option B (Parallel)?
2. **Allocate Token Budget:** 1.11M tokens OK?
3. **Assign Wave Champions:** discovery-scout, data-architect, etc.
4. **Schedule Kickoff:** Week 1 discovery starts
5. **Set Up Monitoring:** Gate 1 artifact validation, token tracking

---

**Data:** 2026-06-26  
**Status:** Ready for Phase 1 Kickoff  
**Next Review:** 2026-06-30 (Phase 1 progress)
