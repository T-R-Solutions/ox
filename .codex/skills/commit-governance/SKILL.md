---
name: commit-governance
description: Govern authorized ITAPIRACÓ commits in one Git root, including full-worktree frontend or backend commit requests.
---

# Commit Governance

## Format

Use Conventional Commits with a US English subject:

```text
<type>(<optional-scope>): <descrição concisa no imperativo>
```

Allowed types are `feat`, `fix`, `docs`, `refactor`, `test`, `perf`, `build`, `ci`, `chore`, and `revert`.

## Workflow

1. Confirm explicit authorization, exactly one Git root, and whether scope is task-local or repository-wide.
2. Re-run the repository top-level and status preflight; inspect staged, unstaged, deleted, conflicted, and untracked paths.
3. For task-local authorization, exclude unrelated work. For a repository-wide phrase defined below, treat the complete visible status of that repository as intentional scope.
4. Group the authorized state into one or more coherent Conventional Commits and run proportional validation.
5. Stage and commit each reviewed group. Repository-wide scope permits `git add -A` only from the verified selected root when it matches the intended group.
6. Verify every hash, subject, committed path, and the final residual status.
   Return these results to `$execution-loop` when operating in an existing change. Commit-only work reuses proportional checks and needs no invented product spec; full-worktree authorization still applies exactly as below.

## Rules

- Never combine backend and frontend in one commit.
- `faça os commits do frontend` authorizes every staged change, unstaged modification, deletion, and untracked path visible to `git status` in `itapiraco_frontend/`, including work from earlier tasks.
- `faça os commits do backend` grants the same complete-state authorization only in `itapiraco_backend/`.
- A repository-wide phrase authorizes multiple coherent commits, not a push, tag, release, amend, fixup, revert, merge, or rebase.
- Ignored paths are not part of “arquivos não versionados” unless the user explicitly authorizes forcing them into Git.
- Stop before committing unresolved conflicts, secrets, credentials, unsafe generated artifacts, or a path outside the selected Git root; report the exact blocker.
- Do not create tags, releases, pushes, amend, fixup, or revert by inference.
- Do not leave a reviewed visible change behind after a repository-wide request; if it cannot be committed safely, report it explicitly.
