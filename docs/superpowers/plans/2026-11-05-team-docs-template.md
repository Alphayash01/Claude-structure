# Team Docs Starter Template Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the 19-file team/internal Markdown starter template under `template/`, plus a checker that enforces the spec's acceptance checks.

**Architecture:** `tools/template_spec.py` holds the spec as data (required files, placeholder registry, per-file headings, links and limits). `tools/check_template.py` validates `template/` against it. Task 1 builds and unit-tests the checker. Tasks 2–7 each add their files' entries to `FILES` (the failing test), write the Markdown, then pass the checker.

**Tech Stack:** GitHub-flavored Markdown, Mermaid, Python 3.14 standard library only (`unittest`, `re`, `pathlib`, `dataclasses`, `argparse`).

**Spec:** `docs/superpowers/specs/2026-11-05-team-docs-template-design.md`

## Global Constraints

- Audience: team/internal repos hosted on GitHub.
- `template/` holds exactly the 19 files of spec §2 and nothing else.
- Two markers only: `{{UPPER_SNAKE_CASE}}` values and `<!-- ADD: what to write here -->` slots. The three `.github/` forms use plain hint comments (`<!-- Describe ... -->`, no `ADD:`) because they are filled per PR/issue, not at adoption.
- Only the 17 placeholders of spec §3.3.
- Length: ≤ 150 lines per file; `RULES.md` ≤ 220; `CLAUDE.md` ≤ 60.
- No language, framework, cloud or vendor names. Allowed: GitHub, Conventional Commits, Keep a Changelog, SemVer, Mermaid, C4. The denylist matches whole words, so write "respond", never the verb "react".
- Examples only where format matters; never invent project facts. Numeric defaults pinned in this plan (turnaround, patch times, rollback target) are editable built-in defaults, not facts.
- Every file except the `.github/` forms and ADRs 0000/0001 opens with `# Title`, a blank line, then `> **Purpose:** <one line>`. Where a task pins one, the next line is `> **Owner:** … · **Review:** …`.
- Links are relative. `.github/` forms link with `{{REPO_URL}}/blob/{{MAIN_BRANCH}}/<path>`. Nothing links to `TEMPLATE_GUIDE.md`.
- Mermaid blocks start with `flowchart` or `sequenceDiagram`, use generic labels ("This system"), and contain no placeholders or markers. Put an `ADD` comment above each diagram.
- Never put `<!-- ADD:` inside a fenced code block (it renders as visible text).
- `tools/` and `tests/` live outside `template/` and are not part of the template.
- Commits use Conventional Commits and end with the trailer `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.

## Review Focus

1. An unclosed `<!--` (e.g. `<!-- ADD: describe users` with no `-->`) hides everything after it on GitHub, so the user sees a half-empty file. → Task 1 `test_unclosed_comment_flagged`.
2. Relative links in `.github/` forms break once GitHub pastes the form into a PR/issue body. → Task 1 `test_github_form_links`.
3. A link to `TEMPLATE_GUIDE.md` breaks the moment the user deletes the guide. → Task 1 `test_link_to_template_guide_flagged`.
4. Near-miss placeholders (`{{ PROJECT_NAME }}`, `{{Project_Name}}`, `{{PROJECT_NAME}`) survive both find-and-replace and the unfinished-work grep. → Task 1 `test_malformed_placeholders_flagged`.
5. Markers inside code: `<!-- ADD:` in a fenced block shows as text, and `{{…}}` inside Mermaid is node-shape syntax that breaks the diagram. → Task 1 `test_add_marker_in_code_block_flagged`, `test_markers_in_mermaid_flagged`.

---

## File map

| Path | Responsibility | Task |
|---|---|---|
| `tools/template_spec.py` | Spec as data | 1 (`FILES` grows in 2–7) |
| `tools/check_template.py` | Validation logic + CLI | 1 |
| `tests/test_check_template.py` | Checker unit tests | 1 |
| `template/INTENT.md`, `template/RULES.md` | Foundation | 2 |
| `template/CONTRIBUTING.md`, `template/CHANGELOG.md`, `template/.github/**` | Team workflow | 3 |
| `template/docs/ARCHITECTURE.md`, `template/docs/adr/*` | Design records | 4 |
| `template/docs/DEVELOPMENT.md`, `template/docs/ONBOARDING.md` | Getting started | 5 |
| `template/docs/DEPLOYMENT.md`, `template/docs/RUNBOOK.md`, `template/docs/SECURITY.md` | Operations | 6 |
| `template/README.md`, `template/CLAUDE.md`, `template/TEMPLATE_GUIDE.md` | Entry points | 7 |

Foundation goes first because everything links to it. Entry points go last because they link to everything.

---

### Task 1: Checker

**Files:**
- Create: `tools/template_spec.py`, `tools/check_template.py`
- Test: `tests/test_check_template.py`

**Interfaces:**
- Produces:
  - `FileSpec(headings: tuple[str, ...] = (), links: tuple[str, ...] = (), max_lines: int = 150, add_slot: bool = True, purpose_line: bool = True)`, a frozen dataclass. `headings` are required H2 texts and must appear in order (other headings may sit between them). `links` are template-root-relative paths the file must link to.
  - `FILES: dict[str, FileSpec]` (starts empty; Tasks 2–7 add `FILES["<rel>"] = FileSpec(...)` lines at the end of `template_spec.py`).
  - `slugify(heading: str) -> str`
  - `check_file(root: Path, rel: str, spec: FileSpec, strict_links: bool = True) -> list[str]`
  - `check_all(root: Path) -> list[str]`, which runs per-file checks on every existing required file using `FILES.get(rel, FileSpec())` plus the global checks.
  - `placeholder_usage(root: Path) -> dict[str, list[str]]`, mapping each registry name (no braces) to the required files using it, in `REQUIRED_FILES` order and excluding `TEMPLATE_GUIDE.md`.
  - `main(argv: list[str] | None = None) -> int`
  - Errors are strings `"{rel}:{line}: {message}"`; line `0` means the whole file.
  - CLI: `python tools/check_template.py` runs `check_all` on `template/` (resolved from the script location). It prints each error, then `N error(s)` with exit 1, or `OK: N file(s) checked` with exit 0. `--files REL [REL ...]` runs `check_file` with `strict_links=False`. `--usage` prints `{{NAME}}: a.md, b.md` (or `{{NAME}}: (unused)`) per registry entry. `--root PATH` overrides the template location. Call `sys.stdout.reconfigure(encoding="utf-8")` first, because Windows consoles default to cp1252.

- [ ] **Step 1: Create `tools/template_spec.py` with this data**

```python
"""The design spec as data. Tasks 2-7 append FILES entries at the end."""
from dataclasses import dataclass


@dataclass(frozen=True)
class FileSpec:
    headings: tuple[str, ...] = ()
    links: tuple[str, ...] = ()
    max_lines: int = 150
    add_slot: bool = True
    purpose_line: bool = True


REQUIRED_FILES = (
    "README.md", "INTENT.md", "RULES.md", "CONTRIBUTING.md", "CHANGELOG.md",
    "CLAUDE.md", "TEMPLATE_GUIDE.md",
    "docs/ARCHITECTURE.md", "docs/ONBOARDING.md", "docs/DEVELOPMENT.md",
    "docs/DEPLOYMENT.md", "docs/RUNBOOK.md", "docs/SECURITY.md",
    "docs/adr/README.md", "docs/adr/0000-template.md",
    "docs/adr/0001-record-architecture-decisions.md",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/ISSUE_TEMPLATE/bug_report.md",
    ".github/ISSUE_TEMPLATE/feature_request.md",
)

REGISTRY = {
    "PROJECT_NAME": "Human-readable project name",
    "PROJECT_DESCRIPTION": "One-line description",
    "TEAM_NAME": "Owning team",
    "TEAM_CHANNEL": "Team chat channel",
    "TECH_LEAD": "Technical lead / primary owner",
    "REPO_URL": "Repository URL",
    "ISSUE_TRACKER_URL": "Issue tracker URL",
    "MAIN_BRANCH": "Default branch name",
    "REQUIRED_APPROVALS": "Number of PR approvals required",
    "ONCALL_CONTACT": "On-call rotation / pager",
    "SECURITY_CONTACT": "Internal security contact",
    "INSTALL_CMD": "Install dependencies",
    "DEV_CMD": "Run locally",
    "TEST_CMD": "Run tests",
    "LINT_CMD": "Lint / format check",
    "BUILD_CMD": "Production build",
    "ADOPTION_DATE": "Date the template was adopted (ADR 0001)",
}

DENYLIST = (
    "python", "java", "javascript", "typescript", "nodejs", "node.js", "npm",
    "yarn", "pnpm", "pip", "maven", "gradle", "react", "angular", "vue",
    "django", "flask", "spring", "dotnet", "golang", "rust", "php", "ruby",
    "aws", "azure", "gcp", "heroku", "vercel", "docker", "kubernetes", "k8s",
    "terraform", "jenkins", "circleci", "github actions", "gitlab",
    "bitbucket", "jira", "confluence", "slack", "pagerduty", "opsgenie",
    "datadog", "sentry", "grafana", "prometheus", "postgres", "postgresql",
    "mysql", "mongodb", "redis",
)

ALLOWED_MERMAID_TYPES = ("flowchart", "sequenceDiagram")
PURPOSE_PREFIX = "> **Purpose:**"
REPO_LINK_PREFIX = "{{REPO_URL}}/blob/{{MAIN_BRANCH}}/"
GUIDE = "TEMPLATE_GUIDE.md"

FILES: dict[str, FileSpec] = {}
```

- [ ] **Step 2: Write the failing tests in `tests/test_check_template.py`**

```python
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

    def test_placeholder_usage(self):
        self.write("README.md", "{{PROJECT_NAME}}\n")
        self.write("TEMPLATE_GUIDE.md", "{{PROJECT_NAME}}\n")
        usage = ct.placeholder_usage(self.root)
        self.assertEqual(usage["PROJECT_NAME"], ["README.md"])
        self.assertEqual(usage["TEAM_NAME"], [])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3: Run the tests to verify they fail**

Run: `python -m unittest discover -s tests -v`
Expected: ERROR with `ModuleNotFoundError: No module named 'check_template'`

- [ ] **Step 4: Implement `tools/check_template.py`**

Approach: parse each file once into lines tagged with fence state (fences are three or more backticks or tildes; record the info string such as `mermaid`). Every check below reads that structure. Strip inline code spans before matching links. Represent resolved targets as posix paths relative to root (normalize, don't `resolve()`), so comparisons with `REQUIRED_FILES` and `spec.links` also work on Windows.

| Check | Applies to | Rule | Message contains |
|---|---|---|---|
| exists | every checked file | file is present (skip all other checks if not) | `missing file` |
| placeholders | whole text | each `{{` starts a token running to the first `}}` on that line, or to line end; the token must fullmatch `\{\{[A-Z_]+\}\}` and its name must be in `REGISTRY` | `malformed placeholder` / `unregistered placeholder {{NAME}}` |
| comments | whole text | each `<!--` is closed by `-->` before the next `<!--` or EOF | `unclosed HTML comment` |
| code markers | fenced lines | no `<!-- ADD:`; inside `mermaid` fences also no `{{` and no `ADD:` | `ADD marker inside code block` / `marker inside mermaid block` |
| mermaid | `mermaid` fences | first non-blank line starts with an `ALLOWED_MERMAID_TYPES` entry | `unsupported mermaid diagram type` |
| links | inline `[t](target)` and reference `[t]: target`, outside fences and inline code | Skip `http://`, `https://` and `mailto:` targets, and targets starting `{{` unless they start with `REPO_LINK_PREFIX` (strip the prefix and resolve from root). Resolve all other targets from the file's directory and strip any `#anchor`. | see rows below |
| ↳ escape | | resolved path outside root | `link escapes template` |
| ↳ .github | file under `.github/` | target neither external nor `REPO_LINK_PREFIX` | `relative link in .github form` |
| ↳ guide | file ≠ `GUIDE` | target is `GUIDE` | `link to TEMPLATE_GUIDE.md` |
| ↳ broken | | target missing (with `strict_links=False`, skip targets listed in `REQUIRED_FILES`) | `broken link` |
| ↳ anchor | same-file `#a`, or an existing `.md` target | anchor not among that file's heading slugs (H1–H6 outside fences; repeated slugs get `-1`, `-2`) | `broken anchor` |
| required links | `spec.links` | each path equals the resolved target of some link in the file | `missing required link {path}` |
| headings | `spec.headings` | `## <text>` lines outside fences contain them as an in-order subsequence; report each one not matched | `missing or out-of-order heading '## <text>'` |
| purpose | `spec.purpose_line` | first non-blank line after the first `# ` line starts with `PURPOSE_PREFIX` | `missing purpose line` |
| ADD slot | `spec.add_slot` | at least one `<!-- ADD:` outside fences | `missing ADD slot` |
| length | `spec.max_lines` | `len(text.splitlines()) <= max_lines` | `exceeds {max_lines} lines` |
| denylist | whole text | no `DENYLIST` term as a case-insensitive `\b`-bounded match | `stack-specific term '{term}'` |
| front matter | `.github/ISSUE_TEMPLATE/*.md` | first line `---`, a later closing `---`; lines between are blank or match `^[a-z_]+:`; `name` and `about` present with non-empty values | `invalid front matter` |
| global | `check_all` only | each `REQUIRED_FILES` path exists (`missing file`); every file under root is in `REQUIRED_FILES` (`unexpected file`); each `REGISTRY` name appears in a required file other than `GUIDE` (`registry placeholder {{NAME}} unused`); if `GUIDE` exists, it mentions every `{{NAME}}` (`TEMPLATE_GUIDE.md does not list {{NAME}}`) | as listed |

`slugify`: lowercase, drop every character that is not a word character, space or hyphen, then replace spaces with hyphens. A root that does not exist counts as empty.

- [ ] **Step 5: Run the tests to verify they pass**

Run: `python -m unittest discover -s tests -v`
Expected: `Ran 19 tests` … `OK`

- [ ] **Step 6: Run the checker on the still-empty template**

Run: `python tools/check_template.py`
Expected: exit 1; 19 `missing file` lines, 17 `unused` lines, final line `36 error(s)`

- [ ] **Step 7: Commit**

```bash
git add tools tests
git commit -m "build: add template checker with spec data" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 2: INTENT.md and RULES.md

**Files:**
- Modify: `tools/template_spec.py` (append `FILES` entries)
- Create: `template/INTENT.md`, `template/RULES.md`

**Interfaces:**
- Consumes: `FileSpec`, `FILES`, the checker CLI (Task 1).
- Produces anchors that later tasks link to: `INTENT.md#goals`; `RULES.md#testing`, `#security`, `#configuration`, `#error-handling`, `#logging-and-observability`, `#documentation`, `#exceptions-log`. Rule IDs `GEN-`, `CODE-`, `STRUCT-`, `ERR-`, `LOG-`, `TEST-`, `DEP-`, `SEC-`, `CFG-`, `PERF-`, `DOC-` (e.g. `TEST-1`, `DOC-1`) that later files cite.

- [ ] **Step 1: Append the specs to `tools/template_spec.py`**

```python
FILES["INTENT.md"] = FileSpec(headings=(
    "Problem", "Users and stakeholders", "Goals", "Non-goals", "Success metrics",
    "Constraints", "Assumptions and open questions", "Decision filter"))
FILES["RULES.md"] = FileSpec(headings=(
    "How these rules work", "Code", "Structure", "Error handling",
    "Logging and observability", "Testing", "Dependencies", "Security",
    "Configuration", "Performance", "Documentation",
    "Language and framework conventions", "Project structure", "Naming conventions",
    "Project-specific rules", "Exceptions log"),
    links=("docs/SECURITY.md", "docs/adr/README.md"), max_lines=220)
```

- [ ] **Step 2: Run the checker to verify it fails**

Run: `python tools/check_template.py --files INTENT.md RULES.md`
Expected: exit 1 with `INTENT.md:0: missing file` and `RULES.md:0: missing file`

- [ ] **Step 3: Write `template/INTENT.md`**

Content follows spec §4 INTENT. Pinned choices:
- H1 `# Intent — {{PROJECT_NAME}}`; Owner line `> **Owner:** {{TECH_LEAD}} · **Review:** when scope changes, and at least quarterly`.
- Goals are numbered `G1`, `G2`, … and non-goals `NG1`, … so issues and PRs can cite them. The Goals section carries the one-line contrast: Bad "Build a dashboard." / Good "Support staff resolve a ticket in under 10 minutes."
- Success metrics is a table `| Metric | Target | How measured | Owner |`. Constraints is a table `| Type | Constraint |` with rows Time, Budget, Compliance, Technical and empty values.
- Decision filter has exactly three questions: serves a goal (cite `G#`)? violates a non-goal (`NG#`)? fits the constraints? It closes with "If the answer is unclear, update this file first, by PR."
- Every section except Decision filter has an `ADD` slot.

- [ ] **Step 4: Write `template/RULES.md`**

Content follows spec §4 RULES. Pinned choices:
- H1 `# Engineering Rules — {{PROJECT_NAME}}`; Owner line `> **Owner:** {{TECH_LEAD}} · **Review:** every 6 months`.
- Rule line format: `- **ERR-1** Validate input at trust boundaries. *Why:* bad data caught at the edge is cheap; deep inside it corrupts state.` Number rules within each section; section prefixes are listed in Interfaces.
- "How these rules work" contains the GEN rules: rules beat preference; cite IDs in reviews (`blocking: violates TEST-1`); change a rule by PR; significant changes get an ADR (link `docs/adr/README.md`); waivers go in the Exceptions log.
- The Security section ends with `Details: [docs/SECURITY.md](docs/SECURITY.md)`.
- The five slot sections (Language and framework conventions … Exceptions log) each have an `ADD` slot. Exceptions log is the table `| Rule | Where | Why | Until | Approved by |`.

- [ ] **Step 5: Run the checker to verify it passes**

Run: `python tools/check_template.py --files INTENT.md RULES.md`
Expected: `OK: 2 file(s) checked`

- [ ] **Step 6: Review the content against the spec**

Every Built-in and Slots bullet of spec §4 INTENT and RULES maps to text in the file. No invented project facts.

- [ ] **Step 7: Commit**

```bash
git add tools/template_spec.py template/INTENT.md template/RULES.md
git commit -m "docs(template): add INTENT and RULES" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 3: CONTRIBUTING, CHANGELOG and GitHub forms

**Files:**
- Modify: `tools/template_spec.py`
- Create: `template/CONTRIBUTING.md`, `template/CHANGELOG.md`, `template/.github/PULL_REQUEST_TEMPLATE.md`, `template/.github/ISSUE_TEMPLATE/bug_report.md`, `template/.github/ISSUE_TEMPLATE/feature_request.md`

**Interfaces:**
- Consumes: anchors and rule IDs from Task 2; `docs/DEPLOYMENT.md#rollback` (created in Task 6; tolerated by `--files` mode, verified in Task 7).
- Produces: `CONTRIBUTING.md#pull-requests`.

- [ ] **Step 1: Append the specs**

```python
FILES["CONTRIBUTING.md"] = FileSpec(headings=(
    "Workflow", "Branches", "Commits", "Pull requests", "Code review",
    "Merging and reverting", "Definition of Done", "Team specifics"),
    links=("RULES.md", "CHANGELOG.md", ".github/PULL_REQUEST_TEMPLATE.md", "docs/DEPLOYMENT.md"))
FILES["CHANGELOG.md"] = FileSpec(headings=("[Unreleased]",))
FILES[".github/PULL_REQUEST_TEMPLATE.md"] = FileSpec(headings=(
    "Summary", "Why", "What changed", "How it was tested", "Screenshots",
    "Risk and rollback", "Checklist"),
    links=("RULES.md", "CHANGELOG.md", "CONTRIBUTING.md", "docs/adr/README.md"),
    add_slot=False, purpose_line=False)
FILES[".github/ISSUE_TEMPLATE/bug_report.md"] = FileSpec(headings=(
    "Description", "Steps to reproduce", "Expected behavior", "Actual behavior",
    "Environment", "Logs and screenshots", "Impact"), add_slot=False, purpose_line=False)
FILES[".github/ISSUE_TEMPLATE/feature_request.md"] = FileSpec(headings=(
    "Problem", "Goal served", "Proposed solution", "Alternatives considered",
    "Acceptance criteria", "Out of scope"),
    links=("INTENT.md",), add_slot=False, purpose_line=False)
```

- [ ] **Step 2: Run the checker to verify it fails**

Run: `python tools/check_template.py --files CONTRIBUTING.md CHANGELOG.md .github/PULL_REQUEST_TEMPLATE.md .github/ISSUE_TEMPLATE/bug_report.md .github/ISSUE_TEMPLATE/feature_request.md`
Expected: exit 1 with five `missing file` lines

- [ ] **Step 3: Write `template/CONTRIBUTING.md`**

Content follows spec §4 CONTRIBUTING. Pinned choices:
- Workflow: a Mermaid `flowchart LR` of Issue → Branch → Pull request → Review → Merge → Deploy.
- Branches: `type/short-description` with types `feat`, `fix`, `docs`, `refactor`, `test`, `chore` (e.g. `feat/export-csv`); merge within 2 days.
- Commits: `type(scope): summary`, imperative, ≤ 72 characters; types `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `perf`, `build`, `ci`; breaking changes use `!` plus a `BREAKING CHANGE:` footer. Show three examples in one fenced block: `feat(auth): add password reset by email`, `fix(orders): return 404 for unknown order id`, `refactor!: remove legacy v1 endpoints` with its footer.
- Pull requests: aim for < 400 changed lines, excluding generated files and lockfiles; the PR title uses the commit format because it becomes the squash commit; open a draft for early feedback; link the PR template.
- Code review: 1-business-day turnaround; `{{REQUIRED_APPROVALS}}` approvals; only `blocking:` comments block a merge; cite RULES IDs; "approve when you would be comfortable owning this code".
- Merging and reverting: squash-merge by default; delete the branch; revert first, fix forward after; production rollback links to `docs/DEPLOYMENT.md#rollback`.
- Definition of Done: a `- [ ]` checklist citing `TEST-1`, `DOC-1` and the CHANGELOG.
- Team specifics: `ADD` slots for review assignment, CI checks and release cadence.

- [ ] **Step 4: Write `template/CHANGELOG.md`**

Keep a Changelog 1.1.0 layout. The purpose line is `> **Purpose:** All notable changes to {{PROJECT_NAME}}, newest first.`, followed by the standard format sentence linking `https://keepachangelog.com/en/1.1.0/` and `https://semver.org/spec/v2.0.0.html`, then the rule "Add your entry in the same PR as the change, written for the people who use the system." `## [Unreleased]` has empty `###` subsections Added, Changed, Deprecated, Removed, Fixed, Security. Below them, an `ADD` slot covers the first release entry and compare links (e.g. `[Unreleased]: {{REPO_URL}}/compare/v1.0.0...HEAD`).

- [ ] **Step 5: Write the three `.github/` forms**

Use plain hint comments, no `ADD:`. Every link uses `{{REPO_URL}}/blob/{{MAIN_BRANCH}}/<path>`.
- Links go in visible text, never inside hint comments, because comments stay hidden in the PR/issue body and their links can't be clicked.
- `PULL_REQUEST_TEMPLATE.md`: the Screenshots hint says "UI changes only; delete otherwise". The Checklist is `- [ ]` items: PR follows the process (`CONTRIBUTING.md#pull-requests`: small, linked issue, self-reviewed); tests added or updated; docs updated in this PR (`RULES.md#documentation`); CHANGELOG entry under Unreleased (`CHANGELOG.md`); no secrets or personal data in code, logs or fixtures; follows `RULES.md`; ADR added for any significant decision (`docs/adr/README.md`).
- `bug_report.md` front matter, exactly:

```yaml
---
name: Bug report
about: Report something that is broken or behaves unexpectedly
title: "[Bug]: "
labels: bug
assignees: ""
---
```

- `feature_request.md` front matter is the same shape with `name: Feature request`, `about: Propose a new capability or an improvement`, `title: "[Feature]: "`, `labels: enhancement`. Goal served starts with the visible line "Which [goal](…/INTENT.md#goals) does this serve (e.g. G2)?"

- [ ] **Step 6: Run the checker to verify it passes**

Run: the command from Step 2.
Expected: `OK: 5 file(s) checked`

- [ ] **Step 7: Review the content against spec §4** for these five files, then commit

```bash
git add tools/template_spec.py template/CONTRIBUTING.md template/CHANGELOG.md template/.github
git commit -m "docs(template): add contributing workflow, changelog and GitHub forms" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 4: ARCHITECTURE and ADRs

**Files:**
- Modify: `tools/template_spec.py`
- Create: `template/docs/ARCHITECTURE.md`, `template/docs/adr/README.md`, `template/docs/adr/0000-template.md`, `template/docs/adr/0001-record-architecture-decisions.md`

**Interfaces:**
- Consumes: `RULES.md` anchors (Task 2).
- Produces: `docs/ARCHITECTURE.md`, `docs/adr/README.md`.

- [ ] **Step 1: Append the specs**

```python
FILES["docs/ARCHITECTURE.md"] = FileSpec(headings=(
    "System context", "Components", "Data flow", "Data and storage",
    "External dependencies", "Cross-cutting concerns", "Quality attributes",
    "Key terms", "Known limitations and tech debt", "Decisions", "Keeping this current"),
    links=("RULES.md", "docs/adr/README.md"))
FILES["docs/adr/README.md"] = FileSpec(headings=(
    "What is an ADR", "When to write one", "Statuses", "Process", "Naming", "Index"),
    links=("docs/adr/0000-template.md", "docs/adr/0001-record-architecture-decisions.md"))
_ADR_HEADINGS = ("Context", "Decision", "Options considered", "Consequences", "Follow-ups")
FILES["docs/adr/0000-template.md"] = FileSpec(headings=_ADR_HEADINGS, purpose_line=False)
FILES["docs/adr/0001-record-architecture-decisions.md"] = FileSpec(
    headings=_ADR_HEADINGS, links=("docs/adr/README.md", "docs/adr/0000-template.md"),
    add_slot=False, purpose_line=False)
```

- [ ] **Step 2: Run the checker to verify it fails**

Run: `python tools/check_template.py --files docs/ARCHITECTURE.md docs/adr/README.md docs/adr/0000-template.md docs/adr/0001-record-architecture-decisions.md`
Expected: exit 1 with four `missing file` lines

- [ ] **Step 3: Write `template/docs/ARCHITECTURE.md`**

Content follows spec §4 ARCHITECTURE. Pinned choices:
- Owner line `> **Owner:** {{TECH_LEAD}} · **Review:** in the PR that changes structure; full pass quarterly`.
- System context: a `flowchart LR` with nodes `user["Users"]`, `sys["This system"]`, `ext["External services"]`. Data flow: a `sequenceDiagram` with participants User, This system, Data store.
- Tables: Components `| Component | Responsibility | Owner |`; External dependencies `| Dependency | Purpose | Owner | Failure impact |`; Quality attributes `| Attribute | Target | How measured |` with rows Availability, Latency (p95), Throughput, Scalability; Key terms `| Term | Meaning |`; Known limitations and tech debt `| Limitation | Impact | Plan |`.
- Cross-cutting concerns: rows for authentication and authorization, observability (`../RULES.md#logging-and-observability`), configuration (`../RULES.md#configuration`) and error handling (`../RULES.md#error-handling`).
- Decisions links `adr/README.md`. Keeping this current cites `DOC-1` (`../RULES.md#documentation`).

- [ ] **Step 4: Write the three ADR files**

- `adr/README.md` follows spec §4. "When to write one" lists: hard to reverse; affects several components or teams; adds a major dependency or technology; changes a shared interface or data model; deviates from RULES. Statuses is the table `| Status | Meaning |`. Process: copy `0000-template.md`, take the next number, open a PR with status Proposed, merge as Accepted. Accepted ADRs are never edited; supersede them with a new ADR and mark the old one `Superseded by NNNN`. Naming: `NNNN-kebab-case-title.md`, 4-digit zero-padded. Index is `| ADR | Title | Status | Date |` with the 0001 row (date `{{ADOPTION_DATE}}`) and an `ADD` slot below.
- `0000-template.md`: H1 `# NNNN. Decision title`, then the list `- **Status:** Proposed`, `- **Date:** YYYY-MM-DD`, `- **Deciders:**`. One `ADD` slot per section. Options considered holds `### Option 1` and `### Option 2`, each with Pros/Cons bullets. Consequences uses bold labels Positive / Negative / Risks.
- `0001-record-architecture-decisions.md`: H1 `# 0001. Record architecture decisions`; Status Accepted; Date `{{ADOPTION_DATE}}`; Deciders `{{TEAM_NAME}}`. Options considered: ADRs in the repo (chosen), wiki pages, no formal record. The text links `README.md` and `0000-template.md`.

- [ ] **Step 5: Run the checker to verify it passes**

Run: the command from Step 2.
Expected: `OK: 4 file(s) checked`

- [ ] **Step 6: Review the content against spec §4** for these four files, then commit

```bash
git add tools/template_spec.py template/docs/ARCHITECTURE.md template/docs/adr
git commit -m "docs(template): add architecture overview and ADRs" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 5: DEVELOPMENT and ONBOARDING

**Files:**
- Modify: `tools/template_spec.py`
- Create: `template/docs/DEVELOPMENT.md`, `template/docs/ONBOARDING.md`

**Interfaces:**
- Consumes: `RULES.md#testing`, `#configuration`, `#logging-and-observability` (Task 2); `docs/RUNBOOK.md` (Task 6, tolerated by `--files` mode).
- Produces: `docs/DEVELOPMENT.md#prerequisites`.

- [ ] **Step 1: Append the specs**

```python
FILES["docs/DEVELOPMENT.md"] = FileSpec(headings=(
    "Prerequisites", "Setup", "Environment variables", "Commands", "Testing",
    "Debugging", "Troubleshooting"), links=("RULES.md",))
FILES["docs/ONBOARDING.md"] = FileSpec(headings=(
    "Day 0: access", "Day 1: set up", "Week 1: goals", "Your buddy",
    "How we communicate", "Team contacts", "Tools and accounts", "Team rituals"),
    links=("docs/DEVELOPMENT.md", "INTENT.md", "docs/ARCHITECTURE.md", "RULES.md", "docs/RUNBOOK.md"))
```

- [ ] **Step 2: Run the checker to verify it fails**

Run: `python tools/check_template.py --files docs/DEVELOPMENT.md docs/ONBOARDING.md`
Expected: exit 1 with two `missing file` lines

- [ ] **Step 3: Write `template/docs/DEVELOPMENT.md`**

Content follows spec §4 DEVELOPMENT. Pinned choices:
- Prerequisites: `| Tool | Version | Install |`.
- Setup: numbered steps covering clone `{{REPO_URL}}`, copy `.env.example` to `.env`, `{{INSTALL_CMD}}`, `{{DEV_CMD}}`, and verify with `{{TEST_CMD}}`; an `ADD` slot for extra steps.
- Environment variables: `| Name | Required | Description | Example |`. Rule: `.env.example` lists every variable with safe example values, and `.env` is never committed (`../RULES.md#configuration`).
- Commands: `| Task | Command |` with all five command placeholders.
- Testing: `| Type | Scope | When it runs |` with rows Unit, Integration, End-to-end; expectations link `../RULES.md#testing`.
- Debugging: four generic tips: reproduce with a failing test first; follow the correlation ID through the logs (`../RULES.md#logging-and-observability`); bisect with `git bisect`; change one thing at a time.
- Troubleshooting: `| Symptom | Cause | Fix |` plus an `ADD` slot.

- [ ] **Step 4: Write `template/docs/ONBOARDING.md`**

Content follows spec §4 ONBOARDING. Pinned choices:
- Owner line `> **Owner:** {{TEAM_NAME}} · **Review:** the newest joiner updates this file`.
- Day 0 is a `- [ ]` checklist: repo `{{REPO_URL}}`, team channel `{{TEAM_CHANNEL}}`, issue tracker `{{ISSUE_TRACKER_URL}}`, CI, cloud console, secrets manager, plus an `ADD` slot. Day 1 links `DEVELOPMENT.md`. Week 1 is a checklist: read INTENT, ARCHITECTURE and RULES; ship a small first PR; shadow one on-call shift (`RUNBOOK.md`).
- Your buddy: the buddy is the first reviewer and holds a daily 15-minute check-in during week 1.
- How we communicate: `| For | Use |` with rows urgent production issue → `{{ONCALL_CONTACT}}`, questions → `{{TEAM_CHANNEL}}`, work tracking → `{{ISSUE_TRACKER_URL}}`.
- Team contacts `| Role | Name | Ask about |` (first row: Tech lead, `{{TECH_LEAD}}`), Tools and accounts, and Team rituals `| Ritual | When | Purpose |` each get an `ADD` slot.

- [ ] **Step 5: Run the checker to verify it passes**

Run: the command from Step 2.
Expected: `OK: 2 file(s) checked`

- [ ] **Step 6: Review the content against spec §4** for these two files, then commit

```bash
git add tools/template_spec.py template/docs/DEVELOPMENT.md template/docs/ONBOARDING.md
git commit -m "docs(template): add development setup and onboarding" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 6: DEPLOYMENT, RUNBOOK and SECURITY

**Files:**
- Modify: `tools/template_spec.py`
- Create: `template/docs/DEPLOYMENT.md`, `template/docs/RUNBOOK.md`, `template/docs/SECURITY.md`

**Interfaces:**
- Consumes: `RULES.md#security`, `#exceptions-log` (Task 2); `CHANGELOG.md` (Task 3).
- Produces: `docs/DEPLOYMENT.md#rollback` (linked from CONTRIBUTING and RUNBOOK); `docs/RUNBOOK.md`.

- [ ] **Step 1: Append the specs**

```python
FILES["docs/DEPLOYMENT.md"] = FileSpec(headings=(
    "Environments", "Promotion flow", "Release checklist", "Versioning", "Rollback",
    "Feature flags", "Database migrations", "Deploy freezes", "Pipeline specifics"),
    links=("docs/RUNBOOK.md", "CHANGELOG.md"))
FILES["docs/RUNBOOK.md"] = FileSpec(headings=(
    "Severity levels", "Incident process", "Roles", "Status updates", "Postmortems",
    "Runbook entries", "Dashboards and alerts", "Escalation"),
    links=("docs/DEPLOYMENT.md",))
FILES["docs/SECURITY.md"] = FileSpec(headings=(
    "Reporting a vulnerability", "Secrets", "Access control", "Dependency vulnerabilities",
    "Data classification", "Secure coding", "Tools in use", "Compliance", "This project's data"),
    links=("RULES.md", "docs/RUNBOOK.md"))
```

- [ ] **Step 2: Run the checker to verify it fails**

Run: `python tools/check_template.py --files docs/DEPLOYMENT.md docs/RUNBOOK.md docs/SECURITY.md`
Expected: exit 1 with three `missing file` lines

- [ ] **Step 3: Write `template/docs/DEPLOYMENT.md`**

Content follows spec §4 DEPLOYMENT. Pinned choices:
- Owner line `> **Owner:** {{TECH_LEAD}} · **Review:** after any failed deploy or rollback`.
- Environments: `| Environment | URL | Purpose | Who can deploy | Data |` with rows dev / staging / production. The built-in Data defaults are synthetic / synthetic or anonymized / real; URLs are left empty with an `ADD` slot.
- Promotion flow: a `flowchart LR` of merge to main → dev (automatic) → staging → production (approval).
- Release checklist: Before / During / After `- [ ]` lists. Versioning: SemVer, tags `vX.Y.Z`, and moving Unreleased entries into the version in `../CHANGELOG.md`.
- Rollback: "Roll back first, debug later." Target: production rolled back within 15 minutes of the decision. Steps: redeploy the previous tag, verify, announce, and open an incident per `RUNBOOK.md` if users were affected. An `ADD` slot holds the rollback commands.
- Feature flags: every flag has an owner and a removal date; remove it within 30 days of full rollout.
- Database migrations: expand → migrate → contract; each migration is compatible with the previously deployed version; never drop or rename in the same release as the code change.
- Deploy freezes: no non-urgent production deploys; urgent fixes need `{{TECH_LEAD}}` approval; an `ADD` slot for freeze windows.

- [ ] **Step 4: Write `template/docs/RUNBOOK.md`**

Content follows spec §4 RUNBOOK. Pinned choices:
- Owner line `> **Owner:** {{TEAM_NAME}} · **Review:** after every SEV1/SEV2, and quarterly`.
- Severity levels: `| Level | Definition | Respond within | Who is paged |`. SEV1: outage, data loss or security breach; 15 minutes; on-call plus tech lead. SEV2: core feature degraded for many users; 30 minutes; on-call. SEV3: partial impact with a workaround; next business day; none. SEV4: cosmetic; normal backlog; none.
- Incident process: a `flowchart LR` of Detect → Triage → Mitigate → Resolve → Postmortem, plus "mitigate before root-causing".
- Roles: `| Role | Responsibilities |` for Incident commander, Communications, Scribe.
- Status updates and Postmortems templates go in fenced blocks. Postmortems are blameless and due within 5 business days for SEV1/SEV2; sections Summary, Impact, Timeline, Root cause, What went well, What went wrong, Action items (owner, due).
- Runbook entries: a fenced template (Symptom / Impact / Diagnosis / Mitigation / Escalation), then one example `### High error rate after a deploy` whose mitigation links `DEPLOYMENT.md#rollback`, then an `ADD` slot.
- Dashboards and alerts: `| Alert | Meaning | First step | Dashboard |` plus an `ADD` slot.
- Escalation: `| Level | Who | When |` with `{{ONCALL_CONTACT}}`, `{{TECH_LEAD}}`, and `{{SECURITY_CONTACT}}` (suspected breach).

- [ ] **Step 5: Write `template/docs/SECURITY.md`**

Content follows spec §4 SECURITY. Pinned choices:
- Owner line `> **Owner:** {{SECURITY_CONTACT}} · **Review:** every 6 months`.
- Reporting: send it to `{{SECURITY_CONTACT}}`; never post details in open channels or public issues; a confirmed issue is handled as an incident per `RUNBOOK.md`.
- Secrets: use the secrets manager only; never put secrets in code, config, logs, tickets or chat; rotate on schedule and when people leave. A leaked secret is rotated immediately, then revoked, then access logs are checked, then an incident is opened.
- Access control: least privilege, MFA everywhere, no shared accounts, quarterly access review, same-day offboarding.
- Dependency vulnerabilities: scan in CI. Patch targets `| Severity | Fix within |`: Critical 7 days, High 30 days, Medium 90 days, Low next planned update. Missed targets are recorded in `../RULES.md#exceptions-log`.
- Data classification: `| Level | Examples | Handling |` for Public, Internal, Confidential, Restricted. Secure coding links `../RULES.md#security`.
- Tools in use is `| Purpose | Tool |` with rows secrets manager, dependency scanning, code scanning and access management, tool cells empty. Compliance and This project's data (`| Data | Level | Where stored | Retention |`) get `ADD` slots.

- [ ] **Step 6: Run the checker to verify it passes**

Run: the command from Step 2.
Expected: `OK: 3 file(s) checked`

- [ ] **Step 7: Review the content against spec §4** for these three files, then commit

```bash
git add tools/template_spec.py template/docs/DEPLOYMENT.md template/docs/RUNBOOK.md template/docs/SECURITY.md
git commit -m "docs(template): add deployment, runbook and security docs" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 7: README, CLAUDE.md, TEMPLATE_GUIDE and full acceptance

**Files:**
- Modify: `tools/template_spec.py`
- Create: `template/README.md`, `template/CLAUDE.md`, `template/TEMPLATE_GUIDE.md`

**Interfaces:**
- Consumes: every file from Tasks 2–6; `python tools/check_template.py --usage` (Task 1).
- Produces: the finished template.

- [ ] **Step 1: Append the specs**

```python
FILES["README.md"] = FileSpec(headings=(
    "About", "Prerequisites", "Quickstart", "Documentation", "Key links",
    "Getting help", "Ownership"),
    links=("INTENT.md", "RULES.md", "CONTRIBUTING.md", "CHANGELOG.md", "CLAUDE.md",
           "docs/ARCHITECTURE.md", "docs/ONBOARDING.md", "docs/DEVELOPMENT.md",
           "docs/DEPLOYMENT.md", "docs/RUNBOOK.md", "docs/SECURITY.md", "docs/adr/README.md"))
FILES["CLAUDE.md"] = FileSpec(headings=(
    "Read first", "Working agreements", "Commands", "Gotchas", "No-go areas", "Domain notes"),
    links=("INTENT.md", "RULES.md", "docs/ARCHITECTURE.md", "docs/DEVELOPMENT.md"), max_lines=60)
FILES["TEMPLATE_GUIDE.md"] = FileSpec(headings=(
    "What this is", "Adopt it", "Fill order", "Placeholders", "Find unfinished work",
    "Keep docs healthy", "When you are done"), add_slot=False)
```

- [ ] **Step 2: Run the checker to verify it fails**

Run: `python tools/check_template.py --files README.md CLAUDE.md TEMPLATE_GUIDE.md`
Expected: exit 1 with three `missing file` lines

- [ ] **Step 3: Write `template/README.md`**

- H1 `# {{PROJECT_NAME}}`, then the purpose line `> **Purpose:** {{PROJECT_DESCRIPTION}}`.
- About: an `ADD` slot. Prerequisites: an `ADD` slot plus a link to `docs/DEVELOPMENT.md#prerequisites`.
- Quickstart: a fenced block of `git clone {{REPO_URL}}`, `{{INSTALL_CMD}}`, `{{DEV_CMD}}`, `{{TEST_CMD}}`, then "Full setup: docs/DEVELOPMENT.md".
- Documentation: `| Doc | Read it when |` with the 12 links from the spec, one row each.
- Key links: `| Link | URL |` with rows Production, Staging, Dashboards plus an `ADD` slot.
- Getting help: `{{TEAM_CHANNEL}}`, `{{ISSUE_TRACKER_URL}}`, and incidents to `{{ONCALL_CONTACT}}`. Ownership: `{{TEAM_NAME}}`, `{{TECH_LEAD}}`.

- [ ] **Step 4: Write `template/CLAUDE.md`** (≤ 60 lines)

- H1 `# CLAUDE.md — {{PROJECT_NAME}}`; purpose line: "How AI assistants work in this repo. Facts live in the linked docs; this file points to them."
- Read first: the 4 links, one line each.
- Working agreements: the 6 agreements of spec §4 CLAUDE.md, each one line, citing rule IDs where one exists.
- Commands: `| Task | Command |` with all five command placeholders.
- Gotchas, No-go areas and Domain notes: one `ADD` slot each.

- [ ] **Step 5: Generate the placeholder usage**

Run: `python tools/check_template.py --usage`
Expected: 17 lines, none ending `(unused)`. Keep the output for Step 6.

- [ ] **Step 6: Write `template/TEMPLATE_GUIDE.md`**

- Purpose line: "How to adopt this template. Delete this file when you are done."
- What this is: three lines plus `| Marker | Means | Example |` for the two markers.
- Adopt it, numbered: 1) `cp -r template/. path/to/new-repo/`, and check `.github/` came along; 2) find-and-replace every placeholder; 3) fill `ADD` slots in fill order; 4) edit built-in defaults that don't fit; 5) run the unfinished-work search; 6) delete this file.
- Fill order: INTENT, RULES, ARCHITECTURE, README, then CONTRIBUTING, DEVELOPMENT, ONBOARDING, DEPLOYMENT, RUNBOOK, SECURITY, CLAUDE, CHANGELOG, ADR 0001, each with a one-line reason.
- Placeholders: `| Placeholder | Meaning | Used in |`, 17 rows; meanings from `REGISTRY`, "Used in" from the Step 5 output.
- Find unfinished work: a fenced block containing `grep -rnE "\{\{[A-Z_]+\}\}|ADD:" .`, with "No output means you're done."
- Keep docs healthy: each doc's Owner/Review line; docs change in the same PR as code (`DOC-1`).
- When you are done: delete this file and commit.

- [ ] **Step 7: Run the full acceptance checks**

Run: `python -m unittest discover -s tests -v`
Expected: `Ran 19 tests` … `OK`

Run: `python tools/check_template.py`
Expected: `OK: 19 file(s) checked` and exit 0. This strict run also verifies the cross-task links and anchors (`docs/DEPLOYMENT.md#rollback`, `docs/RUNBOOK.md`, and others).

- [ ] **Step 8: Review the content against spec §4** for these three files, then commit

```bash
git add tools/template_spec.py template/README.md template/CLAUDE.md template/TEMPLATE_GUIDE.md
git commit -m "docs(template): add README, CLAUDE.md and adoption guide" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```
