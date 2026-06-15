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
- Current final sample: 81 annual reports.
- Year coverage: 2021-2023.
- Year distribution: 2021 = 10, 2022 = 34, 2023 = 37.
- Main metadata file: `data/metadata/metadata.csv`.
- Original PDFs are kept under `data/pdf/`.
- MinerU markdown outputs are kept under `data/parsed/markdown/`.

Each document is tracked by `doc_id`, stock code, stock name, announcement title, CNINFO URL, PDF URL, local PDF path, and parsed markdown path.

## Difficulty
Requested difficulty: standard track, coefficient 1.0.

Reason: the project uses 81 annual-report PDFs, 6 evaluated core fields, section routing/checking, evidence tracing, Pydantic validation, workflow logs, and human evaluation. It is a single complex announcement type rather than a simple field-extraction task.

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

Full current workflow:

```bash
python pipeline_run.py --config configs/workflow_parsed81.yaml --step all
```

If Windows cannot find `python`, activate the Anaconda environment first and then run the same commands.

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

Latest full run:

```text
[parse] parsed docs=81
[parse_check] checked docs=81
[route] sections=243
[extract] extract records=81
[validate] valid=81, errors=0
```

## Core Fields
- `has_cash_dividend`
- `cash_dividend_per_10_shares`
- `parent_net_profit`
- `operating_cash_flow`
- `liquidity_risk_label`
- `consistency_score`

Key fields are accompanied by evidence where available. Pydantic schema is defined in `src/schemas.py`.

## Main Outputs
- `outputs/results/final_results.csv`: final validated CSV output.
- `outputs/results/extract_results.jsonl`: structured extraction JSONL.
- `outputs/logs/sample_run_log.jsonl`: sample workflow log.
- `outputs/reports/eval_report_final.md`: final evaluation report.
- `outputs/reports/analysis_results_parsed81.md`: result analysis.
- `outputs/analysis/flagged_review_list.csv`: priority manual-review list.
- `outputs/evaluation/human_eval_template_81.csv`: human evaluation table for 81 reports.

## Evaluation Summary
The 81-report workflow produced 81 valid records and 0 Pydantic validation errors.

Current result analysis:
- Cash dividend records: 54.
- No-cash-dividend records: 18.
- Dividend field missing records: 9.
- Negative operating cash flow records: 26.
- Negative parent net profit records: 17.
- Cash dividend with negative operating cash flow: 19.
- High liquidity-risk label records: 13.
- Medium liquidity-risk label records: 38.
- Flagged review records: 30.

Earlier human audit on the 37-report stage found that financial field values were more stable than liquidity-risk evidence routing. The main error source was section routing for risk evidence.

## Main Limitations
- Financial amount units are not fully normalized, so cross-company amount ranking should not be made directly from raw numeric columns.
- Liquidity-risk labels are screening labels and require manual evidence review.
- Some evidence page numbers are approximate because parsed markdown page markers are not always stable.
- The baseline extraction is rule-based; LLM extraction was tested separately but is not treated as the only source of truth.

## Secret And Compliance Rules
- Main data comes from public CNINFO announcements.
- The project does not bypass login, captcha, or access restrictions.
- Real API keys must stay only in local `.env`.
- `.env.example` contains placeholders only.
