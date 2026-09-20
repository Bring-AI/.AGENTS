# .AGENTS

**English** | [简体中文](README.zh-CN.md)

**One project, multiple agents. Keep shared rules short and give role knowledge a clear home.**

`.AGENTS` is a directory convention for any Git project, with a Python tool that has no third-party dependencies. Use `.AGENTS/<ROLE>/` to manage each role's **memory** and **skills**, so an agent taking over a task can find its responsibilities, known facts, and reusable methods.

It is not an agent runtime and does not start agents. Its contents are reviewable Markdown files that clients must explicitly read according to the entrypoint instructions.

## Why isn't AGENTS.md enough on its own?

The [official AGENTS.md guide](https://agents.md/) describes it as project instructions for coding agents, with support for instructions scoped to subdirectories. It works well for build commands, coding conventions, and shared rules. Collaboration between multiple agents introduces another dimension: **roles**.

| Situation | Limitation of AGENTS.md alone | What this project adds |
| --- | --- | --- |
| Architecture, implementation, and review touch the same code | File scope is not responsibility scope | A separate `AGENTS.md` for each role |
| Every session rediscovers the project | A Markdown entrypoint has no automatic memory writeback, expiry, or archiving | Memory with sources, dates, and status |
| Every lesson goes into the entrypoint | Irrelevant history consumes context and makes rules harder to maintain | Summaries with records and skills loaded on demand |
| Multiple agents work concurrently | Text conventions provide no scheduling, file locks, or transactions | Ownership and handoff conventions, used with Git/worktrees |
| Methods need to be reused | Project instructions alone do not provide a complete skill management workflow | Separate `skills/<name>/SKILL.md` files |
| Clients change | Discovery and instruction precedence depend on the client | Explicit reading or CLI context assembly |

**Keep AGENTS.md as the entrypoint. Put role knowledge in .AGENTS/.** This is a project convention, not an official AGENTS.md extension. It does not change client permissions or instruction precedence. See [limitations and tradeoffs (Chinese)](docs/limitations.md).

## Layout

```text
your-project/
├── AGENTS.md                     # Shared rules, role selection, loading instructions
├── .AGENTS/
│   ├── _shared/
│   │   └── CONTEXT.md             # Confirmed facts shared across roles
│   ├── architect/
│   │   ├── AGENTS.md                # Responsibilities, boundaries, handoffs
│   │   ├── memory/
│   │   │   ├── MEMORY.md          # Current summary and record index
│   │   │   └── records/*.md       # Decisions and lessons, read on demand
│   │   └── skills/
│   │       └── decision-record/SKILL.md
│   ├── developer/                # Same structure
│   └── reviewer/                 # Same structure
└── tools/agents.py                # Optional, single-file tool
```

`ROLE` describes a responsibility, not a model or vendor. One agent can switch roles, and multiple agent instances can share a role. `_shared` is reserved; role and skill names use lowercase letters, digits, and hyphens.

## Quick start

Requires Python 3.10+ with no dependencies to install. Run these commands from the repository root. On Windows, you may need to replace `python` with `py`, depending on your installation.

```sh
git clone https://github.com/Bring-AI/.AGENTS.git
cd .AGENTS
python tools/agents.py check
python tools/agents.py context developer
python tools/agents.py context developer --skill focused-change
python -m unittest discover -s tests -v
```

Use it with an existing project:

```sh
# Use this repository's tool for another project, or copy the single file there.
python tools/agents.py --root ../your-project init
python tools/agents.py --root ../your-project add-role researcher
python tools/agents.py --root ../your-project context researcher
python tools/agents.py --root ../your-project check
```

`init` creates generic skeletons for `architect`, `developer`, and `reviewer` by default. Customize them with `init --roles frontend backend qa`. It preserves all existing files, including `AGENTS.md`. If the entrypoint already exists, manually merge the [entrypoint template (Chinese)](docs/entrypoint.md). The specialized role instructions and skills in this repository's `.AGENTS/` are examples; initialization does not copy that project-specific content.

Add `.AGENTS/*/local/` to your project's `.gitignore` for temporary context that should not be shared. Ignore rules are not a secrets management mechanism.

## Workflow

1. Choose a role for the task. Read the project entrypoint, shared facts, role responsibilities, and memory summary.
2. Read relevant skills and historical records as needed. Do not load every role's entire history by default.
3. Complete and verify the task. Write reusable findings and their evidence into separate records.
4. Update the role's summary index. Move verified cross-role facts into shared context.
5. Hand off through Git commits and review. Mark replaced knowledge as `superseded` instead of continuing to treat it as current fact.

For example, ask your agent:

> Fix the current issue as the developer role. First read AGENTS.md, .AGENTS/_shared/CONTEXT.md, .AGENTS/developer/AGENTS.md, and that role's memory/MEMORY.md. Read the focused-change skill as needed. After completing the task, record reusable findings with evidence in the role's memory/records/ and report the verification results.

You can also pass the standard output of `context` to your client. It is text for the client to read; it does not automatically inject context into a model, install skills, or execute commands. By default it includes entry files and summaries, followed by skill and record inventories. Use `--skill NAME` and `--record FILE.md` (repeatable) to include selected bodies.

## Documentation and boundaries

The following supporting documents are in Chinese:

- [Directory protocol, memory lifecycle, and concurrent collaboration](docs/protocol.md)
- [AGENTS.md limitations and this approach's boundaries](docs/limitations.md)
- [Entrypoint template for existing projects](docs/entrypoint.md)
- [Contributing](CONTRIBUTING.md)

`check` validates required files, names, nonempty contents, and the basic shape of skill frontmatter. It is not a full YAML validator and does not verify factual accuracy, links, or client compatibility. This project does not implement scheduling, automatic memory extraction, permission isolation, vector retrieval, or automatic conflict resolution.
