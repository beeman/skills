---
name: gh-plan-review
description: Review, challenge, pressure-test, or refine an implementation plan tied to a GitHub issue, GitHub PR, or active branch. Use when Codex needs to inspect the authoritative GitHub state and local repo context, run a scope challenge, identify material plan risks, surface real tradeoffs, and finish with a fixed review summary before any code edits.
---

# Review GitHub Plan

Use this skill when the user wants a deep review of an implementation plan before coding or before broadening an in-flight issue, PR, or branch. This skill is report-only: inspect, challenge, and summarize, but do not edit code, GitHub issues, TODO files, or branch state.

## Boundary Rules

- Use `gh-issue-kickoff` when the user wants to start from an issue and produce the first execution-ready plan.
- Use this skill when the user wants to review, challenge, pressure-test, or refine an existing implementation plan, test strategy, or branch approach.
- Do not widen this skill into execution, issue cleanup, or git mutation work. If the user switches to implementation, hand off to the appropriate execution skill.

## Core Workflow

1. Identify the authoritative plan source:
   - GitHub issue: fetch with `gh issue view {<number> | <url>} --json assignees,author,body,comments,labels,milestone,number,projectItems,state,title,updatedAt,url`
   - GitHub PR: fetch with `gh pr view {<number> | <url>} --json baseRefName,body,files,headRefName,number,state,title,url`
   - Active branch only: inspect `git branch --show-current`, `git status --short`, the current diff, and any local plan or design docs
2. Inspect the relevant local codebase, architecture, tests, and diff before judging the plan.
3. Ground the review in evidence. The authoritative GitHub state, current repo shape, and actual branch diff win over pasted summaries or stale notes.
4. Run `Scope Challenge` before deeper review.
5. Review architecture and boundaries, code shape and maintainability, tests and validation gaps, and performance, rollout, and failure modes.
6. Record obvious fixes directly in the findings without interrupting the user. Ask the user only when a choice materially changes behavior, scope, validation, or rollout.
7. Finish with the required output sections and status line.

## Source Grounding Rules

GitHub CLI commands that require network access should be run outside the sandbox immediately, using approved `gh` prefix rules when available, instead of trying them in-sandbox first.

- If an issue or PR is referenced, fetch the live GitHub state before trusting pasted summaries, screenshots, or memory.
- Read the current diff and nearby code before calling something missing, redundant, or risky.
- Prefer the smallest plan change that makes execution safer or clearer.
- Call out when the plan unnecessarily rebuilds existing flows or ignores nearby patterns.
- If the source of truth is incomplete, say what is missing and whether the gap is material or cosmetic.

## Scope Challenge

Answer these before deeper review:

1. What already exists that partially or fully solves the problem?
2. What is the minimum viable change that achieves the goal?
3. What dependencies, blockers, or unresolved decisions could invalidate the plan?
4. Where is the plan expanding scope beyond the stated goal?

If the plan is still executable with stated assumptions, record those assumptions and continue. If not, flag the smallest decision needed to unblock it.

## Review Sections

### 1. Architecture and boundaries

Evaluate component boundaries, data flow, integration points, security-sensitive edges, and whether the plan creates avoidable coupling or single points of failure.

### 2. Code shape and maintainability

Evaluate module shape, reuse of existing patterns, error handling, edge-case coverage, over-engineering, under-engineering, and whether the plan stays minimal-diff.

### 3. Tests and validation gaps

Evaluate what must be tested, which user-visible paths or failure cases need coverage, and whether the validation plan matches the risk of the change.

### 4. Performance, rollout, and failure modes

Evaluate likely bottlenecks, expensive code paths, rollout and compatibility risks, and realistic failure modes that the plan does not yet account for.

## Materiality and Question Rules

- Focus on material issues. Ignore cosmetic phrasing or document polish unless it hides a real ambiguity.
- A question is material when the answer changes behavior, scope, interfaces, test strategy, rollout, or whether execution is safe.
- If there is an obvious fix with no meaningful tradeoff, include it in `Plan Findings` instead of stopping to ask.
- When asking the user to choose, explain the tradeoff plainly, give a recommendation, and keep the options concrete.
- Do not silently expand scope, invent requirements, or convert open decisions into facts.

## Output Format

After finishing the review, present the result in this order:

1. `Scope Challenge`
2. `Plan Findings`
3. `Open Decisions`
4. `NOT in scope`
5. `What already exists`
6. `Test Strategy`
7. `Next Step`

Then emit exactly one status line in this format:

```text
status | source (issue/pr/branch) | open decisions (n) | execution ready (yes/no)
```

Use these values consistently:

- `status`: `done`, `partial`, or `blocked`
- `source (issue/pr/branch)`: primary source of truth used for the review
- `open decisions (n)`: number of unresolved material choices left for the user or stakeholders
- `execution ready`: `yes` only when the reviewed plan can be executed safely without waiting on unresolved material blockers
