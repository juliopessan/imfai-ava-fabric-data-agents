# 🤝 Branch trabalho-backlog — Colaboração Compartilhada

**Data:** 2026-06-26 | **Status:** ✅ Pronto para Colaboração  
**Branch:** `trabalho-backlog` | **Remotes:** GitHub + Azure DevOps

---

## 🎯 Propósito

Branch isolada para trabalhos conjuntos via SSH remote, mantendo DEV limpa para produção.

```
main (production)
  ↓
Dev (staging)
  ↓
trabalho-backlog (collaborative work, SSH shared)
```

---

## 🔌 Remotes Configurados

### GitHub (via SSH — quando disponível)
```bash
# Adicionar SSH remote (execute quando SSH configurado)
git remote add ssh-github git@github.com:juliopessan/imfai-ava-fabric-data-agents.git

# Configurar para usar SSH em push
git config remote.ssh-github.push ssh-github

# Pull / fetch
git fetch ssh-github trabalho-backlog
git pull ssh-github trabalho-backlog
```

### Azure DevOps (via SSH — quando disponível)
```bash
# SSH URL format para Azure DevOps
git remote add ssh-azure git@ssh.dev.azure.com:v3/IMFAI/imfai-ava-fabric-data-agents/imfai-ava-fabric-data-agents

# Configure para usar SSH
git config remote.ssh-azure.push ssh-azure
```

### Current Remotes (HTTPS)
```bash
# GitHub (HTTPS)
git remote -v | grep github
# Output: github https://github.com/juliopessan/imfai-ava-fabric-data-agents.git

# Azure DevOps (HTTPS)
git remote -v | grep origin
# Output: origin https://IMFAI@dev.azure.com/IMFAI/imfai-ava-fabric-data-agents/_git/...
```

---

## 📦 Estrutura de Backlog

```
trabalho-backlog/
├── .backlog/                           # Coordenação compartilhada
│   ├── ASSIGNMENTS.md                  # Quem trabalha no quê
│   ├── MILESTONES.md                   # Entrega colaborativa
│   ├── SYNC-PROTOCOL.md                # Como sincronizar
│   └── MERGE-CHECKLIST.md              # Validação antes merge
│
├── features/
│   └── [nome-feature]/                 # Trabalhos em progresso
│       ├── code/
│       ├── tests/
│       ├── docs/
│       └── STATUS.md
│
├── experiments/
│   └── [nome-experimento]/             # Testes e protótipos
│       └── STATUS.md
│
└── shared/
    ├── SHARED-UTILITIES.md             # Código reutilizável
    └── COORDINATION.md                 # Notas técnicas compartilhadas
```

---

## 📋 Fluxo de Trabalho Colaborativo

### 1️⃣ Começar Nova Feature

```bash
# Atualizar local
git fetch ssh-github trabalho-backlog  # Ou: git fetch github trabalho-backlog
git pull ssh-github trabalho-backlog

# Criar feature branch (local)
git checkout -b feature/sua-feature trabalho-backlog

# Trabalhar
# ... commits ...

# Publicar para backlog compartilhado
git push ssh-github feature/sua-feature
# Ou: git push github feature/sua-feature
```

### 2️⃣ Sincronizar com Colegas

**Antes de começar:**
```bash
git fetch ssh-github trabalho-backlog
git rebase ssh-github/trabalho-backlog
```

**Após completar:**
```bash
# 1. Validar commits
git log --oneline origin/trabalho-backlog..HEAD

# 2. Push para backlog compartilhado
git push ssh-github trabalho-backlog

# 3. Atualizar .backlog/ASSIGNMENTS.md
# (marcar como completo)

# 4. Abrir pull request para code review
# No GitHub ou Azure DevOps
```

### 3️⃣ Code Review (Peer)

```bash
# Colegas fazem pull
git fetch ssh-github feature/sua-feature
git checkout feature/sua-feature

# Review local + teste
# ... feedback ...

# Merge em trabalho-backlog (maintainer)
git checkout trabalho-backlog
git merge --no-ff feature/sua-feature
git push ssh-github trabalho-backlog

# Delete feature branch
git push ssh-github --delete feature/sua-feature
```

---

## 🔐 SSH Setup (Quando Disponível)

### Step 1: Gerar SSH Key (se não existir)

```bash
ssh-keygen -t rsa -b 4096 -f $env:USERPROFILE\.ssh\id_rsa -N ""
```

### Step 2: Adicionar Key ao GitHub

```bash
# Copy SSH public key
cat $env:USERPROFILE\.ssh\id_rsa.pub | clip

# Ir para: https://github.com/settings/keys
# Click "New SSH key"
# Paste e salvar
```

### Step 3: Adicionar Key ao Azure DevOps

```bash
# Azure DevOps: User Settings → SSH public keys
# Paste mesma chave

# Ou via CLI
az devops configure --use-pat
```

### Step 4: Testar SSH Connection

```bash
# GitHub
ssh -T git@github.com
# Expected: "Hi juliopessan! You've successfully authenticated..."

# Azure DevOps
ssh -T git@ssh.dev.azure.com
# Expected: "Hello! You are now authenticated."
```

### Step 5: Configurar Git para Usar SSH

```bash
# Configure credential helper para SSH
git config --global core.sshCommand "ssh"

# Verify
git config --global --list | findstr "sshCommand"
```

---

## 📍 Assignments (Trabalho Distribuído)

| Trabalho | Assignee | Status | Branch | Deadline |
|----------|----------|--------|--------|----------|
| Feature A | pessoa1 | 🔄 In Progress | `feature/a` | 2026-06-29 |
| Feature B | pessoa2 | ⏳ Waiting review | `feature/b` | 2026-06-28 |
| Experiment C | pessoa3 | 📋 Planning | `exp/c` | 2026-07-05 |
| Utility X | pessoa1,pessoa2 | ⏳ Waiting | `feature/util-x` | 2026-06-30 |

**Updatear este arquivo:**
```bash
git checkout trabalho-backlog
# Edit .backlog/ASSIGNMENTS.md
git add .backlog/ASSIGNMENTS.md
git commit -m "chore: update assignments"
git push ssh-github trabalho-backlog
```

---

## ✅ Checklist Pre-Merge

Antes de fazer merge em `trabalho-backlog`:

- [ ] Todos os commits têm messages claras
- [ ] Código segue conventions do projeto
- [ ] Tests passam localmente
- [ ] Documentation atualizada
- [ ] Não há conflitos com `trabalho-backlog`
- [ ] Code review aprovado por (2 pessoas min)
- [ ] ASSIGNMENTS.md atualizado
- [ ] STATUS.md da feature atualizado

---

## 📞 Sync Protocol

### Diária

```
09:00 — Sync standup via chat
├─ O que fiz ontem?
├─ O que vou fazer hoje?
└─ Bloqueadores?

Push changes para ssh-github/trabalho-backlog
```

### Per Feature

```
Quando terminar trabalho:
1. Validar contra checklist (acima)
2. Abrir PR (pull request)
3. Tag reviewers: @pessoa1 @pessoa2
4. Merge após 2 aprovações
5. Delete feature branch
6. Update ASSIGNMENTS.md
```

### Merge para DEV (Promotion)

```
Semanal (ou quando feature completa):
1. Sync com Dev branch
2. Run full test suite
3. Code review by lead
4. Merge para Dev
5. Deploy para staging (opcional)
```

---

## 🛠️ Utilities Compartilhadas

Local: `.backlog/shared/`

### Adicionar Utility

```bash
# 1. Create in shared/
# .backlog/shared/my-utility.py

# 2. Document in SHARED-UTILITIES.md
# Name, usage, dependencies

# 3. Commit
git add .backlog/shared/
git commit -m "feat: add shared utility - my-utility"

# 4. Push
git push ssh-github trabalho-backlog
```

### Usar Utility

```python
import sys
sys.path.insert(0, '.backlog/shared')

from my_utility import my_function

result = my_function(...)
```

---

## 📊 Monitoramento de Progresso

### Status por Feature

Arquivo: `.backlog/[feature-name]/STATUS.md`

```markdown
# Feature: Name

**Owner:** @pessoa
**Started:** 2026-06-26
**ETA:** 2026-06-30

## Progress
- [x] Fase 1: Design (Done 6/26)
- [ ] Fase 2: Implementation (In progress)
- [ ] Fase 3: Testing (Queued)
- [ ] Fase 4: Review (Queued)

## Metrics
- Lines of code: 450
- Tests added: 12
- Docs: README.md
- Status: 🟡 On track

## Known Issues
- Issue A: [description] (Minor)
- Issue B: [description] (Blocker)
```

---

## 🚀 Workflow Rápido (Copy-Paste)

```bash
# === SETUP (primeira vez) ===
git checkout trabalho-backlog
git fetch ssh-github trabalho-backlog

# === COMEÇAR FEATURE ===
git pull ssh-github trabalho-backlog
git checkout -b feature/minha-feature

# === TRABALHAR ===
# ... edita arquivos ...
git add .
git commit -m "feat: description"

# === PUBLICAR ===
git push ssh-github feature/minha-feature

# === CRIAR PR ===
# No GitHub: https://github.com/juliopessan/imfai-ava-fabric-data-agents
# Click "New pull request"
# Base: trabalho-backlog
# Compare: feature/minha-feature

# === MERGE (after review) ===
git checkout trabalho-backlog
git pull ssh-github trabalho-backlog
git merge --no-ff feature/minha-feature
git push ssh-github trabalho-backlog
git push ssh-github --delete feature/minha-feature

# === CLEANUP ===
git branch -d feature/minha-feature
```

---

## 📚 Documentação Relacionada

| Doc | Propósito | Local |
|-----|----------|-------|
| **ASSIGNMENTS.md** | Quem trabalha no quê | `.backlog/` |
| **STATUS.md** (per feature) | Progresso individual | `features/[name]/` |
| **SYNC-PROTOCOL.md** | Sincronização | `.backlog/` |
| **SHARED-UTILITIES.md** | Código reutilizável | `.backlog/shared/` |

---

## ⚠️ Regras de Ouro

✅ **Sempre:**
- Pull antes de começar trabalho
- Commit com messages claras
- Push diariamente (pelo menos)
- Update STATUS.md regularmente

❌ **Nunca:**
- Force push em trabalho-backlog
- Commit diretamente em DEV
- Merge sem code review
- Deixar branches obsoletas

---

## 🔄 Troubleshooting

### Conflito ao Merge

```bash
# 1. Resolver conflito
# (edit file, git add)

# 2. Completar merge
git commit -m "merge: resolve conflicts"
git push ssh-github trabalho-backlog
```

### Branch desatualizada

```bash
# 1. Fetch
git fetch ssh-github trabalho-backlog

# 2. Rebase (ou merge)
git rebase ssh-github/trabalho-backlog

# 3. Force push (se necessário, use com cuidado)
git push ssh-github --force-with-lease
```

### SSH não conecta

```bash
# 1. Verificar SSH key
ssh -T git@github.com

# 2. Se falhar, adicionar key
ssh-add ~/.ssh/id_rsa

# 3. Retry
ssh -T git@github.com
```

---

## 📞 Support

**Questions?** 
- Check ASSIGNMENTS.md (quem sabe mais)
- Review SYNC-PROTOCOL.md
- Read .backlog/COORDINATION.md

---

**Status:** ✅ Ready for Collaborative Work  
**SSH Configuration:** 📋 Waiting for key setup  
**First Sync:** Ready to execute  

```bash
# Ready? Execute:
git checkout trabalho-backlog
git fetch ssh-github trabalho-backlog  # (will work once SSH configured)
```
