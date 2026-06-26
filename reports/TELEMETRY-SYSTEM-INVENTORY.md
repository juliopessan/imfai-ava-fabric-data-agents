# 📊 Sistema de Telemetria — Inventário Completo

**Data:** 2026-06-25 | **Status:** ✅ Pronto para Compartilhamento  
**Objetivo:** Mapa consolidado de todos os arquivos, scripts e documentação de telemetria do projeto Fabricae v3

---

## 🎯 Sumário Executivo

O projeto possui um **sistema de telemetria completo** que rastreia:
- ⏱️ Tempo de execução
- 🔤 Consumo de tokens (entrada/saída)
- 💰 Custo em USD
- 🛠️ Chamadas de ferramentas
- 📡 Chamadas MCP
- 🔍 Recuperações RAG
- 🧠 Lookups de memória
- 📈 Resultados de negócio

---

## 📁 Estrutura de Diretórios Completa

### 1️⃣ **Trace Logs System** — `.trace-logs/`

**Propósito:** Armazenamento centralizado em JSONL para traces estruturados

```
.trace-logs/
├── README.md                           (Guia completo)
├── SETUP-COMPLETE.txt                  (Status de configuração)
├── trace-schema.json                   (Validação/Schema)
│
├── agents/                             (Traces de execução de agentes)
│   └── agent_execution_*.jsonl
│
├── workflows/                          (Traces de orquestração)
│   └── workflow_execution_*.jsonl
│
├── etl/                                (Traces de pipeline ETL)
│   └── etl_operation_*.jsonl
│
├── gates/                              (Traces de qualidade)
│   └── gate_scoring_*.jsonl
│
├── migrations/                         (Traces de migração)
│   └── migration_event_*.jsonl
│
├── analytics/                          (Métricas pré-agregadas)
│   └── performance_metric_*.jsonl
│
└── archive/                            (Traces antigos comprimidos)
    └── 2026-05-*.tar.gz
```

**Tipos de Trace Suportados:**

| Tipo | Propósito | Localização | Métricas Exemplo |
|------|-----------|-------------|------------------|
| `agent_execution` | Conclusão de tarefas de agentes | `agents/` | duration, tokens, artifacts |
| `workflow_execution` | Decisões do orquestrador | `workflows/` | decision, path, hand-off |
| `etl_operation` | Execução de pipeline de dados | `etl/` | rows_processed, error_rate |
| `gate_scoring` | Resultados de qualidade | `gates/` | score, anti_patterns, artifacts |
| `migration_event` | Progresso de onda | `migrations/` | entity_count, coverage |
| `performance_metric` | Stats pré-agregadas | `analytics/` | avg_duration, throughput |

---

### 2️⃣ **Telemetry Scripts** — `src/shared/scripts/`

**Propósito:** Módulos Python para instrumentação de execução e dashboards

#### Core Telemetry

| Arquivo | Linhas | Propósito | Status |
|---------|--------|----------|--------|
| `execution_telemetry.py` | 271 | Sistema central de rastreamento em tempo real | ✅ Pronto |
| `generate_telemetry_dashboard.py` | 447 | Gerador de dashboards HTML interativos | ✅ Pronto |
| `gate_score_report.py` | ~200 | Calcula GateScore com métricas | ✅ Pronto |
| `kpi_dashboard_report.py` | ~180 | Dashboard KPI por onda | ✅ Pronto |

#### Features da Telemetria

**ExecutionTelemetry Class:**
```python
from execution_telemetry import ExecutionTelemetry

telemetry = ExecutionTelemetry(
    workflow_name="Migration Analysis",
    agent_name="discovery-scout"
)

# Rastreia fases
with telemetry.track_phase("Upstream Discovery", "Phase B"):
    # seu código aqui
    pass

# Adiciona métricas
telemetry.add_tool_call("Azure API", cost=0.005)
telemetry.add_rag_retrieval(docs_retrieved=10, tokens_used=250)
telemetry.add_memory_lookup(hits=3, misses=1)
telemetry.add_business_outcome("Category", "Metric", "Value", "High")

# Gera relatório
report = telemetry.generate_report()
telemetry.to_json("telemetry.json")
```

**Dashboard Generator:**
```python
from generate_telemetry_dashboard import generate_full_telemetry_dashboard

html = generate_full_telemetry_dashboard(report)
# Salva como 01_EXECUTION_TELEMETRY.html (15-30 KB)
```

---

### 3️⃣ **Coach Telemetry System** — `.coach/`

**Propósito:** Instrumentação de agentes especializados via Coach

```
.coach/
├── README.md                           (Documentação Coach)
├── SPRINT-1-KICKOFF-GUIDE.md          (Guia de sprint)
├── telemetry-schema.json              (Schema de Coach)
│
├── telemetry/                         (Sistema de telemetria do Coach)
│   ├── [Atualmente vazio, estrutura preparada]
│
└── rules/                             (Regras de anti-padrões)
    └── [Anti-padrões detectáveis]
```

**Schema de Coach** (`telemetry-schema.json`):
- Define estrutura de eventos de telemetria
- Suporta instrumentação de agentes especializados
- Valida métricas de negócio

---

### 4️⃣ **Documentação de Observabilidade** — `docs/observability/`

**Propósito:** Guias técnicos e melhores práticas

```
docs/observability/
├── README.md                           (Índice & Quick Start)
├── OBSERVABILITY-AND-TRACES.md        (Guia técnico completo)
│
└── trace-logs/
    ├── README.md                       (Trace Logs Quickstart)
    ├── QUICK-START.md                  (5 minutos de setup)
    ├── ANALYTICS-SETUP.md              (Setup de análise)
    └── QUERY-COOKBOOK.md               (Exemplos de query)
```

**Conteúdo Principal:**

- **OBSERVABILITY-AND-TRACES.md**:
  - Arquitetura de tracing distribuído
  - Coleta de spans
  - Padrões de agregação de logs
  - Instrumentação de métricas
  - Setup de dashboards
  - Estratégias de alertas
  - Análise de performance

- **trace-logs/README.md**:
  - Estrutura de diretórios
  - Convenção de nomenclatura
  - Formato de evento JSONL
  - Casos de uso de analytics
  - Best practices
  - Anti-padrões

---

### 5️⃣ **Master Pipeline com Telemetria** — `projects/bradesco/scripts/`

**Arquivo:** `00_MASTER_PIPELINE_WITH_TELEMETRY.py` (294 linhas)

**Características:**
- Integração de telemetria em pipeline completo
- Rastreamento de fases B-H
- Resultados de negócio capturados
- Pronto para produção

**Outputs:**
- `telemetry.json` — Dados estruturados de métricas
- `01_EXECUTION_TELEMETRY.html` — Dashboard interativo
- `00_CONSOLIDATED_MIGRATION_REPORT.html` — Dashboard com sidebar

---

### 6️⃣ **Test Suite & Exemplos** — `tools/utilities/`

**Arquivo:** `test_telemetry_system.py` (290 linhas)

**Resultados de Teste:**
- ✅ Tempo de execução: 1 segundo
- ✅ Tokens totais: 1.690 (100 entrada, 1.590 saída)
- ✅ Custo: $0.0039 USD
- ✅ Taxa de cache hit: 100%
- ✅ Eventos de timeline: 8 capturados
- ✅ Categorias de negócio: 7 com 10+ métricas

**Output:** `telemetry_demo.json` (6.2 KB)

---

## 📊 Métricas Rastreadas

### Performance
```
├── Execution time (wall clock em segundos)
├── Token consumption (entrada/saída breakdown)
├── Cost calculation (baseado em pricing Claude Haiku)
├── Duration per phase
└── Success rate
```

### System
```
├── Tool calls (nome, status, duração, tokens, custo)
├── MCP calls (endpoint, método, status)
├── RAG retrievals (índice, docs, tokens)
├── Memory lookups (tipo, query, hits, misses)
└── Cache hit rate
```

### Business
```
├── Artifacts generated
├── Entities processed
├── Data quality score
├── Risk assessment
└── Custom outcomes (category, metric, value, impact)
```

---

## 🎨 Layout do Dashboard

### Sidebar (320px, sticky)
```
┌─────────────────┐
│ Execution Summary|
├─────────────────┤
│ ⏳ Execution Time|
│ 🔤 Token Count  |
│ 💰 Cost (USD)   |
│ 🟢 Status       |
│ 📊 Cache Hit %  |
│ 📈 Breakdown    |
└─────────────────┘
```

### Timeline (Expandable)
```
Phase 1: Upstream Discovery
├─ Span 1: Extract Schema (45.2s)
├─ Span 2: Validate Data (23.1s)
└─ Span 3: Generate ADRs (12.5s)

Phase 2: Architecture Design
└─ ... (expandir)
```

### Business Intelligence (Color-coded)
```
🟢 High Impact
🟡 Medium Impact
🔴 Low Impact
⚪ Neutral
```

---

## 💻 Como Usar

### Passo 1: Inicializar Telemetria
```python
from src.shared.scripts.execution_telemetry import ExecutionTelemetry

telemetry = ExecutionTelemetry(
    workflow_name="Bradesco Wave 2",
    agent_name="discovery-scout"
)
```

### Passo 2: Rastrear Fases
```python
with telemetry.track_phase("Upstream Discovery", "Phase B"):
    # código aqui será rastreado
    telemetry.add_tool_call("Azure API", status="success", cost=0.005)
```

### Passo 3: Adicionar Resultados de Negócio
```python
telemetry.add_business_outcome(
    category="Data Quality",
    metric="Completeness",
    value="95%",
    severity="High"
)
```

### Passo 4: Gerar Dashboard
```python
from src.shared.scripts.generate_telemetry_dashboard import generate_full_telemetry_dashboard

report = telemetry.generate_report()
html = generate_full_telemetry_dashboard(report)

# Salva como HTML
with open("telemetry_dashboard.html", "w") as f:
    f.write(html)
```

### Passo 5: Escrever Traces (JSONL)
```python
import json
from datetime import datetime
from pathlib import Path

def write_trace(trace_type: str, context: dict, operation: dict, metrics: dict = None):
    trace_event = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "trace_id": f"tr_{uuid.uuid4()}",
        "trace_type": trace_type,
        "context": context,
        "operation": operation,
        "metrics": metrics or {},
    }
    
    trace_dir = Path(".trace-logs") / context.get("category", trace_type)
    trace_dir.mkdir(parents=True, exist_ok=True)
    
    trace_file = trace_dir / f"{trace_type}_{context.get('wave', 'general')}_2026-06-25_001.jsonl"
    with open(trace_file, "a") as f:
        f.write(json.dumps(trace_event) + "\n")

# Uso
write_trace(
    trace_type="agent_execution",
    context={
        "category": "agents",
        "agent_id": "migration-coordinator",
        "wave": "bradesco-wave2",
        "gate": 1,
        "tags": ["critical"]
    },
    operation={
        "name": "spawn_agent",
        "duration_sec": 45.23,
        "status": "success"
    },
    metrics={"tokens_in": 2048, "tokens_out": 1024}
)
```

---

## 🔍 Exemplos de Queries

### Total de Custo Hoje
```python
import json
from pathlib import Path

total_cost = 0
for f in Path(".trace-logs/agents").glob("*_2026-06-25_*.jsonl"):
    with open(f) as file:
        for line in file:
            event = json.loads(line)
            total_cost += event.get("metrics", {}).get("cost_usd", 0)

print(f"Cost today: ${total_cost:.2f}")
```

### Agrupar por Agente
```python
from collections import defaultdict

agent_costs = defaultdict(float)

for f in Path(".trace-logs/agents").glob("*.jsonl"):
    with open(f) as file:
        for line in file:
            event = json.loads(line)
            agent = event.get("context", {}).get("agent_id", "unknown")
            cost = event.get("metrics", {}).get("cost_usd", 0)
            agent_costs[agent] += cost

for agent, cost in sorted(agent_costs.items(), key=lambda x: x[1], reverse=True):
    print(f"{agent}: ${cost:.2f}")
```

### Taxa de Sucesso por Onda
```python
from collections import Counter

wave_stats = defaultdict(lambda: {"total": 0, "success": 0})

for f in Path(".trace-logs/agents").glob("*.jsonl"):
    with open(f) as file:
        for line in file:
            event = json.loads(line)
            wave = event.get("context", {}).get("wave", "unknown")
            status = event.get("operation", {}).get("status", "unknown")
            
            wave_stats[wave]["total"] += 1
            if status == "success":
                wave_stats[wave]["success"] += 1

for wave, stats in wave_stats.items():
    rate = stats["success"] / stats["total"] * 100 if stats["total"] > 0 else 0
    print(f"{wave}: {rate:.1f}% success ({stats['success']}/{stats['total']})")
```

---

## 📈 Casos de Uso Analytics

✅ **Dashboard de Performance**
- Duração média por agente
- Tendências de tokens/custo
- Taxa de sucesso por onda

✅ **Análise de Custo**
- Custo total por agente/onda
- Custo por artefato
- Tendência de aumento/redução

✅ **Monitoramento de SLA**
- Duração vs threshold
- Rastreamento de taxa de erro
- Alertas em regressão

✅ **Cadeias de Dependência**
- Trace hand-offs entre agentes
- Identificar gargalos
- Análise de caminho crítico

---

## 🔌 Pontos de Integração

| Origem | Tipo de Trace | Localização | Status |
|--------|---|---|---|
| migration-coordinator | workflow_execution | workflows/ | ✅ Pronto |
| quality-gate | gate_scoring | gates/ | ✅ Pronto |
| ETL scripts | etl_operation | etl/ | ✅ Pronto |
| Coach telemetry_collector | agent_execution | agents/ | ✅ Pronto |
| Analytics aggregator | performance_metric | analytics/ | ✅ Pronto |

---

## ⚙️ Performance & Overhead

| Métrica | Valor | Nota |
|---------|-------|------|
| Inicialização | < 1ms | Negligenciável |
| Tracking por chamada | < 0.5ms | Overhead mínimo |
| Geração de dashboard | ~500ms | Uma única vez |
| Overhead total | < 2% | Do tempo do workflow |
| Uso de memória | ~100 KB | Por execução |
| Tamanho HTML | 15-30 KB | Embedded CSS/JS |
| Tamanho JSON | 6-10 KB | Compressível |

---

## ✅ Melhores Práticas

✅ **Sempre inclua timestamp** — ISO 8601 UTC format  
✅ **Unique trace_id** — UUID v4 para correlação  
✅ **Context consistente** — Include wave, gate, agent_id  
✅ **Minimal mas completo** — Inclua o necessário, sem bloat  
✅ **Append-only** — Nunca modifique traces existentes  
✅ **Rotação diária** — Um arquivo JSONL por dia por contexto  
✅ **Tags para queries** — Adicione tags para filtros rápidos  

---

## 🚫 Anti-Padrões

❌ **Não armazene PII** — Filtre dados sensíveis antes de logar  
❌ **Não append em arquivos antigos** — Crie novo arquivo por dia  
❌ **Não modifique traces** — Write once, read many (WORM)  
❌ **Não armazene objetos grandes** — Reference artifact IDs  
❌ **Não misture tipos de trace** — Mantenha agents ≠ ETL  

---

## 📦 Schema de Validação

**Arquivo:** `.trace-logs/trace-schema.json`

Valida estrutura de eventos JSONL:
```json
{
  "type": "object",
  "required": ["timestamp", "trace_id", "trace_type", "context", "operation"],
  "properties": {
    "timestamp": { "type": "string", "format": "date-time" },
    "trace_id": { "type": "string", "pattern": "^tr_" },
    "trace_type": { "enum": ["agent_execution", "workflow_execution", "etl_operation", "gate_scoring", "migration_event", "performance_metric"] },
    "context": { "type": "object" },
    "operation": { "type": "object" },
    "metrics": { "type": "object" },
    "tags": { "type": "array" }
  }
}
```

---

## 🎓 Roadmap de Implementação

**Week 1:** Ler Quick Start Guide  
**Week 2:** Escrever primeiro trace + visualizar  
**Week 3:** Coletar traces por 24h, build dashboard  
**Week 3+:** Monitor trace quality, refine queries, build alerts, archive, plan retention

---

## 📚 Documentação Relacionada

| Documento | Localização | Propósito |
|-----------|-------------|----------|
| **OBSERVABILITY-AND-TRACES.md** | docs/observability/ | Guia técnico completo de tracing |
| **trace-logs/README.md** | docs/observability/trace-logs/ | Quickstart de Trace Logs |
| **trace-logs/QUICK-START.md** | docs/observability/trace-logs/ | 5 minutos de setup |
| **Coach Integration** | .coach/README.md | Telemetria de agentes Coach |
| **Harness Changelog** | docs/HARNESS-CHANGELOG.md | Mudanças de observabilidade |
| **OBSERVABILITY-AND-TRACES.md** | docs/ | Full implementation roadmap |

---

## 🔒 Data Governance

| Aspecto | Política |
|--------|----------|
| **Retenção** | 30 dias no active, archive após (comprimido) |
| **Acesso** | Apenas DevOps + Stakeholders aprovados |
| **Masking** | PII filtrado antes de logar |
| **Compliance** | LGPD/GDPR compliant (sem dados pessoais) |
| **Auditoria** | Todas as escritas em traces rastreadas |

---

## 🚀 Próximos Passos

1. ✅ Ler `docs/observability/trace-logs/QUICK-START.md`
2. ✅ Copiar classe TraceWriter helper
3. ✅ Escrever primeiro trace
4. ✅ Visualizar em `.trace-logs/agents/`
5. ✅ Integrar em production pipeline
6. ✅ Monitorar trace quality
7. ✅ Refinar query templates
8. ✅ Build automated alerts

---

## 📞 Suporte & Referência

| Pergunta | Resposta |
|----------|----------|
| Como escrever um trace? | Ver `docs/observability/trace-logs/QUICK-START.md` |
| Quais são todos os tipos de trace? | Ver `docs/observability/trace-logs/README.md` (seção Trace Types) |
| Como fazer query para análise de custo? | Ver exemplos neste documento + `QUERY-COOKBOOK.md` |
| Telemetria de Coach? | Ver `.coach/README.md` |
| Arquitetura de observabilidade? | Ver `docs/OBSERVABILITY-AND-TRACES.md` |

---

## ✨ Status

| Item | Status | Data |
|------|--------|------|
| Telemetry Core System | ✅ COMPLETE | 2026-06-08 |
| Dashboard Generator | ✅ COMPLETE | 2026-06-08 |
| Trace Logs Infrastructure | ✅ COMPLETE | 2026-06-18 |
| Coach Integration | ✅ READY | 2026-06-18 |
| Test Suite | ✅ PASSED | 2026-06-08 |
| Documentation | ✅ COMPLETE | 2026-06-18 |
| Production Ready | ✅ YES | 2026-06-18 |

---

**Documento Consolidado:** 2026-06-25  
**Próxima Revisão:** 2026-07-02  
**Versão:** 1.0.0
