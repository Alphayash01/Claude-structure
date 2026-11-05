# Architecture Decision Records

> **Purpose:** What ADRs are, when to write one, and the index of every decision made in {{PROJECT_NAME}}.

## What is an ADR

A short document recording one significant decision: the context, the options, what we chose, and the consequences. ADRs keep the *why* findable long after the people in the meeting have moved on.

## When to write one

Write an ADR when a decision:

- is hard or expensive to reverse;
- affects several components or teams;
- adds a major dependency or technology;
- changes a shared interface or data model;
- deviates from [RULES.md](../../RULES.md).

When in doubt, write a short one. A 10-line ADR beats a lost decision.

## Statuses

| Status | Meaning |
|---|---|
| Proposed | Open for discussion in a PR |
| Accepted | Agreed; this is how we do it now |
| Deprecated | No longer recommended, but not replaced |
| Superseded | Replaced by a newer ADR; links to it |

## Process

1. Copy [0000-template.md](0000-template.md) to the next number.
2. Fill it in with status **Proposed** and open a PR. Discussion happens in review.
3. When agreed, set status **Accepted** and merge. Add a row to the [Index](#index).
4. Accepted ADRs are never edited. To change a decision, write a new ADR and mark the old one `Superseded by NNNN`.

## Naming

`NNNN-kebab-case-title.md`, 4-digit zero-padded, numbered in order: `0002-use-feature-flags.md`.

## Index

| ADR | Title | Status | Date |
|---|---|---|---|
| [0001](0001-record-architecture-decisions.md) | Record architecture decisions | Accepted | {{ADOPTION_DATE}} |

<!-- ADD: one row per new ADR, newest at the bottom -->
