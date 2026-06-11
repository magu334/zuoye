# Workflow Design

## 项目目标

本项目研究房地产上市公司年报中的分红政策、经营现金流与流动性风险披露是否一致。项目从巨潮资讯网年报 PDF 出发，经 MinerU Markdown 解析、section routing、规则 baseline 抽取、Pydantic 校验和汇总报告，形成可追溯的结构化结果。

## 总流程图

Collect -> Audit -> Parse -> Inspect/Route -> Extract -> Validate -> Aggregate -> Report

## 节点表

| 节点 | 输入 | 输出 | 成功标准 | 失败处理 | 日志 |
|---|---|---|---|---|---|
| Collect | 巨潮公告查询结果、PDF URL | `data/metadata/metadata.csv`, `data/pdf/*.pdf` | metadata 字段完整，PDF 可打开 | 记录下载失败和错误原因 | `outputs/logs/run_log.jsonl` |
| Audit | metadata + PDF 文件 | `outputs/reports/dataset_check_report.md` | 无重复 doc_id，PDF 文件存在，标题属于年报 | 标记缺失、重复、疑似无关记录 | `outputs/logs/run_log.jsonl` |
| Parse | `data/pdf/*.pdf`, MinerU Markdown | `data/parsed/markdown/*.md`, `data/parsed/parsed_docs.jsonl` | 每个 doc_id 有 markdown_path 和 pages | 解析为空则失败，不静默替代 | `outputs/logs/run_log.jsonl` |
| Route | `parsed_docs.jsonl`, `configs/section_rules.yaml` | `data/parsed/sections.jsonl`, `outputs/reports/section_check_report.csv` | 每份文档至少定位分红、财务或风险候选段 | 记录 `not_found`、`too_short`、`wrong_section` | `outputs/logs/run_log.jsonl` |
| Extract | `sections.jsonl` | `outputs/results/extract_results.jsonl` | 字段含 evidence_text，不确定输出 null | 抽取失败写错误记录 | `outputs/logs/run_log.jsonl` |
| Validate | `extract_results.jsonl`, `src/schemas.py` | `outputs/results/records_validated.csv`, `outputs/logs/validation_errors.jsonl` | Pydantic 校验通过或错误可追溯 | 校验失败写入 errors，不混入最终 CSV | `outputs/logs/run_log.jsonl` |
| Report | validated CSV | `outputs/reports/summary_report.md` | 汇总样本量、字段缺失、风险和一致性结果 | 缺少输入则报告失败 | `outputs/logs/run_log.jsonl` |

## 人工检查点

- 抽查 PDF 是否来自巨潮详情页和 metadata。
- 抽查 MinerU markdown 是否有目标章节、是否乱码。
- 抽查 section 是否命中正文，而不是目录或释义。
- 抽查 `evidence_text` 是否真的来自原文。
- 抽查分红字段是否误抓上一年度分红执行情况。
- 抽查经营现金流金额单位是否需要标准化。
- 抽查流动性风险标签是否把行业风险和公司自身压力混淆。

## 配置文件

- `configs/workflow.yaml`
- `configs/section_rules.yaml`

## 最小运行命令

```bash
python src/pipeline_run.py --config configs/workflow.yaml --step all --limit 3
```
