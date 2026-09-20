# Canonicalize both sides of Windows path comparisons

- Date: 2026-09-21
- Owner: developer / initial-cli
- Status: active
- Scope: CLI project-root containment checks
- Evidence: https://github.com/Bring-AI/.AGENTS/actions/runs/35520923577 ; `tests/test_agents.py` portable-copy and short-path regression tests
- Review after: path validation or supported Python versions change

## Finding

The first Windows/Python 3.10 CI run used a temporary path under `RUNNER~1`. Resolving a candidate expanded this short-name alias, while the project root retained the alias. A lexical comparison incorrectly rejected initialization of a new project. Local Python 3.14 and Linux did not expose this failure.

## Consequence

Reject symbolic links and reparse points before canonicalization, then compare resolved candidate and resolved root. Keep a regression for initialization through Windows short-name aliases; do not remove link checks to accommodate aliases.
