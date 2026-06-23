# DMF Coach — Decisões Aprovadas & Próximos Passos

**Data:** 2026-06-18  
**Status:** ✅ Decisões Aprovadas | 🚀 Implementação Sprint 1  
**Owner:** [To be assigned]

---

## Decisões Tomadas (3)

### ✅ DECISÃO 1: Hook de Telemetria

**Pergunta:** Qual arquivo para capturar telemetria de agentes?

**Decisão:** **Opção A — `migration-coordinator.spawn_agent()`**

**Rationale:**
- Hook APÓS execução do agente (resultado disponível)
- Antes de retornar (resultado completo)
- Centralizado (um único ponto para todos os agentes)
- Acesso a metadata: agent_id, wave, gate

**Implementação:**
```python
# File: src/shared/scripts/migration-coordinator.py
# Location: After agent execution result available

from src.shared.coaches import telemetry_hook

result = await agent_execution(agent_id, wave, ...)

# NEW: Log to Coach
telemetry_hook.log_agent_execution(
    agent_id=agent_id,
    wave=wave,
    gate=gate,
    result=result
)

return result
```

**Saída:** `.coach/telemetry/{wave}_{date}.jsonl` (append-only)

---

### ✅ DECISÃO 2: Ajuste Automático de GateScore

**Pergunta:** Deve Coach ajustar automaticamente o GateScore?

**Decisão:** **Sim — Anti-patterns deuzem pontos automaticamente**

**Rationale:**
- Detecta problemas cedo (pré-Gate 3)
- Penaliza comportamentos ruins (incentiva melhorias)
- Garante consistência (sem subjetividade)
- Threshold protegido: base_score + ajuste >= 0.00

**Implementação:**
```python
# File: src/shared/scripts/gate_score_report.py
# Location: In GateScoreCalculator.calculate()

from src.shared.coaches import gate_scorer

base_score = (completude * 0.35) + ...

# NEW: Detect and adjust
adjusted_score, patterns, adjustments = gate_scorer.adjust_score(
    base_score=base_score,
    wave=self.wave_id,
    gate=self.gate_number,
    artifacts={...}
)

# Use adjusted_score for status determination
if adjusted_score >= 0.85: status = "approved"
elif adjusted_score >= 0.70: status = "conditional"
else: status = "blocked"
```

**Impacto de Score:**
- Wave Completion (entity gap < 90%): -15 pts
- STTM Instability (regen > 2× em 2h): -10 pts
- Model Overreliance (GPT-4 on parametric): -5 pts
- Context Bloat (> 70% OR > 40KB): -10 pts
- Silent Executor Failure (output < 1000 tokens): -30 pts 🚨
- GateScore Regression (drop > 5% WoW): -20 pts

**Exemplo:**
```
Base GateScore:      0.82
- Entity gap (-15):    0.67
- Artifact bloat (-10): 0.57  ← Blocked (< 0.70)
```

---

### ✅ DECISÃO 3: Aprovação de Skills

**Pergunta:** Quem aprova skills descobertas?

**Decisão:** **TBD — Governance workflow TBD**

**Current:** Placeholder implementado em `SkillGovernanceWorkflow`

**Próximos Passos:**
1. Definir fluxo (GitHub PR? Jira ticket? Review manual?)
2. Implementar `skill_finder.discover_patterns()`
3. Auto-registry em `.github/skills/`
4. (Sprint 3+)

---

## Implementação Entregue

### Arquivos Criados

1. **src/shared/coaches/integration.py** ✅
   - `TelemetryHook` class (hook para migration-coordinator)
   - `AntiPatternGateScoringAdjustment` class (ajuste de score)
   - `SkillGovernanceWorkflow` class (placeholder para governance)
   - Instâncias globais: `telemetry_hook`, `gate_scorer`, `skill_governance`

2. **src/shared/coaches/INTEGRATION-EXAMPLES.py** ✅
   - Exemplos de código para migration-coordinator
   - Exemplos de código para quality-gate
   - Exemplos de código para wave_status_tracker
   - Testes e checklist

3. **src/shared/coaches/__init__.py** (updated) ✅
   - Exports do novo integration module

---

## Próximos Passos (Sprint 1)

### Semana 1 (Jun 25–28): Integração em migration-coordinator

**Tarefas:**
- [ ] Localize `migration-coordinator.py` (ou arquivo real de spawn)
- [ ] Leia método `spawn_agent()` ou equivalente
- [ ] Insira chamada `telemetry_hook.log_agent_execution()`
- [ ] Teste com agent real (data-architect em clientebanco Wave 2)
- [ ] Valide: `.coach/telemetry/clientebanco_wave_2_*.jsonl` criado

**Recursos:**
- Exemplos: `src/shared/coaches/INTEGRATION-EXAMPLES.py` (EXAMPLE_1)
- Código: `src/shared/coaches/integration.py` (TelemetryHook)

**Saída esperada:**
```
✅ Telemetry logged for data-architect in clientebanco_wave_2 Gate 1
   File: .coach/telemetry/clientebanco_wave_2_2026-06-18.jsonl
   Event: timestamp, agent_id, tokens, cost, artifact_size, etc.
```

---

### Semana 2 (Jul 1–5): Integração em quality-gate + Dashboard

**Tarefas:**
- [ ] Localize `gate_score_report.py` (ou arquivo real de scoring)
- [ ] Leia método `GateScoreCalculator.calculate()`
- [ ] Insira chamada `gate_scorer.adjust_score()`
- [ ] Teste com artifacts contendo anti-patterns
- [ ] Valide: score ajustado corretamente, status final correto

**Recursos:**
- Exemplos: `src/shared/coaches/INTEGRATION-EXAMPLES.py` (EXAMPLE_2)
- Código: `src/shared/coaches/integration.py` (AntiPatternGateScoringAdjustment)

**Saída esperada:**
```
Base GateScore:       0.82
Anti-patterns:        3 detected
  - STTM Instability: -10 pts
  - Entity Gap:       -15 pts
  - Model Overuse:     -5 pts
Adjusted GateScore:   0.52 (BLOCKED)
Recommendations:      (auto-generated)
```

---

### Semana 2 (Jul 1–5): Dashboard Básico

**Tarefas:**
- [ ] Crie `.coach/templates/wave-analysis.html` (Chart.js)
- [ ] Leia telemetry JSONL de clientebanco Wave 2
- [ ] Visualize: timeline agent × tempo, custo breakdown, anti-patterns
- [ ] Crie `.coach/cli.py` (gera HTML de wave summaries)

**Saída esperada:**
```bash
python -m src.shared.coaches.cli --wave clientebanco_wave_2 --action analyze
# → .coach/reports/clientebanco-wave-2-analysis.html (abrir no browser)
```

---

## Como Usar (Developers)

### Quick Test

```bash
# 1. Test telemetry hook
python -c "
from src.shared.coaches import telemetry_hook

result = {
    'model': 'claude-opus-4-1',
    'tokens_input': 1000,
    'tokens_output': 500,
    'artifact_content': 'test' * 1000,
    'artifact_filename': 'test.md',
    'execution_time_sec': 30,
    'status': 'success',
    'artifact_sections': 5,
    'references_entities': 10,
    'validation_passed': True
}

event = telemetry_hook.log_agent_execution(
    agent_id='test-agent',
    wave='demo_wave_1',
    gate=1,
    result=result
)

print(f'✅ Logged: {event[\"timestamp\"]}')
"

# 2. Test gate scorer
python -c "
from src.shared.coaches import gate_scorer

artifacts = {
    'entities_discovered': [f'e_{i}' for i in range(127)],
    'entities_mapped': [f'e_{i}' for i in range(98)],
    'sttm_regenerations': 3,
}

adjusted, patterns, adjustments = gate_scorer.adjust_score(
    base_score=0.82,
    wave='test',
    gate=2,
    artifacts=artifacts
)

print(f'Adjusted Score: {adjusted:.4f} (change: {adjusted - 0.82:+.4f})')
print(f'Anti-patterns: {len(patterns)}')
"
```

---

## Verificação de Status

### ✅ Implementado
- [x] Telemetry schema (JSON)
- [x] TelemetryCollector (captura + armazena)
- [x] AntiPatternDetector (6 regras)
- [x] TelemetryHook (integração migration-coordinator)
- [x] AntiPatternGateScoringAdjustment (integração quality-gate)
- [x] Integration examples (código + testes)
- [x] Documentação (blueprint + guias)

### 🟡 A Fazer (Sprint 1)
- [ ] Hook em migration-coordinator.py (real file)
- [ ] Hook em quality-gate.py (real file)
- [ ] Teste em clientebanco Wave 2 (dados históricos)
- [ ] Dashboard HTML básico
- [ ] CLI wrapper

### 🔵 Futuro (Sprint 2+)
- [ ] Skill Finder (pattern discovery)
- [ ] Context Health Scorer (audit .agent.md)
- [ ] Learning Center (playbooks)
- [ ] Gamification (badges)

---

## Documentação de Referência

1. **Design Completo:** [docs/COACH-INTEGRATION-BLUEPRINT.md](../docs/COACH-INTEGRATION-BLUEPRINT.md)
2. **Visão Estratégica (PT-BR):** [docs/COACH-COMO-TUTOR-BOAS-PRATICAS.md](../docs/COACH-COMO-TUTOR-BOAS-PRATICAS.md)
3. **Quick Start:** [.coach/README.md](../.coach/README.md)
4. **Exemplos de Integração:** [src/shared/coaches/INTEGRATION-EXAMPLES.py](./INTEGRATION-EXAMPLES.py)

---

## Contato & Escalação

**Se encontrar bloqueadores:**

1. **Arquivo migration-coordinator não encontrado?**
   → Procure por pattern: `def spawn_agent` ou `async def spawn_agent`
   
2. **Qual é o formato do result object?**
   → Check: `src/shared/coaches/integration.py` docstring de `log_agent_execution()`
   
3. **GateScore deve estar em [0.0, 1.0]?**
   → Sim. Coach garante com `max(0.0, min(1.0, adjusted_score))`

4. **Posso testar sem modificar production files?**
   → Sim! Use os exemplos em `INTEGRATION-EXAMPLES.py` com dados mock

---

## Timeline & Recursos

| Fase | Semanas | Owner | Status |
|------|---------|-------|--------|
| **Design** | Jun 18–21 | ✅ Complete | Done |
| **Telemetry Hook** | Jun 25–28 | [TBD] | Sprint 1 |
| **GateScore Adj** | Jul 1–5 | [TBD] | Sprint 1 |
| **Dashboard** | Jul 1–5 | [TBD] | Sprint 1 |
| **Anti-Patterns** | Jul 8–19 | [TBD] | Sprint 2 |
| **Skills** | Jul 22–Aug 2 | [TBD] | Sprint 3 |
| **Gamification** | Aug 5–9 | [TBD] | Sprint 4 |

---

## Aprovações

- ✅ Decision 1: Hook em migration-coordinator = **APPROVED**
- ✅ Decision 2: Ajuste automático de GateScore = **APPROVED**
- ✅ Decision 3: Skills governance = **TBD (governance workflow)**

---

**Status:** ✅ Decisions Locked In | 🚀 Ready for Sprint 1 Kickoff  
**Next:** Assign owners → Schedule Sprint 1 standup (Jun 25)

