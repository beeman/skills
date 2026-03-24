# Feature Topologies

Use these patterns to choose a structure that matches the repository. Prefer repository evidence over these examples.

## Table of Contents

- [Choose by Repository Signal](#choose-by-repository-signal)
- [Common Library Types](#common-library-types)
- [Import Boundaries](#import-boundaries)
- [App-Local Feature Folders](#app-local-feature-folders)
- [Backend Feature Modules](#backend-feature-modules)
- [Package-Per-Feature](#package-per-feature)
- [Split-Platform UI Packages](#split-platform-ui-packages)
- [Thin Filesystem Routes](#thin-filesystem-routes)
- [Selection Rules](#selection-rules)

## Choose by Repository Signal

1. Use an app-local feature folder when the repo already groups product code under a single app, such as `apps/web/src/features` or `src/features`.
2. Use a package-per-feature layout when the repo already uses workspaces or package boundaries for domain code.
3. Use split-platform UI packages when the repo already separates native and web UI concerns.
4. Use backend feature modules when the repo centers on services or APIs rather than UI screens.
5. Keep filesystem routes thin when the framework uses route files as entrypoints.

## Common Library Types

Prefer at most four library types when the repository uses explicit layer packages or folders:

- `data-access`
- `feature` or `feature-<app>`
- `ui` or `ui-<app>`
- `util`

Keep existing repository naming when it already differs slightly, such as `features/` as a directory name inside a feature root.

Use `feature` as the smart or orchestration layer and `ui` as the presentational layer. Use `util` only when a pure helper layer is genuinely needed.

Treat `feature` as a composition boundary. A parent feature may consist of smaller child features when the workflow has distinct prerequisites or phases.

## Import Boundaries

- `data-access` may import from other `data-access` modules. It must not import `feature` or `ui`.
- `feature` may import from `data-access` and `ui`. Parent features should hand child features only the minimum state needed to decide what to render or run.
- `ui` may import from other `ui` modules and passive pieces from `data-access`, but not code that performs API calls, mutations, or route orchestration. Prefer granular leaf components over a single screen component when `feature` is doing real composition.
- `util` should stay pure and dependency-light. If the repository already defines stricter import rules for `util`, follow them.

## App-Local Feature Folders

Use this when one app owns the feature and the repo already keeps feature code inside the app tree.

```text
src/features/todo/
├── data-access/
├── todo-feature-index.tsx
├── todo-feature-manage.tsx
├── todo-feature-select-organization.tsx
└── ui/
```

Prefer this when:

- `src/features` or `app/src/features` already exists
- routes or screens import feature files directly
- shared UI lives elsewhere but feature UI is local

Treat `{feature}-feature-*` files as the smart layer and `ui/` as the presentational layer. Let the parent entry feature compose child features when prerequisites or workflow phases are distinct. Add `util/` only when the feature truly needs pure helpers that do not belong in `data-access`, `feature`, or `ui`. For a detailed app-local tree with split hooks and granular UI leaves, read [generic-feature-examples.md](generic-feature-examples.md).

## Backend Feature Modules

Use this when the repo is service-oriented and feature boundaries matter more than screen boundaries.

```text
src/features/payments/
├── data-access/
├── feature/
└── index.ts
```

Prefer this when:

- the feature needs no presentational layer
- the repo organizes around services, handlers, or APIs
- `ui` would be the wrong abstraction name for the code being added

Keep the same four-type model on the backend. Put side-effectful integration work in `data-access`, orchestration in `feature`, and pure helpers in `util` only when needed.

## Package-Per-Feature

Use this when the monorepo already treats packages as the main composition unit.

```text
packages/todo/data-access/
packages/todo/feature/
packages/todo/ui/
```

Prefer this when:

- the feature needs to be portable between apps
- other domains already span multiple apps
- workspaces already exist under `packages/`

Use `feature` or `feature-<app>` for orchestration and `ui` or `ui-<app>` for presentational packages when the monorepo already names layer packages explicitly.

## Split-Platform UI Packages

Use this when the repo shares non-UI logic but keeps platform-specific presentation separate.

```text
packages/todo/data-access/
packages/todo/feature/
packages/todo/ui-native/
packages/todo/ui-web/
```

Prefer this when:

- the UI cannot realistically be shared across platforms
- the data-access and orchestration layers can stay shared
- the repo already distinguishes `*-native` and `*-web`

Preserve the existing suffix pattern. If the repo uses `mobile` and `web` instead of `native` and `web`, follow that.
If orchestration also differs by app or platform, split `feature` into `feature-<app>` packages too.

## Thin Filesystem Routes

Use this when the framework uses file-based routing and route files should stay small.

```text
app/todos/page.tsx
app/todos/[id]/page.tsx
src/features/todo/
└── todo-feature-index.tsx
```

Prefer route files that only import the actual feature entry file and pass through the framework-specific parameters. Keep prerequisite handling and dependent workflow gating inside `feature`, not in the filesystem route. Read [generic-feature-examples.md](generic-feature-examples.md) for the detailed feature-internal shape.

## Selection Rules

- Follow the nearest existing feature for naming, wiring, and boundary conventions when the repo already solved the same problem elsewhere. If that example is weak or monolithic, preserve the topology signal but strengthen the composition shape.
- If two patterns exist, choose the one closest to the target app, package, or runtime.
- If the repo is inconsistent, say so in the proposal and recommend the smallest coherent option instead of pretending the structure is settled.
- If the workflow has distinct prerequisites or phases, prefer child features over a single large feature file with branching state.
- If the repo has no strong feature model, bias toward smaller composable feature files rather than a monolithic smart feature plus dumb screen split.
