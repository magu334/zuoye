# Output Sample

## 目标输出说明
- 输出形式：CSV + JSONL + 分析报告 + 重点复核清单。
- 每条记录对应一份 CNINFO 年报。
- 每条记录需要保留 `doc_id`，并能追溯到 metadata、PDF、MinerU markdown、section 和 evidence。

## 示例表格
| doc_id | stock_code | stock_name | report_year | has_cash_dividend | operating_cash_flow | liquidity_risk_label | consistency_score |
|---|---|---|---:|---|---:|---|---:|
| 1219487237 | 000002 | 万科A | 2023 | false | 3912323920 | medium | 3 |

## 字段解释
| 字段 | 类型 | 是否必填 | 金融含义 | 如何判断对错 |
|---|---|---|---|---|
| `has_cash_dividend` | bool/null | 是 | 公司是否进行现金分红 | 对照利润分配预案 |
| `cash_dividend_per_10_shares` | float/null | 否 | 每10股派现金额 | 对照分红方案原文 |
| `parent_net_profit` | number/null | 否 | 盈利能力 | 对照主要财务指标 |
| `operating_cash_flow` | number/null | 否 | 现金流压力 | 对照现金流量指标 |
| `liquidity_risk_label` | enum | 是 | 风险披露强度 | 对照风险章节 evidence |
| `consistency_score` | int/null | 是 | 一致性筛查 | 对照字段组合和评分规则 |
