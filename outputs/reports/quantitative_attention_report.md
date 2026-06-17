# Quantitative Attention Analysis

## Scope
- Annual-report records: 81
- Companies: 37
- Year coverage: 2021, 2022, 2023
- Companies with at least two years: 34
- Cross-year matching events, all same-company year pairs: 54
- Consecutive cross-year matching events: 44

## Quantitative Scoring
- `liquidity_risk_score` is a normalized 0-100 score from weighted risk-term frequency in the routed risk evidence plus extracted risk keywords.
- `liquidity_risk_quantile` is assigned from the full-sample score distribution, so high/medium/low are comparable across documents in the same run.
- `base_attention_score` is a 0-100 single-year weighted score: dividend pressure 30%, cash-flow pressure 25%, profit pressure 20%, liquidity-risk score 25%.
- `cross_year_pressure_score` is derived from same-company year-to-year signals such as risk-score jumps, base-attention jumps, dividend up while cash flow declines, and profit decline while dividends remain.
- Final `attention_score` is `base_attention_score + 20% * cross_year_pressure_score`, capped at 100, so cross-year deterioration directly affects the priority review list.
- The priority review list is sorted by `attention_score` rather than by a single subjective label.

## Liquidity Risk Quantiles
- high: 17
- medium: 28
- low: 35
- none: 1

## Attention Levels
- priority: 0
- watch: 7
- monitor: 34
- routine: 40

## Cross-Year Pressure Levels
- high: 4
- medium: 9
- low: 19
- none: 49

## Cross-Year Event Types
- baseline: 27
- dividend_with_profit_decline: 18
- dividend_with_negative_cashflow: 10
- attention_score_jump: 4
- dividend_up_cashflow_down: 3
- high_cross_year_pressure: 1

## Top Priority Records
| Rank | Stock | Name | Year | Attention | Reason |
|---:|---|---|---:|---:|---|
| 1 | 000002 | 万科A | 2022 | 74.5 | cash dividend while operating cash flow is weak or negative; liquidity-risk term frequency is high |
| 2 | 600639 | 浦东金桥 | 2023 | 69.0 | cash dividend while operating cash flow is weak or negative; dividend rises while operating cash flow declines; current-year dividend with negative operating cash flow |
| 3 | 600683 | 京投发展 | 2023 | 67.53 | net profit is negative; cross-year base attention score rises; profit turns or remains negative; dividend field is missing |
| 4 | 600533 | 栖霞建设 | 2023 | 62.69 | net profit is negative; cross-year base attention score rises; profit turns or remains negative; dividend field is missing |
| 5 | 600639 | 浦东金桥 | 2022 | 59.75 | cash dividend while operating cash flow is weak or negative |
| 6 | 600848 | 上海临港 | 2023 | 58.24 | cash dividend while operating cash flow is weak or negative; cross-year liquidity-risk score rises; cross-year base attention score rises; current-year dividend with negative operating cash flow |
| 7 | 000965 | 天保基建 | 2023 | 55.08 | cash dividend while operating cash flow is weak or negative; cross-year base attention score rises; current-year dividend with negative operating cash flow; profit declines while dividend remains |