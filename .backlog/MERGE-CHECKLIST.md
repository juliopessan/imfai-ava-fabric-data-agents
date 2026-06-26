# ✅ Merge Checklist — Validação Pré-Merge

**Quando usar:** Antes de fazer merge em `trabalho-backlog`

---

## 📋 Pre-Merge Validation

### Code Quality
- [ ] All commits have descriptive messages (not "wip" or "fix")
- [ ] No debug code (console.log, breakpoints, TODO-XXXX)
- [ ] No hardcoded credentials, API keys, or secrets
- [ ] Code follows project style guide
- [ ] No unused imports or variables

### Testing
- [ ] Unit tests written (if applicable)
- [ ] Tests pass locally: `pytest` or `npm test`
- [ ] No skipped tests (@skip, @pending)
- [ ] Code coverage > 70% (or project minimum)

### Documentation
- [ ] README.md updated (if new feature)
- [ ] Docstrings added to public functions
- [ ] API docs updated (if applicable)
- [ ] Architecture diagram updated (if major change)

### Integration
- [ ] No merge conflicts with `trabalho-backlog`
- [ ] Branch rebased on latest `trabalho-backlog`
- [ ] Commits are not force-pushed after code review
- [ ] All dependencies resolved (no breaking changes)

### Git Hygiene
- [ ] Branch name follows convention (`feature/name` or `exp/name`)
- [ ] History is linear (no "Merge branch 'main' into..." commits)
- [ ] No accidental commits from other branches
- [ ] All commits attributed to correct author

### Approvals
- [ ] Code reviewed by 2+ team members
- [ ] All review comments resolved
- [ ] Reviewers explicitly approved (✅ LGTM or similar)
- [ ] No "needs work" or "request changes" remaining

---

## 🚀 Pre-Deployment (if applicable)

If merging to staging/production after `trabalho-backlog`:

- [ ] All tests pass in CI/CD pipeline
- [ ] No security vulnerabilities (linter passed)
- [ ] Performance benchmarks acceptable
- [ ] Database migrations (if any) tested
- [ ] Rollback plan documented

---

## 📊 Final Review Steps

1. **Visual diff:**
   ```bash
   git diff trabalho-backlog..feature/seu-nome --stat
   ```
   → Review file count and sizes

2. **Commit log:**
   ```bash
   git log trabalho-backlog..feature/seu-nome --oneline
   ```
   → Review commit messages

3. **Full diff (if small):**
   ```bash
   git diff trabalho-backlog..feature/seu-nome
   ```
   → Final visual inspection

4. **Merge locally:**
   ```bash
   git checkout trabalho-backlog
   git pull ssh-github trabalho-backlog
   git merge --no-ff feature/seu-nome
   ```
   → Verify no conflicts

5. **Push:**
   ```bash
   git push ssh-github trabalho-backlog
   ```

---

## ❌ Blocker Issues

Do NOT merge if:

- ❌ Tests failing
- ❌ Code has debug artifacts
- ❌ Unresolved conflicts
- ❌ Security vulnerabilities
- ❌ Missing code review
- ❌ Breaking changes undocumented
- ❌ Hard dependencies on unreleased code

---

## 🎯 Quick Copy-Paste

```bash
# Run full pre-merge validation

git checkout feature/seu-nome
git fetch ssh-github trabalho-backlog

# Check conflicts
git merge --no-commit --no-ff ssh-github/trabalho-backlog && git merge --abort

# Run tests
python -m pytest  # or your test command

# Check code style
pylint **/*.py  # or your linter

# Review commits
git log ssh-github/trabalho-backlog..HEAD --oneline

# If all pass:
echo "✅ Ready to merge"

# Merge
git checkout trabalho-backlog
git pull ssh-github trabalho-backlog
git merge --no-ff feature/seu-nome
git push ssh-github trabalho-backlog
```

---

**Maintainer:** Check all boxes before merge  
**Contributors:** Use this before requesting review  
**Questions?** See COORDINATION.md
