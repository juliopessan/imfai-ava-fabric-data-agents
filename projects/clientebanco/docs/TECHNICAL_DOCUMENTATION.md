# 🏗️ Visão Geral Técnica — ClienteBanco Data Migration Agents

> Arquitetura, componentes, fluxos e stack técnico do suite de agentes de migração de dados.

---

## 📑 Índice

1. [Arquitetura Geral](#arquitetura-geral)
2. [Componentes Principais](#componentes-principais)
3. [Stack Técnico (100% Microsoft)](#stack-técnico-100-microsoft)
4. [Fluxos de Dados](#fluxos-de-dados)
5. [Segurança & Identidade](#segurança--identidade)
6. [Observabilidade](#observabilidade)
7. [Escalabilidade](#escalabilidade)

---

## Arquitetura Geral

### Visão Macro

```
┌─────────────────────────────────────────────────────────────────┐
│                    CLIENTE (On-Premises/Cloud)                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Sistemas Legados (DB, ERP, Data Lake)                  │  │
│  │  ↓                                                        │  │
│  │  [Connector Agent] ← Padrão A/B/C                        │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                      ↓ (SAS/Credential/PrivateLink)
┌─────────────────────────────────────────────────────────────────┐
│              CONSULTORIA AZURE (VNet Injetado)                      │
│                                                                 │
│  ┌──────────────────┐         ┌──────────────────┐            │
│  │  Landing Zone    │         │  Orchestrator    │            │
│  │  (ADLS Gen2)     │────────→│  (Service Bus)   │            │
│  └──────────────────┘         └──────────────────┘            │
│         ↓                            ↓                          │
│  ┌──────────────────┐         ┌──────────────────┐            │
│  │  Agents          │         │  Agents          │            │
│  │  (Foundry)       │         │  (Foundry)       │            │
│  │  • Discovery     │         │  • Transform     │            │
│  │  • Validation    │         │  • Migrate       │            │
│  │  • Cleanse       │         │  • Validate      │            │
│  └──────────────────┘         └──────────────────┘            │
│         ↓                            ↓                          │
│  ┌──────────────────┐         ┌──────────────────┐            │
│  │  Staging         │         │  Target          │            │
│  │  (ADLS Gen2)     │────────→│  (Databricks)    │            │
│  └──────────────────┘         └──────────────────┘            │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Observability: Monitor + Application Insights            │  │
│  │  Security: Key Vault, Managed Identity, Private Link     │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                      ↓ (Leitura: Dashboards)
┌─────────────────────────────────────────────────────────────────┐
│              PORTAL & DASHBOARDS (HTML5 + CDN)                  │
│  • Portal Hub (INDEX.html)                                      │
│  • Proposta Comercial (1-page)                                  │
│  • Calculadora de Esforço                                       │
│  • Dashboard Executivo                                          │
│  • Dashboard Operacional (3-view: Upstream/Mid/Down)           │
└─────────────────────────────────────────────────────────────────┘
```

---

## Componentes Principais

### 1. **Connector Agent** (Cliente)
- **Função:** Extrai dados read-only do ambiente cliente
- **Tipo:** Binário compilado (sem código-fonte)
- **Distribuição:** Wheel/NPM privado com autenticação de licença
- **Credenciais:** Armazenadas apenas em memória, nunca em disco
- **Segurança:** SAS token escrito, TTL 24h, rotação automática

**Responsabilidades:**
```
Input:  Client DB connection → Query specs
Process: Read-only scan → Data extraction → Hashing
Output: Stream → SAS upload → Landing Zone
```

### 2. **Landing Zone** (ADLS Gen2)
- **Função:** Zona de staging para dados brutos do cliente
- **Isolamento:** Prefixo de tenant, isolamento de rede via NSG
- **Lifecycle:** TTL automático para arquivos > 30 dias
- **Auditoria:** Todos os acessos logados no Azure Monitor

**Estrutura:**
```
/landing/{tenant-id}/
  ├── raw/
  │   ├── {connector-run-id}/
  │   │   ├── inventory.json
  │   │   ├── schemas.json
  │   │   └── data-sample.parquet
  │   └── ...
  ├── processed/
  │   ├── validated/
  │   └── transformed/
  └── archive/
```

### 3. **Orchestrator** (Service Bus)
- **Função:** Orquestração de jobs de migração
- **Padrão:** Publisher-subscriber com dead-letter queues
- **Retry:** Exponential backoff, max 3 tentativas
- **Timeout:** 1h por job, escalação automática

**Fluxo de Job:**
```
Trigger → Parse Config → Dequeue → Run Agents → Log Result → Callback
```

### 4. **Foundry Agents** (Compute)
- **Plataforma:** Azure AI Foundry
- **Framework:** Semantic Kernel
- **Deployment:** Container Apps (stateless, VNet-injected)
- **Escalabilidade:** Auto-scale 1-100 instâncias

**Agentes Principais:**
```
├── Discovery Agent
│   ├── Análise de estrutura
│   ├── Catalogação de assets
│   └── Risco/Conformidade
├── Transform Agent
│   ├── Schema mapping
│   ├── Regras de transformação
│   └── Lineage tracking
├── Validate Agent
│   ├── Reconciliação
│   ├── Quality checks
│   └── Alertas
└── Monitor Agent
    ├── Performance tracking
    ├── Anomaly detection
    └── Cost optimization
```

### 5. **Dashboards** (Observability)
- **Frontend:** HTML5 + CSS3 tokens (Consultoria Design System v2.0)
- **Backend:** Azure Monitor KQL queries
- **Refresh:** Near-real-time (30s)
- **Disponibilidade:** 99.95% SLA

**Tipos de Dashboards:**
| Dashboard | Propósito | Público |
|-----------|-----------|---------|
| Executivo | ROI, timeline, value | C-level |
| Operacional | Throughput, latência, erros | Ops, Devs |
| Técnico | Agent logs, system health | SRE |
| Financeiro | Custo por pipeline, ROI | Finance |

---

## Stack Técnico (100% Microsoft)

### Compute & Orchestration

| Componente | Serviço | Função |
|-----------|---------|--------|
| **Agentes** | Azure AI Foundry | Deployment e execução |
| **Orquestração** | Semantic Kernel | Framework de fluxos |
| **Compute** | Azure Container Apps | VNet-injected, stateless |
| **Jobs** | Service Bus | Fila e retry logic |

### Storage & Data

| Componente | Serviço | Função |
|-----------|---------|--------|
| **Landing** | ADLS Gen2 | Dados brutos cliente |
| **Staging** | ADLS Gen2 | Processamento intermediário |
| **Target** | Databricks | Destino final |
| **Config** | Cosmos DB | Metadata e estado |

### Security & Identity

| Componente | Serviço | Função |
|-----------|---------|--------|
| **Auth** | Entra ID | Autenticação principal |
| **Identidade** | Managed Identity | Acesso sem senha |
| **Secrets** | Key Vault | Credenciais encriptadas |
| **Rede** | Private Link | Conectividade air-gapped |
| **Firewall** | Application Gateway | WAF e rate limiting |

### Observability & Monitoring

| Componente | Serviço | Função |
|-----------|---------|--------|
| **Logs** | Log Analytics | Centralização de logs |
| **Telemetria** | Application Insights | Tracing distribuído |
| **Alertas** | Monitor | Notificações automáticas |
| **Consultas** | KQL | Análise ad-hoc |

### DevOps & Deployment

| Componente | Serviço | Função |
|-----------|---------|--------|
| **Versionamento** | GitHub Enterprise | Controle de versão |
| **CI/CD** | Azure DevOps Pipelines | Automação de build/deploy |
| **IaC** | Bicep | Infraestrutura como código |
| **Secrets** | Key Vault | Gestão de credenciais |

---

## Fluxos de Dados

### Fluxo 1: Ingestão (Push Pattern - Padrão A)

```
1. [CLIENTE]
   ├─ Installer: Deploy Connector Agent
   ├─ License: Autenticação com license key
   └─ Config: Especificar fontes de dados

2. [CONNECTOR AGENT]
   ├─ ReadOnly: Conecta aos sistemas legados
   ├─ Extract: Copia dados brutos (read-only)
   ├─ Hash: Calcula MD5 para validação
   └─ Upload: SAS token → Landing Zone

3. [LANDING ZONE]
   ├─ Store: ADLS Gen2 /landing/{tenant}/raw/
   ├─ Audit: Log de acesso
   └─ Trigger: Event Grid → Service Bus

4. [ORCHESTRATOR]
   ├─ Dequeue: Job do Service Bus
   ├─ Route: Direciona ao Agent apropriado
   └─ Execute: Inicia pipeline de transformação
```

### Fluxo 2: Transformação

```
1. [DISCOVERY AGENT]
   ├─ Parse: Analisa estrutura de dados
   ├─ Catalog: Cria inventário de assets
   ├─ Lineage: Rastreia dependências
   └─ Output: Metadata → Cosmos DB

2. [TRANSFORM AGENT]
   ├─ Schema Mapping: Regras de mapeamento
   ├─ Data Cleansing: Limpeza e normalizaçãoExecute: Semantic Kernel scripts
   └─ Output: Dados transformados → Staging

3. [VALIDATE AGENT]
   ├─ Row Count: Reconciliação de linhas
   ├─ MD5 Check: Validação de integridade
   ├─ Quality: Data quality rules
   └─ Output: Relatório → Cosmos DB
```

### Fluxo 3: Publicação

```
1. [TARGET DB]
   ├─ Databricks: Carregamento final
   ├─ Post-check: Validação no destino
   └─ Callback: Notificação de sucesso

2. [OBSERVABILITY]
   ├─ Metrics: KPIs para dashboards
   ├─ Logs: Rastreamento de execução
   └─ Alerts: Notificações de anomalias
```

---

## Segurança & Identidade

### Autenticação

```
┌─────────────────┐
│  Cliente        │
│  (Entra ID)     │
└────────┬────────┘
         │ Service Principal
         ↓
┌─────────────────────────────────┐
│  Foundry                        │
│  Managed Identity               │
│  (No password, no secrets)      │
└────────┬────────────────────────┘
         │ Acesso:
         ├─→ ADLS Gen2 (Landing)
         ├─→ Service Bus (Orchestrator)
         ├─→ Key Vault (Secrets)
         └─→ Databricks (Target)
```

### Autorização (RBAC)

| Identidade | Permissões | Escopo |
|-----------|-----------|--------|
| **Connector Agent** | ReadOnly (cliente) | Client DB |
| **Landing Zone** | Write | `/landing/{tenant}` |
| **Foundry Agents** | Read/Write | `/landing/{tenant}` + Staging |
| **Target DB** | Write | Databricks schemas |
| **Monitoring** | Read | Logs/Metrics |

### Criptografia

```
┌─ Em Trânsito
│  ├─ TLS 1.2+ (HTTPS only)
│  ├─ Azure Service Bus encryption
│  └─ Private Link (no Internet)
│
└─ Em Repouso
   ├─ ADLS Gen2 (SMB encryption)
   ├─ Key Vault (AES-256)
   ├─ Cosmos DB (automatic)
   └─ Databricks (encryption at rest)
```

---

## Observabilidade

### Métricas Principais

```
KPI: Throughput
├─ Rows/hour: Velocidade de ingestão
├─ MB/sec: Taxa de dados
└─ Pipeline duration: Tempo total

KPI: Quality
├─ Row count match %: Reconciliação
├─ MD5 hash match %: Integridade
└─ Data anomalies: Detecção

KPI: Cost
├─ $/pipeline: Custo unitário
├─ $/row: Custo por registro
└─ ROI: Economia vs. manual
```

### Logging

```
Agent Activity Logs (App Insights)
├─ Agent name
├─ Start/end timestamp
├─ Input rows
├─ Output rows
├─ Duration (ms)
└─ Error (if any)

Data Lineage (Cosmos DB)
├─ Source table
├─ Transformations applied
├─ Target table
└─ Execution timestamp
```

### Alertas

| Alerta | Condição | Escalação |
|-------|----------|-----------|
| **Job Timeout** | > 1h | Slack + PagerDuty |
| **High Error Rate** | > 5% | Log Analytics KQL |
| **Data Drift** | Anomalia > 2σ | Alert Rules |
| **Cost Spike** | > Budget | Email + Azure Advisor |

---

## Escalabilidade

### Horizontal (Compute)

```
Container Apps Auto-scale:
├─ Min: 1 instance
├─ Max: 100 instances
├─ Trigger: CPU > 70% OR Memory > 80%
└─ Cooldown: 60s

Service Bus:
├─ Standard tier: 1GB/day throughput
├─ Premium tier: Unlimited (reservado)
└─ Partitions: 32 (max throughput)
```

### Vertical (Storage)

```
ADLS Gen2:
├─ Unlimited scale (petabytes)
├─ Partitioning: /landing/{tenant}/year/month/day/
└─ Performance: 20Gbps throughput

Databricks:
├─ Auto-scaling clusters
├─ Spot instances: Cost optimization
└─ Partitioned delta tables: Query performance
```

### Data Retention

```
Policy:
├─ Landing zone: 30 dias (auto-delete)
├─ Staging: 7 dias (archive to cool)
├─ Target (Databricks): Indefinido
└─ Logs: 90 dias (Log Analytics)
```

---

## Configuração Recomendada

### Desenvolvimento

```yaml
Environment: dev
ContainerApps:
  instances: 1-5
  cpu: 0.5
  memory: 1Gi
  
ADLS:
  tier: Standard
  redundancy: LRS
  
Databricks:
  cluster: all-purpose
  nodes: 2-4 (spot)
```

### Produção

```yaml
Environment: prod
ContainerApps:
  instances: 3-100
  cpu: 2
  memory: 4Gi
  availability_zones: 3
  
ADLS:
  tier: Premium
  redundancy: GRS
  
Databricks:
  cluster: high-concurrency
  nodes: 4-32 (mix reserved+spot)
  autoscaling: true
```

---

## Próximos Passos

1. ✅ Leia [Guia de Integração](INTEGRATION_GUIDE.md) para setup prático
2. ✅ Consulte [Blueprint](BLUEPRINT_GUIDE.md) para escolher padrão de conexão
3. ✅ Valide com [Referência de APIs](API_REFERENCE.md)
4. ✅ Implemente [Best Practices](BEST_PRACTICES.md)

---

**Última atualização:** 2026-06-12 | **Status:** ✅ Produção | **Mantido por:** Arquitetura Consultoria
