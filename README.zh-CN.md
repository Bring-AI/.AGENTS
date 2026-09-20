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
    │       └── decision-record/SKILL.md
    └── reviewer/                 # 相同结构
```

`ROLE` 表示职责，不绑定某个模型或厂商。同一个 agent 可以切换角色，同一个角色也可以由多个 agent 实例承担。`_shared` 是保留目录；角色和技能名称使用小写字母、数字与连字符。

## 快速开始

无需安装工具或运行环境，直接将目录约定应用到你的项目：

1. 将本仓库的 `.AGENTS/` 复制到项目根目录。
2. 根据实际职责调整 `developer`、`reviewer`，或创建自己的角色目录。
3. 修改各角色的 `AGENTS.md`、`memory/MEMORY.md` 和技能内容，替换本仓库的示例知识。
4. 将[入口模板](docs/entrypoint.md)合并到项目根目录的 `AGENTS.md`，保留项目原有规则。
5. 让 agent 按入口说明读取所选角色的文件。

新项目可使用本仓库的结构作为起点。将 `.AGENTS/*/local/` 加入项目的 `.gitignore`，用于不参与共享的临时资料。

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
