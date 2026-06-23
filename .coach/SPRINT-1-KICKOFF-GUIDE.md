# DMF Coach — Sprint 1 Kickoff Guide

**Data:** 2026-06-18  
**Sprint:** 1 (Jun 25–Jul 5)  
**Status:** 🟢 Ready to Start  
**Owner:** [Assign Now]

---

## O Que Você Precisa Fazer

### ✅ Pré-Sprint (Hoje – Jun 24)

**1. Leia os 3 Documentos Essenciais** (30 min)
- [ ] [docs/COACH-DECISIONS-APPROVED.md](../docs/COACH-DECISIONS-APPROVED.md) — Decisões locked in
- [ ] [src/shared/coaches/INTEGRATION-EXAMPLES.py](../src/shared/coaches/INTEGRATION-EXAMPLES.py) — Exemplos de código
- [ ] [.coach/README.md](../../.coach/README.md) — Quick reference

**2. Encontre os Arquivos Reais** (1 hora)
```bash
# Procure por estes patterns:
grep -r "def spawn_agent" src/
grep -r "class.*GateScoreCalculator" src/
grep -r "async def spawn_agent" src/
grep -r "def calculate" src/shared/scripts/

# Salve os caminhos:
# migration-coordinator: _______________
# quality-gate scoring: _______________
```

**3. Clone o Repositório Coach** (se ainda não tiver)
```bash
cd ~/projects/imfai-ava-fabric-data-agents

# Verifique estrutura
ls src/shared/coaches/         # Deve ter: integration.py
ls .coach/                      # Deve ter: README.md, telemetry/, rules/
```

**4. Prepare o Environment**
```bash
# Ative venv (se ainda não estiver)
.\.venv\Scripts\Activate.ps1

# Instale dependências (já deve estar pronto)
pip install pyyaml jsonschema

# Rode testes de importação
python -c "from src.shared.coaches import telemetry_hook, gate_scorer; print('✅ Ready')"
```

---

## Week 1 (Jun 25–28): Hook em migration-coordinator

### Tarefa 1: Localizar migration-coordinator

```bash
# Encontre o arquivo
find . -name "*migration*coordinator*" -type f | grep -E "\.(py|md)$"

# Esperado resultado: 
# .github/agents/migration-coordinator.chatmode.md
# src/shared/scripts/migration_coordinator.py  [ou similar]
```

**Se encontrar `.chatmode.md`:**
→ É uma referência. Procure pelo arquivo real em `src/` ou `src/modules/`

### Tarefa 2: Entender spawn_agent()

```bash
# Abra o arquivo e localize a função
# Procure por pattern:
#   def spawn_agent(...)
#   async def spawn_agent(...)

# Copie a assinatura aqui:
# ________________________________________
# ________________________________________
```

### Tarefa 3: Integrar Telemetry Hook

**Template (copie e adapte):**
```python
# ADICIONE NO FIM DA FUNÇÃO spawn_agent(), ANTES DO return

from src.shared.coaches import telemetry_hook

result = await agent_execution(...)  # <-- Resultado já disponível

# NEW: Log telemetry
try:
    telemetry_hook.log_agent_execution(
        agent_id=agent_id,
        wave=wave,
        gate=gate,
        result=result
    )
except Exception as e:
    logger.warning(f"Coach telemetry logging failed: {e}")

return result
```

**Checklist:**
- [ ] Copiei o código
- [ ] Ajustei `agent_id`, `wave`, `gate` (use variáveis do contexto)
- [ ] Testei import: `from src.shared.coaches import telemetry_hook`
- [ ] Verifiquei que result tem os campos esperados

### Tarefa 4: Testar com Agent Real

```bash
# Execute um agente pequeno da clientebanco Wave 2
python -c "
from src.shared.coaches import telemetry_collector

# Verifique que arquivo foi criado
import os
telemetry_files = list(os.glob('.coach/telemetry/*.jsonl'))
print(f'Telemetry files: {len(telemetry_files)}')

if telemetry_files:
    with open(telemetry_files[0]) as f:
        import json
        event = json.loads(f.readline())
        print(f'✅ First event: {event[\"timestamp\"]}')
"
```

---

## Week 2 (Jul 1–5): Hook em quality-gate + Dashboard

### Tarefa 5: Localizar quality-gate

```bash
# Encontre o arquivo
find . -name "*quality*gate*" -type f | grep -E "\.(py|md)$"

# Esperado:
# .github/agents/quality-gate.chatmode.md
# src/shared/scripts/gate_score_report.py  [ou similar]
```

### Tarefa 6: Entender calculate_gatescore()

```bash
# Abra gate_score_report.py (ou similar)
# Procure por: GateScoreCalculator.calculate()

# Copie a assinatura:
# ________________________________________
# ________________________________________

# Procure por: Determinar status (approved/conditional/blocked)
# Deve usar score >= 0.85, 0.70, < 0.70
```

### Tarefa 7: Integrar Anti-Pattern Adjustment

**Template (copie e adapte):**
```python
# ADICIONE ANTES DE DETERMINAR STATUS

from src.shared.coaches import gate_scorer

base_score = (completude * 0.35) + (quality * 0.25) + ...

# NEW: Adjust for anti-patterns
adjusted_score, patterns, adjustments = gate_scorer.adjust_score(
    base_score=base_score,
    wave=self.wave_id,
    gate=self.gate_number,
    artifacts={
        'entities_discovered': [...],  # Gate 2 only
        'entities_mapped': [...],      # Gate 2 only
        'sttm_regenerations': 0,
        'agent_executions': [...]
    }
)

# USE adjusted_score for final status
if adjusted_score >= 0.85:
    status = "approved"
elif adjusted_score >= 0.70:
    status = "conditional"
else:
    status = "blocked"
```

**Checklist:**
- [ ] Identifiquei onde `base_score` é calculado
- [ ] Identifiquei onde `status` é determinado
- [ ] Copiei o adjustment code entre eles
- [ ] Passei artifacts corretos (ou deixei como None se não aplicável)

### Tarefa 8: Testar com Dados de clientebanco Wave 2

```bash
# Simule um score que deve ser ajustado
python -c "
from src.shared.coaches import gate_scorer

# Trigger anti-patterns
artifacts = {
    'entities_discovered': [f'e_{i}' for i in range(127)],
    'entities_mapped': [f'e_{i}' for i in range(98)],  # Gap!
    'sttm_regenerations': 3,  # Regen too many times!
}

adjusted, patterns, log = gate_scorer.adjust_score(
    base_score=0.82,
    wave='clientebanco_wave_2',
    gate=2,
    artifacts=artifacts
)

print(f'Base:     0.82')
print(f'Adjusted: {adjusted:.4f}')
print(f'Patterns: {len(patterns)}')
for name, impact in log:
    print(f'  - {name}: {impact:+d}')
"
```

---

## Validation Checklist (End of Week 2)

### Telemetry Hook (Week 1)
- [ ] Code added to spawn_agent()
- [ ] No syntax errors (ran Python syntax check)
- [ ] Tested with real agent execution
- [ ] `.coach/telemetry/wave_*.jsonl` files created
- [ ] Events contain: timestamp, agent_id, tokens, cost, artifact

### GateScore Adjustment (Week 2)
- [ ] Code added to calculate_gatescore()
- [ ] No syntax errors
- [ ] Tested with mock artifacts
- [ ] adjusted_score is used for status determination
- [ ] Anti-patterns correctly deducted

### Dashboard (Week 2)
- [ ] Created `.coach/templates/wave-analysis.html` (Chart.js template)
- [ ] Can read JSONL and generate HTML report
- [ ] Created `.coach/cli.py` (if time permits)
- [ ] `python -m src.shared.coaches.cli --wave clientebanco_wave_2 --action analyze` works

---

## Troubleshooting

### Q: Não encontro o arquivo migration-coordinator.py real
**A:** 
- Verifique em `src/shared/scripts/` (comum)
- Verifique em `src/modules/dmf-fabric-agents/core-coordination/` (possível)
- Se só tiver `.chatmode.md`, copie o código para um novo arquivo Python

### Q: Qual é o formato do result object?
**A:** Verifique em `src/shared/coaches/integration.py`, docstring de `log_agent_execution()`:
```python
# Expected result format:
# {
#     'model': 'claude-opus-4-1',
#     'tokens_input': 12500,
#     'tokens_output': 8300,
#     'artifact_content': '...',
#     'artifact_filename': 'architecture.md',
#     ...
# }
```

### Q: GateScore pode ficar abaixo de 0.0?
**A:** Não. Coach garante: `max(0.0, min(1.0, adjusted_score))`

### Q: Preciso modificar quality-gate.py ou posso criar novo arquivo?
**A:** Modifique o existente. Se não quiser, crie um wrapper e importe em quality-gate.

---

## Documentação de Referência

| Documento | Conteúdo | Tempo |
|-----------|----------|-------|
| [COACH-DECISIONS-APPROVED.md](../docs/COACH-DECISIONS-APPROVED.md) | Decisões finais + timeline | 15 min |
| [INTEGRATION-EXAMPLES.py](../src/shared/coaches/INTEGRATION-EXAMPLES.py) | Exemplos de código | 20 min |
| [.coach/README.md](../../.coach/README.md) | Quick reference | 10 min |
| [COACH-INTEGRATION-BLUEPRINT.md](../docs/COACH-INTEGRATION-BLUEPRINT.md) | Design completo | 30 min |

---

## Weekly Standup Template

### Week 1 Standup (Jun 28)
```
- ✅ Encontrouarchivo migration-coordinator
- ✅ / ⚠️ Adicionou telemetry hook
- 🟡 Tested? Yes / No / In progress
- ⛔ Blockers: _______________
- ✅ Next: Start quality-gate hook
```

### Week 2 Standup (Jul 5)
```
- ✅ Encontrou arquivo quality-gate
- ✅ / ⚠️ Adicionou GateScore adjustment
- 🟡 Dashboard? Yes / No / In progress
- ⛔ Blockers: _______________
- 🚀 Ready for Sprint 2? Yes / No
```

---

## Next: Sprint 1 → Sprint 2

Após completion de Sprint 1:
- ✅ Telemetry flowing
- ✅ GateScore adjusting
- ✅ Dashboard showing metrics

Sprint 2 (Jul 8–19) começa com:
- Skill Finder (auto-discovery de padrões)
- Context Health Scorer (audit de .agent.md)
- Refinement based on Wave 2 learnings

---

## Contatos & Escalação

**Se travar:**
1. Verifique TROUBLESHOOTING section acima
2. Veja código de exemplo em INTEGRATION-EXAMPLES.py
3. Rodar testes em isolation (test-telemetry.py, test-gatescore.py)
4. Post em team Slack / ping Coach owner

---

**Status:** 🟢 Ready for Kickoff | **Start:** Jun 25, 2026 | **Owner:** [Assign]

Boa sorte! 🚀
