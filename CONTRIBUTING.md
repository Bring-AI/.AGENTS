# 贡献指南

保持项目轻量：目录协议优先，CLI 仅承担可确定的文件操作。新功能应说明解决了哪个实际的多角色协作问题。

本地验证（Python 3.10+）：

```sh
python -m unittest discover -s tests -v
python tools/agents.py check
python tools/agents.py context developer --skill focused-change
```

协议、CLI 或样例行为变化时更新对应文档。测试关注已有文件保留、角色隔离、路径边界、错误报告和真实初始化流程。无需为了增加测试数量去匹配说明文字。

提交 memory 时只保留可复用知识及可核查来源。不要提交凭据、私人数据或完整会话记录。新增角色前先判断是否可由现有角色承担。
