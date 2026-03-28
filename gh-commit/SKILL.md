---
name: gh-commit
description: Prepare or amend a local Git commit from repo changes. Use when Codex needs to get onto the correct feature branch if needed, inspect `git status --short` and the current diff, run the smallest relevant verification, add any required changeset, write a style-matching commit with a body, refresh stale commit metadata with `git commit --amend`, and stop before any push or PR step.
---

# Commit Changes

Use this skill when the user wants the current local work packaged into a clean commit without taking it through push or GitHub PR creation. Get onto the correct feature branch first when needed, keep commit metadata aligned to the tracked diff, and stop after reporting the local commit result.

## Boundary Rules

- This skill owns local branch, changeset, and commit preparation only. It does not push or create or update GitHub PRs.
- If the user wants to take the work through push and PR creation, use `gh-pr-create` after this skill prepares or refreshes the commit.
- If the user wants a deep critique of the branch approach, implementation plan, or test strategy before mutating git state, use `gh-plan-review`.

## Core Workflow

1. If you are not already on the intended feature branch, create it immediately before doing other work. Do not continue on `main`, `master`, or another default branch.
2. Name the branch `<username>/<descriptive-name>`. Do not use `feature/`, `feat/`, or `fix/`. Use the system username when it is clear; otherwise fall back to the agent name.
3. Inspect `git status --short`, the current diff, and existing repo conventions before committing or amending so the commit describes the actual tracked work rather than a stale summary.
4. Complete the requested work and run the smallest relevant verification for the touched files before committing or amending.
5. If the repo uses Changesets, add the smallest accurate changeset before the final commit or amend.
6. Run `git branch --show-current` immediately before every commit or amend, even if you already checked it earlier in the task.
7. Create a new commit when the work is not yet committed. Amend the current commit when the existing message or body is stale relative to the tracked diff, including cases where PR text changes should be reflected in the single commit that a later `gh pr create --fill` step will use.
8. Write or refresh a commit message that matches the repository history, includes a body, and describes only the tracked staged diff. Do not mention thread discussion, related ideas, or requested changes that are not present in the committed files. When the local style is unclear, use a conventional commit.
9. If the work closes an issue completely, include `Closes #xx` or `Fixes #xx` in the commit body. If the work is partial, include `Part of #xx`.
10. Stop after the local commit step and report the branch name, short commit SHA, and changeset status.

## Branch Rules

- Create the branch as the first operational step when you are not already on the correct feature branch.
- Keep using the same feature branch unless the user explicitly redirects you.
- Never commit directly on `main`, `master`, or another default branch.
- When the user explicitly provides a branch name, use it if it still fits repo policy.

## Commit Rules

- Always run `git branch --show-current` before each commit or amend.
- Keep the commit body informative and non-empty.
- The commit title and body must describe the tracked staged diff only. Do not mention ignored files, local-only files, related discussion, rejected options, or future work unless those points are reflected in the committed files.
- Use `git commit --amend --no-edit` only when the existing commit message still accurately describes the updated tracked diff; otherwise amend the commit message so it matches the current diff.
- Use real newlines in multi-paragraph commit bodies. Prefer repeated `git commit -m` flags, an editor, or a file; never embed literal `\n` sequences and expect Git or GitHub to render them.
- Match existing commit style from nearby history before defaulting to conventional commits.

## Ignored File Rules

- Let Git ignore rules stand by default.
- Never use `git add -f`, `git add --force`, or any other override to stage an ignored path unless the user explicitly instructs you to include that ignored file in version control.
- Never decide on your own that an ignored file should be committed because it seems useful or related.
- Never mention ignored or local-only files in commit metadata unless the user explicitly wanted them included in version control and they are present in the tracked diff being described.

## Changeset Rules

- Add a changeset only when the repo is actually configured for Changesets.
- Treat `.changeset/` or equivalent repo conventions as evidence that Changesets is in use.
- Keep the changeset scoped to the user-visible change. Do not invent package impacts.
