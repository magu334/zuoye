# 难度声明

- 申请难度：挑战档
- 系数：1.1
- 数据量：175 份房地产上市公司年报 PDF
- 结构化记录：175 条已完成解析、字段抽取、校验、单位归一化和量化评分
- 多文档匹配事件：342 组同公司跨年度匹配事件，其中 138 组为连续年度匹配
- 年度覆盖：2020-2024
- 公司数量：37 家
- 字段数量：10 个以上。除原始核心抽取字段外，新增单位标准化金额、现金流/利润比、分红压力分、利润压力分、现金流压力分、流动性风险词频分、流动性风险分位标签、基础关注分、跨年压力分、综合关注分、关注等级和跨年事件类型。

## 申请 1.1 档的理由

项目已将 PDF 样本池扩展到 175 份房地产上市公司年报，超过要求中“150+ 份 PDF”的挑战档数据量口径。当前 175 条记录已经进入完整 workflow，并生成结构化结果、校验结果、量化评分、关注清单和跨年事件。

项目不只把年报作为独立样本抽取，而是将同一公司 2020-2024 年报连接成跨年时间线。当前 175 条结构化记录覆盖 37 家公司，其中 35 家至少有两个年度记录，可构造 342 组同公司跨年度匹配事件，明显超过“50+ 组多文档匹配事件”的挑战档口径。

新增 `quantitative_attention_analysis.py` 后，`liquidity_risk_label` 不再作为唯一判断依据，而是降级为 legacy screening label。正式分析使用 `liquidity_risk_score`：从风险证据文本和抽取关键词中统计风险词频，按“流动性、融资、债务、现金流、市场下行”五类加权，再归一化到 0-100，并按全样本分布生成可比较的 `liquidity_risk_quantile`。

一致性判断也从 1-3 档主观分扩展为 0-100 的 `attention_score`。项目先用分红压力 30%、现金流压力 25%、利润压力 20%、流动性风险 25% 构建 `base_attention_score`，再把同公司跨年匹配事件转化为 `cross_year_pressure_score`。最终 `attention_score = base_attention_score + 20% * cross_year_pressure_score`，使跨年恶化信号直接影响 `outputs/analysis/attention_review_list.csv` 的排序，用于人工复核和答辩展示。

## 对照 1.1 档要求

| 要求方向 | 当前项目情况 |
|---|---|
| 150+ PDF | 已下载并处理 175 份 CNINFO 年报 PDF |
| 50+ 组多文档匹配事件 | 342 组同公司跨年度年报 pair |
| 多字段 | 原始抽取字段 + 标准化字段 + 量化评分字段 + 跨年事件字段 |
| 闭环分析 | 从年报证据抽取到单年量化评分、跨年压力评分，再到关注清单和人工复核 |
| 评分 | `liquidity_risk_score`、`base_attention_score`、`cross_year_pressure_score`、`attention_score`、`attention_level` |
| 可复现 | `python pipeline_run.py --config configs/workflow.yaml --step all` |

## 说明

当前完整运行使用 `pypdf_text_fallback` 从本地 PDF 抽取文本，因为仓库中没有完整的 MinerU markdown 批次。流程已经保留 MinerU 优先入口：如果 `data/parsed/markdown/` 中存在对应 `doc_id` 的 MinerU markdown，解析步骤会优先使用 MinerU。
