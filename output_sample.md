# Output Sample

## Target Output

- CSV + JSONL + analysis report + cross-year event table + attention review list.
- Every annual-report record keeps `doc_id` and can be traced back to metadata, PDF, parsed text, routed section, and evidence.
- Same-company annual reports are linked into cross-year matching events.

## Scored Record Example

| doc_id | stock_code | stock_name | report_year | liquidity_risk_score | liquidity_risk_quantile | base_attention_score | cross_year_pressure_score | attention_score | attention_level |
|---|---|---|---:|---:|---|---:|---:|---:|---|
| 1216273938 | 000002 | 万科A | 2022 | 100.0 | high | 74.5 | 0.0 | 74.5 | watch |

## Cross-Year Event Example

| event_id | stock_code | from_year | to_year | dividend_delta | ocf_delta_cny | risk_score_delta | cross_year_pressure_score | event_type |
|---|---|---:|---:|---:|---:|---:|---:|---|
| 600639_2022_2023 | 600639 | 2022 | 2023 | positive value | negative value | positive value | 60.0 | dividend_up_cashflow_down |

## Key Fields

| Field | Type | Meaning |
|---|---|---|
| `liquidity_term_hits` | int | Raw hit count for risk terms |
| `liquidity_weighted_hits` | float | Weighted hit count by risk category |
| `liquidity_risk_score` | float | 0-100 normalized comparable risk score |
| `liquidity_risk_quantile` | enum | none/low/medium/high from full-sample distribution |
| `dividend_pressure_score` | float | Dividend pressure component |
| `cashflow_pressure_score` | float | Operating-cash-flow pressure component |
| `profit_pressure_score` | float | Profit pressure component |
| `base_attention_score` | float | Single-year weighted review score |
| `cross_year_pressure_score` | float | Same-company cross-year deterioration pressure |
| `cross_year_pressure_level` | enum | none/low/medium/high from cross-year pressure |
| `attention_score` | float | Final review score: base score plus 20% of cross-year pressure |
| `attention_level` | enum | routine/monitor/watch/priority |
| `review_reason` | string | Why the record enters or avoids review |
