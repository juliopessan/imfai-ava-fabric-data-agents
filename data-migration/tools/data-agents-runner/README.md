# data-agents-runner (local)

This folder contains a small, dependency-free Node.js CLI to run the `data_agents` module *without* the BMAD runtime.

It does **not** call any LLM by itself. It orchestrates the module by checking/creating files in `_bmad-output/<project_code>/...`.

## What it can do

- Ensure the artifact folder structure exists (via the module installer).
- Generate/update `planning-artifacts/status.md` (similar to `workflow-status`).
- Validate Gate 1 / Gate 2 / Gate 3 based on presence of required artifacts.
- Orchestrate: decide the next workflow suggestion based on state + missing artifacts.

## Outputs

All outputs are written under:

- `{artifacts_root}/{project_code}/planning-artifacts/`
- `{artifacts_root}/{project_code}/implementation-artifacts/`

By default:

- `artifacts_root = {project-root}/_bmad-output`
- `project_code = trip-data-poc`

## Run (Windows cmd.exe)

```cmd
node tools\data-agents-runner\cli.js selftest
node tools\data-agents-runner\cli.js workflow-status
node tools\data-agents-runner\cli.js gate-1
node tools\data-agents-runner\cli.js orchestrate
```

## Configuration

You can override defaults using args:

- `--project-root` (defaults to repo root)
- `--artifacts-root` (defaults to `{project-root}/_bmad-output`)
- `--project-code` (defaults to `trip-data-poc`)

Example:

```cmd
node tools\data-agents-runner\cli.js orchestrate --project-code my-real-project
```
