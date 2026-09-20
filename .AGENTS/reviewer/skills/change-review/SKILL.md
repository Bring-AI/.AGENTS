---
name: change-review
description: Review code, configuration, documentation or other project changes for concrete defects, regressions and gaps in verification.
---

# Change review

Establish the intended outcome and review scope. Read the change together with the surrounding behavior, relevant requirements and affected consumers. Use project instructions and existing invariants to judge correctness.

Trace plausible failures: incorrect results, broken compatibility, unsafe data handling, missing edge cases or misleading documentation. Verify suspicions with project evidence or a focused check where practical; do not present speculation as a confirmed defect.

For each actionable finding, give a precise location, the condition that triggers it, its impact and the reasoning or reproduction that supports it. Prioritize by actual consequence. Separate optional improvements from defects and avoid repeating findings with the same cause.

If no actionable findings remain, say so and note material verification gaps. Do not imply that review proves the absence of defects. Store confirmed lessons in this role's `memory/MEMORY.md` only when they are reusable across future tasks.
