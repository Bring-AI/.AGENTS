# Developer memory

## Role ownership and explicit loading

- Date: 2026-09-21
- Owner: developer
- Status: active
- Scope: directory protocol
- Evidence: `docs/protocol.md`, `README.md`
- Review after: a client integration or directory protocol change

Roles describe responsibilities, not model identities. Multiple instances can share a role, so role folders do not isolate execution or serialize writes. Keep shared rules in the root AGENTS.md and explicitly read the selected role's AGENTS.md and memory/MEMORY.md. Select skill bodies as needed. Use separate worktrees and review to reconcile concurrent memory edits.

## Project scope

This project supplies a directory convention and Markdown templates. Adoption requires copying and customizing files, with no runtime or installation step. Keep examples aligned with that workflow.
