# Step 05 — Gate 2 Review

**Agente:** migration-coordinator  
**Task:** validate-gate-2  
**Input:** `outputs/midstream/` completo + `outputs/midstream/validation-report.md`  
**Output:** `outputs/summary/gate2-decision.md`

## Instrução
Ativar `migration-coordinator` e executar `*validate-gate-2`. O agente verifica se todos os artefatos de Gate 2 estão presentes e calcula o GateScore.

## Critério de Conclusão
- [ ] GateScore ≥ 0.85 (threshold Gate 2)
- [ ] `gate2-decision.md` emitido com decisão APPROVED
- [ ] Aprovação formal registrada antes de avançar para DOWNSTREAM
