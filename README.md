# .AGENTS

**English** | [简体中文](README.zh-CN.md)

**One project, multiple agents. Keep shared rules short and give role knowledge a clear home.**

`.AGENTS` is a directory convention and a set of Markdown templates for any Git project. Use `.AGENTS/<ROLE>/` to manage each role's **memory** and **skills**, so an agent taking over a task can find its responsibilities, known facts, and reusable methods.

It is not an agent runtime and does not start agents. Its contents are reviewable Markdown files that clients must explicitly read according to the entrypoint instructions.

## Why isn't AGENTS.md enough on its own?

The [official AGENTS.md guide](https://agents.md/) describes it as project instructions for coding agents, with support for instructions scoped to subdirectories. It works well for build commands, coding conventions, and shared rules. Collaboration between multiple agents introduces another dimension: **roles**.

| Situation | Limitation of AGENTS.md alone | What this project adds |
| --- | --- | --- |
| Architecture, implementation, and review touch the same code | File scope is not responsibility scope | A separate `AGENTS.md` for each role |
| Every session rediscovers the project | A Markdown entrypoint has no automatic memory writeback, expiry, or archiving | Memory with sources, dates, and status |
| Every lesson goes into the entrypoint | Irrelevant history consumes context and makes rules harder to maintain | Concise role memory and skills loaded on demand |
| Multiple agents work concurrently | Text conventions provide no scheduling, file locks, or transactions | Ownership and handoff conventions, used with Git/worktrees |
| Methods need to be reused | Project instructions alone do not provide a complete skill management workflow | Separate `skills/<name>/SKILL.md` files |
| Clients change | Discovery and instruction precedence depend on the client | Explicit role-file reading through the project entrypoint |

**Keep AGENTS.md as the entrypoint. Put role knowledge in .AGENTS/.** This is a project convention, not an official AGENTS.md extension. It does not change client permissions or instruction precedence. See [limitations and tradeoffs (Chinese)](docs/limitations.md).

## Layout

```text
your-project/
├── AGENTS.md                     # Shared rules, role selection, loading instructions
└── .AGENTS/
    ├── _shared/
    │   └── CONTEXT.md             # Confirmed facts shared across roles
    ├── developer/
    │   ├── AGENTS.md              # Responsibilities, boundaries, handoffs
    │   ├── memory/
    │   │   └── MEMORY.md          # Current facts, decisions, and lessons
    │   └── skills/
    │       └── decision-record/SKILL.md
    └── reviewer/                 # Same structure
```

`ROLE` describes a responsibility, not a model or vendor. One agent can switch roles, and multiple agent instances can share a role. `_shared` is reserved; role and skill names use lowercase letters, digits, and hyphens.

## Quick start

No tools or runtime to install. Apply the convention directly to your project:

1. Copy this repository's `.AGENTS/` directory into your project root.
2. Adapt `developer` and `reviewer` to your responsibilities, or create your own role directories.
3. Customize each role's `AGENTS.md`, `memory/MEMORY.md`, and skills, replacing this repository's example knowledge.
4. Merge the [entrypoint template (Chinese)](docs/entrypoint.md) into your root `AGENTS.md`, preserving existing project rules.
5. Ask your agent to read the selected role's files according to the entrypoint instructions.

For a new project, use this repository's layout as a starting point. Add `.AGENTS/*/local/` to your project's `.gitignore` for temporary material that should not be shared.

## Workflow

1. Choose a role for the task. Read the project entrypoint, shared facts, role responsibilities, and memory summary.
2. Read relevant skills as needed. Keep the selected role's memory concise and current.
3. Complete and verify the task. Write reusable findings and their evidence into the role's `memory/MEMORY.md`.
4. Reconcile concurrent memory edits through review. Move verified cross-role facts into shared context.
5. Hand off through Git commits and review. Mark replaced knowledge as `superseded` instead of continuing to treat it as current fact.

For example, ask your agent:

> Fix the current issue as the developer role. First read AGENTS.md, .AGENTS/_shared/CONTEXT.md, .AGENTS/developer/AGENTS.md, and that role's memory/MEMORY.md. Read the focused-change skill as needed. After completing the task, record reusable findings with evidence in the role's memory/MEMORY.md and report the verification results.

## Documentation and boundaries

The following supporting documents are in Chinese:

- [Directory protocol, memory lifecycle, and concurrent collaboration](docs/protocol.md)
- [AGENTS.md limitations and this approach's boundaries](docs/limitations.md)
- [Entrypoint template for existing projects](docs/entrypoint.md)
- [Contributing](CONTRIBUTING.md)

This is a file organization convention. It does not provide automatic loading, scheduling, memory extraction, permission isolation, vector retrieval, or automatic conflict resolution.
