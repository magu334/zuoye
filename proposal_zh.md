# 中文 Proposal

## 项目题目

房地产上市公司年报中的分红政策、经营现金流与流动性风险一致性分析。

## 一、研究背景

房地产行业具有资金密集、融资依赖较高、项目周期长等特点。上市公司年报中通常会同时披露利润分配方案、经营活动现金流量、债务与融资环境、销售回款压力等信息。

如果一家房地产公司在经营现金流偏弱、利润承压或流动性风险披露较强的情况下仍进行现金分红，投资者和分析师可能需要进一步复核其分红政策是否稳健。因此，本项目希望用公开年报文本和结构化财务字段，生成一个可追溯、可解释的关注清单。

## 二、金融问题

本项目关注的问题是：

> 房地产上市公司的现金分红决策，是否与其经营现金流表现、归母净利润水平和流动性风险披露相一致？

进一步拆分为三个子问题：

1. 公司是否披露现金分红方案，现金分红强度如何？
2. 公司当年的经营活动现金流量净额是否能够覆盖归母净利润？
3. 年报中的流动性风险、融资压力、债务压力、销售回款压力等披露是否较强？

最终输出是一个“值得关注的人工复核清单”，而不是直接给出投资结论。

## 三、数据来源与样本范围

数据来源为巨潮资讯网公开披露的上市公司年度报告 PDF。

当前数据情况：

| 项目 | 当前数量 |
|---|---:|
| PDF 样本池 | 175 份 |
| 公司数量 | 37 家 |
| 年份范围 | 2020-2024 |
| 当前已解析并评分记录 | 81 条 |
| 同公司跨年匹配事件 | 54 条 |
| 下载失败记录 | 0 条 |

数据文件：

- `data/metadata/metadata.csv`
- `data/pdf/`
- `data/parsed/parsed_docs_sample.jsonl`
- `outputs/results/final_results.csv`

说明：项目已将 PDF 样本池扩展到 175 份。当前 81 条记录已经完成解析、字段抽取、校验和量化评分，后续可继续对剩余 PDF 做 MinerU 解析并纳入同一流程。

## 四、目标字段

| 字段 | 含义 |
|---|---|
| `doc_id` | 巨潮公告 ID |
| `stock_code` | 股票代码 |
| `stock_name` | 公司名称 |
| `report_year` | 报告年份 |
| `has_cash_dividend` | 是否有现金分红 |
| `cash_dividend_per_10_shares` | 每 10 股现金分红 |
| `parent_net_profit_cny` | 归母净利润，统一为人民币元 |
| `operating_cash_flow_cny` | 经营活动现金流量净额，统一为人民币元 |
| `ocf_to_profit_ratio` | 经营现金流对利润覆盖比 |
| `liquidity_risk_score` | 基于风险词频和权重的流动性风险评分 |
| `liquidity_risk_quantile` | 基于样本分布的流动性风险分位标签 |
| `attention_score` | 综合关注分数 |
| `attention_level` | 关注等级 |
| `review_reason` | 进入关注清单的原因 |

## 五、技术路线

项目 workflow 如下：

```text
metadata -> PDF 下载 -> 数据审计 -> MinerU 解析 -> Section Routing
-> 字段抽取 -> Pydantic 校验 -> 金额单位归一化
-> 流动性风险量化 -> 综合关注评分 -> 关注清单 / 跨年事件
```

关键方法：

1. 使用巨潮公开公告信息构建标准 `metadata.csv`。
2. 使用 MinerU 将 PDF 年报解析为可检索文本。
3. 通过 section routing 定位分红、财务指标和风险披露章节。
4. 抽取现金分红、归母净利润、经营现金流和风险关键词。
5. 使用 Pydantic Schema 校验结构化结果。
6. 将金额统一归一化到人民币元。
7. 用词频和权重构建 `liquidity_risk_score`，替代单次主观 high/medium/low 判断。
8. 用分红压力、现金流压力、利润压力和流动性风险披露构建 `attention_score`。
9. 生成同公司跨年匹配事件和人工复核清单。

## 六、核心改进点

### 1. 样本量扩展

原项目只有约 80 份 PDF，样本量偏小。当前已扩展到 175 份房地产上市公司年报 PDF，覆盖 2020-2024 年。

### 2. 流动性风险标签量化

旧字段 `liquidity_risk_label` 是 high/medium/low 文本标签，容易被质疑不同批次抽取不可比。

本项目新增：

- `liquidity_term_hits`
- `liquidity_weighted_hits`
- `liquidity_risk_score`
- `liquidity_risk_quantile`

其逻辑是根据年报风险披露中的关键词命中频次和权重计算分数，再放到全样本分布中比较，从而增强客观性和可比性。

### 3. 一致性评分量化

旧字段 `consistency_score` 解释性较弱。

本项目新增 `base_attention_score` 和最终 `attention_score`。其中 `base_attention_score` 由四类单年指标加权构成：

| 指标 | 权重 |
|---|---:|
| 分红压力 | 30% |
| 经营现金流压力 | 25% |
| 利润压力 | 20% |
| 流动性风险披露 | 25% |

项目再根据同公司跨年匹配结果生成 `cross_year_pressure_score`，例如风险评分跳升、基础关注分跳升、分红上升但现金流下降、利润下降但仍分红等。最终 `attention_score = base_attention_score + 20% * cross_year_pressure_score`，用于输出 `attention_level` 和 `review_reason`，形成值得关注的人工复核清单。

### 4. 跨年匹配

项目对同一公司的不同年份记录进行匹配，生成 54 条跨年事件，用于观察风险披露和现金流表现的变化。跨年事件不只是单独展示，还会转化为跨年压力分并进入最终关注清单排序。这比单年、单文档抽取更符合 1.1 档的复杂度要求。

## 七、预期输出

| 输出 | 路径 |
|---|---|
| 最终结果表 | `outputs/results/final_results.csv` |
| 量化评分表 | `outputs/results/quantitative_scored_records.csv` |
| 关注清单 | `outputs/analysis/attention_review_list.csv` |
| 跨年事件 | `outputs/analysis/cross_year_matching_events.csv` |
| 汇总报告 | `outputs/reports/summary_report.md` |
| 量化模型说明 | `outputs/reports/quantitative_attention_report.md` |
| 1.1 档升级说明 | `outputs/reports/challenge_1_1_upgrade_report.md` |
| 最终评估报告 | `outputs/reports/eval_report_final.md` |

## 八、难度档位说明

本项目目标为 1.1 档。

理由：

1. 数据规模从约 80 份 PDF 扩展到 175 份 PDF。
2. 不只做单文档摘要，而是做字段抽取、校验、归一化、评分和清单生成。
3. 使用 section routing 和 evidence 思路降低全文抽取噪声。
4. 使用 Pydantic Schema 保证结构化输出可复现。
5. 对同公司跨年记录进行匹配，形成 54 条跨年事件。
6. 将主观标签改造为词频/权重/分位数评分，增强可比性。
7. 生成可操作的人工复核清单，具有明确金融分析意义。

## 九、风险与应对

| 风险 | 应对 |
|---|---|
| 年报 PDF 较大，GitHub 上传体积偏高 | 保留样本 PDF、完整 metadata 和下载脚本 |
| MinerU 解析可能遗漏表格或页码 | 保留解析样本和人工检查报告 |
| 金额单位不一致 | 增加 CNY 归一化字段 |
| 风险标签主观性强 | 使用词频、权重和分位数评分 |
| 自动抽取可能误判 | 输出关注清单，保留人工复核环节 |

## 十、一句话总结

本项目通过巨潮年报、结构化抽取、风险词频量化和跨年匹配，将房地产上市公司的分红、现金流和流动性风险披露转化为可比较的关注分数，并生成面向人工复核的重点清单。
