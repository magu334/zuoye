# Human Evaluation Audit Summary

## Summary
- Total audited field rows: 222
- Value incorrect rows: 20
- Evidence incorrect rows: 52
- Corrected records output: outputs\results\records_validated_audited.csv
- Copied audit table: outputs\evaluation\human_eval_audit_report.csv

## Error Type Counts
- parse_error: 10
- prompt_error: 2
- section_error: 40
- workflow_error: 12

## Affected Companies
- 000006, 深振业A: 2 field rows
- 000069, 华侨城A: 2 field rows
- 000514, 渝开发: 2 field rows
- 000573, 粤宏远A: 2 field rows
- 000736, 中交地产: 2 field rows
- 000797, 中国武夷: 2 field rows
- 000897, 津滨发展: 2 field rows
- 001979, 招商蛇口: 2 field rows
- 002146, 荣盛发展: 2 field rows
- 002244, 滨江集团: 2 field rows
- 600094, 大名城: 4 field rows
- 600383, 金地集团: 2 field rows
- 600533, 栖霞建设: 3 field rows
- 600639, 浦东金桥: 6 field rows
- 600648, 外高桥: 6 field rows
- 600649, 城投控股: 2 field rows
- 600657, 信达地产: 2 field rows
- 600658, 电子城: 2 field rows
- 600663, 陆家嘴: 2 field rows
- 600665, 天地源: 4 field rows
- 600675, 中华企业: 2 field rows
- 600683, 京投发展: 3 field rows
- 600743, 华远地产: 4 field rows
- 600895, 张江高科: 2 field rows

## Interpretation
- is_correct checks whether the extracted field value is correct.
- evidence_correct checks whether the source evidence supports the field value.
- records_validated_audited.csv uses gold_value when available and keeps audit status columns for traceability.
- Financial values include raw value, unit code, and CNY-normalized value.
- source_file_problem rows should not be used as fully reliable pipeline evidence until PDF/Markdown binding is fixed.
