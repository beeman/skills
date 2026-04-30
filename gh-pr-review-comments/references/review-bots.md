# Review Bot Registry

Use this reference when you need the exact re-review summon comment or when adding support for another review bot. Human reviewers are not listed here; re-request them with GitHub review requests instead of summon comments.

| Bot key | Summon comment | Preferred evidence | Fallback evidence |
| --- | --- | --- | --- |
| `chatgpt-codex-connector` | `@codex review` | Review comments or top-level PR comments clearly authored by the Codex connector | Explicit user instruction, optionally corroborated by prior `@codex` summon comments |
| `coderabbitai` | `@coderabbitai review` | Review comments or top-level PR comments clearly authored by CodeRabbit | Explicit user instruction, optionally corroborated by prior `@coderabbitai` summon comments |
| `gemini-code-assist` | `@gemini-code-assist review` | Review comments or top-level PR comments clearly authored by Gemini | Explicit user instruction, optionally corroborated by prior `@gemini-code-assist` summon comments |

## Rules

- Keep rows alphabetized by `Bot key`.
- Prefer `Preferred evidence` over `Fallback evidence` when deciding whether a bot is relevant.
- Post one standalone PR comment per bot using the exact `Summon comment` text.
- If multiple supported bots participated on the same PR, summon each of them once after fixes are pushed.
- Never use a prior summon comment as the only evidence that a bot should be re-requested.
- If a bot is not in this table, do not invent a summon. Ask the user or skip re-review.
- When adding a new bot, include its exact summon text and the clearest detection hint you can verify.
