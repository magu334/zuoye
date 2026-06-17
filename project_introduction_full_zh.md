# 项目完整介绍

## 1. 项目名称

房地产上市公司年报中的分红政策、经营现金流与流动性风险一致性分析

## 2. 项目要解决的问题

本项目研究 A 股房地产上市公司在年度报告中披露的现金分红政策，是否与公司的经营现金流、盈利能力和流动性风险披露相一致。

核心问题可以表达为：

> 如果一家房地产公司经营现金流偏弱、利润承压或流动性风险披露较强，它是否仍然进行了现金分红？如果存在这种情况，哪些公司和年份最值得人工进一步复核？

因此，本项目不直接给出投资建议，而是生成一个“值得关注的人工复核清单”。清单中的公司年度记录，需要分析师回到年报原文继续检查其分红政策、现金流压力和风险披露是否存在不一致。

## 3. 数据来源和样本规模

数据来自巨潮资讯网公开披露的上市公司年度报告 PDF。

| 指标 | 当前结果 |
|---|---:|
| 年报 PDF 样本 | 175 份 |
| 覆盖公司 | 37 家 |
| 覆盖年份 | 2020-2024 |
| 完成结构化抽取记录 | 175 条 |
| 通过 Pydantic 校验记录 | 175 条 |
| 单位归一化记录 | 175 条 |
| 量化评分记录 | 175 条 |
| 同公司跨年匹配事件 | 342 条 |
| 最终关注清单记录 | 27 条 |

本次完整运行中，175 份 PDF 均已完成文本解析、字段抽取、校验、单位归一化、量化评分和跨年匹配。由于仓库中没有完整的 MinerU markdown 批次，解析步骤使用 `pypdf_text_fallback` 从本地 PDF 抽取文本；如果后续加入 MinerU markdown，流程会优先使用 MinerU 解析结果。

## 4. 总体工作流

```text
巨潮 metadata
-> PDF 下载
-> 数据审计
-> PDF 文本解析
-> Section Routing
-> 字段抽取
-> Pydantic 校验
-> 金额单位归一化
-> 流动性风险量化
-> 单年基础关注分
-> 同公司跨年压力分
-> 最终关注分
-> 值得关注清单 / 跨年事件表 / 报告
```

可复现命令：

```bash
python pipeline_run.py --config configs/workflow.yaml --step all
```

最新完整运行结果：

```text
[parse] parsed docs=175, mineru=0, pdf_text_fallback=175
[parse_check] checked docs=175
[route] sections=525
[extract] extract records=175
[validate] valid=175, errors=0
[analysis] scored_records=175
[analysis] flagged_records=27
[analysis] cross_year_events=342
```

## 5. 核心字段体系

项目字段可以分成六层：基础追溯字段、原始抽取字段、单位归一化字段、流动性风险量化字段、单年关注评分字段、跨年压力与最终清单字段。

### 5.1 基础追溯字段

这些字段保证每一条结果都能回到原始公告。

| 字段 | 含义 | 来源 |
|---|---|---|
| `doc_id` | 巨潮公告 ID，也是全流程主键 | metadata |
| `stock_code` | 股票代码 | metadata |
| `stock_name` | 公司名称 | metadata |
| `report_year` | 年报年份 | metadata |
| `title` | 公告标题 | metadata / parsed record |
| `cninfo_url` | 巨潮公告页面 URL | metadata |
| `pdf_url` | PDF 下载 URL | metadata |
| `local_pdf_path` | 本地 PDF 路径 | metadata |

其中 `doc_id` 是最重要的主键，它连接 metadata、PDF、解析文本、section、抽取结果、校验结果、评分结果和人工复核清单。

### 5.2 原始抽取字段

这些字段来自 `outputs/results/records_validated.csv`。

| 字段 | 含义 | 用途 |
|---|---|---|
| `has_cash_dividend` | 是否存在现金分红 | 判断公司是否进行现金分红 |
| `cash_dividend_per_10_shares` | 每 10 股现金分红金额 | 衡量分红强度 |
| `parent_net_profit` | 归母净利润原始抽取值 | 衡量盈利能力 |
| `operating_cash_flow` | 经营活动现金流量净额原始抽取值 | 衡量现金流质量 |
| `liquidity_risk_label` | 旧版流动性风险标签 | 兼容旧结果，不作为最终排序核心 |
| `risk_keywords` | 命中的风险关键词 | 供风险词频评分使用 |
| `consistency_score` | 旧版一致性筛查分 | 兼容旧结果，不作为最终排序核心 |
| `consistency_reason` | 旧版一致性理由 | 保留解释信息 |

本项目被质疑的两个旧字段是：

- `liquidity_risk_label`：如果每次单独判断 high/medium/low，不同批次之间可能不可比较。
- `consistency_score`：1-3 档过于粗糙，不能说明关注分来自分红、现金流、利润还是风险披露。

所以后续新增了可比较的量化字段。

### 5.3 单位归一化字段

年报中的金额单位可能是元、万元或亿元。为了避免不同公司和年份之间量纲不一致，项目增加单位归一化步骤，输出 `outputs/results/records_validated_unit_normalized.csv`。

| 字段 | 含义 |
|---|---|
| `parent_net_profit_raw` | 归母净利润原始数值 |
| `parent_net_profit_unit` | 识别出的利润金额单位 |
| `parent_net_profit_cny` | 统一换算成人民币元的归母净利润 |
| `operating_cash_flow_raw` | 经营现金流原始数值 |
| `operating_cash_flow_unit` | 识别出的现金流金额单位 |
| `operating_cash_flow_cny` | 统一换算成人民币元的经营现金流 |
| `unit_source` | 单位识别依据文本 |
| `unit_confidence` | 单位识别置信度 |
| `unit_note` | 单位识别说明 |

当前结果中：

- `parent_net_profit_cny` 完整率：175/175。
- `operating_cash_flow_cny` 完整率：175/175。
- `unit_confidence = high`：175/175。

### 5.4 流动性风险量化字段

旧字段 `liquidity_risk_label` 只给出文本标签，不够可比。新方法把年报风险披露中的关键词进行分组计数和加权，得到 0-100 的量化分。

风险词大致分为五类：

| 风险词组 | 示例含义 | 权重逻辑 |
|---|---|---|
| 流动性 | 流动性、资金压力、资金安全、资金链 | 权重最高 |
| 融资 | 融资、借款、贷款、授信、债券、有息负债 | 反映融资环境 |
| 债务 | 债务、偿债、负债、资产负债率、短期借款 | 反映债务压力 |
| 现金流 | 现金流、经营活动现金流、回款 | 反映现金流压力 |
| 市场 | 销售回款、去化、市场下行、行业下行、需求下行、调控 | 反映行业和销售压力 |

相关字段：

| 字段 | 含义 |
|---|---|
| `liquidity_term_hits` | 风险词原始命中次数 |
| `liquidity_weighted_hits` | 按词组权重加权后的命中分 |
| `liquidity_risk_score` | 将加权命中分归一化到 0-100 |
| `liquidity_risk_quantile` | 根据全样本分布生成 none/low/medium/high |
| `legacy_liquidity_risk_label` | 旧版风险标签，保留用于对照 |

分位结果：

- high：36 条。
- medium：61 条。
- low：55 条。
- none：23 条。

这样做的好处是：风险不再只依赖单次 high/medium/low 判断，而是使用词频、权重和全样本分布，增强不同公司和不同年份之间的可比性。

### 5.5 单年关注评分字段

项目先为每一条公司年度记录生成一个单年基础关注分 `base_attention_score`。

基础关注分由四部分组成：

| 指标 | 字段 | 权重 | 解释 |
|---|---|---:|---|
| 分红压力 | `dividend_pressure_score` | 30% | 现金分红越高，关注度越高 |
| 现金流压力 | `cashflow_pressure_score` | 25% | 经营现金流为负，或现金流对利润覆盖弱时提高关注 |
| 利润压力 | `profit_pressure_score` | 20% | 利润为负或偏低时提高关注 |
| 流动性风险 | `liquidity_risk_score` | 25% | 风险词频评分越高，关注度越高 |

计算公式：

```text
base_attention_score =
  30% * dividend_pressure_score
  + 25% * cashflow_pressure_score
  + 20% * profit_pressure_score
  + 25% * liquidity_risk_score
```

各分项的含义：

| 字段 | 含义 |
|---|---|
| `dividend_pressure_score` | 由是否分红和每 10 股分红金额转换而来 |
| `cashflow_pressure_score` | 由经营现金流正负、现金流/利润覆盖比转换而来 |
| `profit_pressure_score` | 由归母净利润正负和规模转换而来 |
| `ocf_to_profit_ratio` | 经营现金流对归母净利润的覆盖比 |
| `base_attention_score` | 不考虑跨年因素时的单年关注分 |

### 5.6 跨年压力字段

为了满足 1.1 档“多文档匹配、时间线、闭环分析”的要求，项目把同一公司不同年份的年报记录进行两两匹配，形成 `outputs/analysis/cross_year_matching_events.csv`。

跨年事件表核心字段：

| 字段 | 含义 |
|---|---|
| `event_id` | 跨年事件 ID |
| `stock_code` | 股票代码 |
| `stock_name` | 公司名称 |
| `from_year` | 起始年份 |
| `to_year` | 目标年份 |
| `year_gap` | 两个年份间隔 |
| `is_consecutive_pair` | 是否连续年度 |
| `from_doc_id` | 起始年报 doc_id |
| `to_doc_id` | 目标年报 doc_id |
| `dividend_delta` | 分红变化 |
| `ocf_delta_cny` | 经营现金流变化 |
| `profit_delta_cny` | 归母净利润变化 |
| `risk_score_delta` | 流动性风险分变化 |
| `base_attention_score_delta` | 基础关注分变化 |
| `final_attention_score_delta` | 最终关注分变化 |
| `cross_year_pressure_score` | 跨年压力分 |
| `event_type` | 跨年事件类型 |
| `review_reason` | 事件解释 |

跨年事件类型包括：

- `dividend_up_cashflow_down`：分红上升但经营现金流下降。
- `dividend_with_negative_cashflow`：目标年度分红且经营现金流为负。
- `dividend_with_profit_decline`：利润下降但仍分红。
- `risk_score_jump`：流动性风险分明显跳升。
- `attention_score_jump`：基础关注分明显跳升。
- `high_cross_year_pressure`：跨年压力较高。
- `baseline`：普通跨年对照事件。

当前跨年事件结果：

- 跨年匹配事件：342 条。
- 连续年度事件：138 条。
- 有正跨年压力输入的记录：114/175。

### 5.7 最终关注字段

跨年压力最终会进入关注分，而不是单独放在另一张表里。

最终公式：

```text
attention_score = base_attention_score + 20% * cross_year_pressure_score
```

如果分数超过 100，则封顶为 100。

最终关注等级：

| 字段 | 规则 |
|---|---|
| `priority` | `attention_score >= 75` |
| `watch` | `attention_score >= 55` 且小于 75 |
| `monitor` | `attention_score >= 35` 且小于 55 |
| `routine` | `attention_score < 35` |

最终字段：

| 字段 | 含义 |
|---|---|
| `cross_year_pressure_score` | 该记录受到的最大跨年恶化压力 |
| `cross_year_pressure_level` | none/low/medium/high |
| `cross_year_reason` | 跨年压力来源 |
| `attention_score` | 最终关注分 |
| `attention_level` | 最终关注等级 |
| `review_reason` | 进入清单或常规复核的原因 |

当前关注等级分布：

- priority：2 条。
- watch：25 条。
- monitor：67 条。
- routine：81 条。

## 6. 最终关注清单的生成步骤

最终清单文件为：

```text
outputs/analysis/attention_review_list.csv
```

它的生成不是直接根据一个主观标签筛选，而是经过以下步骤。

### Step 1：读取单位归一化后的 175 条记录

输入文件：

```text
outputs/results/records_validated_unit_normalized.csv
```

这一步确保利润和现金流字段已经统一为人民币元：

- `parent_net_profit_cny`
- `operating_cash_flow_cny`

### Step 2：读取抽取上下文和风险证据

输入文件：

```text
outputs/results/extract_results.jsonl
```

系统从里面读取：

- 旧版 `liquidity_risk_label`
- 风险关键词 `risk_keywords`
- 风险证据文本 `risk_evidence_text`

这些内容用于后续风险词频评分。

### Step 3：计算流动性风险量化分

对风险证据文本和关键词进行计数：

```text
liquidity_term_hits
liquidity_weighted_hits
liquidity_risk_score
liquidity_risk_quantile
```

其中 `liquidity_risk_score` 是 0-100 标准化分数，`liquidity_risk_quantile` 是基于 175 条全样本分布生成的分位标签。

### Step 4：计算三个财务压力分

对每条记录计算：

```text
dividend_pressure_score
cashflow_pressure_score
profit_pressure_score
```

逻辑是：

- 有现金分红，且分红金额更高，则分红压力更高。
- 经营现金流为负，或现金流对利润覆盖弱，则现金流压力更高。
- 归母净利润为负或偏低，则利润压力更高。

### Step 5：计算单年基础关注分

使用权重公式：

```text
base_attention_score =
  0.30 * dividend_pressure_score
  + 0.25 * cashflow_pressure_score
  + 0.20 * profit_pressure_score
  + 0.25 * liquidity_risk_score
```

这个分数只看公司某一年的情况，不看跨年变化。

### Step 6：生成同公司跨年事件

系统按 `stock_code` 分组，把同一公司的不同年份记录两两匹配。

例如同一家公司有 2020、2021、2022、2023、2024 五年记录，就会形成多个年度 pair：

```text
2020 -> 2021
2020 -> 2022
2020 -> 2023
2020 -> 2024
2021 -> 2022
...
```

每个 pair 会比较：

- 分红是否上升。
- 经营现金流是否下降。
- 利润是否下降或转负。
- 流动性风险分是否跳升。
- 基础关注分是否跳升。

输出为：

```text
outputs/analysis/cross_year_matching_events.csv
```

### Step 7：把跨年事件转化为跨年压力分

每条目标年度记录会得到一个 `cross_year_pressure_score`。

加分逻辑包括：

- 流动性风险分跳升：增加跨年压力。
- 基础关注分跳升：增加跨年压力。
- 分红上升但经营现金流下降：增加跨年压力。
- 目标年度分红且经营现金流为负：增加跨年压力。
- 利润下降但仍分红：增加跨年压力。
- 利润转负或持续为负：增加跨年压力。
- 如果是连续年度 pair，跨年压力会更受重视。

这样，跨年匹配因素会直接进入最后清单，而不是和清单分开。

### Step 8：计算最终关注分

公式：

```text
attention_score = base_attention_score + 0.20 * cross_year_pressure_score
```

含义：

- `base_attention_score` 反映单年分红、现金流、利润和风险披露。
- `cross_year_pressure_score` 反映同公司不同年份之间是否出现恶化。
- 最终 `attention_score` 同时考虑单年情况和跨年变化。

### Step 9：生成关注等级

按最终分数生成：

```text
priority / watch / monitor / routine
```

规则：

- `priority`：75 分及以上。
- `watch`：55 分及以上、75 分以下。
- `monitor`：35 分及以上、55 分以下。
- `routine`：35 分以下。

### Step 10：筛选最终清单

最终关注清单筛选：

```text
attention_level in {"priority", "watch"}
```

也就是说：

- priority 记录一定进入清单。
- watch 记录也进入清单。
- monitor 和 routine 记录保留在最终结果表中，但不进入优先人工复核清单。

当前结果：

- `priority`：2 条。
- `watch`：25 条。
- 最终清单合计：27 条。

### Step 11：生成进入清单的理由

每条清单记录都有 `review_reason`。

理由可能包括：

- 现金分红但经营现金流较弱或为负。
- 归母净利润为负。
- 流动性风险词频较高。
- 跨年基础关注分上升。
- 跨年流动性风险分跳升。
- 分红上升但经营现金流下降。
- 利润下降但仍分红。
- 分红字段缺失，需要人工确认。

因此最终清单不只是给一个分数，还能解释为什么这条记录值得人工复核。

## 7. 主要输出文件

| 文件 | 内容 |
|---|---|
| `outputs/results/records_validated.csv` | 175 条原始抽取并通过 schema 校验的记录 |
| `outputs/results/records_validated_unit_normalized.csv` | 175 条单位归一化后的记录 |
| `outputs/results/quantitative_scored_records.csv` | 175 条量化评分记录 |
| `outputs/results/final_results.csv` | 最终 175 条结果表 |
| `outputs/analysis/attention_review_list.csv` | 27 条值得关注的人工复核清单 |
| `outputs/analysis/cross_year_matching_events.csv` | 342 条同公司跨年事件 |
| `outputs/reports/quantitative_attention_report.md` | 量化模型和结果报告 |
| `outputs/reports/full_pdf_extraction_report.md` | 175 份 PDF 完整提取状态 |
| `outputs/reports/eval_report_final.md` | 最终评估报告 |

## 8. 项目相对旧版本的关键提升

### 8.1 样本量提升

旧版本约 80 份 PDF，当前扩展到 175 份 PDF，并且 175 条记录全部进入结构化流程。

### 8.2 风险标签从主观分类变成可比较分数

旧版：

```text
liquidity_risk_label = high / medium / low
```

新版：

```text
liquidity_term_hits
liquidity_weighted_hits
liquidity_risk_score
liquidity_risk_quantile
```

### 8.3 一致性判断从 1-3 档变成加权评分

旧版：

```text
consistency_score = 1 / 2 / 3
```

新版：

```text
base_attention_score
cross_year_pressure_score
attention_score
attention_level
review_reason
```

### 8.4 跨年匹配真正影响最终清单

项目不是单独生成跨年事件表就结束，而是把跨年恶化信号转化为 `cross_year_pressure_score`，再加入最终 `attention_score`。这样最终清单和跨年匹配因素是连在一起的。

## 9. 可以在答辩中强调的结论

1. 项目满足 1.1 档数据规模：175 份 PDF。
2. 项目满足 1.1 档复杂任务：342 条同公司跨年匹配事件。
3. 旧的 `liquidity_risk_label` 已经被更客观的词频量化分替代。
4. 旧的 `consistency_score` 已经被加权的 `attention_score` 替代。
5. 最终清单不是主观挑选，而是由财务字段、风险词频、跨年变化共同计算得到。
6. 清单输出的是人工复核优先级，不是直接投资结论，符合课程对 evidence 和 human-in-the-loop 的要求。

## 10. 一句话总结

本项目把巨潮年报 PDF 转化为可追溯、可校验、可比较的结构化指标，并通过“单年压力评分 + 同公司跨年压力评分”生成 27 条值得人工重点复核的房地产上市公司年度记录。
