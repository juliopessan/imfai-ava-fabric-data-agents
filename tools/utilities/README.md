# 🛠️ Scripts Auxiliares

Utilidades e scripts de suporte para a Data Migration Factory.

## Scripts Disponíveis

### test_telemetry_system.py

**Propósito:** Testar sistema de telemetria e coleta de métricas

**Uso:**
```bash
python test_telemetry_system.py
```

**Testa:**
- Inicialização do sistema de telemetria
- Coleta de métricas
- Persistência de dados
- Integração com observabilidade

**Output:** Relatório de testes + status de telemetria

---

## Como Executar

### Verificar Ambiente
```bash
# Ativar venv
.\.venv\Scripts\Activate.ps1

# Verificar Python
python --version

# Instalar dependências
pip install -r config/requirements-dev.txt
```

### Executar Testes
```bash
# Testar telemetria
python tools/utilities/test_telemetry_system.py

# Com verbose
python tools/utilities/test_telemetry_system.py -v

# Salvar output em arquivo
python tools/utilities/test_telemetry_system.py > telemetry_report.txt
```

---

## Saída Esperada

### Sucesso ✓
```
Testing Telemetry System...
✓ System initialized
✓ Metrics collected
✓ Data persisted
✓ All tests passed
```

### Com Avisos
```
⚠ WARNING: Slow metric collection (>1s)
⚠ TIP: Check system resources
```

---

## Troubleshooting

### Erro de Importação
```bash
# Garantir que está no diretório correto
cd c:\Users\julio.cesar.d.pessan\Downloads\imfai-ava-fabric-data-agents

# Reinstalar dependências
pip install --upgrade -r config/requirements-dev.txt
```

### Permissões
```powershell
# Se receber erro de execução
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

---

## Próximas Melhorias

- [ ] Dashboard de telemetria em tempo real
- [ ] Exportação de métricas para Grafana
- [ ] Alertas automáticos
- [ ] Análise de tendências

---

## Referências

- [Documentação de Ferramentas](../README.md)
- [Sistema de Telemetria Completo](../../src/shared/scripts/README.md)
- [Organização do Repositório](../../REPOSITORY-ORGANIZATION.md)

**Última atualização:** 2026-06-09
