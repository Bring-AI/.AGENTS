# Role ownership and explicit loading

- Date: 2026-09-21
- Owner: architect / initial-design
- Status: active
- Scope: directory protocol v1
- Evidence: `docs/protocol.md`, `tools/agents.py` context command
- Review after: a native client integration or directory protocol revision

## Finding

Roles are responsibilities, not model identities. Two agents can have the same role while working on different tasks. Role folders therefore organize knowledge but do not isolate execution or serialize writes.

## Consequence

Retain AGENTS.md for shared rules and routing. Explicitly load shared facts plus one role's entry files, then select relevant records and skills. Use worktrees and distinct record filenames for concurrent tasks. Do not claim that the custom directory is automatically discovered by clients.
