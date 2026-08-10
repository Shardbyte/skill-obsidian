from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "skill-obsidian" / "scripts" / "check_markdown_style.py"
SPEC = importlib.util.spec_from_file_location("check_markdown_style", SCRIPT)
CHECKER = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = CHECKER
SPEC.loader.exec_module(CHECKER)


class MarkdownStyleCheckerTests(unittest.TestCase):
    def write_note(self, directory: Path, name: str, content: str) -> Path:
        path = directory / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def test_valid_obsidian_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            note = self.write_note(
                Path(temporary),
                "valid.md",
                "---\ntags:\n  - test\nrelated: \"[[Index]]\"\n---\n\n# Valid note\n\n"
                "Visible [[Index]]. `%% [[not syntax]]` %% [[also ignored]] ``` %%\n\n"
                "```text\n%% [[ignored in fence]]\n```\n",
            )
            self.assertEqual(CHECKER.check_file(note), [])

    def test_frontmatter_must_start_at_first_byte(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            note = self.write_note(Path(temporary), "late.md", "\n---\nstatus: draft\n---\n")
            self.assertTrue(any(item.code == "frontmatter-position" for item in CHECKER.check_file(note)))

    def test_duplicate_yaml_key_is_an_error(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            note = self.write_note(
                Path(temporary),
                "duplicate.md",
                "---\nproject:\n  status: draft\n  status: done\n---\n\nBody.\n",
            )
            issues = CHECKER.check_file(note)
            self.assertTrue(any(item.code == "frontmatter-yaml" and item.severity == "error" for item in issues))

    def test_invalid_yaml_type_is_an_error(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            note = self.write_note(Path(temporary), "list.md", "---\n- one\n- two\n---\n\nBody.\n")
            self.assertTrue(any(item.code == "frontmatter-type" for item in CHECKER.check_file(note)))

    def test_unclosed_constructs_are_errors(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            note = self.write_note(
                Path(temporary),
                "broken.md",
                "# Broken\n\n[[Missing\n\n```text\nunclosed\n",
            )
            codes = {item.code for item in CHECKER.check_file(note)}
            self.assertEqual({"fence-unclosed", "wikilink-unbalanced"}, codes)

    def test_unclosed_comment_is_an_error(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            note = self.write_note(Path(temporary), "comment.md", "Body.\n\n%% unclosed\n")
            self.assertTrue(any(item.code == "comment-unclosed" for item in CHECKER.check_file(note)))

    def test_style_warnings_are_distinct_from_errors(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            note = self.write_note(Path(temporary), "style.md", "# Heading\nBody\n- item")
            issues = CHECKER.check_file(note)
            self.assertTrue(issues)
            self.assertTrue(all(item.severity == "warning" for item in issues))

    def test_directory_expansion_is_recursive_and_deduplicated(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            first = self.write_note(root, "one.md", "One.\n")
            second = self.write_note(root, "nested/two.md", "Two.\n")
            files, issues = CHECKER.expand_paths([root, first])
            self.assertEqual(files, sorted([first, second], key=str))
            self.assertEqual(issues, [])

    def test_json_cli_and_errors_only(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            note = self.write_note(Path(temporary), "warning.md", "# Heading\nBody")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--format", "json", "--errors-only", str(note)],
                check=False,
                capture_output=True,
                text=True,
            )
            report = json.loads(result.stdout)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(report["files_checked"], 1)
            self.assertEqual(report["issues"], [])


if __name__ == "__main__":
    unittest.main()
