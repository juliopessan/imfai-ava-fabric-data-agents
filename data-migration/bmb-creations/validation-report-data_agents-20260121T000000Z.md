---
validationDate: 2026-01-21
targetType: full
moduleCode: data_agents
targetPath: src/modules/data_agents/
status: COMPLETE
summary:
  fileStructure: PASS
  moduleYaml: PASS
  agentSpecs: PASS
  workflowSpecs: PASS_WITH_NOTES
  documentation: PASS
  installationReadiness: PASS_WITH_NOTES
notes:
  - "Workflow spec buildTrackingFile path typo detected in BMAD step template (not in this module): step-06-workflows.md references {bmad_creations_output_folder}; module uses our tracking file path directly. No action needed."
  - "No IDE-specific handlers were created in _module-installer/platform-specifics/. This is OK unless required."
recommendations:
  - "Next: run agent-builder on each agents/*.spec.md to generate final agent files."
  - "Next: run workflow-builder on each workflows/*/*.spec.md to generate runnable workflows."
  - "Consider adding a single shared workflow for 'data-quality' if you want to split governance into dq-rules vs monitoring."

# Validation Report — data_agents

## Target
- Module: `data_agents`
- Path: `src/modules/data_agents/`

## Checks

### 1) File structure
- Found: `module.yaml`, `README.md`, `TODO.md`, `docs/`, `agents/`, `workflows/`, `_module-installer/` ✅

### 2) module.yaml
- Required fields present: `code`, `name`, `header`, `subheader`, `default_selected` ✅
- Variables present and well-formed: `platform_target`, `project_code`, `artifacts_root`, `enable_bi_agent` ✅

### 3) Agent specs
- Found 10 `*.spec.md` in `agents/` ✅
- Naming is consistent (kebab-case) ✅

### 4) Workflow specs
- Found 14 workflow folders with `*.spec.md` ✅
- Core flows cover UP/MID/DOWN + gates + routing ✅

### 5) Docs
- Found `docs/getting-started.md`, `docs/agents.md`, `docs/workflows.md`, `docs/examples.md` ✅

### 6) Installation readiness
- Installer present: `_module-installer/installer.js` ✅
- Creates artifact folders based on `artifacts_root` + `project_code` ✅

