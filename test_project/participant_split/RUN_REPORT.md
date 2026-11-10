# 首次完整流程测试记录

日期：2026-11-10。工作区：`F:\project\codex-dsh-collaboration`。任务范围：只允许 DeepSeek 修改 `test_project/participant_split/split.py`。

## 原始执行记录

1. Terra 选定受试者分组任务，并写下目标和三个自动检查。
2. 第一次 Astra 调用使用 Codex CLI `--ephemeral`，子代理启动报 `no rollout found for thread id`；本次不计为有效委派。去掉该参数后，`astra_adviser` 成功返回：拒绝缺失或空白身份；受试者隔离优先于精确记录数。
3. 原始按记录划分的版本运行三个 `unittest` 用例，三项均失败：受试者交叉、空白 ID 未报错、输入顺序改变分配。
4. Codex CLI 以 Terra 启动，通过 `dsh-baton` 的 `dsh_send` 和 `dsh_wait` 把实现交给 DeepSeek Harness，保持 `workspace-write`。桥接成功返回；DeepSeek 报告仅修改 `split.py`，三个测试均通过，固定样例的训练集 6 行、测试集 2 行。
5. 主协调者独立运行同一测试命令，三项均通过；读取 `split.py` 确认了分组、身份验证和确定性分配逻辑。

## 审查与修复

- `luna_organizer` 成功读取本记录，提取了已验证步骤、`--ephemeral` 子代理失败及恢复方式，并将当时尚未完成的检查列为待办。Luna 没有把错误的首次委派计为成功。
- `sol_analyst` 审查任务说明、实现和测试，发现非字符串 ID 中 `1` 与 `True` 可能合并为同一 Python 字典键，造成顺序稳定性问题；还指出记录保留测试会漏掉重复记录，以及缺失 ID 和两名受试者的边界未覆盖。
- Terra 将 ID 明确限定为非空字符串，补充测试。新增测试先在数字和布尔 ID 上失败。第二次通过 `dsh-baton` 交给 DeepSeek 只改 `split.py`；桥接返回后，五项测试在执行端及独立复测中均通过。

## 默认路由试验

在被 `.gitignore` 排除的 `verification/auto_flow` 中复制原始错误版本和相同测试。原始副本的五个测试方法产生九处失败。给新 Terra 会话的任务只说明目标、范围和测试命令，没有指定任何模型角色。

Terra 自行选择通过 `dsh-baton` 委派 DeepSeek 实现，随后收到完成回执，独立读取代码并运行测试：五项通过。它另外检查了不均等组大小、输入逆序、空输入、单一受试者及接近 0 和 1 的划分比例。本轮没有调用额外的 Codex 审查代理，符合规则已明确时按需调用的设定。Harness 报告内部使用了只读验证子代理；这属于观察到的额外调用，尚未评估其成本。

## Terra 最终验收

主测试项目的最终独立检查：`python -m unittest discover -s test_project/participant_split -p test_split.py -v`，五项通过。固定八行样例中，训练集六行、测试集两行，受试者无交叉。`fixtures/leaky_split.py` 保留可复位的原始错误版本，正式实现位于 `split.py`。本测试证实了各角色的实际调用和默认委派路径；没有测试真实科研数据，也不以此证明任意未来项目都能自动通过相同流程。
