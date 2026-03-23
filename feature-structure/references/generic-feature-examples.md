# Generic Feature Examples

Use these examples only for structural guidance. They are intentionally generic and contain no business logic.

## App-Local React Feature

```text
apps/web/src/features/todo/
├── data-access/
│   ├── use-todo-query-list.ts
│   └── use-todo-mutation-create.ts
├── todo-feature-detail.tsx
├── todo-feature-index.tsx
└── ui/
    ├── todo-ui-card.tsx
    └── todo-ui-list.tsx
```

Use this when the app owns both routing and rendering for the feature.

- `todo-feature-*` files are the smart layer. They read route params, call `data-access`, and pass data or callbacks into `ui`.
- `ui/*` files are the presentational layer. They render props and callbacks instead of owning fetching or route parsing.
- `data-access/*` files own query hooks, mutation hooks, adapters, or persistence code.

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
├── todo-feature-detail.tsx
└── todo-feature-index.tsx
```

Prefer route files that stay thin and import the real feature implementation.

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
