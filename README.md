# skills

Reusable agent skills published from `beeman/skills`.

## Available Skills

- `gh-issue-kickoff`: Start work on a GitHub issue with a readiness gate and execution-ready plan.
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
npx skills add -g beeman/skills --skill gh-issue-kickoff
npx skills add -g beeman/skills --skill gh-pr-review-comments
```

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
npx skills remove -g gh-issue-kickoff
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
