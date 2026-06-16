# 项目流程说明：用于 PPT

## 1. 项目题目

房地产上市公司年报中的分红政策、经营现金流与流动性风险一致性分析。

核心问题：上市公司在进行现金分红时，是否同时存在经营现金流偏弱、利润承压或流动性风险披露较强的情况？

最终产出不是简单摘要，而是一个“值得关注的人工复核清单”，帮助分析哪些公司/年份需要进一步阅读年报原文。

## 2. 数据来源与样本范围

数据来源为巨潮资讯网公开披露的上市公司年度报告 PDF。

当前样本池：

| 指标 | 当前数量 |
|---|---:|
| PDF 总数 | 175 份 |
| 公司数量 | 37 家 |
| PDF 覆盖年份 | 2020-2024 |
| 当前已解析并评分样本 | 81 条 |
| 已形成同公司跨年匹配事件 | 54 条 |
| 下载失败记录 | 0 条 |

说明：175 份 PDF 已下载到 `data/pdf/`；当前 81 条已完成结构化抽取、校验、量化评分和清单生成。后续可继续对剩余 PDF 做 MinerU 解析并纳入同一流程。

## 3. 总体 Workflow

```mermaid
flowchart LR
    A["巨潮公告检索"] --> B["metadata.csv"]
    B --> C["PDF 下载"]
    C --> D["数据审计"]
    D --> E["MinerU 解析"]
    E --> F["Section Routing"]
    F --> G["字段抽取"]
    G --> H["Pydantic 校验"]
    H --> I["金额单位归一化"]
    I --> J["量化评分"]
    J --> K["关注清单"]
    J --> L["跨年匹配事件"]
    K --> M["最终报告与展示"]
    L --> M
```

## 4. Step 1：巨潮公告检索与样本扩展

输入：目标行业公司名单、年度范围、公告类型“年度报告”。

方法：

- 使用巨潮公开公告接口检索公司年报。
- 去除修订版、英文版等非目标公告。
- 记录公告 ID、公司名称、股票代码、报告年份、公告日期、巨潮 URL、PDF URL。

输出：

- `data/metadata/metadata.csv`
- `metadata_2020_2024_pool150.csv`
- `outputs/reports/dataset_expansion_to150.md`

PPT 重点：样本从原来的约 80 份扩展到 175 份 PDF，满足 1.1 档“样本量更大、可跨年比较”的方向。

## 5. Step 2：PDF 下载与数据审计

输入：`metadata.csv` 中的 PDF URL。

方法：

- 将 PDF 下载到 `data/pdf/`。
- 检查本地文件是否存在、是否重复、是否能与 metadata 对应。
- 下载失败写入日志，不静默忽略。

输出：

- `data/pdf/*.pdf`
- `failed_downloads_to150.csv`
- `outputs/reports/dataset_expansion_to150.md`

当前结果：175 份 PDF 全部下载成功，失败记录为空。

## 6. Step 3：MinerU 解析 PDF

输入：年报 PDF。

方法：

- 使用 MinerU 将 PDF 转换为可检索文本/Markdown。
- 保留文档 ID、页码、标题、正文等信息。
- 将解析后的文本统一整理为 JSONL。

输出：

- `parsed_docs.jsonl`
- `data/parsed/parsed_docs_sample.jsonl`

当前状态：81 条已解析样本进入后续结构化流程；其余 PDF 可以按同样方式继续解析扩展。

## 7. Step 4：Section Routing

目的：不直接在整份年报中抽字段，而是先定位与任务相关的章节，降低噪声。

目标章节：

- 分红政策、利润分配方案、现金分红。
- 财务指标、归母净利润、经营活动现金流量净额。
- 风险提示、流动性风险、融资风险、债务压力。

输出：

- `sections.jsonl`
- `data/parsed/sections_sample.jsonl`
- `section_check_report.md`

PPT 重点：Section routing 让抽取有证据来源，也便于人工复核。

## 8. Step 5：核心字段抽取

主要字段：

| 字段 | 含义 |
|---|---|
| `has_cash_dividend` | 是否存在现金分红 |
| `cash_dividend_per_10_shares` | 每 10 股现金分红金额 |
| `parent_net_profit` / `parent_net_profit_cny` | 归母净利润 |
| `operating_cash_flow` / `operating_cash_flow_cny` | 经营活动现金流量净额 |
| `risk_keywords` | 风险披露关键词 |
| `liquidity_risk_score` | 流动性风险量化分数 |
| `attention_score` | 综合关注分数 |
| `attention_level` | 关注等级 |

输出：

- `extract_results.jsonl`
- `outputs/results/records_validated.csv`

## 9. Step 6：Pydantic Schema 校验

目的：保证抽取结果不是随意文本，而是结构化、类型可控的数据。

校验内容：

- 布尔值、数值、字符串字段类型是否正确。
- 缺失值是否符合 null rule。
- 每条记录是否包含文档 ID、公司、年份等追溯信息。

输出：

- `outputs/results/records_validated.csv`
- `outputs/logs/validation_errors.jsonl`

当前结果：81 条当前结构化记录通过校验，校验错误日志为空。

## 10. Step 7：金额单位归一化

问题：年报中的金额可能使用“元、万元、亿元”等不同单位，直接比较会导致量纲不一致。

处理方式：

- 将归母净利润、经营活动现金流量净额统一到人民币元。
- 生成 `parent_net_profit_cny`、`operating_cash_flow_cny`。
- 计算经营现金流对利润覆盖比：`ocf_to_profit_ratio`。

输出：

- `records_validated_unit_normalized.csv`

PPT 重点：量化评分必须建立在统一量纲上。

## 11. Step 8：流动性风险量化评分

原问题：旧字段 `liquidity_risk_label` 是 high/medium/low 文本标签，每次单独判断可能缺乏可比性。

改进方式：

- 保留旧标签作为兼容字段。
- 新增基于词频和权重的 `liquidity_risk_score`。
- 对融资、债务、现金流、偿债、销售回款、市场下行等关键词分组计数。
- 以全样本分布生成 `liquidity_risk_quantile`，让不同年份、不同公司之间更可比较。

输出：

- `outputs/results/quantitative_scored_records.csv`
- `outputs/results/quantitative_scored_records.jsonl`

## 12. Step 9：综合关注分数

原问题：旧字段 `consistency_score` 只有简单分数，解释性和可比性不足。

改进方式：改为多指标加权评分。

| 指标 | 权重 | 含义 |
|---|---:|---|
| 分红压力 | 30% | 分红金额越高，关注度越高 |
| 经营现金流压力 | 25% | 经营现金流为负或覆盖利润偏弱时提高关注 |
| 利润压力 | 20% | 利润为负或偏低时提高关注 |
| 流动性风险披露 | 25% | 风险词频与权重越高，关注度越高 |

输出字段：

- `dividend_pressure_score`
- `cashflow_pressure_score`
- `profit_pressure_score`
- `liquidity_risk_score`
- `attention_score`
- `attention_level`

PPT 重点：从主观标签升级为可解释、可比较、可排序的量化分数。

## 13. Step 10：生成值得关注的清单

规则：将高综合关注分、现金分红但现金流弱、流动性风险披露强、利润承压等情况列入人工复核队列。

输出：

- `outputs/analysis/attention_review_list.csv`

当前结果：生成 4 条优先关注记录，供人工阅读年报原文进一步判断。

## 14. Step 11：跨年匹配事件

目的：1.1 档要求强调更复杂的结构和比较。本项目将同一公司不同年份记录连接起来，观察风险变化。

事件类型示例：

- 流动性风险评分上升。
- 经营现金流覆盖变弱。
- 分红行为与风险披露同时存在。
- 同公司连续多年触发关注条件。

输出：

- `outputs/analysis/cross_year_matching_events.csv`

当前结果：已形成 54 条同公司跨年匹配事件。

## 15. Step 12：评估与人工复核

评估材料：

- `eval_report_final.md`
- `human_eval_template_81.csv`
- `human_eval_audit_report.csv`
- `outputs/reports/eval_report_final.md`

评估重点：

- 字段抽取是否正确。
- Section routing 是否命中相关章节。
- 金额单位是否归一化正确。
- 关注清单是否具有金融解释意义。

## 16. 当前可复现命令

当前 81 条已解析样本的可复现命令：

```bash
python pipeline_run.py --config configs/workflow_parsed81.yaml --step all
```

预期输出：

```text
[validate] valid=81, errors=0
[report] summary report=outputs/reports/summary_report.md
[analysis] scored_records=81
[analysis] flagged_records=4
[analysis] cross_year_events=54
```

## 17. 最终展示建议页序

1. 研究问题：分红、现金流、流动性风险是否一致。
2. 数据来源：巨潮年报，175 份 PDF，37 家公司，2020-2024。
3. Workflow：metadata -> PDF -> MinerU -> routing -> extraction -> validation -> scoring。
4. Schema：核心字段与证据追溯。
5. 1.1 档升级点：样本扩展、跨年匹配、量化评分、关注清单。
6. 旧字段问题与改进：从 `liquidity_risk_label` / `consistency_score` 到量化分数。
7. 结果展示：最终结果表、关注清单、跨年事件。
8. Demo：选一份年报展示从 metadata 到 final result。
9. 局限与下一步：继续解析剩余 PDF、扩大人工评估、优化章节命中。

## 18. 一句话总结

本项目把房地产上市公司年报从 PDF 文本转化为可追溯、可校验、可比较的结构化指标，并用量化评分生成需要人工重点复核的公司年度清单。
