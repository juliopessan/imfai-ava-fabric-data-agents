# 🎯 Plano de Integração: Azure Databricks + MCP + Agentes

**Data:** 4 de Fevereiro de 2026  
**Status:** 📋 Em Implementação  
**Versão:** 1.0  
**Autor:** Master Agent + Data Engineering Team

---

## 📋 Índice

1. [Visão Geral](#1-visão-geral)
2. [Problema a Resolver](#2-problema-a-resolver)
3. [Arquitetura Escolhida](#3-arquitetura-escolhida)
4. [MCP Selecionado](#4-mcp-selecionado)
5. [Decisão sobre Scripts](#5-decisão-sobre-scripts)
6. [Fluxo de Trabalho](#6-fluxo-de-trabalho)
7. [Configurações Necessárias](#7-configurações-necessárias)
8. [Integração com Agentes](#8-integração-com-agentes)
9. [Cronograma de Implementação](#9-cronograma-de-implementação)
10. [Referências](#10-referências)

---

## 1. Visão Geral

### 1.1 Objetivo Principal

Criar uma integração **100% agêntica** entre o VS Code e o Azure Databricks, permitindo que os agentes de dados (DataStrategist, DataArchitect, DataSteward, etc.) possam:

- ✅ Explorar catálogos, schemas e tabelas
- ✅ Executar queries SQL via linguagem natural
- ✅ Criar e modificar estruturas de dados
- ✅ Analisar lineage e dependências
- ✅ Trabalhar com dados em tempo real

### 1.2 Escopo

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           ESCOPO DO PROJETO                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ✅ INCLUÍDO:                                                               │
│     • Configuração do Azure Databricks                                      │
│     • Instalação e configuração do MCP Databricks                           │
│     • Upload de dados de teste (NYC Taxi)                                   │
│     • Criação de schemas Medallion (Bronze/Silver/Gold)                     │
│     • Integração MCP com VS Code                                            │
│     • Uso dos agentes existentes com dados Databricks                       │
│                                                                             │
│  ❌ FORA DO ESCOPO (por enquanto):                                          │
│     • Migração automatizada SQL Server → Databricks                         │
│     • Criação de novos agentes específicos para Databricks                  │
│     • Jobs agendados / Workflows Databricks                                 │
│     • Integração com Power BI                                               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Problema a Resolver

### 2.1 Situação Atual

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           ANTES (Situação Atual)                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  📁 Arquivos Locais              🤖 Agentes VS Code                         │
│  ┌─────────────────┐             ┌─────────────────┐                        │
│  │ CSV, JSON, TSV  │             │ DataStrategist  │                        │
│  │ (Files/)        │      ❌      │ DataArchitect   │                        │
│  │                 │◄─ ─ ─ ─ ─ ─►│ DataSteward     │                        │
│  └─────────────────┘  Sem conexão │ BizAnalyst     │                        │
│                                   └─────────────────┘                        │
│                                                                             │
│  ⚠️ PROBLEMAS:                                                              │
│     • Agentes não acessam dados em cloud                                    │
│     • Sem persistência (dados só em arquivos)                               │
│     • Sem capacidade de query SQL                                           │
│     • Análises limitadas a arquivos pequenos                                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Situação Desejada

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           DEPOIS (Situação Desejada)                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ☁️ Azure Databricks             🤖 Agentes VS Code                         │
│  ┌─────────────────┐             ┌─────────────────┐                        │
│  │ Unity Catalog   │             │ DataStrategist  │                        │
│  │ ├─ bronze.*     │      ✅      │ DataArchitect   │                        │
│  │ ├─ silver.*     │◄───────────►│ DataSteward     │                        │
│  │ ├─ gold.*       │     MCP     │ BizAnalyst      │                        │
│  │ └─ reference.*  │             └─────────────────┘                        │
│  └─────────────────┘                                                        │
│                                                                             │
│  ✅ BENEFÍCIOS:                                                             │
│     • Dados centralizados em cloud                                          │
│     • Queries SQL via linguagem natural                                     │
│     • Escalabilidade (terabytes de dados)                                   │
│     • Lineage e governança                                                  │
│     • 100% agêntico (conversacional)                                        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Arquitetura Escolhida

### 3.1 Diagrama de Arquitetura

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        ARQUITETURA DA SOLUÇÃO                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                         VS CODE (Local)                             │    │
│  │  ┌─────────────────────────────────────────────────────────────┐    │    │
│  │  │                    GITHUB COPILOT CHAT                      │    │    │
│  │  │                                                             │    │    │
│  │  │   User: "Mostre as 10 viagens mais caras"                   │    │    │
│  │  │                          │                                  │    │    │
│  │  │                          ▼                                  │    │    │
│  │  │   ┌─────────────────────────────────────────────────┐       │    │    │
│  │  │   │             MCP DATABRICKS SERVER               │       │    │    │
│  │  │   │                                                 │       │    │    │
│  │  │   │  Tools:                                         │       │    │    │
│  │  │   │  • execute_sql_query()                          │       │    │    │
│  │  │   │  • list_uc_catalogs()                           │       │    │    │
│  │  │   │  • describe_uc_table()                          │       │    │    │
│  │  │   │  • describe_uc_schema()                         │       │    │    │
│  │  │   │  • describe_uc_catalog()                        │       │    │    │
│  │  │   └─────────────────────────────────────────────────┘       │    │    │
│  │  │                          │                                  │    │    │
│  │  └──────────────────────────│──────────────────────────────────┘    │    │
│  └─────────────────────────────│───────────────────────────────────────┘    │
│                                │                                            │
│                                │ HTTPS + Token Auth                         │
│                                │                                            │
│  ┌─────────────────────────────▼───────────────────────────────────────┐    │
│  │                      AZURE DATABRICKS                               │    │
│  │  ┌─────────────────────────────────────────────────────────────┐    │    │
│  │  │                    SQL WAREHOUSE                            │    │    │
│  │  │                    (Serverless)                             │    │    │
│  │  └─────────────────────────────────────────────────────────────┘    │    │
│  │                                │                                    │    │
│  │                                ▼                                    │    │
│  │  ┌─────────────────────────────────────────────────────────────┐    │    │
│  │  │                    UNITY CATALOG                            │    │    │
│  │  │                                                             │    │    │
│  │  │   main (catalog)                                            │    │    │
│  │  │   ├── bronze (schema)                                       │    │    │
│  │  │   │   └── taxi_trips_raw (table)                            │    │    │
│  │  │   ├── silver (schema)                                       │    │    │
│  │  │   │   └── taxi_trips (table)                                │    │    │
│  │  │   ├── gold (schema)                                         │    │    │
│  │  │   │   └── daily_summary (table)                             │    │    │
│  │  │   └── reference (schema)                                    │    │    │
│  │  │       ├── payment_types (table)                             │    │    │
│  │  │       ├── rate_codes (table)                                │    │    │
│  │  │       └── trip_types (table)                                │    │    │
│  │  └─────────────────────────────────────────────────────────────┘    │    │
│  │                                │                                    │    │
│  │                                ▼                                    │    │
│  │  ┌─────────────────────────────────────────────────────────────┐    │    │
│  │  │                    DELTA LAKE (Storage)                     │    │    │
│  │  │                    DBFS / ADLS Gen2                         │    │    │
│  │  └─────────────────────────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Componentes

| Componente | Tecnologia | Função |
|------------|------------|--------|
| **VS Code** | Editor | Interface do usuário + Agentes |
| **GitHub Copilot** | LLM | Processamento de linguagem natural |
| **MCP Server** | Python | Bridge entre Copilot e Databricks |
| **Azure Databricks** | PaaS | Plataforma de dados em cloud |
| **SQL Warehouse** | Compute | Execução de queries |
| **Unity Catalog** | Metastore | Governança e catálogo |
| **Delta Lake** | Storage | Armazenamento de dados |

---

## 4. MCP Selecionado

### 4.1 Escolha: RafaelCartenet/mcp-databricks-server

**Repositório:** https://github.com/RafaelCartenet/mcp-databricks-server

### 4.2 Justificativa da Escolha

| Critério | RafaelCartenet MCP | JordiNeil MCP |
|----------|-------------------|---------------|
| **Stars GitHub** | 35 ⭐ | 46 ⭐ |
| **Última atualização** | ~1 semana ✅ | ~11 meses ⚠️ |
| **SDK usado** | Oficial Databricks ✅ | SQL Connector |
| **Autenticação** | PAT + OAuth M2M ✅ | Apenas PAT |
| **Unity Catalog** | Completo ✅ | Básico |
| **Lineage** | Sim ✅ | Não |
| **Decisão** | **ESCOLHIDO** ✅ | Descartado |

### 4.3 Tools Disponíveis

```python
# Tools do MCP RafaelCartenet

@mcp.tool()
async def execute_sql_query(sql: str) -> str:
    """Executa qualquer SQL no Databricks"""
    
@mcp.tool()
async def list_uc_catalogs() -> str:
    """Lista todos os Unity Catalogs disponíveis"""
    
@mcp.tool()
async def describe_uc_catalog(catalog_name: str) -> str:
    """Detalha schemas de um catálogo"""
    
@mcp.tool()
async def describe_uc_schema(catalog_name: str, schema_name: str, include_columns: bool = False) -> str:
    """Lista tabelas de um schema"""
    
@mcp.tool()
async def describe_uc_table(full_table_name: str, include_lineage: bool = False) -> str:
    """Detalha estrutura de uma tabela + lineage opcional"""
```

### 4.4 Auditoria de Segurança

**Status:** ✅ Aprovado para uso

| Item | Status | Observação |
|------|--------|------------|
| Usa SDK oficial | ✅ | `databricks-sdk==0.77.0` |
| Variáveis ambiente | ✅ | Via `.env` (dotenv) |
| Sem hardcoded secrets | ✅ | Verificado |
| OAuth M2M suportado | ✅ | Mais seguro que PAT |
| Código auditado | ✅ | ~500 linhas, limpo |

---

## 5. Decisão sobre Scripts

### 5.1 Scripts Existentes (azure-databricks-integration/)

```
📁 azure-databricks-integration/
├── 01-provision-azure/
│   └── provision-databricks.ps1        ❌ NÃO USAR (já criamos via Portal)
├── 02-configure-databricks/
│   └── setup-databricks-cli.ps1        ❌ NÃO USAR (MCP substitui)
├── 03-database-setup/
│   ├── create-schemas.sql              📖 REFERÊNCIA (SQL útil)
│   ├── create-tables.sql               📖 REFERÊNCIA (SQL útil)
│   └── execute-ddl.ps1                 ❌ NÃO USAR (MCP substitui)
├── 04-data-ingestion/
│   ├── ingest-from-csv-universal.py    ❌ NÃO USAR (upload via interface)
│   ├── ingest-from-json.py             ❌ NÃO USAR
│   ├── ingest-from-api.py              ❌ NÃO USAR
│   └── execute-sql-via-api.py          ❌ NÃO USAR (MCP substitui)
└── 05-orchestration/
    ├── run-all.ps1                     ❌ NÃO USAR
    └── run-modular.ps1                 ❌ NÃO USAR
```

### 5.2 Decisão Final

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        DECISÃO: MCP ONLY                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ❌ NÃO EXECUTAR scripts Python/PowerShell                                  │
│                                                                             │
│  ✅ USAR MCP para:                                                          │
│     • Criar schemas (via execute_sql_query)                                 │
│     • Criar tabelas (via execute_sql_query)                                 │
│     • Executar queries (via execute_sql_query)                              │
│     • Explorar estrutura (via describe_uc_*)                                │
│                                                                             │
│  ✅ USAR Interface Web Databricks para:                                     │
│     • Upload de arquivos CSV/JSON (uma vez)                                 │
│                                                                             │
│  📖 MANTER scripts como REFERÊNCIA:                                         │
│     • create-schemas.sql → SQL para criar schemas                           │
│     • create-tables.sql → SQL para criar tabelas                            │
│     • Documentação da estrutura Medallion                                   │
│                                                                             │
│  RESULTADO:                                                                 │
│  ═══════════                                                                │
│  • 0 scripts para executar                                                  │
│  • 0 dependências Python adicionais                                         │
│  • 100% agêntico (via chat)                                                 │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Fluxo de Trabalho

### 6.1 Setup Inicial (Uma Vez)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        FASE 1: SETUP AZURE DATABRICKS                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Passo 1.1: Criar Workspace (Portal Azure)                                  │
│  ─────────────────────────────────────────                                  │
│  • Azure Portal → Create Resource → "Azure Databricks"                      │
│  • Subscription: [sua subscription]                                         │
│  • Resource Group: rg-databricks-teste                                      │
│  • Workspace name: dbw-avanade-teste                                        │
│  • Region: Brazil South ou East US                                          │
│  • Pricing: Trial (14 dias Premium grátis)                                  │
│  • [Create] → Aguardar ~5 minutos                                           │
│                                                                             │
│  Passo 1.2: Criar SQL Warehouse                                             │
│  ──────────────────────────────                                             │
│  • Launch Workspace → SQL Warehouses → Create                               │
│  • Name: sql-warehouse-teste                                                │
│  • Size: 2X-Small (mais barato)                                             │
│  • Auto stop: 10 minutes                                                    │
│  • [Create] → Aguardar ficar Running                                        │
│                                                                             │
│  Passo 1.3: Gerar Token                                                     │
│  ──────────────────────                                                     │
│  • User Settings → Developer → Access Tokens → Generate                     │
│  • Comment: "MCP VS Code"                                                   │
│  • Lifetime: 90 days                                                        │
│  • ⚠️ COPIAR TOKEN IMEDIATAMENTE                                            │
│                                                                             │
│  Passo 1.4: Anotar Credenciais                                              │
│  ────────────────────────────                                               │
│  • DATABRICKS_HOST: adb-XXXXX.X.azuredatabricks.net                         │
│  • DATABRICKS_TOKEN: dapi_XXXXXXXXXXXXX                                     │
│  • DATABRICKS_SQL_WAREHOUSE_ID: XXXXXXXXXXXX                                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                        FASE 2: UPLOAD DE DADOS                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Passo 2.1: Upload via Interface Web                                        │
│  ─────────────────────────────────                                          │
│  • Databricks Workspace → Data → DBFS → FileStore                           │
│  • Criar pasta: data-agents                                                 │
│  • Upload arquivos:                                                         │
│    - green_tripdata_2021-04.csv                                             │
│    - green_tripdata_2021-05.csv                                             │
│    - green_tripdata_2021-06.csv                                             │
│    - rate_code.json                                                         │
│    - payment_type_array.json                                                │
│    - trip_type.tsv                                                          │
│                                                                             │
│  Passo 2.2: Verificar Upload                                                │
│  ─────────────────────────                                                  │
│  • Arquivos devem estar em: dbfs:/FileStore/data-agents/                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                        FASE 3: CONFIGURAR MCP                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Passo 3.1: Clonar repositório MCP                                          │
│  ────────────────────────────────                                           │
│  cd C:\Users\e.a.de.albuquerque\Documents                                   │
│  git clone https://github.com/RafaelCartenet/mcp-databricks-server.git      │
│                                                                             │
│  Passo 3.2: Instalar dependências                                           │
│  ────────────────────────────────                                           │
│  cd mcp-databricks-server                                                   │
│  python -m venv .venv                                                       │
│  .\.venv\Scripts\Activate                                                   │
│  pip install -r requirements.txt                                            │
│                                                                             │
│  Passo 3.3: Configurar credenciais                                          │
│  ─────────────────────────────────                                          │
│  Criar arquivo .env:                                                        │
│  ┌─────────────────────────────────────────────────────────────┐            │
│  │ DATABRICKS_HOST=adb-XXXXX.X.azuredatabricks.net             │            │
│  │ DATABRICKS_TOKEN=dapi_XXXXXXXXXXXXX                         │            │
│  │ DATABRICKS_SQL_WAREHOUSE_ID=XXXXXXXXXXXX                    │            │
│  └─────────────────────────────────────────────────────────────┘            │
│                                                                             │
│  Passo 3.4: Configurar VS Code                                              │
│  ─────────────────────────────                                              │
│  Editar settings.json:                                                      │
│  ┌─────────────────────────────────────────────────────────────┐            │
│  │ {                                                           │            │
│  │   "mcp.servers": {                                          │            │
│  │     "databricks": {                                         │            │
│  │       "command": "python",                                  │            │
│  │       "args": ["C:\\...\\mcp-databricks-server\\main.py"],  │            │
│  │       "env": {                                              │            │
│  │         "DATABRICKS_HOST": "adb-XXXXX...",                  │            │
│  │         "DATABRICKS_TOKEN": "dapi_...",                     │            │
│  │         "DATABRICKS_SQL_WAREHOUSE_ID": "..."                │            │
│  │       }                                                     │            │
│  │     }                                                       │            │
│  │   }                                                         │            │
│  │ }                                                           │            │
│  └─────────────────────────────────────────────────────────────┘            │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 6.2 Criação de Estrutura (Via MCP/Chat)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        FASE 4: CRIAR ESTRUTURA VIA MCP                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Usuário diz no chat:                                                       │
│  ────────────────────                                                       │
│                                                                             │
│  "Crie os schemas bronze, silver, gold e reference no Databricks"           │
│                                                                             │
│  MCP executa:                                                               │
│  ────────────                                                               │
│  CREATE SCHEMA IF NOT EXISTS bronze;                                        │
│  CREATE SCHEMA IF NOT EXISTS silver;                                        │
│  CREATE SCHEMA IF NOT EXISTS gold;                                          │
│  CREATE SCHEMA IF NOT EXISTS reference;                                     │
│                                                                             │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                             │
│  Usuário diz:                                                               │
│  ────────────                                                               │
│                                                                             │
│  "Crie uma tabela bronze.taxi_trips_raw a partir dos CSVs em                │
│   dbfs:/FileStore/data-agents/"                                             │
│                                                                             │
│  MCP executa:                                                               │
│  ────────────                                                               │
│  CREATE TABLE IF NOT EXISTS bronze.taxi_trips_raw                           │
│  USING CSV                                                                  │
│  OPTIONS (                                                                  │
│    path 'dbfs:/FileStore/data-agents/green_tripdata*.csv',                  │
│    header 'true',                                                           │
│    inferSchema 'true'                                                       │
│  );                                                                         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 6.3 Uso Diário (Exemplos)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        EXEMPLOS DE USO DIÁRIO                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  EXPLORAÇÃO:                                                                │
│  ───────────                                                                │
│  User: "Quais tabelas existem no schema bronze?"                            │
│  MCP:  describe_uc_schema("main", "bronze", include_columns=True)           │
│                                                                             │
│  User: "Mostre a estrutura da tabela taxi_trips_raw"                        │
│  MCP:  describe_uc_table("bronze.taxi_trips_raw", include_lineage=True)     │
│                                                                             │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                             │
│  ANÁLISE:                                                                   │
│  ────────                                                                   │
│  User: "Quantas viagens temos por mês?"                                     │
│  MCP:  execute_sql_query("""                                                │
│          SELECT month(lpep_pickup_datetime) as mes,                         │
│                 COUNT(*) as total_viagens                                   │
│          FROM bronze.taxi_trips_raw                                         │
│          GROUP BY 1 ORDER BY 1                                              │
│        """)                                                                 │
│                                                                             │
│  User: "Qual a viagem mais cara?"                                           │
│  MCP:  execute_sql_query("""                                                │
│          SELECT * FROM bronze.taxi_trips_raw                                │
│          ORDER BY total_amount DESC LIMIT 1                                 │
│        """)                                                                 │
│                                                                             │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                             │
│  TRANSFORMAÇÃO:                                                             │
│  ──────────────                                                             │
│  User: "Crie uma tabela silver com dados limpos (sem valores negativos)"    │
│  MCP:  execute_sql_query("""                                                │
│          CREATE TABLE silver.taxi_trips AS                                  │
│          SELECT * FROM bronze.taxi_trips_raw                                │
│          WHERE fare_amount > 0                                              │
│            AND trip_distance > 0                                            │
│            AND passenger_count > 0                                          │
│        """)                                                                 │
│                                                                             │
│  User: "Crie um resumo diário na camada gold"                               │
│  MCP:  execute_sql_query("""                                                │
│          CREATE TABLE gold.daily_summary AS                                 │
│          SELECT date(lpep_pickup_datetime) as data,                         │
│                 COUNT(*) as total_viagens,                                  │
│                 SUM(total_amount) as receita_total,                         │
│                 AVG(trip_distance) as distancia_media                       │
│          FROM silver.taxi_trips                                             │
│          GROUP BY 1                                                         │
│        """)                                                                 │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Configurações Necessárias

### 7.1 Credenciais Azure Databricks

```env
# Arquivo: mcp-databricks-server/.env

# Host do workspace (sem https://)
DATABRICKS_HOST=adb-XXXXXXXXXXXXXX.XX.azuredatabricks.net

# Personal Access Token (gerado em User Settings → Developer)
DATABRICKS_TOKEN=dapi_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# SQL Warehouse ID (encontrado em SQL Warehouses → Connection Details)
DATABRICKS_SQL_WAREHOUSE_ID=XXXXXXXXXXXXXXXX
```

### 7.2 Configuração VS Code (settings.json)

```json
{
  "mcp.servers": {
    "databricks": {
      "command": "python",
      "args": [
        "C:\\Users\\e.a.de.albuquerque\\Documents\\mcp-databricks-server\\main.py"
      ],
      "env": {
        "DATABRICKS_HOST": "adb-XXXXX.XX.azuredatabricks.net",
        "DATABRICKS_TOKEN": "dapi_XXXXX",
        "DATABRICKS_SQL_WAREHOUSE_ID": "XXXXX"
      }
    }
  }
}
```

### 7.3 Estrutura de Dados (Medallion)

```sql
-- Schemas
CREATE SCHEMA IF NOT EXISTS bronze;    -- Dados brutos
CREATE SCHEMA IF NOT EXISTS silver;    -- Dados limpos
CREATE SCHEMA IF NOT EXISTS gold;      -- Dados agregados
CREATE SCHEMA IF NOT EXISTS reference; -- Tabelas de lookup

-- Tabelas principais
bronze.taxi_trips_raw     -- CSV original
silver.taxi_trips         -- Dados validados
gold.daily_summary        -- Agregação diária
gold.vendor_summary       -- Agregação por vendor
reference.payment_types   -- Tipos de pagamento
reference.rate_codes      -- Códigos de tarifa
reference.trip_types      -- Tipos de viagem
```

---

## 8. Integração com Agentes

### 8.1 Agentes Existentes Compatíveis

| Agente | Uso com Databricks |
|--------|-------------------|
| **DataStrategist** | Definir KPIs baseados em dados reais |
| **DataArchitect** | Modelar schemas e validar estruturas |
| **DataSteward** | Verificar qualidade e governança |
| **BusinessAnalyst** | Analisar dados e gerar insights |
| **Orchestrator** | Coordenar fluxos de dados |

### 8.2 Exemplos de Uso por Agente

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    USO POR AGENTE                                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  DataStrategist:                                                            │
│  ───────────────                                                            │
│  "Analise os dados de bronze.taxi_trips_raw e sugira KPIs relevantes        │
│   para monitorar performance de táxis"                                      │
│                                                                             │
│  DataArchitect:                                                             │
│  ─────────────                                                              │
│  "Revise a estrutura de silver.taxi_trips e sugira otimizações              │
│   de particionamento"                                                       │
│                                                                             │
│  DataSteward:                                                               │
│  ────────────                                                               │
│  "Verifique a qualidade dos dados em bronze.taxi_trips_raw:                 │
│   - Valores nulos                                                           │
│   - Outliers                                                                │
│   - Consistência de tipos"                                                  │
│                                                                             │
│  BusinessAnalyst:                                                           │
│  ───────────────                                                            │
│  "Gere um relatório de tendências mensais usando gold.daily_summary"        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 9. Cronograma de Implementação

### 9.1 Timeline

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        CRONOGRAMA                                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  FASE 1: Setup Azure Databricks                    ⏳ EM ANDAMENTO          │
│  ═══════════════════════════════                                            │
│  • [✅] Criar workspace Azure Databricks                                    │
│  • [ ] Criar SQL Warehouse                                                  │
│  • [ ] Gerar Token de acesso                                                │
│  • [ ] Anotar credenciais                                                   │
│  Tempo estimado: 30 minutos                                                 │
│                                                                             │
│  FASE 2: Upload de Dados                           ⏸️ AGUARDANDO            │
│  ═══════════════════════                                                    │
│  • [ ] Upload CSVs via interface web                                        │
│  • [ ] Upload JSONs via interface web                                       │
│  • [ ] Verificar arquivos no DBFS                                           │
│  Tempo estimado: 15 minutos                                                 │
│                                                                             │
│  FASE 3: Configurar MCP                            ⏸️ AGUARDANDO            │
│  ══════════════════════                                                     │
│  • [ ] Clonar repositório MCP                                               │
│  • [ ] Instalar dependências Python                                         │
│  • [ ] Configurar .env com credenciais                                      │
│  • [ ] Configurar VS Code settings.json                                     │
│  • [ ] Testar conexão                                                       │
│  Tempo estimado: 20 minutos                                                 │
│                                                                             │
│  FASE 4: Criar Estrutura via MCP                   ⏸️ AGUARDANDO            │
│  ═══════════════════════════════                                            │
│  • [ ] Criar schemas (bronze, silver, gold, reference)                      │
│  • [ ] Criar tabelas a partir dos CSVs                                      │
│  • [ ] Criar tabelas de referência                                          │
│  • [ ] Validar estrutura                                                    │
│  Tempo estimado: 15 minutos                                                 │
│                                                                             │
│  FASE 5: Testar com Agentes                        ⏸️ AGUARDANDO            │
│  ══════════════════════════                                                 │
│  • [ ] Testar queries via chat                                              │
│  • [ ] Testar com DataStrategist                                            │
│  • [ ] Testar com DataArchitect                                             │
│  • [ ] Documentar resultados                                                │
│  Tempo estimado: 30 minutos                                                 │
│                                                                             │
│  ─────────────────────────────────────────────────────────────────────────  │
│  TEMPO TOTAL ESTIMADO: ~2 horas                                             │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 9.2 Checklist de Progresso

```
FASE 1: AZURE DATABRICKS
[ ] Workspace criado
[ ] SQL Warehouse criado e running
[ ] Token gerado e salvo
[ ] HOST anotado
[ ] WAREHOUSE_ID anotado

FASE 2: UPLOAD DADOS
[ ] green_tripdata_2021-04.csv uploaded
[ ] green_tripdata_2021-05.csv uploaded
[ ] green_tripdata_2021-06.csv uploaded
[ ] rate_code.json uploaded
[ ] payment_type_array.json uploaded

FASE 3: MCP
[ ] Repositório clonado
[ ] Dependências instaladas
[ ] .env configurado
[ ] VS Code settings.json configurado
[ ] Conexão testada

FASE 4: ESTRUTURA
[ ] Schemas criados
[ ] bronze.taxi_trips_raw criada
[ ] Tabelas reference criadas
[ ] Dados verificados

FASE 5: AGENTES
[ ] Query simples funcionando
[ ] DataStrategist testado
[ ] DataArchitect testado
[ ] Documentação final
```

---

## 10. Referências

### 10.1 Links Úteis

| Recurso | URL |
|---------|-----|
| **MCP Databricks** | https://github.com/RafaelCartenet/mcp-databricks-server |
| **Azure Databricks** | https://portal.azure.com |
| **Databricks Docs** | https://docs.databricks.com |
| **Unity Catalog** | https://docs.databricks.com/data-governance/unity-catalog |
| **Delta Lake** | https://docs.delta.io |

### 10.2 Arquivos de Referência no Projeto

| Arquivo | Conteúdo |
|---------|----------|
| `azure-databricks-integration/03-database-setup/create-schemas.sql` | SQL para criar schemas |
| `azure-databricks-integration/03-database-setup/create-tables.sql` | SQL para criar tabelas |
| `azure-databricks-integration/.env.azure.example` | Template de credenciais Azure |
| `Agent-data-engineer/Files/` | Arquivos CSV/JSON para upload |

### 10.3 Suporte

- **Problemas com Azure:** Portal Azure → Support
- **Problemas com Databricks:** Databricks Community Forums
- **Problemas com MCP:** GitHub Issues do repositório

---

## 📝 Histórico de Alterações

| Data | Versão | Alteração |
|------|--------|-----------|
| 2026-02-04 | 1.0 | Documento inicial criado |

---

*Documento gerado pelo Master Agent - Avanade Method*
