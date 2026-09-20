---
name: focused-change
description: Implement changes to the .AGENTS CLI while preserving existing files, role isolation and explicit context loading.
---

# Focused CLI change

Read the affected command and its documented behavior in `README.md` and `docs/protocol.md`. Reproduce the intended operation in a temporary project, including an existing AGENTS.md when initialization is affected.

Preserve these contracts where relevant to the change:

- Initialization never overwrites a user's existing file.
- Selecting one role does not include another role's memory or skill bodies.
- Only explicitly selected skill bodies enter assembled context; role memory comes from `memory/MEMORY.md`.
- Names and filesystem links cannot redirect operations outside the selected project.

Run `python -m unittest discover -s tests -v` and `python tools/agents.py check`. Add a behavior test for a changed contract or demonstrated regression; avoid assertions that merely copy implementation details.

Report observable behavior and remaining limitations. Store reusable, verified findings in `memory/MEMORY.md` with evidence rather than copying the full session log.
