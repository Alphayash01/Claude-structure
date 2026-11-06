import re
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import check_template as ct  # noqa: E402
from template_spec import REQUIRED_FILES, FileSpec  # noqa: E402

FENCE = "`" * 3
CLEAN = "# T\n\n> **Purpose:** x\n\n<!-- ADD: y -->\n"
FORM = FileSpec(add_slot=False, purpose_line=False)


class CheckerTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def write(self, rel, text):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def check(self, rel, text, spec=FileSpec(), strict=True):
        self.write(rel, text)
        return ct.check_file(self.root, rel, spec, strict_links=strict)

    def assertHas(self, errors, fragment):
        self.assertTrue(any(fragment in e for e in errors), f"{fragment!r} not in {errors}")

    def test_clean_file_passes(self):
        self.assertEqual(self.check("A.md", CLEAN + "{{PROJECT_NAME}}\n"), [])

    def test_malformed_placeholders_flagged(self):
        for bad in ("{{ PROJECT_NAME }}", "{{Project_Name}}", "{{PROJECT_NAME}"):
            self.assertHas(self.check("A.md", CLEAN + bad + "\n"), "malformed placeholder")

    def test_unregistered_placeholder_flagged(self):
        self.assertHas(self.check("A.md", CLEAN + "{{FOO_BAR}}\n"),
                       "unregistered placeholder {{FOO_BAR}}")

    def test_unclosed_comment_flagged(self):
        self.assertHas(self.check("A.md", CLEAN + "<!-- ADD: describe users\n\n## Goals\n"),
                       "unclosed HTML comment")

    def test_mermaid_arrow_does_not_close_comment(self):
        text = CLEAN + "<!-- ADD: diagram\n" + f"{FENCE}mermaid\nflowchart LR\n  a -->|x| b\n{FENCE}\n"
        self.assertHas(self.check("A.md", text), "unclosed HTML comment")

    def test_add_marker_requires_colon(self):
        self.assertHas(self.check("A.md", CLEAN + "| <!-- ADD --> |\n"), "ADD marker without colon")
        self.assertHas(self.check("A.md", CLEAN + "| <!-- ADD --> | <!-- ADD: x --> |\n"),
                       "ADD marker without colon")

    def test_link_case_must_match(self):
        self.write("RULES.md", "# R\n")
        self.assertHas(self.check("A.md", CLEAN + "[r](rules.md)\n"), "broken link")

    def test_root_relative_link_survives_move(self):
        self.write("RULES.md", "# R\n\n## Testing\n")
        text = CLEAN + "[r](/RULES.md#testing)\n"
        self.assertEqual(self.check("docs/tasks/7-x.md", text), [])
        self.assertEqual(self.check("docs/tasks/archive/7-x.md", text), [])
        self.assertHas(self.check("docs/tasks/7-x.md", CLEAN + "[m](/missing.md)\n"), "broken link")

    def test_add_marker_in_code_block_flagged(self):
        text = CLEAN + f"{FENCE}\n<!-- ADD: x -->\n{FENCE}\n"
        self.assertHas(self.check("A.md", text), "ADD marker inside code block")

    def test_markers_in_mermaid_flagged(self):
        text = CLEAN + f'{FENCE}mermaid\nflowchart LR\n  a["{{{{PROJECT_NAME}}}}"]\n{FENCE}\n'
        self.assertHas(self.check("A.md", text), "marker inside mermaid block")

    def test_mermaid_type_checked(self):
        bad = CLEAN + f"{FENCE}mermaid\nC4Context\n{FENCE}\n"
        good = CLEAN + f"{FENCE}mermaid\nflowchart LR\n  a --> b\n{FENCE}\n"
        self.assertHas(self.check("A.md", bad), "unsupported mermaid diagram type")
        self.assertEqual(self.check("A.md", good), [])

    def test_links_and_anchors(self):
        self.write("RULES.md", "# R\n\n## Testing\n")
        self.assertHas(self.check("A.md", CLEAN + "[x](missing.md)\n"), "broken link")
        self.assertHas(self.check("A.md", CLEAN + "[x](RULES.md#nope)\n"), "broken anchor")
        self.assertEqual(self.check("A.md", CLEAN + "[x](RULES.md#testing) [y](#t)\n"), [])
        self.assertHas(self.check("docs/B.md", CLEAN + "[x](../../outside.md)\n"),
                       "link escapes template")

    def test_skipped_and_code_links(self):
        text = (CLEAN + "[a]({{ISSUE_TRACKER_URL}}) [b](https://x.io) [c](mailto:a@b.c) "
                "`[d](no.md)`\n" + f"{FENCE}\n[e](no.md)\n{FENCE}\n"
                "[f]: {{REPO_URL}}/compare/v1...HEAD\n")
        self.assertEqual(self.check("A.md", text), [])

    def test_github_form_links(self):
        self.write("RULES.md", "# R\n")
        rel = ".github/PULL_REQUEST_TEMPLATE.md"
        self.assertHas(self.check(rel, "[r](../RULES.md)\n", FORM),
                       "relative link in .github form")
        self.assertHas(self.check(rel, "[r]({{REPO_URL}}/blob/{{MAIN_BRANCH}}/MISSING.md)\n", FORM),
                       "broken link")
        self.assertEqual(self.check(rel, "[r]({{REPO_URL}}/blob/{{MAIN_BRANCH}}/RULES.md)\n", FORM), [])

    def test_link_to_template_guide_flagged(self):
        self.write("TEMPLATE_GUIDE.md", "# G\n")
        self.assertHas(self.check("A.md", CLEAN + "[g](TEMPLATE_GUIDE.md)\n"),
                       "link to TEMPLATE_GUIDE.md")

    def test_strict_links_toggle(self):
        text = CLEAN + "[s](docs/SECURITY.md)\n"
        self.assertHas(self.check("A.md", text), "broken link")
        self.assertEqual(self.check("A.md", text, strict=False), [])

    def test_required_links_and_headings(self):
        spec = FileSpec(headings=("Goals", "Non-goals"), links=("RULES.md",))
        self.write("RULES.md", "# R\n")
        errors = self.check("A.md", CLEAN + "## Non-goals\n## Goals\n", spec)
        self.assertHas(errors, "missing or out-of-order heading '## Non-goals'")
        self.assertHas(errors, "missing required link RULES.md")
        ok = CLEAN + "## Goals\n## Other\n## Non-goals\n[r](RULES.md)\n"
        self.assertEqual(self.check("A.md", ok, spec), [])

    def test_purpose_add_slot_and_length(self):
        self.assertHas(self.check("A.md", "# T\n\nText\n<!-- ADD: y -->\n"), "missing purpose line")
        self.assertHas(self.check("A.md", "# T\n\n> **Purpose:** x\n"), "missing ADD slot")
        self.assertEqual(self.check("A.md", "# T\n", FORM), [])
        self.assertHas(self.check("A.md", CLEAN + "x\n" * 146), "exceeds 150 lines")

    def test_denylist(self):
        self.assertHas(self.check("A.md", CLEAN + "Run npm install.\n"), "stack-specific term 'npm'")
        self.assertHas(self.check("A.md", CLEAN + "Deploy with GitHub Actions.\n"),
                       "stack-specific term 'github actions'")
        self.assertEqual(self.check("A.md", CLEAN + "GitHub, Mermaid, SemVer, a graph node.\n"), [])

    def test_front_matter(self):
        rel = ".github/ISSUE_TEMPLATE/bug_report.md"
        self.assertHas(self.check(rel, "---\nname: Bug report\nlabels: bug\n---\n", FORM),
                       "invalid front matter")
        self.assertHas(self.check(rel, "## Description\n", FORM), "invalid front matter")
        good = '---\nname: Bug report\nabout: Report a bug\nlabels: bug\ntitle: "[Bug]: "\n---\n'
        self.assertEqual(self.check(rel, good, FORM), [])

    def test_skill_front_matter(self):
        rel = ".claude/skills/dev-fast/SKILL.md"
        good = ("---\nname: dev-fast\ndescription: Fast mode\ndisable-model-invocation: true\n"
                'argument-hint: "[#issue] what"\neffort: low\n---\n')
        self.assertEqual(self.check(rel, good, FORM), [])
        self.assertHas(self.check(rel, "---\nname: dev-fast\ndisable-model-invocation: true\n---\n", FORM),
                       "invalid front matter")
        self.assertHas(self.check(rel, "---\nname: dev-fast\ndescription: x\n---\n", FORM),
                       "skill must set disable-model-invocation: true")

    def test_slugify(self):
        self.assertEqual(ct.slugify("Day 0: access"), "day-0-access")
        self.assertEqual(ct.slugify("[Unreleased]"), "unreleased")
        self.assertEqual(ct.slugify("Logging and observability"), "logging-and-observability")
        self.assertEqual(ct.slugify("This project's data"), "this-projects-data")

    def test_check_all_global(self):
        self.write("stray.md", "# S\n")
        errors = ct.check_all(self.root)
        self.assertEqual(sum("missing file" in e for e in errors), len(REQUIRED_FILES))
        self.assertHas(errors, "stray.md:0: unexpected file")
        self.assertHas(errors, "registry placeholder {{PROJECT_NAME}} unused")
        self.write("TEMPLATE_GUIDE.md", "{{PROJECT_NAME}}\n")
        errors = ct.check_all(self.root)
        self.assertHas(errors, "TEMPLATE_GUIDE.md does not list {{TEAM_NAME}}")
        self.assertHas(errors, "registry placeholder {{PROJECT_NAME}} unused")

    def test_guide_row_must_list_every_file_using_placeholder(self):
        self.write("README.md", "{{PROJECT_NAME}}\n")
        self.write("INTENT.md", "{{PROJECT_NAME}}\n")
        self.write("TEMPLATE_GUIDE.md", "| `{{PROJECT_NAME}}` | Name | README.md |\n")
        self.assertHas(ct.check_all(self.root),
                       "TEMPLATE_GUIDE.md row for {{PROJECT_NAME}} misses INTENT.md")
        self.write("TEMPLATE_GUIDE.md", "| `{{PROJECT_NAME}}` | Name | docs/adr/README.md, INTENT.md |\n")
        self.assertHas(ct.check_all(self.root),
                       "TEMPLATE_GUIDE.md row for {{PROJECT_NAME}} misses README.md")
        self.write("TEMPLATE_GUIDE.md", "| Marker | Example | `{{PROJECT_NAME}}` |\n"
                                        "| `{{PROJECT_NAME}}` | Name | README.md, INTENT.md |\n")
        self.assertFalse(any("row for {{PROJECT_NAME}}" in e for e in ct.check_all(self.root)))

    def test_placeholder_usage(self):
        self.write("README.md", "{{PROJECT_NAME}}\n")
        self.write("TEMPLATE_GUIDE.md", "{{PROJECT_NAME}}\n")
        usage = ct.placeholder_usage(self.root)
        self.assertEqual(usage["PROJECT_NAME"], ["README.md"])
        self.assertEqual(usage["TEAM_NAME"], [])


class TemplateGuideSearchTest(unittest.TestCase):
    """The guide's unfinished-work search must come back empty once a project is filled in."""

    def test_unfinished_search_is_empty_once_filled(self):
        root = Path(__file__).resolve().parent.parent / "template"
        guide = (root / "TEMPLATE_GUIDE.md").read_text(encoding="utf-8")
        command = next(line.strip() for line in guide.splitlines() if line.strip().startswith("grep "))
        pattern = re.search(r'"([^"]+)"', command).group(1)
        excludes = re.findall(r"--exclude=(\S+)", command)
        leftovers = []
        for path in root.rglob("*.md"):
            if path.name == "TEMPLATE_GUIDE.md" or path.name in excludes:
                continue
            text = path.read_text(encoding="utf-8")
            if path.name != "0000-template.md":  # its slots stay: every new ADR is copied from it
                text = re.sub(r"<!-- ADD:.*?-->", "", text, flags=re.S)
            if re.search(pattern, ct.PLACEHOLDER_RE.sub("filled", text)):
                leftovers.append(path.relative_to(root).as_posix())
        self.assertEqual(leftovers, [])


if __name__ == "__main__":
    unittest.main()
