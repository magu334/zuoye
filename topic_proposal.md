# Topic Proposal

## 项目题目
房地产上市公司年报分红政策、经营现金流与流动性风险一致性分析

## 金融问题
房地产上市公司在年报中披露的分红决策，是否与其经营活动现金流、归母净利润和流动性风险披露相一致？

该问题具有实际意义：如果公司在经营现金流为负、盈利承压或流动性风险较高时仍进行现金分红，投资者和分析师需要进一步复核其分红可持续性、资金压力和风险披露是否充分。

## 巨潮数据来源
巨潮资讯网公开披露的上市公司年度报告 PDF。

## 公告类型
年度报告。

## 示例公告
| 公司 | 代码 | 标题 | 日期 | URL |
|---|---|---|---|---|
| 万科A | 000002 | 2023年年度报告 | 2024 | 见 `data/metadata/metadata.csv` |
| 保利发展 | 600048 | 2023年年度报告 | 2024 | 见 `data/metadata/metadata.csv` |
| 招商蛇口 | 001979 | 2023年年度报告 | 2024 | 见 `data/metadata/metadata.csv` |

## 目标字段
| 字段 | 类型 | 是否必填 | 金融含义 | 证据来源 |
|---|---|---|---|---|
| `has_cash_dividend` | bool/null | 是 | 是否实施或提出现金分红 | 分红预案或利润分配章节 |
| `cash_dividend_per_10_shares` | float/null | 否 | 每10股派现金额 | 分红预案或利润分配章节 |
| `parent_net_profit` | number/null | 否 | 盈利能力和分红基础 | 主要财务指标或利润表相关章节 |
| `operating_cash_flow` | number/null | 否 | 分红现金来源和资金压力 | 主要财务指标或现金流量表章节 |
| `liquidity_risk_label` | enum | 是 | 流动性风险披露强度 | 风险因素、经营情况讨论、资金风险相关章节 |
| `consistency_score` | int/null | 是 | 分红-现金流-风险一致性筛查结果 | 由字段组合和证据规则生成 |

## 最终输出形式
- `outputs/results/final_results.csv`
- `outputs/results/extract_results.jsonl`
- `outputs/analysis/flagged_review_list.csv`
- `outputs/reports/eval_report_final.md`

## 难度档位
- 1.0
- 理由：81 份年报，单一复杂公告类型，6 个核心字段，有 section 检查、证据回填、Pydantic 校验、workflow 日志和人工评估。

## 风险与备选方案
- 风险：流动性风险 section 可能误命中非目标章节。
- 风险：财务金额单位可能不统一。
- 备选：最终分析强调正负号、风险标签和筛查清单，不直接做跨公司金额排名。
