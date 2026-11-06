# Onboarding — {{PROJECT_NAME}}

> **Purpose:** Get a new team member from zero to their first merged PR in one week: access, setup, people and habits.
> **Owner:** {{TEAM_NAME}} · **Review:** the newest joiner updates this file

## Day 0: access

Request these before or on the first day. Your buddy or {{TECH_LEAD}} can approve.

- [ ] Repository: {{REPO_URL}}
- [ ] Team channel: {{TEAM_CHANNEL}}
- [ ] Issue tracker: {{ISSUE_TRACKER_URL}}
- [ ] CI system (view logs, rerun jobs)
- [ ] Cloud console, read-only to start
- [ ] Secrets manager (never copy secrets into files or chat)
- [ ] On-call and alerting tool: {{ONCALL_CONTACT}}

<!-- ADD: other accounts, VPN, hardware, licenses -->

## Day 1: set up

- [ ] Follow [DEVELOPMENT.md](DEVELOPMENT.md) until `{{TEST_CMD}}` passes
- [ ] Run the app locally and click through the main journey
- [ ] Fix anything in the setup docs that was wrong or missing; that's your first PR

<!-- ADD: team-specific day-1 steps -->

## Week 1: goals

- [ ] Read [INTENT.md](../INTENT.md): why we exist and what we don't do
- [ ] Read [ARCHITECTURE.md](ARCHITECTURE.md) and the ADRs it links
- [ ] Read [RULES.md](../RULES.md) and [CONTRIBUTING.md](../CONTRIBUTING.md)
- [ ] Read [docs/tasks/README.md](tasks/README.md) and, once some exist, a few archived task files
- [ ] Ship a small first PR (a good-first-issue or a docs fix)
- [ ] Shadow one on-call shift and read the [RUNBOOK](RUNBOOK.md)
- [ ] Have a 1:1 with {{TECH_LEAD}} about expectations and growth

## Your buddy

Every joiner gets a buddy from the team for their first month.

- The buddy is the joiner's **first reviewer** and first person to ask, with no question too small.
- Daily 15-minute check-in during week 1, then weekly for the rest of the month.
- The buddy makes sure the joiner's first PR merges in week 1.

<!-- ADD: how buddies are assigned -->

## How we communicate

| For | Use |
|---|---|
| Urgent production issue | {{ONCALL_CONTACT}} |
| Questions and discussion | {{TEAM_CHANNEL}} |
| Work tracking | {{ISSUE_TRACKER_URL}} |
| Significant decisions | An [ADR](adr/README.md) |

Prefer public channels over direct messages so answers help everyone.

## Team contacts

| Role | Name | Ask about |
|---|---|---|
| Tech lead | {{TECH_LEAD}} | Architecture, priorities, rules |
| <!-- ADD: product owner, designers, ops or SRE, security, neighboring teams --> | | |

## Tools and accounts

<!-- ADD: tools the team uses (editor setup, design, docs, dashboards) and how to get access -->

## Team rituals

| Ritual | When | Purpose |
|---|---|---|
| <!-- ADD: standup, planning, review, retro, demos --> | | |
