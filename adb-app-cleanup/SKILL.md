---
description: Review and remove Android app packages with `adb` by first choosing the app class, listing numbered candidates, and uninstalling only explicit user selections. Use when the user wants to clean up either pre-installed or pre-loaded native apps such as Maps, Drive, or YouTube, or dev and test apps installed during local development.
name: adb-app-cleanup
---

# ADB App Cleanup

Review Android packages on a connected device or emulator, number the candidates for user approval, and remove only the packages the user explicitly confirms.

## Workflow

1. Run `adb devices` first.
2. If more than one device is connected and the user did not name a serial, stop and ask which device to target.
3. If the user did not specify an app class, ask them to choose one:
   - `native`, with aliases `pre-installed`, `pre-loaded`, and `preloaded`
   - `dev`, with alias `test`
4. Run `python3 ./scripts/list-app-packages.py --mode <mode>` from this skill folder.
5. In `native` mode, treat the default output as a filtered list of likely removable consumer or OEM preloads. Use `--all` only when the user wants the full system package list.
6. Present the numbered packages in alphabetical order and ask which numbers to keep or uninstall.
7. Do not uninstall anything until the user explicitly confirms the selection.
8. For `dev` mode, uninstall confirmed packages with `adb uninstall <package>`.
9. For `native` mode, uninstall confirmed packages with `adb shell pm uninstall --user 0 <package>`. Explain that this removes the package for the current user and is the common non-root approach for pre-installed apps.
10. After uninstalling, rerun `python3 ./scripts/list-app-packages.py --mode <mode>` and summarize what remains.

## Commands

- Use `python3 ./scripts/list-app-packages.py --mode dev` for locally installed development or test apps.
- Use `python3 ./scripts/list-app-packages.py --mode native` for pre-installed or pre-loaded apps. The default native view is filtered to likely removable user-facing packages.
- Use `python3 ./scripts/list-app-packages.py --mode <mode> --all` to disable mode-specific filtering heuristics.
- Use `python3 ./scripts/list-app-packages.py --mode <mode> --json` if structured output is easier to work with.
- Use `python3 ./scripts/list-app-packages.py --mode <mode> --serial <device-serial>` when the target device is known.

## Safety Rules

- In `native` mode, warn before uninstalling packages that look core to Android, especially `android` and packages starting with `com.android.`.
- Treat `native` mode as higher risk than `dev` mode. Ask for explicit reconfirmation if the user selects packages that appear device-critical.
- Never infer consent from an earlier cleanup pass. Each uninstall batch needs its own confirmation.

## Failure Handling

- If `adb devices` shows no connected devices, stop and report that no device or emulator is available.
- If the helper script reports multiple connected devices, ask the user which serial to target.
- If the helper script returns no matching packages, say that no matching packages were found instead of guessing.
- If an uninstall fails, report the package name and the exact failure, then continue only if the user wants to proceed.

## Output Rules

- Keep package lists alphabetically ordered.
- Number the candidate packages so the user can answer with keep or uninstall selections.
- Prefer package names over guessed marketing names unless the app label is known with confidence.
- Keep the app class explicit in the summary so the user knows whether they are reviewing `native` or `dev` packages.
