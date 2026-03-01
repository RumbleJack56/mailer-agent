---
trigger: model_decision
description: Use when starting any new feature or fix, committing code, or merging work. Always read before touching git.
---

# Git Workflow

**Always create a branch before writing a single line of code.** No exceptions.

---

## Branch Strategy

```
main       ← production, only promoted from staging after user testing
staging    ← pre-production, promoted from dev at release points
dev        ← integration branch, all PRs merge here
  └── feature/short-description   ← your work
  └── fix/short-description
```

- `main` is what's live in production — never commit directly to it
- `staging` mirrors what's about to go live — no direct commits
- `dev` is where all work lands — always branch from here

---

## Starting Work (Do This First)

Before touching any code:
```bash
git checkout dev
git pull origin dev
git checkout -b feature/short-description
# now start coding
```

If it's a bug fix: `fix/short-description`
If it's a chore: `chore/short-description`

---

## Committing

```
feat: add user login
fix: return 404 when user not found
chore: upgrade dependencies
docs: update setup instructions
refactor: extract db session to dependency
```

- Subject ≤ 50 characters, imperative mood ("add" not "added")
- One logical change per commit — if you need "and", make two commits
- Never commit secrets, `.env` files, or debug code

---

## Merging (Pull Request)

1. Push branch: `git push origin feature/short-description`
2. Open PR against **`dev`** — never directly against staging or main
3. PR title matches commit format: `feat: add user login`
4. Description: what changed, why, how to test
5. Merge only when CI passes
6. Delete branch after merge

---

## Promotion Flow

**dev → staging** (release candidate)
```bash
git checkout staging
git pull origin staging
git merge dev
git push origin staging
```
Do this when a batch of features is ready for pre-production testing.

**staging → main** (production release)
```bash
git checkout main
git pull origin main
git merge staging
git push origin main
git tag v1.x.x   # tag every production release
```
Only after user testing on staging passes. Never skip staging.

---

## Quick Reference

| Situation | Command |
|---|---|
| Start new work | `git checkout dev && git pull && git checkout -b feature/name` |
| Save progress | `git add -p && git commit -m "feat: ..."` |
| Sync with dev | `git fetch origin && git rebase origin/dev` |
| Push branch | `git push origin feature/name` |
| Promote dev → staging | `git checkout staging && git merge dev && git push` |
| Promote staging → main | `git checkout main && git merge staging && git push && git tag v1.x.x` |
| Undo last commit (keep changes) | `git reset --soft HEAD~1` |