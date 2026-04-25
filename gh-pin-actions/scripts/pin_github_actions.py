#!/usr/bin/env python3
"""Update GitHub Actions uses references to latest stable SemVer SHA pins."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any


USES_RE = re.compile(
    r"^(?P<prefix>\s*(?:-\s*)?uses\s*:\s*)"
    r"(?P<quote>['\"]?)"
    r"(?P<value>[^'\"\s#]+)"
    r"(?P=quote)"
    r"(?P<suffix>[ \t]*(?:#.*)?)"
    r"(?P<newline>\r?\n?)$"
)
SEMVER_RE = re.compile(
    r"^v?"
    r"(?P<major>0|[1-9]\d*)\."
    r"(?P<minor>0|[1-9]\d*)\."
    r"(?P<patch>0|[1-9]\d*)"
    r"(?P<suffix>(?:[-+].*)?)$"
)
SHA_RE = re.compile(r"^[0-9a-f]{40}$", re.IGNORECASE)


@dataclass(frozen=True)
class ActionRef:
    action_path: str
    file: Path
    line_number: int
    prefix: str
    quote: str
    ref: str
    repo_key: str
    suffix: str
    value: str


@dataclass(frozen=True)
class ResolvedAction:
    repo_key: str
    sha: str
    tag: str


class GitHubApi:
    def __init__(self, api_url: str, token: str | None) -> None:
        self.api_url = api_url.rstrip("/")
        self.token = token

    def get_json(self, path_or_url: str) -> Any:
        if path_or_url.startswith("https://") or path_or_url.startswith("http://"):
            url = path_or_url
        else:
            url = f"{self.api_url}/{path_or_url.lstrip('/')}"

        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "gh-pin-actions-skill",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        request = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as error:
            body = error.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"GitHub API {error.code} for {url}: {body}") from error
        except urllib.error.URLError as error:
            raise RuntimeError(f"GitHub API request failed for {url}: {error}") from error


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Scan .github YAML files, update external GitHub Actions to the "
            "latest stable exact SemVer tag, and pin uses lines to the tag SHA."
        )
    )
    parser.add_argument(
        "targets",
        nargs="*",
        default=["."],
        help="Repository roots, .github directories, YAML files, or directories to scan.",
    )
    parser.add_argument(
        "--api-url",
        default="https://api.github.com",
        help="GitHub API base URL.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit with status 1 if changes would be made. Does not write files.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned updates without writing files.",
    )
    parser.add_argument(
        "--github-token-env",
        default="GITHUB_TOKEN",
        help="Environment variable containing a GitHub API token.",
    )
    parser.add_argument(
        "--include-prereleases",
        action="store_true",
        help="Allow SemVer prerelease or build-metadata tags.",
    )
    parser.add_argument(
        "--max-tag-pages",
        type=int,
        default=10,
        help="Maximum 100-tag pages to inspect per repository.",
    )
    return parser.parse_args()


def yaml_files_for_target(target: Path) -> list[Path]:
    target = target.resolve()
    if target.is_file():
        return [target] if target.suffix.lower() in {".yaml", ".yml"} else []

    scan_root = target / ".github" if (target / ".github").is_dir() else target
    if not scan_root.is_dir():
        return []

    return sorted(
        path
        for path in scan_root.rglob("*")
        if path.is_file() and path.suffix.lower() in {".yaml", ".yml"}
    )


def discover_yaml_files(targets: list[str]) -> list[Path]:
    files: dict[str, Path] = {}
    for raw_target in targets:
        for path in yaml_files_for_target(Path(raw_target)):
            files[str(path)] = path
    return [files[key] for key in sorted(files)]


def parse_uses_line(file: Path, line: str, line_number: int) -> ActionRef | None:
    match = USES_RE.match(line)
    if not match:
        return None

    value = match.group("value")
    if "@" not in value:
        return None

    action_path, ref = value.rsplit("@", 1)
    if (
        action_path.startswith("./")
        or action_path.startswith("../")
        or action_path.startswith("/")
        or action_path.startswith("docker://")
    ):
        return None

    parts = action_path.split("/")
    if len(parts) < 2 or not parts[0] or not parts[1]:
        return None

    repo_key = f"{parts[0]}/{parts[1]}".lower()
    return ActionRef(
        action_path=action_path,
        file=file,
        line_number=line_number,
        prefix=match.group("prefix"),
        quote=match.group("quote"),
        ref=ref,
        repo_key=repo_key,
        suffix=match.group("suffix"),
        value=value,
    )


def discover_action_refs(files: list[Path]) -> list[ActionRef]:
    refs: list[ActionRef] = []
    for file in files:
        lines = file.read_text(encoding="utf-8").splitlines(keepends=True)
        for line_number, line in enumerate(lines, start=1):
            action_ref = parse_uses_line(file, line, line_number)
            if action_ref:
                refs.append(action_ref)
    return sorted(refs, key=lambda ref: (str(ref.file), ref.line_number, ref.action_path.lower()))


def prerelease_key(suffix: str) -> tuple[tuple[int, int | str], ...]:
    if not suffix.startswith("-"):
        return ()

    prerelease = suffix[1:].split("+", 1)[0]
    identifiers: list[tuple[int, int | str]] = []
    for identifier in prerelease.split("."):
        if identifier.isdecimal():
            identifiers.append((0, int(identifier)))
        else:
            identifiers.append((1, identifier))
    return tuple(identifiers)


def parse_semver(tag: str, include_prereleases: bool) -> tuple[Any, ...] | None:
    match = SEMVER_RE.match(tag)
    if not match:
        return None

    suffix = match.group("suffix")
    if suffix and not include_prereleases:
        return None
    is_prerelease = suffix.startswith("-")

    return (
        int(match.group("major")),
        int(match.group("minor")),
        int(match.group("patch")),
        0 if is_prerelease else 1,
        prerelease_key(suffix),
        1 if tag.startswith("v") else 0,
        tag,
    )


def latest_semver_tag(
    api: GitHubApi,
    repo_key: str,
    include_prereleases: bool,
    max_tag_pages: int,
) -> str:
    candidates: list[tuple[tuple[Any, ...], str]] = []
    owner_repo = urllib.parse.quote(repo_key, safe="/")

    for page in range(1, max_tag_pages + 1):
        tags = api.get_json(f"/repos/{owner_repo}/tags?per_page=100&page={page}")
        if not isinstance(tags, list):
            raise RuntimeError(f"Unexpected tag response for {repo_key}")
        if not tags:
            break

        for tag in tags:
            name = tag.get("name") if isinstance(tag, dict) else None
            if not isinstance(name, str):
                continue
            parsed = parse_semver(name, include_prereleases)
            if parsed:
                candidates.append((parsed, name))

        if len(tags) < 100:
            break

    if not candidates:
        exact = "stable exact SemVer"
        if include_prereleases:
            exact = "exact SemVer"
        raise RuntimeError(f"No {exact} tag found for {repo_key}")

    candidates.sort(key=lambda item: item[0])
    return candidates[-1][1]


def resolve_tag_sha(api: GitHubApi, repo_key: str, tag: str) -> str:
    owner_repo = urllib.parse.quote(repo_key, safe="/")
    encoded_tag = urllib.parse.quote(tag, safe="")
    ref = api.get_json(f"/repos/{owner_repo}/git/ref/tags/{encoded_tag}")
    if not isinstance(ref, dict) or not isinstance(ref.get("object"), dict):
        raise RuntimeError(f"Unexpected ref response for {repo_key}@{tag}")

    obj = ref["object"]
    seen: set[str] = set()
    while isinstance(obj, dict) and obj.get("type") == "tag":
        url = obj.get("url")
        if not isinstance(url, str) or url in seen:
            raise RuntimeError(f"Could not dereference annotated tag for {repo_key}@{tag}")
        seen.add(url)
        tag_obj = api.get_json(url)
        if not isinstance(tag_obj, dict) or not isinstance(tag_obj.get("object"), dict):
            raise RuntimeError(f"Unexpected tag object response for {repo_key}@{tag}")
        obj = tag_obj["object"]

    sha = obj.get("sha") if isinstance(obj, dict) else None
    if not isinstance(sha, str) or not SHA_RE.match(sha):
        raise RuntimeError(f"Could not resolve commit SHA for {repo_key}@{tag}")
    return sha


def resolve_actions(
    refs: list[ActionRef],
    api: GitHubApi,
    include_prereleases: bool,
    max_tag_pages: int,
) -> dict[str, ResolvedAction]:
    resolved: dict[str, ResolvedAction] = {}
    for repo_key in sorted({ref.repo_key for ref in refs}):
        tag = latest_semver_tag(api, repo_key, include_prereleases, max_tag_pages)
        sha = resolve_tag_sha(api, repo_key, tag)
        resolved[repo_key] = ResolvedAction(repo_key=repo_key, sha=sha, tag=tag)
    return resolved


def uses_comment(tag: str, suffix: str) -> str:
    tag_comment = f"# {tag}"
    existing = suffix.strip()
    if not existing:
        return tag_comment

    comment_text = existing.removeprefix("#").strip()
    if not comment_text:
        return tag_comment

    comment_parts = comment_text.split(maxsplit=1)
    if SEMVER_RE.match(comment_parts[0]):
        if len(comment_parts) == 1:
            return tag_comment
        return f"{tag_comment} {comment_parts[1]}"

    return f"{tag_comment} {comment_text}"


def rewrite_file(file: Path, resolved: dict[str, ResolvedAction], write: bool) -> int:
    lines = file.read_text(encoding="utf-8").splitlines(keepends=True)
    changed = 0
    new_lines: list[str] = []

    for line_number, line in enumerate(lines, start=1):
        action_ref = parse_uses_line(file, line, line_number)
        if not action_ref:
            new_lines.append(line)
            continue

        resolved_action = resolved[action_ref.repo_key]
        new_value = f"{action_ref.action_path}@{resolved_action.sha}"
        newline = "\n" if line.endswith("\n") else ""
        if line.endswith("\r\n"):
            newline = "\r\n"
        comment = uses_comment(resolved_action.tag, action_ref.suffix)
        new_line = (
            f"{action_ref.prefix}{action_ref.quote}{new_value}{action_ref.quote}"
            f" {comment}{newline}"
        )
        if new_line != line:
            changed += 1
        new_lines.append(new_line)

    if changed and write:
        file.write_text("".join(new_lines), encoding="utf-8")
    return changed


def print_summary(
    refs: list[ActionRef],
    resolved: dict[str, ResolvedAction],
    changed_by_file: dict[Path, int],
    dry_run: bool,
) -> None:
    action_paths = sorted({ref.action_path for ref in refs}, key=str.lower)
    print(f"Found {len(action_paths)} unique action uses in {len({ref.file for ref in refs})} files.")

    if action_paths:
        print("\nActions:")
        for action_path in action_paths:
            repo_key = "/".join(action_path.split("/")[:2]).lower()
            resolved_action = resolved[repo_key]
            print(f"  {action_path} -> {resolved_action.tag} @ {resolved_action.sha}")

    total_changed = sum(changed_by_file.values())
    label = "Would update" if dry_run else "Updated"
    print(f"\n{label} {total_changed} uses lines across {len(changed_by_file)} files.")
    for file in sorted(changed_by_file):
        print(f"  {file}: {changed_by_file[file]}")


def main() -> int:
    args = parse_args()
    write = not args.dry_run and not args.check
    token = os.environ.get(args.github_token_env)
    api = GitHubApi(args.api_url, token)

    files = discover_yaml_files(args.targets)
    if not files:
        print("No .github YAML files found.", file=sys.stderr)
        return 1

    refs = discover_action_refs(files)
    if not refs:
        print("No external GitHub action uses references found.")
        return 0

    try:
        resolved = resolve_actions(
            refs=refs,
            api=api,
            include_prereleases=args.include_prereleases,
            max_tag_pages=args.max_tag_pages,
        )
    except RuntimeError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    changed_by_file: dict[Path, int] = {}
    for file in files:
        changed = rewrite_file(file, resolved, write=write)
        if changed:
            changed_by_file[file] = changed

    print_summary(refs, resolved, changed_by_file, dry_run=not write)

    if args.check and changed_by_file:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
