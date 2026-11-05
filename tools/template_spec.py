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
FILES["docs/DEVELOPMENT.md"] = FileSpec(headings=(
    "Prerequisites", "Setup", "Environment variables", "Commands", "Testing",
    "Debugging", "Troubleshooting"), links=("RULES.md",))
FILES["docs/ONBOARDING.md"] = FileSpec(headings=(
    "Day 0: access", "Day 1: set up", "Week 1: goals", "Your buddy",
    "How we communicate", "Team contacts", "Tools and accounts", "Team rituals"),
    links=("docs/DEVELOPMENT.md", "INTENT.md", "docs/ARCHITECTURE.md", "RULES.md", "docs/RUNBOOK.md"))
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
