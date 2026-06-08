# Agent Instructions

## Environment

Use **Python 3.13+** with venv: `.venv\Scripts\Activate.ps1`
Dependencies: `pip install pytest pyyaml`

## File-Scoped Commands

| Task              | Command                                                    |
| ----------------- | ---------------------------------------------------------- |
| All tests         | `python -m pytest tests/ -q`                               |
| Single test       | `python -m pytest tests/test_<module>.py -v`               |
| Validate wave     | `python -m scripts.validate_wave_config <file>.yaml`       |
| Validate Gate N   | `python -m scripts.validate_gate{1,2,3}_artifacts <dir>`   |
| Run full analysis  | `python -m src.shared.scripts.run_full_analysis projects/<project>/outputs/WAVE-XXX` |
| Chatmode align    | `python -m scripts.check_chatmode_alignment --root .`      |
| Lint              | `ruff check scripts/ tests/`                               |

## Commit Attribution

AI commits MUST include:

```text
Co-Authored-By: GitHub Copilot <noreply@github.com>
```

## Key Conventions

- **Wave config:** validate with `validate_wave_config.py` before Gate 1
- **Gate decisions:** record in `gate{N}-decision.md` with score + approvers
- **Agent outputs:** store in `<agent-name>-agent/<domain>-outputs/`
- **Platform agnostic:** never hardcode Databricks/Fabric/Snowflake
- **Entry point:** start with `master-agent` → `*route`
- **Coordinator:** use `migration-coordinator` (Orion), NOT `orchestrator` (deprecated)
- **Artifact ownership:** Winston → `architecture.md`, `decisions.md`, `monitoring-spec.md`; Sofia → `data-model.md`, `data-contracts.md`
- **Scripts:** always run tests after editing — expected `python -m pytest tests/ -q` → all passed

## Structure

- `scripts/` — 23 governance modules (see `scripts/README.md`)
- `tests/` — full pytest coverage
- `.github/agents/` — 19 chatmode agents
- `.github/skills/` — 26 domain skills
- `docs/` — playbooks, PRD, operating model
- `wave-config-sample.yaml` — reference template
