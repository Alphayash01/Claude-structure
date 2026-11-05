# Development — {{PROJECT_NAME}}

> **Purpose:** Everything needed to build, run, test and debug the project locally. If a step here is wrong, fix it in your first PR.

## Prerequisites

| Tool | Version | Install |
|---|---|---|
| Git | Latest | <https://git-scm.com/downloads> |
| <!-- ADD: runtime, package manager, database, CLIs; pin exact versions --> | | |

## Setup

1. Clone the repository and move into it:

   ```sh
   git clone {{REPO_URL}}
   cd <repository-folder>
   ```

2. Copy `.env.example` to `.env` and fill in local values (see [Environment variables](#environment-variables)).
3. Install dependencies: `{{INSTALL_CMD}}`
4. Verify everything works: `{{TEST_CMD}}` should pass on a fresh clone.
5. Start the app: `{{DEV_CMD}}`. It keeps running; open a second terminal for other commands.

<!-- ADD: extra steps such as seeding a local database, creating accounts, or trusting local certificates -->

## Environment variables

- `.env.example` lists **every** variable with a safe example value and is committed.
- `.env` holds your real local values and is **never** committed.
- Configuration comes from the environment per [CFG-1](../RULES.md#configuration).

| Name | Required | Description | Example |
|---|---|---|---|
| <!-- ADD: one row per variable --> | | | |

## Commands

| Task | Command |
|---|---|
| Install dependencies | `{{INSTALL_CMD}}` |
| Run locally | `{{DEV_CMD}}` |
| Run tests | `{{TEST_CMD}}` |
| Lint and format check | `{{LINT_CMD}}` |
| Production build | `{{BUILD_CMD}}` |

## Testing

| Type | Scope | When it runs |
|---|---|---|
| Unit | One unit in isolation, fast, no network | Locally on every change; CI on every push |
| Integration | Several units with real dependencies (database, queues) | CI on every push |
| End-to-end | Critical user journeys through the deployed system | CI before release |

Expectations (bug-fix tests, determinism, green CI) live in [RULES.md](../RULES.md#testing).

<!-- ADD: how to run a single test, where test data and fixtures live, how to run integration tests locally -->

## Debugging

- **Reproduce with a failing test first.** It pins the bug and becomes the regression test (TEST-1).
- **Follow the correlation ID** through the logs to see one request end to end ([LOG-4](../RULES.md#logging-and-observability)).
- **Bisect** when something used to work: `git bisect` finds the breaking commit quickly.
- **Change one thing at a time** and re-run. Many changes at once hide the real cause.

<!-- ADD: how to attach a debugger, enable verbose logging, or inspect local data -->

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| <!-- ADD: one row per problem people hit more than once --> | | |
