# Summary Report

## Scope
- Validated records: 81
- Current sample: 2021-2023 annual reports covering 37 A-share real estate companies.
- Note: this is a rule-baseline workflow result and still requires human evaluation.

## Dividend
- Cash dividend records: 54
- No cash dividend records: 18

## Liquidity Risk Labels
- high: 13
- low: 29
- medium: 38
- missing: 1

## Consistency Scores
- 1: 10
- 2: 56
- 3: 14
- missing: 1

## Quantitative Liquidity Risk
- The old `liquidity_risk_label` is retained as a legacy screening field.
- Comparable analysis uses `liquidity_risk_score` and `liquidity_risk_quantile` from weighted risk-term frequency.
- high: 17
- medium: 28
- low: 35
- none: 1

## Attention Scores
- `attention_score` is weighted from dividend pressure, cash-flow pressure, profit pressure, and liquidity-risk score.
- watch: 4
- monitor: 28
- routine: 49

## Cross-Year Matching
- Same-company year-pair events: 54
- Consecutive-year events: 44

## Quality Notes
- Rule baseline is intentionally simple and should be reviewed manually.
- Unit-normalized financial fields are available in `records_validated_unit_normalized.csv`.
- High-attention records should be manually verified against evidence before being used as financial conclusions.
- Evidence page numbers are approximate because the current MinerU markdown keeps text but not stable original PDF page markers.