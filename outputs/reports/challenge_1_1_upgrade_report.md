# Challenge 1.1 Upgrade Report

## Upgrade Goal

The original project was positioned around 81 independent annual-report PDFs and a standard-track workflow. The upgraded project targets challenge track 1.1 by adding cross-year multi-document matching, objective risk quantification, weighted attention scoring, and a review list.

## 1.1 Difficulty Evidence

| Item | Result |
|---|---:|
| Downloaded annual-report PDFs | 175 |
| Structured/scored annual-report records | 81 |
| Companies | 37 |
| PDF year coverage | 2020-2024 |
| Structured/scored year coverage | 2021-2023 |
| Companies with at least two years | 34 |
| Same-company cross-year matching events | 54 |
| Consecutive-year matching events | 44 |

The course requirement allows challenge-track positioning through either 150+ PDFs or 50+ multi-document matching events. This project now satisfies both defensible routes: 175 downloaded CNINFO annual-report PDFs, plus 54 same-company cross-year matching events in the currently structured/scored sample.

The newly downloaded full PDF pool is tracked in `metadata_2020_2024_pool150.csv` and audited in `outputs/reports/dataset_expansion_to150.md`. The structured extraction/scoring workflow remains at 81 records until the additional PDFs are parsed by MinerU.

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

- A coarse 1-3 label cannot show how much of the concern comes from dividend pressure, cash flow, profit, or risk disclosure.

New weighted score:

| Component | Weight |
|---|---:|
| Dividend pressure | 30% |
| Cash-flow pressure | 25% |
| Profit pressure | 20% |
| Liquidity-risk score | 25% |

New fields:

- `dividend_pressure_score`
- `cashflow_pressure_score`
- `profit_pressure_score`
- `attention_score`
- `attention_level`
- `review_reason`

Output:

- `outputs/analysis/attention_review_list.csv`

## Cross-Year Event Output

The cross-year table compares same-company annual-report pairs and records changes in dividend, operating cash flow, net profit, risk score, and attention score.

Output:

- `outputs/analysis/cross_year_matching_events.csv`

Event types include:

- `dividend_up_cashflow_down`
- `dividend_with_negative_cashflow`
- `dividend_with_profit_decline`
- `risk_score_jump`
- `attention_score_jump`
- `baseline`

## Reproducible Commands

```bash
python pipeline_run.py --config configs/workflow_parsed81.yaml --step validate
python pipeline_run.py --config configs/workflow_parsed81.yaml --step analysis
python pipeline_run.py --config configs/workflow_parsed81.yaml --step all
```

Latest verification:

```text
[validate] valid=81, errors=0
[report] summary report=outputs/reports/summary_report.md
[analysis] scored_records=81
[analysis] flagged_records=4
[analysis] cross_year_events=54
```
