# Per-task Docs — Design Spec

- **Date:** 2026-11-06
- **Status:** Approved
- **Extends:** `2026-11-05-team-docs-template-design.md` (19 → 22 files)

## 1. Intent

The template covers project-wide docs but has nothing for a single piece of work. This adds a process and files for working on one task (a feature or a bug) in a project that adopted the template.

| # | Question | Decision |
|---|---|---|
| 1 | What task files are for | Plan before coding, track progress during, record after (all three) |
| 2 | Where they live | In the repo, linked from the issue |
| 3 | After done | Move to an archive folder |
| 4 | How much paperwork | One `task.md` for every task, scaled to its size |
| 5 | Who updates it | Claude writes, a human approves each change |
| 6 | Superpowers spec and plan | Stay in `docs/superpowers/`, linked from `task.md` |

## 2. Layout in an adopted project

```
docs/tasks/
  README.md                 the process (§4)
  TEMPLATE.md               copy this for each new task
  123-export-csv.md         one file per active task: <issue#>-<kebab-slug>.md
  archive/
    README.md               "finished tasks; never edited"
    98-login-timeout.md     done tasks, moved here with the same file name
```

No hand-maintained index: active tasks are `docs/tasks/*.md`, finished ones are in `docs/tasks/archive/`. Index tables edited by hand cause merge conflicts when several PRs add rows.

## 3. `TEMPLATE.md`

H1 `# NNN. Task title`, then a metadata list: **Status** (Planned / In progress / Blocked / Done), **Issue**, **Branch** (`type/NNN-slug`), **Serves** (an INTENT goal, e.g. G2), **Owner**.

H2 sections, in order: Goal; Scope (In / Out); Design (short for a fix; a big task links its superpowers spec); Plan (checklist; a big task links its superpowers plan and mirrors its task list); Progress (dated log, newest last); Decisions (dated, each with a why; hard-to-reverse ones link an ADR); Open questions; Done summary (what changed, plus a checklist of where lasting facts went: ADR, ARCHITECTURE, RULES, RUNBOOK, CHANGELOG).

Uses plain hint comments, not `ADD:` markers: it is filled per task, not at adoption — the same rule as the `.github/` forms — so it never pollutes the unfinished-work search.

## 4. The process (`docs/tasks/README.md`)

1. **Start:** an issue exists. Create branch `type/NNN-slug`, copy `TEMPLATE.md` to `docs/tasks/NNN-slug.md`, fill Goal, Scope, Design, and comment the file's link on the issue.
2. **Plan:** fill the Plan checklist. For bigger work, open a draft PR containing only `task.md` so the design is reviewed before code.
3. **Work:** at each milestone, update Progress and Decisions. Claude proposes each edit and saves it only after approval.
4. **Update mid-flight:** a scope change edits Scope and Plan and is recorded under Decisions with a date and reason. Never rewrite the Progress log.
5. **Finish (in the final PR):** write the Done summary; move lasting facts into the permanent docs; set Status to Done; `git mv` the file into `archive/`; the issue's closing comment gives the archive path.
6. **Change a finished task:** never edit an archived file. Open a new issue and task file that links back.
7. **Big tasks with superpowers:** spec and plan stay in `docs/superpowers/`; `task.md` links them and stays the one place to start.

## 5. Changes to existing template files

| File | Change |
|---|---|
| CONTRIBUTING.md | Workflow step 1 creates the task file; branches become `type/NNN-short-description`; Definition of Done adds "task file has a Done summary and is archived"; links `docs/tasks/README.md` |
| CLAUDE.md | Read first adds the task file; working agreement: find `docs/tasks/NNN-*.md` from the branch's issue number, read it first, propose Progress/Decisions updates at milestones and before ending, save only after approval. Stays ≤ 60 lines |
| .github/PULL_REQUEST_TEMPLATE.md | Checklist item "Task file updated" (repo-absolute link) |
| README.md | Documentation row for `docs/tasks/README.md` |
| docs/ONBOARDING.md | Week 1 adds reading `docs/tasks/README.md` |

## 6. Acceptance

The original spec's §6 checks apply to all 22 files, with one addition to §6.6's allowed names: the superpowers plugin, mentioned only in `docs/tasks/` and always as optional ("if you use…"). Links inside task files are root-relative (`/docs/...`) so they survive the move to `archive/`; the checker resolves them from the template root. `TEMPLATE.md` and `archive/README.md` need no `ADD` slot; `TEMPLATE.md` needs no purpose line (it is a form). CONTRIBUTING, CLAUDE, README and the PR template must link `docs/tasks/README.md`.
