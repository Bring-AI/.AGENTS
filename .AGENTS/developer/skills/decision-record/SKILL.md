---
name: decision-record
description: Record protocol or role-ownership decisions when changing the .AGENTS layout, loading contract or collaboration boundaries.
---

# Decision record

Read `docs/protocol.md` and this role's `memory/MEMORY.md`. Identify the exact contract being changed and its callers, including the CLI and project entrypoint.

Compare the proposed change with keeping the current convention. State migration cost and distinguish guarantees enforced by code from conventions enforced by collaborators.

Capture an accepted decision as a concise section in this role's `memory/MEMORY.md` with date, owner, scope, status, evidence and a review condition. Mark replaced conclusions as superseded; retain history through Git. Do not present an unapproved proposal as an accepted fact.

Hand off affected files and observable acceptance conditions to the implementation owner. A decision record does not expand the user's authorized scope.
