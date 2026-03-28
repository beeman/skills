---
name: gh-pr-create
description: Create a GitHub pull request from local repo changes. Use when Codex must get feature-branch setup or local commit preparation from `gh-commit`, get approval before pushing, show the exact PR title and body that will be sent, get explicit confirmation before opening the PR on GitHub, push the feature branch, and open or update the PR with gh.
---

# Create PR

Use this skill when the user wants the current work packaged into a reviewable GitHub pull request. This skill requires access to `gh-commit` for branch and commit preparation before it takes the work through push and PR creation.

## Boundary Rules

- This skill packages already-decided work for review. It does not challenge or redesign the implementation plan.
- This skill requires `gh-commit` for branch, changeset, and commit rules.
- If you can locate [`../gh-commit/SKILL.md`](../gh-commit/SKILL.md) or another installed `gh-commit` skill, read and follow it whenever the current branch is not the intended feature branch or the local commit state is missing or stale.
- If you cannot locate `gh-commit`, stop and ask the user what to do before creating or updating a PR. Ask specifically which branch to use and which commit or amend flow the PR should be created from.
- If the user wants a deep critique of the branch approach, implementation plan, or test strategy before mutating git state, use `gh-plan-review`.

## Core Workflow

1. Treat `gh-commit` as a required dependency before any push or PR work. If you can locate [`../gh-commit/SKILL.md`](../gh-commit/SKILL.md) or another installed `gh-commit` skill, read and follow it whenever the current branch is not already the intended feature branch or the local commit state is missing or stale. If you cannot locate `gh-commit`, stop and ask the user what to do, including which branch to use and which commit or amend flow the PR should be created from.
2. Follow the repo and user push policy. If explicit user approval is required before pushing, stop and get it.
3. When creating a new PR, resolve the intended PR base first. Honor an explicit user-specified base when present, otherwise honor `branch.<name>.gh-merge-base` when configured, and only then fall back to the repository default branch. Check how many commits the branch has relative to that resolved base. A multi-commit new-PR branch should be treated as unexpected and must trigger an explicit user prompt before continuing.
4. After resolving the PR base and determining whether the PR will use the single-commit `--fill` path or the multi-commit explicit `--title` and `--body` path, show the exact PR title and body you plan to send and get explicit user confirmation before any `gh pr create` call. On a single-commit `--fill` path, that should match the commit title and body prepared through `gh-commit`, and if the user wants changes you should route back through [`../gh-commit/SKILL.md`](../gh-commit/SKILL.md) to amend the commit first. On a multi-commit fallback, preview the explicit `--title` and `--body` text instead.
5. Push the feature branch to GitHub.
6. If the branch has exactly one commit and the approved PR text matches that commit, create the PR with `gh pr create --fill`. If the branch has multiple commits and the user explicitly wants to continue without first collapsing it to one commit, create the PR with explicit `--title` and `--body` values that describe the full branch diff against the resolved PR base instead of `--fill`. Preserve any applicable issue trailer from the local commit when it still accurately describes the full PR diff. If you need to set or repair the PR body manually, pass actual multiline text, not literal `\n` escape sequences.
7. Report the branch name, commit SHA, changeset status, and PR URL.

## Push and PR Rules

GitHub CLI commands that require network access should be run outside the sandbox immediately, using approved `gh` prefix rules when available, instead of trying them in-sandbox first.

- Treat the current branch, local diff, and existing open PR state as authoritative when deciding whether to create a new PR or update an existing one.
- If the branch already has an open PR, treat that PR's current base as authoritative unless the user explicitly wants to retarget it. Only resolve a local PR base the same way `gh pr create` does when creating a new PR: explicit user-provided base first, then `branch.<name>.gh-merge-base` when configured, then the repository default branch.
- Never push without explicit user approval when repo or user policy requires approval.
- Push only the feature branch you are preparing for review.
- Resolve the PR base and determine the actual PR creation path before previewing the exact PR title and body for approval.
- Before any `gh pr create` call, show the exact PR title and body that will be sent to the user and stop for explicit confirmation.
- Treat more than one branch commit as an unexpected state only when creating a new PR. If the branch already has an open PR, update it instead of reprompting just because the branch has multiple commits.
- PR title and body must describe the tracked PR diff against the base branch only. On a single-commit branch, that should match the approved commit title and body prepared through `gh-commit`. On a multi-commit fallback, it must describe the full branch diff against the base branch rather than just the last staged diff.
- Use `gh pr create --fill` only when the branch has exactly one commit and the approved PR title and body match that commit.
- If the branch has multiple commits and the user explicitly wants to proceed anyway, pass explicit `--title` and `--body` values that describe the full branch diff against the resolved base branch instead of relying on `--fill`.
- When you synthesize an explicit PR body, preserve any applicable `Closes #xx`, `Fixes #xx`, or `Part of #xx` trailer when it still accurately describes the full PR diff.
- If you provide or edit a PR body explicitly, use actual multiline text such as `--body-file` or shell quoting that produces real line breaks, not escaped `\n` sequences.
- If the branch already has an open PR, update that PR instead of creating a duplicate.
- If the push or PR step is blocked, stop and report the blocker clearly.
