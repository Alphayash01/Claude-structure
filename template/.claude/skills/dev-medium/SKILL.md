---
name: dev-medium
description: Balanced mode for features or bugs across a few files - short approved design, test-first, full test and lint run, self-review, task file at milestones. Run only when the user types /dev-medium.
disable-model-invocation: true
argument-hint: "[#issue or @task-file] what to build or fix"
effort: medium
---

# /dev-medium

Deliver a solid change with a light process.

Request: $ARGUMENTS

## Stop and escalate

Stop, say why in one line, and suggest `/dev-high` if:

- it creates a new subsystem or a new module boundary;
- it needs a hard-to-reverse decision, one that deserves an ADR;
- the requirements are still unclear after two questions;
- it is security-sensitive: authentication, permissions, secrets, personal data.

## Steps

1. **Task file.** Find it from the issue number (rules in CLAUDE.md). If none exists, propose one from `docs/tasks/TEMPLATE.md` with Goal, Scope and Design.
2. **Understand.** Read the relevant code and the parts of INTENT.md, RULES.md and docs/ARCHITECTURE.md that apply. Ask questions one at a time, and only when the answer changes the design.
3. **Design, then wait.** Present at most 10 lines: approach, files to touch, tests to add, risks. Start only after the user approves.
4. **Plan.** Propose the Plan checklist for the task file.
5. **Build test-first.** For each behavior change, write a failing test, watch it fail, then make it pass.
6. **Verify.** Run the full test and lint commands in CLAUDE.md. All must pass.
7. **Self-review.** Read your diff against RULES.md and the task's Scope. Fix what you find; list anything out of scope as a follow-up.
8. **Task file at milestones.** Propose Plan ticks, Progress and Decisions; save each only after approval. If this finishes the task, propose the Done summary and the move to `docs/tasks/archive/`.

## Report

The change in a few lines, test and lint results, decisions made, follow-ups.
