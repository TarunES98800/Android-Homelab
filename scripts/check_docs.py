#!/usr/bin/env python3
"""Validate local Markdown links and fenced code blocks in this repository."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
LINK_PATTERN = re.compile(r"!?(?:\[[^\]]*\])\(([^)]+)\)")
FENCE_OPEN_PATTERN = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")


def check_fences(path: Path, text: str) -> list[str]:
    """Return errors for unclosed or mismatched Markdown code fences."""
    errors: list[str] = []
    opening: tuple[str, int, int] | None = None

    for line_number, line in enumerate(text.splitlines(), start=1):
        match = FENCE_OPEN_PATTERN.match(line)
        if not match:
            continue

        marker = match.group(1)
        marker_char = marker[0]
        marker_length = len(marker)

        if opening is None:
            opening = (marker_char, marker_length, line_number)
            continue

        open_char, open_length, open_line = opening
        if (
            marker_char == open_char
            and marker_length >= open_length
            and match.group(2).strip() == ""
        ):
            # A closing fence may contain only trailing whitespace.
            opening = None

    if opening is not None:
        marker_char, marker_length, line_number = opening
        errors.append(
            f"{path.relative_to(ROOT)}:{line_number}: "
            f"unclosed {marker_char * marker_length} code fence"
        )

    return errors


def check_links(path: Path, text: str) -> list[str]:
    """Check local Markdown links and image references."""
    errors: list[str] = []

    for match in LINK_PATTERN.finditer(text):
        raw_target = match.group(1).strip()
        if not raw_target:
            continue

        # Markdown permits an optional title after the destination.
        target = raw_target.split(maxsplit=1)[0]
        if target.startswith("<") and target.endswith(">"):
            target = target[1:-1]

        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc or not parsed.path:
            # External links and same-page anchors are outside this local check.
            continue

        relative_target = Path(unquote(parsed.path))
        resolved = (path.parent / relative_target).resolve()

        try:
            resolved.relative_to(ROOT)
        except ValueError:
            errors.append(
                f"{path.relative_to(ROOT)}: link escapes repository: {target}"
            )
            continue

        if not resolved.exists():
            line_number = text.count("\n", 0, match.start()) + 1
            errors.append(
                f"{path.relative_to(ROOT)}:{line_number}: "
                f"missing local target: {target}"
            )

    return errors


def main() -> int:
    markdown_files = sorted(ROOT.rglob("*.md"))
    all_errors: list[str] = []

    for path in markdown_files:
        content = path.read_text(encoding="utf-8")
        all_errors.extend(check_fences(path, content))
        all_errors.extend(check_links(path, content))

    if all_errors:
        print("Documentation checks failed:")
        for error in all_errors:
            print(f"- {error}")
        return 1

    print(
        f"Documentation checks passed: checked local links and fenced code "
        f"blocks in {len(markdown_files)} Markdown files."
    )
    print("Note: external URL availability and technical correctness are not checked.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
