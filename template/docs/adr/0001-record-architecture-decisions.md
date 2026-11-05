# 0001. Record architecture decisions

- **Status:** Accepted
- **Date:** {{ADOPTION_DATE}}
- **Deciders:** {{TEAM_NAME}}

## Context

Significant decisions get made in meetings, chats and PR threads, then lost. New team members can't tell why the system looks the way it does, so they either repeat old debates or undo good decisions by accident.

## Decision

We will record significant decisions as Architecture Decision Records in `docs/adr/`, following the process and criteria in [README.md](README.md) and the format in [0000-template.md](0000-template.md).

## Options considered

### Option 1: ADRs in the repository (chosen)

- **Pros:** versioned with the code; reviewed in PRs; easy to find and link.
- **Cons:** needs the discipline to write them.

### Option 2: Wiki pages

- **Pros:** easy to edit; familiar to non-engineers.
- **Cons:** drift away from the code; no review step; often go stale.

### Option 3: No formal record

- **Pros:** no effort.
- **Cons:** decisions are lost; debates repeat; onboarding is slower.

## Consequences

**Positive:** the reasoning behind the system is searchable and reviewed; onboarding gets faster.

**Negative:** writing an ADR adds a small step to significant changes.

**Risks:** ADRs go unwritten under time pressure. The PR checklist asks for one to keep this visible.

## Follow-ups

- Link ADRs from the sections of `docs/ARCHITECTURE.md` they affect.
