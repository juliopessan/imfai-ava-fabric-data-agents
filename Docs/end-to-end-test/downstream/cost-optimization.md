# 💰 Cost Optimization Report - NYC Green Taxi Analytics

**Projeto:** NYC Green Taxi Analytics  
**Plataforma:** Azure Databricks + ADLS Gen2  
**Analista:** Kai 🔁 (IterationImprovement)  
**Data:** 2026-02-05  
**Versão:** 1.0

> ⚠️ **Importante:** Este relatório contém estimativas baseadas na arquitetura documentada. Valores reais de custo devem ser validados com dados de billing do Azure.

---

## 📋 Executive Summary

| Métrica | Valor Estimado | Status |
|---------|----------------|--------|
| **Custo Mensal Atual** | ~$214.60 | ⚠️ Estimado (validar com billing) |
| **Custo Otimizado Projetado** | ~$160.00 | 🎯 Economia de 25% |
| **Economia Potencial** | ~$54.60/mês (~$655/ano) | ✅ Identificado |
| **ROI de Otimizações** | A DEFINIR | ⚠️ Requer esforço de implementação |

---

## 💸 Breakdown de Custos Atual

### 1. Databricks Compute (~$108/mês)

| Cluster Type | Usage | Unit Cost | Monthly Cost | % do Total |
|-------------|-------|-----------|--------------|------------|
| **Job Clusters - Bronze** | 30 runs × 15 min | $0.40/DBU ×4 | $12.00 | 11% |
| **DLT Pipeline - Silver** | 30 runs × 20 min | $0.40/DBU ×8 | $32.00 | 30% |
| **Job Clusters - Gold** | 30 runs × 15 min | $0.40/DBU ×4 | $12.00 | 11% |
| **SQL Warehouse** | ~100 hrs runtime | $0.55/DBU ×8 | $44.00 | 41% |
| **Interactive (Dev)** | ~20 hrs/mês | $0.40/DBU ×4 | $8.00 | 7% |
| **SUBTOTAL** | | | **$108.00** | **100%** |

**Observações:**
- ⚠️ SQL Warehouse representa 41% do custo de compute
- ⚠️ DLT Pipeline Silver é o job mais caro (30%)
- ✅ Jobs Bronze e Gold são eficientes (11% cada)

---

### 2. Azure Infrastructure (~$56.60/mês)

| Serviço | Usage | Unit Cost | Monthly Cost | % do Total |
|---------|-------|-----------|--------------|------------|
| **ADLS Gen2 Storage** | ~50 GB hot tier | $0.02/GB | $1.00 | 2% |
| **ADLS Transactions** | ~10M operations | $0.05/10K | $0.50 | 1% |
| **Private Endpoints** | 3 endpoints | $7.30/endpoint | $21.90 | 39% |
| **Data Transfer** | ~100 GB | $0.05/GB | $5.00 | 9% |
| **Key Vault** | ~1K operations | $0.03/10K | $0.10 | <1% |
| **Azure Monitor** | ~10 GB logs | $2.76/GB | $27.60 | 49% |
| **Alerting** | 5 rules | $0.10/rule | $0.50 | 1% |
| **SUBTOTAL** | | | **$56.60** | **100%** |

**Observações:**
- ⚠️ Azure Monitor representa 49% do custo de infra
- ⚠️ Private Endpoints custam 39% da infra
- ✅ Storage é muito eficiente (<3%)

---

### 3. Business Intelligence (~$50/mês)

| Serviço | Usage | Unit Cost | Monthly Cost |
|---------|-------|-----------|--------------|
| **Power BI Pro licenses** | 5 users | $10.00/user | $50.00 |
| **SUBTOTAL** | | | **$50.00** |

---

### 4. Total Cost Breakdown

```
┌────────────────────────────────────────────────────────────────┐
│                     TOTAL MONTHLY COST                         │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  💻 Databricks Compute:         $108.00  (50%)                │
│  ☁️  Azure Infrastructure:       $56.60  (26%)                │
│  📊 Power BI:                    $50.00  (24%)                │
│  ═══════════════════════════════════════                      │
│  🎯 TOTAL:                      $214.60  (100%)               │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Oportunidades de Otimização

### Oportunidade #1: Spot Instances para Job Clusters 🔴 P0

**Problema:**
- Job clusters (Bronze, Gold) rodam com clusters on-demand
- Custo: $12 + $12 = $24/mês

**Solução:**
- Migrar para **Spot Instances** (até 80% de desconto)
- Databricks retenta automaticamente se preempted

**Economia Projetada:**
```
Atual:     $24.00/mês (on-demand)
Otimizado: $5.00/mês (spot com ~80% desconto)
───────────────────────────────────
ECONOMIA:  $19.00/mês (~$228/ano)
```

**Implementação:**
```python
# Cluster config: adicionar spot policy
cluster_config = {
    "cluster_name": "etl-bronze-spot",
    "spark_version": "14.x-scala2.12",
    "node_type_id": "Standard_DS3_v2",
    "num_workers": 4,
    "autotermination_minutes": 10,
    "enable_elastic_disk": True,
    "aws_attributes": {  # ou azure_attributes
        "first_on_demand": 1,
        "availability": "SPOT_WITH_FALLBACK"
    }
}
```

**ROI:**
- Esforço: 2 horas (configuração + teste)
- Economia: $228/ano
- ROI: **114x** (assumindo $2/hora de esforço)

**Riscos:**
- ⚠️ Spot preemption pode atrasar jobs em horários de pico
- ✅ Mitigação: fallback para on-demand automático

---

### Oportunidade #2: Otimizar SQL Warehouse - Auto-Stop 🔴 P0

**Problema:**
- SQL Warehouse representa $44/mês (41% do Databricks)
- Uso estimado: ~100 hrs/mês
- Possível idle time não configurado adequadamente

**Solução:**
- Reduzir auto-stop de 10 min → **5 min**
- Configurar scaling mais agressivo

**Economia Projetada:**
```
Cenário: 20% do tempo é idle (pode ser desligado)
Atual:     $44.00/mês (100hrs com 10min auto-stop)
Otimizado: $35.00/mês (80hrs efetivo com 5min auto-stop)
───────────────────────────────────
ECONOMIA:  $9.00/mês (~$108/ano)
```

**Implementação:**
```sql
-- No Databricks UI: SQL Warehouses → Edit
{
  "auto_stop_mins": 5,  -- reduzir de 10 para 5
  "min_num_clusters": 1,
  "max_num_clusters": 2,  -- reduzir de 8 para 2 (MVP não precisa mais)
  "enable_serverless_compute": true
}
```

**Ações:**
1. ⚠️ **Validar uso real** - Revisar métricas de utilização do Warehouse
2. Ajustar auto-stop baseado em padrões reais
3. Considerar migrar queries pesadas para job clusters

**ROI:**
- Esforço: 1 hora (configuração + validação)
- Economia: $108/ano
- ROI: **108x**

---

### Oportunidade #3: Reduzir Retenção de Logs (Azure Monitor) 🟡 P1

**Problema:**
- Azure Monitor: $27.60/mês (49% do custo infra)
- Retenção configurada: A DEFINIR (padrão 30 dias?)

**Solução:**
- Reduzir para **7 dias** de retenção (suficiente para troubleshooting)
- Exportar logs históricos para ADLS (custo muito menor)

**Economia Projetada:**
```
Assumindo redução de 30d → 7d (77% menos retenção):
Atual:     $27.60/mês (30 dias)
Otimizado: $10.00/mês (7 dias + export para ADLS)
───────────────────────────────────
ECONOMIA:  $17.60/mês (~$211/ano)
```

**Implementação:**
```bash
# Azure CLI: Configurar retenção no workspace
az monitor log-analytics workspace update \
  --resource-group rg-nyctaxi \
  --name law-nyctaxi \
  --retention-time 7

# Configurar export para ADLS
az monitor log-analytics workspace data-export create \
  --resource-group rg-nyctaxi \
  --workspace-name law-nyctaxi \
  --name export-to-adls \
  --destination adls-nyctaxi \
  --tables ["AzureDatabricks", "AzureMetrics"]
```

**Ações:**
1. ⚠️ **Confirmar retenção atual** (verificar no portal Azure)
2. Verificar requirements de compliance/auditoria
3. Implementar export para ADLS antes de reduzir retenção

**ROI:**
- Esforço: 3 horas (configuração + validação)
- Economia: $211/ano
- ROI: **70x**

---

### Oportunidade #4: Reserved Capacity (1 ano) 🟢 P2

**Problema:**
- Databricks pago on-demand (~$108/mês)
- Workload é previsível (diário, estável)

**Solução:**
- Comprar **Reserved Capacity** (1 ano pré-pago)
- Desconto típico: 15-20%

**Economia Projetada:**
```
Assumindo 15% de desconto:
Atual:     $108.00/mês × 12 = $1,296/ano
Otimizado: $91.80/mês × 12 = $1,101/ano (pago upfront)
───────────────────────────────────
ECONOMIA:  $16.20/mês (~$195/ano)
```

**Considerações:**
- ⚠️ Requer compromisso de 1 ano
- ⚠️ Pagamento upfront (~$1,101)
- ✅ Workload é estável, baixo risco

**Ações:**
1. Validar com stakeholders (commitment de 1 ano)
2. Confirmar desconto atual com Microsoft/Databricks
3. Avaliar crescimento do projeto (pode precisar de mais capacity)

**ROI:**
- Esforço: 4 horas (análise + procurement)
- Economia: $195/ano
- ROI: **49x**

---

### Oportunidade #5: Eliminar Private Endpoints Desnecessários 🟢 P3

**Problema:**
- 3 Private Endpoints: $21.90/mês (39% do custo infra)
- Possível over-engineering para MVP

**Solução:**
- Avaliar se todos os 3 endpoints são necessários
- Consolidar ou usar service endpoints (grátis)

**Economia Projetada:**
```
Cenário: Reduzir de 3 → 1 endpoint (manter apenas Databricks)
Atual:     $21.90/mês (3 endpoints)
Otimizado: $7.30/mês (1 endpoint)
───────────────────────────────────
ECONOMIA:  $14.60/mês (~$175/ano)
```

**⚠️ Validação Necessária:**
- Verificar requirements de segurança
- Confirmar se há mandato de private networking
- Avaliar impacto em compliance

**Ações:**
1. Listar endpoints atuais e seus usos
2. Avaliar se service endpoints são suficientes
3. Discutir com time de segurança

**ROI:**
- Esforço: 2 horas (análise de segurança)
- Economia: $175/ano
- ROI: **87x** (se aprovado por segurança)

---

## 📊 Consolidado de Otimizações

| # | Oportunidade | Prioridade | Esforço | Economia/Ano | ROI |
|---|--------------|------------|---------|--------------|-----|
| 1 | Spot Instances | 🔴 P0 | 2h | $228 | 114x |
| 2 | SQL Warehouse Auto-Stop | 🔴 P0 | 1h | $108 | 108x |
| 3 | Logs Retention | 🟡 P1 | 3h | $211 | 70x |
| 4 | Reserved Capacity | 🟢 P2 | 4h | $195 | 49x |
| 5 | Private Endpoints | 🟢 P3 | 2h | $175 | 87x |
| **TOTAL** | | | **12h** | **$917/ano** | **76x** |

**Economia Total Projetada:**
```
Custo Atual:     $214.60/mês × 12 = $2,575/ano
Custo Otimizado: $137.95/mês × 12 = $1,655/ano
───────────────────────────────────────────────
ECONOMIA TOTAL:  $76.65/mês = $920/ano (36%)
```

---

## 🎯 Implementação - Fase 1 (Próximas 2 semanas)

### Quick Wins (P0 - Esta semana)

| Ação | Owner | Deadline | Economia |
|------|-------|----------|----------|
| Configurar Spot Instances para Bronze/Gold | A DEFINIR | A DEFINIR | $228/ano |
| Otimizar SQL Warehouse auto-stop (10min → 5min) | A DEFINIR | A DEFINIR | $108/ano |
| **SUBTOTAL Quick Wins** | | | **$336/ano** |

### Medium Priority (P1 - Próximas 2 semanas)

| Ação | Owner | Deadline | Economia |
|------|-------|----------|----------|
| Validar retenção atual do Azure Monitor | A DEFINIR | A DEFINIR | - |
| Reduzir retenção de logs (30d → 7d) | A DEFINIR | A DEFINIR | $211/ano |
| Configurar export de logs para ADLS | A DEFINIR | A DEFINIR | - |
| **SUBTOTAL P1** | | | **$211/ano** |

---

## 📈 Métricas de Acompanhamento

### KPIs de Custo (Monitorar mensalmente)

| KPI | Baseline | Target | Métrica |
|-----|----------|--------|---------|
| **Custo Total Mensal** | $214.60 | $160.00 | ⬇️ -25% |
| **Custo por Pipeline Run** | A DEFINIR | A DEFINIR | TBD |
| **Custo por TB processado** | A DEFINIR | A DEFINIR | TBD |
| **% Idle Time (SQL Warehouse)** | A DEFINIR | <10% | TBD |
| **Spot Preemption Rate** | 0% | <5% | TBD |

> ⚠️ **Nota:** Métricas marcadas como "A DEFINIR" requerem dados de billing real do Azure para baseline.

---

## 🛠️ Próximos Passos

### Imediato (Esta semana)
1. [ ] **Validar custos reais** - Acessar Azure Cost Management e confirmar valores estimados
2. [ ] **Configurar cost tracking tags** - Tag recursos por layer (bronze/silver/gold)
3. [ ] **Implementar Quick Wins** - Spot instances + SQL Warehouse auto-stop

### Curto prazo (Próximas 2 semanas)
4. [ ] **Criar dashboard de custo** - Monitoramento contínuo no Azure Monitor
5. [ ] **Reduzir retenção de logs** - Implementar com export para ADLS
6. [ ] **Estabelecer budget alerts** - Alertas em 80%, 90%, 100% do budget

### Médio prazo (Próximo mês)
7. [ ] **Avaliar Reserved Capacity** - Análise de commitment de 1 ano
8. [ ] **Revisar Private Endpoints** - Discussão com time de segurança
9. [ ] **Otimização de queries** - Review de queries lentas no SQL Warehouse

---

## 📚 Referências

- [Azure Databricks Pricing](https://azure.microsoft.com/en-us/pricing/details/databricks/)
- [Databricks Spot Instances Best Practices](https://docs.databricks.com/clusters/cluster-config-best-practices.html#use-spot-instances)
- [Azure Monitor Pricing](https://azure.microsoft.com/en-us/pricing/details/monitor/)
- [ADLS Gen2 Pricing](https://azure.microsoft.com/en-us/pricing/details/storage/data-lake/)
- [Architecture Document](../architecture/architecture.md) - Seção 10: Cost Estimates

---

## 📝 Changelog

| Versão | Data | Autor | Mudanças |
|--------|------|-------|----------|
| 1.0 | 2026-02-05 | Kai (IterationImprovement) | Versão inicial com 5 oportunidades |

---

**Criado por:** Kai 🔁 (IterationImprovement)  
**Data:** 2026-02-05  
**Status:** ✅ Completo - Aguardando validação de custos reais

---

*"Cost optimization is not about cutting corners, it's about eliminating waste while maintaining quality."*
