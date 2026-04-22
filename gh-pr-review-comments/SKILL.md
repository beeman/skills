---
name: gh-pr-review-comments
description: Address GitHub pull request review comments on an existing feature branch. Use when Codex needs to fetch live PR review comments with gh, classify each comment as actionable, optional, or rejectable, apply only accepted fixes on the same branch, run a self-review pass for contradictions introduced by those fixes, and then either create a new commit or follow an explicitly approved history-rewrite path before pushing, resolving threads, and re-requesting review.
---

# Address PR Review Comments

Use this skill to run a full GitHub PR review follow-up pass from live comment data instead of screenshots or pasted summaries. Fetch the comments, decide what to accept, update only the current PR branch, resolve threads deliberately, and finish with the exact status line the user expects.

## Boundary Rules

- This skill addresses existing review comments on the current PR branch. It does not run a fresh end-to-end critique of the implementation plan.
- If the user wants a broader challenge of the plan, branch approach, or test strategy beyond the current review comments, use `gh-plan-review`.

## Core Workflow

1. Confirm you are already on the PR feature branch you intend to update, not `main`, `master`, or another default branch.
2. Fetch the authoritative review comments with `gh api --paginate repos/{owner}/{repo}/pulls/{pr}/comments`.
3. Exclude reply comments such as items with `in_reply_to_id` before triaging, so you classify top-level review requests rather than thread replies.
4. Classify every remaining review comment before touching code.
5. Inspect the relevant files, diff, and surrounding context for accepted comments.
6. Apply only the accepted fixes on the same PR branch.
7. Run the smallest relevant verification for the touched code.
8. Determine whether the PR branch has exactly one branch commit or multiple branch commits relative to the PR base. A multi-commit PR branch must not default to amend or force-push.
9. Before committing or pushing, re-read the affected workflow, file, or ruleset end-to-end and do a self-review for contradictions, path-specific regressions, or metadata mismatches introduced by the accepted fixes.
10. If that self-review introduces additional edits, run the smallest relevant verification again for the final diff.
11. If the PR branch has multiple branch commits relative to the PR base and the user did not explicitly request amend, squash, or another history rewrite, ask whether to create a new commit, amend `HEAD`, or use another explicit rewrite flow, and stop until the user answers.
12. Create a new commit when the chosen path is additive. Amend the existing PR commit only when the branch has exactly one branch commit relative to the PR base or when the user explicitly requested amend or squash. If the user explicitly requested another history rewrite, follow that instruction instead of assuming amend. Use `git commit --amend --no-edit` only when the existing commit message still accurately describes the updated branch diff; otherwise amend the commit message so it matches the current branch diff.
13. If a new commit was created, get any required user or repo-policy approval for pushing, then push the feature branch with `git push`. If history was rewritten, get any required user or repo-policy approval for pushing, then push the feature branch with `git push --force-with-lease`.
14. If the open PR title or body is now stale relative to the current branch diff, update the PR metadata before re-requesting review.
15. Post a short reply on every handled review thread describing the action taken, then resolve it intentionally.
16. After resolving handled threads, re-request review from each relevant human reviewer and supported review bot unless the user says not to. If a relevant bot is clearly identified but missing from [references/review-bots.md](references/review-bots.md), mention its username explicitly and ask the user whether to re-request that bot or add it to the registry instead of silently skipping it.
17. Report the result in the required status format.

## Triage Rules

Classify every top-level review comment into exactly one bucket before making edits. Do not treat reply comments as separate actionable review requests.

- `✅ valid/actionable`: Implement the change. Use this for correctness issues, real regressions, missing edge cases, missing tests, or maintainability problems that clearly matter.
- `⚪ optional/nit`: Decide case-by-case. Accept only if the change stays inside the current scope and keeps the diff minimal.
- `❌ invalid/circular/conflicting`: Do not change code blindly. Use this for stale feedback, misunderstandings, contradictory requests, circular churn, or scope expansion that is not justified by the PR.

Treat conflicting comments as a single decision, not two independent tasks. If a comment is unclear, inspect the code, tests, current PR diff, and related discussion before deciding.

## Implementation Rules

GitHub CLI commands that require network access should be run outside the sandbox immediately, using approved `gh` prefix rules when available, instead of trying them in-sandbox first.

- Work from live GitHub review data, not screenshots.
- Paginate `gh api` calls whenever the endpoint is paginated and the workflow depends on a complete result set.
- Keep the current PR branch intact. Preserve the single-commit flow only when the branch has exactly one branch commit relative to the PR base or the user explicitly requested history rewrite.
- Follow the repo and user push policy. If approval is required before any push, obtain it before pushing.
- On a multi-commit PR branch, ask before rewriting history.
- Use `git push` after a new commit on the PR feature branch.
- Use `git push --force-with-lease` only after amend, rebase, or another explicit history rewrite on the PR feature branch. Never force-push `main`, `master`, or another default branch.
- Touch only the files required to address accepted comments.
- Decline scope expansion unless the user explicitly asks for it.
- Avoid cosmetic churn when a comment is optional or invalid.
- If no comments are accepted, do not manufacture code changes just to appear responsive.
- If accepted fixes materially change the branch summary, refresh the commit message and open PR title/body so they still describe the current diff before re-requesting review. When refreshing an open PR body, preserve any applicable `Closes #xx`, `Fixes #xx`, or `Part of #xx` trailer and any required template sections that still accurately describe the current diff.
- If the self-review pass adds or changes files, rerun the smallest relevant verification on the final diff before committing and pushing.

## Self-Review Rules

- After applying accepted fixes and before re-requesting review, run a short adversarial self-review of the affected workflow or file, not just the touched hunk.
- Check whether the new wording or code creates contradictions with other paths, especially distinctions like single-commit versus multi-commit, new PR versus existing PR, commit metadata versus PR metadata, and default base versus configured base.
- If the accepted fix changes what text, behavior, or command will actually be sent or executed, verify that any preview, confirmation, or metadata rule still matches that actual behavior.
- Fix any material contradiction you can justify from local context before pushing and re-requesting review, including stale commit or PR metadata when the branch summary has changed.
- If fixing that contradiction changes the diff, rerun the smallest relevant verification before you commit and push.

## Thread Resolution Rules

- Every handled review thread must receive a short reply before you resolve it.
- Resolve `fixed` comments after the fix is present locally and ready to push, and reply with a short acknowledgement of what changed.
- Resolve `dismissed/no-change` comments only after posting a concise rationale.
- Resolve `partially-fixed` comments only after explaining exactly what changed and what did not.
- Do not leave handled comments open between passes.
- Count only threads you actually resolved during this pass in the final status line.
- Read [references/github-review-threads.md](references/github-review-threads.md) only when you need reply endpoints, thread IDs, or GraphQL resolution commands.

## Reviewer Rules

- Read [references/review-bots.md](references/review-bots.md) when you need the supported bot table, exact summon text, or preferred bot-detection evidence.
- Determine relevant human reviewers from handled review comments authored by non-bot users and from explicit user instruction.
- Re-request human reviewers with GitHub review requests when possible. Read [references/github-review-threads.md](references/github-review-threads.md) when you need the request-review command.
- If multiple human reviewers participated in the current review round, re-request each relevant human once after the fix is pushed.
- Determine relevant review bots in this order: handled review comments from a supported bot, explicit user instruction, then bot-authored top-level PR comments.
- If the bot is not obvious from inline review comments, inspect top-level PR comments with `gh api --paginate repos/{owner}/{repo}/issues/{pr}/comments` and prefer bot-authored comments over summon comments.
- Treat prior PR summon comments as historical context only. Use them only to corroborate explicit user instruction or current-round bot activity, never as the sole reason to re-request bot review.
- If multiple supported bots participated in the current review round, post one exact summon comment for each of them after pushing the fix.
- If a bot is clearly identified from PR context but is not listed in [references/review-bots.md](references/review-bots.md), mention the bot username explicitly and ask the user whether to re-request that bot or add it to the registry. Do not invent summon text.
- If a human reviewer or bot username cannot be identified confidently, do not guess. Skip that re-review request unless the user names the reviewer or you can confirm it from PR context.

## Git and Review Commands

Use one of these command paths after accepted fixes are ready on a PR feature branch:

```bash
# Single-commit branch or explicit history rewrite
git commit --amend --no-edit
git push --force-with-lease
```

```bash
# Multi-commit branch with additive update
git commit
git push
```

If the repo or user policy requires approval before pushing, obtain that approval first. Use `git push` after a new commit. Use `git push --force-with-lease` only after amend, rebase, or another explicit history rewrite on the PR feature branch.

When the PR branch has multiple branch commits relative to the PR base and the user did not explicitly request history rewrite, stop and ask whether to create a new commit, amend `HEAD`, or use another explicit rewrite flow.

When the self-review pass finds that the chosen commit message is stale, update it so it matches the current branch diff instead of blindly reusing old metadata. When the open PR title or body is stale, update the PR metadata before re-requesting review, preserving any applicable issue trailer or required template section that still matches the current diff instead of blindly replacing the body.

Re-request review when the pass is complete by requesting each relevant human reviewer again and by posting one standalone PR comment per relevant supported bot, using the exact summon text from [references/review-bots.md](references/review-bots.md). If a relevant bot is clearly identified but missing from that registry, mention its username explicitly and ask the user whether to re-request that bot or add it to the registry; do not invent a summon comment.

If no code changed, skip commit and push. If re-review would be misleading because the task is blocked or incomplete, or no relevant human reviewer or supported bot was identified, report `no` in the final status line.

## Output Format

After finishing the pass, emit exactly one status line in this format:

```text
status | commit | comments resolved (n) | re-review requested (yes/no)
```

Use these values consistently:

- `status`: `done`, `partial`, `blocked`, or `no-change`
- `commit`: short SHA of the created or updated commit, or `unchanged` if no commit was created
- `comments resolved (n)`: number of threads resolved in this pass
- `re-review requested (yes/no)`: `yes` only if you actually re-requested one or more relevant reviewers, whether by human review request or bot summon comment

Example:

```text
done | abc1234 | comments resolved (5) | re-review requested (yes)
```
