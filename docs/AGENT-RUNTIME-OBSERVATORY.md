# Agent Runtime Observatory — Visão geral

Contexto: plataforma VS Code–nativa para observabilidade e inteligência de execuções de agentes. Transforma cada execução em evento de negócio persistente, pesquisável e auditável.

**Entregáveis deste documento:** arquitetura, diagrama de componentes, schema PostgreSQL (DDL), APIs, modelo de eventos, modelo de telemetria (OpenTelemetry), arquitetura da extensão VS Code, wireframes de UI, considerações de escalabilidade, roadmap MVP (30 dias) e produção (90 dias), diferenciação competitiva.

**Premissas:** backend Python/FastAPI, PostgreSQL, OpenTelemetry, frontend React+TS via VS Code Webview, deploy em Azure.

**1. High-level Architecture**
- **Frontend VS Code:** Extensão com painel lateral (Execution List), timeline, BI summaries e replay controls.
- **Edge Agent SDK:** biblioteca instrumentando agentes para emitir eventos e spans (Python/JS).
- **Ingest API (FastAPI):** recebe eventos, normaliza, enfileira (Kafka/EventHub).
- **Processing Pipeline:** stream processors (Flink/Beam or lightweight Python workers) → enrich (KG linker, cost calc, BI extractor) → persist to PostgreSQL + GraphDB + Vector index + Blob store for artifacts.
- **Query & BI API:** agregações, replay endpoints, pattern-mining jobs, assets publish.
- **Observability:** OpenTelemetry collector → Azure Monitor/Grafana/Prometheus.

**2. Component Diagram (resumo)**
- **VS Code Extension** ↔ `Ingest API` ↔ `Processing Pipeline` ↔ {`Postgres`, `GraphDB`, `VectorIndex`, `BlobStore`}.
- **OpenTelemetry Collector** ingest spans + metrics from agents and services.

**3. Database Schema (DDL) — PostgreSQL (inicial)**

```sql
-- Agent runs
CREATE TABLE agent_runs (
  id UUID PRIMARY KEY,
  agent_name TEXT NOT NULL,
  workflow_name TEXT,
  status TEXT,
  started_at timestamptz,
  finished_at timestamptz,
  tokens integer,
  cost numeric(12,6),
  dag jsonb,
  metadata jsonb
);

CREATE INDEX ON agent_runs (agent_name);
CREATE INDEX ON agent_runs (workflow_name);

-- Actions / nodes
CREATE TABLE agent_actions (
  id UUID PRIMARY KEY,
  run_id UUID REFERENCES agent_runs(id) ON DELETE CASCADE,
  node_name TEXT,
  type TEXT,
  start_at timestamptz,
  end_at timestamptz,
  inputs jsonb,
  outputs jsonb,
  cost numeric(12,6),
  metrics jsonb
);

-- Decisions
CREATE TABLE agent_decisions (
  id UUID PRIMARY KEY,
  run_id UUID REFERENCES agent_runs(id),
  decision TEXT,
  rationale jsonb,
  actor TEXT,
  created_at timestamptz
);

-- Tool calls
CREATE TABLE tool_calls (
  id UUID PRIMARY KEY,
  run_id UUID REFERENCES agent_runs(id),
  tool_name TEXT,
  request jsonb,
  response jsonb,
  latency_ms integer,
  success boolean,
  created_at timestamptz
);

-- MCP calls
CREATE TABLE mcp_calls (
  id UUID PRIMARY KEY,
  run_id UUID REFERENCES agent_runs(id),
  server TEXT,
  endpoint TEXT,
  payload jsonb,
  response jsonb,
  latency_ms integer,
  status_code integer,
  created_at timestamptz
);

-- Memory & KG events
CREATE TABLE memory_events (
  id UUID PRIMARY KEY,
  run_id UUID REFERENCES agent_runs(id),
  entity_id TEXT,
  action TEXT,
  payload jsonb,
  created_at timestamptz
);

-- Business events
CREATE TABLE business_events (
  id UUID PRIMARY KEY,
  run_id UUID REFERENCES agent_runs(id),
  event_type TEXT,
  payload jsonb,
  value numeric,
  currency TEXT,
  created_at timestamptz
);
```

**4. API Design (representative endpoints)**
- POST /v1/ingest/run — inicia/atualiza `AgentRun` (payload includes `dag`)
- POST /v1/ingest/action — registrar `AgentAction` (node start/end, inputs/outputs)
- POST /v1/ingest/tool — registrar `ToolCall`
- POST /v1/ingest/mcp — registrar `McpCall`
- POST /v1/ingest/memory — registrar `MemoryEvent`
- POST /v1/ingest/business — registrar `BusinessEvent`
- GET /v1/runs/{id} — retorna run + DAG + actions + metrics
- POST /v1/replay/{id} — inicia replay (query params: deterministic=true/false)
- GET /v1/bi/summary — agregações por agent/workflow/date range
- GET /v1/kg/query?q= — query hybrid (graph + semantic)

Exemplo de payload (AgentAction):

```json
{
  "id":"uuid",
  "run_id":"uuid",
  "node_name":"Memory Search",
  "type":"memory_search",
  "start_at":"2026-06-05T10:00:00Z",
  "end_at":"2026-06-05T10:00:02Z",
  "inputs":{ },
  "outputs":{ },
  "metrics":{ "hits": 3, "score": 0.87 }
}
```

**5. Event Model**
- Core fields (all events): `id`, `run_id`, `type`, `timestamp`, `actor`, `payload`, `trace_id`, `span_id`, `metadata`.
- Events são append-only e podem ser assinados (HMAC) para prova de integridade.

**6. Telemetry Model (OpenTelemetry + metrics)**
- Traces: um `trace` por `AgentRun`. Spans por `AgentAction`/`ToolCall`/`McpCall` com atributos: `agent.name`, `workflow.name`, `node`, `cost`, `tokens`, `success`, `retries`.
- Metrics: `agent_runs.started`, `agent_runs.completed`, `agent_tokens.count`, `agent_cost.total`, `tool_call.latency` (histogram), `memory_hit_rate` (gauge), `business_value.generated` (counter).
- Logs: structured JSON com `execution_id`, `node`, `severity`, `message`.

**7. VS Code Extension Architecture**
- `Extension Host` (Node) roda background: autenticação, WS com backend, caching local.
- `Webview Panel` (React+TS) renderiza: Execution List, Timeline, BI Summary, Replay controls.
- `Agent SDK` (JS/TS) usado por agentes locais para emitir eventos direto do editor.
- Comandos: `agent-observatory.open`, `agent-observatory.replay`, `agent-observatory.publishAsset`.
- Offline: armazenamento local (LevelDB) com flush transacional.

**8. UI Wireframes (resumo)**
- Left: Execution List (pesquisa, filtros). Item mostra: `elapsed`, `tokens`, `cost`, `status`, `BI tag`.
- Center: Execution Timeline — passos expansíveis com detalhes (inputs/outputs, span, provenance).
- Right: BI Summary — KPIs (Business Value, Risks, Recommendations), Graph agent→agent, Replay.
- Bottom: Raw JSON / Playback console com controles (step/step-over/breakpoints).

**9. Scalability & Reliability**
- Ingest: API autoscale + EventHub; use batching and backpressure.
- Storage: particionamento temporal e por workflow; replicas para leitura; materialized views para BI.
- Processing: stateless stream-workers + stateful jobs com checkpointing.
- KG & Vector: cluster dedicado, sharding por tenant/namespace.
- Replay: snapshot de ambiente; emulação sandbox para chamadas externas.
- Segurança: encryption, RBAC, signed events, retention policies.

**10. MVP Roadmap (30 dias)**
- Day 0–7: scaffold FastAPI ingest, schema migrations, OTEL collector, VS Code extension scaffold (panel + list).
- Day 8–14: implement POST /v1/ingest/run & /action; persist run/actions; extension reads and displays runs + timeline skeleton.
- Day 15–21: simple BI extractor rules; tool-call capture; basic metrics (tokens, cost); basic replay endpoint (read-only playback).
- Day 22–30: implement memory events storage + minimal KG stub, demo POC with one agent emitting events, basic dashboards (PowerBI/Grafana).

**11. Production Roadmap (90 dias)**
- 0–30: MVP (acima).
- 31–60: stream processing, GraphDB integration, vector index, advanced BI extraction (NLP rules + LLM judgments), auth & multi-tenant isolation.
- 61–90: pattern-mining jobs, asset publish pipeline, replay engine with deterministic emulation, RBAC, SLA, backup/DR, cost-optimization, full OTEL integration.

**12. Competitive Differentiation**
- **Business-first telemetry:** converte execuções em `BusinessEvents` (ex.: €42k exposure) — Langfuse/LangSmith focam em tokens/traces.
- **VS Code native UX:** painel integrado + replay step-debug inside editor — immediate developer experience advantage versus SaaS-only consoles.
- **Knowledge Graph + Vector hybrid:** permite reasoning across relationships, not just embedding similarity.
- **Replay + Deterministic Audit:** signed append-only events + environment snapshot for forensic replay — strong compliance differentiator.
- **BI layer & ROI metrics:** built-in rules to compute business value, automation rate, time saved and ROI per agent.

---

Arquivo relacionado: use [docs/HARNESS-OS.md](docs/HARNESS-OS.md) como complemento técnico ao design.

Quer que eu implemente o scaffold do POC agora (FastAPI + migrations + extensão VS Code scaffold)? Responda `POC` e eu começo a criar os artefatos.
