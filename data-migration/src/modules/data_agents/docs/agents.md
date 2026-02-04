# Agents Reference — `data_agents`

Este módulo define um time de agentes por esteira (UP/MID/DOWN) mais um **Orchestrator**.

> Nesta fase, os agentes estão como **specs** em `src/modules/data_agents/agents/*.spec.md`.

---

## UPSTREAM

### Data Strategist / Product Agent
- Spec: `agents/data-strategist.spec.md`
- Papel: definir valor, escopo, KPIs, success criteria

### Business Analyst Agent (Enhanced)
- Spec: `agents/business-analyst.spec.md`
- Papel: perguntas analíticas, regras técnicas, STTM, DQ inicial

---

## MIDSTREAM

### Data Solution Architect Agent
- Spec: `agents/data-solution-architect.spec.md`
- Papel: arquitetura, AOD/DDS, segurança, observabilidade

### Data Modeler Agent
- Spec: `agents/data-modeler.spec.md`
- Papel: modelo lógico, metadados, métricas

### Agent Design / AI Design Agent
- Spec: `agents/agent-designer.spec.md`
- Papel: blueprint multiagente, contratos, limites de autonomia

---

## DOWNSTREAM

### Data Engineer Execution Agent (Unificado)
- Spec: `agents/data-engineer-exec.spec.md`
- Papel: gerar SQL/DDL/PySpark, DQ checks, testes, docs

### BI / Semantic Layer Agent (Opcional)
- Spec: `agents/bi-semantic.spec.md`
- Papel: semantic layer e dashboards baseline

### Data Steward / Governance Agent
- Spec: `agents/data-steward.spec.md`
- Papel: DQ, monitoring spec, auditoria, compliance

### Iteration & Improvement Agent
- Spec: `agents/iteration-improvement.spec.md`
- Papel: melhoria contínua, backlog, hipóteses

---

## CORE

### Orchestrator Agent
- Spec: `agents/orchestrator.spec.md`
- Papel: gates, estado UP/MID/DOWN, roteamento por artefatos
