---
name: dev-high
description: Full-process mode for the best outcome on big or risky work - superpowers brainstorming, spec, plan, subagent execution with per-task review, a final fresh review, and permanent-doc updates. Uses more time and tokens. Run only when the user types /dev-high.
disable-model-invocation: true
argument-hint: "[#issue or @task-file] what to build"
effort: high
---

# /dev-high

Take the full process. Quality comes before speed and token use.

Request: $ARGUMENTS

## Before you start

- This mode needs the superpowers plugin. If `/superpowers:brainstorming` is not available, say so, show the install command from `docs/CLAUDE_SKILLS.md`, and offer `/dev-medium` instead.
- Find or create the task file (rules in CLAUDE.md). It stays the one place to start.
- Every edit to the task file is proposed first and saved only after the user approves.

## Steps

1. **Brainstorm.** Use `superpowers:brainstorming`. The spec goes to `docs/superpowers/specs/`; propose linking it under the task file's Design.
2. **Plan.** Use `superpowers:writing-plans`. Link the plan under the task file's Plan and mirror its task list there.
3. **Isolate.** Work on the task's branch; use `superpowers:using-git-worktrees` when other work is in progress.
4. **Execute.** Prefer `superpowers:subagent-driven-development`: a fresh implementer and reviewer per task. Use `superpowers:executing-plans` when subagents are unavailable or the user prefers inline work.
5. **Test and verify.** Follow `superpowers:test-driven-development` throughout, and `superpowers:verification-before-completion` before calling any task done.
6. **Review.** Run `superpowers:requesting-code-review` on the whole branch with a fresh reviewer, and fix Critical and Important findings test-first. Run `/security-review` when the change touches security.
7. **Permanent docs.** Record lasting facts: an ADR for each hard-to-reverse decision, plus ARCHITECTURE, RULES and RUNBOOK updates and a CHANGELOG entry as needed.
8. **Finish.** Propose the task file's Done summary and the move to `docs/tasks/archive/`, then use `superpowers:finishing-a-development-branch`.

## Report

What was built; links to the spec, plan and task file; test and review results; decisions and their ADRs; follow-ups.
