# Examples — `data_agents`

## Exemplo 1: Piloto Trip Data (medalhão)

**Objetivo:** sair do PRD até geração de código e validação por gates.

### Sequência sugerida

1. `data-strategy`
2. `business-analysis`
3. `gate-1-up-mid`
4. `architecture`
5. `data-model`
6. `agent-blueprint` + `agent-contracts`
7. `gate-2-mid-down`
8. `delivery`
9. `unit-tests`
10. `governance`
11. `gate-3-down-prod`

---

## Exemplo 2: Só gerar esqueleto para novo projeto

- Rode `workflow-status` para checar o que já existe.
- Use `routing` para sugerir o próximo workflow.

---

## Troubleshooting (comum)

- **Nada é gerado:** verifique `artifacts_root` e `project_code` no `module.yaml`.
- **Pastas não aparecem:** rode a instalação do módulo (installer) no runtime BMAD.
- **Gate falha:** abra o relatório do gate e complete os itens faltantes no artefato correspondente.
