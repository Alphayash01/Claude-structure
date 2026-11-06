---
name: dev-fast
description: Fast, low-token mode for small, clear changes (typo, obvious bug, config tweak, 1-3 files). Skips design and plan documents. Run only when the user types /dev-fast.
disable-model-invocation: true
argument-hint: "[#issue or @task-file] what to change"
effort: low
---

# /dev-fast

Make a small, clear change quickly, using as few tokens as possible.

Request: $ARGUMENTS

## Stop and escalate

Stop, say why in one line, and suggest `/dev-medium` if:

- the change needs more than 3 files, or a choice between design options;
- it touches security, permissions, secrets, personal data, payments or database migrations;
- the cause is still unclear after one look.

## Steps

1. **Issue and task file.** Get the issue number from the request or the branch name (rules in CLAUDE.md). If there is none, ask once.
2. **Read only what the change needs.** No broad exploration, no subagents, no brainstorming, no spec or plan files.
3. **Make the smallest change that does the job**, following RULES.md. A bug fix includes a test that fails without the fix (TEST-1).
4. **Run only the affected tests**, using the test command in CLAUDE.md. If they still fail after two fixes, stop and suggest `/dev-medium`.
5. **Task file, in one approval at the end.**
   - None yet: propose a minimal one copied from `docs/tasks/TEMPLATE.md`, filling only the metadata, Goal, one Plan item and one Progress line.
   - Already exists: propose one Progress line.
   - Save only after the user approves.

## Report

At most 5 lines: files changed, test command and result, anything not done.
