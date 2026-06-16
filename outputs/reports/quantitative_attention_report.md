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
- `attention_score` is a 0-100 weighted score: dividend pressure 30%, cash-flow pressure 25%, profit pressure 20%, liquidity-risk score 25%.
- The priority review list is sorted by `attention_score` rather than by a single subjective label.

## Liquidity Risk Quantiles
- high: 17
- medium: 28
- low: 35
- none: 1

## Attention Levels
- priority: 0
- watch: 4
- monitor: 28
- routine: 49

## Cross-Year Event Types
- baseline: 27
- dividend_with_profit_decline: 18
- dividend_with_negative_cashflow: 10
- attention_score_jump: 4
- dividend_up_cashflow_down: 3

## Top Priority Records
| Rank | Stock | Name | Year | Attention | Reason |
|---:|---|---|---:|---:|---|
| 1 | 000002 | 万科A | 2022 | 74.5 | cash dividend while operating cash flow is weak or negative; liquidity-risk term frequency is high |
| 2 | 600639 | 浦东金桥 | 2022 | 59.75 | cash dividend while operating cash flow is weak or negative |
| 3 | 600683 | 京投发展 | 2023 | 58.53 | net profit is negative; dividend field is missing |
| 4 | 600639 | 浦东金桥 | 2023 | 57.0 | cash dividend while operating cash flow is weak or negative |