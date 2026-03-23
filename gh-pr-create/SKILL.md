---
name: gh-pr-create
description: Create a GitHub pull request from local repo changes. Use when Codex needs to move work onto a feature branch immediately if needed, confirm the current branch before every commit, write a style-matching commit with a body, add a changeset when the repo uses Changesets, get approval before pushing, show the exact PR title and body that will be sent, get explicit confirmation before opening the PR on GitHub, push the branch, and open the PR with gh.
---

# Create PR

Use this skill when the user wants the current work packaged into a reviewable GitHub pull request. Start by getting onto the correct feature branch before other work, keep the commit history clean, and take the change all the way through push and PR creation.

## Boundary Rules

- This skill packages already-decided work for review. It does not challenge or redesign the implementation plan.
- If the user wants a deep critique of the branch approach, implementation plan, or test strategy before mutating git state, use `gh-plan-review`.

## Core Workflow

1. If you are not already on the intended feature branch, create it immediately before doing other work. Do not continue on `main`, `master`, or another default branch.
2. Name the branch `<username>/<descriptive-name>`. Do not use `feature/`, `feat/`, or `fix/`. Use the system username when it is clear; otherwise fall back to the agent name.
3. Inspect `git status --short`, the current diff, and existing repo conventions before committing so the PR describes the actual work rather than a stale summary.
4. Complete the requested work and run the smallest relevant verification for the touched files before committing.
5. Run `git branch --show-current` immediately before every commit, even if you already checked it earlier in the task.
6. Write a commit message that matches the repository history, includes a body, and describes only the staged diff. Do not mention thread discussion, related ideas, or requested changes that are not present in the committed files. When the local style is unclear, use a conventional commit.
7. If the work closes an issue completely, include `Closes #xx` or `Fixes #xx` in the commit body. If the work is partial, include `Part of #xx`.
8. If the repo uses Changesets, add the smallest accurate changeset before pushing.
9. Follow the repo and user push policy. If explicit user approval is required before pushing, stop and get it.
10. When creating a new PR, resolve the intended PR base first. Honor an explicit user-specified base when present, otherwise honor `branch.<name>.gh-merge-base` when configured, and only then fall back to the repository default branch. Check how many commits the branch has relative to that resolved base. A multi-commit new-PR branch should be treated as unexpected and must trigger an explicit user prompt before continuing.
11. After resolving the PR base and determining whether the PR will use the single-commit `--fill` path or the multi-commit explicit `--title` and `--body` path, show the exact PR title and body you plan to send and get explicit user confirmation before any `gh pr create` call. On a single-commit `--fill` path, that should match the commit title and body, and if the user wants changes you should amend the commit first. On a multi-commit fallback, preview the explicit `--title` and `--body` text instead.
12. Push the feature branch to GitHub.
13. If the branch has exactly one commit and the approved PR text matches that commit, create the PR with `gh pr create --fill`. If the branch has multiple commits and the user explicitly wants to continue without first collapsing it to one commit, create the PR with explicit `--title` and `--body` values that describe the full branch diff against the resolved PR base instead of `--fill`. Preserve any applicable issue trailer from step 7 in that explicit PR body when it still accurately describes the full PR diff. If you need to set or repair the PR body manually, pass actual multiline text, not literal `\n` escape sequences.
14. Report the branch name, commit SHA, changeset status, and PR URL.

## Branch Rules

- Create the branch as the first operational step when you are not already on the correct feature branch.
- Keep using the same feature branch unless the user explicitly redirects you.
- Never commit directly on `main`, `master`, or another default branch.
- When the user explicitly provides a branch name, use it if it still fits repo policy.

## Commit Rules

- Always run `git branch --show-current` before each commit.
- Keep the commit body informative and non-empty.
- The commit title and body must describe the tracked staged diff only. Do not mention ignored files, local-only files, related discussion, rejected options, or future work unless those points are reflected in the committed files.
- Use real newlines in multi-paragraph commit bodies. Prefer repeated `git commit -m` flags, an editor, or a file; never embed literal `\n` sequences and expect Git or GitHub to render them.
- Match existing commit style from nearby history before defaulting to conventional commits.

## Ignored File Rules

- Let Git ignore rules stand by default.
- Never use `git add -f`, `git add --force`, or any other override to stage an ignored path unless the user explicitly instructs you to include that ignored file in version control.
- Never decide on your own that an ignored file should be committed because it seems useful or related.
- Never mention ignored or local-only files in commit or PR metadata unless the user explicitly wanted them included in version control and they are present in the tracked diff being described.

## Changeset Rules

- Add a changeset only when the repo is actually configured for Changesets.
- Treat `.changeset/` or equivalent repo conventions as evidence that Changesets is in use.
- Keep the changeset scoped to the user-visible change. Do not invent package impacts.

## Push and PR Rules

GitHub CLI commands that require network access should be run outside the sandbox immediately, using approved `gh` prefix rules when available, instead of trying them in-sandbox first.

- Treat the current branch, local diff, and existing open PR state as authoritative when deciding whether to create a new PR or update an existing one.
- If the branch already has an open PR, treat that PR's current base as authoritative unless the user explicitly wants to retarget it. Only resolve a local PR base the same way `gh pr create` does when creating a new PR: explicit user-provided base first, then `branch.<name>.gh-merge-base` when configured, then the repository default branch.
- Never push without explicit user approval when repo or user policy requires approval.
- Push only the feature branch you are preparing for review.
- Resolve the PR base and determine the actual PR creation path before previewing the exact PR title and body for approval.
- Before any `gh pr create` call, show the exact PR title and body that will be sent to the user and stop for explicit confirmation.
- Treat more than one branch commit as an unexpected state only when creating a new PR. If the branch already has an open PR, update it instead of reprompting just because the branch has multiple commits.
- PR title and body must describe the tracked PR diff against the base branch only. On a single-commit branch, that should match the approved commit title and body. On a multi-commit fallback, it must describe the full branch diff against the base branch rather than just the last staged diff.
- Use `gh pr create --fill` only when the branch has exactly one commit and the approved PR title and body match that commit.
- If the branch has multiple commits and the user explicitly wants to proceed anyway, pass explicit `--title` and `--body` values that describe the full branch diff against the resolved base branch instead of relying on `--fill`.
- When you synthesize an explicit PR body, preserve any applicable `Closes #xx`, `Fixes #xx`, or `Part of #xx` trailer when it still accurately describes the full PR diff.
- If you provide or edit a PR body explicitly, use actual multiline text such as `--body-file` or shell quoting that produces real line breaks, not escaped `\n` sequences.
- If the branch already has an open PR, update that PR instead of creating a duplicate.
- If the push or PR step is blocked, stop and report the blocker clearly.
