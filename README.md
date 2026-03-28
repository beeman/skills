# skills

Reusable agent skills published from `beeman/skills`.

## Available Skills

- `gh-commit`: Prepare or amend a clean local commit without pushing or opening a PR.
- `gh-issue-kickoff`: Start work on a GitHub issue with a readiness gate and execution-ready plan.
- `gh-plan-review`: Review and pressure-test a GitHub issue, PR, or branch implementation plan before coding.
- `gh-pr-create`: Requires `gh-commit`, then previews the exact PR title and body, pushes, and requires explicit confirmation before opening a GitHub PR.
- `gh-pr-rebase`: Rebase a PR branch onto the latest default-branch history and resolve conflicts safely.
- `gh-pr-review-comments`: Handle GitHub PR review comments on an existing feature branch.

## Use This Repository With `skills`

Preview the skills in this repository before installing anything:

```bash
npx skills add -g beeman/skills --list
```

Install this repository globally:

```bash
npx skills add -g beeman/skills
```

Install a single skill instead of everything in the repository:

```bash
npx skills add -g beeman/skills --skill gh-commit
npx skills add -g beeman/skills --skill gh-issue-kickoff
npx skills add -g beeman/skills --skill gh-plan-review
npx skills add -g beeman/skills --skill gh-pr-create
npx skills add -g beeman/skills --skill gh-pr-rebase
npx skills add -g beeman/skills --skill gh-pr-review-comments
```

`gh-pr-create` requires `gh-commit`. When installing skills individually, install both or `gh-pr-create` will stop and ask how to handle branch and commit preparation before creating the PR.

Install for specific agents only:

```bash
npx skills add -g beeman/skills --agent claude-code cursor
```

Check what is installed globally:

```bash
npx skills ls -g
```

Remove a specific skill:

```bash
npx skills remove -g gh-commit
npx skills remove -g gh-issue-kickoff
npx skills remove -g gh-plan-review
npx skills remove -g gh-pr-create
npx skills remove -g gh-pr-rebase
npx skills remove -g gh-pr-review-comments
```

Remove skills interactively:

```bash
npx skills remove -g
```

## Keep Skills Up To Date

Check for updates:

```bash
npx skills check
```

Update installed skills:

```bash
npx skills update
```

## Credits

The review structure for `gh-plan-review` and parts of the GitHub planning workflow in this repo were informed by [garrytan/gstack](https://github.com/garrytan/gstack), especially the [`plan-eng-review`](https://github.com/garrytan/gstack/blob/main/plan-eng-review/SKILL.md) and [`plan-design-review`](https://github.com/garrytan/gstack/blob/main/plan-design-review/SKILL.md) skills.
