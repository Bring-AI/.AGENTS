# Shared context

- This repository defines a project-local role knowledge convention, not an agent runtime.
- The public interface is documented in `README.md` and `docs/protocol.md`.
- The optional CLI lives in `tools/agents.py`, uses the Python standard library, and targets Python 3.10+.
- `.AGENTS/` requires explicit loading. No automatic discovery by a client is assumed.
- Verification: `python -m unittest discover -s tests -v` and `python tools/agents.py check`.

Sources: the current repository implementation and protocol. Review these facts when the CLI or protocol changes.
