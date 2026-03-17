---
name: gh-pr-review-comments
description: Address GitHub pull request review comments on an existing feature branch. Use when Codex needs to fetch live PR review comments with gh, classify each comment as actionable, optional, or rejectable, apply only accepted fixes on the same branch, keep a single-commit PR flow with git commit --amend and git push --force-with-lease, resolve review threads with explicit rationale, re-request relevant human reviewers and configured review bots, and report the result in the exact status line format.
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
8. Amend the existing PR commit with `git commit --amend --no-edit` if code changed.
9. If a new commit was created, get any required user or repo-policy approval for pushing, then push the feature branch with `git push --force-with-lease`.
10. Post a short reply on every handled review thread describing the action taken, then resolve it intentionally.
11. After resolving handled threads, re-request review from each relevant human reviewer and supported review bot unless the user says not to.
12. Report the result in the required status format.

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
- Keep the current PR branch and single-commit flow intact.
- Follow the repo and user push policy. If approval is required before any push, obtain it before pushing.
- Use `git push --force-with-lease` only on the PR feature branch. Never force-push `main`, `master`, or another default branch.
- Touch only the files required to address accepted comments.
- Decline scope expansion unless the user explicitly asks for it.
- Avoid cosmetic churn when a comment is optional or invalid.
- If no comments are accepted, do not manufacture code changes just to appear responsive.

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
- If a human reviewer or supported bot cannot be identified confidently, do not guess. Skip that re-review request unless the user names the reviewer or you can confirm it from PR context.

## Git and Review Commands

Use these commands for the single-commit PR flow after accepted fixes are ready on a PR feature branch:

```bash
git commit --amend --no-edit
git push --force-with-lease
```

If the repo or user policy requires approval before pushing, obtain that approval first. Once pushing is allowed, use `git push --force-with-lease` for the PR feature branch update.

Re-request review when the pass is complete by requesting each relevant human reviewer again and by posting one standalone PR comment per relevant bot, using the exact summon text from [references/review-bots.md](references/review-bots.md).

If no code changed, skip amend and push. If re-review would be misleading because the task is blocked or incomplete, or no relevant human reviewer or supported bot was identified, report `no` in the final status line.

## Output Format

After finishing the pass, emit exactly one status line in this format:

```text
status | commit | comments resolved (n) | re-review requested (yes/no)
```

Use these values consistently:

- `status`: `done`, `partial`, `blocked`, or `no-change`
- `commit`: short SHA of the amended commit, or `unchanged` if no commit was created
- `comments resolved (n)`: number of threads resolved in this pass
- `re-review requested (yes/no)`: `yes` only if you actually re-requested one or more relevant reviewers, whether by human review request or bot summon comment

Example:

```text
done | abc1234 | comments resolved (5) | re-review requested (yes)
```
