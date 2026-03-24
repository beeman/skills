---
name: feature-structure
description: Refactor code into a composition-first feature structure or create a new feature by inferring repository conventions, selecting a matching topology, and enforcing boundaries between data-access, feature, ui, and util modules. Use when Codex needs to move code into feature folders or feature packages, split prerequisite workflows into parent and child features, add a new feature modeled after nearby modules, or wire thin route files and exports around a feature-based design in frontend, backend, or monorepo codebases while waiting for confirmation before edits.
---

# Build Feature Structure

## Overview

Use this skill to reorganize code around features or scaffold a new feature without embedding business logic. Treat a feature as a composition boundary, not just a place to move one large smart component. Infer the local pattern first, prefer the nearest existing feature as the model, and keep changes minimal-diff unless the user asks for broader restructuring.

## Layer Roles and Import Boundaries

When normalizing or creating a feature-based structure, prefer at most four library types: `data-access`, `feature` or `feature-<app>`, `ui` or `ui-<app>`, and optional `util`. If the repository already uses names such as `features/` for folders, keep the naming and apply the same responsibilities.

- `data-access`: own adapters, fetching, invalidation, mutations, mutation-side effects, persistence, and other side-effectful integration work. It may import from other `data-access` modules. It must not import `feature` or `ui`. Prefer one exported thing per file, one hook per file when hooks are used, and concrete imports over barrels unless the repository already standardizes a different pattern.
- `feature` or `feature-<app>`: act as the smart or orchestration layer. It should own routed screen logic and route params, decide which `data-access` calls run, compose child features when a workflow has distinct phases or prerequisites, and pass resolved data and callbacks into `ui`. In file-based routing repos, framework-owned route files stay as thin wrappers outside the feature tree. It may import from `data-access` and `ui`.
- `ui` or `ui-<app>`: stay presentational or dumb. It may import from other `ui` modules and passive pieces from `data-access`, such as pure helpers or types, but it must not own route parsing, API calls, mutations, or other side-effectful work. Prefer granular leaf components over a single large screen component when `feature` is orchestrating multiple states or workflows.
- `util`: stay optional and rare. Use it for pure helpers, usually on the backend, and keep it free of rendering, route handling, and side-effectful orchestration.

## Composition Rules

- Bias toward smaller composable `feature` files when a workflow has distinct prerequisites, phases, or branching ownership boundaries, especially when the repository has no strong existing model to copy.
- Do not mount a dependent child feature until its prerequisites are satisfied or the child has enough state to make its own decision safely.
- Keep feature-to-feature handoff contracts minimal and stable. Pass only the state a child feature needs to decide what to render or which query or mutation to run.
- Prefer early-return composition over `let content` accumulation or long `else if` chains in `feature` files. If a feature starts accumulating many branches, treat that as a signal to split the workflow across feature boundaries.
- Prefer local interfaces and types inside each file. Avoid shared exported type modules unless multiple files genuinely need the same domain shape.

## Core Workflow

1. Inspect the repository before proposing a structure. Read AGENTS files, docs, entrypoints, exports, package boundaries, routes, and nearby features or modules.
2. Infer the target topology from the repo. Read [references/feature-topologies.md](references/feature-topologies.md) when multiple layouts are plausible or the structure is not obvious.
3. Identify the nearest model feature or module. Prefer the closest existing pattern over inventing a new skeleton, and explain the choice.
4. Identify prerequisite workflows, distinct phases, and likely child feature boundaries before deciding where code moves.
5. Ask focused questions only for material unknowns that cannot be inferred safely.
6. Write a concrete proposal before editing. Read [references/proposal-contract.md](references/proposal-contract.md) and use that contract every time.
7. Wait for explicit confirmation before mutating files, moving code, or wiring entrypoints.
8. After confirmation, implement the approved structure and verify the affected imports, routes, exports, and tests.

## Discovery Rules

- Ask about product behavior only when it changes the scaffold or move plan. Do not ask about file locations or naming conventions you can inspect yourself.
- Check whether the workflow has prerequisite states or phases that should become separate child features instead of branches inside one file.
- Infer the minimum stable handoff contract between parent and child features before deciding which props or state move across the boundary.
- Inspect actual repository structure before deciding between app-local features, backend feature modules, or package-per-feature layouts.
- Inspect the import graph to determine whether the repo already enforces boundaries between `data-access`, `feature`, `ui`, and `util`.
- Let existing exports, path aliases, platform splits, route conventions, and workspace boundaries outweigh generic examples.
- Pick the nearest model by platform, responsibility, and runtime when several nearby features exist.
- Read [references/generic-feature-examples.md](references/generic-feature-examples.md) only as a structural fallback, never as repository truth.
- Treat a sparse or empty `features/` directory as a weak signal. Do not assume one smart feature file plus one screen component is the right default just because no stronger model exists.

## Implementation Rules

- Avoid speculative cleanup, renames, or extractions outside the requested feature move or scaffold.
- Avoid barrels and `index.ts` exports by default unless the repository already standardizes them.
- Enforce the layer boundaries above when moving or adding code. Do not leave route handling in `ui` or presentation logic as the owner of data-fetching side effects.
- Keep behavior unchanged during refactors unless the user asks to change it.
- Keep related code colocated so a future change does not require jumping across unrelated directories.
- Keep shared exported types local unless multiple files genuinely need the same domain shape.
- Preserve public imports, path aliases, and naming conventions when possible. If a move forces updates, change all affected call sites in the same edit set.
- Run the smallest relevant verification after editing and state what you did not verify.

## Refactor Rules

- Keep the diff minimal. Do not mix structural work with unrelated cleanup.
- Keep thin entrypoints such as route files, package exports, or filesystem wrappers when the repo expects them.
- Move code by feature first and by responsibility second.
- Move route parsing, query or mutation orchestration, and other smart behavior into `feature` files when the target pattern expects dumb `ui`.
- Prefer splitting workflow phases into separate child features over moving the same monolithic branching logic into a different folder.
- Update imports, exports, and route wiring as part of the same change when the move would otherwise leave broken references.

## Creation Rules

- Create the smallest viable feature structure that matches the chosen model feature.
- Do not invent business logic, API contracts, or domain data. Ask when the requested feature behavior is material and cannot be inferred.
- For UI-driven features, default to `feature` files that handle route params and `data-access` calls, then pass data and callbacks into `ui`.
- Leave explicit placeholders only when the repository pattern clearly requires a file but the user-facing behavior is still unknown.
- Prefer a parent feature plus child features when a routed screen has prerequisite selection, setup, or gating flows before the dependent workflow can run.
- Wire obvious integrations after confirmation, such as exports, route registration, or thin filesystem route files.

## Reference Files

- Read [references/feature-topologies.md](references/feature-topologies.md) to compare supported layouts and choose one.
- Read [references/generic-feature-examples.md](references/generic-feature-examples.md) when you need sanitized naming or tree examples.
- Read [references/proposal-contract.md](references/proposal-contract.md) immediately before presenting the pre-edit proposal.
