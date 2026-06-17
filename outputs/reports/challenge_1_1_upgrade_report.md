# Challenge 1.1 Upgrade Report

## Upgrade Goal
The original project was close to a standard-track workflow. The upgraded project targets challenge track 1.1 by expanding the sample to 175 annual-report PDFs, processing the full sample through a reproducible workflow, adding objective risk quantification, adding same-company cross-year matching, and generating a weighted review list.

## 1.1 Difficulty Evidence

| Item | Result |
|---|---:|
| Downloaded annual-report PDFs | 175 |
| Structured/scored annual-report records | 175 |
| Companies | 37 |
| Year coverage | 2020-2024 |
| Companies with at least two years | 35 |
| Same-company cross-year matching events | 342 |
| Consecutive-year matching events | 138 |
| Attention review records | 27 |

The course requirement describes challenge-track positioning as 150+ PDFs or 50+ multi-document matching events. This project satisfies both routes: it has 175 CNINFO annual-report PDFs and 342 same-company cross-year matching events.

The full PDF pool is tracked in `data/metadata/metadata.csv` and `metadata_2020_2024_pool150.csv`. Original PDF files are intentionally not uploaded to Git in this branch because the user requested not to upload annual-report PDF originals.

## Full-Sample Processing Status
Latest full workflow:

```bash
python pipeline_run.py --config configs/workflow.yaml --step all
```

Latest verification:

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
[analysis] report=outputs/reports/quantitative_attention_report.md
[report] summary report=outputs/reports/summary_report.md
```

The parser uses MinerU markdown when available and falls back to `pypdf` text extraction when MinerU markdown is absent. The latest full run used fallback text for all 175 PDFs.

## Liquidity Risk Revision
Old field:

- `liquidity_risk_label`: none/low/medium/high from each individual extraction.

Problem:

- A label assigned independently for each document can be hard to compare across documents or years.

New comparable fields:

- `liquidity_term_hits`: raw risk-term hit count.
- `liquidity_weighted_hits`: weighted hit count across liquidity, financing, debt, cash-flow, and market-pressure terms.
- `liquidity_risk_score`: normalized 0-100 full-sample score.
- `liquidity_risk_quantile`: none/low/medium/high assigned by full-sample score distribution.

Output:

- `outputs/results/quantitative_scored_records.csv`

## Consistency Score Revision
Old field:

- `consistency_score`: 1/2/3 screening score.

Problem:

- A coarse 1-3 label cannot show how much of the concern comes from dividend pressure, cash flow, profit, risk disclosure, or cross-year deterioration.

New weighted score:

| Component | Weight |
|---|---:|
| Dividend pressure | 30% |
| Cash-flow pressure | 25% |
| Profit pressure | 20% |
| Liquidity-risk score | 25% |

The final score then adds cross-year pressure:

```text
attention_score = base_attention_score + 20% * cross_year_pressure_score
```

New fields:

- `dividend_pressure_score`
- `cashflow_pressure_score`
- `profit_pressure_score`
- `base_attention_score`
- `cross_year_pressure_score`
- `attention_score`
- `attention_level`
- `review_reason`

Output:

- `outputs/analysis/attention_review_list.csv`

## Cross-Year Event Output
The cross-year table compares same-company annual-report pairs and records changes in dividend, operating cash flow, net profit, risk score, base attention score, final attention score, and cross-year pressure score.

Output:

- `outputs/analysis/cross_year_matching_events.csv`

Event types include:

- `dividend_up_cashflow_down`
- `dividend_with_negative_cashflow`
- `dividend_with_profit_decline`
- `risk_score_jump`
- `attention_score_jump`
- `high_cross_year_pressure`
- `baseline`

## Conclusion
The upgraded project reaches the 1.1 challenge-track argument on both data scale and task complexity: 175 PDFs, 175 structured scored records, 342 cross-year events, comparable liquidity-risk scoring, weighted attention scoring, and a final review list connected to cross-year deterioration signals.
