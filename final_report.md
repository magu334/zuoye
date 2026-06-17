# 最终报告

## 1. 项目题目
房地产上市公司年报中的分红政策、经营现金流与流动性风险一致性分析

## 2. 研究问题
本项目研究 A 股房地产上市公司的现金分红决策，是否与其经营现金流表现、归母净利润水平和流动性风险披露相一致。

如果公司在经营现金流偏弱、利润承压或流动性风险披露较强的情况下仍进行现金分红，该公司年度记录会被列入人工复核清单。项目输出不是投资建议，而是一个可追溯、可解释、可排序的筛查结果。

## 3. 数据来源与样本
数据来源为巨潮资讯网公开披露的上市公司年度报告 PDF。

| 指标 | 当前结果 |
|---|---:|
| PDF 样本池 | 175 份 |
| 公司数量 | 37 家 |
| 年份范围 | 2020-2024 |
| 完成结构化提取和评分记录 | 175 条 |
| 同公司跨年匹配事件 | 342 条 |
| 连续年度匹配事件 | 138 条 |
| 下载失败记录 | 0 条 |

关键数据文件：
- `data/metadata/metadata.csv`
- `metadata_2020_2024_pool150.csv`
- `data/parsed/parsed_docs_sample.jsonl`
- `data/parsed/sections_sample.jsonl`
- `outputs/results/final_results.csv`

说明：175 份 PDF 已全部完成本地文本抽取、字段抽取、校验、单位标准化、量化评分和跨年事件生成。当前完整解析使用 `pypdf_text_fallback`；如果后续有 MinerU markdown，流程会优先使用 MinerU 解析文本。

## 4. Workflow

```text
metadata -> PDF 下载 -> 数据审计 -> PDF 文本解析
-> Section Routing -> 字段抽取 -> Pydantic 校验
-> 金额单位归一化 -> 流动性风险量化
-> 综合关注评分 -> 关注清单 / 跨年事件
```

可复现命令：

```bash
python pipeline_run.py --config configs/workflow.yaml --step all
```

最新运行结果：

```text
[parse] parsed docs=175, mineru=0, pdf_text_fallback=175
[route] sections=525
[extract] extract records=175
[validate] valid=175, errors=0
[analysis] scored_records=175
[analysis] flagged_records=27
[analysis] cross_year_events=342
```

## 5. 核心字段

| 字段 | 含义 |
|---|---|
| `has_cash_dividend` | 是否存在现金分红 |
| `cash_dividend_per_10_shares` | 每 10 股现金分红金额 |
| `parent_net_profit_cny` | 归母净利润，统一为人民币元 |
| `operating_cash_flow_cny` | 经营活动现金流量净额，统一为人民币元 |
| `ocf_to_profit_ratio` | 经营现金流对利润覆盖比 |
| `liquidity_term_hits` | 流动性风险词原始命中次数 |
| `liquidity_weighted_hits` | 按词类加权后的风险词命中 |
| `liquidity_risk_score` | 0-100 流动性风险量化分 |
| `liquidity_risk_quantile` | 基于全样本分布的风险分位标签 |
| `base_attention_score` | 单年度基础关注分 |
| `cross_year_pressure_score` | 同公司跨年恶化压力分 |
| `attention_score` | 最终综合关注分 |
| `attention_level` | 关注等级 |
| `review_reason` | 进入关注清单的原因 |

## 6. 针对旧版本问题的改进

### 6.1 流动性风险标签
旧字段 `liquidity_risk_label` 只表示 none/low/medium/high，容易被质疑不同批次之间不可比较。

本版本保留旧字段作为兼容信息，同时新增：
- `liquidity_term_hits`
- `liquidity_weighted_hits`
- `liquidity_risk_score`
- `liquidity_risk_quantile`

新分数基于风险关键词命中频次和权重，并按全样本分布生成分位标签，因此比单次文本判断更客观、可比较。

### 6.2 一致性筛查分数
旧字段 `consistency_score` 是 1-3 档粗粒度判断。

本版本新增 `base_attention_score` 和最终 `attention_score`。基础关注分由四类单年指标加权构成：

| 指标 | 权重 |
|---|---:|
| 分红压力 | 30% |
| 经营现金流压力 | 25% |
| 利润压力 | 20% |
| 流动性风险披露 | 25% |

随后将同公司跨年匹配事件转化为 `cross_year_pressure_score`。若出现流动性风险分跳升、基础关注分跳升、分红上升但现金流下降、利润下降但仍分红等信号，则对目标年度加跨年压力分。

最终公式：

```text
attention_score = base_attention_score + 20% * cross_year_pressure_score
```

这样，跨年匹配不再只是单独展示，而是直接影响值得关注清单排序。

## 7. 当前结果

- 175 条记录完成结构化校验，Pydantic 校验错误为 0。
- 175 条记录完成单位标准化，单位识别高置信记录为 175。
- 175 条记录完成量化评分。
- 27 条记录进入优先关注清单。
- 342 条同公司跨年匹配事件已生成。
- 114 条记录存在大于 0 的跨年压力输入。

量化分布：
- 流动性风险分位：high 36, medium 61, low 55, none 23。
- 关注等级：priority 2, watch 25, monitor 67, routine 81。
- 跨年压力等级：high 15, medium 35, low 64, none 61。

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
2. 175 条结构化样本均已完成抽取、校验、单位归一化和评分。
3. 项目不是单纯总结公告，而是完成字段抽取、证据追溯、单位归一化、量化评分和清单生成。
4. 形成 342 条同公司跨年匹配事件。
5. 对流动性风险和一致性筛查进行了量化改造，增强可比性。
6. 输出可以直接用于人工复核的关注清单。

## 9. 局限性
- 当前 175 条完整结果是基于规则和 PDF 文本抽取的 baseline，高关注记录仍需要人工核对原文证据。
- PDF 文本抽取对复杂表格的保真度弱于版面感知解析，后续可补充 MinerU 结果进一步增强表格和页码质量。
- 量化评分用于筛查和排序，不应被视为最终风险结论。
- 人工评估样本还可以继续扩大，以校准抽取准确率和关注清单命中质量。

## 10. 后续改进
1. 对高关注记录做人工逐条 evidence 复核。
2. 用 MinerU 或更强表格解析器替换部分复杂 PDF 的 fallback 文本。
3. 扩大人工标注样本，评估字段抽取准确率。
4. 继续优化风险关键词权重和行业词表。
5. 在 PPT 展示中选取一家公司，完整展示从 PDF 到最终关注分数的链路。
