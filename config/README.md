# ⚙️ Configurações

Arquivos de configuração centralizada para a Data Migration Factory.

## Conteúdo

### requirements-dev.txt

**Descrição:** Dependências Python para desenvolvimento

**Conteúdo:**
- pytest (framework de testes)
- pytest-cov (cobertura de testes)
- pyyaml (parsing de YAML)
- Outras dependências do projeto

**Uso:**
```bash
# Instalar dependências
pip install -r config/requirements-dev.txt

# Em um venv
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r config/requirements-dev.txt
```

### azure-pipelines.yml

**Descrição:** Configuração de CI/CD no Azure Pipelines

**Conteúdo:**
- Triggers (quando executar)
- Jobs (etapas de build)
- Tasks (ações específicas)
- Artifact publishing

**Uso:**
```yaml
# Exemplo de trigger
trigger:
  branches:
    include:
    - main
    - develop

# Exemplo de job
jobs:
- job: ValidateIntegration
  displayName: 'Validate Integration'
  steps:
  - script: python -m pytest src/shared/tests/ -q
```

---

## Setup Inicial

### 1. Clonar Repositório
```bash
git clone <repo-url>
cd imfai-ava-fabric-data-agents
```

### 2. Criar Virtual Environment
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Instalar Dependências
```bash
pip install -r config/requirements-dev.txt
```

### 4. Verificar Setup
```bash
python -m pytest src/shared/tests/ -q
# Esperado: 315 passed
```

---

## Configuração de Environment

### Variáveis de Ambiente

```bash
# .env (não versionado)
MIGRATION_ENV=development
LOG_LEVEL=INFO
```

### Padrões por Ambiente

| Variável | Dev | Staging | Prod |
|----------|-----|---------|------|
| `LOG_LEVEL` | DEBUG | INFO | ERROR |
| `DB_RETRY_COUNT` | 3 | 5 | 10 |
| `TIMEOUT_SEC` | 60 | 30 | 10 |

---

## Troubleshooting

### "pip: command not found"
```bash
# Usar python -m
python -m pip install -r config/requirements-dev.txt
```

### "ModuleNotFoundError: No module named 'pytest'"
```bash
# Reinstalar dependências
pip uninstall -r config/requirements-dev.txt -y
pip install -r config/requirements-dev.txt
```

### Permissão negada no PowerShell
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

---

## CI/CD Integration

### GitHub Actions
Usar arquivo em `.github/workflows/` que referencia `config/requirements-dev.txt`

### Azure DevOps
Usar `config/azure-pipelines.yml` diretamente

### Local Testing
```bash
# Simular CI/CD localmente
python -m pytest src/shared/tests/ -v
```

---

## Best Practices

✅ **DO:**
- Manter `requirements-dev.txt` versionado
- Usar pins de versão específicas em produção
- Testar localmente antes de push
- Documentar novas dependências

❌ **DON'T:**
- Usar `pip install` sem `-r requirements.txt`
- Deixar `.env` com secrets em versionamento
- Modificar `azure-pipelines.yml` sem CI/CD review
- Usar dependências não aprovadas

---

## Referências

- [Organização do Repositório](../REPOSITORY-ORGANIZATION.md)
- [Documentação de Ferramentas](../tools/README.md)
- [Estrutura Geral](../INDEX.md)
- [Documentação de Dependências](https://requirements.readthedocs.io/)

**Última atualização:** 2026-06-09
