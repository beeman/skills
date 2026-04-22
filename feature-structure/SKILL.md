---
description: Use when reorganizing code around feature boundaries, splitting monolithic screen components or state hooks, deciding whether logic belongs in data-access, feature, ui, or child features, or moving orchestration out of prop-heavy UI files.
name: feature-structure
---

# Build Feature Structure

## Overview

Use this skill to reorganize code around features or scaffold a new feature without embedding business logic. Treat a feature as a composition boundary, not just a place to move one large smart component. Infer the local pattern first, preserve established repository naming and wiring when they already exist, and keep changes minimal-diff unless the user asks for broader restructuring.

A feature file should compose child features and leaf UI directly. Do not default to one large screen-shaped UI component that receives the whole feature state and callback surface as props. Features may import other features. UI is not a dumping ground for screen orchestration.

## Layer Roles and Import Boundaries

When normalizing or creating a feature-based structure, prefer at most four library types: `data-access`, `feature` or `feature-<app>`, `ui` or `ui-<app>`, and optional `util`. If the repository already uses names such as `features/` for folders, keep the naming and apply the same responsibilities.

- `data-access`: own adapters, fetching, invalidation, mutations, mutation-side effects, persistence, platform checks, and other side-effectful integration work. It may import from other `data-access` modules. It must not import `feature` or `ui`. Prefer one exported thing per file, one hook per file when hooks are used, one query or mutation per hook when possible, and concrete imports over barrels unless the repository already standardizes a different pattern. Mutation hooks should own error handling, invalidation, and side effects.
- `feature` or `feature-<app>`: act as the smart or orchestration layer. It should own routed screen logic and route params, decide which `data-access` calls run, compose child features when a workflow or screen subsection has distinct phases, prerequisites, or hook orchestration, and pass only minimal resolved data or imperative domain actions into `ui`. In file-based routing repos, framework-owned route files stay as thin wrappers outside the feature tree. It may import from `data-access`, `ui`, and narrower `feature` files.
- `ui` or `ui-<app>`: stay presentational or dumb. It may import from other `ui` modules and passive pieces from `data-access`, such as pure helpers or types, but it must not own route parsing, API calls, mutations, or other side-effectful workflow orchestration. Prefer granular leaf components over a single large screen component when `feature` is orchestrating multiple states or workflows. Keep ephemeral form or input state local to the leaf UI component unless multiple siblings genuinely need it. Do not turn `ui` into a screen-shaped prop bag sink.
- `util`: stay optional and rare. Use it for pure helpers, usually on the backend, and keep it free of rendering, route handling, and side-effectful orchestration.

## File Shape Defaults

- Prefer one primary export per file: one React component or one hook.
- Additional exports should be limited to colocated types, constants, or tiny pure helpers.
- If a file starts exporting multiple independently useful components, split them into separate files.
- Reject files that export a shell plus several cards, buttons, messages, and details components together unless the repository explicitly standardizes that pattern and the proposal says why it stays.

## Feature vs UI Test

Use a `feature` file when a unit:
- calls one or more `data-access` hooks
- branches between workflow states
- gates prerequisites
- decides which child components or child features to mount
- coordinates a subsection of a screen with its own behavior

Use a `ui` file when a unit:
- renders one visual or layout responsibility
- receives only the minimal props it needs
- does not own workflow branching
- does not call query or mutation hooks by default
- can be reused as a leaf under a feature without understanding broader screen state

## Composition Rules

- Bias toward smaller composable `feature` files when a workflow has distinct prerequisites, phases, or branching ownership boundaries, especially when the repository has no strong existing model to copy.
- Features may import narrower child features. When a subsection owns its own hooks, branching, or prerequisite checks, pull it into a child feature instead of routing everything through a parent feature or giant UI component.
- Do not mount a dependent child feature until its prerequisites are satisfied. The parent feature should own prerequisite checks and branch early instead of passing booleans down so the child can sort it out.
- Keep feature-to-feature handoff contracts minimal and stable. Pass only the state a child feature needs to decide what to render or which query or mutation to run.
- Treat large UI prop bags as a design smell. If a UI component needs several booleans, callbacks, labels, and domain values to represent a workflow, stop and split the workflow into child features and leaf UI components.
- Prefer the parent feature composing several small UI leaves and child features directly over a single screen-level `ui` component that receives the whole state and callback bag.
- Prefer imperative domain action names over vague event names. Favor contracts such as `createTodo`, `deleteTodo`, `setActiveOrganization`, and `toggleTodo` over names like `onActiveOrganizationChange`.
- Prefer early-return composition over `let content` accumulation or long `else if` chains in `feature` files. If a feature starts accumulating many branches, treat that as a signal to split the workflow across feature boundaries.
- Prefer local interfaces and types inside each file. Avoid shared exported type modules unless multiple files genuinely need the same domain shape.

## Naming Defaults

- `data-access`: name hook files after one query or one mutation. Prefer file names such as `use-todo-create.ts`, `use-todo-delete.ts`, `use-todo-list-query.ts`, `use-todo-organizations-query.ts`, `use-todo-set-active-organization.ts`, and `use-todo-toggle.ts`. When naming exported identifiers, prefer valid forms such as `useTodoCreate`, `useTodoDelete`, `useTodoListQuery`, `useTodoOrganizationsQuery`, `useTodoSetActiveOrganization`, and `useTodoToggle`. Use query-shaped names for reads and imperative domain actions for mutations. Reject transport or placeholder names such as `use-todo-fetch-data.ts`, `use-todo-get-all.ts`, `use-todo-handle-submit.ts`, `useTodoFetchData`, `useTodoGetAll`, and `useTodoHandleSubmit` unless the repository already standardizes them and the proposal says why they stay.
- `feature` or `feature-<app>`: name files by workflow responsibility or phase. Prefer names such as `todo-feature-active-organization.tsx`, `todo-feature-entry.tsx`, and `todo-feature-organization-selection.tsx`. Reject placeholder defaults such as `*-feature-index`, `*-feature-manage`, `*-screen`, `*-view`, and `*-wrapper` unless the repository already standardizes them and the proposal says why they stay.
- `ui` or `ui-<app>`: name files by the concrete presentational unit they render. Prefer names such as `todo-ui-create-form.tsx`, `todo-ui-list.tsx`, `todo-ui-list-item.tsx`, `todo-ui-loading.tsx`, `todo-ui-organization-select.tsx`, `todo-ui-shell.tsx`, and `todo-ui-status-message.tsx`. These are valid because they describe leaf UI responsibilities, not orchestration placeholders.

## Data-Access Defaults

- If the caller needs success or failure to drive UI behavior, return a useful result from the async contract instead of forcing the UI to swallow errors.
- Mutation hooks should expose awaited contracts such as `mutateAsync` when follow-up behavior depends on success.
- Prefer one query or one mutation per data-access hook. Reject aggregate hooks such as `useTodoManagement` or `useTodoOrganizationState` unless the repository already has a deliberate contract the user asked to preserve.
- Prefer small domain-specific hook file names and exported identifiers that describe one action or one query directly. Use query-shaped names for reads and imperative domain verbs for mutations unless the repository already standardizes a different pattern.
- Do not leave reusable hooks inline in `feature` files when they belong in `data-access`.

## UI Defaults

- Do not use empty `catch(() => {})` wrappers in UI. If the UI needs to react to success, design the async contract to return enough information.
- Keep ephemeral draft, filter, or input state in the leaf UI component by default. Do not lift it into `feature` just to clear it after success.
- Let the UI clear local state after an awaited success from a feature or data-access action.
- Prefer small leaf components such as create forms, list items, lists, loading states, selectors, shells, and status messages over one generic `*-manage` screen that still owns most rendering. Names such as `todo-ui-list.tsx` and `todo-ui-list-item.tsx` are good because they describe concrete presentational units.
- Each `ui` file should usually render one concrete presentational unit. If a `ui` file starts exporting multiple independently useful leaf components, split them.
- UI components should receive the smallest possible props. If a UI component needs many booleans, callbacks, labels, and domain values, re-evaluate the boundary.

## Anti-Patterns to Reject

- child features that receive prerequisite booleans and branch internally instead of being mounted only when ready
- one large aggregate state hook that mixes queries, mutations, gating, and UI-local state
- one screen-shaped `ui` component that accepts a large state and action prop bag from `feature`
- one `ui` file exporting many concrete leaf components that should be separate files
- a parent `feature` that only pumps props into a giant child `ui` component instead of composing leaf UI and child features directly
- one large `*-manage` or screen component that still owns most rendering after the extraction
- proposals that copy a weak local monolith without explaining why stronger composition is not appropriate

## Core Workflow

1. Inspect the repository before proposing a structure. Read AGENTS files, docs, entrypoints, exports, package boundaries, routes, and nearby features or modules.
2. Infer the target topology from the repo. Read [references/feature-topologies.md](references/feature-topologies.md) when multiple layouts are plausible or the structure is not obvious.
3. Identify the nearest model feature or module. Preserve the closest existing naming, wiring, and boundary conventions, but do not copy a weak monolith just because it is nearby.
4. Identify prerequisite workflows, distinct phases, likely child feature boundaries, single-purpose query and mutation hooks, file-shape boundaries, and leaf UI boundaries before deciding where code moves.
5. Ask focused questions only for material unknowns that cannot be inferred safely.
6. Write a concrete proposal before editing. Read [references/proposal-contract.md](references/proposal-contract.md) and use that contract every time.
7. Wait for explicit confirmation before mutating files, moving code, or wiring entrypoints.
8. After confirmation, implement the approved structure and verify the affected imports, routes, exports, and tests.

## Discovery Rules

- Ask about product behavior only when it changes the scaffold or move plan. Do not ask about file locations or naming conventions you can inspect yourself.
- Check whether the workflow has prerequisite states or phases that should become separate child features instead of branches inside one file.
- Check whether a screen subsection is really a child feature instead of a prop-heavy `ui` component.
- Check whether ephemeral form or input state can stay in leaf UI instead of moving into `feature`.
- Infer the minimum stable handoff contract between parent and child features before deciding which props or state move across the boundary.
- Inspect actual repository structure before deciding between app-local features, backend feature modules, or package-per-feature layouts.
- Inspect the import graph to determine whether the repo already enforces boundaries between `data-access`, `feature`, `ui`, and `util`.
- Let existing exports, path aliases, platform splits, route conventions, and workspace boundaries outweigh generic examples.
- Map the likely query and mutation split before accepting any aggregate hook shape.
- Pick the nearest model by platform, responsibility, and runtime when several nearby features exist.
- Read [references/generic-feature-examples.md](references/generic-feature-examples.md) only as a structural fallback, never as repository truth.
- Treat nearby route-level CRUD files, dashboards, or other sparse examples as input material, not automatically as the target feature shape.
- Treat a sparse or empty `features/` directory as a weak signal. Do not assume one smart feature file plus one screen component is the right default just because no stronger model exists.

## Implementation Rules

- Avoid speculative cleanup, renames, or extractions outside the requested feature move or scaffold.
- Avoid barrels and `index.ts` exports by default unless the repository already standardizes them.
- Enforce the layer boundaries above when moving or adding code. Do not leave route handling in `ui` or presentation logic as the owner of data-fetching side effects.
- Keep behavior unchanged during refactors unless the user asks to change it.
- Keep related code colocated so a future change does not require jumping across unrelated directories.
- Keep shared exported types local unless multiple files genuinely need the same domain shape.
- Preserve established repository naming, imports, path aliases, route wiring, and workspace boundaries when they already exist, but do not introduce new placeholder names just because the nearest example is weak or monolithic.
- Preserve public imports, path aliases, and naming conventions when possible. If a move forces updates, change all affected call sites in the same edit set.
- Prefer one primary export per file over multi-component utility dumps.
- Prefer one query or mutation per data-access hook over introducing a new aggregate management hook.
- Run the smallest relevant verification after editing and state what you did not verify.

## Refactor Rules

- Keep the diff minimal. Do not mix structural work with unrelated cleanup.
- Keep thin entrypoints such as route files, package exports, or filesystem wrappers when the repo expects them.
- Move code by feature first and by responsibility second.
- Move route parsing, query or mutation orchestration, and other smart behavior into `feature` files when the target pattern expects dumb `ui`.
- Prefer feature-to-feature composition over pumping a large state and callback bag into one `ui` component.
- Prefer splitting workflow phases into separate child features over moving the same monolithic branching logic into a different folder.
- Split monolithic hooks or screen components when they would otherwise leave the feature behaving like the same monolith in a new directory.
- Update imports, exports, and route wiring as part of the same change when the move would otherwise leave broken references.

## Creation Rules

- Create the smallest viable feature structure that matches the chosen model feature.
- Do not invent business logic, API contracts, or domain data. Ask when the requested feature behavior is material and cannot be inferred.
- For UI-driven features, default to a thin parent feature that composes child features and leaf UI files directly. Do not default to a single screen-level `ui` component that receives the entire feature state and callback surface as props.
- Leave explicit placeholders only when the repository pattern clearly requires a file but the user-facing behavior is still unknown.
- Prefer imperative domain action names for feature and data-access contracts.
- Prefer a parent feature plus child features when a routed screen has prerequisite selection, setup, or gating flows before the dependent workflow can run.
- Prefer local UI state for ephemeral forms and clear it after awaited success instead of moving the field state into the feature layer.
- Wire obvious integrations after confirmation, such as exports, route registration, or thin filesystem route files.

## Reference Files

- Read [references/feature-topologies.md](references/feature-topologies.md) to compare supported layouts and choose one.
- Read [references/generic-feature-examples.md](references/generic-feature-examples.md) when you need responsibility-clear tree examples.
- Read [references/proposal-contract.md](references/proposal-contract.md) immediately before presenting the pre-edit proposal.
