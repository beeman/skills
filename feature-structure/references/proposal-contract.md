# Proposal Contract

Present this proposal before making any edit, move, scaffold, or route change.

## Required Sections

### Goal

State whether the work is a refactor, a new feature, or a mixed change.

### Inferred Topology

State the structure you plan to use and why it matches the repository.

Example:

```text
Use an app-local feature folder under src/features because the repo already groups feature code there and routes import feature entry files directly.
```

### Layering and Imports

State where the smart or orchestration layer lives, where the presentational layer lives, and which import boundaries the proposal will preserve or introduce.

Include:

- whether framework-owned route files stay as thin wrappers outside the feature tree
- whether route params stay in `feature`
- whether `ui` stays presentational
- whether any import edges must be removed to match the target boundaries

### Model Feature

Name the nearest existing feature or module you plan to copy. If no suitable model exists, say so explicitly.

### Planned Changes

List the intended adds, moves, and updates.

Include:

- files or folders to add
- files to move
- files to update for imports, exports, registration, or boundary fixes

### Wiring Changes

Call out integrations such as:

- filesystem route wrappers
- package exports
- route registration
- service registration

### Unknowns

List only material questions that cannot be inferred safely. If there are no material unknowns, say that.

### Confirmation

End with an explicit pause for approval.

Use wording equivalent to:

```text
If this structure looks right, confirm and I will apply it. If not, tell me what to change in the proposal first.
```

## Additional Rules

- Do not hide business-logic guesses inside file names or placeholders.
- Keep the proposal concrete enough that the user can approve or redirect it without rereading the repository.
- Separate confirmed facts from assumptions.
- Stop after the proposal if the user has not confirmed.
