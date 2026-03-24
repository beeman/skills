# Proposal Contract

Present this proposal before making any edit, move, scaffold, or route change.

## Table of Contents

- [Required Sections](#required-sections)
- [Goal](#goal)
- [Inferred Topology](#inferred-topology)
- [Feature Composition](#feature-composition)
- [Data-Access Contract](#data-access-contract)
- [Layering and Imports](#layering-and-imports)
- [UI Composition](#ui-composition)
- [Model Feature](#model-feature)
- [Planned Changes](#planned-changes)
- [Wiring Changes](#wiring-changes)
- [Unknowns](#unknowns)
- [Leftovers](#leftovers)
- [Confirmation](#confirmation)
- [Additional Rules](#additional-rules)

## Required Sections

### Goal

State whether the work is a refactor, a new feature, or a mixed change.

### Inferred Topology

State the structure you plan to use and why it matches the repository.

Example:

```text
Use an app-local feature folder under src/features because the repo already groups feature code there and routes import feature entry files directly.
```

### Feature Composition

State whether the workflow has distinct prerequisite or dependent phases and whether those phases should become separate child features.

Include:

- which feature owns gating and which child feature is conditionally mounted
- how dependent features are gated until prerequisites are satisfied
- the minimum state or props handed from parent features to child features
- which file acts as the parent entry feature and which files act as child features

### Data-Access Contract

State the query and mutation split you plan to use.

Include:

- whether async callers need an awaited contract such as `mutateAsync`
- where mutation error handling, invalidation, and side effects live
- which hooks or modules will exist and which single responsibility each one owns
- which imperative domain actions the feature or hooks will expose
- why aggregate management hooks are avoided or, if retained, why they are required

### Layering and Imports

State where the smart or orchestration layer lives, where the presentational layer lives, and which import boundaries the proposal will preserve or introduce.

Include:

- whether any import edges must be removed to match the target boundaries
- whether framework-owned route files stay as thin wrappers outside the feature tree
- whether route params stay in `feature`
- whether `ui` stays presentational

### UI Composition

State how the presentational layer will be split.

Include:

- how the UI reacts to async success without empty catch wrappers
- where ephemeral form or input state lives
- which UI responsibilities stay in leaf components versus `feature`
- whether any large screen component will be broken into smaller leaves

### Model Feature

Name the nearest existing feature or module you plan to copy. If no suitable model exists, say so explicitly.

### Planned Changes

List the intended adds, moves, and updates.

Include:

- files or folders to add
- files to move
- files to update for imports, exports, registration, or boundary fixes
- whether large branching feature files or screen components will be split into smaller feature or `ui` files

### Wiring Changes

Call out integrations such as:

- filesystem route wrappers
- package exports
- route registration
- service registration

### Unknowns

List only material questions that cannot be inferred safely. If there are no material unknowns, say that.

### Leftovers

Call out any monolithic behavior or structure that will intentionally remain.

Include:

- any large hook or screen component not being split
- any parent-level gating that still lives inside a child
- why each leftover is being kept for this change

### Confirmation

End with an explicit pause for approval.

Use wording equivalent to:

```text
If this structure looks right, confirm and I will apply it. If not, tell me what to change in the proposal first.
```

## Additional Rules

- Do not hide business-logic guesses inside file names or placeholders.
- Keep the proposal concrete enough that the user can approve or redirect it without rereading the repository.
- Keep the proposal explicit about data-access hook granularity, imperative action names, and UI-local ephemeral state.
- Keep the proposal explicit about parent and child feature boundaries instead of describing the result as one smart feature plus one screen.
- Treat weak local examples as naming or wiring references, not proof that a monolithic structure is acceptable.
- Prefer early-return composition language over describing long `else if` chains as the intended outcome.
- Separate confirmed facts from assumptions.
- Stop after the proposal if the user has not confirmed.
