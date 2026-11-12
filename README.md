# Codex × DeepSeek Harness 协作

本项目让 Codex 主导开发任务，按任务影响选择模型和验证深度；DeepSeek Harness（DSH）在适合委派时直接修改项目工作区。

## 当前分工

| 角色 | 模型或工具 | 适用场景 |
| --- | --- | --- |
| 主协调 | GPT-6.1 Terra | 理解目标、安排执行、判断影响、汇报结果 |
| 执行 | DeepSeek Harness | 范围明确的实现和自检，通过 `dsh-baton` 接收 Codex 任务 |
| 深入分析与审查 | GPT-6.1 Sol | 复杂代码、跨模块问题、关键计算或数据处理变更 |
| 重大决策 | GPT-6 Astra | 架构取舍、研究可信度、持续无法解释的失败 |
| 资料整理 | GPT-6 Luna | 值得单独委派的长日志或资料提取 |

角色按需调用，没有固定的多模型流水线。实现前的重大未决选择交 Astra；范围明确的实现优先交 DeepSeek，并合并相关工作；关键结果需要独立核验、检查失败或证据冲突时，交 Sol 针对性分析；长材料确需单独整理时才交 Luna。简单任务可由 Terra 直接完成；同一阶段合并必要审查，跟踪其他任务时以完成、需关注和阶段关口为节点。

## 本机部署状态

2026-11-10 已在当前 Windows 用户的 Codex 配置中部署 Terra 默认模型和三个自定义代理，并追加全局路由规则。新 Codex CLI 会话能识别三个代理及对应模型。`dsh-baton` 的任务发送、结果返回和 DSH 工作区写入已做过范围受控的端到端验证。测试项目中已分别实际调用 Astra、Luna、Sol，并验证 Terra 在未指定角色时自行委派 DeepSeek。

仓库中的 [`deployment/agents`](deployment/agents) 和 [`deployment/AGENTS.append.md`](deployment/AGENTS.append.md) 是个人配置的可复用副本。克隆仓库本身不会自动安装这些个人配置或 DSH 插件。互联与 Windows 工作区权限的验证记录见 [`docs/协作流程设计草案.md`](docs/协作流程设计草案.md)。

可重复的完整流程测试项目位于 [`test_project/participant_split`](test_project/participant_split)，包含原始错误版本、验收测试、DeepSeek 修复后的实现和首次运行记录。
