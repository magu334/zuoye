# Quantitative Attention Analysis

## Scope
- Annual-report records: 175
- Companies: 37
- Year coverage: 2020, 2021, 2022, 2023, 2024
- Companies with at least two years: 35
- Cross-year matching events, all same-company year pairs: 342
- Consecutive cross-year matching events: 138

## Quantitative Scoring
- `liquidity_risk_score` is a normalized 0-100 score from weighted risk-term frequency in the routed risk evidence plus extracted risk keywords.
- `liquidity_risk_quantile` is assigned from the full-sample score distribution, so high/medium/low are comparable across documents in the same run.
- `base_attention_score` is a 0-100 single-year weighted score: dividend pressure 30%, cash-flow pressure 25%, profit pressure 20%, liquidity-risk score 25%.
- `cross_year_pressure_score` is derived from same-company year-to-year signals such as risk-score jumps, base-attention jumps, dividend up while cash flow declines, and profit decline while dividends remain.
- Final `attention_score` is `base_attention_score + 20% * cross_year_pressure_score`, capped at 100, so cross-year deterioration directly affects the priority review list.
- The priority review list is sorted by `attention_score` rather than by a single subjective label.

## Liquidity Risk Quantiles
- high: 36
- medium: 61
- low: 55
- none: 23

## Attention Levels
- priority: 2
- watch: 25
- monitor: 67
- routine: 81

## Cross-Year Pressure Levels
- high: 15
- medium: 35
- low: 64
- none: 61

## Cross-Year Event Types
- baseline: 154
- dividend_with_profit_decline: 125
- dividend_with_negative_cashflow: 64
- attention_score_jump: 50
- high_cross_year_pressure: 29
- dividend_up_cashflow_down: 28
- risk_score_jump: 6

## Top Priority Records
| Rank | Stock | Name | Year | Attention | Reason |
|---:|---|---|---:|---:|---|
| 1 | 000002 | 万科A | 2021 | 80.39 | cash dividend while operating cash flow is weak or negative; liquidity-risk term frequency is high; cross-year base attention score rises; profit declines while dividend remains |
| 2 | 000002 | 万科A | 2022 | 79.75 | cash dividend while operating cash flow is weak or negative; liquidity-risk term frequency is high; cross-year base attention score rises; profit declines while dividend remains |
| 3 | 600639 | 浦东金桥 | 2022 | 73.82 | cash dividend while operating cash flow is weak or negative; cross-year base attention score rises; current-year dividend with negative operating cash flow; profit declines while dividend remains |
| 4 | 000002 | 万科A | 2024 | 72.81 | net profit is negative; liquidity-risk term frequency is high; cross-year base attention score jumps; profit turns or remains negative |
| 5 | 000069 | 华侨城A | 2022 | 72.33 | net profit is negative; cross-year liquidity-risk score jumps; cross-year base attention score jumps; profit turns or remains negative |
| 6 | 600639 | 浦东金桥 | 2023 | 71.82 | cash dividend while operating cash flow is weak or negative; cross-year base attention score jumps; dividend rises while operating cash flow declines; current-year dividend with negative operating cash flow |
| 7 | 600683 | 京投发展 | 2023 | 70.65 | net profit is negative; cross-year base attention score rises; profit turns or remains negative; dividend field is missing |
| 8 | 600683 | 京投发展 | 2024 | 69.15 | net profit is negative; cross-year base attention score jumps; profit turns or remains negative; dividend field is missing |
| 9 | 600657 | 信达地产 | 2024 | 68.84 | net profit is negative; cross-year base attention score jumps; profit turns or remains negative; dividend field is missing |
| 10 | 000573 | 粤宏远A | 2022 | 65.9 | cash dividend while operating cash flow is weak or negative; cross-year liquidity-risk score rises; cross-year base attention score jumps; current-year dividend with negative operating cash flow; profit declines while dividend remains |