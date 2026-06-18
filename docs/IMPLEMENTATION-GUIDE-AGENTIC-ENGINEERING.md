# Implementation Guide — DMF v3 Agentic Engineering

**Date:** 2026-06-16  
**Status:** Recommendations → Ready for Implementation  
**Based On:** "The New SDLC with Vibe Coding" (Google, May 2026)  

---

## 🎯 Executive Summary

Implementamos **5 recomendações estruturais** que transformam DMF de "agentes que fazem coisas" para "sistema de engenharia agentic disciplinado":

1. ✅ **Harness Manifest** → Formaliza o harness como artefato versionado
2. ✅ **Harness Changelog** → Rastreia impacto de mudanças
3. ✅ **Observability & Traces** → Root cause analysis + cost attribution
4. ✅ **Human-Agent Checkpoints** → Escalation automática baseada em confiança
5. ✅ **Wave Config Extended** → Skills versionadas + Specs executáveis
6. ✅ **Spec-as-Executable** → Convertemos docs estáticos em validators

**Resultado:** De vibe coding → agentic engineering (Gate 1, 2, 3 completos).

---

## 📂 Arquivos Criados

### 1. HARNESS-MANIFEST.md
**Localização:** `docs/HARNESS-MANIFEST.md`  
**Propósito:** Documentação formal do Harness como primeira-classe citizen.

**Contém:**
- 6 componentes de harness (Instructions, Tools, Sandboxes, Orchestration, Guardrails, Observability)
- Mapeamento de componentes per gate (1, 2, 3)
- Políticas de governança (No vibe coding em prod; Skills versioning; Context Rot Detection)
- Harness-as-Code (yaml schema)
- Adoption checklist

**Ação Imediata:**
```bash
# 1. Review com time (arquitetos, SRE)
# 2. Refine guardrails & policies com contexto real
# 3. Approve harness v1.0.0 formalmente
```

---

### 2. HARNESS-CHANGELOG.md
**Localização:** `docs/HARNESS-CHANGELOG.md`  
**Propósito:** Append-only log de todas as mudanças de harness com rationale.

**Contém:**
- 6 mudanças já documentadas (2026-06-16)
  - Harness Formalization
  - Skills Versioning
  - Trajectory Evals
  - Distributed Traces
  - Human-Agent Checkpoints
  - Context Rot Audit
- Template para futuras mudanças
- Summary table

**Ação Imediata:**
```bash
# 1. Git add + commit: "Harness v1.0.0 formalized"
# 2. Exigir changelog entry para cada mudança de harness (como SDD review)
# 3. Monthly audit: flag se static context > 25 KB
```

---

### 3. OBSERVABILITY-AND-TRACES.md
**Localização:** `docs/OBSERVABILITY-AND-TRACES.md`  
**Propósito:** Instrumentação completa com trace IDs, span schemas, cost attribution.

**Contém:**
- Trace ID propagation architecture
- TraceContext dataclass (Python)
- 5 tipos de spans (Agent, LLM Call, Tool, Sub-Agent, Decision)
- Observability pipeline (generation → aggregation → dashboard)
- Cost attribution model
- Drift detection (baseline + alerts)
- Privacy & security (masking rules)
- 8-week implementation roadmap

**Ação Imediata:**
```bash
# Week 1: Implement TraceContext + propagation in orchestrator
# Week 2: Span collection in agent loop
# Week 3: Application Insights pipeline
# Week 4: PowerBI dashboard ("Agent Observatory")
# ... (see docs for full roadmap)
```

**Impacto:**
- 💰 Habilitamos cost attribution (saber quem gastou quanto)
- 🔍 Habilitamos root cause analysis (trace ID linking)
- 📊 Habilitamos drift detection (agent behavior change detection)

---

### 4. HUMAN-AGENT-CHECKPOINTS.md
**Localização:** `docs/HUMAN-AGENT-CHECKPOINTS.md`  
**Propósito:** Framework de escalation automática baseado em confiança (scores de evals).

**Contém:**
- Three-Tier Model (Auto-Approve > Tier 2 Human Review > Tier 3 Critical)
- Gate-specific escalation rules (Gate 1, 2, 3)
- EscalationEngine class (Python pseudocode)
- Routing matrix (qual humano revisar)
- Retry loop (agent pode tentar de novo após feedback)
- Audit trail (cada decisão logada)
- SLA management (60 min Tier 2, 15 min Tier 3)
- Metrics & reporting (weekly escalation report)

**Ação Imediata:**
```bash
# 1. Define eval score thresholds per gate (com SME input)
# 2. Implement EscalationEngine class
# 3. Set up Slack/Teams routing
# 4. Create audit trail table (CosmosDB or SQL)
# 5. Test retry loop em sandbox
# 6. Train on-call team
```

**Impacto:**
- 🟢 Auto-approve quando agent está confiante (output_quality > 0.85)
- 🟡 Escalate quando agent está incerto (0.70–0.85)
- 🔴 Block quando agent claramente quebrado (< 0.50)

---

### 5. wave-config-extended.yaml
**Localização:** `src/shared/schemas/wave-config-extended.yaml`  
**Propósito:** Schema estendido com skills versioning + specifications executáveis.

**Contém:**
- Wave metadata (arquiteto, discovery owner, steward, approvers)
- Harness configuration per wave
- **NEW: Skills versionadas** (ava-dmf-data-quality@v2.1.0)
  - Fallback versioning (se v2.1.0 indisponível, use v2.0.5)
- **NEW: Specifications section** (data contracts, DQ rules, acceptance criteria)
  - Entity scope (customer, transaction)
  - Data quality rules (executáveis)
  - Data contracts (formal reconciliation specs)
  - Performance targets (SLAs)
  - Security requirements
  - Acceptance criteria (por gate)
- Quality gates (approval criteria, escalation thresholds, timeouts)
- Agent orchestration (qual agent roda em qual ordem)
- Observability (tracing, metrics, dashboards, alerts)
- Deployment & rollback plan

**Ação Imediata:**
```bash
# 1. Usar como template para próximas waves
# 2. Validate com validate_wave_config.py
# 3. Atualizar exemplo (Bradesco) com dados reais
# 4. Implementar skills versioning no orchestrator
```

**Impacto:**
- 📌 Skills agora versionadas e pinned (não quebra waves antigas)
- 📋 Specifications são YAML (legível por humans e machines)
- ✅ Evals conseguem ler specs e validar automaticamente

---

### 6. spec-as-executable.md
**Localização:** `src/shared/schemas/spec-as-executable.md`  
**Propósito:** Converter specs estáticas em validators executáveis.

**Contém:**
- Data Contract Schema (YAML declarativo)
  - Business keys, columns, nullability, PII flags
  - Reconciliation specs (hash method, tolerances)
  - Quality rules (assertions em SQL)
  - Performance SLAs
- DataContractValidator (Python executável)
  - `validate_schema()` → Check target schema matches contract
  - `validate_quality_rules()` → Run SQL assertions
  - `validate_reconciliation()` → Compare source ↔ target
  - `validate_performance_sla()` → Check latency/throughput
  - `aggregate_score()` → Composite score
- Integration com Gate 3 (validator blocks deployment se critical failures)
- Before/After exemplo (spec document-driven vs. executable)

**Ação Imediata:**
```bash
# 1. Implement DataContractValidator class
# 2. Integrate into validate_gate3_artifacts.py
# 3. Test com mock source/target connections
# 4. Write data contracts YAML para Bradesco
# 5. Add "Spec Review" checklist para gate approvals
```

**Impacto:**
- 🤖 Specs não são mais documentos estáticos; são tests que rodam
- 🔒 Deployment blocks automaticamente se DQ rules falham
- 📈 Score agregado: schema(20%) + quality(30%) + reconciliation(30%) + performance(20%)

---

## 🔄 Integração Completa

```
┌─ Wave Config (wave-config-extended.yaml)
│  ├─ Harness configuration (tools, guardrails, sandbox)
│  ├─ Skills (versionadas!)
│  ├─ Specifications (data contracts + quality rules)
│  └─ Agent orchestration (sequência de agentes)
│
├─ HARNESS-MANIFEST.md
│  └─ Documenta o que É o harness (componentes, políticas)
│
├─ HARNESS-CHANGELOG.md
│  └─ Rastreia MUDANÇAS ao harness (por quê, impacto)
│
├─ OBSERVABILITY-AND-TRACES.md
│  ├─ TraceContext propagation
│  ├─ Span schemas (5 tipos)
│  ├─ Cost attribution (tokens + tool execution)
│  └─ Drift detection
│
├─ HUMAN-AGENT-CHECKPOINTS.md
│  ├─ EscalationEngine (Tier 1/2/3)
│  ├─ Gate-specific rules
│  ├─ SLA management
│  └─ Audit trail
│
└─ spec-as-executable.md
   ├─ Data contracts (YAML)
   └─ DataContractValidator (Python)
       └─ Rodapé Gate 3 validator (blocks deployment se fails)
```

---

## 📊 Mapeamento: Insights → Implementação

| Insight | Impl. | Docs | Impact | Owner |
|---------|------|------|--------|-------|
| Harness é 70% do comportamento | HARNESS-MANIFEST | Architecture | High | architect |
| Versionar skills independentemente | wave-config-extended | Orchestrator | Medium | agent-dev |
| Specs devem ser executáveis | spec-as-executable | Gate 3 | High | qa-lead |
| Context engineering (static vs. dynamic) | Wave config + skills | Orchestrator | Medium | agent-dev |
| Observability: traces + cost | OBSERVABILITY-AND-TRACES | SRE | High | sre-lead |
| Escalation rules (3 tiers) | HUMAN-AGENT-CHECKPOINTS | Process | High | process-owner |
| Trajectory evals (not just output) | HARNESS-CHANGELOG | Gate 3 | High | qa-lead |
| No vibe coding em production | All docs | Governance | High | cto |

---

## 🚀 Implementation Roadmap (4 Weeks)

### Week 1: Baseline & Harness Formalization
- [ ] Review HARNESS-MANIFEST.md com time
- [ ] Approve harness v1.0.0
- [ ] Document current state (13 tools, 21 agents, 26 skills)
- [ ] Add HARNESS-CHANGELOG.md ao README

**Deliverable:** Harness formalizado; baseline estabelecido.

### Week 2: Skills Versioning
- [ ] Implement skill versioning em `.github/skills/`
- [ ] Update wave-config schema (accept `skill@version`)
- [ ] Migrate Bradesco wave to new schema
- [ ] Test fallback logic (versão não disponível)

**Deliverable:** Skills versionadas; wave-config-extended.yaml pronto.

### Week 3: Observability & Traces
- [ ] Implement TraceContext class
- [ ] Add trace propagation em orchestrator
- [ ] Integrar com Application Insights
- [ ] Build PowerBI dashboard ("Agent Observatory")

**Deliverable:** Traces fluindo; dashboard funcional.

### Week 4: Checkpoints & Spec-as-Executable
- [ ] Implement EscalationEngine
- [ ] Set up routing (Slack/Teams)
- [ ] Implement DataContractValidator
- [ ] Integrate em Gate 3
- [ ] Write data contracts para Bradesco

**Deliverable:** Escalations automáticas; specs executáveis; Gate 3 robusto.

---

## ✅ Validation Checklist

Antes de considerar "completo", verificar:

- [ ] Harness v1.0.0 formally approved (com sign-off)
- [ ] Skills versioning testado com Bradesco (2+ waves)
- [ ] Observability: 100% de traces coletados (application insights)
- [ ] Human-Agent Checkpoints: escalations rodam por 1 week sem issue
- [ ] Spec-as-Executable: DataContractValidator passing 90% de validações
- [ ] Equipe treinada em novo framework
- [ ] Runway wave (próxima) usando todos os 5 artefatos

---

## 📚 Quick Reference

| Need | File | Use Case |
|------|------|----------|
| "O que é harness?" | HARNESS-MANIFEST | New team member onboarding |
| "Por que meu agente não auto-approved?" | HUMAN-AGENT-CHECKPOINTS | Debugging escalation |
| "Como rastrear custo por agent?" | OBSERVABILITY-AND-TRACES | Cost optimization |
| "Como atualizar skills sem quebrar?" | wave-config-extended | Skill deployment |
| "Como garantir data quality?" | spec-as-executable | Gate 3 validation |
| "Meu harness é v1.0?" | HARNESS-CHANGELOG | Versioning check |

---

## 🔗 Relacionado ao Paper

**"The New SDLC with Vibe Coding" — Key Mappings:**

| Paper Concept | DMF Impl. |
|---|---|
| Model + Harness = Agent | HARNESS-MANIFEST |
| Context Engineering | wave-config-extended + skills versioning |
| Spec-Driven Development | spec-as-executable |
| Conductor vs. Orchestrator | HUMAN-AGENT-CHECKPOINTS (escalation) |
| Observability as part of harness | OBSERVABILITY-AND-TRACES |
| Trajectory vs. Output evals | HARNESS-CHANGELOG (entry: Trajectory Evals) |
| 80% problem | HUMAN-AGENT-CHECKPOINTS (Tier 2 human review) |
| Factory model | Entire DMF framework |

---

## 📝 Next: Lessons Learned

Uma vez implementado, adicionar entrada em `/memories/repo/brd-orchestra-lessons-learned.md`:

```markdown
### 2026-07-16 — Agentic Engineering Baseline Established

- **Context:** Implemented 5 recommendations from "New SDLC" paper.
- **Lesson:** Harness > Model. Formalization enables reproducibility. Evals (trajectory + output) catch 80% failures before production.
- **Action:** HARNESS-MANIFEST, OBSERVABILITY, CHECKPOINTS now part of DMF standard. Skills versioning prevents wave-to-wave breaks.
- **Tag:** [process|quality|architecture]
```

---

**Status:** 🟢 Ready for implementation  
**Next Step:** Week 1 kickoff (HARNESS-MANIFEST review)  
**Questions?** See individual doc files for detailed guidance.
