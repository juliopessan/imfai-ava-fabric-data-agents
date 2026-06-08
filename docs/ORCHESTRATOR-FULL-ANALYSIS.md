**Orchestrator — Full Analysis Workflow**

Context: Orquestrador sequencial para executar validações e relatórios de gate para uma `wave`/projeto.

Recommended sequence (implemented in `src/shared/scripts/run_full_analysis.py`):

- `validate_wave_config` — valida config da wave (YAML)
- `validate_gate1_artifacts` — valida artefatos Gate 1
- `validate_gate2_artifacts` — valida artefatos Gate 2
- `validate_gate3_artifacts` — valida artefatos Gate 3
- `gate_score_report` — calcula GateScore e gera relatório
- `wave_status_tracker` — consolida estado da wave

Behavior:
- O runner executa cada módulo em sequência, pulando módulos ausentes e reportando avisos em caso de falha.
- Design seguro para CI: não falha o job se um módulo estiver ausente (mas retorna código != 0 caso algum módulo presente falhe).

Where to include or adjust instructions:

- `docs/PLAYBOOK-MIGRATION-OPERATIONS.md`: adicionar uma seção "Run full analysis" com o comando exemplo:
  - `python -m src.shared.scripts.run_full_analysis projects/<project>/outputs/WAVE-XXX`
- `docs/COPILOT-AGENTS-GUIDE.md` / `AGENTS.md`: para agentes orquestradores (e.g., `master-agent` ou `migration-coordinator`), na frontmatter e `body` incluir uma referência a esta sequência e ao arquivo `src/shared/scripts/run_full_analysis.py` como opção programática de execução.
- `azure-pipelines.yml` or `.github/workflows/*`: adicionar job/trigger que invoque o orchestrator (ex.: `full-analysis.yml` workflow presente neste repositório).
- `src/shared/scripts/` — garantir que os módulos referenciados (`validate_wave_config.py`, `validate_gate1_artifacts.py`, etc.) existam; caso contrário, implementar stubs que executem validações mínimas.

Example local run (PowerShell):
```
.
.venv\Scripts\Activate.ps1
python -m src.shared.scripts.run_full_analysis projects/bradesco/outputs/WAVE-002
```

Next actions:
- Add/implement missing validator scripts or extend the orchestrator sequence to call project-specific scripts (upstream phases) when present.
- Wire the orchestrator into the `master-agent` instructions and Copilot Studio agent definitions where orchestration is required.
