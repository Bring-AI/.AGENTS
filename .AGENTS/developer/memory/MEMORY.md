# Developer memory

- The CLI is a standalone file: `tools/agents.py`. It must remain usable after copying it into another project.
- Existing files are preserved during initialization; an existing AGENTS.md requires manual entrypoint integration.
- Tests use temporary projects and the standard-library `unittest` runner.

Evidence: `tools/agents.py`, `tests/test_agents.py`. Review when changing initialization or distribution.

## Role ownership and explicit loading

- Date: 2026-09-21
- Owner: developer / directory-design
- Status: active
- Scope: directory protocol
- Evidence: `docs/protocol.md`, `tools/agents.py`
- Review after: a client integration or directory protocol change

Roles describe responsibilities, not model identities. Multiple instances can share a role, so role folders do not isolate execution or serialize writes. Keep shared rules in the root AGENTS.md and load the selected role's AGENTS.md and memory/MEMORY.md explicitly. Select skill bodies as needed. Use separate worktrees and review to reconcile concurrent memory edits.

## Windows path aliases

- Date: 2026-09-21
- Owner: developer / initial-cli
- Status: active
- Scope: project-root containment checks
- Evidence: https://github.com/Bring-AI/.AGENTS/actions/runs/35520923577 ; `tests/test_agents.py` portable-copy and short-path regression tests
- Review after: path validation or supported Python versions change

The first Windows/Python 3.10 CI run used a temporary path under `RUNNER~1`. Resolving the candidate but not the root caused a false containment failure. Reject symbolic links and reparse points before canonicalization, then compare both resolved paths. Keep the short-path regression; do not remove link checks to accommodate aliases.
