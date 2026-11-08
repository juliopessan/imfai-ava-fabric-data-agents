# Token Metrics Dashboard

Dashboard HTML que mostra, por execução, os valores **observados** de tokens, compressão e custo.
Código: `src/shared/scripts/token_metrics_dashboard.py` · Testes: `src/shared/tests/test_token_metrics_dashboard.py`.

O dashboard não gera métricas. Se uma métrica não foi observada, ela aparece como **Indisponível**.
Uma execução sem nenhuma métrica mostra o estado vazio ("Sem métricas observadas para esta execução.")
e **não** mostra valor de economia.

## Origem de cada métrica

| Métrica exibida | Origem | Disponibilidade |
|---|---|---|
| Tokens de entrada | `ExecutionTelemetry.generate_report()["metrics"]["input_tokens"]` (`execution_telemetry.py`) ou campo `input_tokens` do JSON de entrada | Indisponível se ausente |
| Tokens de saída | `ExecutionTelemetry.generate_report()["metrics"]["output_tokens"]` ou campo `output_tokens` do JSON | Indisponível se ausente |
| Taxa de compressão | `CompressionStats.compression_ratio` (`headroom_context_manager.py`), exibida em % | Indisponível sem evento de compressão |
| Método de compressão | `CompressionStats.method` (`headroom` ou `mock`) | Indisponível sem evento de compressão |
| Tokens economizados | Calculado: `CompressionStats.input_tokens - output_tokens` | Indisponível sem evento de compressão |
| Economia estimada (USD) | Calculado: tokens economizados × preço de entrada do modelo | Só aparece com compressão **e** preço cadastrado |
| Custo (USD) | Calculado: tokens de entrada/saída × tabela de preços do modelo | Indisponível sem modelo, sem preço cadastrado ou sem tokens |
| Unidade de preço | Campo `unit` da tabela de preços (`USD / 1K tokens` ou `USD / 1M tokens`) | Indisponível junto com o custo |

Observações:

- Compressão com `method = mock` é uma estimativa heurística, não uma medição. O dashboard marca
  essas execuções com o aviso "Compressão simulada (mock), não medida."
- Os tokens de `ExecutionTelemetry` incluem contagens estimadas pelo chamador; o dashboard apenas exibe o valor recebido.
- A tabela de preços padrão (`DEFAULT_PRICE_TABLE`) contém só o preço já registrado no repositório
  (`claude-haiku`: 0,80 / 2,40 USD por 1M tokens, de `execution_telemetry.py`). Modelos fora da tabela
  ficam com custo indisponível; passe a tabela própria em `render_dashboard(runs, price_table)`.

## Uso

```bash
python -m src.shared.scripts.token_metrics_dashboard --input runs.json --output dashboard.html
```

`runs.json` é uma lista; todo campo exceto `run_id` é opcional:

```json
[
  {
    "run_id": "wave-001-upstream",
    "model": "claude-haiku",
    "input_tokens": 130808,
    "output_tokens": 65404,
    "compression": {"input_tokens": 130808, "output_tokens": 39242, "compression_ratio": 0.7, "method": "headroom"}
  },
  {"run_id": "wave-001-sem-metricas"}
]
```

Em Python: `run_from_telemetry_report(run_id, report, model, compression)` e `compression_from_stats(stats)`
convertem `ExecutionTelemetry` e `CompressionStats` para o dashboard.

## Testes

```bash
python -m pytest src/shared/tests/test_token_metrics_dashboard.py -q
```

A suíte de UI usa Playwright (Chromium) e verifica dados e estado vazio nos viewports de 1440 px e
390 px, incluindo ausência de rolagem horizontal. Instale o navegador com `playwright install chromium`;
sem Playwright/Chromium esses testes são pulados (com motivo), e os demais continuam rodando.
