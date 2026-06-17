# Real Estate Dividend, Cash Flow, and Liquidity Risk Project

## Project Title
房地产上市公司年报中的分红政策、经营现金流与流动性风险一致性分析

## Financial Question
This project asks whether A-share real-estate listed companies' cash-dividend decisions are consistent with operating cash flow, profitability pressure, and liquidity-risk disclosure in annual reports.

The output is an analyst review list. It is not investment advice. It flags company-year records that deserve manual review, especially cases where dividends coexist with weak operating cash flow, negative profit, or stronger liquidity-risk disclosure.

## Data Source And Scope
- Source: public CNINFO annual-report announcements.
- Announcement type: annual reports.
- Industry scope: A-share real-estate listed companies.
- PDF pool: 175 annual reports.
- Structured extraction/scoring records: 175 annual reports.
- Companies: 37.
- Year coverage: 2020-2024.
- Download failures: 0.
- Metadata: `data/metadata/metadata.csv` and `metadata_2020_2024_pool150.csv`.

Each document is tracked by `doc_id`, stock code, stock name, report year, announcement title, CNINFO URL, PDF URL, local PDF path, parser name, and parsed text path.

## Difficulty
Requested difficulty: challenge track, coefficient 1.1.

The project exceeds the 150+ PDF threshold with 175 CNINFO annual reports. It also builds same-company cross-year comparisons from the structured records: 35 companies have at least two years, producing 342 same-company year-pair events, including 138 consecutive-year events. The workflow adds weighted scoring, cross-year pressure, and a final review list.

## Directory Structure
- `configs/`: workflow, model, crawl, and section-routing configuration.
- `data/metadata/`: CNINFO metadata CSV files.
- `data/parsed/`: parsed text samples and routed section samples.
- `prompts/`: prompt templates.
- `src/`: shared workflow helpers.
- Root scripts: audit, parse, route, extract, validate, normalize, analyze, and report.
- `outputs/results/`: extraction, validation, normalized, scored, and final result files.
- `outputs/analysis/`: attention review list and cross-year events.
- `outputs/reports/`: dataset, unit normalization, quantitative, evaluation, and summary reports.
- `outputs/evaluation/`: human evaluation templates and audit records.

Original PDFs are kept locally under `data/pdf/` but are intentionally ignored by Git because they are large. The repository includes metadata and scripts so the PDF pool can be reproduced.

## Setup
```bash
python -m pip install -r requirements.txt
```

Create a local `.env` from `.env.example` if using API-based extraction. Keep real keys local only. Do not commit `.env`.

## Reproducible Commands
Check the runner:

```bash
python pipeline_run.py --help
```

Run the full current workflow:

```bash
python pipeline_run.py --config configs/workflow.yaml --step all
```

The full workflow parses the 175 local PDFs. If MinerU markdown exists for a `doc_id`, `parse_docs.py` uses it; otherwise it uses the local `pypdf_text_fallback`. The latest full run used the fallback for all 175 PDFs because no full MinerU markdown batch was present in the repository.

## Workflow
```text
metadata
  -> audit dataset
  -> parse PDF text
  -> parse check
  -> route dividend / financial / liquidity-risk sections
  -> extract core fields
  -> Pydantic validation
  -> unit normalization
  -> quantitative attention analysis
  -> summary report
```

Latest full run:

```text
[audit] dataset report=outputs/reports/dataset_check_report.md
[parse] parsed docs=175, mineru=0, pdf_text_fallback=175
[parse_check] checked docs=175
[route] sections=525
[extract] extract records=175
[validate] valid=175, errors=0
[analysis] scored_records=175
[analysis] flagged_records=27
[analysis] cross_year_events=342
[report] summary report=outputs/reports/summary_report.md
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
- `liquidity_term_hits`
- `liquidity_weighted_hits`
- `liquidity_risk_score`
- `liquidity_risk_quantile`
- `base_attention_score`
- `cross_year_pressure_score`
- `attention_score`
- `attention_level`

Pydantic schema is defined in `schemas.py`.

## Main Outputs
- `outputs/results/extract_results.jsonl`: structured extraction JSONL.
- `outputs/results/records_validated.csv`: 175 Pydantic-validated records.
- `outputs/results/records_validated_unit_normalized.csv`: 175 unit-normalized records.
- `outputs/results/quantitative_scored_records.csv`: 175 comparable scoring records.
- `outputs/results/final_results.csv`: final 175-record result table.
- `outputs/analysis/attention_review_list.csv`: 27 records sorted by final `attention_score`.
- `outputs/analysis/cross_year_matching_events.csv`: 342 same-company cross-year events.
- `outputs/reports/quantitative_attention_report.md`: scoring and cross-year matching report.
- `outputs/reports/eval_report_final.md`: final evaluation report.
- `final_report.md`: final project report.
- `proposal_zh.md`: Chinese proposal.
- `ppt_project_steps_zh.md`: PPT-ready project flow.

## Evaluation Summary
- Metadata records: 175.
- Parsed records: 175.
- Routed sections: 525.
- Validated records: 175.
- Validation errors: 0.
- Parent net profit completeness: 175/175.
- Operating cash flow completeness: 175/175.
- Unit normalization high-confidence records: 175/175.
- Attention levels: priority 2, watch 25, monitor 67, routine 81.
- Cross-year pressure levels: high 15, medium 35, low 64, none 61.

`liquidity_risk_label` and `consistency_score` are retained for backward compatibility. The final comparison uses `liquidity_risk_score`, `liquidity_risk_quantile`, `base_attention_score`, `cross_year_pressure_score`, `attention_score`, and `attention_level`.

## Main Limitations
- The current 175-record extraction is a rule baseline based on parsed PDF text. High-attention records still need manual evidence review.
- PDF text extraction can be weaker than layout-aware parsing for complex tables; MinerU can be added later for stronger page/table fidelity.
- Evidence page markers are approximate because parsed text may not preserve stable original PDF page markers.
- The attention score is a screening score for review prioritization, not a final financial-risk conclusion.

## Secret And Compliance Rules
- Main data comes from public CNINFO announcements.
- The project does not bypass login, captcha, or access restrictions.
- Real API keys must stay only in local `.env`.
- `.env.example` contains placeholders only.
