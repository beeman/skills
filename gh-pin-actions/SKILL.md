---
name: gh-pin-actions
description: Update and pin GitHub Actions references in repository .github YAML files. Use when Codex needs to find unique workflow or composite-action uses entries, resolve each external action to its latest stable exact SemVer tag, and rewrite uses lines to commit SHA pins with version comments like owner/repo@40-character-sha # v1.2.3.
---

# Pin GitHub Actions

## Workflow

Use the bundled script for the heavy lifting. Resolve the script path from this skill directory and pass the target repository root:

```bash
python3 scripts/pin_github_actions.py /path/to/repository
```

The script recursively scans `.github/**/*.yml` and `.github/**/*.yaml`, including `.github/workflows`, `.github/actions`, and nested directories. It updates only external GitHub action references shaped like `owner/repo[/path]@ref`; it skips local actions such as `./.github/actions/foo` and Docker actions such as `docker://...`.

## Operating Rules

- Let the script discover unique actions, fetch latest stable exact SemVer tags, resolve tags to commit SHAs, and rewrite files in one pass.
- Run the script from the skill directory, or use the discovered skill directory path, and pass the repository root, `.github` directory, or specific YAML file as the target.
- Use `--dry-run` first when the user asked to preview changes or when the repository is sensitive.
- Use `GITHUB_TOKEN` in the environment when available to avoid GitHub API rate limits.
- Review the diff after the script runs. The expected final line format is:

```yaml
uses: actions/setup-node@48b55a011bda9f5d6aeb4c2d9c7362e8dae4041e # v6.4.0
```

## Useful Commands

Preview changes:

```bash
python3 scripts/pin_github_actions.py /path/to/repository --dry-run
```

Allow prerelease tags when explicitly requested:

```bash
python3 scripts/pin_github_actions.py /path/to/repository --include-prereleases
```

Check whether files are already pinned without writing:

```bash
python3 scripts/pin_github_actions.py /path/to/repository --check
```

## Failure Handling

- If a repository has no stable exact SemVer tag, stop and report the action name; do not invent a version.
- If GitHub API access fails, rerun with network permission or `GITHUB_TOKEN`.
- If a `uses:` line has an unusual YAML shape the script skips, inspect it manually and keep the final `uses: <action-name>@<hash> # <tag>` format.
