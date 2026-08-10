#!/usr/bin/env python3
"""Run lightweight structural checks on Obsidian Markdown files."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


FENCE_RE = re.compile(r"^( {0,3})(`{3,}|~{3,})(.*)$")
HEADING_RE = re.compile(r"^ {0,3}#{1,6}(?:\s+|$)")
LIST_RE = re.compile(r"^\s{0,3}(?:[-+*]|\d+[.)])\s+")


def add_issue(issues: list[str], path: Path, line: int, message: str) -> None:
    issues.append(f"{path}:{line}: {message}")


def check_file(path: Path) -> list[str]:
    issues: list[str] = []
    try:
        raw = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return [f"{path}: unable to read UTF-8 text: {exc}"]

    lines = raw.splitlines()
    if raw and not raw.endswith("\n"):
        add_issue(issues, path, len(lines), "missing final newline")

    body_start = 0
    if lines and lines[0] == "---":
        try:
            closing = lines.index("---", 1)
        except ValueError:
            add_issue(issues, path, 1, "frontmatter is not closed with ---")
            closing = len(lines) - 1
        body_start = closing + 1
        if body_start < len(lines) and lines[body_start].strip():
            add_issue(issues, path, body_start + 1, "add a blank line after frontmatter")

        keys: dict[str, int] = {}
        for number, line in enumerate(lines[1:closing], start=2):
            match = re.match(r"^([A-Za-z0-9_-]+):(?:\s|$)", line)
            if match:
                key = match.group(1)
                if key in keys:
                    add_issue(
                        issues,
                        path,
                        number,
                        f"duplicate top-level property {key!r}; first seen on line {keys[key]}",
                    )
                keys[key] = number

    fence: tuple[str, int, int] | None = None
    wiki_balance = 0
    comment_open = False

    for index, line in enumerate(lines, start=1):
        if index <= body_start:
            continue

        fence_match = FENCE_RE.match(line)
        if fence_match:
            marker = fence_match.group(2)
            if fence is None:
                fence = (marker[0], len(marker), index)
            elif marker[0] == fence[0] and len(marker) >= fence[1] and not fence_match.group(3).strip():
                fence = None
            continue

        if fence is not None:
            continue

        if line.endswith(" ") and not line.endswith("  "):
            add_issue(issues, path, index, "single trailing space")

        if HEADING_RE.match(line):
            if not re.search(r"#\s+\S", line):
                add_issue(issues, path, index, "heading has no text")
            if index < len(lines) and lines[index].strip():
                add_issue(issues, path, index + 1, "add a blank line after the heading")

        if LIST_RE.match(line) and index > 1:
            previous = lines[index - 2]
            previous_is_list = bool(LIST_RE.match(previous))
            previous_is_nested = bool(previous.startswith((" ", "\t")))
            previous_is_quote = previous.lstrip().startswith(">")
            if previous.strip() and not (previous_is_list or previous_is_nested or previous_is_quote):
                add_issue(issues, path, index, "add a blank line before the list")

        if "[[" in line or "]]" in line:
            wiki_balance += line.count("[[") - line.count("]]" )

        if "%%" in line:
            for _ in range(line.count("%%")):
                comment_open = not comment_open

    if fence is not None:
        add_issue(issues, path, fence[2], "fenced code block is not closed")
    if wiki_balance != 0:
        add_issue(issues, path, 1, "wikilink delimiters appear unbalanced")
    if comment_open:
        add_issue(issues, path, 1, "Obsidian comment delimiters appear unbalanced")

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path, help="Markdown files to check")
    args = parser.parse_args()

    all_issues: list[str] = []
    for path in args.paths:
        if path.suffix.lower() != ".md":
            all_issues.append(f"{path}: expected a .md file")
            continue
        all_issues.extend(check_file(path))

    if all_issues:
        print("\n".join(all_issues))
        return 1

    print(f"Checked {len(args.paths)} Markdown file(s): no structural issues found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
