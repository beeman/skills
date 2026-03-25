# Generic Feature Examples

Use these examples only for structural guidance. They are intentionally generic and contain no business logic.

## App-Local React Feature

```text
apps/web/src/features/todo/
├── data-access/
│   ├── use-todo-create.ts
│   ├── use-todo-delete.ts
│   ├── use-todo-list-query.ts
│   ├── use-todo-organizations-query.ts
│   ├── use-todo-set-active-organization.ts
│   └── use-todo-toggle.ts
├── todo-feature-active-organization.tsx
├── todo-feature-entry.tsx
├── todo-feature-organization-selection.tsx
└── ui/
    ├── todo-ui-create-form.tsx
    ├── todo-ui-list.tsx
    ├── todo-ui-list-item.tsx
    ├── todo-ui-loading.tsx
    ├── todo-ui-organization-select.tsx
    ├── todo-ui-shell.tsx
    └── todo-ui-status-message.tsx
```

Use this when the app owns both routing and rendering for the feature.

- `data-access/*` files own query hooks, mutation hooks, adapters, or persistence code. Prefer one exported thing per file, one query or mutation per hook, hook-owned invalidation and error handling, query-style names such as `use-todo-list-query.ts`, and imperative mutation names such as `use-todo-toggle.ts`. Do not introduce transport placeholders such as `use-todo-get-all.ts` unless the repository already standardizes them.
- `todo-feature-active-organization.tsx` is named after the dependent workflow it owns instead of a placeholder such as `todo-feature-manage.tsx`.
- `todo-feature-entry.tsx` acts as the parent entry feature. It checks prerequisites, branches early, and mounts `todo-feature-active-organization.tsx` only when the dependent workflow is ready.
- `todo-feature-organization-selection.tsx` acts as the prerequisite child feature. The parent passes only the minimal handoff contract, such as available organizations plus an imperative `setActiveOrganization` action.
- `ui/*` files are the presentational layer. Ephemeral draft state lives in `todo-ui-create-form.tsx`, which clears after awaited success instead of moving that field state into `feature`.
- `ui/*` stays granular. `todo-ui-list.tsx` and `todo-ui-list-item.tsx` are good names because they describe concrete leaf UI responsibilities. `todo-ui-loading.tsx`, `todo-ui-organization-select.tsx`, `todo-ui-shell.tsx`, and `todo-ui-status-message.tsx` do the same instead of collapsing back into one generic screen.

## Backend Feature Module

```text
apps/api/src/features/payments/
├── data-access/
├── feature/
└── index.ts
```

Use this when the main outputs are handlers or services instead of screens.

Treat `feature/` as the smart layer on the backend too. Keep adapters and integration work in `data-access/`, and add `util/` only when a pure helper layer is actually needed.

## Filesystem Route Wrapper

```text
app/todos/page.tsx
app/todos/[id]/page.tsx
src/features/todo/
└── todo-feature-entry.tsx
```

Prefer route files that stay thin and import the real feature implementation. Keep workflow composition inside `feature`.

## Package-Per-Feature Monorepo

```text
packages/todo/data-access/
packages/todo/feature/
packages/todo/ui/
```

Use this when the feature must be portable across apps and the monorepo already organizes code by workspace package.

## Split-Platform UI Monorepo

```text
packages/todo/data-access/
packages/todo/feature/
packages/todo/ui-native/
packages/todo/ui-web/
```

Use this when the platform-specific presentation differs but the feature logic can stay shared.

If orchestration also differs by app or platform, split `feature/` into `feature-<app>` packages too.

## Optional Util Layer

```text
src/features/payments/util/
```

Use this only for pure helpers that do not belong in `data-access`, `feature`, or `ui`. It is rare and more common on the backend than in UI-heavy features.
