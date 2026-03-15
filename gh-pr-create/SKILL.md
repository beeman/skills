---
name: gh-pr-create
description: Create a GitHub pull request from local repo changes. Use when Codex needs to move work onto a feature branch immediately if needed, confirm the current branch before every commit, write a style-matching commit with a body, add a changeset when the repo uses Changesets, get approval before pushing, push the branch, and open the PR with gh.
---

# Create PR

Use this skill when the user wants the current work packaged into a reviewable GitHub pull request. Start by getting onto the correct feature branch before other work, keep the commit history clean, and take the change all the way through push and PR creation.

## Core Workflow

1. If you are not already on the intended feature branch, create it immediately before doing other work. Do not continue on `main`, `master`, or another default branch.
2. Name the branch `<username>/<descriptive-name>`. Do not use `feature/`, `feat/`, or `fix/`. Use the system username when it is clear; otherwise fall back to the agent name.
3. Complete the requested work and run the smallest relevant verification for the touched files before committing.
4. Run `git branch --show-current` immediately before every commit, even if you already checked it earlier in the task.
5. Write a commit message that matches the repository history and include a body. When the local style is unclear, use a conventional commit.
6. If the work closes an issue completely, include `Closes #xx` or `Fixes #xx` in the commit body. If the work is partial, include `Part of #xx`.
7. If the repo uses Changesets, add the smallest accurate changeset before pushing.
8. Follow the repo and user push policy. If explicit user approval is required before pushing, stop and get it.
9. Push the feature branch to GitHub.
10. Create the PR with `gh pr create --fill` when the commit title and body are already clean. If you need to set or repair the PR body manually, pass actual multiline text, not literal `\n` escape sequences.
11. Report the branch name, commit SHA, changeset status, and PR URL.

## Branch Rules

- Create the branch as the first operational step when you are not already on the correct feature branch.
- Keep using the same feature branch unless the user explicitly redirects you.
- Never commit directly on `main`, `master`, or another default branch.
- When the user explicitly provides a branch name, use it if it still fits repo policy.

## Commit Rules

- Always run `git branch --show-current` before each commit.
- Keep the commit body informative and non-empty.
- Use real newlines in multi-paragraph commit bodies. Prefer repeated `git commit -m` flags, an editor, or a file; never embed literal `\n` sequences and expect Git or GitHub to render them.
- Match existing commit style from nearby history before defaulting to conventional commits.

## Changeset Rules

- Add a changeset only when the repo is actually configured for Changesets.
- Treat `.changeset/` or equivalent repo conventions as evidence that Changesets is in use.
- Keep the changeset scoped to the user-visible change. Do not invent package impacts.

## Push and PR Rules

GitHub CLI commands that require network access should be run outside the sandbox immediately, using approved `gh` prefix rules when available, instead of trying them in-sandbox first.

- Never push without explicit user approval when repo or user policy requires approval.
- Push only the feature branch you are preparing for review.
- Use `gh pr create --fill` so the PR title and body inherit from the commit when that matches the repo workflow.
- If you provide or edit a PR body explicitly, use actual multiline text such as `--body-file` or shell quoting that produces real line breaks, not escaped `\n` sequences.
- If the branch already has an open PR, update that PR instead of creating a duplicate.
- If the push or PR step is blocked, stop and report the blocker clearly.
