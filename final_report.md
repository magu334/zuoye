# 最终报告

## 1. 项目题目

房地产上市公司年报中的分红政策、经营现金流与流动性风险一致性分析。

## 2. 研究问题

本项目研究 A 股房地产上市公司的现金分红决策，是否与其经营现金流表现、归母净利润水平和流动性风险披露相一致。

具体来说，如果公司在经营现金流偏弱、利润承压或流动性风险披露较强的情况下仍进行现金分红，该公司年度记录会被列入人工复核清单。项目输出不是投资建议，而是一个可追溯、可解释的分析辅助结果。

## 3. 数据来源与样本

数据来源为巨潮资讯网公开披露的上市公司年度报告 PDF。

| 指标 | 当前结果 |
|---|---:|
| PDF 样本池 | 175 份 |
| 公司数量 | 37 家 |
| PDF 年份范围 | 2020-2024 |
| 当前已解析并评分记录 | 81 条 |
| 同公司跨年匹配事件 | 54 条 |
| 下载失败记录 | 0 条 |

关键数据文件：

- `data/metadata/metadata.csv`
- `data/pdf/`
- `data/parsed/parsed_docs_sample.jsonl`
- `outputs/results/final_results.csv`

当前项目已经完成 175 份 PDF 的样本池扩展。由于剩余 PDF 仍需继续执行 MinerU 解析，最终结构化评分部分目前覆盖 81 条已解析记录。

## 4. Workflow

```text
metadata -> PDF 下载 -> 数据审计 -> MinerU 解析 -> Section Routing
-> 字段抽取 -> Pydantic 校验 -> 金额单位归一化
-> 流动性风险量化 -> 综合关注评分 -> 关注清单 / 跨年事件
```

当前可复现命令：

```bash
python pipeline_run.py --config configs/workflow_parsed81.yaml --step all
```

运行后会生成：

- `outputs/results/final_results.csv`
- `outputs/results/quantitative_scored_records.csv`
- `outputs/analysis/attention_review_list.csv`
- `outputs/analysis/cross_year_matching_events.csv`
- `outputs/reports/summary_report.md`
- `outputs/reports/quantitative_attention_report.md`

## 5. 核心字段

| 字段 | 含义 |
|---|---|
| `has_cash_dividend` | 是否存在现金分红 |
| `cash_dividend_per_10_shares` | 每 10 股现金分红金额 |
| `parent_net_profit_cny` | 归母净利润，统一为人民币元 |
| `operating_cash_flow_cny` | 经营活动现金流量净额，统一为人民币元 |
| `ocf_to_profit_ratio` | 经营现金流对利润覆盖比 |
| `liquidity_risk_score` | 基于风险词频和权重的流动性风险评分 |
| `liquidity_risk_quantile` | 基于样本分布的流动性风险分位标签 |
| `attention_score` | 综合关注分数 |
| `attention_level` | 关注等级 |
| `review_reason` | 进入关注清单的原因 |

## 6. 对旧版本问题的改进

### 6.1 流动性风险标签

旧版本使用 `liquidity_risk_label` 表示 high/medium/low，容易被质疑不同批次抽取结果不可比。

本版本保留旧字段作为兼容信息，同时新增：

- `liquidity_term_hits`
- `liquidity_weighted_hits`
- `liquidity_risk_score`
- `liquidity_risk_quantile`

新评分基于风险关键词命中频次和权重，并根据全样本分布生成分位标签，因此比单次文本判断更客观、更可比较。

### 6.2 一致性筛查分数

旧版本的 `consistency_score` 解释性较弱。

本版本新增 `attention_score`，由四个指标加权构成：

| 指标 | 权重 |
|---|---:|
| 分红压力 | 30% |
| 经营现金流压力 | 25% |
| 利润压力 | 20% |
| 流动性风险披露 | 25% |

综合评分生成 `attention_level` 和 `review_reason`，并输出人工复核清单。

## 7. 当前结果

当前工作流结果：

- 81 条记录完成结构化校验。
- `validation_errors.jsonl` 为空。
- 81 条记录完成量化评分。
- 4 条记录进入优先关注清单。
- 54 条同公司跨年匹配事件已生成。

关键输出：

- `outputs/results/final_results.csv`
- `outputs/analysis/attention_review_list.csv`
- `outputs/analysis/cross_year_matching_events.csv`
- `outputs/reports/quantitative_attention_report.md`
- `outputs/reports/challenge_1_1_upgrade_report.md`

## 8. 难度档位说明

本项目目标为 1.1 档。

主要依据：

1. 样本池从约 80 份 PDF 扩展到 175 份 PDF。
2. 当前 81 条结构化样本已完成抽取、校验和评分。
3. 项目不是单纯总结公告，而是完成字段抽取、单位归一化、量化评分和清单生成。
4. 形成 54 条同公司跨年匹配事件。
5. 对流动性风险和一致性筛查进行了量化改造，增强可比性。
6. 输出可以直接用于人工复核的关注清单。

## 9. 局限性

- 当前 175 份 PDF 中，仍有部分 PDF 需要继续执行 MinerU 解析后才能纳入结构化评分。
- Section routing 和字段抽取仍可能受到 PDF 表格格式、OCR 质量和年报写法差异影响。
- 量化评分用于筛查和排序，不应被视为最终风险结论。
- 人工评估样本还可以继续扩大，以进一步校准抽取准确率。

## 10. 后续改进

1. 对剩余 PDF 继续执行 MinerU 解析，扩大结构化评分样本。
2. 增加人工标注样本，评估字段抽取准确率和关注清单命中质量。
3. 继续优化风险关键词权重和行业词表。
4. 增加更多跨年事件类型，例如风险改善、分红持续性和现金流反转。
5. 在 PPT 展示中选取一家公司，完整展示从 PDF 到最终关注分数的链路。
