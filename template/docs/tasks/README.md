# Task Files — {{PROJECT_NAME}}

> **Purpose:** How to plan, track and record one piece of work (a feature or a bug) in a single `task.md` file.

## What goes here

- **One file per task**, named after its issue: `NNN-short-slug.md`, e.g. `123-export-csv.md`. `NNN` is the issue number as is, not zero-padded: issue 7 becomes `7-short-slug.md`. Copy it from [TEMPLATE.md](TEMPLATE.md).
- **One file per issue, even across several PRs.** A later branch for the same issue keeps using the existing file; never create a second one.
- **Where to find a task:** while in progress, the file lives on its branch, so find it through the issue. Tasks spanning several PRs sit in this folder between merges. **Finished tasks** move to [archive/](archive/README.md) with the same file name.
- **Links inside task files start with `/`** (root-relative), e.g. `[ADR 0005](/docs/adr/0005-use-feature-flags.md)`. GitHub resolves them from the repo root, so they keep working after the file moves to `archive/`. Relative links like `../adr/…` break on the move.

A task file does three jobs: it is the **plan** before coding, the **progress log** during the work, and the **record** afterwards. Anyone (you tomorrow, a teammate, or Claude in a new session) should be able to pick up the task from this file alone.

The issue in {{ISSUE_TRACKER_URL}} stays the short *what and why*; this file holds the detail.

## Start a task

1. Make sure an issue exists. It carries the number `NNN`.
2. Create the branch `type/NNN-short-slug`, e.g. `feat/123-export-csv` (see [CONTRIBUTING.md](../../CONTRIBUTING.md#branches)).
3. Copy `TEMPLATE.md` to `docs/tasks/NNN-short-slug.md` and set **Status: Planned**. If the file already exists (a later PR of the same task), keep using it.
4. Fill in **Goal**, **Scope** and **Design**. Cite the goal it serves from [INTENT.md](../../INTENT.md#goals), e.g. G2.
5. Comment a link to the file on the issue. It points at the branch while the work is in progress; the closing comment later gives the archived path.

Size the file to the task: a typo fix may need three lines; a new feature may need a page.

## Plan

- Fill in the **Plan** checklist: small steps, each with a checkable result.
- For bigger work, open a **draft PR containing only the task file** and ask for review before writing code. Agreeing on the design first is cheaper than reworking code. Once the design is agreed, keep working on the same branch and PR; the code joins the task file there.
- Set **Status: In progress** when coding starts.

## Work

- At each milestone, add a dated line to **Progress** and tick the Plan items you finished.
- Record every non-obvious choice under **Decisions** with a date and a *why*. A hard-to-reverse decision also gets an [ADR](../adr/README.md).
- Note blockers under **Open questions** and set **Status: Blocked** until they are resolved.
- **With Claude:** Claude proposes every edit to the task file and saves it only after you approve. It reads the task file before starting work and proposes an update before ending a session.
- **PR links to the issue:** use `Refs #NNN` in PRs that don't finish the task, and `Closes #NNN` only in the PR that does. Otherwise the first merge closes the issue early.

## Change a task mid-flight

Scope changes happen; hiding them is the problem.

- Edit **Scope** and **Plan** to match the new reality.
- Add a dated entry under **Decisions** explaining what changed and why.
- Never rewrite or delete old **Progress** lines. The log is history.
- If the change is large, update the issue too, or split the extra work into a new issue and task file.

## Finish

In the PR that completes the task:

1. Write the **Done summary**: what changed, and anything left for later.
2. Move lasting facts into the permanent docs. The task file is a snapshot; once merged into `archive/`, it is never updated. Work through the Done summary checklist: ADR, ARCHITECTURE, RULES, RUNBOOK, and an entry in [CHANGELOG.md](../../CHANGELOG.md).
3. Set **Status: Done**.
4. Move the file: `git mv docs/tasks/NNN-short-slug.md docs/tasks/archive/`. Review fixes on this same PR may still edit it; the freeze starts at merge.
5. The PR says `Closes #NNN`, so merging closes the issue. Then comment the archived file's link on the issue.

## Change a finished task

Archived task files are **never edited once merged**. For follow-up work or a bug found later:

1. Open a new issue.
2. Create a new task file and link the archived one under **Design**, root-relative: `Follows up [98-login-timeout](/docs/tasks/archive/98-login-timeout.md)`.

## Big tasks with superpowers

If you use the superpowers plugin for Claude Code, its brainstorming and planning skills write a spec to `docs/superpowers/specs/` and a plan to `docs/superpowers/plans/`. Keep them there:

- Link the spec under **Design** and the plan under **Plan**.
- Mirror the plan's task list in the **Plan** checklist so progress is visible here.
- The task file stays the one place to start.

## Team conventions

<!-- ADD: anything your team adds to this process, e.g. labels, who reviews task-only draft PRs, how long Blocked may last before escalation -->
