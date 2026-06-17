# Unit Normalization Report

## Summary
- Input records: 175
- Valid normalized records: 175
- Pydantic validation errors: 0

## Detected Units
- yuan: 166
- wan_yuan: 9
- yi_yuan: 0
- unknown: 0

## Unit Confidence
- high: 175
- medium: 0
- low: 0
- unknown: 0

## Output Fields
- `parent_net_profit_raw` and `operating_cash_flow_raw` preserve the original extracted values.
- `parent_net_profit_unit` and `operating_cash_flow_unit` record detected table units.
- `parent_net_profit_cny` and `operating_cash_flow_cny` convert values to yuan when a unit is detected.
- Records with `unit = unknown` keep CNY fields empty and require manual review before amount ranking.

## Important Note
This normalization is an enhanced output for analysis. It does not overwrite the original extraction result.