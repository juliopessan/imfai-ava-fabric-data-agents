# 📸 Playwright Visual Documentation — Setup Guide

## 🎯 Objetivo

Automatizar a captura de screenshots de estágios da migração para gerar documentação técnica visual **Before & After** com Playwright.

---

## 📋 Pré-requisitos

- **Python 3.8+** (já instalado)
- **VS Code** (já em uso)
- **Playwright** (será instalado)

---

## 🚀 Setup Inicial

### 1️⃣ Instalar Playwright

```bash
# Ativar virtual environment
.\.venv\Scripts\Activate.ps1

# Instalar Playwright
pip install playwright

# Instalar navegadores
playwright install chromium
```

### 2️⃣ Verificar Instalação

```bash
python -c "import playwright; print(f'Playwright v{playwright.__version__} OK')"
```

Saída esperada:
```
Playwright v1.40.0 OK
```

---

## 📖 Uso Rápido

### Capturar Screenshots de um Estágio

```bash
# Capturar etapa Upstream (Discovery)
python reports/_templates/playwright_screenshot_generator.py --project clientebanco --stage upstream

# Capturar etapa Midstream (Design)
python reports/_templates/playwright_screenshot_generator.py --project clientebanco --stage midstream

# Capturar etapa Downstream (Execution)
python reports/_templates/playwright_screenshot_generator.py --project clientebanco --stage downstream
```

---

## 📁 Estrutura de Saída

```
reports/screenshots/
├── clientebanco/
│   ├── metadata.json
│   ├── before_after_comparison.html
│   ├── upstream_executive_dashboard_estado_inicial.png
│   ├── upstream_roi_analysis_antes_da_migracao.png
│   ├── midstream_test_report_validacoes_em_progresso.png
│   └── downstream_3_tier_dashboard_estado_final.png
```

---

## 🎨 Recursos do HTML Gerado

### ✅ Recursos Implementados

1. **Header Consultoria** com branding
2. **Métricas resumidas** (total de etapas, screenshots, data)
3. **Galeria Before & After** com screenshots em alta qualidade
4. **Metadados** (data, hora, viewport, URL)
5. **Design Responsivo** (mobile, tablet, desktop)
6. **Comparação visual** de estágios
7. **Footers com informações de geração**

### 📊 Exemplo de Estrutura HTML

```html
<!-- Header com gradiente Consultoria -->
<div class="header">
    <h1>📊 Before & After — Visual Migration Documentation</h1>
</div>

<!-- Métricas -->
<div class="metrics">
    <div class="metric-card">
        <div class="metric-label">Total de Etapas</div>
        <div class="metric-value">3</div>
    </div>
</div>

<!-- Screenshots organizados por etapa -->
<div class="comparison-item">
    <div class="comparison-label after">📸 Label da Etapa</div>
    <div class="screenshot-container">
        <img src="screenshot.png" />
    </div>
</div>
```

---

## 🔧 VS Code Integration

### Option 1: Tasks.json

Adicionar ao `.vscode/tasks.json`:

```json
{
    "label": "Playwright: Capture Screenshots",
    "type": "shell",
    "command": "python",
    "args": [
        "reports/_templates/playwright_screenshot_generator.py",
        "--project", "clientebanco",
        "--stage", "upstream"
    ],
    "group": {
        "kind": "build",
        "isDefault": false
    },
    "presentation": {
        "reveal": "always",
        "panel": "new"
    }
}
```

### Option 2: VS Code Command

Executar no Terminal do VS Code:

```powershell
python reports/_templates/playwright_screenshot_generator.py --project clientebanco --stage upstream
```

---

## 📝 Customização

### Adicionar Novo Dashboard

Editar `playwright_screenshot_generator.py`:

```python
dashboards_to_capture = {
    "seu_projeto": {
        "upstream": [
            {
                "url": "file:///caminho/seu_dashboard.html",
                "stage": "upstream",
                "label": "Seu Dashboard - Descrição"
            }
        ]
    }
}
```

### Alterar Resolução de Screenshot

```python
page = await browser.new_page(viewport={"width": 2560, "height": 1440})  # 2K
```

---

## 🐛 Troubleshooting

### ❌ Erro: "playwright module not found"

```bash
pip install playwright
playwright install chromium
```

### ❌ Erro: "Chromium not found"

```bash
playwright install
```

### ❌ Erro: "Navigation timeout"

Aumentar timeout na captura:

```python
await page.goto(dashboard_url, wait_until="networkidle", timeout=30000)
```

---

## 📈 Casos de Uso

### 1️⃣ Documentação Comparativa
Comparar estado do sistema antes e depois da migração

### 2️⃣ Validação Visual
Verificar se transformações foram aplicadas corretamente

### 3️⃣ Relatórios para Stakeholders
Gerar evidência visual do progresso

### 4️⃣ Arquivo Histórico
Manter registro de cada etapa da migração

### 5️⃣ Treinamento
Usar screenshots como material educativo

---

## 🚀 Próximas Evoluções

- [ ] Diff automático entre screenshots (OpenCV)
- [ ] PDF export com comparações lado a lado
- [ ] Integração com Power BI / Analytics
- [ ] Versionamento de screenshots em Git
- [ ] API para recuperar screenshots programaticamente
- [ ] Notificações quando novos screenshots estão prontos

---

## 📞 Suporte

Para ajuda ou extensões:
1. Consultar documentação Playwright: https://playwright.dev
2. Verificar logs em `reports/screenshots/{project}/metadata.json`
3. Testar URL manualmente no navegador antes de capturar

---

**Generated by Consultoria Data Migration Factory v3**
