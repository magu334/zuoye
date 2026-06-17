# Evaluation Report Final

## 1. Evaluation Scope
- Downloaded PDF pool: 175 CNINFO annual reports.
- Structured workflow sample: 81 parsed CNINFO annual reports.
- PDF year coverage: 2020-2024.
- Structured workflow year coverage: 2021-2023.
- Industry: A-share real-estate listed companies.
- Current validated output: `records_validated.csv` and `outputs/results/records_validated.csv`.
- Human evaluation template: `outputs/evaluation/human_eval_template_81.csv`.
- Quantitative scored output: `outputs/results/quantitative_scored_records.csv`.
- Cross-year event output: `outputs/analysis/cross_year_matching_events.csv`.

## 2. Data Quality
| Item | Result |
|---|---:|
| Metadata records | 81 |
| Downloaded PDF pool | 175 |
| Parsed markdown records | 81 |
| Validated records | 81 |
| Validation errors | 0 |

`metadata_2021_2023_pool107.csv` preserves `doc_id`, stock code, stock name, title, CNINFO URL, PDF URL, and local file path so each result can be traced back to its source announcement.

## 3. Section Quality
The workflow routed 243 candidate sections for 81 documents. Section routing covers dividend policy, financial indicators, and liquidity-risk disclosure. The section report is saved as `outputs/reports/section_check_report.csv`.

Known risk: liquidity-risk routing is the most fragile part. Earlier manual audit found that risk evidence can sometimes hit unrelated sections such as property tables, commitment tables, project plans, or financing fragments.

## 4. Extraction And Quantitative Scoring Quality
The final CSV contains six evaluated fields:

`has_cash_dividend`, `cash_dividend_per_10_shares`, `parent_net_profit`, `operating_cash_flow`, `liquidity_risk_label`, `consistency_score`.

The final 81-record workflow passed Pydantic validation with 0 validation errors. This confirms that output types and required structure are stable, but it does not by itself prove that every value is factually correct. Manual evidence checking remains necessary.

The two challenged fields were redesigned as follows:

- `liquidity_risk_label` is kept as a legacy screening label. The comparable result is now `liquidity_risk_score`, a 0-100 weighted risk-term frequency score computed from evidence text and extracted risk keywords. `liquidity_risk_quantile` then assigns none/low/medium/high from the full-sample score distribution.
- `consistency_score` is kept as a legacy 1-3 label. The comparable result is now `attention_score`, a 0-100 weighted score combining dividend pressure 30%, cash-flow pressure 25%, profit pressure 20%, and liquidity-risk score 25%.

## 5. Evidence Quality
Each key result is designed to trace back to parsed sections or parsed document text. Evidence quality is evaluated separately from value correctness because a value can be right while the evidence route is wrong.

Earlier 37-report audit:
- Audited field rows: 222.
- `is_correct = FALSE`: 20 rows.
- `evidence_correct = FALSE`: 52 rows.
- Main error type: `section_error`.

Interpretation: the system is more reliable for financial numeric fields than for liquidity-risk evidence routing.

## 6. Pipeline Stability
Latest artifact workflow command:

```bash
python pipeline_run.py --config configs/workflow_parsed81.yaml --step all
```

Latest workflow result in the current flat repository layout:

```text
[validate] valid=81, errors=0
[analysis] scored_records=81
[analysis] flagged_records=7
[analysis] cross_year_events=54
[report] summary report=outputs/reports/summary_report.md
```

Run log: `outputs/logs/sample_run_log.jsonl`.

## 7. Result Analysis
From the 81 validated records:
- Cash dividend records: 54.
- No-cash-dividend records: 18.
- Dividend field missing records: 9.
- Negative operating cash flow records: 26.
- Negative parent net profit records: 17.
- Cash dividend with negative operating cash flow: 19.
- Quantitative liquidity-risk quantiles: high 17, medium 28, low 35, none 1.
- Weighted attention levels: watch 4, monitor 28, routine 49.
- Priority/watch review records: 4.

The weighted review list is saved to `outputs/analysis/attention_review_list.csv`.

## 8. Cross-Year Matching Analysis

The project constructs 54 same-company cross-year matching events from 81 annual reports:

- 34 companies have at least two annual-report records.
- 54 total same-company year-pair events are generated.
- 44 events are consecutive-year comparisons.
- Event rules include dividend increase while cash flow declines, dividend with negative cash flow, dividend with profit decline, risk-score jump, and attention-score jump.

This changes the project from single-document extraction to a multi-document timeline and closed-loop screening task.

## 9. Error Types Used In Human Evaluation
Allowed values:

`data_error`, `parse_error`, `section_error`, `prompt_error`, `schema_error`, `hallucination`, `normalization_error`, `workflow_error`, `human_label_unclear`.

## 10. Main Limitations
- Amount units are not fully normalized, so direct cross-company numeric ranking is not reliable.
- Liquidity-risk scores depend on section routing quality and require manual evidence verification for high-attention records.
- MinerU markdown may not always preserve stable original page markers.
- The current full-sample extraction is a rule baseline; LLM extraction can be used later but should still pass the same Pydantic schema.

## 11. Conclusion
The current project supports a challenge-track difficulty claim: it contains 81 CNINFO annual reports, 54 same-company cross-year matching events, a complete workflow, Pydantic validation, evidence tracing, section checking, human evaluation templates, quantitative risk scoring, and a weighted attention review list. The key remaining caveat is that high-attention records should still be manually checked against evidence before being used as final financial conclusions.
