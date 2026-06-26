# ✅ Scripts de Validação

Validação de integração, qualidade e conformidade da Data Migration Factory.

## Scripts Disponíveis

### 1. WORKFLOW-INTEGRATION-CHECK.py

**Propósito:** Validação base de integração de componentes

**Uso:**
```bash
python WORKFLOW-INTEGRATION-CHECK.py
```

**Verifica:**
- Integridade de arquivos de configuração
- Conectividade entre módulos
- Status dos workflows

**Output:** Relatório de status em stdout + JSON

---

### 2. WORKFLOW-INTEGRATION-CHECK-v2.py

**Propósito:** Validação melhorada com métricas avançadas

**Uso:**
```bash
python WORKFLOW-INTEGRATION-CHECK-v2.py
```

**Melhorias em relação à v1:**
- Verificações mais detalhadas
- Métricas de performance
- Recomendações automáticas

**Output:** Relatório expandido + recommendations

---

### 3. run_Financeiro_tier1_validation.py

**Propósito:** Validação específica para o projeto Financeiro (TIER 1)

**Uso:**
```bash
python run_Financeiro_tier1_validation.py
```

**Valida:**
- Estrutura do projeto Financeiro
- Conformidade com padrões TIER 1
- Artefatos de descoberta
- Integridade de dados

**Output:** Relatório específico de Financeiro

---

## Integração com CI/CD

### GitHub Actions

Os scripts são executados automaticamente em:
- **Push:** Validação rápida
- **Pull Request:** Validação completa
- **Schedule:** Validação noturna

### Azure Pipelines

Configurado em `config/azure-pipelines.yml`:
```yaml
- script: python tools/validation/WORKFLOW-INTEGRATION-CHECK.py
  displayName: 'Run Integration Checks'
```

---

## Saída Esperada

### Sucesso ✓
```
✓ All checks passed
✓ Integration status: READY
✓ No blockers found
```

### Aviso ⚠️
```
⚠ WARNING: Some components not fully initialized
⚠ Recommendations: See detailed report
```

### Falha ✗
```
✗ CRITICAL: Integration failed
✗ Errors: [list of blockers]
✗ Action: Review logs and remediate
```

---

## Troubleshooting

### "ModuleNotFoundError"
```bash
# Ativar venv e instalar dependências
.\.venv\Scripts\Activate.ps1
pip install -r config/requirements-dev.txt
```

### Script não encontrado
```bash
# Certificar que está no diretório correto
cd c:\Users\julio.cesar.d.pessan\Downloads\imfai-ava-fabric-data-agents
ls tools/validation/
```

### Permissão negada
```powershell
# Windows: Executar PowerShell como Admin
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

---

## Referências

- [Documentação de Ferramentas](../README.md)
- [Organização do Repositório](../../REPOSITORY-ORGANIZATION.md)
- [Estrutura Geral](../../INDEX.md)

**Última atualização:** 2026-06-09
