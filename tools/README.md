# 🔧 Ferramentas de Desenvolvimento

Scripts de validação, testes e utilidades para a Data Migration Factory.

## Estrutura

### `validation/` — Scripts de Validação

Scripts para validação de integração, qualidade e conformidade.

| Script | Propósito | Uso |
|--------|-----------|-----|
| `WORKFLOW-INTEGRATION-CHECK.py` | Validação inicial de integração | `python WORKFLOW-INTEGRATION-CHECK.py` |
| `WORKFLOW-INTEGRATION-CHECK-v2.py` | Validação melhorada (v2) | `python WORKFLOW-INTEGRATION-CHECK-v2.py` |
| `run_financeiro_tier1_validation.py` | Validação específica Financeiro TIER 1 | `python run_financeiro_tier1_validation.py` |

### `utilities/` — Scripts Auxiliares

Scripts de suporte e utilidades do sistema.

| Script | Propósito |
|--------|-----------|
| `test_telemetry_system.py` | Testes do sistema de telemetria |

## Como Usar

### Executar Validação

```bash
# Ativar ambiente virtual
.\.venv\Scripts\Activate.ps1

# Executar validação
python tools/validation/WORKFLOW-INTEGRATION-CHECK.py

# Executar validação v2
python tools/validation/WORKFLOW-INTEGRATION-CHECK-v2.py

# Validar projeto Financeiro
python tools/validation/run_Financeiro_tier1_validation.py
```

### Executar Testes de Telemetria

```bash
python tools/utilities/test_telemetry_system.py
```

## Integração com CI/CD

Esses scripts são executados no pipeline de CI/CD:
- **GitHub Actions:** `.github/workflows/`
- **Azure Pipelines:** `config/azure-pipelines.yml`

## Outputs Esperados

Os scripts geram:
- Relatórios de status (stdout)
- Logs de validação
- Artefatos em `reports/` (se aplicável)

---

Para mais informações:
- [`validation/README.md`](./validation/README.md)
- [`utilities/README.md`](./utilities/README.md)
- [`REPOSITORY-ORGANIZATION.md`](../REPOSITORY-ORGANIZATION.md)

**Última atualização:** 2026-06-09
