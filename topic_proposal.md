# Topic Proposal 中文版

## 项目题目

房地产上市公司年报中的分红政策、经营现金流与流动性风险一致性分析。

## 金融问题

本项目研究 A 股房地产上市公司的现金分红决策，是否与其经营现金流表现、归母净利润水平和流动性风险披露相一致。

项目不直接给出投资建议，而是生成一个“值得关注的人工复核清单”：当公司存在现金分红，同时经营现金流偏弱、利润承压或流动性风险披露较强时，将其列入后续人工阅读年报原文的重点对象。

## 数据来源

数据来源为巨潮资讯网公开披露的年度报告 PDF。

## 公告类型

年度报告。

## 样本范围

| 指标 | 当前数量 |
|---|---:|
| 已下载 PDF | 175 份 |
| 公司数量 | 37 家 |
| PDF 覆盖年份 | 2020-2024 |
| 已解析并评分记录 | 81 条 |
| 同公司跨年匹配事件 | 54 条 |

说明：175 份 PDF 已作为样本池下载完成；当前结构化流程已对 81 条记录完成解析、抽取、校验和量化评分。后续可继续对剩余 PDF 执行 MinerU 解析并并入同一 workflow。

## 目标字段

| 字段 | 类型 | 含义 |
|---|---|---|
| `has_cash_dividend` | bool/null | 是否存在现金分红 |
| `cash_dividend_per_10_shares` | float/null | 每 10 股现金分红金额 |
| `parent_net_profit_cny` | float/null | 归母净利润，统一为人民币元 |
| `operating_cash_flow_cny` | float/null | 经营活动现金流量净额，统一为人民币元 |
| `ocf_to_profit_ratio` | float/null | 经营现金流对利润覆盖比 |
| `liquidity_risk_score` | float | 基于风险词频和权重的 0-100 评分 |
| `liquidity_risk_quantile` | enum | 基于样本分布的 none/low/medium/high 标签 |
| `attention_score` | float | 综合关注分数 |
| `attention_level` | enum | routine/monitor/watch/priority |
| `review_reason` | string | 进入关注清单的原因 |

## 方法路线

```text
metadata -> PDF 下载 -> 数据审计 -> MinerU 解析 -> Section Routing
-> 字段抽取 -> Pydantic 校验 -> 金额单位归一化
-> 流动性风险量化 -> 综合关注评分 -> 关注清单 / 跨年事件
```

核心方法包括：

- 使用标准 `metadata.csv` 保证 PDF 与公告来源可追溯。
- 使用 MinerU 解析 PDF 年报文本。
- 使用 section routing 先定位分红、财务指标和风险披露章节。
- 使用 Pydantic Schema 约束字段类型和缺失值规则。
- 将金额统一归一化为人民币元。
- 用风险词频、权重和样本分位数替代单次 high/medium/low 主观标签。
- 用分红压力、现金流压力、利润压力和流动性风险披露构建综合关注分数。

## 最终输出

- `outputs/results/final_results.csv`
- `outputs/results/quantitative_scored_records.csv`
- `outputs/analysis/attention_review_list.csv`
- `outputs/analysis/cross_year_matching_events.csv`
- `outputs/reports/quantitative_attention_report.md`
- `outputs/reports/challenge_1_1_upgrade_report.md`

## 难度档位

目标档位：1.1。

理由：

- 样本池扩展到 175 份 PDF。
- 当前结构化样本包含 81 条已解析记录。
- 形成 54 条同公司跨年匹配事件。
- 不只做摘要，而是完成抽取、校验、单位归一化、量化评分和清单生成。
- 将 `liquidity_risk_label` 和 `consistency_score` 的主观性问题改造为可比较的量化指标。

## 风险与应对

| 风险 | 应对 |
|---|---|
| PDF 文件较大，仓库体积可能过大 | 保留样本 PDF、完整 metadata 和下载脚本 |
| 解析文本可能漏掉表格细节 | 保留 evidence、解析样本和人工评估材料 |
| 金额单位不统一 | 使用 CNY 归一化字段 |
| 自动评分可能误判 | 将结果定义为人工复核清单，而不是最终投资判断 |
