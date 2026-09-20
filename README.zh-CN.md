# .AGENTS

[English](README.md) | **简体中文**

**一个项目，多个 agent；公共规则保持简短，角色知识各有归属。**

`.AGENTS` 是一套可放进任意 Git 项目的目录约定和 Markdown 模板。使用 `.AGENTS/<ROLE>/` 管理不同角色的 **memory** 和 **skill**，让接手任务的 agent 可以找到职责、已知事实和可复用工作方法。

它不是 agent 运行时，也不会自动启动多个 agent。目录内容是可审查的 Markdown，客户端需要按入口说明显式读取。

## 为什么只有 AGENTS.md 还不够？

[`AGENTS.md` 官方说明](https://agents.md/)将它定位为面向编码 agent 的项目说明，并支持按子目录划分指令。它很适合保存构建命令、代码约定和公共规则。但多 agent 协作还有另一条维度：**角色**。

| 场景 | 单靠 AGENTS.md 的局限 | 本项目的补充 |
| --- | --- | --- |
| 架构、开发和评审操作同一份代码 | 文件路径范围不等于职责范围 | 每个角色独立的 `AGENTS.md` |
| 每次会话都重新探索项目 | Markdown 入口没有自动记忆写回、过期和归档机制 | 有来源、日期和状态的 memory |
| 所有经验都堆进入口文件 | 无关历史增加上下文开销，规则更难维护 | 简短的角色记忆与按需加载的技能 |
| 多个 agent 同时工作 | 文本约定不提供调度、文件锁或事务 | 明确所有权与交接约定，配合 Git/worktree |
| 方法需要反复复用 | 项目指令本身不提供完整的技能管理工作流 | 独立 `skills/<name>/SKILL.md` |
| 切换客户端 | 自动发现和指令优先级由客户端实现决定 | 通过项目入口显式读取角色文件 |

**保留 AGENTS.md，作为入口；把角色知识放到 .AGENTS/。** 这是一项项目级扩展约定，不是 AGENTS.md 的官方扩展，也不改变任何客户端的权限或指令优先级。详见[局限与设计取舍](docs/limitations.md)。

## 目录

```text
your-project/
├── AGENTS.md                     # 公共约定、角色选择与加载说明
└── .AGENTS/
    ├── _shared/
    │   └── CONTEXT.md             # 跨角色的已确认事实
    ├── developer/
    │   ├── AGENTS.md              # 职责、边界与交接
    │   ├── memory/
    │   │   └── MEMORY.md          # 当前事实、决策与经验
    │   └── skills/
    │       ├── focused-change/SKILL.md
    │       └── decision-record/SKILL.md
    └── reviewer/                 # 相同结构
```

`ROLE` 表示职责，不绑定某个模型或厂商。同一个 agent 可以切换角色，同一个角色也可以由多个 agent 实例承担。`_shared` 是保留目录；角色和技能名称使用小写字母、数字与连字符。

## 快速开始

无需安装工具，也不必先填完模板。根目录的 `AGENTS.md` 和默认角色可直接使用；项目事实和记忆在实际任务中逐步建立。

### 新项目：clone 后直接开始

```sh
git clone https://github.com/Bring-AI/.AGENTS.git my-project
cd my-project
```

在这个目录中打开你的 agent，给出项目目标和第一个任务。例如：

> 阅读 AGENTS.md，使用 developer 角色，根据我的需求开始开发。先了解已有文件；项目尚未确定的技术栈和约束不要当作事实。将工作中确认、值得复用的项目知识写入对应 memory。

如果客户端不会自动读取 `AGENTS.md`，在任务提示中明确要求它读取。选择角色不要求启动多个 agent，同一个 agent 可以依次开发和评审。

### 已有项目：合并入口，复制角色目录

1. 将本仓库 clone 到现有项目之外。
2. 将 `.AGENTS/` 复制到项目根目录；已有同名文件时逐项合并，保留原有内容。
3. 如果项目还没有 `AGENTS.md`，复制本仓库的根入口；已有入口则合并[角色读取说明](docs/entrypoint.md)，保留原有规则。
4. 将 `.AGENTS/*/local/` 加入项目的 `.gitignore`，然后给 agent 一个实际任务。

根入口和 `.AGENTS/` 可以独立使用，不依赖本仓库的 README、贡献指南或 `docs/`。这些文件用于解释约定，可按项目需要保留或替换。默认角色和技能不预设语言、框架或构建命令；按需求调整即可。

## 工作流程

1. 根据任务选择角色，读取公共入口、共享事实和该角色的职责及记忆摘要。
2. 根据任务读取相关 skill，保持当前角色的记忆简短、有效。
3. 完成任务并验证，将值得复用的事实与证据写入该角色的 `memory/MEMORY.md`。
4. 通过评审协调并发的记忆修改；跨角色事实经核对后放入共享上下文。
5. 通过 Git 提交和评审交接。过期知识标记为 `superseded`，不要继续作为当前事实使用。

例如让你的 agent 执行：

> 以 developer 角色修复当前问题。先读 AGENTS.md、.AGENTS/_shared/CONTEXT.md、.AGENTS/developer/AGENTS.md 和 memory/MEMORY.md。按需读取 focused-change 技能。完成后将有证据的复用经验记录到该角色 memory/MEMORY.md，并说明验证结果。

## 文档与边界

- [目录协议、记忆生命周期与并发协作](docs/protocol.md)
- [AGENTS.md 的局限与本方案的边界](docs/limitations.md)
- [已有项目的入口模板](docs/entrypoint.md)
- [贡献指南](CONTRIBUTING.md)

这是一套文件组织约定，不提供自动加载、调度、自动记忆提取、权限隔离、向量检索或冲突自动合并。
