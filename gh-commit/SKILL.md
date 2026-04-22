---
name: gh-commit
description: Prepare a local Git commit from repo changes. Use when Codex needs to get onto the correct feature branch if needed, inspect `git status --short`, the current diff, and branch history, run the smallest relevant verification, add any required changeset, and package the tracked work into either a new commit or an explicitly approved amend flow before any push or PR step.
---

# Commit Changes

Use this skill when the user wants the current local work packaged into a clean commit without taking it through push or GitHub PR creation. Get onto the correct feature branch first when needed, keep commit metadata aligned to the tracked diff, ask before rewriting history on non-default multi-commit branches, and stop after reporting the local commit result.

## Boundary Rules

- This skill owns local branch, changeset, and commit preparation only. It does not push or create or update GitHub PRs.
- If the user wants to take the work through push and PR creation, use `gh-pr-create` after this skill prepares or refreshes the commit.
- If the user wants a deep critique of the branch approach, implementation plan, or test strategy before mutating git state, use `gh-plan-review`.

## Core Workflow

1. If you are not already on the intended feature branch, create it immediately before doing other work. Do not continue on `main`, `master`, or another default branch.
2. Name the branch `<username>/<descriptive-name>`. Do not use `feature/`, `feat/`, or `fix/`. Use the system username when it is clear; otherwise fall back to the agent name.
3. Inspect `git status --short`, the current diff, existing repo conventions, and branch history before deciding whether to create a new commit or amend.
4. Determine whether the current branch is single-commit or multi-commit. Count branch commits relative to the intended PR base when that base is known; otherwise count relative to the repository default-branch merge-base. More than one branch commit is multi-commit.
5. Complete the requested work and run the smallest relevant verification for the touched files before committing or amending.
6. If the repo uses Changesets, add the smallest accurate changeset before the final commit or amend.
7. On a non-default multi-commit branch, do not assume amend or squash. Ask whether to create a new commit, amend `HEAD`, or do another explicit history rewrite, and stop until the user answers.
8. Run `git branch --show-current` immediately before every commit or amend, even if you already checked it earlier in the task.
9. Create a new commit when the work is not yet committed, when the user explicitly asked for a new commit, or when a non-default multi-commit branch has already gone through the ask-first gate and the user chose an additive update. Amend the current commit when the branch has exactly one branch commit or when the user explicitly requested amend or squash. If the user explicitly requested another history rewrite, follow that instruction instead of assuming amend.
10. Write or refresh a commit message that matches the repository history, includes a body, and describes only the tracked staged diff. Describe the code or file changes themselves, not the chat history of how the decision was reached. Do not mention thread discussion, steering, rejected options, or requested changes that are not present in the committed files. Prefer concrete change descriptions such as what was added, removed, or updated over process notes such as "made sure not to use X" unless that removal is itself part of the tracked diff. When the local style is unclear, use a conventional commit.
11. If the work closes an issue completely, include `Closes #xx` or `Fixes #xx` in the commit body. If the work is partial, include `Part of #xx`.
12. Stop after the local commit step and report the branch name, short commit SHA, and changeset status.

## Branch Rules

- Create the branch as the first operational step when you are not already on the correct feature branch.
- Keep using the same feature branch unless the user explicitly redirects you.
- Never commit directly on `main`, `master`, or another default branch.
- When the user explicitly provides a branch name, use it if it still fits repo policy.

## Commit Rules

- Always run `git branch --show-current` before each commit or amend.
- Determine single-commit versus multi-commit branch state before deciding to amend. Count branch commits relative to the intended PR base when known; otherwise use the repository default-branch merge-base.
- Keep the commit body informative and non-empty.
- On a non-default multi-commit branch, do not assume amend or squash. Ask whether to create a new commit, amend `HEAD`, or do another explicit history rewrite, and stop until the user answers.
- The commit title and body must describe the tracked staged diff only. Describe the resulting change, not the conversation, steering, or decision path behind it. Do not mention ignored files, local-only files, related discussion, rejected options, implementation process, or future work unless those points are reflected in the committed files.
- Amend by default only when the branch has exactly one branch commit or the user explicitly requested amend or squash.
- If the user explicitly requested another history rewrite, follow that instruction instead of assuming amend.
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
