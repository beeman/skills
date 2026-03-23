#!/usr/bin/env python3

import argparse
import json
import re
import subprocess
import sys

LOCAL_INSTALLERS = {"", "com.android.shell", "null"}
MODE_ALIASES = {
    "dev": "dev",
    "native": "native",
    "pre-installed": "native",
    "pre-loaded": "native",
    "preloaded": "native",
    "test": "dev",
}
NATIVE_CONSUMER_EXACT = {
    "com.android.soundpicker",
    "com.android.wallpaper",
    "com.android.wallpaper.livepicker",
    "com.google.android.calendar",
    "com.google.android.contacts",
    "com.google.android.deskclock",
    "com.google.android.dialer",
    "com.google.android.documentsui",
    "com.google.android.gm",
    "com.google.android.googlequicksearchbox",
    "com.google.android.projection.gearhead",
    "com.google.android.youtube",
}
NATIVE_CONSUMER_PREFIXES = ("com.google.android.apps.",)
NATIVE_EXCLUDED_EXACT = {"android"}
NATIVE_EXCLUDED_SUBSTRINGS = (
    ".auto_generated_",
    ".cts.",
    ".overlay",
    ".rro",
    "ctsshim",
    "mainline",
    "modulemetadata",
)
PACKAGE_LINE_RE = re.compile(r"^package:(?P<package>\S+)(?:\s+installer=(?P<installer>\S+))?$")


def fail(message: str) -> "NoReturn":
    raise SystemExit(message)


def normalize_mode(raw_mode: str) -> str:
    mode = MODE_ALIASES.get(raw_mode.strip().lower())
    if not mode:
        valid_modes = ", ".join(sorted(MODE_ALIASES))
        fail(f"Unknown mode '{raw_mode}'. Valid values: {valid_modes}")
    return mode


def run_adb(serial: str | None, *args: str) -> str:
    command = ["adb"]
    if serial:
        command.extend(["-s", serial])
    command.extend(args)
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        stderr = result.stderr.strip()
        stdout = result.stdout.strip()
        fail(stderr or stdout or f"adb command failed: {' '.join(command)}")
    return result.stdout


def choose_serial(requested_serial: str | None) -> str:
    output = run_adb(None, "devices")
    devices: list[str] = []

    for raw_line in output.splitlines()[1:]:
        line = raw_line.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) >= 2 and parts[1] == "device":
            devices.append(parts[0])

    devices.sort()

    if requested_serial:
        if requested_serial not in devices:
            available = ", ".join(devices) or "none"
            fail(f"Requested serial '{requested_serial}' is not connected. Available devices: {available}")
        return requested_serial

    if not devices:
        fail("No connected adb devices found.")

    if len(devices) > 1:
        fail(f"Multiple adb devices found: {', '.join(devices)}. Rerun with --serial.")

    return devices[0]


def parse_packages(output: str, source: str) -> list[dict[str, str]]:
    packages: list[dict[str, str]] = []

    for raw_line in output.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        match = PACKAGE_LINE_RE.match(line)
        if not match:
            continue
        installer = match.group("installer") or ""
        package = match.group("package")
        packages.append(
            {
                "installer": installer,
                "package": package,
                "source": source,
            }
        )

    packages.sort(key=lambda item: item["package"])
    return packages


def filter_dev_packages(packages: list[dict[str, str]], include_all: bool) -> list[dict[str, str]]:
    if include_all:
        return packages
    return [
        package
        for package in packages
        if package["installer"].lower() in LOCAL_INSTALLERS
    ]


def is_native_candidate(package_name: str) -> bool:
    if package_name in NATIVE_EXCLUDED_EXACT:
        return False
    return not any(fragment in package_name for fragment in NATIVE_EXCLUDED_SUBSTRINGS)


def filter_native_packages(packages: list[dict[str, str]], include_all: bool) -> list[dict[str, str]]:
    if include_all:
        return packages

    filtered_packages: list[dict[str, str]] = []

    for package in packages:
        package_name = package["package"]
        if not is_native_candidate(package_name):
            continue
        if package_name in NATIVE_CONSUMER_EXACT:
            filtered_packages.append(package)
            continue
        if package_name.startswith(NATIVE_CONSUMER_PREFIXES):
            filtered_packages.append(package)
            continue
        if package_name.startswith(("android", "com.android.", "com.google.android.")):
            continue
        filtered_packages.append(package)

    return filtered_packages


def list_packages(serial: str, mode: str, include_all: bool) -> list[dict[str, str]]:
    if mode == "dev":
        output = run_adb(serial, "shell", "pm", "list", "packages", "-3", "-i")
        return filter_dev_packages(parse_packages(output, "third-party"), include_all)

    output = run_adb(serial, "shell", "pm", "list", "packages", "-s")
    return filter_native_packages(parse_packages(output, "system"), include_all)


def print_plain(packages: list[dict[str, str]], mode: str, serial: str) -> None:
    if not packages:
        print(f"No matching {mode} packages found on {serial}.")
        return

    for index, package in enumerate(packages, start=1):
        print(f"{index}. {package['package']}")
        if mode == "dev":
            installer = package["installer"] or "null"
            print(f"   installer={installer}")
        else:
            print(f"   source={package['source']}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="List numbered Android packages from adb by app class.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Disable mode-specific filtering heuristics.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON instead of plain text.",
    )
    parser.add_argument(
        "--mode",
        required=True,
        help="App class: dev, test, native, pre-installed, pre-loaded, or preloaded.",
    )
    parser.add_argument(
        "--serial",
        help="Target adb device serial.",
    )
    args = parser.parse_args()

    mode = normalize_mode(args.mode)
    serial = choose_serial(args.serial)
    packages = list_packages(serial, mode, args.all)

    if args.json:
        print(
            json.dumps(
                {
                    "mode": mode,
                    "packages": packages,
                    "serial": serial,
                },
                indent=2,
            )
        )
        return

    print_plain(packages, mode, serial)


if __name__ == "__main__":
    main()
