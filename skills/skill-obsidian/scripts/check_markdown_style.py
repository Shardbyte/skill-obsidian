#!/usr/bin/env python3
"""Check Obsidian Markdown for structural errors and reviewable style issues."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

try:
    import yaml
except ImportError:  # Report a useful CLI error instead of a traceback.
    yaml = None


FENCE_RE = re.compile(r"^(?: {0,3}> ?)*( {0,3})(`{3,}|~{3,})(.*)$")
HEADING_RE = re.compile(r"^ {0,3}#{1,6}(?:\s+|$)")
LIST_RE = re.compile(r"^\s{0,3}(?:[-+*]|\d+[.)])\s+")


@dataclass(frozen=True)
class Issue:
    path: str
    line: int
    severity: str
    code: str
    message: str


if yaml is not None:
    class UniqueKeyLoader(yaml.SafeLoader):
        """Safe YAML loader that rejects duplicate mapping keys."""


    def construct_unique_mapping(loader, node, deep=False):
        mapping = {}
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node, deep=deep)
            try:
                duplicate = key in mapping
            except TypeError as exc:
                raise yaml.constructor.ConstructorError(
                    "while constructing a mapping",
                    node.start_mark,
                    "found an unhashable key",
                    key_node.start_mark,
                ) from exc
            if duplicate:
                raise yaml.constructor.ConstructorError(
                    "while constructing a mapping",
                    node.start_mark,
                    f"found duplicate key {key!r}",
                    key_node.start_mark,
                )
            mapping[key] = loader.construct_object(value_node, deep=deep)
        return mapping


    UniqueKeyLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_unique_mapping,
    )


def issue(path: Path, line: int, severity: str, code: str, message: str) -> Issue:
    return Issue(str(path), max(1, line), severity, code, message)


def yaml_error_line(exc: Exception, offset: int = 1) -> int:
    mark = getattr(exc, "problem_mark", None)
    return offset + (mark.line if mark is not None else 0)


def check_frontmatter(path: Path, lines: list[str]) -> tuple[list[Issue], int]:
    issues: list[Issue] = []
    if not lines or lines[0] != "---":
        return issues, 0

    try:
        closing = lines.index("---", 1)
    except ValueError:
        issues.append(issue(path, 1, "error", "frontmatter-unclosed", "frontmatter is not closed with ---"))
        return issues, len(lines)

    if yaml is None:
        issues.append(
            issue(
                path,
                1,
                "error",
                "dependency-missing",
                "PyYAML is required; install scripts/requirements.txt",
            )
        )
    else:
        source = "\n".join(lines[1:closing])
        try:
            parsed = yaml.load(source, Loader=UniqueKeyLoader) if source.strip() else {}
            if parsed is not None and not isinstance(parsed, dict):
                issues.append(issue(path, 2, "error", "frontmatter-type", "frontmatter must be a YAML mapping"))
        except yaml.YAMLError as exc:
            problem = getattr(exc, "problem", None) or str(exc).splitlines()[0]
            issues.append(
                issue(path, yaml_error_line(exc), "error", "frontmatter-yaml", f"invalid YAML: {problem}")
            )

    body_start = closing + 1
    if body_start < len(lines) and lines[body_start].strip():
        issues.append(
            issue(path, body_start + 1, "warning", "frontmatter-spacing", "add a blank line after frontmatter")
        )
    return issues, body_start


def mask_inline_code(line: str) -> str:
    """Mask complete backtick spans while leaving unmatched runs visible."""
    chars = list(line)
    index = 0
    while index < len(line):
        if line[index] == "\\":
            chars[index] = " "
            if index + 1 < len(line):
                chars[index + 1] = " "
            index += 2
            continue
        if line[index] != "`":
            index += 1
            continue
        end_run = index
        while end_run < len(line) and line[end_run] == "`":
            end_run += 1
        marker = line[index:end_run]
        closing = line.find(marker, end_run)
        if closing == -1:
            index = end_run
            continue
        for position in range(index, closing + len(marker)):
            chars[position] = " "
        index = closing + len(marker)
    return "".join(chars)


def mask_comments(line: str, comment_open: bool) -> tuple[str, bool]:
    chars = list(line)
    index = 0
    while index < len(line):
        if line.startswith("%%", index):
            chars[index] = chars[index + 1] = " "
            comment_open = not comment_open
            index += 2
            continue
        if comment_open:
            chars[index] = " "
        index += 1
    return "".join(chars), comment_open


def check_file(path: Path) -> list[Issue]:
    issues: list[Issue] = []
    try:
        raw = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return [issue(path, 1, "error", "read-failed", f"unable to read UTF-8 text: {exc}")]

    if raw.startswith("\ufeff"):
        issues.append(issue(path, 1, "error", "bom", "remove the UTF-8 byte-order mark before frontmatter"))
        raw = raw.removeprefix("\ufeff")

    lines = raw.splitlines()
    if raw and not raw.endswith("\n"):
        issues.append(issue(path, len(lines), "warning", "final-newline", "missing final newline"))

    if lines and lines[0] != "---":
        first_content = next((number for number, line in enumerate(lines, start=1) if line.strip()), None)
        if first_content is not None and lines[first_content - 1] == "---":
            issues.append(
                issue(
                    path,
                    first_content,
                    "error",
                    "frontmatter-position",
                    "frontmatter must begin at the first byte of the file",
                )
            )

    frontmatter_issues, body_start = check_frontmatter(path, lines)
    issues.extend(frontmatter_issues)

    fence: tuple[str, int, int] | None = None
    wiki_balance = 0
    comment_open = False
    comment_start = 1

    for index, line in enumerate(lines, start=1):
        if index <= body_start:
            continue

        if fence is not None:
            fence_match = FENCE_RE.match(line)
            if fence_match:
                marker = fence_match.group(2)
                trailer = fence_match.group(3).strip()
                if marker[0] == fence[0] and len(marker) >= fence[1] and not trailer:
                    fence = None
            continue

        visible = mask_inline_code(line)
        was_comment_open = comment_open
        visible, comment_open = mask_comments(visible, comment_open)
        if not was_comment_open and comment_open:
            comment_start = index

        fence_match = FENCE_RE.match(visible)
        if fence_match:
            marker = fence_match.group(2)
            fence = (marker[0], len(marker), index)
            continue

        if line.endswith(" ") and not line.endswith("  "):
            issues.append(issue(path, index, "warning", "trailing-space", "single trailing space"))

        if HEADING_RE.match(visible):
            if not re.search(r"#\s+\S", visible):
                issues.append(issue(path, index, "error", "heading-empty", "heading has no text"))
            if index < len(lines) and lines[index].strip():
                issues.append(
                    issue(path, index + 1, "warning", "heading-spacing", "add a blank line after the heading")
                )

        if LIST_RE.match(visible) and index > 1:
            previous = lines[index - 2]
            previous_is_list = bool(LIST_RE.match(previous))
            previous_is_indented = bool(previous.startswith((" ", "\t")))
            previous_is_quote = previous.lstrip().startswith(">")
            if previous.strip() and not (previous_is_list or previous_is_indented or previous_is_quote):
                issues.append(
                    issue(path, index, "warning", "list-spacing", "add a blank line before the list")
                )

        wiki_balance += visible.count("[[") - visible.count("]]" )

    if fence is not None:
        issues.append(issue(path, fence[2], "error", "fence-unclosed", "fenced code block is not closed"))
    if wiki_balance != 0:
        issues.append(issue(path, 1, "error", "wikilink-unbalanced", "wikilink delimiters appear unbalanced"))
    if comment_open:
        issues.append(
            issue(path, comment_start, "error", "comment-unclosed", "Obsidian comment delimiters are unbalanced")
        )
    return issues


def expand_paths(paths: Iterable[Path]) -> tuple[list[Path], list[Issue]]:
    files: set[Path] = set()
    issues: list[Issue] = []
    for path in paths:
        if not path.exists():
            issues.append(issue(path, 1, "error", "path-missing", "path does not exist"))
        elif path.is_dir():
            files.update(candidate for candidate in path.rglob("*.md") if candidate.is_file())
        elif path.is_file() and path.suffix.lower() == ".md":
            files.add(path)
        else:
            issues.append(issue(path, 1, "error", "path-type", "expected a Markdown file or directory"))
    return sorted(files, key=lambda item: str(item)), issues


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path, help="Markdown files or directories to check")
    parser.add_argument("--format", choices=("text", "json"), default="text", dest="output_format")
    parser.add_argument("--errors-only", action="store_true", help="suppress warnings and fail only on errors")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    files, all_issues = expand_paths(args.paths)
    for path in files:
        all_issues.extend(check_file(path))

    visible = [item for item in all_issues if not args.errors_only or item.severity == "error"]
    visible.sort(key=lambda item: (item.path, item.line, item.severity, item.code))
    errors = sum(item.severity == "error" for item in visible)
    warnings = sum(item.severity == "warning" for item in visible)

    if args.output_format == "json":
        print(
            json.dumps(
                {
                    "files_checked": len(files),
                    "errors": errors,
                    "warnings": warnings,
                    "issues": [asdict(item) for item in visible],
                },
                indent=2,
            )
        )
    else:
        for item in visible:
            print(f"{item.path}:{item.line}: {item.severity}: {item.code}: {item.message}")
        print(f"Checked {len(files)} Markdown file(s): {errors} error(s), {warnings} warning(s).")

    return 1 if visible else 0


if __name__ == "__main__":
    sys.exit(main())
