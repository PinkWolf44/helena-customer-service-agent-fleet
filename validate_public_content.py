#!/usr/bin/env python3
"""Small public-repository safety check using only the Python standard library."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {
    ".md",
    ".mmd",
    ".py",
    ".yml",
    ".yaml",
    ".txt",
    ".js",
    ".json",
    ".html",
    ".gs",
}
SKIP_DIRS = {".git", "__pycache__", "private", "raw-evidence"}

PATTERNS = {
    "absolute user path": re.compile(r"(?:/" r"Users/|/" r"home/)[^\s`]+"),
    "workspace token": re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"),
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "generic API secret": re.compile(
        r"(?i)\b(?:api[_-]?key|client[_-]?secret|access[_-]?token)\b\s*[:=]\s*['\"][^'\"]{8,}['\"]"
    ),
    "webhook URL": re.compile(r"https://[^\s`]+/(?:webhook|hooks)/[^\s`)]+", re.IGNORECASE),
    "non-example email": re.compile(
        r"\b[A-Z0-9._%+-]+@(?!example\.(?:com|org)\b)[A-Z0-9.-]+\.[A-Z]{2,}\b",
        re.IGNORECASE,
    ),
}

REQUIRED = [
    ROOT / "README.md",
    ROOT / "examples/SOUL.sample.md",
    ROOT / "examples/BASELINE.sample.md",
    ROOT / "examples/HEALTH_CARD.sample.md",
    ROOT / "examples/STABILITY_PROTOCOL.sample.md",
]


def iter_text_files() -> list[Path]:
    return [
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and path.suffix.lower() in TEXT_SUFFIXES
        and not any(part in SKIP_DIRS for part in path.parts)
    ]


def load_private_terms() -> list[str]:
    blocklist = ROOT / ".private-blocklist"
    if not blocklist.exists():
        return []
    return [
        line.strip()
        for line in blocklist.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def main() -> int:
    failures: list[str] = []

    for required in REQUIRED:
        if not required.is_file():
            failures.append(f"missing required file: {required.relative_to(ROOT)}")

    private_terms = load_private_terms()
    for path in iter_text_files():
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(ROOT)
        for label, pattern in PATTERNS.items():
            if pattern.search(text):
                failures.append(f"{relative}: possible {label}")
        lowered = text.casefold()
        for term in private_terms:
            if term.casefold() in lowered:
                failures.append(f"{relative}: private blocklist term found")

    if failures:
        print("Public-content validation failed:")
        for failure in sorted(set(failures)):
            print(f"- {failure}")
        return 1

    print("Public-content validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
