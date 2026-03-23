---
name: feature-structure
description: Refactor code into a feature-based structure or create a new feature by inferring repository conventions, selecting a matching topology, enforcing layer boundaries and import rules between data-access, feature, ui, and util modules, proposing the exact file and wiring changes, and waiting for confirmation before edits. Use when Codex needs to move code into feature folders or feature packages, add a new feature modeled after nearby modules, split code into layers such as data-access, feature, ui, or util, or wire thin route files and exports around a feature-based design in frontend, backend, or monorepo codebases.
---

# Build Feature Structure

## Overview

Use this skill to reorganize code around features or scaffold a new feature without embedding business logic. Infer the local pattern first, prefer the nearest existing feature as the model, and keep changes minimal-diff unless the user asks for broader restructuring.

## Layer Roles and Import Boundaries

When normalizing or creating a feature-based structure, prefer at most four library types: `data-access`, `feature` or `feature-<app>`, `ui` or `ui-<app>`, and optional `util`. If the repository already uses names such as `features/` for folders, keep the naming and apply the same responsibilities.

- `data-access`: own fetching, mutations, persistence, adapters, and other side-effectful integration work. It may import from other `data-access` modules. It must not import `feature` or `ui`.
- `feature` or `feature-<app>`: act as the smart/orchestrating layer. It should own routed screen logic and route params, decide which `data-access` calls run, and pass resolved data and callbacks into `ui`. In file-based routing repos, framework-owned route files stay as thin wrappers outside the feature tree. It may import from `data-access` and `ui`.
- `ui` or `ui-<app>`: stay presentational or dumb. It may import from other `ui` modules and passive pieces from `data-access`, such as types or pure helpers, but it must not own route parsing, API calls, mutations, or other side-effectful work.
- `util`: stay optional and rare. Use it for pure helpers, usually on the backend, and keep it free of rendering, route handling, and side-effectful orchestration.

## Core Workflow

1. Inspect the repository before proposing a structure. Read AGENTS files, docs, entrypoints, exports, package boundaries, routes, and nearby features or modules.
2. Infer the target topology from the repo. Read [references/feature-topologies.md](references/feature-topologies.md) when multiple layouts are plausible or the structure is not obvious.
3. Identify the nearest model feature or module. Prefer the closest existing pattern over inventing a new skeleton, and explain the choice.
4. Ask focused questions only for material unknowns that cannot be inferred safely.
5. Write a concrete proposal before editing. Read [references/proposal-contract.md](references/proposal-contract.md) and use that contract every time.
6. Wait for explicit confirmation before mutating files, moving code, or wiring entrypoints.
7. After confirmation, implement the approved structure and verify the affected imports, routes, exports, and tests.

## Discovery Rules

- Ask about product behavior only when it changes the scaffold or move plan. Do not ask about file locations or naming conventions you can inspect yourself.
- Inspect actual repository structure before deciding between app-local features, backend feature modules, or package-per-feature layouts.
- Inspect the import graph to determine whether the repo already enforces boundaries between `data-access`, `feature`, `ui`, and `util`.
- Let existing exports, path aliases, platform splits, route conventions, and workspace boundaries outweigh generic examples.
- Pick the nearest model by platform, responsibility, and runtime when several nearby features exist.
- Read [references/generic-feature-examples.md](references/generic-feature-examples.md) only as a structural fallback, never as repository truth.

## Implementation Rules

- Avoid speculative cleanup, renames, or extractions outside the requested feature move or scaffold.
- Enforce the layer boundaries above when moving or adding code. Do not leave route handling in `ui` or presentation logic as the owner of data-fetching side effects.
- Keep behavior unchanged during refactors unless the user asks to change it.
- Keep related code colocated so a future change does not require jumping across unrelated directories.
- Preserve public imports, path aliases, and naming conventions when possible. If a move forces updates, change all affected call sites in the same edit set.
- Run the smallest relevant verification after editing and state what you did not verify.

## Refactor Rules

- Keep the diff minimal. Do not mix structural work with unrelated cleanup.
- Move code by feature first and by responsibility second.
- Move route parsing, query or mutation orchestration, and other smart behavior into `feature` files when the target pattern expects dumb `ui`.
- Preserve thin entrypoints such as route files, package exports, or filesystem wrappers when the repo expects them.
- Update imports, exports, and route wiring as part of the same change when the move would otherwise leave broken references.

## Creation Rules

- Create the smallest viable feature structure that matches the chosen model feature.
- Do not invent business logic, API contracts, or domain data. Ask when the requested feature behavior is material and cannot be inferred.
- Leave explicit placeholders only when the repository pattern clearly requires a file but the user-facing behavior is still unknown.
- For UI-driven features, default to `feature` files that handle route params and `data-access` calls, then pass data and callbacks into `ui`.
- Wire obvious integrations after confirmation, such as exports, route registration, or thin filesystem route files.

## Reference Files

- Read [references/feature-topologies.md](references/feature-topologies.md) to compare supported layouts and choose one.
- Read [references/generic-feature-examples.md](references/generic-feature-examples.md) when you need sanitized naming or tree examples.
- Read [references/proposal-contract.md](references/proposal-contract.md) immediately before presenting the pre-edit proposal.
