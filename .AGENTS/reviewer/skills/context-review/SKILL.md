---
name: context-review
description: Review changes to role context assembly and memory handling for accidental cross-role loading, unsupported guarantees and loss of existing content.
---

# Context review

Create a temporary project with two roles and distinct markers in each role's memory and skill body. Assemble one role's context and check that the other role's content is absent. Check both default output and explicit skill or record selection.

For initialization changes, start with a custom AGENTS.md and role memory, run initialization twice, and compare existing file bytes. For path handling changes, try a parent-directory role name and a linked directory; neither should access an unintended path.

Compare claims in the README with observed behavior. Highlight any claim of automatic discovery, execution isolation or semantic validation that lacks an implementation.

Report reproducible defects with impact and affected files; separate optional improvements from correctness findings. Record durable review lessons only after confirming them.
