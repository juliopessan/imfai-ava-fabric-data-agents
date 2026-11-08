# Captura de traces — orquestrador Financeiro simulado (Card C-14)

Integra `tools/trace-integration/trace_writer.py` (ver
[`TRACE_INTEGRATION_GUIDE.md`](../../../tools/trace-integration/TRACE_INTEGRATION_GUIDE.md))
ao orquestrador `projects/financeiro/scripts/FINANCEIRO_WAVES_1-4_PARALLEL_OPTIMIZED.py`.

## ⚠️ Limitações da simulação

- Os gates são **simulados**: cada gate é um `time.sleep(0.05)` mais fórmulas. Nenhum
  serviço externo, Databricks, Cloudera, ETL ou migração é executado ou conectado.
- Tokens, custo (USD), completeness/quality/reconciliation e GateScore são **estimativas**
  calculadas por fórmulas e constantes (`CLAUDE_PRICING`, `WAVE_CONFIGS`), não medições.
- A única medição é `duration_sec`: tempo de relógio (wall-clock) da própria simulação.
  Não representa tempo de trabalho de produção.
- O status `PASS` é resultado simulado; no trace aparece como `operation.status = "success"`
  e `metadata.simulated_gate_result = "PASS"`.
- Estes traces **não** são coleta de produção. Nenhum evento `etl_operation`,
  `migration_event`, `agent_execution` ou `workflow_execution` é emitido: só `gate_scoring`.

## Como habilitar

A captura é opt-in (sem opção, o comportamento é o de antes e nada é gravado).

```bash
# opção 1: flag
python3 projects/financeiro/scripts/FINANCEIRO_WAVES_1-4_PARALLEL_OPTIMIZED.py --trace-dir /tmp/financeiro-traces

# opção 2: variável de ambiente
FINANCEIRO_TRACE_DIR=/tmp/financeiro-traces python3 projects/financeiro/scripts/FINANCEIRO_WAVES_1-4_PARALLEL_OPTIMIZED.py
```

Use um diretório dedicado/temporário para não misturar eventos simulados com o `.trace-logs/`
versionado. O script executa a linha de base serial e a execução paralela, então um run
gera 24 eventos (12 `serial` + 12 `parallel`).

Uso programático (uma instância compartilhada entre as threads das waves):

```python
writer = build_trace_writer("/tmp/financeiro-traces")
FinanceiroBrallelOrchestrator(trace_writer=writer).execute_parallel()
```

## Como verificar

Os eventos ficam em `<trace-dir>/gates/gate_scoring_financeiro-wave{N}_{DATA}_001.jsonl`.

```bash
cat /tmp/financeiro-traces/gates/*.jsonl | python3 -c "import sys,json; [json.loads(l) for l in sys.stdin]; print('JSONL válido')"
cat /tmp/financeiro-traces/gates/*.jsonl | jq -c '[.context.execution_mode,.context.wave_id,.context.gate,.operation.status,.operation.duration_sec]'
```

Campos de cada evento (`trace_type = "gate_scoring"`):

| Campo | Conteúdo |
|-------|----------|
| `context.wave` / `context.wave_id` | `financeiro-waveN` / `Wave N` |
| `context.gate` / `context.gate_id` | `1..3` / `GATEn` |
| `context.execution_mode` / `context.run_id` | `serial` ou `parallel` / id da instância do orquestrador |
| `operation.duration_sec`, `operation.status`, `operation.error` | duração observada, `success`/`failure`, erro |
| `metrics.measured` | só `duration_sec` (medido na simulação) |
| `metrics.estimated` | tokens, custo, percentuais e GateScore (estimados) |
| `metadata.data_origin`, `metadata.environment` | `simulated`, `simulation` |
| `metadata.measured_fields` / `estimated_fields` | quais campos são medidos / estimados |
| `tags` | `simulated`, `estimated-metrics`, modo de execução |

## Falhas

- **Falha de gate**: é gravado um evento com `operation.status = "failure"` e `operation.error`,
  e a exceção original é propagada (comportamento anterior preservado). Gates que não
  executaram não geram evento.
- **Falha de escrita do trace**: `TraceWriter` apenas imprime em stderr e retorna `None`.
  O orquestrador registra cada falha em `orchestrator.trace_errors`, imprime
  `❌ Trace not written: ...` em stderr e, ao final de `execute_serial()`/`execute_parallel()`,
  levanta `TraceCaptureError` (com a lista de erros). Pela linha de comando isso resulta em
  `❌ TRACE CAPTURE FAILED` e código de saída 1 — nunca sucesso silencioso.

## Testes

```bash
python3 -m unittest projects/financeiro/tests/test_trace_integration.py -v
# ou, com pytest instalado: pytest projects/financeiro/tests/test_trace_integration.py
```

Usam diretórios temporários e nenhum serviço externo. Cobrem: JSONL válido; um evento por gate
nas 4 waves × 3 gates (serial, paralelo, ambos na mesma instância e vários orquestradores
concorrentes com um writer compartilhado); marcações de origem simulada e medido × estimado;
ausência de eventos ETL/migração; falha de gate (serial e paralelo); falha de escrita de trace
(`None`, exceção e erro real de I/O); e a CLI (`--trace-dir`, variável de ambiente e padrão desligado).

Resultado: 14 testes, todos passando (`Ran 14 tests ... OK`).
