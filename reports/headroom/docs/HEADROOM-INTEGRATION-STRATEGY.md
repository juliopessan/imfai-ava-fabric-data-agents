# Headroom Integration Strategy — Token Optimization para DMF

**Data:** 2026-06-15  
**Status:** 📋 Blueprint (pronto para implementação)  
**Owner:** Migration Wave Orchestrator (migration-coordinator)

---

## 1. Situação Atual do Repositório

### ✅ Token Metrics (já implementado)

| Componente | Status | Função |
|---|---|---|
| `token_metrics_collector.py` | ✅ Ativo | Coleta uso de tokens por agente/fase |
| `dashboard_server.py` | ✅ Pronto | Visualiza metrics em tempo real (Flask) |
| `TOKEN-METRICS-GUIDE.md` | ✅ Completo | Documentação de tracking |
| **Tracking Atual** | Downstream | Conta tokens *após* consumo |

### 🔴 Gap: Compressão de Contexto

- Sem otimização de contexto: **cada requisição ao agente envia dados brutos**
- Sem CCR (Compress-Cache-Retrieve): dados não são recuperáveis
- Sem cache estável: KV cache não aproveita prefixos comprimidos
- Sem multi-agent context: dados entre agentes não são comprimidos

---

## 2. O que Headroom Oferece

### Redução de Tokens: 70–90% em cenários reais

| Tipo de Dado | Redução | Caso DMF |
|---|---|---|
| **JSON arrays** (tool outputs) | 70–90% | Resultados de STTM, schema mapping |
| **Source code** (Git diffs, DDL) | 40–70% | Arquivos .sql, diffs de migração |
| **Build/test logs** | 80–95% | Logs de validação de gate |
| **Search results** (DB queries) | 60–80% | Resultados de discovery queries |
| **Plain text** (análise) | 30–50% | Saídas de análise de agentes |

### Exemplo DMF: Data Architect → Code Generator

**Antes (sem Headroom):**
```
Data Architecture Designer (data-architect) output: 45K tokens (schema completo)
  → raw para Code & ETL Generator (code-generator)
  → Code & ETL Generator envia para LLM: 45K + 12K contexto = 57K tokens
  
Total: 57K tokens
Custo: ~$0.085 USD
```

**Depois (com Headroom CCR):**
```
Data Architecture Designer output: 45K tokens → compress() → 5.4K tokens (88% redução)
  → Code & ETL Generator recebe 5.4K + headroom_retrieve tool
  → Se Code & ETL Generator precisa detalhe: usa headroom_retrieve (hit de cache)
  
Total (sem retrieve): 5.4K tokens
Custo: ~$0.008 USD
Economia: $0.077 USD por handoff (90%)
```

---

## 3. Oportunidades de Integração

### 3.1 **Compressão de Saídas de Agentes** (Prioridade 🔴 ALTA)

**Momento:** Depois que agente completa → antes de enviar para próximo

**Agentes beneficiados:**
- `data-architect` → `code-generator`: diffs + schemas (40–70% redução)
- `data-modeler` → `business-analyst`: data models JSON (70–90%)
- `discovery-scout` → `data-strategist`: inventário + queries (60–80%)

**Implementação:**
```python
# Em migration-coordinator.py
from headroom import compress

def handoff_to_next_agent(current_output: dict, next_agent: str):
    # Comprimir saída antes de passar
    compressed = compress(
        current_output,
        model="gpt-4o",  # ou Azure OpenAI
        store_originals=True  # CCR: guardar originals
    )
    
    stats[next_agent]["tokens_saved"] = compressed["tokensSaved"]
    return compressed["content"]
```

### 3.2 **Cache Otimizado para KV-Cache** (Prioridade 🟡 MÉDIA)

**Momento:** Em agentes de longa execução (> 50K tokens)

**Benefícios:**
- Prefixo comprimido se estabiliza → hits de cache provider (90% discount)
- Menos re-compute de embeddings

**Agentes candidatos:**
- `logic-extractor`: processa grandes arquivos .sql
- `reconciliation`: analisa divergências grandes

### 3.3 **Persistência de Context Comprimido** (Prioridade 🟡 MÉDIA)

**Momento:** Entre gates (Gate 1 → Gate 2 → Gate 3)

**Implementação com AgentDB (já no repo):**
```python
# Em gate_score_report.py
from agentdb import AgentDB
from headroom import compress

gate1_output = load_gate1_artifacts()
compressed = compress(gate1_output, store_originals=True)

# Store comprimido + retriever
db.store({
    "gate": 1,
    "compressed_content": compressed["content"],
    "retriever_id": compressed["retrieverId"],  # Para headroom_retrieve
})
```

### 3.4 **Failure Learning + Compression** (Prioridade 🟢 BAIXA — futuro)

**Momento:** Agent falha → analisar logs comprimidos → aprender

Headroom detecta anomalias em logs grandes sem perder erros críticos.

---

## 4. Plano de Implementação (12 semanas)

### **Fase 1: Proof of Concept** (Semana 1–2)

**Objetivo:** Validar redução de tokens em 1 handoff real

```bash
# Step 1: Instalar Headroom
pip install headroom-ai

# Step 2: Setup MCP tools (Headroom já tem MCP integrado)
headroom mcp install

# Step 3: Integração em mock
python src/shared/scripts/headroom_poc.py \
  --input projects/clientebanco/outputs/midstream/architecture.json \
  --agent data-architect \
  --output reports/headroom-poc-results.json
```

**Métricas a coletar:**
- Tokens antes/depois
- Latência (compressão + envio)
- Custo poupado (USD/BRL)

**Gate:** ✅ Redução > 50% de tokens OU Skip (não viável)

---

### **Fase 2: Integração em Migration Coordinator** (Semana 3–5)

**Arquivo novo:** `src/shared/scripts/headroom_context_manager.py`

```python
class HeadroomContextManager:
    """Gerencia compressão de contexto entre agentes."""
    
    def __init__(self, store_path: str = "/tmp/headroom-store"):
        self.compress = compress
        self.store_path = store_path
    
    def compress_handoff(self, data: dict, source: str, target: str) -> dict:
        """Comprime output de agent antes de passar para próximo."""
        
    def retrieve_if_needed(self, retriever_id: str) -> dict:
        """Recupera original via headroom_retrieve."""
```

**Integrar em:** `migration-coordinator.py` + cada agente handoff

---

### **Fase 3: Dashboard Upgrade** (Semana 6–7)

**Novo widget em `dashboard_server.py`:**

| Métrica | Cálculo | Exibição |
|---|---|---|
| **Tokens Economizados** | sum(tokensSaved por handoff) | `342K → 51K (85% redução)` |
| **USD Economizado** | tokens_saved * $0.0015 | `$0.51 USD economizado` |
| **Taxa de Hit de Cache** | cache_hits / total_requests | `72% KV cache reuse` |
| **Compressão por Tipo** | JSON vs logs vs code | Stacked bar chart |

---

### **Fase 4: Governança + Testes** (Semana 8–12)

**Adicionar validações:**

```python
# src/shared/scripts/validate_headroom_compliance.py
def validate_compression(artifact: dict, min_ratio: float = 0.70):
    """Gate: redução mínima de 30% ou falha."""
    
    ratio = artifact["compressionRatio"]
    if ratio < min_ratio:
        return {
            "status": "FAILED",
            "reason": f"Compression only {ratio*100:.0f}%, need >{min_ratio*100:.0f}%",
        }
    return {"status": "PASSED", "saved_tokens": artifact["tokensSaved"]}
```

**Testes:**
- 23 novos testes em `src/shared/tests/test_headroom_integration.py`
- Validação: output original recoverable via headroom_retrieve
- Benchmark: latência + accuracy

---

## 5. Impacto Financeiro Estimado

### Cenário: ClienteBanco Tier 1 + Tier 2 (18K tokens mensais em produção)

**Sem Headroom:**
- 18,000 tokens/mês × $0.0015 = **$27 USD/mês**

**Com Headroom** (75% de compressão em handoffs):
- 18,000 × 0.25 = 4,500 tokens/mês × $0.0015 = **$6.75 USD/mês**
- **Economia: $20.25/mês ou $243/ano**

**Com Scale (10 projects como ClienteBanco):**
- **Economia: $2,430/ano**

**Mais importante:** ⏱️ Latência reduzida → ciclos de gate mais rápidos

---

## 6. Roadmap de Decisão

### ✅ **GO** se:
- [ ] PoC reduz tokens > 50%
- [ ] Latência compressão < 500ms
- [ ] Originals 100% recoveráveis (CCR test)
- [ ] Compatível com Azure OpenAI + Microsoft Stack

### 🛑 **NO-GO** se:
- [ ] Redução < 30% (não compensa overhead)
- [ ] Dependency em ferramentas não-Microsoft (❌ Headroom é open-source, aceito se MS-compatible)
- [ ] Latência > 2s (pipeline slows down)

---

## 7. Próximos Passos

### Semana de 2026-06-15:

1. **[IMMEDIATE]** Ler docs: https://headroom-docs.vercel.app/docs/quickstart
2. **[IMMEDIATE]** Rodar exemplo Headroom com arquivo de teste:
   ```bash
   python -m headroom compress \
     --input projects/clientebanco/outputs/midstream/architecture.json \
     --model "gpt-4o"
   ```
3. **[2 DAYS]** Criar PoC script (`src/shared/scripts/headroom_poc.py`)
4. **[3 DAYS]** Testar com 3 handoffs reais (discovery → architect, architect → modeler, etc.)
5. **[GATE]** Revisar resultados → decisão GO/NO-GO

---

## 8. Compliance & Constraints

### Stack Checks:
- ✅ **Headroom:** MIT open-source, suporta Azure OpenAI via LiteLLM
- ✅ **Framework:** Python + TypeScript SDKs disponíveis
- ✅ **Storage:** CCR store pode usar SQLite local (já em repo) ou Cosmos DB
- ✅ **Microsoft-only:** Integrado com Azure OpenAI (não chama OpenAI public API)

### Governance:
- Adicionar `headroom_context_manager` ao `validate_agent_contracts.py`
- Log de compressão em cada gate: `gate{N}-compression-report.md`
- Audit trail: quem comprimiu, quanto economizou, quando recuperou originals

---

## 📊 Sumário Executivo

**Por que Headroom agora?**
1. Tokens são custo real (18K/mês × $0.0015 = $27 USD em ClienteBanco)
2. Já temos token tracking (`token_metrics_collector.py`) — Headroom é próximo passo natural
3. 75–90% compressão validada em mil+ deployments (Headroom community stats)
4. Handoffs de agentes são pontos ótimos para compressão

**Risco:** Nenhum — PoC é 2–3 dias, go/no-go decision antes de semana 2

**Win:** 85% economia de tokens + cache otimizado + arquivos recuperáveis

---

**Author:** System  
**Last Updated:** 2026-06-15  
**Status:** 🟡 Awaiting PoC decision
