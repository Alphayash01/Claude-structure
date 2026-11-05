# Security — {{PROJECT_NAME}}

> **Purpose:** How we report vulnerabilities, handle secrets and access, patch dependencies, and classify data.
> **Owner:** {{SECURITY_CONTACT}} · **Review:** every 6 months

## Reporting a vulnerability

- Report it to **{{SECURITY_CONTACT}}** directly.
- Do **not** post details in open channels, public issues or PR descriptions.
- Include what is affected, how to reproduce it, and the potential impact.
- A confirmed vulnerability is handled as an incident per [RUNBOOK.md](RUNBOOK.md); a breach is SEV1.

## Secrets

- Secrets live only in the secrets manager. Never in code, config files, logs, tickets or chat ([SEC-1](../RULES.md#security)).
- Each service and environment gets its own secrets; never share them across environments.
- Rotate secrets on a schedule, and whenever someone with access leaves.

**If a secret leaks:**

1. **Rotate it immediately**, before investigating.
2. Revoke the old value and any tokens issued with it.
3. Check access logs for use of the leaked secret.
4. Open an incident and remove the secret from history if it was committed.

## Access control

- Least privilege for people, services and tokens ([SEC-2](../RULES.md#security)).
- MFA on every account that supports it. No shared accounts.
- Review access quarterly; remove what isn't used.
- Offboarding removes all access on the person's last day.

## Dependency vulnerabilities

Scan dependencies in CI on every build and on a daily schedule.

| Severity | Fix within |
|---|---|
| Critical | 7 days |
| High | 30 days |
| Medium | 90 days |
| Low | Next planned update |

If a target can't be met, record it in the [RULES exceptions log](../RULES.md#exceptions-log) with a mitigation and a new date.

## Data classification

| Level | Examples | Handling |
|---|---|---|
| Public | Marketing pages, public docs | No restrictions |
| Internal | Internal docs, non-sensitive metrics | Staff only |
| Confidential | Customer data, contracts, source code | Need-to-know; encrypted in transit and at rest |
| Restricted | Credentials, payment data, health or government IDs | Strictly limited; encrypted; access logged and reviewed |

## Secure coding

Follow the security rules in [RULES.md](../RULES.md#security): no secrets in code, least privilege, parameterized queries, encoded output. Treat every input from outside a trust boundary as hostile.

## Tools in use

| Purpose | Tool |
|---|---|
| Secrets manager | <!-- ADD: tool name --> |
| Dependency scanning | <!-- ADD: tool name --> |
| Code scanning | <!-- ADD: tool name --> |
| Access management | <!-- ADD: tool name --> |

## Compliance

<!-- ADD: regulations and standards that apply (privacy law, industry standards, customer contracts) and what each requires of this project -->

## This project's data

| Data | Level | Where stored | Retention |
|---|---|---|---|
| <!-- ADD: one row per kind of data the system handles --> | | | |
