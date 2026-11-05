# Intent — {{PROJECT_NAME}}

> **Purpose:** Why this project exists, who it serves, and what is out of scope. Every other doc builds on this one.
> **Owner:** {{TECH_LEAD}} · **Review:** when scope changes, and at least quarterly

This file answers *why* and *what*. *How* it is built lives in [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md); how we write code lives in [RULES.md](RULES.md).

## Problem

What is broken, slow, risky or missing today, and for whom? Describe the problem, not the solution.

<!-- ADD: 2–4 sentences on the problem and its cost today (time, money, risk, frustration) -->

## Users and stakeholders

| Who | What they need from this project | How we reach them |
|---|---|---|
| <!-- ADD: primary users --> | | |
| <!-- ADD: stakeholders (sponsor, ops, support, compliance) --> | | |

## Goals

Goals are **outcomes, not features**. Each one should be measurable in [Success metrics](#success-metrics).

- Bad: "Build a dashboard."
- Good: "Support staff resolve a ticket in under 10 minutes."

Number goals so issues and PRs can cite them (`Serves G2`).

<!-- ADD: G1, G2, G3 … one line each, most important first -->

- **G1**

## Non-goals

What this project deliberately does **not** do, even if asked. Non-goals stop scope creep and settle debates early.

<!-- ADD: NG1, NG2 … one line each, with a short reason -->

- **NG1**

## Success metrics

| Metric | Target | How measured | Owner |
|---|---|---|---|
| <!-- ADD: one row per goal; cite the goal, e.g. "G1: median ticket time" --> | | | |

## Constraints

Fixed limits the design must respect.

| Type | Constraint |
|---|---|
| Time | <!-- ADD: deadlines, milestones --> |
| Budget | <!-- ADD: cost ceilings, headcount --> |
| Compliance | <!-- ADD: legal, regulatory, contractual --> |
| Technical | <!-- ADD: mandated platforms, integrations, legacy systems --> |

## Assumptions and open questions

Write down what you believe but have not proven. Revisit them; a wrong assumption is a risk.

| # | Assumption or question | How we will find out | Status |
|---|---|---|---|
| <!-- ADD: A1, Q1 … --> | | | |

## Decision filter

Before accepting new work, ask:

1. Does it serve a goal? Cite the `G#`.
2. Does it violate a non-goal? Check every `NG#`.
3. Does it fit the constraints?

If the answer is unclear, update this file first, by PR. Scope changes that are hard to reverse also get an [ADR](docs/adr/README.md).
