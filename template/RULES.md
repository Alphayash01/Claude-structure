# Engineering Rules — {{PROJECT_NAME}}

> **Purpose:** The standards every change in this repo follows. Built-in rules are sensible defaults; edit them to fit, then hold the line.
> **Owner:** {{TECH_LEAD}} · **Review:** every 6 months

## How these rules work

- **GEN-1** Rules beat personal preference. If a rule is wrong, change it; don't ignore it. *Why:* consistency is worth more than any single style choice.
- **GEN-2** Cite rule IDs in reviews, e.g. `blocking: violates TEST-1`. *Why:* a shared reference ends taste debates quickly.
- **GEN-3** Change a rule by PR. Significant changes also get an [ADR](docs/adr/README.md). *Why:* rules are decisions; decisions need a record.
- **GEN-4** A waived rule goes in the [Exceptions log](#exceptions-log) with an expiry date. *Why:* silent exceptions become the new rule.

## Code

- **CODE-1** Prefer readable over clever. Optimize for the next reader. *Why:* code is read far more often than it is written.
- **CODE-2** Keep units small with one purpose. If a name needs "and", split it. *Why:* small units are easier to test, review and replace.
- **CODE-3** Names reveal intent: `overdue_invoices`, not `list2`. *Why:* good names remove the need for comments.
- **CODE-4** No dead or commented-out code. Git remembers. *Why:* stale code misleads readers and rots silently.
- **CODE-5** Comments explain *why*, not *what*. *Why:* the code already says what; only you know why.

## Structure

- **STRUCT-1** Organize by feature or domain, not by technical type. *Why:* changes stay local when related code lives together.
- **STRUCT-2** Each module exposes a small, clear public interface; internals stay private. *Why:* you can change internals without breaking callers.
- **STRUCT-3** No circular dependencies between modules. *Why:* cycles make code impossible to understand, test or split in isolation.

## Error handling

- **ERR-1** Validate input at trust boundaries (APIs, files, queues, user input). *Why:* bad data caught at the edge is cheap; deep inside it corrupts state.
- **ERR-2** Fail fast on impossible states; don't limp on. *Why:* an early crash is easier to debug than late corruption.
- **ERR-3** Never swallow errors. Handle them, or pass them on with context. *Why:* a silent failure is the most expensive kind.
- **ERR-4** Errors carry context: what failed, with which input, and why. *Why:* "something went wrong" costs hours in an incident.
- **ERR-5** Separate user-facing messages from internal details. *Why:* users need guidance; stack traces leak internals.

## Logging and observability

- **LOG-1** Use structured logs (key-value), not free-text sentences. *Why:* structured logs can be searched, filtered and alerted on.
- **LOG-2** Use levels consistently: `error` needs action, `warn` is unexpected but handled, `info` is a business event, `debug` is for developers. *Why:* noisy levels hide real problems.
- **LOG-3** Never log secrets, tokens or personal data. *Why:* logs are widely readable and kept for a long time.
- **LOG-4** Pass a correlation ID through every request and job. *Why:* one ID lets you follow a failure across services.

## Testing

- **TEST-1** Every bug fix includes a test that fails without the fix. *Why:* it proves the fix and stops the bug returning.
- **TEST-2** New behavior ships with tests in the same PR. *Why:* "tests later" means no tests.
- **TEST-3** Tests are deterministic: no real clocks, random seeds or network calls without control. *Why:* flaky tests train people to ignore failures.
- **TEST-4** Test behavior through public interfaces, not internals. *Why:* tests survive refactoring and document real use.
- **TEST-5** CI must be green before merge. No exceptions for "small" changes. *Why:* a red main branch blocks everyone.

## Dependencies

- **DEP-1** Justify every new dependency in the PR: what it does, why not write it, and its maintenance health. *Why:* each dependency is code you now own.
- **DEP-2** Commit lockfiles and pin versions. *Why:* builds must be reproducible.
- **DEP-3** Prefer well-maintained, widely used libraries with compatible licenses. *Why:* abandoned libraries become security debt.
- **DEP-4** Automate dependency updates and review them like any other PR. *Why:* small regular updates beat painful big-bang upgrades.

## Security

- **SEC-1** No secrets in code, config files, tests or commit history. *Why:* repositories leak; rotated secrets are cheaper than breaches.
- **SEC-2** Grant least privilege to services, people and tokens. *Why:* it limits the damage when something is compromised.
- **SEC-3** Use parameterized queries; never build queries or commands from strings. *Why:* injection is still among the most common attacks.
- **SEC-4** Encode output for its context (HTML, shell, URLs). *Why:* it prevents injection on the way out.

Details: [docs/SECURITY.md](docs/SECURITY.md)

## Configuration

- **CFG-1** Read configuration from the environment; ship safe defaults. *Why:* the same build runs in every environment.
- **CFG-2** No environment-specific branches in code (`if env == "prod"`). *Why:* such branches hide behavior you can only test in production.

## Performance

- **PERF-1** Measure before optimizing; keep the benchmark or profile in the PR. *Why:* intuition about bottlenecks is usually wrong.
- **PERF-2** Watch for N+1 access patterns and unbounded queries or loops. *Why:* they work in development and fall over in production.

## Documentation

- **DOC-1** Update docs in the same PR as the behavior change. *Why:* docs that lag the code are worse than no docs.
- **DOC-2** Record significant decisions as ADRs. *Why:* future readers need the *why*, not just the *what*.

## Language and framework conventions

Name the formatter, linter and style guide, and let tools enforce them rather than reviewers.

| Concern | Tool or guide | Enforced in CI? |
|---|---|---|
| <!-- ADD: formatter --> | | |
| <!-- ADD: linter --> | | |
| <!-- ADD: style guide --> | | |

## Project structure

<!-- ADD: the top-level folder tree with one line per folder explaining what lives there -->

## Naming conventions

| Thing | Convention | Example |
|---|---|---|
| <!-- ADD: files, modules, types, functions, variables, branches, env vars --> | | |

## Project-specific rules

Use your own prefix, e.g. `PROJ-1`, so these never clash with the built-in IDs.

<!-- ADD: rules unique to this project, same format: ID, rule, Why -->

## Exceptions log

| Rule | Where | Why | Until | Approved by |
|---|---|---|---|---|
| <!-- ADD: one row per waived rule; remove the row when the exception ends --> | | | | |
