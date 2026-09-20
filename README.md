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
    ├── developer/
    │   ├── AGENTS.md              # Responsibilities, boundaries, handoffs
    │   ├── memory/
    │   │   └── MEMORY.md          # Current facts, decisions, and lessons
    │   └── skills/
    │       ├── focused-change/SKILL.md
    │       └── decision-record/SKILL.md
    └── reviewer/                 # Same structure
```

`ROLE` describes a responsibility, not a model or vendor. One agent can switch roles, and multiple agent instances can share a role. Role and skill names use lowercase letters, digits, and hyphens.

## Quick start

No installation or template-filling step is required. The root `AGENTS.md` and default roles are ready to use; project facts and memory are established through actual work.

### New project: clone and start

```sh
git clone https://github.com/Bring-AI/.AGENTS.git my-project
cd my-project
```

Open your agent in this directory and give it the project goal and first task. For example:

> Read AGENTS.md and work as developer to implement my requirements. Inspect the existing files first. Do not treat an undecided stack or constraint as fact. Save confirmed, reusable project knowledge in the appropriate memory file as the work progresses.

If your client does not automatically read `AGENTS.md`, explicitly ask it to do so. Choosing a role does not require multiple agents; one agent can develop and review sequentially.

### Existing project: merge the entrypoint and copy role files

1. Clone this repository outside the existing project.
2. Copy `.AGENTS/` into the project root. Merge any existing files individually, preserving their contents.
3. If the project has no `AGENTS.md`, copy this repository's root entrypoint. Otherwise, merge the [role-reading instructions (Chinese)](docs/entrypoint.md) while keeping existing rules.
4. Add `.AGENTS/*/local/` to the project's `.gitignore`, then give your agent a real task.

The root entrypoint and `.AGENTS/` work independently of this repository's READMEs, contribution guide and `docs/`. Those files explain the convention and can be kept or replaced to suit your project. The default roles and skills assume no language, framework or build commands; adapt them as needed.

## Workflow

1. Choose a role for the task. Read the root `AGENTS.md` for project context and shared rules, then the role instructions and memory.
2. Read relevant skills as needed. Keep the selected role's memory concise and current.
3. Complete and verify the task. Write reusable findings and their evidence into the role's `memory/MEMORY.md`.
4. Reconcile concurrent memory edits through review. Keep verified project context useful to all roles in the root `AGENTS.md`.
5. Hand off through Git commits and review. Mark replaced knowledge as `superseded` instead of continuing to treat it as current fact.

For example, ask your agent:

> Fix the current issue as the developer role. First read AGENTS.md, .AGENTS/developer/AGENTS.md, and that role's memory/MEMORY.md. Read the focused-change skill as needed. After completing the task, record reusable findings with evidence in the role's memory/MEMORY.md and report the verification results.

## Documentation and boundaries

The following supporting documents are in Chinese:

- [Directory protocol, memory lifecycle, and concurrent collaboration](docs/protocol.md)
- [AGENTS.md limitations and this approach's boundaries](docs/limitations.md)
- [Entrypoint template for existing projects](docs/entrypoint.md)
- [Contributing](CONTRIBUTING.md)

This is a file organization convention. It does not provide automatic loading, scheduling, memory extraction, permission isolation, vector retrieval, or automatic conflict resolution.
