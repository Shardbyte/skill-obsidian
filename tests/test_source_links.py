from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "skill-obsidian" / "scripts" / "check_source_links.py"
SOURCES = ROOT / "skills" / "skill-obsidian" / "references" / "sources.md"
SPEC = importlib.util.spec_from_file_location("check_source_links", SCRIPT)
LINK_CHECKER = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = LINK_CHECKER
SPEC.loader.exec_module(LINK_CHECKER)


class SourceLinkTests(unittest.TestCase):
    def test_sources_are_unique_https_links(self) -> None:
        urls = LINK_CHECKER.extract_urls(SOURCES)
        self.assertGreaterEqual(len(urls), 25)
        self.assertEqual(LINK_CHECKER.structural_issues(urls), [])


if __name__ == "__main__":
    unittest.main()
