# Template Guide

> **Purpose:** How to adopt this template in a new repository. Delete this file when you are done.

## What this is

A starter set of team docs with senior-level defaults already written in. You adapt it rather than write from scratch.

- **Built-in content** is plain text: rules, processes, checklists and defaults that suit most teams. Keep what fits, edit what doesn't.
- **Slots** are places only you can fill: your users, your stack, your contacts.
- **Placeholders** are single values used across many files, filled by find-and-replace.

| Marker | Means | Example |
|---|---|---|
| Double braces around an upper-case name | A single value; replace it everywhere at once | `{{PROJECT_NAME}}` |
| `<!-- ADD: … -->` | Write project content here; hidden when rendered on GitHub | `<!-- ADD: 2–3 sentences on what this service does -->` |

## Adopt it

1. Copy the template into your new repository, including the hidden `.github/` and `.claude/` folders:

   ```sh
   cp -r template/. path/to/new-repo/
   ```

   Check that `.github/` and `.claude/` came along; some file managers skip hidden folders. Without `.claude/`, the `/dev-fast`, `/dev-medium` and `/dev-high` commands are missing.
2. Find-and-replace every placeholder in the [Placeholders](#placeholders) table across the repo.
3. Fill the `ADD` slots, following the [Fill order](#fill-order).
4. Read the built-in defaults (review turnaround, patch times, rollback target, severity levels) and edit any that don't fit your team.
5. Run the search in [Find unfinished work](#find-unfinished-work) until it finds nothing.
6. Delete this file and commit.

## Fill order

Each file builds on the ones before it.

1. **INTENT.md**: everything else depends on knowing why and for whom.
2. **RULES.md**: add your language conventions, folder structure and naming.
3. **docs/ARCHITECTURE.md**: context, components and key terms.
4. **README.md**: the front door, now that you can describe the project.
5. **CONTRIBUTING.md**: review assignment, CI checks, release cadence.
6. **docs/DEVELOPMENT.md**: prerequisites, setup steps, environment variables.
7. **docs/ONBOARDING.md**: accounts, contacts, rituals.
8. **docs/DEPLOYMENT.md**: environments, pipeline, rollback commands.
9. **docs/RUNBOOK.md**: alerts, dashboards, service-specific entries.
10. **docs/SECURITY.md**: tools, compliance, your data.
11. **CLAUDE.md**: gotchas and no-go areas, once you know them.
12. **CHANGELOG.md**: add the first entry with your first release.
13. **docs/adr/0001**: already written; just check that the date and deciders are filled.
14. **docs/tasks/README.md**: works as-is; add any team conventions for task files.
15. **docs/CLAUDE_SKILLS.md**: list your extra and stack-specific Claude skills.

## Placeholders

| Placeholder | Meaning | Used in |
|---|---|---|
| `{{PROJECT_NAME}}` | Human-readable project name | README.md, INTENT.md, RULES.md, CONTRIBUTING.md, CHANGELOG.md, CLAUDE.md, docs/ARCHITECTURE.md, docs/ONBOARDING.md, docs/DEVELOPMENT.md, docs/DEPLOYMENT.md, docs/RUNBOOK.md, docs/SECURITY.md, docs/adr/README.md, docs/tasks/README.md, docs/CLAUDE_SKILLS.md |
| `{{PROJECT_DESCRIPTION}}` | One-line description | README.md |
| `{{TEAM_NAME}}` | Owning team | README.md, docs/ONBOARDING.md, docs/RUNBOOK.md, docs/adr/0001-record-architecture-decisions.md |
| `{{TEAM_CHANNEL}}` | Team chat channel | README.md, docs/ONBOARDING.md, docs/DEPLOYMENT.md |
| `{{TECH_LEAD}}` | Technical lead / primary owner | README.md, INTENT.md, RULES.md, CONTRIBUTING.md, docs/ARCHITECTURE.md, docs/ONBOARDING.md, docs/DEPLOYMENT.md, docs/RUNBOOK.md |
| `{{REPO_URL}}` | Repository URL | README.md, CHANGELOG.md, docs/ONBOARDING.md, docs/DEVELOPMENT.md, .github/PULL_REQUEST_TEMPLATE.md, .github/ISSUE_TEMPLATE/feature_request.md |
| `{{ISSUE_TRACKER_URL}}` | Issue tracker URL | README.md, CONTRIBUTING.md, docs/ONBOARDING.md, docs/tasks/README.md |
| `{{MAIN_BRANCH}}` | Default branch name | CONTRIBUTING.md, .github/PULL_REQUEST_TEMPLATE.md, .github/ISSUE_TEMPLATE/feature_request.md |
| `{{REQUIRED_APPROVALS}}` | Number of PR approvals required | CONTRIBUTING.md |
| `{{ONCALL_CONTACT}}` | On-call rotation / pager | README.md, docs/ONBOARDING.md, docs/RUNBOOK.md |
| `{{SECURITY_CONTACT}}` | Internal security contact | docs/RUNBOOK.md, docs/SECURITY.md |
| `{{INSTALL_CMD}}` | Install dependencies | README.md, CLAUDE.md, docs/DEVELOPMENT.md |
| `{{DEV_CMD}}` | Run locally | README.md, CLAUDE.md, docs/DEVELOPMENT.md |
| `{{TEST_CMD}}` | Run tests | README.md, CLAUDE.md, docs/ONBOARDING.md, docs/DEVELOPMENT.md |
| `{{LINT_CMD}}` | Lint / format check | CLAUDE.md, docs/DEVELOPMENT.md |
| `{{BUILD_CMD}}` | Production build | CLAUDE.md, docs/DEVELOPMENT.md |
| `{{ADOPTION_DATE}}` | Date the template was adopted (ADR 0001) | docs/adr/README.md, docs/adr/0001-record-architecture-decisions.md |

## Find unfinished work

Run from the repository root:

```sh
grep -rnE --exclude=0000-template.md "\{\{[A-Z_]+\}\}|ADD:" .
```

No output means you're done. `docs/adr/0000-template.md` is excluded because its slots must stay: every new ADR is copied from it. Until you delete it, this guide shows up in the results too.

## Keep docs healthy

- Each doc names its **owner** and **review cadence** at the top. Put those reviews in the owners' calendars.
- Docs change in the same PR as the code they describe ([DOC-1](RULES.md#documentation)).
- The newest joiner updates ONBOARDING.md; the RUNBOOK is reviewed after every SEV1/SEV2.
- Rule changes go through a PR. Significant ones also get an ADR.

## When you are done

Delete this file and commit, e.g. `docs: adopt team docs template`.
