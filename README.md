# .AGENTS

**一个项目，多个 agent；公共规则保持简短，角色知识各有归属。**

`.AGENTS` 是一套可放进任意 Git 项目的目录约定，以及一个零第三方依赖的 Python 工具。使用 `.AGENTS/<ROLE>/` 管理不同角色的 **memory** 和 **skill**，让接手任务的 agent 可以找到职责、已知事实和可复用工作方法。

它不是 agent 运行时，也不会自动启动多个 agent。目录内容是可审查的 Markdown，客户端需要按入口说明显式读取。

## 为什么只有 AGENTS.md 还不够？

[`AGENTS.md` 官方说明](https://agents.md/)将它定位为面向编码 agent 的项目说明，并支持按子目录划分指令。它很适合保存构建命令、代码约定和公共规则。但多 agent 协作还有另一条维度：**角色**。

| 场景 | 单靠 AGENTS.md 的局限 | 本项目的补充 |
| --- | --- | --- |
| 架构、开发和评审操作同一份代码 | 文件路径范围不等于职责范围 | 每个角色独立的 `ROLE.md` |
| 每次会话都重新探索项目 | Markdown 入口没有自动记忆写回、过期和归档机制 | 有来源、日期和状态的 memory |
| 所有经验都堆进入口文件 | 无关历史增加上下文开销，规则更难维护 | 摘要入口与按需加载的记录、技能 |
| 多个 agent 同时工作 | 文本约定不提供调度、文件锁或事务 | 明确所有权与交接约定，配合 Git/worktree |
| 方法需要反复复用 | 项目指令本身不提供完整的技能管理工作流 | 独立 `skills/<name>/SKILL.md` |
| 切换客户端 | 自动发现和指令优先级由客户端实现决定 | 显式读取或 CLI 组装上下文 |

**保留 AGENTS.md，作为入口；把角色知识放到 .AGENTS/。** 这是一项项目级扩展约定，不是 AGENTS.md 的官方扩展，也不改变任何客户端的权限或指令优先级。详见[局限与设计取舍](docs/limitations.md)。

## 目录

```text
your-project/
├── AGENTS.md                     # 公共约定、角色选择与加载说明
├── .AGENTS/
│   ├── _shared/
│   │   └── CONTEXT.md             # 跨角色的已确认事实
│   ├── architect/
│   │   ├── ROLE.md                # 职责、边界与交接
│   │   ├── memory/
│   │   │   ├── MEMORY.md          # 当前摘要与记录索引
│   │   │   └── records/*.md       # 决策与经验，按需读取
│   │   └── skills/
│   │       └── decision-record/SKILL.md
│   ├── developer/                # 相同结构
│   └── reviewer/                 # 相同结构
└── tools/agents.py                # 可选，单文件工具
```

`ROLE` 表示职责，不绑定某个模型或厂商。同一个 agent 可以切换角色，同一个角色也可以由多个 agent 实例承担。`_shared` 是保留目录；角色和技能名称使用小写字母、数字与连字符。

## 快速开始

需要 Python 3.10+，无需安装依赖。以下命令在本仓库根目录运行，Windows 可按安装方式将 `python` 替换为 `py`。

```sh
git clone https://github.com/Bring-AI/.AGENTS.git
cd .AGENTS
python tools/agents.py check
python tools/agents.py context developer
python tools/agents.py context developer --skill focused-change
python -m unittest discover -s tests -v
```

接入已有项目：

```sh
# 将本仓库中的工具用于另一个项目（也可以直接复制该单文件）
python tools/agents.py --root ../your-project init
python tools/agents.py --root ../your-project add-role researcher
python tools/agents.py --root ../your-project context researcher
python tools/agents.py --root ../your-project check
```

`init` 默认建立 `architect`、`developer`、`reviewer` 的通用骨架，可以用 `init --roles frontend backend qa` 自定义。它保留所有已有文件，不会覆盖已有 `AGENTS.md`；如果入口已存在，请手动合并[入口模板](docs/entrypoint.md)。示例角色的专业说明与技能位于本仓库 `.AGENTS/` 中，初始化骨架不自动复制这些项目特定内容。

新项目还应将 `.AGENTS/*/local/` 加入自己的 `.gitignore`，用来保存不参与共享的临时上下文。忽略规则不是秘密管理机制。

## 工作流程

1. 根据任务选择角色，读取公共入口、共享事实和该角色的职责及记忆摘要。
2. 根据任务读取相关 skill 和历史记录；不要默认加载所有角色全部历史。
3. 完成任务并验证，将值得复用的事实与证据写入独立记录。
4. 更新该角色摘要中的索引；跨角色事实经核对后放入共享上下文。
5. 通过 Git 提交和评审交接。过期知识标记为 `superseded`，不要继续作为当前事实使用。

例如让你的 agent 执行：

> 以 developer 角色修复当前问题。先读 AGENTS.md、.AGENTS/_shared/CONTEXT.md、.AGENTS/developer/ROLE.md 和 memory/MEMORY.md。按需读取 focused-change 技能。完成后将有证据的复用经验记录到该角色 memory/records/，并说明验证结果。

也可以将 `context` 的标准输出传给客户端。该输出只是供读取的文本，不会自动注入模型、安装技能或执行其中的命令。默认只输出入口与摘要，附技能/记录清单；使用 `--skill NAME`、`--record FILE.md`（可重复）才加入选中的正文。

## 文档与边界

- [目录协议、记忆生命周期与并发协作](docs/protocol.md)
- [AGENTS.md 的局限与本方案的边界](docs/limitations.md)
- [已有项目的入口模板](docs/entrypoint.md)
- [贡献指南](CONTRIBUTING.md)

`check` 检查必要文件、命名、非空内容和技能前置元数据的基本形状；它不是完整 YAML 校验器，也不验证事实真伪、链接有效性或客户端兼容性。本项目不实现调度、自动记忆提取、权限隔离、向量检索或冲突自动合并。
