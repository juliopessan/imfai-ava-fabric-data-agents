# 🔄 Sync Protocol — Como Sincronizar

**Versão:** 1.0 | **Última atualização:** 2026-06-26

---

## 📅 Sync Diário (Standup)

### Timing
- **Hora:** 09:00 AM (seu timezone)
- **Canal:** #trabalho-backlog (Slack/Teams)
- **Duração:** 10 minutos
- **Participants:** Toda equipe no trabalho-backlog

### Formato

```
@channel — Daily Standup

[Pessoa 1]
✅ Ontem: [o que fez]
🎯 Hoje: [o que vai fazer]
🚧 Blockers: [nenhum | descrição]
Push: [sim/não] — [branch]

[Pessoa 2]
...
```

### Git Sync (Pós-standup)

```bash
# 1. Cada um publica seu trabalho
git push ssh-github feature/seu-nome

# 2. Maintainer sincroniza trabalho-backlog
git fetch ssh-github trabalho-backlog
git merge --no-ff feature/xxx (se pronto)
git push ssh-github trabalho-backlog

# 3. Todos atualizam local
git fetch ssh-github trabalho-backlog
git rebase ssh-github/trabalho-backlog  # ou merge
```

---

## 📞 Per-Feature Sync

### Before Starting

```bash
git fetch ssh-github trabalho-backlog
git pull ssh-github trabalho-backlog
```

### After Each Session (End of Day)

```bash
# 1. Commit local
git add .
git commit -m "wip: [description]"

# 2. Rebase on latest
git fetch ssh-github trabalho-backlog
git rebase ssh-github/trabalho-backlog

# 3. Push feature
git push ssh-github feature/seu-nome

# 4. Update STATUS.md
# → Edit .backlog/features/seu-nome/STATUS.md
# → git add, commit, push

# 5. Notify team (optional Slack message)
"Pushed updates to feature/seu-nome - [quick summary]"
```

---

## 🎯 Code Review Sync

### When Ready for Review

1. **Notifique no chat:**
   ```
   @reviewer1 @reviewer2 — Ready for review
   Branch: feature/seu-nome
   Summary: [1-2 sentences]
   Checklist: .backlog/MERGE-CHECKLIST.md
   ```

2. **Reviewers fazem:**
   ```bash
   git fetch ssh-github feature/seu-nome
   git checkout feature/seu-nome
   # Review local + test
   # Comment on GitHub PR or in chat
   ```

3. **After Approval:**
   - Maintainer merge em trabalho-backlog
   - Delete feature branch
   - Notifique team

---

## 🔁 Rebase vs Merge

### Rebase (Use when possible)

```bash
git fetch ssh-github trabalho-backlog
git rebase ssh-github/trabalho-backlog
git push ssh-github --force-with-lease
```

**Pros:** Linear history, clean  
**Cons:** Rewrites history (careful if shared)

### Merge (When unsure)

```bash
git fetch ssh-github trabalho-backlog
git merge ssh-github/trabalho-backlog
git push ssh-github feature/seu-nome
```

**Pros:** Safe, preserves history  
**Cons:** Extra merge commits

---

## 📊 Sync Status Check

### Quick Status

```bash
# What's on work-backlog
git log ssh-github/trabalho-backlog --oneline -10

# What's on your feature
git log feature/seu-nome --oneline -5

# Diff against backlog
git diff trabalho-backlog..feature/seu-nome --stat
```

### Conflict Detection

```bash
# Before merge/rebase
git fetch ssh-github trabalho-backlog
git merge --no-commit --no-ff ssh-github/trabalho-backlog

# If conflict, abort and rebase
git merge --abort
git rebase ssh-github/trabalho-backlog
```

---

## 🔔 Notifications

### Team Updates (Slack Template)

```
:rocket: [Person] pushed to feature/xxx
✅ Done: [feature milestone]
🎯 Next: [what's coming]
```

### Blocker Alert

```
:warning: [Person] — BLOCKER in feature/xxx
Issue: [description]
Impact: [what's blocked]
Help needed: [@expert or @reviewer]
```

---

## ⏰ Weekly Promotion to DEV

### Friday Sync (Promotion Ready Features)

1. **Prepare:**
   ```bash
   git checkout trabalho-backlog
   git pull ssh-github trabalho-backlog
   git log Dev..trabalho-backlog --oneline
   ```

2. **QA Check:**
   - Run test suite
   - Validate per MERGE-CHECKLIST.md

3. **Merge to Dev:**
   ```bash
   git checkout Dev
   git pull origin Dev
   git merge --no-ff trabalho-backlog
   git push origin Dev
   ```

4. **Tag Release (if applicable):**
   ```bash
   git tag -a v0.1-alpha -m "Promotion from trabalho-backlog"
   git push origin v0.1-alpha
   ```

---

## 🚨 Emergency Sync (If Push Required)

### Immediate Promote to Dev

```bash
# Only if critical fix needed

# 1. Feature is DONE + REVIEWED
# 2. Notify team in #critical-alert

git checkout Dev
git pull origin Dev
git merge --no-ff feature/critical-fix
git push origin Dev

# 3. Tag as hotfix
git tag -a hotfix-YYYYMMDD -m "Critical: [description]"
```

---

## 📝 Sync Checklist

Before pushing:
- [ ] All commits have clear messages
- [ ] No debug code / console.log
- [ ] Tests pass locally
- [ ] Code follows project conventions
- [ ] No conflicts with trabalho-backlog
- [ ] STATUS.md updated
- [ ] ASSIGNMENTS.md reflects current work

---

**Próxima revisão:** 2026-07-03  
**Feedback channel:** #trabalho-backlog-feedback
