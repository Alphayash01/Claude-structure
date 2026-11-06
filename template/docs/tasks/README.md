# Task Files — {{PROJECT_NAME}}

> **Purpose:** How to plan, track and record one piece of work (a feature or a bug) in a single `task.md` file.

## What goes here

- **One file per task**, named after its issue: `NNN-short-slug.md`, e.g. `123-export-csv.md`. Copy it from [TEMPLATE.md](TEMPLATE.md).
- **Active tasks** sit in this folder. **Finished tasks** move to [archive/](archive/README.md) with the same file name.
- There is no index to maintain: the folder listing *is* the index.

A task file does three jobs: it is the **plan** before coding, the **progress log** during the work, and the **record** afterwards. Anyone (you tomorrow, a teammate, or Claude in a new session) should be able to pick up the task from this file alone.

The issue in {{ISSUE_TRACKER_URL}} stays the short *what and why*; this file holds the detail.

## Start a task

1. Make sure an issue exists. It carries the number `NNN`.
2. Create the branch `type/NNN-short-slug`, e.g. `feat/123-export-csv` (see [CONTRIBUTING.md](../../CONTRIBUTING.md#branches)).
3. Copy `TEMPLATE.md` to `docs/tasks/NNN-short-slug.md` and set **Status: Planned**.
4. Fill in **Goal**, **Scope** and **Design**. Cite the goal it serves from [INTENT.md](../../INTENT.md#goals), e.g. G2.
5. Comment a link to the file on the issue.

Size the file to the task: a typo fix may need three lines; a new feature may need a page.

## Plan

- Fill in the **Plan** checklist: small steps, each with a checkable result.
- For bigger work, open a **draft PR containing only the task file** and ask for review before writing code. Agreeing on the design first is cheaper than reworking code.
- Set **Status: In progress** when coding starts.

## Work

- At each milestone, add a dated line to **Progress** and tick the Plan items you finished.
- Record every non-obvious choice under **Decisions** with a date and a *why*. A hard-to-reverse decision also gets an [ADR](../adr/README.md).
- Note blockers under **Open questions** and set **Status: Blocked** until they are resolved.
- **With Claude:** Claude proposes each change to the task file and saves it only after you approve. It reads the task file before starting work and proposes an update before ending a session.

## Change a task mid-flight

Scope changes happen; hiding them is the problem.

- Edit **Scope** and **Plan** to match the new reality.
- Add a dated entry under **Decisions** explaining what changed and why.
- Never rewrite or delete old **Progress** lines. The log is history.
- If the change is large, update the issue too, or split the extra work into a new issue and task file.

## Finish

In the PR that completes the task:

1. Write the **Done summary**: what changed, and anything left for later.
2. Move lasting facts into the permanent docs. The task file is a snapshot; it is never updated after it is archived. Work through the Done summary checklist: ADR, ARCHITECTURE, RULES, RUNBOOK, and an entry in [CHANGELOG.md](../../CHANGELOG.md).
3. Set **Status: Done**.
4. Move the file: `git mv docs/tasks/NNN-short-slug.md docs/tasks/archive/`
5. When the PR merges, close the issue with a comment linking the archived file.

## Change a finished task

Archived task files are **never edited**. For follow-up work or a bug found later:

1. Open a new issue.
2. Create a new task file and link the archived one under **Design**, e.g. `Follows up [98-login-timeout](archive/98-login-timeout.md)`.

## Big tasks with superpowers

When Claude uses the superpowers brainstorming and planning skills, they write a spec to `docs/superpowers/specs/` and a plan to `docs/superpowers/plans/`. Keep them there:

- Link the spec under **Design** and the plan under **Plan**.
- Mirror the plan's task list in the **Plan** checklist so progress is visible here.
- The task file stays the one place to start.

## Team conventions

<!-- ADD: anything your team adds to this process, e.g. labels, who reviews task-only draft PRs, how long Blocked may last before escalation -->
