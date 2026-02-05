# Licoes Aprendidas - Data Migration Project

> Documento vivo que registra erros encontrados, diagnostico e solucoes aplicadas durante o desenvolvimento do projeto.

**Ultima atualizacao:** 05/02/2026  
**Versao:** 1.0

---

## Indice de Problemas

| # | Problema | Categoria | Severidade |
|---|----------|-----------|------------|
| [1](#1-encoding-windows-cp1252---caracteres-unicode) | Encoding Windows cp1252 - Caracteres Unicode | PowerShell/Windows | Alta |
| [2](#2-databricks_host-sem-prefixo-https) | DATABRICKS_HOST sem prefixo https:// | Configuracao | Media |
| [3](#3-run-allps1-exigia-flags-obrigatorias) | run-all.ps1 exigia flags obrigatorias | Script | Media |
| [4](#4-caminho-incorreto-para-pasta-files) | Caminho incorreto para pasta Files | Script | Media |
| [5](#5-max_num_clusters--0-na-api-do-databricks) | max_num_clusters = 0 na API do Databricks | API Databricks | Alta |
| [6](#6-warehouse-criado-como-pro-em-vez-de-serverless) | Warehouse criado como PRO em vez de Serverless | API Databricks | Media |
| [7](#7-timeout-aguardando-warehouse-iniciar) | Timeout aguardando warehouse iniciar | Script | Baixa |

---

## Detalhamento dos Problemas

---

### 1. Encoding Windows cp1252 - Caracteres Unicode

**Categoria:** PowerShell/Windows  
**Severidade:** Alta  
**Data:** 05/02/2026

#### Descricao do Erro

Scripts PowerShell e Python falhavam com erros de encoding ao tentar exibir mensagens com caracteres especiais (acentos, emojis, simbolos Unicode).

```
UnicodeEncodeError: 'charmap' codec can't encode character '\u2714' in position 0: character maps to <undefined>
```

```
At line:X char:Y - The term '...' is not recognized
```

#### Como Identificamos

- Erros apareciam ao executar scripts com `Write-Host` contendo caracteres como `[OK]`, `[X]`, acentos (`configuracao`, `conexao`)
- Console do Windows usa cp1252 por padrao, que nao suporta caracteres Unicode estendidos
- Python tambem falhava ao tentar imprimir caracteres especiais no stdout

#### Analise da Causa Raiz

O Windows PowerShell usa encoding cp1252 (Windows-1252) por padrao no console. Este encoding suporta apenas 256 caracteres e nao inclui:
- Emojis e simbolos Unicode
- Caracteres especiais fora do conjunto Latin-1

Quando o script tentava exibir esses caracteres, o sistema nao conseguia mapea-los.

#### Solucao Aplicada

1. **Remover todos os caracteres Unicode** dos scripts PowerShell e Python
2. **Substituir acentos** por equivalentes ASCII:
   - `configuracao` → `configuracao` (sem cedilha visual, mas funcionando)
   - `conexao` → `conexao`
3. **Substituir simbolos** por texto ASCII:
   - `[OK]` em vez de checkmarks
   - `[X]` em vez de X vermelho
   - `[i]` em vez de icones de informacao

#### Codigo Antes/Depois

```powershell
# ANTES (falhava)
Write-Host "✓ Conexão estabelecida!" -ForegroundColor Green

# DEPOIS (funciona)
Write-Host "[OK] Conexao estabelecida!" -ForegroundColor Green
```

#### Alternativas Consideradas

| Alternativa | Pros | Contras | Decisao |
|-------------|------|---------|---------|
| Mudar encoding do console para UTF-8 | Manteria caracteres especiais | Requer configuracao do usuario | Rejeitada |
| Usar `[Console]::OutputEncoding` | Solucao programatica | Pode nao funcionar em todos os ambientes | Rejeitada |
| Remover caracteres especiais | Funciona em qualquer ambiente | Perde formatacao visual | **Aprovada** |
| Usar arquivos .ps1 salvos como UTF-8 BOM | Pode ajudar | Nao resolve problema do console | Rejeitada |

---

### 2. DATABRICKS_HOST sem prefixo https://

**Categoria:** Configuracao  
**Severidade:** Media  
**Data:** 05/02/2026

#### Descricao do Erro

Conexao com Databricks falhava mesmo com credenciais corretas.

```
Error connecting to Databricks: Invalid URL format
```

#### Como Identificamos

- Scripts de ingestao falhavam ao tentar conectar
- Ao inspecionar o arquivo `.env`, notamos que o host estava sem protocolo
- A biblioteca `databricks-sql-connector` exige URL completa

#### Analise da Causa Raiz

O valor do `DATABRICKS_HOST` no `.env` estava como:
```
DATABRICKS_HOST=adb-7405607395070159.19.azuredatabricks.net
```

Mas deveria incluir o protocolo:
```
DATABRICKS_HOST=https://adb-7405607395070159.19.azuredatabricks.net
```

#### Solucao Aplicada

Atualizado o arquivo `.env` para incluir `https://`:

```bash
DATABRICKS_HOST=https://adb-7405607395070159.19.azuredatabricks.net
```

#### Codigo Modificado

Adicionamos normalizacao no script para remover `https://` quando necessario para chamadas de API REST:

```powershell
$databricksHost = $env:DATABRICKS_HOST -replace "^https?://", ""
```

#### Alternativas Consideradas

| Alternativa | Pros | Contras | Decisao |
|-------------|------|---------|---------|
| Adicionar https:// no .env | Padrao correto | Precisa ajustar scripts de API | **Aprovada** |
| Remover https:// e adicionar nos scripts | Menos mudanca no .env | Inconsistente entre scripts | Rejeitada |
| Usar duas variaveis (HOST e URL) | Flexibilidade | Duplicacao, mais confuso | Rejeitada |

---

### 3. run-all.ps1 exigia flags obrigatorias

**Categoria:** Script  
**Severidade:** Media  
**Data:** 05/02/2026

#### Descricao do Erro

O script `run-all.ps1` falhava quando executado sem flags, tentando provisionar recursos Azure mesmo quando ja existiam.

```powershell
# Isso falhava
.\run-all.ps1

# Precisava rodar assim
.\run-all.ps1 -SkipProvisioning -SkipConfig
```

#### Como Identificamos

- Usuario reportou que precisava sempre passar flags
- Script tentava criar recursos Azure que ja existiam
- Erro: "Resource already exists"

#### Analise da Causa Raiz

O script nao tinha logica para:
1. Carregar automaticamente o `.env`
2. Detectar se credenciais ja existiam
3. Pular etapas de provisionamento automaticamente

#### Solucao Aplicada

Modificamos o `run-all.ps1` para:

1. **Carregar .env automaticamente** no inicio do script
2. **Auto-detectar credenciais** e pular provisioning se existirem
3. **Corrigir caminho da pasta Files**

```powershell
# Carregar .env automaticamente
$envPath = Join-Path $ScriptRoot "..\.env"
if (Test-Path $envPath) {
    Get-Content $envPath | ForEach-Object {
        if ($_ -match '^([^#=]+)=(.*)$') {
            $key = $matches[1].Trim()
            $value = $matches[2].Trim()
            [Environment]::SetEnvironmentVariable($key, $value, "Process")
        }
    }
}

# Auto-skip se credenciais existem
if ($env:DATABRICKS_HOST -and $env:DATABRICKS_TOKEN) {
    $SkipProvisioning = $true
    $SkipConfig = $true
}
```

#### Alternativas Consideradas

| Alternativa | Pros | Contras | Decisao |
|-------------|------|---------|---------|
| Auto-detectar e pular | UX mais simples | Menos controle explicito | **Aprovada** |
| Exigir flags sempre | Controle explicito | Ruim para UX | Rejeitada |
| Criar arquivo de estado | Rastreia execucoes anteriores | Complexidade adicional | Rejeitada |

---

### 4. Caminho incorreto para pasta Files

**Categoria:** Script  
**Severidade:** Media  
**Data:** 05/02/2026

#### Descricao do Erro

Scripts nao encontravam arquivos CSV para ingestao.

```
[X] Nenhum arquivo CSV encontrado em C:\...\Files
```

#### Como Identificamos

- Pasta Files existia e continha arquivos
- Caminho no script estava errado em relacao a localizacao do script

#### Analise da Causa Raiz

O script usava:
```powershell
$filesPath = Join-Path $ScriptRoot "..\..\Files"
```

Mas a estrutura real era:
```
azure-databricks-integration/
  05-orchestration/
    run-all.ps1       <- script aqui
  Files/              <- pasta aqui (um nivel acima, nao dois)
```

Deveria ser `"..\Files"` e nao `"..\..\Files"`.

#### Solucao Aplicada

Corrigido o caminho relativo:

```powershell
$filesPath = Join-Path $ScriptRoot "..\Files"
```

#### Alternativas Consideradas

| Alternativa | Pros | Contras | Decisao |
|-------------|------|---------|---------|
| Corrigir caminho relativo | Simples e direto | Depende da estrutura de pastas | **Aprovada** |
| Usar caminho absoluto | Independente de estrutura | Nao portavel | Rejeitada |
| Parametro para caminho | Flexibilidade | Adiciona complexidade | Considerada para futuro |

---

### 5. max_num_clusters = 0 na API do Databricks

**Categoria:** API Databricks  
**Severidade:** Alta  
**Data:** 05/02/2026

#### Descricao do Erro

Criacao de SQL Warehouse falhava com erro de validacao.

```json
{
  "error_code": "INVALID_PARAMETER_VALUE",
  "message": "0 is not a valid value for max_num_clusters. The value must be greater than or equal to 1, and less than or equal to 40."
}
```

#### Como Identificamos

- Erro retornado pela API REST do Databricks
- Mensagem clara indicando o parametro invalido

#### Analise da Causa Raiz

Na primeira tentativa de criar warehouse Serverless, removemos os parametros `min_num_clusters` e `max_num_clusters` pensando que nao seriam necessarios para Serverless.

Porem, a API do Databricks **sempre exige** esses parametros, mesmo para warehouses Serverless. Quando nao especificados, o valor padrao e 0, que e invalido.

#### Solucao Aplicada

Adicionamos os parametros obrigatorios na configuracao:

```powershell
$warehouseConfig = @{
    name = $WarehouseName
    cluster_size = $WarehouseSize
    min_num_clusters = 1      # Obrigatorio
    max_num_clusters = 1      # Obrigatorio
    auto_stop_mins = $AutoStopMinutes
    enable_serverless_compute = $true
    channel = @{ name = "CHANNEL_NAME_CURRENT" }
} | ConvertTo-Json -Depth 10
```

#### Alternativas Consideradas

| Alternativa | Pros | Contras | Decisao |
|-------------|------|---------|---------|
| Adicionar min/max = 1 | Funciona para todos os casos | Pode limitar scaling | **Aprovada** |
| Parametrizar min/max | Flexibilidade | Adiciona complexidade | Considerada para futuro |
| Usar valores maiores | Mais capacidade | Custo maior | Rejeitada |

---

### 6. Warehouse criado como PRO em vez de Serverless

**Categoria:** API Databricks  
**Severidade:** Media  
**Data:** 05/02/2026

#### Descricao do Erro

O warehouse estava sendo criado no modo PRO quando o usuario esperava Serverless.

#### Como Identificamos

- Usuario observou no portal Databricks que o warehouse nao era Serverless
- Revisao do codigo mostrou `warehouse_type = "PRO"` e `enable_serverless_compute = $false`

#### Analise da Causa Raiz

Configuracao inicial do script usava modo PRO:

```powershell
warehouse_type = "PRO"
enable_serverless_compute = $false
```

#### Solucao Aplicada

Alterado para modo Serverless:

```powershell
# Removido warehouse_type (nao aplicavel a serverless)
enable_serverless_compute = $true
```

**Nota:** Mesmo com `enable_serverless_compute = $true`, ainda precisamos de `min_num_clusters` e `max_num_clusters` (ver problema #5).

#### Alternativas Consideradas

| Alternativa | Pros | Contras | Decisao |
|-------------|------|---------|---------|
| Usar Serverless | Mais economico, inicio mais rapido | Requer workspace habilitado | **Aprovada** |
| Usar PRO | Mais controle | Custo, tempo de inicio | Rejeitada |
| Parametrizar escolha | Flexibilidade | Complexidade | Considerada para futuro |

---

### 7. Timeout aguardando warehouse iniciar

**Categoria:** Script  
**Severidade:** Baixa  
**Data:** 05/02/2026

#### Descricao do Erro

Script falhava ou continuava antes do warehouse estar pronto.

```
[X] Timeout aguardando warehouse. Continue manualmente.
```

No Databricks aparecia:
```
Cluster Start-up Delayed. Please wait while we continue to try and start the cluster.
```

#### Como Identificamos

- Script terminava mas warehouse ainda estava em STARTING
- Erros de DDL porque warehouse nao estava pronto
- Tempo de espera hardcoded (2-3 minutos) era insuficiente

#### Analise da Causa Raiz

O script tinha um timeout fixo:
```powershell
$maxWait = 180  # 3 minutos
```

Warehouses podem levar mais tempo para iniciar, especialmente:
- Primeira execucao
- Horarios de pico
- Workspaces novos

#### Solucao Aplicada

Removido o limite de tempo e aguardando indefinidamente:

```powershell
Write-Info "Aguardando warehouse iniciar (sem limite de tempo)..."
Write-Info "Pressione Ctrl+C para cancelar"

$waited = 0

do {
    Start-Sleep -Seconds 10
    $waited += 10
    
    $statusUrl = "https://$databricksHost/api/2.0/sql/warehouses/$($newWarehouse.id)"
    $status = Invoke-RestMethod -Uri $statusUrl -Headers $headers -Method Get
    
    $minutes = [math]::Floor($waited / 60)
    $seconds = $waited % 60
    Write-Host "  Status: $($status.state) (${minutes}m ${seconds}s)" -ForegroundColor Gray
    
} while ($status.state -ne "RUNNING")
```

**Melhorias:**
- Sem limite de tempo
- Mostra tempo decorrido em formato legivel (Xm Xs)
- Usuario pode cancelar com Ctrl+C

#### Alternativas Consideradas

| Alternativa | Pros | Contras | Decisao |
|-------------|------|---------|---------|
| Aguardar indefinidamente | Sempre funciona | Pode travar se houver problema | **Aprovada** |
| Aumentar timeout | Simples | Ainda pode nao ser suficiente | Rejeitada |
| Continuar em background | Nao bloqueia | Complexidade, pode falhar DDL | Rejeitada |
| Retry com backoff exponencial | Elegante | Complexo, ainda pode falhar | Considerada |

---

## Padroes e Recomendacoes

### Checklist para Novos Scripts

1. [ ] Usar apenas caracteres ASCII (sem acentos, emojis, Unicode)
2. [ ] Carregar `.env` automaticamente
3. [ ] Validar variaveis de ambiente obrigatorias
4. [ ] Usar caminhos relativos corretos
5. [ ] Aguardar recursos estarem prontos antes de usa-los
6. [ ] Tratar erros com mensagens claras
7. [ ] Permitir cancelamento com Ctrl+C

### Convencoes de Mensagens

```powershell
Write-Host "[OK] Sucesso" -ForegroundColor Green
Write-Host "[X] Erro" -ForegroundColor Red
Write-Host "[i] Informacao" -ForegroundColor Gray
Write-Host "> Executando acao..." -ForegroundColor Yellow
```

---

## Historico de Atualizacoes

| Data | Versao | Descricao |
|------|--------|-----------|
| 05/02/2026 | 1.0 | Criacao inicial com 7 problemas documentados |

---

*Este documento deve ser atualizado sempre que novos problemas forem encontrados e resolvidos.*
