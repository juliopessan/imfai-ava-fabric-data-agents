# Workflows Reference — `data_agents`

Abaixo estão os workflows planejados (specs) para este módulo.

---

## UPSTREAM

### data-strategy
- Spec: `workflows/data-strategy/data-strategy.spec.md`
- Propósito: problem statement + KPIs + success criteria

### business-analysis
- Spec: `workflows/business-analysis/business-analysis.spec.md`
- Propósito: perguntas analíticas, regras técnicas, STTM, DQ inicial

---

## MIDSTREAM

### architecture
- Spec: `workflows/architecture/architecture.spec.md`
- Propósito: AOD/DDS + decisões, segurança, observabilidade

### data-model
- Spec: `workflows/data-model/data-model.spec.md`
- Propósito: modelo lógico + metadados + métricas

### agent-blueprint
- Spec: `workflows/agent-blueprint/agent-blueprint.spec.md`
- Propósito: blueprint multiagente

### agent-contracts
- Spec: `workflows/agent-contracts/agent-contracts.spec.md`
- Propósito: contracts/guardrails por agente

---

## DOWNSTREAM

### delivery
- Spec: `workflows/delivery/delivery.spec.md`
- Propósito: gerar DDL/SQL/PySpark para o piloto

### unit-tests
- Spec: `workflows/unit-tests/unit-tests.spec.md`
- Propósito: gerar testes automatizados

### governance
- Spec: `workflows/governance/governance.spec.md`
- Propósito: monitoring spec + DQ rules + auditoria

---

## CORE / Utilitários

### workflow-status
- Spec: `workflows/workflow-status/workflow-status.spec.md`
- Propósito: status do projeto e próximos passos

### gate-1-up-mid
- Spec: `workflows/gate-1-up-mid/gate-1-up-mid.spec.md`
- Propósito: validar Gate 1 (UP→MID)

### gate-2-mid-down
- Spec: `workflows/gate-2-mid-down/gate-2-mid-down.spec.md`
- Propósito: validar Gate 2 (MID→DOWN)

### gate-3-down-prod
- Spec: `workflows/gate-3-down-prod/gate-3-down-prod.spec.md`
- Propósito: validar Gate 3 (DOWN→PROD)

### routing
- Spec: `workflows/routing/routing.spec.md`
- Propósito: roteamento por artefatos
