# Evaluation Report Final

## 1. Evaluation Scope
- Final workflow sample: 81 parsed CNINFO annual reports.
- Year coverage: 2021-2023.
- Industry: A-share real-estate listed companies.
- Current validated output: `outputs/results/final_results.csv`.
- Human evaluation template: `outputs/evaluation/human_eval_template_81.csv`.

## 2. Data Quality
| Item | Result |
|---|---:|
| Metadata records | 81 |
| Parsed markdown records | 81 |
| Validated records | 81 |
| Validation errors | 0 |

`data/metadata/metadata.csv` preserves `doc_id`, stock code, stock name, title, CNINFO URL, PDF URL, and local file path so each result can be traced back to its source announcement.

## 3. Section Quality
The workflow routed 243 candidate sections for 81 documents. Section routing covers dividend policy, financial indicators, and liquidity-risk disclosure. The section report is saved as `outputs/reports/section_check_report.csv`.

Known risk: liquidity-risk routing is the most fragile part. Earlier manual audit found that risk evidence can sometimes hit unrelated sections such as property tables, commitment tables, project plans, or financing fragments.

## 4. Extraction Quality
The final CSV contains six evaluated fields:

`has_cash_dividend`, `cash_dividend_per_10_shares`, `parent_net_profit`, `operating_cash_flow`, `liquidity_risk_label`, `consistency_score`.

The final 81-record workflow passed Pydantic validation with 0 validation errors. This confirms that output types and required structure are stable, but it does not by itself prove that every value is factually correct. Manual evidence checking remains necessary.

## 5. Evidence Quality
Each key result is designed to trace back to parsed sections or parsed document text. Evidence quality is evaluated separately from value correctness because a value can be right while the evidence route is wrong.

Earlier 37-report audit:
- Audited field rows: 222.
- `is_correct = FALSE`: 20 rows.
- `evidence_correct = FALSE`: 52 rows.
- Main error type: `section_error`.

Interpretation: the system is more reliable for financial numeric fields than for liquidity-risk evidence routing.

## 6. Pipeline Stability
Latest full workflow command:

```bash
python pipeline_run.py --config configs/workflow_parsed81.yaml --step all
```

Latest workflow result:

```text
[parse] parsed docs=81
[parse_check] checked docs=81
[route] sections=243
[extract] extract records=81
[validate] valid=81, errors=0
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
- High liquidity-risk label records: 13.
- Medium liquidity-risk label records: 38.
- Flagged review records: 30.

The flagged review list is saved to `outputs/analysis/flagged_review_list.csv`.

## 8. Error Types Used In Human Evaluation
Allowed values:

`data_error`, `parse_error`, `section_error`, `prompt_error`, `schema_error`, `hallucination`, `normalization_error`, `workflow_error`, `human_label_unclear`.

## 9. Main Limitations
- Amount units are not fully normalized, so direct cross-company numeric ranking is not reliable.
- Liquidity-risk labels are screening results and require manual evidence verification.
- MinerU markdown may not always preserve stable original page markers.
- The current full-sample extraction is a rule baseline; LLM extraction can be used later but should still pass the same Pydantic schema.

## 10. Conclusion
The current project satisfies the standard-difficulty evaluation requirement: it contains 81 CNINFO annual reports, a complete workflow, Pydantic validation, evidence tracing, section checking, human evaluation templates, and error analysis. The key improvement before final defense is to present one clear failure case and explain how it was detected through human evaluation.
