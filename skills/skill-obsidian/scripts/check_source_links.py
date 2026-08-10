#!/usr/bin/env python3
"""Validate source URLs structurally and optionally probe them over HTTPS."""

from __future__ import annotations

import argparse
import re
import sys
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path


LINK_RE = re.compile(r"\[[^\]]+\]\((https?://[^)\s]+)\)")


def extract_urls(path: Path) -> list[str]:
    return LINK_RE.findall(path.read_text(encoding="utf-8"))


def structural_issues(urls: list[str]) -> list[str]:
    issues = [f"non-HTTPS source: {url}" for url in urls if not url.startswith("https://")]
    duplicates = sorted(url for url, count in Counter(urls).items() if count > 1)
    issues.extend(f"duplicate source: {url}" for url in duplicates)
    if not urls:
        issues.append("no Markdown source links found")
    return issues


def probe(url: str, timeout: float) -> str | None:
    headers = {"User-Agent": "skill-obsidian-source-check/1.0"}
    for method in ("HEAD", "GET"):
        request = urllib.request.Request(url, headers=headers, method=method)
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                if 200 <= response.status < 400:
                    return None
                return f"HTTP {response.status}: {url}"
        except urllib.error.HTTPError as exc:
            if method == "HEAD" and exc.code in {403, 405}:
                continue
            return f"HTTP {exc.code}: {url}"
        except (urllib.error.URLError, TimeoutError) as exc:
            return f"request failed: {url}: {exc}"
    return f"request failed: {url}"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    default = Path(__file__).resolve().parents[1] / "references" / "sources.md"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", type=Path, default=default)
    parser.add_argument("--online", action="store_true", help="probe every URL over HTTPS")
    parser.add_argument("--timeout", type=float, default=15.0, help="per-request timeout in seconds")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        urls = extract_urls(args.path)
    except (OSError, UnicodeError) as exc:
        print(f"unable to read {args.path}: {exc}", file=sys.stderr)
        return 2

    issues = structural_issues(urls)
    if args.online and not issues:
        issues.extend(result for url in urls if (result := probe(url, args.timeout)) is not None)

    if issues:
        print("\n".join(issues))
        return 1
    suffix = " and reached online" if args.online else ""
    print(f"Checked {len(urls)} unique HTTPS source link(s){suffix}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
