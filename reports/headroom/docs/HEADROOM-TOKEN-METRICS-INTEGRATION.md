# Headroom + Token Metrics — Integração

**Relação:** Headroom (redução) + Token Metrics (tracking) = **Complete Token Optimization Stack**

---

## 🎯 Quadro Atual (Sem Headroom)

### Fluxo Atual

```
Agent A (45K tokens)
  ↓
outputs/[phase]/[artifact].json
  ↓
Agent B lê arquivo (45K tokens injetados no contexto)
  ↓
token_metrics_collector.py coleta: "45K tokens consumidos"
  ↓
dashboard_server.py exibe: "Agente B: 45K tokens"
  ↓
Realização: "Consumemos 45K tokens" 💸
```

**Problema:** Métricas mostram consumo *após* acontecer. Sem otimização.

---

## 🚀 Quadro Com Headroom (Proposto)

### Novo Fluxo

```
Agent A (45K tokens)
  ↓
compress() ← NOVO: Headroom comprime antes de passar
  ↓ 
Comprimido: 5.4K tokens (no arquivo ou contexto)
  ↓
Agent B lê (5.4K tokens injetados)
  ↓
token_metrics_collector.py coleta: "5.4K tokens consumidos + 39.6K saved"
  ↓
dashboard_server.py exibe:
    - Input: 45K
    - Output: 5.4K
    - Saved: 39.6K (88%)
    - Cost avoided: $0.059 USD
  ↓
Realização: "Economizamos 88% de tokens" 🎯💰
```

**Ganho:** Métricas + otimização = visibilidade + economia.

---

## 📊 Integração de Componentes

### 1. Token Metrics Collector (Existente)

**Arquivo:** `reports/_templates/token_metrics_collector.py`  
**Status:** ✅ Pronto  
**Faz:** Coleta de tokens por agente/fase

**Mudança com Headroom:**
```python
# Adicionar campos comprimidos
metrics = {
    "agent": "data-architect",
    "input_tokens": 45_000,
    "output_tokens": 5_400,      # ← NOVO
    "tokens_saved": 39_600,       # ← NOVO
    "compression_ratio": 0.88,    # ← NOVO
    "cost_avoided_usd": 0.059,    # ← NOVO
}
```

---

### 2. Dashboard Server (Existente)

**Arquivo:** `reports/_templates/dashboard_server.py`  
**Status:** ✅ Pronto  
**Faz:** Visualiza metrics em Flask

**Novo Widget Headroom:**

```html
<div class="headroom-metrics">
  <h3>⚡ Token Compression (Headroom)</h3>
  <table>
    <tr>
      <td>Tokens Economizados (Period)</td>
      <td>342K → 51K (-85%)</td>
    </tr>
    <tr>
      <td>USD Economizado</td>
      <td>$0.51 USD</td>
    </tr>
    <tr>
      <td>Compression Ratio (Average)</td>
      <td>85% reduction</td>
    </tr>
    <tr>
      <td>Cache Hit Rate</td>
      <td>72% (KV cache reuse)</td>
    </tr>
  </table>
</div>
```

---

### 3. Headroom (Novo)

**Arquivo:** `src/shared/scripts/headroom_poc.py` (PoC) + future integration  
**Status:** 🟡 PoC phase  
**Faz:** Comprime contexto entre agentes

**Integração em:** `src/shared/scripts/headroom_context_manager.py` (Phase 1)

```python
class HeadroomContextManager:
    def __init__(self):
        self.compress = compress  # from headroom
        self.metrics_collector = TokenMetricsCollector()
    
    def compress_and_log_handoff(self, data, source_agent, target_agent):
        """Compress + track metrics."""
        
        # Comprimir
        result = compress(data)
        
        # Log nos metrics
        self.metrics_collector.record_handoff({
            "source": source_agent,
            "target": target_agent,
            "input_tokens": result["inputTokens"],
            "output_tokens": result["outputTokens"],
            "tokens_saved": result["tokensSaved"],
            "compression_ratio": result["compressionRatio"],
        })
        
        return result["content"]  # Passa comprimido para próximo agente
```

---

### 4. Gate Validation (Existente + Enhanced)

**Arquivo:** `src/shared/scripts/validate_gate{N}_artifacts.py`  
**Status:** ✅ Existe  
**Faz:** Valida artifacts em cada gate

**Novo check Headroom:**
```python
def validate_compression(artifact: dict):
    """Gate validation: compression ratio >= 70%"""
    
    ratio = artifact.get("compression_ratio", 0)
    if ratio < 0.70:
        return {
            "status": "FAILED",
            "reason": f"Compression only {ratio*100:.0f}%, need >70%",
        }
    
    saved = artifact.get("tokens_saved", 0)
    cost_saved = saved / 1_000_000 * 0.0015
    
    return {
        "status": "PASSED",
        "tokens_saved": saved,
        "cost_saved_usd": cost_saved,
    }
```

---

## 🔄 Data Flow Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    Migration Coordinator                 │
│                   (orchestration loop)                   │
└────────────────────────┬────────────────────────────────┘
                         │
            ┌────────────┴────────────┐
            │                         │
    ┌───────▼──────────────┐  ┌──────▼────────────┐
    │  Agent A Output      │  │  Compress Flow   │
    │  (45K tokens)        │  │  (Headroom)      │
    └───────┬──────────────┘  └──────┬────────────┘
            │                         │
            │  ← compress() ←─────────┘
            │
    ┌───────▼──────────────────────────────┐
    │  Compressed Output (5.4K tokens)     │
    │  + Retriever ID (CCR store)          │
    └───────┬──────────────────────────────┘
            │
            │
    ┌───────▼──────────────────────────────────────┐
    │  Token Metrics Recorder                      │
    │  • input_tokens: 45,000                      │
    │  • output_tokens: 5,400                      │
    │  • tokens_saved: 39,600                      │
    │  • compression_ratio: 88%                    │
    └───────┬──────────────────────────────────────┘
            │
            │
    ┌───────▼──────────────────────────────────────┐
    │  Dashboard Server (Live Widget)              │
    │  • Compression metrics card                  │
    │  • Savings (USD) display                     │
    │  • Cache hit rate                            │
    │  • Phase distribution (original + saved)    │
    └──────────────────────────────────────────────┘
```

---

## 📈 Sample Dashboard View

**Before Headroom:**
```
Token Usage Analytics
  upstream    :  77,000 ( 22.4%)
  midstream   : 204,000 ( 59.3%)
  downstream :  63,000 ( 18.3%)
  ──────────────────────
  Total       : 344,000 tokens
  Cost        : $0.51 USD
```

**After Headroom:**
```
Token Usage Analytics
  upstream    :  77,000 input  → 10,000 (87% saved)
  midstream   : 204,000 input  → 30,000 (85% saved)
  downstream :  63,000 input   → 8,000 (87% saved)
  ──────────────────────────────────────
  Total input : 344,000 tokens
  Total output: 48,000 tokens (86% reduction)
  
⚡ Compression Metrics
  Tokens Saved      : 296,000
  Cost Avoided      : $0.44 USD
  Cache Hit Rate    : 72% (KV reuse)
```

---

## 🔧 Implementation Roadmap

### Phase 1: PoC + Metrics Integration (Semana 1–2)

| Task | Owner | Status |
|------|-------|--------|
| Run PoC (`headroom_poc.py`) | You | 🟡 Start 6/16 |
| Validate compression > 50% | You | 🟡 Target 6/18 |
| Create `headroom_context_manager.py` | Dev | 🟡 If GO |
| Update `token_metrics_collector.py` | Dev | 🟡 If GO |
| Add compression fields to metrics | Dev | 🟡 If GO |

### Phase 2: Dashboard Integration (Semana 3–4)

| Task | Owner | Status |
|------|-------|--------|
| Add Headroom widget to `dashboard_server.py` | Dev | 🔴 Phase 2 |
| Update HTML templates | Dev | 🔴 Phase 2 |
| Test metrics end-to-end | QA | 🔴 Phase 2 |

### Phase 3: Gate Validation (Semana 5–6)

| Task | Owner | Status |
|------|-------|--------|
| Add compression check to gates | Dev | 🔴 Phase 3 |
| Test gate pass/fail scenarios | QA | 🔴 Phase 3 |
| Update playbooks | Docs | 🔴 Phase 3 |

---

## 💾 Files Affected

| File | Change | Type |
|------|--------|------|
| `token_metrics_collector.py` | Add compression fields | Minor |
| `dashboard_server.py` | Add widget + HTML | Minor |
| `migration-coordinator.py` | Integrate CCR handoff | Major |
| `validate_gate{N}_artifacts.py` | Add compression check | Minor |
| `TOKEN-METRICS-GUIDE.md` | Update docs | Docs |

---

## ✅ Compliance

- ✅ **Token tracking:** Mantém `token_metrics_collector.py` + estende
- ✅ **Stack:** Headroom + Azure OpenAI (Microsoft-only)
- ✅ **Reversibility:** CCR system = dados nunca perdidos
- ✅ **Governance:** Metrics logged, auditable

---

## 🎯 Expected Outcome

**Today (without Headroom):**
- 344K tokens/phase
- $0.51 USD cost
- Sem otimização

**After Phase 1 (with Headroom):**
- 48K tokens/phase (86% reduction)
- $0.07 USD cost (86% savings)
- Transparência em cada handoff
- Validação em cada gate

---

## 📚 References

| Resource | Link | Purpose |
|----------|------|---------|
| Token Metrics (existing) | `token-metrics-implementation-status.md` | Current state |
| Headroom Strategy | `reports/HEADROOM-INTEGRATION-STRATEGY.md` | Full blueprint |
| PoC Quick Start | `reports/HEADROOM-POC-QUICK-START.md` | How to test |
| Decision Template | `reports/HEADROOM-POC-DECISION-TEMPLATE.md` | How to decide |

---

**Created:** 2026-06-15  
**Status:** 🟡 Design phase (awaiting PoC decision)  
**Next:** Start PoC → validate compression → GO/NO-GO decision
