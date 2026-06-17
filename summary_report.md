# Summary Report

## Scope
- Validated records: 175
- Current sample: 2020-2024 annual reports covering 37 A-share real estate companies.
- Note: this is a rule-baseline workflow result and still requires human evaluation.

## Dividend
- Cash dividend records: 116
- No cash dividend records: 39

## Liquidity Risk Labels
- high: 9
- low: 111
- medium: 32
- none: 23

## Consistency Scores
- 1: 7
- 2: 154
- 3: 14

## Quantitative Liquidity Risk
- The old `liquidity_risk_label` is retained as a legacy screening field.
- Comparable analysis uses `liquidity_risk_score` and `liquidity_risk_quantile` from weighted risk-term frequency.
- high: 36
- medium: 61
- low: 55
- none: 23

## Attention Scores
- `base_attention_score` is weighted from dividend pressure, cash-flow pressure, profit pressure, and liquidity-risk score.
- Final `attention_score` adds cross-year pressure from same-company matching events, so the review list is connected to cross-year deterioration signals.
- priority: 2
- watch: 25
- monitor: 67
- routine: 81

## Cross-Year Matching
- Same-company year-pair events: 342
- Consecutive-year events: 138

## Quality Notes
- Rule baseline is intentionally simple and should be reviewed manually.
- Unit-normalized financial fields are available in `records_validated_unit_normalized.csv`.
- High-attention records should be manually verified against evidence before being used as financial conclusions.
- Evidence page numbers are approximate because parsed text may not preserve stable original PDF page markers.