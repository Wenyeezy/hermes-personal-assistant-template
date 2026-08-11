#!/usr/bin/env python3
"""Scan Git-tracked public files for common secret and private-path leaks."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SUSPICIOUS_NAMES = re.compile(
    r"(^|/)(\.env($|\.)|.*\.(?:key|pem|p12|token|log|sqlite|db)$|"
    r"(?:secrets?|sessions?|real-memory|private)/)",
    re.IGNORECASE,
)
CONTENT_PATTERNS = {
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "GitHub token": re.compile(r"\b(?:ghp|github_pat)_[A-Za-z0-9_]{20,}\b"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "Slack token": re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"),
    "OpenAI-style secret": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "macOS private path": re.compile(r"/Users/[^/\s`]+/"),
    "Linux private path": re.compile(r"/home/[^/\s`]+/"),
    "Windows private path": re.compile(r"[A-Za-z]:\\Users\\[^\\\s`]+\\"),
    "email address": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
}
FALLBACK_EXCLUDED_PARTS = {
    ".git",
    ".hermes",
    ".idea",
    ".vscode",
    "__pycache__",
    "cache",
    "logs",
    "private",
    "real-memory",
    "sessions",
}


def tracked_files() -> list[Path]:
    try:
        result = subprocess.run(
            ["git", "ls-files", "-co", "--exclude-standard"],
            cwd=REPO_ROOT,
            check=True,
            text=True,
            capture_output=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        # GitHub ZIP downloads do not include .git. Scan the public tree while
        # preserving the same private/generated boundaries as .gitignore.
        return sorted(
            path
            for path in REPO_ROOT.rglob("*")
            if path.is_file()
            and not FALLBACK_EXCLUDED_PARTS.intersection(path.relative_to(REPO_ROOT).parts)
            and path.name not in {".DS_Store", "Thumbs.db"}
            and path.suffix not in {".pyc", ".tmp", ".bak"}
        )
    return [REPO_ROOT / line for line in result.stdout.splitlines() if line]


def main() -> int:
    findings: list[str] = []
    for path in tracked_files():
        relative = path.relative_to(REPO_ROOT).as_posix()
        # This scanner necessarily contains literal examples of the patterns it
        # detects. Test its behavior separately instead of flagging its source.
        if relative == "scripts/privacy_check.py":
            continue
        if SUSPICIOUS_NAMES.search(relative):
            findings.append(f"suspicious public filename: {relative}")
            continue
        try:
            data = path.read_bytes()
        except OSError as exc:
            findings.append(f"unreadable file: {relative}: {exc}")
            continue
        if b"\x00" in data:
            continue
        text = data.decode("utf-8", errors="replace")
        for label, pattern in CONTENT_PATTERNS.items():
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                findings.append(f"{label}: {relative}:{line}")

    if findings:
        print("Privacy check failed:", file=sys.stderr)
        for finding in sorted(set(findings)):
            print(f"- {finding}", file=sys.stderr)
        return 1
    print("Privacy check passed: no common secret, identity, or private-path leaks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
