# 📊 MAPEAMENTO DE ESCOPO — PROJETO FINANCEIRO

**Data:** 2026-06-26  
**Escopo:** Análise completa para cálculo de tokens e planejamento de migração  
**Status:** ✅ Finalizado

---

## 1️⃣ RESUMO EXECUTIVO

| Métrica | Valor |
|---------|-------|
| **Total de arquivos** | 795 |
| **Tamanho total** | 43.67 MB |
| **Estimativa de tokens** | ~11.4M (bruto) / ~15M (com overhead) |
| **Entidades de BD** | 103 (8 tabelas + 1 proc + 2 views + 92 Hive) |
| **Scripts de lógica** | 98 (22 reproc + 76 outros) |
| **Complexidade** | 🔴 **ALTA** |

---

## 2️⃣ DISTRIBUIÇÃO DE ARQUIVOS

### Por Tipo de Arquivo

| Extensão | Quantidade | Tamanho | % do Total | Categoria |
|----------|-----------|--------|-----------|-----------|
| `.pkl` | 8 | 23.77 MB | 54.4% | 📦 Pickles/Serialized |
| `.dtsx` | 75 | 8.29 MB | 19.0% | 🔄 SSIS/ETL |
| `.zip` | 3 | 4.91 MB | 11.2% | 📦 Archives |
| `.dtproj` | 2 | 1.33 MB | 3.0% | 🔄 SSIS Projects |
| `.py` | 104 | 1.24 MB | 2.8% | 🐍 Python |
| `.json` | 45 | 1.19 MB | 2.7% | ⚙️ Config |
| `.md` | 108 | 1.06 MB | 2.4% | 📄 Docs |
| `.html` | 33 | 772 KB | 1.7% | 🌐 Reports |
| `.hql` | 92 | 333 KB | 0.7% | 🐘 Hive SQL |
| `.sql` | 43 | 294 KB | 0.7% | 🗄️ SQL |
| `.sh` | 234 | 283 KB | 0.6% | 🔧 Shell Scripts |
| **Outros** | 48 | 96 KB | 0.2% | 📁 Diversos |

### Por Categoria

| Categoria | Quantidade | Tamanho | % |
|-----------|-----------|--------|---|
| **SSIS/ETL** | 77 | 8.29 MB | 19.0% |
| **Python** | 104 | 1.24 MB | 2.8% |
| **Configuration** | 57 | 1.24 MB | 2.8% |
| **Documentação** | 111 | 1.07 MB | 2.5% |
| **SQL** | 43 | 294 KB | 0.7% |
| **Shell** | 234 | 283 KB | 0.6% |

---

## 3️⃣ ENTIDADES DE BANCO DE DADOS

### Objetos SQL
- **Tabelas:** 8
  - `sacl_stg`
  - `sacl_ddm`
  - `rentabilidade`
  - `procedencia`
  - `financeiro_bronze`
  - (+ 3 outras)

- **Stored Procedures:** 1
  - `dbo.*` (grupo de procedures)

- **Views:** 2
  - `sacl_acc`
  - `IF` (e relacionadas)

### Hive/HDFS (Legacy Big Data)
- **Arquivos HQL:** 92
  - **sql_partitions:** Criação de partições (Hive)
  - **sql_tables:** Definição de tabelas Hive
  - **sql_temp_tables:** Tabelas temporárias
  - **indices_econm:** Índices econômicos

**Exemplo de estrutura:**
```
hive/
├── sql_partitions/          (criar partições)
├── sql_tables/              (criar tabelas)
├── sql_temp_tables/         (temp)
├── indices_econm/           (índices econ)
├── exec_hive/               (execução)
└── exec_hist_hive/          (histórico)
```

---

## 4️⃣ SCRIPTS E LÓGICA DE TRANSFORMAÇÃO

### Python Scripts (104 total)

**Reproc Scripts (Reprocessamento):** 22
```
reproc_agora.py
reproc_capn.py
reproc_carteira.py
reproc_categ_prodt.py
reproc_cefi.py
reproc_class_ativo.py
reproc_csl_acum_gen.py
reproc_csl_gen.py
reproc_hist_gen.py
reproc_jcot.py
reproc_mclass.py
reproc_mes_acum_prodt_gen.py
reproc_mes_vig_acum_prodt.py
reproc_periodos_gen.py
reproc_portfolio.py
reproc_pre_agrup.py
reproc_prev.py
reproc_produto.py
reproc_rent_prodt_csl.py
reproc_rent_scap_capn.py
reproc_scap.py
reproc_tmrf.py
```

**Outros Scripts Python:** 76
- Consolidação, limpeza de tipos, utilitários
- Processamento de dados economicos
- Integrações de dados

### Shell Scripts (234 total)
- HDFS operations
- Hive execução
- PowerCenter workflows
- TDCH (Teradata Connector)
- Monitoração

### SSIS/ETL (77 arquivos)
- **.dtsx:** 75 (packages SSIS)
- **.dtproj:** 2 (SSIS projects)

---

## 5️⃣ ESTRUTURA DE DIRETÓRIOS

```
projects/financeiro/
├── legacy/extracted/
│   ├── aaar-srv-calc-rentabilidade-script/
│   │   ├── hive/               (92 arquivos HQL)
│   │   ├── python/             (22+ scripts reproc)
│   │   ├── powercenter/        (workflows)
│   │   ├── ssis/               (SSIS packages)
│   │   ├── ssis_BulkInsert/
│   │   ├── spark/              (config Spark)
│   │   ├── sqlserver/          (procedures)
│   │   ├── tdch/               (Teradata)
│   │   ├── teradata/           (tabelas)
│   │   └── utils/              (utilitários)
│   │
│   └── aadg-srv-d4960-algoritmo-procedencia/
│       ├── ddl/                (definições)
│       ├── dml/                (dados)
│       ├── modelos/            (modelos)
│       ├── python/
│       └── shell/
│
├── outputs/                    (151 arquivos - resultados)
├── state/                      (41 arquivos - estado)
├── scripts/                    (40 arquivos - utilitários)
├── docs/                       (7 arquivos)
├── context/
└── README.md
```

---

## 6️⃣ ESTIMATIVA DE TOKENS

### Cálculo Base
```
Total em bytes:        45,786,841
Estimativa bruta:      ~11,446,710 tokens
  (1 token ≈ 4 caracteres)

Com overhead (30%):    ~14,880,723 tokens
  (para análise, contexto, iterações)
```

### Breakdown por Fase de Migração

| Fase | Estimativa | Notas |
|------|-----------|-------|
| **Inventário** | 50k | Scan + mapping de arquivos |
| **Análise SQL/Python** | 200k | Parse de 135 objetos |
| **Design Target** | 300k | Arquitetura Fabric, Spark, Data Factory |
| **Validação** | 100k | Testes, reconciliação |
| **Documentação** | 50k | Runbooks, modelos, ADRs |
| **────────────** | **────────** | **────────** |
| **TOTAL** | **~700k** | **Estimado para execução completa** |

### Token Burn por Atividade

```
🔍 Descoberta (Upstream):     150-200k tokens
   └─ Scan, inventário, mapping

🏗️ Design (Midstream):        250-350k tokens
   └─ Arquitetura, código, validação

🚀 Execução (Downstream):     150-250k tokens
   └─ Implementação, testes, deploy
```

---

## 7️⃣ COMPLEXIDADE E RISCOS

### Fatores de Complexidade

| Fator | Nível | Descrição |
|-------|-------|-----------|
| **Entidades (103)** | 🟠 Alto | 8 tabelas + 92 Hive + procedures |
| **Lógica (98 scripts)** | 🟠 Alto | 22 reproc + transformações |
| **Legacy stack** | 🔴 Crítico | Hive + SSIS + PowerCenter + Teradata |
| **Interdependências** | 🟠 Alto | Scripts encadeados de reprocessamento |
| **Documentação** | 🟢 Bom | 111 arquivos de doc existentes |

### Riscos Principais

🔴 **CRÍTICO**
- Migração de Hive para Spark: 92 scripts HQL
- SSIS packages (75): Requer análise de cada workflow
- PowerCenter workflows: Lógica de negócio complexa

🟠 **ALTO**
- Reproc scripts encadeados (22 scripts interdependentes)
- Teradata + TDCH: Conectores custom
- Pickles binárias (23.77 MB): Requer conversão

🟡 **MÉDIO**
- Shell scripts (234): Automação de baixo nível
- Procedures SQL complexas
- Índices econômicos (tempo real)

---

## 8️⃣ RECOMENDAÇÕES PARA ANÁLISE

### Sequência de Análise (Token-otimizada)

```
1️⃣ Inventário Rápido (50k tokens)
   └─ Lista todas as tabelas, procedures, scripts

2️⃣ Análise SQL (100k tokens)
   └─ Parse de DDL, DML, dependências

3️⃣ Análise Python (100k tokens)
   └─ Parse de reproc, lógica de transformação

4️⃣ Análise Hive/SSIS (200k tokens)
   └─ Mapeamento para Spark + Data Factory

5️⃣ Design Target (250k tokens)
   └─ Arquitetura Fabric, data contracts, GUID

6️⃣ Validação (100k tokens)
   └─ Gate 2, reconciliação, testes
```

### Ferramentas Recomendadas

| Tool | Para | Token Cost |
|------|------|-----------|
| **Azure Data Studio** | SQL + Hive parse | Baixo (local) |
| **Python AST** | Script analysis | Baixo (local) |
| **Fabric Synapse** | Spark validation | Médio |
| **Data Factory** | ETL mapping | Médio |
| **Copilot** (subagent) | Design + docs | 200-300k |

---

## 9️⃣ NEXT STEPS

- [ ] **Phase 1:** Executar inventário detalhado via `discovery-scout`
- [ ] **Phase 2:** Analisar dependências entre scripts (dependency graph)
- [ ] **Phase 3:** Mapear stack legado → Microsoft (Hive→Spark, SSIS→DF, etc)
- [ ] **Phase 4:** Design data model (dbt + Semantic Kernel)
- [ ] **Phase 5:** Gate 2 validation + token burn tracking

---

**Gerado:** 2026-06-26  
**Arquivo:** `/memories/repo/financeiro-escopo-tokens.md`
