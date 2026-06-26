# Remote Configuration

Este repositório está configurado com **dois remotes** para sincronização:

## Remotes Configurados

### 🐙 GitHub (remote: `github`)
- **URL:** https://github.com/juliopessan/imfai-ava-fabric-data-agents.git
- **Branches:** Dev (default), main, feat/*, fix/*
- **Uso:** Desenvolvimento colaborativo e versionamento público/privado

### 🔵 Azure DevOps (remote: `origin`)
- **URL:** https://IMFAI@dev.azure.com/IMFAI/imfai-ava-fabric-data-agents/_git/imfai-ava-fabric-data-agents
- **Branches:** Dev (tracking), main, feat/*
- **Uso:** Integração com Azure Pipelines e DevOps workflows

---

## Comandos Úteis

### Push para ambos os remotes
```powershell
# Push para GitHub (padrão agora)
git push github Dev

# Push para Azure DevOps
git push origin Dev

# Push para ambos ao mesmo tempo
git push github Dev && git push origin Dev
```

### Verificar status dos remotes
```powershell
git remote -v
git branch -vv
```

### Alterar remote padrão
```powershell
# Definir GitHub como padrão para a branch atual
git branch --set-upstream-to=github/Dev Dev

# Voltar para Azure DevOps como padrão
git branch --set-upstream-to=origin/Dev Dev
```

---

## Branches Sincronizadas

| Branch | GitHub | Azure DevOps | Status |
|--------|--------|--------------|--------|
| **Dev** | ✅ Sincronizada | ✅ Sincronizada | Default branch |
| **main** | ✅ Sincronizada | ✅ Sincronizada | Production |
| **feat/standardize-folder-structure** | ✅ Sincronizada | ✅ Sincronizada | Feature |
| **fix/data-strategist-template-refs** | ✅ Sincronizada | ✅ Sincronizada | Bugfix |

---

## Sincronização Inicial Realizada

**Data:** 2026-06-23  
**Commits enviados:** 14 commits (2397 objects, 20.19 MiB)  
**Branch tracking:** Dev → github/Dev

### Sumário da Sincronização
- ✅ Remote GitHub adicionado como `github`
- ✅ Remote Azure DevOps mantido como `origin`
- ✅ Branch Dev sincronizada (com tracking)
- ✅ Branch main sincronizada
- ✅ Branches de features sincronizadas
- ✅ Commit final do Wave 4 Financeiro incluído

---

## Acesso ao Repositório

🔗 **GitHub:** [juliopessan/imfai-ava-fabric-data-agents](https://github.com/juliopessan/imfai-ava-fabric-data-agents)  
🔗 **Azure DevOps:** [IMFAI/imfai-ava-fabric-data-agents](https://dev.azure.com/IMFAI/imfai-ava-fabric-data-agents/_git/imfai-ava-fabric-data-agents)

---

## Workflow Recomendado

1. **Desenvolvimento local:** trabalhar na branch Dev ou features
2. **Commit:** `git commit -m "tipo(escopo): mensagem"`
3. **Push GitHub:** `git push github Dev` (padrão atual)
4. **Push Azure DevOps:** `git push origin Dev` (se necessário)
5. **Pull Request:** criar PRs no GitHub para review

---

**Configurado por:** GitHub Copilot  
**Última atualização:** 2026-06-23
