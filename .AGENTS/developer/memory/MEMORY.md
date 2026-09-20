# Developer memory

- The CLI is a standalone file: `tools/agents.py`. It must remain usable after copying it into another project.
- Existing files are preserved during initialization; an existing AGENTS.md requires manual entrypoint integration.
- Tests use temporary projects and the standard-library `unittest` runner.

Evidence: `tools/agents.py`, `tests/test_agents.py`. Review when changing initialization or distribution.

- [Windows path aliases](records/2026-09-21-windows-path-aliases.md): compare canonical paths after link checks; the first Windows/Python 3.10 CI run exposed a short-name alias failure.
