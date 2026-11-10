# 受试者分组测试项目

这是 Codex 与 DeepSeek Harness 协作流程的可重复测试任务。代码仅使用 Python 标准库，不使用真实研究数据。

## 任务

原始版本按记录随机划分训练集和测试集，同一受试者的记录可能出现在两边。复跑时将 `fixtures/leaky_split.py` 复制到 `split.py`，然后要求执行器修复 `split_rows(rows, test_fraction=0.25, seed=0)`：

- 同一 `participant_id` 的所有记录必须处于同一集合。
- `participant_id` 必须是非空字符串；缺失、非字符串或仅含空白时必须报 `ValueError`，并以从 1 开始的行号指出有问题的记录位置。
- 固定种子和相同记录集合应得到相同的受试者分配，不受输入行顺序影响。
- 保留所有输入记录，函数返回 `{"train": [...], "test": [...]}`。受试者隔离优先于精确行数比例；报告实际两边的记录数。
- 当至少有两个受试者且 `0 < test_fraction < 1` 时，两边都应有记录。

这个边界由 Astra 在首次完整流程测试中决定。测试项目不要求标签分层、精确行数优化或研究结论。

## 流程检查点

1. Terra 理解任务、指定工作区和改动范围。
2. Astra 决定缺失身份与比例冲突时的规则。
3. 运行测试，确认原始错误版本失败。
4. Codex 经 `dsh-baton` 委派 DeepSeek 修改 `split.py` 并自检。
5. 本地自动测试检查隔离、输入验证、确定性和记录保留。
6. Luna 整理执行记录；Sol 对有研究含义的划分逻辑做针对性审查。
7. Terra 核对最终差异、测试结果和未解决问题。

三个 Codex 子代理在这里都运行，是为了验证部署链路；日常任务仍按需调用。

## 运行与复位

在仓库根目录执行：

```powershell
python -m unittest discover -s test_project/participant_split -p test_split.py -v
```

`fixtures/leaky_split.py` 保留原始错误版本。复跑流程时，先把它复制到 `split.py`，确认测试失败，再委派执行器修复。复制会覆盖当前解法，建议在独立工作区中复跑。
