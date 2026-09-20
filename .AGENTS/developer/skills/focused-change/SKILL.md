---
name: focused-change
description: Implement a feature, bug fix or bounded project change, tracing affected behavior and verifying the requested outcome.
---

# Focused change

Establish the expected outcome from the task and current project behavior. For a defect, reproduce it when feasible or identify the evidence that explains it. Read the affected interfaces and consumers before selecting an approach.

Make a coherent change using the project's existing patterns. Include affected callers, configuration and documentation when necessary. Avoid unrelated cleanup that makes the result harder to assess.

Use the project's documented checks where applicable. Add or update tests when they demonstrate changed behavior or prevent a meaningful regression. For documentation or other non-code artifacts, verify the content, references and intended use directly. Match verification effort to the actual change.

Review the final diff for unintended edits. Report the outcome and verification evidence, including checks that could not run. Record reusable findings in this role's `memory/MEMORY.md` only when they will help future work.
