# CLAUDE.md — {{PROJECT_NAME}}

> **Purpose:** How AI assistants work in this repo. Facts live in the linked docs; this file points to them.

## Read first

- [INTENT.md](INTENT.md): why the project exists; goals (`G#`) and non-goals (`NG#`).
- [RULES.md](RULES.md): coding standards with rule IDs. Follow them; cite IDs when relevant.
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md): components, data flow, key terms.
- [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md): setup, environment variables, commands.
- The task file for this branch. NNN is the digits right after `type/` in the branch name (`feat/123-export-csv` → `docs/tasks/123-*.md`); also check `docs/tasks/archive/`, which is read-only once merged. No number, no match, or several matches: ask. Never create a task file unasked. Process: [docs/tasks/README.md](docs/tasks/README.md).

## Working agreements

- Read the task file before starting. Propose updates to its Progress and Decisions at each milestone and before ending a session. Propose every edit to the task file and save it only after the human approves.
- Follow RULES.md. If a rule blocks you, say so; don't silently work around it.
- Keep diffs small and focused on the task. No drive-by refactors.
- Run `{{TEST_CMD}}` and `{{LINT_CMD}}` before saying work is done, and report the real result.
- When intent is unclear, ask, or check INTENT.md, before guessing.
- Update docs in the same change as behavior (DOC-1).
- Never commit secrets, tokens or personal data (SEC-1, LOG-3).

## Commands

| Task | Command |
|---|---|
| Install | `{{INSTALL_CMD}}` |
| Run locally | `{{DEV_CMD}}` |
| Test | `{{TEST_CMD}}` |
| Lint and format | `{{LINT_CMD}}` |
| Build | `{{BUILD_CMD}}` |

## Gotchas

<!-- ADD: non-obvious things that trip people up (slow tests, generated files, local quirks) -->

## No-go areas

Don't modify these without asking first:

<!-- ADD: paths such as migrations, generated code, vendored code, infrastructure config -->

## Domain notes

<!-- ADD: domain rules an assistant must respect; link Key terms in ARCHITECTURE.md rather than repeating them -->
