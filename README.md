# Real Estate Dividend, Cash Flow, and Liquidity Risk Project

## Project Title
房地产上市公司年报分红政策、经营现金流与流动性风险一致性分析

## Financial Question
This project asks whether A-share real-estate listed companies' dividend decisions are consistent with their operating cash flow, profitability pressure, and liquidity-risk disclosure in annual reports.

The practical output is an analyst review ledger. It does not directly produce investment advice; instead, it flags companies that deserve manual review, such as firms paying cash dividends while operating cash flow or net profit is negative, or while liquidity-risk disclosure is high.

## Data Source And Scope
- Source: public CNINFO annual-report announcements.
- Announcement type: annual reports.
- Industry scope: A-share real-estate listed companies.
- Downloaded PDF pool: 175 annual reports.
- Structured parsed/scored sample: 81 annual reports.
- PDF year coverage: 2020-2024.
- Parsed/scored year coverage: 2021-2023.
- Expanded metadata file: `metadata_2020_2024_pool150.csv`.
- Existing parsed metadata/result files remain available for the 81-record structured workflow.
- Some course-template paths still use `data/metadata/`, `data/pdf/`, and `data/parsed/`; the runner has a fallback layer so current flat files can still be used.
- The final reproducible 81-record checks use the saved extraction and normalized result artifacts.

Each document is tracked by `doc_id`, stock code, stock name, announcement title, CNINFO URL, PDF URL, local PDF path, and parsed markdown path.

## Difficulty
Requested difficulty: challenge track, coefficient 1.1.

Reason: the project now has a 175-PDF CNINFO annual-report pool, exceeding the 150+ PDF challenge-track threshold. The current structured workflow additionally treats the parsed 81 annual reports as a cross-year matching dataset: 34 companies have at least two years of parsed/scored records, producing 54 same-company cross-year matching events. The project also adds timeline comparison, weighted scoring, and a priority review list.

## Directory Structure
- `configs/`: workflow, model, crawl, and section-routing configuration.
- `data/metadata/`: CNINFO metadata CSV files.
- `data/pdf/`: downloaded CNINFO PDF files.
- `data/parsed/`: parsed documents, markdown files, and routed sections.
- `prompts/`: prompt templates.
- `src/`: parsing, routing, extraction, validation, reporting, and workflow scripts.
- `outputs/logs/`: run logs and validation errors.
- `outputs/results/`: extraction and validated result files.
- `outputs/reports/`: dataset, section, evaluation, and analysis reports.
- `outputs/evaluation/`: human evaluation templates and audit records.
- `outputs/analysis/`: result analysis tables.
- `work/`: local temporary working files. Do not treat this as final submission material.

## Setup
```bash
python -m pip install -r requirements.txt
```

Create a local `.env` from `.env.example` and fill real keys locally only. Do not commit `.env`.

## Minimal Check
If `python` is available in your current environment:

```bash
python pipeline_run.py --help
```

Current artifact workflow:

```bash
python pipeline_run.py --config configs/workflow_parsed81.yaml --step all
```

For the current flat repository layout, `--step all` runs enabled reproducible steps only: validate, report, and quantitative analysis for the existing 81 structured records. Expanding the structured workflow from 81 to the full 175-PDF pool requires sending the newly downloaded PDFs through MinerU and then rerunning parse/route/extract.

## Workflow
```text
metadata
  -> audit
  -> parse
  -> parse_check
  -> route
  -> extract
  -> validate
  -> report
```

Latest artifact run:

```text
[validate] valid=81, errors=0
[report] summary report=outputs/reports/summary_report.md
[analysis] scored_records=81
[analysis] flagged_records=4
[analysis] cross_year_events=54
```

## Core Fields
- `has_cash_dividend`
- `cash_dividend_per_10_shares`
- `parent_net_profit`
- `operating_cash_flow`
- `liquidity_risk_label` legacy screening label
- `consistency_score` legacy 1-3 screening score
- `parent_net_profit_cny`
- `operating_cash_flow_cny`
- `ocf_to_profit_ratio`
- `dividend_pressure_score`
- `profit_pressure_score`
- `cashflow_pressure_score`
- `liquidity_risk_score`
- `liquidity_risk_quantile`
- `attention_score`
- `attention_level`

Key fields are accompanied by evidence where available. Pydantic schema is defined in `src/schemas.py`.

## Main Outputs
- `records_validated.csv` and `outputs/results/records_validated.csv`: validated CSV output.
- `extract_results.jsonl`: structured extraction JSONL.
- `outputs/results/quantitative_scored_records.csv`: 81 records with comparable risk and attention scores.
- `outputs/logs/sample_run_log.jsonl`: sample workflow log.
- `outputs/reports/eval_report_final.md`: final evaluation report.
- `outputs/reports/quantitative_attention_report.md`: quantitative scoring and cross-year matching report.
- `outputs/reports/analysis_results_parsed81.md`: result analysis.
- `outputs/analysis/attention_review_list.csv`: priority manual-review list sorted by weighted attention score.
- `outputs/analysis/cross_year_matching_events.csv`: 54 same-company cross-year matching events.
- `outputs/evaluation/human_eval_template_81.csv`: human evaluation table for 81 reports.

## Evaluation Summary
The 81-report workflow produced 81 valid records and 0 Pydantic validation errors.

Current result analysis:
- Downloaded PDF pool: 175.
- PDF year distribution: 2020 = 33, 2021 = 35, 2022 = 35, 2023 = 37, 2024 = 35.
- Cash dividend records: 54.
- No-cash-dividend records: 18.
- Dividend field missing records: 9.
- Negative operating cash flow records: 26.
- Negative parent net profit records: 17.
- Cash dividend with negative operating cash flow: 19.
- Quantitative liquidity-risk quantiles: high 17, medium 28, low 35, none 1.
- Weighted attention levels: watch 4, monitor 28, routine 49.
- Cross-year matching events: 54 total same-company year pairs, including 44 consecutive year pairs.

`liquidity_risk_label` and `consistency_score` are retained for backward compatibility. The final comparison uses `liquidity_risk_score`, `liquidity_risk_quantile`, `attention_score`, and `attention_level`, all generated by `quantitative_attention_analysis.py`.

Earlier human audit on the 37-report stage found that financial field values were more stable than liquidity-risk evidence routing. The main error source was section routing for risk evidence.

## Main Limitations
- 175 PDFs have been downloaded, but the structure-scored workflow currently covers 81 parsed reports. The remaining PDFs need MinerU parsing before field extraction.
- Liquidity-risk scores are screening scores and require manual evidence review.
- Some evidence page numbers are approximate because parsed markdown page markers are not always stable.
- The baseline extraction is rule-based; LLM extraction was tested separately but is not treated as the only source of truth.

## Secret And Compliance Rules
- Main data comes from public CNINFO announcements.
- The project does not bypass login, captcha, or access restrictions.
- Real API keys must stay only in local `.env`.
- `.env.example` contains placeholders only.
