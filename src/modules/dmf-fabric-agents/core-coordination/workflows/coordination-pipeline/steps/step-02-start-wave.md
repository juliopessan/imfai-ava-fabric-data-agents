# Step 02 — Start Wave

**Agente:** migration-coordinator  
**Task:** start-wave  
**Input:** `projects/{project_name}/context/project-config.yaml`, `agent-task-config.yaml`  
**Output:** wave iniciada com trace_id registrado

## Instrução
Ativar `migration-coordinator` e executar `*start-wave`. O agente valida o wave-config, gera o trace_id, registra o início da wave e dispara o primeiro módulo (upstream-discovery).

## Critério de Conclusão
- [ ] `wave-config` validado pelo `validate_wave_config.py`
- [ ] trace_id UUID gerado e registrado
- [ ] upstream-discovery pipeline iniciado
