# Team Docs Starter Template — Design Spec

- **Date:** 2026-11-05
- **Status:** Draft — awaiting review
- **Path:** Architectural (new project, no existing code)

## 1. Intent

**Goal.** A reusable set of Markdown documentation files that a senior developer would set up in a new **team / internal** repository. Each file ships with senior-level, project-agnostic best practices already written in, plus clearly marked spaces where the user adds project-specific content.

**How it is used.** Copy the contents of `template/` into a new repo, fill the placeholders and `ADD` slots, adjust the built-in defaults to the project's needs, delete `TEMPLATE_GUIDE.md`.

**Success criteria.**
- Copy → usable repo docs in about 30 minutes of filling in.
- Built-in content is useful as-is for most teams; nothing reads as filler.
- Every spot needing project input is findable with one search.
- Each fact lives in exactly one file; others link to it.

**Non-goals.**
- Open-source-only files (CODE_OF_CONDUCT, SUPPORT, FUNDING, LICENSE).
- Non-Markdown config (CODEOWNERS, .editorconfig, CI workflows).
- A generator script or CLI.
- Language- or framework-specific content (no assumed stack).

**Assumptions (confirmed or unchallenged in brainstorming).**
- Repos are hosted on GitHub (`.github/` templates).
- `CLAUDE.md` is included for AI-assisted development.

## 2. Repository layout

The working folder is the template's home. Copyable files live under `template/`; design docs (this spec, the plan) live under `docs/superpowers/` and are **not** part of the template.

```
template/
  README.md
  INTENT.md
  RULES.md
  CONTRIBUTING.md
  CHANGELOG.md
  CLAUDE.md
  TEMPLATE_GUIDE.md
  docs/
    ARCHITECTURE.md
    ONBOARDING.md
    DEVELOPMENT.md
    DEPLOYMENT.md
    RUNBOOK.md
    SECURITY.md
    adr/
      README.md
      0000-template.md
      0001-record-architecture-decisions.md
  .github/
    PULL_REQUEST_TEMPLATE.md
    ISSUE_TEMPLATE/
      bug_report.md
      feature_request.md
```

19 files total. Extended to 22 by `2026-11-06-task-docs-design.md` (adds `docs/tasks/`), then to 26 by the dev modes: `docs/CLAUDE_SKILLS.md` and `.claude/skills/{dev-fast,dev-medium,dev-high}/SKILL.md` (project skills; `effort` low/medium/high; `disable-model-invocation: true` so they run only when typed). Plugin names (superpowers, agent-skills) are allowed in those four files and in `docs/tasks/` only.

## 3. Content model

### 3.1 Two layers in every file

| Layer | What it is | How it looks |
|---|---|---|
| **Built-in** | Senior-level, stack-agnostic practices that apply to most teams. Editable defaults, not law. | Plain Markdown. Rules carry a one-line `Why:` so the user can judge fit. |
| **Project slot** | A marked space for project-specific content. | `<!-- ADD: what to write here -->` followed by an empty line or a skeleton (table header, list stub). |

### 3.2 Markers (exactly two kinds)

| Marker | Purpose | Example |
|---|---|---|
| `{{UPPER_SNAKE_CASE}}` | A single value, filled by find-and-replace across all files. | `{{PROJECT_NAME}}` |
| `<!-- ADD: ... -->` | A slot for free-form project content. Invisible when rendered on GitHub. | `<!-- ADD: 2–3 sentences on what this service does -->` |

Find all unfinished work with: `grep -rnE --exclude=0000-template.md "\{\{[A-Z_]+\}\}|ADD:" .` (the ADR template keeps its slots, because every new ADR is copied from it).

### 3.3 Placeholder registry

Only these placeholders may appear. `TEMPLATE_GUIDE.md` lists each one with its meaning and the files that use it.

| Placeholder | Meaning |
|---|---|
| `{{PROJECT_NAME}}` | Human-readable project name |
| `{{PROJECT_DESCRIPTION}}` | One-line description |
| `{{TEAM_NAME}}` | Owning team |
| `{{TEAM_CHANNEL}}` | Team chat channel |
| `{{TECH_LEAD}}` | Technical lead / primary owner |
| `{{REPO_URL}}` | Repository URL |
| `{{ISSUE_TRACKER_URL}}` | Issue tracker URL |
| `{{MAIN_BRANCH}}` | Default branch name |
| `{{REQUIRED_APPROVALS}}` | Number of PR approvals required |
| `{{ONCALL_CONTACT}}` | On-call rotation / pager |
| `{{SECURITY_CONTACT}}` | Internal security contact |
| `{{INSTALL_CMD}}` | Install dependencies |
| `{{DEV_CMD}}` | Run locally |
| `{{TEST_CMD}}` | Run tests |
| `{{LINT_CMD}}` | Lint / format check |
| `{{BUILD_CMD}}` | Production build |
| `{{ADOPTION_DATE}}` | Date the template was adopted (ADR 0001) |

Repeating a value through the same placeholder is allowed (e.g. `{{TEST_CMD}}` in README, CLAUDE.md, DEVELOPMENT.md). Repeating prose is not.

### 3.4 Writing style

- Imperative, concise, scannable: headings, tables, checklists; no prose walls.
- Length targets: ≤ 150 lines per file; `RULES.md` ≤ 220; `CLAUDE.md` ≤ 60 (loaded into AI context every session).
- Examples only where format matters (commit messages, ADR, runbook entry, PR checklist). Never invent project facts.
- Diagrams in Mermaid (renders on GitHub, diffable).
- Each file opens with a one-line statement of its purpose and, where useful, an "Owner / review cadence" line.

## 4. File specifications

Each entry lists **Built-in** content and **Slots** (`ADD`).

### README.md
- **Built-in:** title + `{{PROJECT_DESCRIPTION}}`; Quickstart using `{{INSTALL_CMD}}`, `{{DEV_CMD}}`, `{{TEST_CMD}}`; documentation map table linking every doc with a one-line purpose; Getting help (`{{TEAM_CHANNEL}}`, `{{ISSUE_TRACKER_URL}}`); Ownership (`{{TEAM_NAME}}`, `{{TECH_LEAD}}`).
- **Slots:** what the project does (2–3 sentences); prerequisites; key links (environments, dashboards).

### INTENT.md — why and what
- **Built-in:** section structure; guidance on writing good goals ("outcomes, not features") and non-goals; a *decision filter* ("does this work serve a goal? does it violate a non-goal?"); review cadence (revisit when scope changes or quarterly).
- **Slots:** problem statement; users & stakeholders; goals (measurable); non-goals; success metrics table (metric, target, how measured); constraints (time, budget, compliance, technical); assumptions & open questions.

### RULES.md — how we write code
- **Built-in** (each rule one line + `Why:`):
  - Precedence: rules beat personal preference; change a rule via PR; significant changes get an ADR.
  - Code: readability over cleverness; small single-purpose units; names reveal intent; no dead or commented-out code.
  - Structure: organise by feature/domain by default; each module exposes a clear public interface; no circular dependencies.
  - Error handling: validate at trust boundaries; fail fast; never swallow errors; errors carry context; separate user-facing from internal messages.
  - Logging & observability: structured logs; consistent levels; no secrets/PII in logs; correlation IDs across calls.
  - Testing: every bug fix includes a regression test; new behaviour ships with tests; tests are deterministic; CI green before merge.
  - Dependencies: justify each new dependency; commit lockfiles; prefer maintained libraries; automate updates.
  - Security: no secrets in code; least privilege; parameterised queries; sanitise output. (Details → `docs/SECURITY.md`.)
  - Configuration: config from environment; no environment-specific branches in code.
  - Performance: measure before optimising; watch for N+1 access patterns.
  - Documentation: update docs in the same PR as the behaviour change.
- **Slots:** language & framework conventions (formatter, linter, style guide); project folder structure (tree); naming conventions; project-specific rules; exceptions log (rule waived, where, why, until when).

### CONTRIBUTING.md — how we work together
- **Built-in:** workflow overview (issue → branch → PR → review → merge → deploy, as Mermaid); short-lived branches off `{{MAIN_BRANCH}}` named `type/short-description`; Conventional Commits with examples; PR guidance (small — aim < 400 changed lines; self-review first; link the issue; CI green); code review (reviewer duties, 1-business-day turnaround target, comment prefixes `nit:` / `question:` / `blocking:`, approval criteria, `{{REQUIRED_APPROVALS}}` approvals); squash-merge default; how to revert; Definition of Done checklist.
- **Slots:** review assignment rules; CI specifics; release cadence.

### CHANGELOG.md
- **Built-in:** Keep a Changelog 1.1.0 header; SemVer note; `[Unreleased]` with Added / Changed / Deprecated / Removed / Fixed / Security; rule: entry lands in the same PR as the change, written for the system's users.
- **Slots:** first release entry.

### CLAUDE.md — instructions for AI assistants
- **Built-in:** read-first pointers to `INTENT.md`, `RULES.md`, `docs/ARCHITECTURE.md`, `docs/DEVELOPMENT.md` (links, no copied content); working agreements (follow RULES; keep diffs small and focused; run `{{TEST_CMD}}` and `{{LINT_CMD}}` before claiming done; ask when intent is unclear; update docs with behaviour changes; never commit secrets); commands table using command placeholders.
- **Slots:** project gotchas; no-go areas (paths not to modify without asking); domain notes.

### TEMPLATE_GUIDE.md — delete after adoption
- **Built-in:** what the template is; adoption steps (copy `template/` contents into the new repo root, including the hidden `.github/` folder); fill order — INTENT → RULES → ARCHITECTURE → README → the rest; the placeholder registry (§3.3) with files that use each; the grep command for unfinished work; doc maintenance (owners, review cadence); "delete this file when done".
- **Slots:** none.

### docs/ARCHITECTURE.md — how it is built
- **Built-in:** structure (C4-lite): system context (Mermaid skeleton with placeholder nodes); components/containers; data flow; data & storage; external dependencies table (name, purpose, owner, failure impact); cross-cutting concerns (auth, observability, config, error handling — link to RULES); quality attributes table (availability, latency, throughput, scalability targets); key terms (glossary); known limitations & tech debt; link to ADR index; "keep this current" guidance.
- **Slots:** the content of every section above.

### docs/ONBOARDING.md — people and access
- **Built-in:** Day 0 access checklist (repo `{{REPO_URL}}`, chat `{{TEAM_CHANNEL}}`, issue tracker, CI, cloud console, secrets manager); Day 1 (set up via DEVELOPMENT.md); Week 1 goals (read INTENT, ARCHITECTURE, RULES; ship a small first PR; shadow on-call); buddy system; how the team communicates; "the newest joiner updates this doc".
- **Slots:** team contacts table; tools & accounts list; team rituals (standups, planning, retros).

### docs/DEVELOPMENT.md — technical setup
- **Built-in:** prerequisites table (tool, version, install link); setup steps skeleton; environment variables table (name, required, description, example) with `.env.example` convention; common commands table (all five command placeholders: install, dev, test, lint, build); testing (unit vs integration, how to run, link to RULES testing section); generic debugging tips; troubleshooting table (symptom, cause, fix).
- **Slots:** actual prerequisites, steps, variables, troubleshooting rows.

### docs/DEPLOYMENT.md
- **Built-in:** environments table (dev / staging / prod: URL, purpose, who can deploy); promotion flow (Mermaid); release checklist (pre-deploy, deploy, post-deploy verification); versioning (SemVer + git tags); rollback principles ("roll back first, debug later", target time to roll back); feature-flag guidance; database migration rules (backward-compatible, expand → migrate → contract); deploy-freeze policy.
- **Slots:** pipeline specifics; environment URLs; approvals; rollback commands.

### docs/RUNBOOK.md — operations
- **Built-in:** severity table (SEV1–SEV4: definition, response target, who is paged); incident process (detect → triage → mitigate → resolve → postmortem); roles (incident commander, communications, scribe); status-update template; blameless postmortem template; runbook entry template (Symptom / Impact / Diagnosis / Mitigation / Escalation) with one generic filled example for format.
- **Slots:** dashboards & alerts list; service-specific runbook entries; escalation contacts (`{{ONCALL_CONTACT}}`).

### docs/SECURITY.md
- **Built-in:** reporting a vulnerability internally (`{{SECURITY_CONTACT}}`, don't post details in open channels); secrets management (secrets manager only, rotation, leaked secret → rotate first, then investigate); access control (least privilege, review access quarterly, offboarding); dependency vulnerabilities (scan in CI, patch-time targets by severity table); data classification (public / internal / confidential / restricted with handling rules); secure-coding pointer to RULES.
- **Slots:** tools in use; compliance requirements; classification of this project's data.

### docs/adr/README.md
- **Built-in:** what an ADR is; when to write one (criteria list); statuses (Proposed, Accepted, Deprecated, Superseded); process (PR + review); naming `NNNN-kebab-case-title.md`; index table.
- **Slots:** index rows.

### docs/adr/0000-template.md
- **Built-in:** Title; Status; Date; Deciders; Context; Decision; Options considered (pros/cons each); Consequences (positive, negative, risks); Follow-ups.
- **Slots:** the whole form (it is copied per decision).

### docs/adr/0001-record-architecture-decisions.md
- **Built-in:** complete ADR — "We record architecture decisions as ADRs"; Status: Accepted; Date: `{{ADOPTION_DATE}}`.
- **Slots:** none beyond the placeholder.

### .github/PULL_REQUEST_TEMPLATE.md
- **Built-in:** Summary; Why (link issue); What changed; How it was tested; Screenshots (if UI); Risk & rollback; checklist (tests added/updated, docs updated, CHANGELOG entry, no secrets, follows RULES, ADR if a significant decision).

### .github/ISSUE_TEMPLATE/bug_report.md
- **Built-in:** front matter (`name`, `about`, `labels: bug`); description; steps to reproduce; expected vs actual; environment; logs/screenshots; impact/severity.

### .github/ISSUE_TEMPLATE/feature_request.md
- **Built-in:** front matter (`labels: enhancement`); problem / user need; which INTENT goal it serves; proposed solution; alternatives considered; acceptance criteria; out of scope.

## 5. Cross-file links (single source of truth)

| Fact | Lives in | Linked from |
|---|---|---|
| Why the project exists, goals, non-goals | INTENT.md | README, CLAUDE.md, feature_request |
| Coding standards | RULES.md | CONTRIBUTING, CLAUDE.md, PR template |
| Security details | docs/SECURITY.md | RULES (security section) |
| Branch / commit / PR / review process | CONTRIBUTING.md | README, PR template |
| System design | docs/ARCHITECTURE.md | README, CLAUDE.md, ONBOARDING |
| Local setup, env vars, commands | docs/DEVELOPMENT.md | README, CLAUDE.md, ONBOARDING |
| Release & rollback | docs/DEPLOYMENT.md | RUNBOOK, CONTRIBUTING |
| Incidents | docs/RUNBOOK.md | DEPLOYMENT, SECURITY |
| Decisions | docs/adr/ | RULES, ARCHITECTURE, PR template |

All links are relative so they work after copying into any repo. **Exception:** `.github/` forms are pasted into PR/issue bodies, where relative links break, so they link with `{{REPO_URL}}/blob/{{MAIN_BRANCH}}/<path>`. No file links to `TEMPLATE_GUIDE.md`, because it is deleted after adoption.

## 6. Acceptance checks

1. All 19 files exist at the paths in §2.
2. Every `{{...}}` used appears in the registry (§3.3), and every registry entry is used at least once.
3. Every relative link resolves to an existing file within `template/`.
4. Each file is within its length target (§3.4).
5. Every file except `TEMPLATE_GUIDE.md`, `docs/adr/0001-*.md` and the three `.github/` forms has at least one `ADD` slot.
6. Built-in content names no specific language, framework, cloud, or vendor tool. Allowed exceptions: GitHub (assumed host) and the named conventions Conventional Commits, Keep a Changelog, SemVer, Mermaid, C4.
7. Issue-template front matter is valid YAML.
