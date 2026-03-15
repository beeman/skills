---
name: gh-issue-kickoff
description: Kick off work on a GitHub issue with gh. Use when Codex needs to start working an issue by inspecting the live issue and local codebase, checking whether the issue is materially ready, applying only safe issue improvements, escalating real blockers or stale or incoherent requirements, and producing an execution-ready implementation plan.
---

# Kick Off Issue Work

Use this skill to start work on a GitHub issue from live GitHub data and current repo context. Treat readiness review as the opening gate inside the kickoff, not the end goal.

## Overview

Assume the issue is probably good enough to start from. Only stop or escalate when you find a material blocker, contradiction, stale detail, or planning-critical omission that would make execution unsafe or incoherent.

## Core Workflow

1. Fetch the authoritative issue state with `gh issue view {<number> | <url>} --json assignees,author,body,comments,labels,milestone,number,projectItems,state,title,updatedAt,url`.
2. Read the title, body, comments, labels, and update timing before making assumptions about the issue's quality.
3. Inspect the relevant local codebase, current architecture, and nearby docs so the plan reflects reality instead of issue wording alone.
4. Build the implementation approach while checking whether the issue is materially ready to execute.
5. Classify the issue as `ready`, `ready-with-minor-fixes`, `needs-clarification`, or `blocked`.
6. Apply only safe `gh issue edit` changes when the fix is factual, non-controversial, and does not change product intent.
7. Use `gh issue comment` when the issue should not be edited directly but a concise clarification request or planning note would help stakeholders unblock the work.
8. Escalate to stakeholders only when missing or conflicting information materially changes the implementation plan or makes execution unsafe.
9. Produce the implementation plan, issue findings, any issue updates, any stakeholder follow-up, and the next execution step.
10. End with the required status line.

## Material Readiness Rules

Flag only material issue problems. Ignore cosmetic polish, tone, and formatting nits unless they hide a real ambiguity.

- Treat missing or weak acceptance criteria as material when you cannot tell what success looks like from the issue plus repo context.
- Treat stale details as material when referenced files, APIs, branches, workflows, or linked discussions no longer match the current codebase or project state.
- Treat contradictions as material when the title, body, comments, labels, or local implementation constraints point to incompatible outcomes.
- Treat dependency gaps as material when the plan depends on another issue, missing API, unresolved decision, or unavailable system.
- Treat repo mismatch as material when the issue assumes architecture, directories, tooling, or ownership that the current codebase does not support.
- Treat scope gaps as material when the issue is too underspecified to produce a credible execution-ready plan.

## Safe Issue Update Rules

- Use `gh issue edit` for factual corrections, broken or stale references, obvious structural cleanup, or concise clarifications that preserve the original intent.
- Use `gh issue comment` for questions, risks, or planning notes that need stakeholder visibility or should remain part of the issue discussion.
- Do not invent requirements, rewrite the product direction, silently narrow or widen scope, or convert open decisions into assumed facts.
- If a change would reasonably need product, design, or stakeholder agreement, do not edit the issue body as if the decision is already made.
- Keep updates minimal and directly tied to execution readiness.

## Stakeholder Escalation Rules

- Escalate only when unresolved information would materially change the plan, timeline, validation strategy, or user-facing behavior.
- Ask focused questions tied to the blocker instead of requesting a general issue rewrite.
- If the issue is still executable with stated assumptions, record those assumptions and continue rather than blocking on optional detail.
- If the issue is not safely executable, say why and name the smallest decision or clarification needed to unblock it.

## Output Format

After finishing the kickoff pass, present the result in this order:

1. `Implementation Plan`
2. `Material Issue Findings`
3. `Issue Updates`
4. `Stakeholder Follow-up`
5. `Next Execution Step`

Then emit exactly one status line in this format:

```text
status | issue updates (none/drafted/applied) | stakeholder follow-up (yes/no) | execution ready (yes/no)
```

Use these values consistently:

- `status`: `done`, `partial`, or `blocked`
- `issue updates`: `none`, `drafted`, or `applied`
- `stakeholder follow-up`: `yes` only if you actually identified or posted a required stakeholder follow-up
- `execution ready`: `yes` only when the plan is actionable without waiting on unresolved material blockers
