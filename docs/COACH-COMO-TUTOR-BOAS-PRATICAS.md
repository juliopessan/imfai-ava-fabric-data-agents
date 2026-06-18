# DMF Coach como Tutor de Boas Práticas — O Caso de Uso

**Data:** 2026-06-18  
**Público:** Engenheiros de dados, Orquestra de agentes, Leadership

---

## O Problema

### Hoje (2026-06-18)
- ✅ Temos uma **Fábrica de Dados funcionando** (21 agentes, 4 ondas/projetos)
- ✅ Temos **gates de qualidade** (GateScore 0.70–0.89)
- ❌ Mas **faltam insights evolutivos** após cada onda
- ❌ **Não detectamos anti-patterns** até tarde (pós-Gate 2)
- ❌ **Não escalamos skills reusáveis** de onda para onda
- ❌ **Não vemos tendências** (está piorando ou melhorando?)

### O Resultado
- **Desperdício de contexto:** Artifacts crescem 300% entre Gate 1 → 2
- **Retrabalho:** STTM regenerada 4× numa onda (sinalizador de caos)
- **Execução silenciosa:** Downstream-executor diz "sucesso" mas não escreveu tabelas
- **Custo escondido:** Modelagem usando GPT-4 em tasks parametrizadas
- **Fadiga organizacional:** Sem feedback, time não melhora

---

## A Solução: Coach como Tutor

### Missão
> Após cada execução de agente, **capturar sinais**, **detectar problemas**, **sugerir melhorias** — e fazer isso **invisível para o usuário**.

### As 4 Responsabilidades de um Tutor

#### 1️⃣ Observar (Observe)
**O Coach vê:**
- Quando cada agente rodou
- Qual modelo foi usado
- Quanto tempo levou
- Quantos tokens consumiu
- Qual artefato foi gerado

**Resultado:** Timeline executiva (quem fez o quê e quando)

**Exemplo:**
```
Wave: bradesco_wave_2 | Gate: 1
├─ 14:00 discovery-scout      15 min | 12.5k tokens | $0.045
├─ 14:20 data-architect       15 min | 11.2k tokens | $0.042
├─ 14:40 business-analyst     30 min | 18.3k tokens | $0.068 ⚠️ (regenerated 3x)
├─ 15:15 data-modeler         45 min | 16.7k tokens | $0.062
└─ 16:00 [pending]
```

#### 2️⃣ Medir (Measure)
**O Coach calcula:**
- Produtividade por agente (tokens/hora)
- Custo efetivo ($ por feature descoberta)
- Consumo de contexto (% da janela usada)
- Padrões de trabalho (noturno? fim de semana? burnout?)

**Resultado:** Dashboard de métricas (burndown, distribuição de custo, tempo)

**Exemplo:**
```
MEDIDAS — Bradesco Wave 2
├─ Tokens gerados: 78.7K (vs 65K em Wave 1) ↑21%
├─ Custo total: $0.289 (vs $0.245 em Wave 1) ↑18%
├─ Tempo Gate 1: 120 min (vs 105 min em Wave 1) ↑14%
├─ Agente mais caro: business-analyst $0.068 (23.5% total)
└─ Agente mais rápido: discovery-scout 15 min
```

#### 3️⃣ Melhorar (Improve)
**O Coach detecta:**
- Entidades descobertas mas não mapeadas em STTM (cobertura 87%, alvo 90%)
- STTM regenerada 3× em 2 horas (sinalizador de confusão)
- GPT-4 usado em task paramétrica (downgrade para Haiku = -88% custo)
- Artifacts consumindo 77% do context window (split em 2 waves)
- Executor output com < 1000 tokens (silencioso = falha não detectada)
- GateScore caindo 7% onda-a-onda (trend negativa)

**Resultado:** Recomendações acionáveis (o que fazer → quem → quando)

**Exemplo:**
```
🚨 PROBLEMAS DETECTADOS — Bradesco Wave 2

1. STTM Instabilidade (Score -10)
   Problem: Regenerada 3 vezes em 2 horas
   Action: Requête com stakeholders antes de Gate 2 sign-off
   Owner: Business-Analyst (Vicente)
   
2. Model Overreliance (Score -5)
   Problem: discovery-scout usou GPT-4 ($0.075 waste)
   Action: Downgrade discovery-scout.model → claude-haiku
   Owner: Migration-Coordinator (config)
   
3. Context Bloat (Score 0, monitor)
   Problem: Gate 1 artifacts: 53.2 KB (77% window)
   Action: Watch for auto-compaction em Wave 3
   Owner: Data-Architect (future architecture)
```

#### 4️⃣ Elevar (Level Up)
**O Coach descobre:**
- "PII-validation pattern" apareceu em 4 waves (prompts recorrentes)
  → Proposta: Criar skill `ava-dmf-pii-validator` + adicionar a data-steward template
- "Column lineage extraction" apareceu 2 vezes
  → Proposta: Documentar para logic-extractor reuse

**Resultado:** Skill library evolutiva (reutilização automática)

**Exemplo:**
```
💡 SKILLS DESCOBERTAS — Bradesco + Einstein + Headroom

1. PII Validation Pattern (encontrado 7×)
   Prompts recorrentes: "Validate if column X contains PII"
   Proposta: Criar skill `ava-dmf-data-steward-pii-validator`
   
2. Column Lineage Pattern (encontrado 3×)
   Prompts recorrentes: "Extract lineage from SQL views"
   Proposta: Documentar para logic-extractor reuse
   
3. Stakeholder Requête Pattern (encontrado 5×)
   Prompts recorrentes: "Clarify requirement with stakeholder"
   Proposta: Auto-invoke quando STTM instability detectada
```

---

## Como Funciona a Tutoria (Operacional)

### O Ciclo de Feedback

```
┌─────────────────────────────────────────────────┐
│ 1. EXECUÇÃO (Agent rodando)                     │
│    migration-coordinator.spawn_agent(...)       │
│    → Coach observa → telemetria capturada       │
└──────────────┬──────────────────────────────────┘
               ↓
┌─────────────────────────────────────────────────┐
│ 2. QUALIDADE (Gate check)                       │
│    quality-gate.validate(...)                   │
│    → Coach mede → anti-patterns detectados      │
│    → GateScore ajustado                         │
└──────────────┬──────────────────────────────────┘
               ↓
┌─────────────────────────────────────────────────┐
│ 3. ANÁLISE (Fim da onda)                        │
│    wave_status_tracker.mark_wave_complete(...)  │
│    → Coach analisa → relatório gerado           │
│    → Skills propostas + recomendações           │
└──────────────┬──────────────────────────────────┘
               ↓
┌─────────────────────────────────────────────────┐
│ 4. APRENDIZADO (Próxima onda)                   │
│    → Team aprende com feedback                  │
│    → Skill criada + integrada                   │
│    → Processo melhora iterativamente            │
└─────────────────────────────────────────────────┘
```

### Exemplos de Tutoria em Ação

#### Exemplo 1: Deteção de Sinal Silencioso
```
Downstream-executor rodou com "sucesso"
├─ Output: 847 tokens (< 1000 threshold)
├─ Artifact size: 2.1 KB (< 10 KB threshold)
└─ → Coach: 🚨 CRÍTICO! Executor não escreveu tabelas!

TUTOR AÇÃO:
1. Alerta: "Silent executor failure detected"
2. Score: -30 pts (penalidade crítica)
3. Ação: "Auto-trigger self-healing agent"
4. Follow-up: Rodar self-healing, validar output real

RESULTADO: Falha é pega PRÉ-Gate 3 (não post-mortem)
```

#### Exemplo 2: Escalação de Skill Reutilizável
```
Wave 1 (6 semanas atrás):
├─ Discovery: "Validate PII in columns A, B, C"
├─ Custo: 0.5 horas human guidance
└─ Resultado: Template armazenado (logs)

Wave 2 (3 semanas atrás):
├─ Discovery: "Validate PII in columns X, Y, Z"
├─ Coach: "Detectado PII-validation pattern"
├─ Proposta: "Usar template anterior"
└─ Custo: 0.1 horas (5x mais rápido)

Wave 3 (hoje):
├─ Discovery: "Validate PII in columns..."
├─ Coach: "Skill já existe → ava-dmf-pii-validator"
├─ Action: "Invocar skill diretamente"
└─ Custo: 2 minutos (parametric, zero thinking)

GANHO CUMULATIVO: 0.5h → 0.1h → 0.033h (15× mais rápido em 3 ondas)
```

#### Exemplo 3: Prevenção de Cascade
```
Wave 2, Gate 1:
├─ discovery-scout output: 127 entities
├─ business-analyst STTM: 98 entities mapeadas (87% cobertura)
├─ Coach: ⚠️ "Entity gap de 23% (alvo 90%)"
├─ Ação: "Requête com stakeholders"
└─ Resultado: Descobre que 29 entities estão fora-de-scope (expectativa corrigida)

SEM COACH:
├─ Discrepância passa despercebida
├─ Downstream (data-modeler) recebe STTM incompleta
├─ Modela apenas 98/127 tabelas
├─ Descobre gap em Gate 2 (tarde demais)
├─ Retrabalho: +2 dias, custo +$2K

COM COACH:
├─ Gap detectado em Gate 1 (+2 horas)
├─ Clarificação com sponsor
├─ STTM corrigida antes de Gate 2
├─ Sem retrabalho, sem surpresas
├─ Economia: $2K + 2 dias
```

---

## Métricas de Sucesso (Coach como Tutor)

### O Que Esperamos Melhorar

| Métrica | Baseline (Sem Coach) | Com Coach (Alvo) | Melhoria |
|---------|----------------------|------------------|----------|
| **GateScore Variância** | σ² = 0.008 | σ² = 0.004 | -50% (mais previsível) |
| **Detecção de falhas silenciosas** | 0% (pós-mortem) | 100% (pré-Gate 3) | Detecta tudo |
| **Retrabalho por onda** | Avg 1.2 dias | Avg 0.3 dias | -75% retrabalho |
| **Skills reutilizáveis/factory** | ~0 | 5–10 | +∞ (valor emergente) |
| **Consumo de contexto (artifacts)** | Média 52 KB | Máx 40 KB | -23% otimização |
| **Custo por entidade descoberta** | $0.015 | $0.010 | -33% eficiência |
| **Regenerações STTM/onda** | Avg 2.8× | Avg 1.2× | -57% (menos confusão) |
| **Time satisfaction** | Sem feedback → frustração | Feedback contínuo → clareza | +X NPS |

### Como Medir

Coach captura telemetria automaticamente. Métricas calculadas ao fim de cada onda:

```python
# Ao fim da onda
coach_report = telemetry_collector.summarize_wave('bradesco_wave_2')
# Retorna: event_count, agents_used, gates_covered, total_tokens, total_cost_usd, total_time_sec

anti_patterns = anti_pattern_detector.generate_report('bradesco_wave_2')
# Retorna: [list of AntiPattern objects com evidence + action]

trend = compare_waves(['bradesco_wave_1', 'bradesco_wave_2', 'bradesco_wave_3'])
# Retorna: WoW/MoM trends, regressions, improvements
```

---

## Coach como Tutor: A Diferença

### Sem Coach (Hoje)
```
Wave 1 → Gate 1 ✓ → Gate 2 ✓ → Gate 3 ✓ [Post-mortem: "What went well?"]
Wave 2 → Gate 1 ⚠️ → Gate 2 ❌ (surpresa!) → Retrabalho 2 dias
Wave 3 → Gate 1 ⚠️ → Gate 2 ⚠️ → Gate 3 ⚠️ (mesmos problemas, sem aprendizado)
```

### Com Coach (2026)
```
Wave 1 → [Telemetria capturada, baseline estabelecida]
Wave 2 → [Coach detecta 3 anti-patterns PRÉ-Gate 2]
         → ["STTM instability + entity gap + executor silence"]
         → [Team fixa ANTES de Gate 2]
         → [Onda completa com melhor qualidade]
Wave 3 → [Mesmos problemas NÃO recorrem]
         → ["Skills de onda anterior reutilizadas"]
         → [Onda 3 MAIS RÁPIDA e MAIS BARATA]
         → [GateScore: 0.82 → 0.85 → 0.88 (trend positiva)]
```

---

## Essencial para Ser "Tutor" (Check-list)

### ✅ Obrigatório (Sem isso, não é tutor)
- [x] **Observação** — Capturar eventos de execução (telemetria)
- [x] **Análise** — Detectar padrões (6 anti-patterns DMF-específicos)
- [x] **Feedback** — Gerar recomendações acionáveis (action-oriented)
- [x] **Memória** — Comparar onda-a-onda (detecção de trends)

### 🟡 Altamente Desejável
- [ ] **Scoring** — Ajustar GateScore automaticamente
- [ ] **Skill discovery** — Propostas de reutilização
- [ ] **Context audit** — Validar saúde de .agent.md
- [ ] **Gamification** — Badges, achievements, learning center

### 🔵 Nice-to-Have (Value-add, não crítico)
- [ ] **Auto-pause** — Pausar onda se qualidade < threshold
- [ ] **Rules marketplace** — Compartilhar rules entre factories
- [ ] **Predictive** — ML para antecipar problemas

---

## Conclusão

Coach é um **tutor silencioso** para a Fábrica de Dados:
- ✅ Observa cada execução (sem intrusi

vidade)
- ✅ Detecta problemas **antes** de ficarem piores
- ✅ Propõe soluções específicas (não genéricas)
- ✅ Aprende de onda para onda (feedback loop)
- ✅ Escalona skills reutilizáveis (automação)

**Resultado:** Uma fábrica que melhora **continuamente**, com **feedback em tempo real**, e **menos surpresas**.

---

**Próximo Passo:** Aprovar Sprint 1 (telemetria + integração)  
**Data:** June 25–July 5, 2026  
**Owner:** [TBD]

