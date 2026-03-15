---
name: gh-pr-rebase
description: Rebase an existing GitHub PR branch onto the repository default branch. Use when Codex needs to fetch the latest default-branch history, keep the local default branch current when that is safe, rebase the current feature branch, resolve straightforward conflicts carefully, ask the user to decide ambiguous conflicts, and update the remote PR branch with `git push --force-with-lease` after any required approval.
---

# Rebase PR Branch

## Overview

Use this skill when the user wants the current PR branch refreshed on top of the latest default-branch history instead of merged. Keep the existing feature branch safe, keep the local default branch current when that can be done without rewriting local-only work, and escalate only the conflicts that need human judgment.

## Core Workflow

1. Confirm you are on the feature branch that should be rebased, not `main`, `master`, or another default branch, and not a detached `HEAD`. If you are on the wrong branch, switch to the intended PR branch or ask instead of rebasing from the wrong starting point.
2. Inspect repository state before starting. If a rebase is already in progress, continue or abort that rebase deliberately instead of starting a second history-rewrite operation on top of it.
3. Record the starting branch name and `HEAD` SHA before changing history so recovery is straightforward if the rebase must be aborted.
4. Check `git status --short`. If the worktree or index is dirty, do not start the rebase blindly. Ask whether to commit, stash, use `--autostash`, or stop.
5. Determine the repository default branch from `refs/remotes/origin/HEAD` when available. If it is unclear or stale, use `gh repo view --json defaultBranchRef` or equivalent repo metadata.
6. Fetch the latest remote state for the default branch and prune stale refs before rebasing.
7. Keep the local default branch current when safe so switching back shows the latest changes:
   - If `<default>` does not exist locally, create it to track `origin/<default>` when that is safe.
   - If `<default>` exists and can be fast-forwarded to `origin/<default>`, update it.
   - If local `<default>` has local-only commits or would need a non-fast-forward rewrite, stop and ask instead of rewriting it silently.
8. Rebase the current feature branch onto `origin/<default>` unless repo context or existing branch history clearly requires `git rebase --rebase-merges`.
9. Resolve conflicts commit-by-commit. Preserve both intended changes when they are compatible; ask the user when the conflict changes behavior or the winner is not obvious.
10. If a rebased commit becomes empty because its change already exists upstream, confirm that explanation fits the diff before using `git rebase --skip`.
11. Run the smallest relevant verification for files touched by conflict resolution or rebase fallout.
12. Confirm the branch is in a clean post-rebase state and compare it with its upstream remote branch.
13. If history changed and push policy allows it, update the remote branch with `git push --force-with-lease`. If the repo or user policy requires approval before pushing, stop and get it first.
14. Report the branch name, resulting `HEAD` SHA, what changed, any conflicts that needed human judgment, and whether the remote branch was updated.

## Branch Rules

- Work on the existing PR feature branch unless the user explicitly redirects you.
- Never run the rebase pass on `main`, `master`, or another default branch.
- If the user explicitly names the branch to rebase, use it if it still fits repo policy.
- Do not create a new branch for routine rebase maintenance unless the user asks for a separate branch.

## Default Branch Rules

- Prefer the repo's actual default branch over hard-coding `main`.
- Use the remote-tracking default branch as the authoritative rebase base, even if you also update the local default branch for convenience.
- Do not silently rewrite or reset the local default branch if it has unique local commits.
- If the default branch cannot be identified confidently, ask rather than guessing.

## Conflict Resolution Rules

- Do not use blanket `-X ours`, `-X theirs`, or file-wide checkout strategies unless the conflict is genuinely mechanical and you have inspected the hunk.
- Treat formatting-only, lockfile, or import-order conflicts as routine; resolve them locally and continue.
- Treat behavioral conflicts, deleted-vs-modified conflicts, schema changes, API contract changes, and test expectation changes as potentially ambiguous until you inspect intent.
- Ask the user when the conflict reflects contradictory behavior, unclear ownership, or two valid but incompatible outcomes.
- When asking, name the file, the conflicting intent, and the smallest decision needed.
- If the rebase becomes unsafe or the chosen resolution is still uncertain, use `git rebase --abort` instead of improvising.

## Push Rules

GitHub CLI commands that require network access should be run outside the sandbox immediately, using approved `gh` prefix rules when available, instead of trying them in-sandbox first.

- Push only the rebased feature branch, never the default branch.
- Use `git push --force-with-lease`, not plain `--force`.
- Respect repo and user approval policy before any push.
- Keep the existing review branch intact; use the rebase to refresh it rather than creating a replacement PR branch.
- If the branch has no upstream or the upstream remote is not the expected PR remote, confirm the target before pushing.
- If the rebase made no history change or the remote already matches the local branch, skip the force-push and report that nothing needed updating.

## Output Format

After finishing the rebase pass, present the result in this order:

1. `Rebase Summary`
2. `Conflict Decisions`
3. `Verification`
4. `Remote Update`
5. `Next Step`

Include the current branch name and resulting `HEAD` SHA in `Rebase Summary`.

Then emit exactly one status line in this format:

```text
status | default branch | conflicts handled (n) | push (done/skipped/blocked)
```

Use these values consistently:

- `status`: `done`, `partial`, `blocked`, or `no-change`
- `default branch`: detected default branch name
- `conflicts handled (n)`: number of conflict stops resolved during this pass
- `push`: `done` only when the rewritten branch was pushed, `skipped` when no push was needed, and `blocked` when a push was required but could not be completed
