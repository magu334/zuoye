# Evaluation Report Final

## 1. Evaluation Scope
- Downloaded PDF pool: 175 CNINFO annual reports.
- Structured workflow sample: 175 annual reports.
- Year coverage: 2020-2024.
- Industry: A-share real-estate listed companies.
- Current validated output: `outputs/results/records_validated.csv`.
- Unit-normalized output: `outputs/results/records_validated_unit_normalized.csv`.
- Quantitative scored output: `outputs/results/quantitative_scored_records.csv`.
- Final result output: `outputs/results/final_results.csv`.
- Attention review output: `outputs/analysis/attention_review_list.csv`.
- Cross-year event output: `outputs/analysis/cross_year_matching_events.csv`.

## 2. Data Quality
| Item | Result |
|---|---:|
| Metadata records | 175 |
| Downloaded PDF pool | 175 |
| Parsed text records | 175 |
| Routed sections | 525 |
| Extracted records | 175 |
| Validated records | 175 |
| Validation errors | 0 |

`data/metadata/metadata.csv` preserves `doc_id`, stock code, stock name, title, CNINFO URL, PDF URL, and local file path so each result can be traced back to its source announcement.

## 3. Parse And Section Quality
The latest full run parsed all 175 local PDFs:

```text
[parse] parsed docs=175, mineru=0, pdf_text_fallback=175
[parse_check] checked docs=175
[route] sections=525
```

The parser first looks for MinerU markdown. If it is not available, it falls back to local PDF text extraction with `pypdf`. In the current repository state, the full 175-record run used the fallback parser for all PDFs. This is reproducible and sufficient for the rule baseline, but complex tables should still be checked manually or reprocessed with MinerU when page/table fidelity is important.

Section routing covers dividend policy, financial indicators, and liquidity-risk disclosure.

## 4. Extraction Quality
The validated CSV contains these original extraction fields:

`has_cash_dividend`, `cash_dividend_per_10_shares`, `parent_net_profit`, `operating_cash_flow`, `liquidity_risk_label`, `consistency_score`.

Field completeness:
- `has_cash_dividend`: 155/175.
- `cash_dividend_per_10_shares`: 155/175.
- `parent_net_profit`: 175/175.
- `operating_cash_flow`: 175/175.
- `liquidity_risk_label`: 175/175.
- `consistency_score`: 175/175.

The 20 missing dividend records are kept as missing rather than force-filled, because annual-report dividend wording varies and should follow the null rule.

## 5. Unit Normalization Quality
The unit normalization step produced 175 valid records and 0 Pydantic validation errors.

Detected unit confidence:
- high: 175.
- medium: 0.
- low: 0.
- unknown: 0.

Detected units:
- yuan: 166.
- wan_yuan: 9.
- yi_yuan: 0.
- unknown: 0.

Both `parent_net_profit_cny` and `operating_cash_flow_cny` are complete for all 175 records.

## 6. Quantitative Scoring Quality
The two challenged fields were redesigned as follows:

- `liquidity_risk_label` is kept as a legacy screening label. The comparable result is now `liquidity_risk_score`, a 0-100 weighted risk-term frequency score computed from evidence text and extracted risk keywords. `liquidity_risk_quantile` assigns none/low/medium/high from the full-sample score distribution.
- `consistency_score` is kept as a legacy 1-3 label. The comparable result is now `attention_score`, a 0-100 weighted score combining dividend pressure 30%, cash-flow pressure 25%, profit pressure 20%, and liquidity-risk score 25%. The final score also adds 20% of `cross_year_pressure_score`.

Latest scoring result:
- Scored records: 175.
- Attention review records: 27.
- Same-company cross-year events: 342.
- Records with positive cross-year pressure: 114/175.

## 7. Result Analysis
From the 175 validated records:
- Cash dividend records: 116.
- No-cash-dividend records: 39.
- Liquidity risk labels: high 9, medium 32, low 111, none 23.
- Legacy consistency scores: score 1 = 7, score 2 = 154, score 3 = 14.
- Quantitative liquidity-risk quantiles: high 36, medium 61, low 55, none 23.
- Weighted attention levels: priority 2, watch 25, monitor 67, routine 81.
- Cross-year pressure levels: high 15, medium 35, low 64, none 61.

The weighted review list is saved to `outputs/analysis/attention_review_list.csv`.

## 8. Cross-Year Matching Analysis
The project constructs 342 same-company cross-year matching events from 175 annual reports:

- 35 companies have at least two annual-report records.
- 342 total same-company year-pair events are generated.
- 138 events are consecutive-year comparisons.
- Event rules include dividend increase while cash flow declines, dividend with negative cash flow, dividend with profit decline, risk-score jump, attention-score jump, and high cross-year pressure.

This changes the project from single-document extraction to a multi-document timeline and closed-loop screening task.

## 9. Human Evaluation Notes
Earlier manual audit found that financial numeric fields were more stable than liquidity-risk evidence routing. The main error type was section routing for risk evidence. That remains the primary manual review target for high-attention records.

Allowed human-evaluation error types:

`data_error`, `parse_error`, `section_error`, `prompt_error`, `schema_error`, `hallucination`, `normalization_error`, `workflow_error`, `human_label_unclear`.

## 10. Pipeline Stability
Latest full workflow command:

```bash
python pipeline_run.py --config configs/workflow.yaml --step all
```

Latest workflow result:

```text
[validate] valid=175, errors=0
[analysis] scored_records=175
[analysis] flagged_records=27
[analysis] cross_year_events=342
[report] summary report=outputs/reports/summary_report.md
```

Run logs:
- `outputs/logs/run_log.jsonl`
- `outputs/logs/sample_run_log.jsonl`

## 11. Main Limitations
- The current full-sample extraction is a rule baseline and should be checked manually before being used as a financial conclusion.
- PDF text fallback is reproducible but may lose table layout; MinerU can improve layout fidelity for selected high-attention PDFs.
- Liquidity-risk scores depend on routed evidence quality and require manual verification.
- Evidence page numbers are approximate because parsed text may not preserve stable original PDF page markers.

## 12. Conclusion
The current project supports a challenge-track difficulty claim: it contains 175 CNINFO annual reports, 342 same-company cross-year matching events, a complete workflow, Pydantic validation, unit normalization, quantitative risk scoring, and a weighted attention review list. The key caveat is that high-attention records should still be manually checked against evidence before being used as final financial conclusions.
